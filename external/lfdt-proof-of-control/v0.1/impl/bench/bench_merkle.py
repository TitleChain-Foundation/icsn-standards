#!/usr/bin/env python3
"""What a Merkle tree buys over a hash chain.

THE QUESTION. Our evidence log was a hash chain. A chain detects alteration and
omission perfectly well -- but only if you replay it. Ask "was this one action
in the log?" and a chain gives you no way to answer except to fetch every
record from the beginning and rehash the lot. For an auditor sampling one
action out of a million, that means downloading a million records to check one.

This is not a hypothetical inefficiency. It decides whether audit is something
you do continuously or something you do once a year with a data-transfer
budget.

Certificate Transparency solved this in 2013 with an append-only Merkle tree,
and we cite CT throughout the specification, so the fix is adoption rather than
invention. The tree answers two questions with proofs logarithmic in log size:

  M1  INCLUSION. Is record i in the log whose root you published?
  M2  CONSISTENCY. Is today's log an append-only extension of yesterday's, or
      did something get rewritten in between?

M3 asks the question that decides whether any of this is adoptable: what does
maintaining the tree cost on the hot path, where every microsecond is charged
to a live agent action?
"""
from __future__ import annotations

import json
import math
import statistics as st
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from poc import (MerkleTree, canonical, leaf_hash, sha256, verify_consistency,
                 verify_inclusion)

SIZES = [10, 100, 1_000, 10_000, 100_000]
HASH_BYTES = 32
RECORD_BYTES = 1_227          # measured: schema/vectors/positive/allow-read.json


def build(n: int):
    """A log of n records, held both ways."""
    recs = [canonical({"snapshot": sha256(f"s{i}".encode()), "verdict": "ALLOW"})
            for i in range(n)]
    tree = MerkleTree()
    for r in recs:
        tree.append(r)
    chain = []
    head = sha256(b"poc-genesis")
    for r in recs:
        head = sha256((head + sha256(r) + "ALLOW").encode())
        chain.append(head)
    return recs, tree, chain


# ---------------------------------------------------------------- M1
def m1_inclusion():
    """Verify that ONE record is in the log. Chain: replay everything.
    Tree: check an inclusion proof."""
    print("M1  proving one record is in the log\n")
    print(f"  {'log size':>9}{'chain replay':>15}{'proof verify':>14}"
          f"{'speedup':>10}{'proof':>8}{'fetch':>12}")
    rows = []
    for n in SIZES:
        recs, tree, chain = build(n)
        root = tree.root()
        idx = n // 2                      # a record in the middle, not the end

        # --- chain: an auditor must re-fold the whole history
        reps = 5 if n >= 10_000 else 50
        t0 = time.perf_counter_ns()
        for _ in range(reps):
            head = sha256(b"poc-genesis")
            for r in recs:
                head = sha256((head + sha256(r) + "ALLOW").encode())
            assert head == chain[-1]
        chain_us = (time.perf_counter_ns() - t0) / 1000 / reps

        # --- tree: verify a proof
        proof = tree.inclusion_proof(idx)
        leaf = leaf_hash(recs[idx])
        reps = 2000
        t0 = time.perf_counter_ns()
        for _ in range(reps):
            verify_inclusion(idx, n, leaf, proof, root)
        proof_us = (time.perf_counter_ns() - t0) / 1000 / reps
        assert verify_inclusion(idx, n, leaf, proof, root)

        proof_bytes = len(proof) * HASH_BYTES
        fetch_chain = n * RECORD_BYTES
        fetch_tree = RECORD_BYTES + proof_bytes
        rows.append({
            "n": n, "chain_replay_us": round(chain_us, 2),
            "proof_verify_us": round(proof_us, 3),
            "speedup": round(chain_us / proof_us, 1),
            "proof_hashes": len(proof), "proof_bytes": proof_bytes,
            "bytes_fetched_chain": fetch_chain,
            "bytes_fetched_tree": fetch_tree,
            "fetch_reduction": round(1 - fetch_tree / fetch_chain, 6),
        })
        print(f"  {n:>9,}{chain_us:>13,.0f}us{proof_us:>12.2f}us"
              f"{chain_us/proof_us:>9,.0f}x{proof_bytes:>7}B"
              f"{fetch_chain/1e6:>9.1f}MB")
    return rows


# ---------------------------------------------------------------- M2
def m2_consistency():
    """Detect a rewritten history.

    The chain-based check we had compares an anchor's step count against the
    number of records presented. It catches plain truncation, but it says
    nothing about a log that is the RIGHT LENGTH and has been altered in the
    middle -- to see that, you replay. A consistency proof settles it in
    O(log n), and it settles it in the strong direction: the operator cannot
    produce one for a history it rewrote.
    """
    print("\nM2  proving the log was only appended to\n")
    print(f"  {'old -> new':>18}{'proof':>8}{'verify':>10}   rewritten history?")
    rows = []
    for old, new in ((1_000, 1_001), (1_000, 2_000), (1_000, 100_000),
                     (50_000, 100_000)):
        recs, tree, _ = build(new)
        proof = tree.consistency_proof(old, new)
        r_old, r_new = tree.root_at(old), tree.root()
        reps = 2000
        t0 = time.perf_counter_ns()
        for _ in range(reps):
            verify_consistency(old, new, r_old, r_new, proof)
        us = (time.perf_counter_ns() - t0) / 1000 / reps
        assert verify_consistency(old, new, r_old, r_new, proof)

        # now rewrite one record inside the already-published prefix and see
        # whether the operator can still produce a passing proof
        alt = list(recs)
        alt[old // 2] = canonical({"snapshot": sha256(b"tampered"),
                                   "verdict": "ALLOW"})
        t2 = MerkleTree()
        for r in alt:
            t2.append(r)
        forged = t2.consistency_proof(old, new)
        caught = not verify_consistency(old, new, r_old, t2.root(), forged)

        rows.append({"old": old, "new": new, "proof_hashes": len(proof),
                     "proof_bytes": len(proof) * HASH_BYTES,
                     "verify_us": round(us, 3),
                     "rewrite_detected": caught})
        print(f"  {f'{old:,} -> {new:,}':>18}{len(proof)*HASH_BYTES:>7}B"
              f"{us:>8.2f}us   {'detected' if caught else 'MISSED'}")
    return rows


# ---------------------------------------------------------------- M3
def m3_hot_path():
    """What the tree costs the live agent.

    A structure that helps the auditor and hurts the agent is a bad trade. The
    chain is one hash per action. The tree is amortized ~2 hashes per action
    plus a root fold of at most log2(n) hashes. Both should be invisible beside
    the 85 microseconds a signature costs.
    """
    print("\nM3  cost on the hot path, per action\n")
    print(f"  {'log size':>9}{'chain append':>15}{'tree append+root':>19}"
          f"{'added':>10}{'vs signing':>12}")
    SIGN_US = 85.5                        # measured Ed25519 signing, bench.py
    rows = []
    for n in SIZES:
        rec = canonical({"snapshot": sha256(b"x"), "verdict": "ALLOW"})
        # chain: prime a head, then time one extension
        head = sha256(b"poc-genesis")
        reps = 20_000
        t0 = time.perf_counter_ns()
        for _ in range(reps):
            head = sha256((head + sha256(rec) + "ALLOW").encode())
        chain_us = (time.perf_counter_ns() - t0) / 1000 / reps

        # tree: grow to n, then time appends including a fresh root each time
        tree = MerkleTree()
        for i in range(n):
            tree.append(canonical({"snapshot": sha256(f"s{i}".encode()),
                                   "verdict": "ALLOW"}))
        reps = 5_000
        t0 = time.perf_counter_ns()
        for _ in range(reps):
            tree.append(rec)
            tree.root()
        tree_us = (time.perf_counter_ns() - t0) / 1000 / reps

        rows.append({"n": n, "chain_append_us": round(chain_us, 3),
                     "tree_append_root_us": round(tree_us, 3),
                     "added_us": round(tree_us - chain_us, 3),
                     "added_fraction_of_signing":
                         round((tree_us - chain_us) / SIGN_US, 5)})
        print(f"  {n:>9,}{chain_us:>13.3f}us{tree_us:>17.3f}us"
              f"{tree_us-chain_us:>8.3f}us{(tree_us-chain_us)/SIGN_US:>11.2%}")
    return rows


# ---------------------------------------------------------------- M4
def m4_audit_budget():
    """Turn the proof sizes into the number that decides adoption: how much an
    auditor must transfer to spot-check a sample of a year's evidence."""
    print("\nM4  sampling audit of one year of a 1,000-agent fleet\n")
    fleet, per_day, days = 1_000, 100, 365
    n = fleet * per_day * days
    depth = math.ceil(math.log2(n))
    rows = []
    print(f"  log size {n:,} records, tree depth {depth}")
    print(f"  {'sample':>9}{'chain (replay all)':>22}{'tree (proofs)':>17}"
          f"{'ratio':>12}")
    for sample in (1, 100, 10_000, 1_000_000):
        chain_bytes = n * RECORD_BYTES               # replay is all-or-nothing
        tree_bytes = sample * (RECORD_BYTES + depth * HASH_BYTES)
        rows.append({"sample": sample, "log_records": n,
                     "chain_bytes": chain_bytes, "tree_bytes": tree_bytes,
                     "ratio": round(chain_bytes / tree_bytes, 1)})
        print(f"  {sample:>9,}{chain_bytes/1e9:>20.1f}GB"
              f"{tree_bytes/1e9:>15.3f}GB{chain_bytes/tree_bytes:>11,.0f}x")
    print("\n  Replaying a chain costs the same whether you wanted to check one\n"
          "  record or a million. Proofs cost what you actually asked for.")
    return {"log_records": n, "tree_depth": depth, "rows": rows}


def main():
    print("Merkle inclusion and consistency proofs\n")
    out = {"record_bytes": RECORD_BYTES,
           "m1_inclusion": m1_inclusion(),
           "m2_consistency": m2_consistency(),
           "m3_hot_path": m3_hot_path(),
           "m4_audit_budget": m4_audit_budget()}
    p = Path(__file__).resolve().parent.parent / "results" / "merkle.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwritten to {p}")


if __name__ == "__main__":
    main()
