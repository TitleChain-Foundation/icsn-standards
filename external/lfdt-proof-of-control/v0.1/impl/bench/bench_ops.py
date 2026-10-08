#!/usr/bin/env python3
"""Operational experiments: scaling at depth, the anchoring interval, batch
signing, and what retention costs.

E2  Scaling to 50,000 steps -- does the bounded summary stay flat, or does it
    quietly degrade at depth?
E3  The anchoring interval Delta, measured instead of asserted: what it costs
    to publish, and how many actions sit inside the undetectable window.
E4  Batch signing. Signing is 87% of a step, so the obvious question is why not
    sign one root per N actions. This measures what you buy and what you pay.
E5  Storage over a retention period, for a realistic fleet, classical vs
    post-quantum.
"""
from __future__ import annotations

import json
import statistics as st
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from poc import (Action, AttestingEnvironment, EvidenceStore, Gateway, Grant,
                 PathSummary, PolicyEngine, TransparencyLog, canonical, sha256)


def stack(path_aware=True, anchor=None):
    g = Grant("user:alice", frozenset({"db.read", "http.post"}),
              frozenset({"customers", "api.partner.com"}),
              max_spend=1e9, max_sensitivity_egress="restricted")
    ae = AttestingEnvironment(PolicyEngine(g, path_aware), anchor=anchor,
                              anchor_interval_s=1e9)
    s = EvidenceStore()
    return ae, s, Gateway(ae, s)


# ---------------------------------------------------------------- E2
def e2_scaling_deep():
    print("E2  scaling to 50,000 steps")
    lengths = [10, 100, 1_000, 5_000, 10_000, 50_000]
    rows = []
    for L in lengths:
        ae, store, gw = stack()
        acts = [Action("db.read", "customers", {"row": i % 97}) for i in range(L)]
        for a in acts[:-1]:
            gw.submit(a)
        samples = []
        for _ in range(300):
            t0 = time.perf_counter_ns()
            ae.policy.evaluate(acts[-1], ae.phi)
            samples.append((time.perf_counter_ns() - t0) / 1000)
        # naive: re-fold the whole history (fewer reps at depth)
        reps = 20 if L <= 10_000 else 5
        hist = [(a, "ALLOW") for a in acts[:-1]]
        naive = []
        for _ in range(reps):
            t0 = time.perf_counter_ns()
            phi = PathSummary()
            for a, v in hist:
                phi = phi.fold(a, v)
            ae.policy.evaluate(acts[-1], phi)
            naive.append((time.perf_counter_ns() - t0) / 1000)
        row = {"path_length": L,
               "bounded_us": round(st.median(samples), 3),
               "naive_us": round(st.median(naive), 2)}
        rows.append(row)
        print(f"    {L:>6}: bounded {row['bounded_us']:>7.3f} us   "
              f"naive {row['naive_us']:>12.2f} us")
    return rows


# ---------------------------------------------------------------- E3
def e3_anchoring():
    """Publishing cost against Delta, and the exposure window it leaves."""
    print("\nE3  anchoring interval")
    ae, store, gw = stack(anchor=TransparencyLog())
    # cost of one publication: sign the root and append
    sk = Ed25519PrivateKey.generate()
    samples = []
    for _ in range(2000):
        t0 = time.perf_counter_ns()
        sk.sign(canonical({"root": "a" * 64, "index": 12345}))
        samples.append((time.perf_counter_ns() - t0) / 1000)
    pub_us = st.median(samples)

    # measured single-core action rate from the gateway
    a = Action("db.read", "customers", {"row": 1})
    for _ in range(200):
        gw.submit(a)
    t0 = time.perf_counter_ns()
    for _ in range(2000):
        gw.submit(a)
    per_action_us = (time.perf_counter_ns() - t0) / 1000 / 2000
    rate = 1e6 / per_action_us

    print(f"    one publication: {pub_us:.1f} us; action rate {rate:,.0f}/s")
    print(f"    {'Delta':>8}{'exposure (actions)':>22}{'publish overhead':>20}")
    rows = []
    for delta_s in (0.001, 0.01, 0.1, 1.0, 10.0, 60.0, 3600.0):
        exposure = rate * delta_s
        overhead = pub_us / (delta_s * 1e6)          # fraction of wall time
        rows.append({"delta_s": delta_s,
                     "exposure_actions": round(exposure),
                     "publish_overhead_fraction": round(overhead, 9)})
        label = (f"{delta_s}s" if delta_s < 60 else
                 f"{int(delta_s/60)}min" if delta_s < 3600 else "1h")
        print(f"    {label:>8}{exposure:>22,.0f}{overhead:>19.2e}")
    return {"publication_us": round(pub_us, 2),
            "action_rate_per_s": round(rate),
            "rows": rows}


# ---------------------------------------------------------------- E4
def e4_batch_signing():
    """Sign one root per N actions instead of one signature per action."""
    print("\nE4  batch signing")
    sk = Ed25519PrivateKey.generate()
    payload = canonical({"poc": "evidence", "step": 1, "verdict": "ALLOW"})

    def per_action_cost(batch):
        # each action: canonicalize + hash + chain; each batch: one signature
        t0 = time.perf_counter_ns()
        reps = 2000
        for i in range(reps):
            d = sha256(payload)
            sha256((d + d + "ALLOW").encode())
            if (i + 1) % batch == 0:
                sk.sign(payload)
        return (time.perf_counter_ns() - t0) / 1000 / reps

    rows = []
    print(f"    {'batch':>7}{'us/action':>12}{'steps/s':>12}{'worst-case delay':>19}")
    for b in (1, 2, 4, 8, 16, 32, 64, 128):
        us = per_action_cost(b)
        rate = 1e6 / us
        # an action is only covered by a signature once its batch closes
        delay_us = us * (b - 1)
        rows.append({"batch": b, "us_per_action": round(us, 2),
                     "steps_per_s": round(rate),
                     "worst_case_unsigned_delay_us": round(delay_us, 1)})
        print(f"    {b:>7}{us:>12.2f}{rate:>12,.0f}{delay_us:>18.1f}u")
    speedup = rows[0]["us_per_action"] / rows[-1]["us_per_action"]
    print(f"    batching 128 is {speedup:.1f}x cheaper per action")
    return {"rows": rows, "speedup_128": round(speedup, 2)}


# ---------------------------------------------------------------- E5
def e5_retention():
    """What a fleet's evidence costs to keep, classical vs post-quantum."""
    print("\nE5  storage over a retention period")
    # taken from bench_pq.json rather than restated, so the two experiments
    # cannot drift apart
    pq = json.loads((Path(__file__).resolve().parent.parent / "results" /
                     "bench_pq.json").read_text())
    by_scheme = {r["scheme"].split(" (")[0].replace("Hybrid Ed25519 + ML-DSA-44",
                                                    "Hybrid"): r
                 for r in pq["storage"]}
    RECORD = {k: by_scheme[k]["record_bytes"] for k in
              ("Ed25519", "ML-DSA-44", "Hybrid")}
    RECORD_CBOR = {k: by_scheme[k]["record_bytes_cbor"] for k in
                   ("Ed25519", "ML-DSA-44", "Hybrid")}
    agents, actions_per_agent_day = 1000, 100
    per_day = agents * actions_per_agent_day
    rows = []
    print(f"    fleet: {agents:,} agents x {actions_per_agent_day} actions/day "
          f"= {per_day:,} actions/day")
    print(f"    {'years':>7}" + "".join(f"{k:>14}" for k in RECORD))
    for years in (1, 3, 5, 7, 10):
        actions = per_day * 365 * years
        row = {"years": years, "actions": actions}
        for k, size in RECORD.items():
            row[k] = round(actions * size / 1e12, 3)     # TB
            row[k + "_cbor"] = round(actions * RECORD_CBOR[k] / 1e12, 3)
        rows.append(row)
        print(f"    {years:>7}" + "".join(f"{row[k]:>12.2f} TB" for k in RECORD))
    print(f"    same evidence in the CWT/CBOR rendering, 7 years: "
          f"{rows[3]['ML-DSA-44_cbor']:.2f} TB post-quantum "
          f"(vs {rows[3]['Ed25519']:.2f} TB for classical JSON)")
    return {"fleet": {"agents": agents,
                      "actions_per_agent_day": actions_per_agent_day},
            "record_bytes": RECORD, "record_bytes_cbor": RECORD_CBOR,
            "rows": rows}


def main():
    print("Operational experiments\n")
    out = {"e2_scaling_deep": e2_scaling_deep(),
           "e3_anchoring": e3_anchoring(),
           "e4_batch_signing": e4_batch_signing(),
           "e5_retention": e5_retention()}
    p = Path(__file__).resolve().parent.parent / "results" / "ops.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwritten to {p}")


if __name__ == "__main__":
    main()
