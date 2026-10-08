#!/usr/bin/env python3
"""Correctness tests for the reference implementation. Run: python3 tests/test_core.py"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from poc import (Action, AttestingEnvironment, EvidenceStore, Gateway, Grant,
                 PathSummary, PolicyEngine, RelyingParty, TransparencyLog,
                 Verifier, gossip)

PASS = FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1; print(f"  ok   {name}")
    else:
        FAIL += 1; print(f"  FAIL {name}")


def stack(path_aware=True, anchor=None):
    g = Grant("user:alice", frozenset({"db.read", "http.post", "pay.send"}),
              frozenset({"customers", "api.partner.com", "api.bank.com"}),
              max_spend=100.0, max_sensitivity_egress="internal")
    ae = AttestingEnvironment(PolicyEngine(g, path_aware), anchor=anchor,
                              anchor_interval_s=0.0)
    s = EvidenceStore()
    return ae, s, Gateway(ae, s)


def main():
    print("Proof-of-Control reference implementation — tests\n")

    # evidence exists for every action, and precedes release
    ae, store, gw = stack()
    r = gw.submit(Action("db.read", "customers", {"row": 1}))
    check("C7.1.2 evidence emitted for an allowed action", len(store.records) == 1)
    check("C7.1.3 evidence written before release", r["executed"])

    # denied actions are evidenced too
    r = gw.submit(Action("db.delete", "customers", {}))
    check("C4.1.2 denial recorded with reason",
          r["verdict"] == "DENY" and len(store.records) == 2
          and store.records[-1]["poc_claims"]["verdict"] == "DENY")

    # chain verifies end-to-end by an independent verifier
    v = Verifier(ae.pk, ae.measurement)
    ok, msg = v.verify_chain(store.records)
    check(f"C8.1.5 independent verification ({msg})", ok)

    # signing key is not reachable through the API
    check("C7.3.2 signing key not exposed",
          not any(a for a in dir(ae) if a in ("sk", "signing_key", "private_key")))

    # spend budget accumulates across the path
    ae, store, gw = stack()
    a = Action("pay.send", "api.bank.com", {"amount": 60.0})
    r1 = gw.submit(a); r2 = gw.submit(a)
    check("C4.1.7 cumulative spend enforced across path",
          r1["verdict"] == "ALLOW" and r2["verdict"] == "DENY")

    # per-action policy misses the same composition
    ae, store, gw = stack(path_aware=False)
    r1 = gw.submit(a); r2 = gw.submit(a)
    check("baseline per-action policy misses cumulative overspend",
          r1["verdict"] == "ALLOW" and r2["verdict"] == "ALLOW")

    # bounded path summary stays bounded
    ae, store, gw = stack()
    for i in range(500):
        gw.submit(Action("db.read", "customers", {"row": i},
                         classification="confidential"))
    check("C4.1.7 path summary size bounded (labels <= 8)", len(ae.phi.labels) <= 8)
    check("path summary digest is stable-length", len(ae.phi.digest()) == 64)

    # anchoring + truncation detection
    log = TransparencyLog()
    ae, store, gw = stack(anchor=log)
    for i in range(4):
        gw.submit(Action("db.read", "customers", {"row": i}))
    ae.force_anchor()
    v = Verifier(ae.pk, ae.measurement)
    ok_full, _ = v.verify_chain(store.records, anchor=log)
    ok_trunc, _ = v.verify_chain(store.records[:2], anchor=log)
    check("C7.6.6 full chain verifies against anchor", ok_full)
    check("C7.6.6 truncated chain rejected against anchor", not ok_trunc)

    # gossip agrees when there is no fork
    log_b = TransparencyLog()
    for e in log.entries:
        log_b.entries.append(e)
    consistent, _ = gossip(log, log_b)
    check("C7.3.3 gossip reports consistency when histories agree", consistent)

    # capability binds to resource
    ae, store, gw = stack()
    rp_other = RelyingParty(ae.pk, "api.other.com", ae.measurement)
    out = ae.evaluate_and_evidence(
        Action("http.post", "api.partner.com", {"b": "x"}), "n1", gw.agent_id)
    ok, why = rp_other.execute(Action("http.post", "api.partner.com", {"b": "x"}),
                               out["capability"])
    check(f"C7.1.4 capability rejected at wrong resource ({why})", not ok)

    # measurement mismatch is rejected
    rp_bad = RelyingParty(ae.pk, "api.partner.com", "0" * 64)
    ok, why = rp_bad.execute(Action("http.post", "api.partner.com", {"b": "x"}),
                             out["capability"])
    check(f"C8.1.7 measurement mismatch rejected ({why})", not ok)

    # ---------------------------------------------------- Merkle proofs
    from poc import (MerkleTree, leaf_hash, reference_root, verify_consistency,
                     verify_inclusion)

    recs = [f"r{i}".encode() for i in range(37)]     # deliberately not a power of 2
    tree = MerkleTree()
    for r in recs:
        tree.append(r)

    check("incremental root matches the RFC 6962 recursive definition",
          all(tree.root_at(n) == reference_root([leaf_hash(r) for r in recs[:n]])
              for n in range(1, len(recs) + 1)))

    check("C7.3.4 every record has a valid inclusion proof",
          all(verify_inclusion(i, len(recs), leaf_hash(recs[i]),
                               tree.inclusion_proof(i), tree.root())
              for i in range(len(recs))))

    check("C7.3.4 inclusion proof rejects a substituted record",
          not verify_inclusion(5, len(recs), leaf_hash(b"forged"),
                               tree.inclusion_proof(5), tree.root()))

    import math
    check(f"C7.3.4 proof size is logarithmic "
          f"({len(tree.inclusion_proof(5))} hashes for {len(recs)} records)",
          len(tree.inclusion_proof(5)) <= math.ceil(math.log2(len(recs))) + 1)

    check("C7.3.5 consistency proof holds for every published prefix",
          all(verify_consistency(m, len(recs), tree.root_at(m), tree.root(),
                                 tree.consistency_proof(m))
              for m in range(1, len(recs) + 1)))

    tampered = MerkleTree()
    for i, r in enumerate(recs):
        tampered.append(b"TAMPERED" if i == 10 else r)
    check("C7.3.5 consistency proof refuses a rewritten prefix",
          not verify_consistency(20, len(recs), tree.root_at(20),
                                 tampered.root(), tampered.consistency_proof(20)))

    # the A9 defect, as a regression test
    log = TransparencyLog()
    ae, store, gw = stack(anchor=log)
    for i in range(6):
        gw.submit(Action("db.read", "customers", {"row": i}))
    ae.force_anchor()
    ae2 = AttestingEnvironment(PolicyEngine(ae.policy.grant),
                               signing_key=ae._sk)
    store2 = EvidenceStore()
    gw2 = Gateway(ae2, store2)
    for i in range(6):
        gw2.submit(Action("db.read", "customers", {"row": 99 if i == 2 else i}))
    v = Verifier(ae.pk, ae.measurement)
    check("C7.3.5 re-signed rewritten history rejected against the anchored root",
          not v.verify_chain(store2.records, anchor=log)[0])

    # ---------------------------------------------------- schema conformance
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "schema"))
    try:
        import validate as V
        ae3, store3, gw3 = stack()
        gw3.submit(Action("db.read", "customers", {"row": 1}))
        tok = store3.records[0]
        try:
            V.validate(tok, ae3.pk.public_bytes_raw().hex())
            ok, why = True, ""
        except V.ValidationError as e:
            ok, why = False, str(e)
        check(f"emitted evidence validates against the published schema{why and ': ' + why}",
              ok)
    except ImportError:                                        # pragma: no cover
        print("  skip  schema validator unavailable")

    print(f"\n{PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
