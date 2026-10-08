#!/usr/bin/env python3
"""The CWT/CBOR rendering of the Evidence claim set, and proof that it says the
same thing as the JSON one.

A profile that defines two renderings has to demonstrate they are equivalent,
or the second rendering is just a second chance to be incompatible. This module
implements the mapping declared in poc-evidence.cddl and round-trips every
published test vector through it: JSON -> CBOR -> JSON must return exactly the
object it started from.

    python3 schema/cbor_profile.py          round-trip all vectors, report sizes

Claim keys are the PROVISIONAL private-use allocation from the CDDL. They are
not stable until IANA registration; the round-trip property is what is being
demonstrated here, not the specific integers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from validate import jcs, load_token  # noqa: E402

# ---- claim keys, mirroring poc-evidence.cddl -------------------------------
STD = {"iss": 1, "iat": 6, "nonce": 10, "eat_profile": 265, "submods": 266}
POC = {
    "agent_id": -70001, "initiating_user": -70002, "agbom_digest": -70003,
    "interception_point": -70004, "step_index": -70005, "chain_head": -70006,
    "policy_bundle_hash": -70007, "target_resource": -70008,
    "canonical_snapshot_hash": -70009, "path_summary_hash": -70010,
    "verdict": -70011, "reason": -70012, "alg": -70013,
    "merkle_root": -70014, "tree_size": -70015,
    "dispatched_snapshot_hash": -70016,
}
HOOKS = ["TASK_INITIALIZATION", "CONTEXT_ASSEMBLY", "PLAN_GENERATION",
         "PRE_CALL_TOOL_INVOCATION", "POST_CALL_TOOL_RESULT", "MEMORY_WRITE",
         "SUBAGENT_DELEGATION", "TASK_COMPLETION"]
VERDICTS = ["ALLOW", "DENY", "MODIFY", "ESCALATE"]
# COSE algorithm identifiers, as poc-evidence.cddl defines alg-id. A list
# position here once stood in for them, so tokens from this encoder failed
# CDDL validation at key -70013.
ALGS = {"EdDSA": -8, "ES256": -7, "ML-DSA-44": -48, "ML-DSA-65": -49,
        "Ed25519+ML-DSA-44": -1000}
ALG_NAMES = {v: k for k, v in ALGS.items()}
HASHES = ["sha-256", "sha-384", "sha-512", "sha3-256"]


def _dig_to_cbor(s: str):
    """'sha-256:9f86...' -> [1, h'9f86...']. The tag becomes an integer and the
    hex becomes actual bytes, which is where most of the size saving comes from."""
    alg, _, hexval = s.partition(":")
    return [HASHES.index(alg) + 1, bytes.fromhex(hexval)]


def _dig_from_cbor(v) -> str:
    alg, raw = v
    return f"{HASHES[alg - 1]}:{raw.hex()}"


DIGEST_CLAIMS = {"agbom_digest", "chain_head", "merkle_root",
                 "policy_bundle_hash", "canonical_snapshot_hash",
                 "path_summary_hash", "dispatched_snapshot_hash"}


def to_cbor(token: dict) -> bytes:
    import cbor2
    c = token["poc_claims"]
    m: dict = {
        STD["iss"]: token["iss"],
        STD["iat"]: token["iat"],
        STD["nonce"]: token["nonce"].encode("utf-8"),
        STD["eat_profile"]: token["eat_profile"],
    }
    for k, v in c.items():
        key = POC.get(k)
        if key is None:
            m[k] = v                                  # extension: keep the name
        elif k in DIGEST_CLAIMS:
            m[key] = _dig_to_cbor(v)
        elif k == "interception_point":
            m[key] = HOOKS.index(v) + 1
        elif k == "verdict":
            m[key] = VERDICTS.index(v) + 1
        elif k == "alg":
            m[key] = ALGS[v]
        else:
            m[key] = v
    att = dict(token["submods"]["attestation"])
    att["measurement"] = _dig_to_cbor(att["measurement"])
    m[STD["submods"]] = {"attestation": att}
    if "signature" in token:
        m["signature"] = bytes.fromhex(token["signature"])
    # RFC 8949 section 4.2 deterministic encoding
    return cbor2.dumps(m, canonical=True)


def from_cbor(data: bytes) -> dict:
    import cbor2
    m = cbor2.loads(data)
    inv = {v: k for k, v in POC.items()}
    claims: dict = {}
    for key, v in m.items():
        if key in (STD["iss"], STD["iat"], STD["nonce"], STD["eat_profile"],
                   STD["submods"], "signature"):
            continue
        name = inv.get(key, key)
        if name in DIGEST_CLAIMS:
            claims[name] = _dig_from_cbor(v)
        elif name == "interception_point":
            claims[name] = HOOKS[v - 1]
        elif name == "verdict":
            claims[name] = VERDICTS[v - 1]
        elif name == "alg":
            claims[name] = ALG_NAMES[v]
        else:
            claims[name] = v
    att = dict(m[STD["submods"]]["attestation"])
    att["measurement"] = _dig_from_cbor(att["measurement"])
    out = {
        "iss": m[STD["iss"]],
        "iat": m[STD["iat"]],
        "nonce": m[STD["nonce"]].decode("utf-8"),
        "eat_profile": m[STD["eat_profile"]],
        "poc_claims": claims,
        "submods": {"attestation": att},
    }
    if "signature" in m:
        out["signature"] = m["signature"].hex()
    return out


def main() -> int:
    try:
        import cbor2  # noqa: F401
    except ImportError:
        print("cbor2 not installed: pip install cbor2")
        return 2

    manifest = json.loads((HERE / "vectors" / "manifest.json").read_text())
    print("JSON -> CBOR -> JSON round trip\n")
    print(f"  {'vector':<40}{'JSON':>9}{'CBOR':>9}{'saved':>9}  result")
    ok = fail = 0
    tj = tc = 0
    for entry in manifest["positive"]:
        p = HERE / "vectors" / entry["file"]
        tok = load_token(p.read_text())
        enc = to_cbor(tok)
        back = from_cbor(enc)
        nj, nc = len(jcs(tok)), len(enc)
        tj += nj
        tc += nc
        same = jcs(back) == jcs(tok)
        ok, fail = (ok + 1, fail) if same else (ok, fail + 1)
        name = entry["file"].split("/")[-1]
        print(f"  {name:<40}{nj:>9}{nc:>9}{1 - nc/nj:>8.0%}  "
              f"{'identical' if same else 'DIFFERS'}")
        if not same:
            for k in set(tok["poc_claims"]) ^ set(back["poc_claims"]):
                print(f"      claim differs: {k}")

    print(f"\n  totals{'':<34}{tj:>9}{tc:>9}{1 - tc/tj:>8.0%}")
    print(f"\n  {ok} identical, {fail} differing")
    if not fail:
        print("\n  The two renderings carry the same claim set. The CBOR form is\n"
              "  smaller mainly because digests travel as bytes rather than as\n"
              "  hex text, which halves every one of them.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
