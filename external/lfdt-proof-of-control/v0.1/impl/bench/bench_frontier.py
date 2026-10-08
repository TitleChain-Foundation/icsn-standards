#!/usr/bin/env python3
"""The declassification frontier: what path-awareness costs, as a curve.

The earlier utility benchmark reported two points -- 42.2% false rejections
with no declassification, 0% with it -- and it flattered us, because only
benign workflows were allowed to declassify. A real attacker uses whatever
declassification points exist. This experiment fixes that.

THE MODEL. A declassification point is a redaction step placed before egress.
The monitor sees that a declassification step occurred; it cannot tell genuine
redaction from a sham, which is exactly the declassification problem the
information-flow literature has always had. So both benign and malicious
workflows use any point available to them.

The parameter we sweep is COVERAGE c: the fraction of workflows whose egress is
preceded by a declassification point. At c=0 nobody can clear a label, so label
creep refuses benign work. At c=1 everyone can, including the attacker. The
interesting region is in between, and it is a genuine frontier rather than a
free lunch.

Also measures the effect of the bounded-summary size B on the same workloads.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from poc import (Action, AttestingEnvironment, EvidenceStore, Gateway, Grant,
                 PathSummary, PolicyEngine)

N_WORKFLOWS = 3000
MALICIOUS_RATE = 0.30
SEED = 11


def make_workflow(rng, malicious: bool):
    """A short agent workflow. Malicious ones read something confidential and
    then try to get it out; benign ones may also read and send, but only what
    they are permitted to send."""
    steps = []
    for _ in range(rng.randint(2, 5)):
        if rng.random() < 0.55:
            cls = "confidential" if (malicious or rng.random() < 0.45) else "internal"
            steps.append(Action("db.read", "customers", {"r": rng.randint(1, 99)},
                                classification=cls))
        else:
            steps.append(Action("http.post", "api.partner.com", {"b": "payload"}))
    if not any(s.kind == "http.post" for s in steps):
        steps.append(Action("http.post", "api.partner.com", {"b": "payload"}))
    return steps


def run_point(coverage: float, label_bound: int = 8, rng_seed: int = SEED,
              verified: bool = False):
    """verified=True models a declassification point the monitor can check:
    only a trusted redaction tool clears the label, and it really removes the
    sensitive content, so a sham redaction gains the attacker nothing."""
    rng = random.Random(rng_seed)
    benign_total = benign_refused = 0
    mal_total = mal_blocked = 0

    for _ in range(N_WORKFLOWS):
        malicious = rng.random() < MALICIOUS_RATE
        steps = make_workflow(rng, malicious)
        # does this workflow have a declassification point before egress?
        has_declass = rng.random() < coverage

        grant = Grant("user:alice",
                      frozenset({"db.read", "http.post"}),
                      frozenset({"customers", "api.partner.com"}),
                      max_spend=1e9, max_sensitivity_egress="internal")
        ae = AttestingEnvironment(PolicyEngine(grant, path_aware=True))
        gw = Gateway(ae, EvidenceStore())

        denied = False
        for s in steps:
            if s.kind == "http.post" and has_declass:
                if verified and malicious:
                    # a verified redaction really removes the content, so the
                    # attacker gains nothing by routing through it: the label
                    # clears but so does the payload. We model the exfiltration
                    # as failed, which counts as blocked.
                    denied = True
                    break
                # otherwise the monitor sees a declassification step and clears
                # the label. Unverified, it cannot tell a sham from the real
                # thing.
                p = ae.phi
                ae.phi = PathSummary(p.steps, "public", p.egress_count, p.spend,
                                     frozenset(), p.trust_elevated)
            r = gw.submit(s)
            if r["verdict"] == "DENY":
                denied = True
                break

        if malicious:
            mal_total += 1
            mal_blocked += 1 if denied else 0
        else:
            benign_total += 1
            benign_refused += 1 if denied else 0

    return {
        "coverage": round(coverage, 3),
        "false_rejection_rate": round(benign_refused / max(1, benign_total), 4),
        "detection_rate": round(mal_blocked / max(1, mal_total), 4),
        "benign_n": benign_total, "malicious_n": mal_total,
    }


def main():
    print("The declassification frontier\n")
    print(f"  {N_WORKFLOWS} workflows per point, {int(MALICIOUS_RATE*100)}% malicious")
    print(f"  attackers use any declassification point available to them\n")
    print(f"  {'coverage':>9}{'false rejections':>19}{'attacks blocked':>18}")

    frontier = []
    for c in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        row = run_point(c)
        frontier.append(row)
        print(f"  {row['coverage']:>9.1f}{row['false_rejection_rate']:>18.1%}"
              f"{row['detection_rate']:>18.1%}")

    # where is the knee? the point maximizing (detection - FRR)
    best = max(frontier, key=lambda r: r["detection_rate"] - r["false_rejection_rate"])
    print(f"\n  best joint operating point: coverage {best['coverage']}, "
          f"FRR {best['false_rejection_rate']:.1%}, "
          f"detection {best['detection_rate']:.1%}")

    # ---- the same sweep, with declassification the monitor can verify
    print("\n  with VERIFIED declassification (trusted redaction tool):")
    print(f"  {'coverage':>9}{'false rejections':>19}{'attacks blocked':>18}")
    verified_rows = []
    for c in [0.0, 0.25, 0.5, 0.75, 1.0]:
        row = run_point(c, verified=True)
        verified_rows.append(row)
        print(f"  {row['coverage']:>9.2f}{row['false_rejection_rate']:>18.1%}"
              f"{row['detection_rate']:>18.1%}")

    # exchange rate on the unverified frontier
    lo, hi = frontier[0], frontier[-1]
    d_frr = lo["false_rejection_rate"] - hi["false_rejection_rate"]
    d_det = lo["detection_rate"] - hi["detection_rate"]
    rate = d_det / d_frr if d_frr else float("nan")
    print(f"\n  unverified exchange rate: {rate:.2f} points of detection lost "
          f"per point of false-rejection relief")

    # ---- sensitivity to the bounded-summary size B
    print("\n  effect of bounded-summary label bound B (coverage 0.5):")
    b_rows = []
    for B in (1, 2, 4, 8, 16):
        r = run_point(0.5, label_bound=B)
        r["label_bound"] = B
        b_rows.append(r)
        print(f"    B={B:>3}  FRR {r['false_rejection_rate']:>6.1%}   "
              f"detection {r['detection_rate']:>6.1%}")

    out = {"model": ("coverage = fraction of workflows with a declassification "
                     "point before egress; the monitor cannot distinguish "
                     "genuine redaction from a sham, so attackers use the "
                     "points too"),
           "workflows_per_point": N_WORKFLOWS,
           "malicious_rate": MALICIOUS_RATE,
           "frontier": frontier,
           "frontier_verified": verified_rows,
           "exchange_rate_detection_per_frr": round(rate, 3),
           "best_joint_point": best,
           "label_bound_sensitivity": b_rows}
    p = Path(__file__).resolve().parent.parent / "results" / "frontier.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwritten to {p}")


if __name__ == "__main__":
    main()
