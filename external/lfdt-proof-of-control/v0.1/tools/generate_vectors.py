#!/usr/bin/env python3
"""Generate the published test vectors for the Evidence claim set.

The positive vectors are not hand-written. They come out of the reference
implementation in impl/poc, are then re-signed under a fixed key with a fixed
timestamp so the files are byte-reproducible, and are checked by the
independent validator in schema/validate.py. So each positive vector
demonstrates three things at once: the implementation emits conforming
evidence, the schema accepts it, and the bytes are stable enough to compare
across implementations.

The negative vectors are hand-built, because each one has to break exactly one
rule and nothing else. A vector that breaks two rules cannot show which check
caught it.

Usage:  python3 tools/generate_vectors.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "impl"))
sys.path.insert(0, str(ROOT / "schema"))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from poc import Action, AttestingEnvironment, EvidenceStore, Gateway, Grant, PolicyEngine  # noqa: E402
from validate import jcs, python_canonical, signing_input  # noqa: E402

# Measured, not invented: MRTD of a GCP C3 Confidential VM, read out of
# tests/fixtures/gcp-c3-tdx/quote.bin in the parallax repository at offset
# 48 + 136 (quote header + TD report body offset), length 48.
MRTD_GCP_C3 = (
    "sha-384:c1ee9c16e3afc506cfe042c5b846a368528f3b37618eafb27469bc114cf914e9"
    "222c91618470e7f2b28ac360968270a5"
)

OUT = ROOT / "schema" / "vectors"

# A published test key. It signs nothing but test vectors; the whole point is
# that everyone has it.
SEED = bytes.fromhex(
    "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
FROZEN_IAT = 1_754_400_000          # 2025-08-05T12:00:00Z, fixed so files are
                                    # byte-identical on every run


def resign(token: dict, sk: Ed25519PrivateKey) -> dict:
    """Freeze the timestamp and re-sign over the canonical signing input."""
    token = {k: v for k, v in token.items() if k != "signature"}
    token["iat"] = FROZEN_IAT
    token["signature"] = sk.sign(signing_input(token)).hex()
    return token


def write(path: Path, obj: dict | str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, str):
        path.write_text(obj, encoding="utf-8")
    else:
        path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}")


def main() -> int:
    sk = Ed25519PrivateKey.from_private_bytes(SEED)
    pk_hex = sk.public_key().public_bytes_raw().hex()

    grant = Grant("user:alice", frozenset({"db.read", "http.post"}),
                  frozenset({"customers", "api.partner.com"}),
                  max_spend=1000.0, max_sensitivity_egress="internal")
    ae = AttestingEnvironment(PolicyEngine(grant, path_aware=True),
                              signing_key=sk)
    gw = Gateway(ae, EvidenceStore(), agent_id="did:web:example.org:agents:ref-1")

    print("Positive vectors")
    # step 0: an ordinary permitted read
    r0 = gw.submit(Action("db.read", "customers", {"row": 42},
                          classification="confidential"))
    allow = resign(r0["token"], sk)
    write(OUT / "positive" / "allow-read.json", allow)

    # step 1: egress after a confidential read -- refused on the path, not the
    # action. A DENY is evidence too, and a verifier must handle it.
    r1 = gw.submit(Action("http.post", "api.partner.com", {"body": "..."}))
    deny = resign(r1["token"], sk)
    write(OUT / "positive" / "deny-path-composition.json", deny)

    # the same claim set as it looks from a real TEE rather than a software
    # stand-in. Structurally identical; only the attestation submodule differs,
    # and that difference is the whole distance between Tier 2 and Tier 3.
    hw = json.loads(json.dumps(allow))
    hw["submods"]["attestation"] = {
        "platform": "INTEL_TDX",
        # A real MRTD, captured from a GCP C3 Confidential VM (TDX) and
        # extracted from the quote at the v4 TD-report offset. It is 48 bytes,
        # because an MRTD is SHA-384.
        #
        # This line previously read
        #     allow["submods"]["attestation"]["measurement"]
        # which copied the SOFTWARE stand-in's SHA-256 digest into a vector
        # labelled INTEL_TDX. The result was 32 bytes -- a value that cannot be
        # an MRTD -- and it validated, because the schema's digest pattern did
        # not tie the algorithm tag to the width. Both are fixed together;
        # neither fix alone would have caught the other.
        "measurement": MRTD_GCP_C3,
        "reference_values_uri": "https://advancedaisociety.org/poc/refvalues/ref-1",
    }
    hw = resign(hw, sk)
    write(OUT / "positive" / "hardware-attested.json", hw)

    # a MODIFY verdict that correctly commits to what was actually dispatched
    mod = json.loads(json.dumps(allow))
    mod["poc_claims"]["verdict"] = "MODIFY"
    mod["poc_claims"]["reason"] = "recipient domain rewritten to the approved partner"
    mod["poc_claims"]["dispatched_snapshot_hash"] = "sha-256:" + hashlib.sha256(
        b"the action that actually ran").hexdigest()
    mod = resign(mod, sk)
    write(OUT / "positive" / "modify-bound.json", mod)

    print("\nNegative vectors")
    neg = OUT / "negative"

    def broken(mutate, name):
        t = json.loads(json.dumps(allow))
        mutate(t)
        t = resign(t, sk)
        write(neg / name, t)

    def drop_bundle(t):
        del t["poc_claims"]["policy_bundle_hash"]
    broken(drop_bundle, "missing-policy-bundle-hash.json")

    def untag(t):
        t["poc_claims"]["chain_head"] = \
            t["poc_claims"]["chain_head"].split(":", 1)[1]
    broken(untag, "untagged-digest.json")

    def alg_width_mismatch(t):
        # The shape of the defect that put a 32-byte SOFTWARE digest into a
        # vector labelled INTEL_TDX: a digest whose declared algorithm does not
        # match its width. The earlier pattern accepted any tag with any length
        # in 64-128 hex, so this validated. Nothing else in the suite covers it.
        head = t["poc_claims"]["chain_head"].split(":", 1)[1]
        t["poc_claims"]["chain_head"] = "sha-384:" + head   # 48-byte tag, 32-byte value
    broken(alg_width_mismatch, "digest-alg-width-mismatch.json")

    def wrong_profile(t):
        t["eat_profile"] = "https://example.com/some-other-profile/v3"
    broken(wrong_profile, "wrong-profile.json")

    def bad_hook(t):
        t["poc_claims"]["interception_point"] = "BEFORE_THE_THING"
    broken(bad_hook, "bad-interception-point.json")

    def small_tree(t):
        t["poc_claims"]["step_index"] = 9
        t["poc_claims"]["tree_size"] = 4
    broken(small_tree, "tree-size-too-small.json")

    def unbound_modify(t):
        t["poc_claims"]["verdict"] = "MODIFY"
    broken(unbound_modify, "modify-unbound.json")

    # An uppercase digest in an EXTENSION claim. The schema cannot catch this:
    # extension claims are open by design, so canonicalization is the only
    # thing standing between two implementations and two different digests.
    def upper_ext(t):
        t["poc_claims"]["vendor_context_digest"] = \
            "sha-256:" + hashlib.sha256(b"ctx").hexdigest().upper()
    broken(upper_ext, "uppercase-hex-extension.json")

    # A float where the profile allows none. `iat` is typed "number", so the
    # schema passes it; only the canonical layer refuses.
    def float_iat(t):
        t["poc_claims"]["step_index"] = 0
    t = json.loads(json.dumps(allow))
    float_iat(t)
    t = resign(t, sk)
    t["iat"] = 1754400000.5
    t["signature"] = sk.sign(signing_input(t)).hex()
    write(neg / "float-timestamp.json", t)

    # A signature over different bytes than the token presents.
    t = json.loads(json.dumps(allow))
    t["poc_claims"]["target_resource"] = "api.attacker.example"
    write(neg / "bad-signature.json", t)      # signature deliberately NOT redone

    # Duplicate keys cannot be produced by a serializer; the file is written by
    # hand. A last-wins parser accepts this and sees verdict=ALLOW, while a
    # first-wins parser sees DENY: one file, two meanings, which is the whole
    # attack.
    dup = json.dumps(allow, indent=2, sort_keys=True)
    dup = dup.replace('"verdict": "ALLOW"',
                      '"verdict": "DENY",\n    "verdict": "ALLOW"', 1)
    write(neg / "duplicate-key.json", dup + "\n")

    print("\nCanonical-form vectors")
    canon = OUT / "canonical"

    # Strings that make serializers disagree: control characters, a character
    # that must not be escaped, and an emoji outside the BMP.
    tricky = {
        "ascii": "plain",
        "quote": 'he said "no"',
        "backslash": "a\\b",
        "controls": "tab\there\nnewline",
        "unicode": "café über naïve",
        "astral": "\U0001F5DD key",
        "nested": {"b": 2, "a": 1, "é": 3},
        "empty_obj": {},
        "empty_arr": [],
        "ints": [0, -1, 1000000],
    }
    write(canon / "tricky-strings.json", tricky)

    # The divergence named in canonicalization.md, as a concrete artifact.
    # U+1F600 is a surrogate pair in UTF-16, so it sorts BEFORE U+FF00 under
    # RFC 8785 and AFTER it under code-point ordering.
    nonbmp = {"\U0001F600": "astral", "＀": "bmp", "a": "ascii"}
    write(canon / "nonbmp-key-ordering.json", nonbmp)

    j, p = jcs(nonbmp), python_canonical(nonbmp)
    print(f"    RFC 8785 order : {j.decode()[:60]}")
    print(f"    code-point order: {p.decode()[:60]}")
    print(f"    they differ: {j != p}  <- this is why the vector exists")

    print("\nManifest")
    manifest = {
        "profile": "https://advancedaisociety.org/poc/v0.1",
        "note": ("Test vectors for the Proof-of-Control Evidence claim set. "
                 "The signing key below is PUBLISHED and must never be used "
                 "for anything but these vectors."),
        "public_key": pk_hex,
        "private_key_seed": SEED.hex(),
        "frozen_iat": FROZEN_IAT,
        "positive": [
            {"file": "positive/allow-read.json",
             "description": "permitted read, software attestation"},
            {"file": "positive/deny-path-composition.json",
             "description": "DENY: egress after a confidential read"},
            {"file": "positive/hardware-attested.json",
             "description": "same claims, Intel TDX attestation"},
            {"file": "positive/modify-bound.json",
             "description": "MODIFY that commits to what was dispatched"},
        ],
        "negative": [
            {"file": "negative/missing-policy-bundle-hash.json",
             "expect_code": "schema",
             "why": "a verdict that cannot be re-derived is not evidence"},
            {"file": "negative/untagged-digest.json", "expect_code": "schema",
             "why": "the hash algorithm must never be guessed"},
            {"file": "negative/digest-alg-width-mismatch.json",
             "expect_code": "schema",
             "why": "a digest cannot be what its tag says at that width"},
            {"file": "negative/wrong-profile.json", "expect_code": "schema",
             "why": "claims must not be interpreted under an unknown profile"},
            {"file": "negative/bad-interception-point.json",
             "expect_code": "schema",
             "why": "an unrecognised hook makes coverage unassessable"},
            {"file": "negative/tree-size-too-small.json",
             "expect_code": "tree-size",
             "why": "a record must be a leaf of the tree it names"},
            {"file": "negative/modify-unbound.json",
             "expect_code": "modify-unbound",
             "why": "MODIFY must commit to the action that actually runs"},
            {"file": "negative/uppercase-hex-extension.json",
             "expect_code": "hex-case",
             "why": "extension claims are open, so canonicalization is the "
                    "only defence against two digests for one value"},
            {"file": "negative/float-timestamp.json",
             "expect_code": "float-in-claims",
             "why": "number formatting is the hardest part of canonicalization; "
                    "the claim set avoids it by forbidding floats"},
            {"file": "negative/bad-signature.json", "expect_code": "signature",
             "why": "a claim altered after signing"},
            {"file": "negative/duplicate-key.json", "expect_code": "duplicate-key",
             "why": "one file that means ALLOW to one parser and DENY to another"},
        ],
        "canonical": [],
    }
    for f, desc in (("canonical/tricky-strings.json",
                     "escaping, Unicode, empty containers"),
                    ("canonical/nonbmp-key-ordering.json",
                     "UTF-16 vs code-point key order (RFC 8785 section 3.2.3)")):
        obj = json.loads((OUT / f).read_text(encoding="utf-8"))
        manifest["canonical"].append({
            "file": f, "description": desc,
            "canonical_sha256": hashlib.sha256(jcs(obj)).hexdigest(),
        })
    write(OUT / "manifest.json", manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
