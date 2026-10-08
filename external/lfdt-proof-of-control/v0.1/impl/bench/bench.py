#!/usr/bin/env python3
"""Benchmarks for the Proof-of-Control reference implementation.

B1 Per-step latency, broken out by component (canonicalization, policy
   evaluation, signing, chain append, store append) with percentiles.
B2 Scaling with path length: validates the O(1)-per-step claim of the bounded
   path summary against a naive full-path baseline.
B3 Verification cost: independent verifier throughput over chain length.
B4 Utility cost of path-aware authorization: false-rejection rate on benign
   workloads, and the effect of a declassification point.

Latencies EXCLUDE enclave transition costs (no TEE in this environment); see
impl/README.md for what that means for the numbers.
"""
from __future__ import annotations

import json
import platform
import statistics as st
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from poc import (Action, AttestingEnvironment, EvidenceStore, Gateway, Grant,
                 PathSummary, PolicyEngine, TransparencyLog, Verifier,
                 canonical, sha256)

N_WARMUP, N_ITERS = 200, 5000


def pct(xs, p):
    xs = sorted(xs)
    k = max(0, min(len(xs) - 1, int(round((p / 100) * (len(xs) - 1)))))
    return xs[k]


def summarize(name, samples_us):
    return {
        "component": name,
        "n": len(samples_us),
        "mean_us": round(st.mean(samples_us), 2),
        "median_us": round(st.median(samples_us), 2),
        "p95_us": round(pct(samples_us, 95), 2),
        "p99_us": round(pct(samples_us, 99), 2),
        "max_us": round(max(samples_us), 2),
    }


def make_stack(path_aware=True):
    grant = Grant("user:alice",
                  frozenset({"db.read", "http.post", "pay.send"}),
                  frozenset({"customers", "api.partner.com", "api.bank.com"}),
                  max_spend=1e9, max_sensitivity_egress="restricted")
    policy = PolicyEngine(grant, path_aware=path_aware)
    ae = AttestingEnvironment(policy, anchor=None)
    return ae, EvidenceStore(), policy


# ---------------------------------------------------------------- B1
def b1_latency():
    ae, store, policy = make_stack()
    gw = Gateway(ae, store)
    action = Action("db.read", "customers", {"row": 42},
                    classification="internal")

    for _ in range(N_WARMUP):
        gw.submit(action)

    t_canon, t_policy, t_sign, t_chain, t_store, t_total = [], [], [], [], [], []
    sk = Ed25519PrivateKey.generate()

    for i in range(N_ITERS):
        # component-level timing on representative payloads
        snap = {"agent_id": gw.agent_id,
                "action": json.loads(action.canonical_form()),
                "path_summary": ae.phi.digest(), "step_index": i}
        t0 = time.perf_counter_ns()
        b = canonical(snap); d = sha256(b)
        t1 = time.perf_counter_ns()
        policy.evaluate(action, ae.phi)
        t2 = time.perf_counter_ns()
        sk.sign(b)
        t3 = time.perf_counter_ns()
        sha256((ae.chain_head + d + "ALLOW").encode())
        t4 = time.perf_counter_ns()

        t_canon.append((t1 - t0) / 1000)
        t_policy.append((t2 - t1) / 1000)
        t_sign.append((t3 - t2) / 1000)
        t_chain.append((t4 - t3) / 1000)

        # end-to-end through the gateway
        t5 = time.perf_counter_ns()
        gw.submit(action)
        t6 = time.perf_counter_ns()
        t_total.append((t6 - t5) / 1000)

    rows = [summarize("canonicalization + digest", t_canon),
            summarize("policy evaluation", t_policy),
            summarize("Ed25519 signing", t_sign),
            summarize("chain append", t_chain),
            summarize("end-to-end gateway step", t_total)]
    for r in rows:
        print(f"  {r['component']:<28} mean {r['mean_us']:>8.2f} us   "
              f"p95 {r['p95_us']:>8.2f}   p99 {r['p99_us']:>8.2f}")
    thr = 1e6 / st.mean(t_total)
    print(f"  {'throughput (single core)':<28} {thr:>11.0f} steps/s")
    return {"components": rows, "throughput_steps_per_s": round(thr)}


# ---------------------------------------------------------------- B2
def b2_scaling():
    """Bounded summary (fold) vs naive full-path re-evaluation."""
    lengths = [10, 50, 100, 500, 1000, 5000]
    out = []
    for L in lengths:
        ae, store, policy = make_stack()
        gw = Gateway(ae, store)
        acts = [Action("db.read", "customers", {"row": i}) for i in range(L)]
        for a in acts[:-1]:
            gw.submit(a)
        # bounded-summary step cost at depth L
        samples = []
        for _ in range(300):
            t0 = time.perf_counter_ns()
            policy.evaluate(acts[-1], ae.phi)
            samples.append((time.perf_counter_ns() - t0) / 1000)
        # naive baseline: re-fold the entire path each step
        naive = []
        history = [(a, "ALLOW") for a in acts[:-1]]
        for _ in range(30):
            t0 = time.perf_counter_ns()
            phi = PathSummary()
            for a, v in history:
                phi = phi.fold(a, v)
            policy.evaluate(acts[-1], phi)
            naive.append((time.perf_counter_ns() - t0) / 1000)
        row = {"path_length": L,
               "bounded_summary_us": round(st.median(samples), 3),
               "naive_full_path_us": round(st.median(naive), 3)}
        out.append(row)
        print(f"  path {L:>5}: bounded {row['bounded_summary_us']:>8.3f} us   "
              f"naive {row['naive_full_path_us']:>10.3f} us")
    return out


# ---------------------------------------------------------------- B3
def b3_verification():
    out = []
    for L in [100, 1000, 5000]:
        ae, store, _ = make_stack()
        gw = Gateway(ae, store)
        for i in range(L):
            gw.submit(Action("db.read", "customers", {"row": i}))
        v = Verifier(ae.pk, ae.measurement)
        t0 = time.perf_counter_ns()
        ok, msg = v.verify_chain(store.records)
        dt = (time.perf_counter_ns() - t0) / 1e6
        assert ok, msg
        row = {"records": L, "verify_ms": round(dt, 2),
               "per_record_us": round(dt * 1000 / L, 2)}
        out.append(row)
        print(f"  verify {L:>5} records: {row['verify_ms']:>8.2f} ms "
              f"({row['per_record_us']:.2f} us/record)")
    return out


# ---------------------------------------------------------------- B4
def b4_utility():
    """False-rejection rate of path-aware policy on benign workloads.

    Workload model: sequences of reads and egresses. A sequence is *benign* if
    its egresses carry no data above the permitted class; the path-aware
    monitor is conservative (it refuses any egress after a higher-class read,
    regardless of content), so benign-but-refused sequences are the utility
    cost. We then add an explicit declassification point (a redaction step
    that resets the label) and re-measure.
    """
    import random
    rng = random.Random(7)
    N = 2000
    results = {}

    for declassify in (False, True):
        refused_benign = 0
        total_benign = 0
        blocked_malicious = 0
        total_malicious = 0
        for _ in range(N):
            grant = Grant("user:alice",
                          frozenset({"db.read", "http.post", "redact"}),
                          frozenset({"customers", "api.partner.com"}),
                          max_spend=1e9, max_sensitivity_egress="internal")
            policy = PolicyEngine(grant, path_aware=True)
            ae = AttestingEnvironment(policy)
            gw = Gateway(ae, EvidenceStore())

            # random benign or malicious sequence
            malicious = rng.random() < 0.3
            steps = []
            for _ in range(rng.randint(2, 6)):
                if rng.random() < 0.5:
                    cls = "confidential" if (malicious or rng.random() < 0.4) else "internal"
                    steps.append(Action("db.read", "customers", {"r": 1},
                                        classification=cls))
                else:
                    steps.append(Action("http.post", "api.partner.com", {"b": "x"}))
            if not any(s.kind == "http.post" for s in steps):
                steps.append(Action("http.post", "api.partner.com", {"b": "x"}))

            # a benign workflow redacts before egress when declassification exists
            seq = []
            for s in steps:
                if declassify and s.kind == "http.post" and not malicious:
                    seq.append(("redact", None))
                seq.append(("act", s))

            denied = False
            for kind, s in seq:
                if kind == "redact":
                    # explicit declassification point: resets accumulated label
                    ae.phi = PathSummary(ae.phi.steps, "public",
                                         ae.phi.egress_count, ae.phi.spend,
                                         frozenset(), ae.phi.trust_elevated)
                    continue
                r = gw.submit(s)
                if r["verdict"] == "DENY":
                    denied = True
                    break
            if malicious:
                total_malicious += 1
                blocked_malicious += 1 if denied else 0
            else:
                total_benign += 1
                refused_benign += 1 if denied else 0

        frr = refused_benign / max(1, total_benign)
        det = blocked_malicious / max(1, total_malicious)
        key = "with_declassification" if declassify else "no_declassification"
        results[key] = {
            "benign_sequences": total_benign,
            "benign_refused": refused_benign,
            "false_rejection_rate": round(frr, 4),
            "malicious_sequences": total_malicious,
            "malicious_blocked": blocked_malicious,
            "detection_rate": round(det, 4),
        }
        print(f"  {key:<24} FRR {frr:6.1%}   malicious blocked {det:6.1%}")
    return results


def main():
    print("Proof-of-Control reference implementation — benchmarks")
    print(f"  platform: {platform.platform()}  python {platform.python_version()}")
    print(f"  cpu: {platform.processor()}\n")

    print("B1  per-step latency (components + end-to-end)")
    b1 = b1_latency()
    print("\nB2  scaling with path length (bounded summary vs naive)")
    b2 = b2_scaling()
    print("\nB3  independent verification cost")
    b3 = b3_verification()
    print("\nB4  utility cost of path-aware authorization")
    b4 = b4_utility()

    out = {
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "note": ("latencies exclude TEE transition costs; the attesting "
                     "environment is modelled in-process"),
        },
        "b1_latency": b1, "b2_scaling": b2,
        "b3_verification": b3, "b4_utility": b4,
    }
    p = Path(__file__).resolve().parent.parent / "results" / "bench.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwritten to {p}")


if __name__ == "__main__":
    main()
