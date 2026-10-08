#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build the RFC 0002 crosswalk against the vendored Proof-of-Control checklist.

Writes conformance/proof-of-control/crosswalk-poc-v0.1.json: one entry for each
of the 127 PoC v0.1 requirements, with the TitleChain profile disposition, the
LE requirements that extend it, and the status of the mapped M5 implementation.
M5 status is recorded only where it was checked against code; everything else is
NOT_ASSESSED. tests/validate_proof_of_control_profile.py fails on drift.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "external" / "lfdt-proof-of-control" / "v0.1" / "checklist" / "poc-checklist.json"
OUTPUT = ROOT / "conformance" / "proof-of-control" / "crosswalk-poc-v0.1.json"

LE_REQUIREMENTS = [
    ("LE1.1", 1, "Agent, legal entity, accountable human and role authority on every record", ["5.1.1"]),
    ("LE1.2", 2, "Accountable human's role authority validated before a grant", ["4.1.1", "5.1.2"]),
    ("LE1.3", 2, "Signed human -> entity role -> agent chain with scope intersection", ["4.2.2", "4.2.3"]),
    ("LE1.4", 1, "Agents are never principals and cannot over-delegate", ["4.2.3"]),
    ("LE1.5", 2, "Human or entity revokes without agent or provider consent", ["4.1.2"]),
    ("LE1.6", 2, "Grants revoked or reaffirmed when the accountable human's role ends", ["4.2.2"]),
    ("LE2.1", 2, "Key rotation leaves identifiers unchanged, with linking record", ["6.3.2"]),
    ("LE2.2", 2, "A compromised key alone cannot move title, roles or delegations", ["6.3.3"]),
    ("LE2.3", 2, "Verification distinguishes event-time, deprecated and compromised-after", ["6.3.4", "6.3.5"]),
    ("LE3.1", 3, "Pseudonymous subject with evidence of a valid entity delegation", ["4.2.4"]),
    ("LE3.2", 2, "Pseudonym linkage held by the principal; disclosure conditions declared", ["10.2.1"]),
    ("LE3.3", 2, "Scores over pseudonymous subjects use a published method", ["7.5.1"]),
    ("LE4.1", 2, "Protected records stay in the principal-controlled store", ["1.4.1", "2.1.2", "2.4.1"]),
    ("LE4.2", 2, "Exportable verification bundle, verifiable offline", ["3.2.1", "8.1.5"]),
    ("LE4.3", 3, "Signed linking record across a provider move", ["3.2.2"]),
    ("LE5.1", 2, "Computation manifest; records cite manifest and parameter digests", ["7.7.1", "10.1.5"]),
    ("LE5.2", 2, "Time-triggered events stamped at their deadline", ["7.2.1"]),
    ("LE5.3", 2, "Canonical numbers representable identically in every language", ["7.7.2", "7.7.4"]),
    ("LE5.4", 3, "Two independent implementations held to shared vectors", ["7.7.4"]),
    ("LE6.1", 2, "Accountable-human approval for consequential actions", ["4.1.6"]),
    ("LE6.2", 2, "Reversible, hash-chained settlement hold", ["7.3.1"]),
    ("LE6.3", 1, "Automated responses record their rule and trigger", ["4.1.2"]),
]

PRIVATE = "Implemented in a private repository; publication to the public commons is required for external verification."
M5_ASSESSED = {
    "4.1.6": ("PARTIAL", "Settlement and adjudication events record the acting party and decision; the actor is not yet cryptographically authenticated."),
    "6.3.4": ("PARTIAL", "Digests carry an explicit 'sha256:' algorithm label and M5-CRP-001 defines a migration path; evidence is not yet signed."),
    "7.2.1": ("PARTIAL", "Events are written when applied, stamped with the event time or, for automatic events, the deadline; no transaction-level capture yet."),
    "7.3.1": ("PARTIAL", "Settlement events are hash-chained from an opening hash and verify_event_chain detects modification, insertion and reordering; scheduled verification is not configured."),
    "7.7.1": ("PARTIAL", "M5 Value Receipt JSON Schema covers every field and receipts validate against it. " + PRIVATE),
    "7.7.2": ("PARTIAL", "Canonical JSON fixes key order, number formatting and escaping (M5-MATH-001 MATH-CANONICAL-HASH); the meaning of an absent field is not yet stated."),
    "7.7.3": ("PARTIAL", "Every digest carries the 'sha256:' identifier; verifiers do not yet reject unlabeled digests."),
    "7.7.4": ("PARTIAL", "Published canonical-hash vectors, matched by Python and JavaScript, include rejected cases; not every negative vector names its tested reason."),
    "7.7.5": ("GAP", "The JSON parser resolves duplicate keys last-wins; rejection is not implemented."),
    "8.1.8": ("PARTIAL", "A receipt verifier (receipt-verify.js) exists. " + PRIVATE),
}


def build() -> dict:
    checklist = json.loads(CHECKLIST.read_text(encoding="utf-8"))
    ids = {item["id"] for item in checklist}
    extended_by: dict[str, list[str]] = {}
    for le_id, _, _, extends in LE_REQUIREMENTS:
        for poc_id in extends:
            if poc_id not in ids:
                raise SystemExit(f"{le_id} extends unknown PoC requirement {poc_id}")
            extended_by.setdefault(poc_id, []).append(le_id)
    unknown = sorted(set(M5_ASSESSED) - ids)
    if unknown:
        raise SystemExit(f"M5 assessment names unknown requirements: {unknown}")
    entries = []
    for item in checklist:
        status, note = M5_ASSESSED.get(item["id"], ("NOT_ASSESSED", None))
        entries.append(
            {
                "poc_id": item["id"],
                "chapter": item["chapter"],
                "level": item["level"],
                "profile_disposition": "ADOPTED_AND_EXTENDED" if item["id"] in extended_by else "ADOPTED",
                "extended_by": extended_by.get(item["id"], []),
                "m5_implementation": {
                    "label": "implementation-specific, external, subject to separate terms",
                    "status": status,
                    "note": note,
                },
            }
        )
    return {
        "profile": "TitleChain Foundation RFC 0002",
        "base_standard": "LFDT Proof-of-Control Standard v0.1",
        "base_commit": json.loads(
            (CHECKLIST.parents[2] / "UPSTREAM-v0.1.json").read_text(encoding="utf-8")
        )["commit"],
        "license": "Apache-2.0",
        "status_values": {
            "profile_disposition": ["ADOPTED", "ADOPTED_AND_EXTENDED"],
            "m5_implementation": ["IMPLEMENTED", "PARTIAL", "GAP", "NOT_APPLICABLE", "NOT_ASSESSED"],
        },
        "le_requirements": [
            {"id": le_id, "level": level, "title": title, "extends": extends}
            for le_id, level, title, extends in LE_REQUIREMENTS
        ],
        "requirements": entries,
    }


if __name__ == "__main__":
    OUTPUT.write_text(json.dumps(build(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
