# M5-MATH — Specification and reference profile

M5-MATH defines versioned mathematical specifications and reproducibility requirements proposed for maintenance through the ICSN standards process. See [RFC 0003](../../rfcs/0003-m5-math-versioned-specification.md) for requirements, conformance and update governance. The RFC is Draft; its number is proposed pending editor allocation.

M5Labs calculators identify the M5-MATH version they implement. Calculator updates may contribute proposed specification revisions; they do not automatically change an adopted ICSN version. Independent implementations are welcome under the published materials' applicable licenses.

## Initial reference profile

| Record | Value |
|---|---|
| Profile | M5-MATH-001 v0.1.0 |
| Specification status | Draft proposal; no Candidate or Stable adoption claimed |
| Reference source | `ac68847627795dfee226d302f8e57fa62a21fdca` |
| Payload | [Written rules](0.1.0/docs/standards/M5-MATH-001.md), Python/JavaScript implementations and vectors |
| Integrity and scope | [Per-file manifest](UPSTREAM-0.1.0.json) |
| Release terms | [License notice](M5NASH-NOTICE.md) and [repository matrix](../../LICENSES/LICENSE-MATRIX.md) |

The profile covers canonical JSON/hashing, value-receipt validation and the proposed M5Nash calculation. M5Nash weights in this reference remain PROPOSED without economic consequences. Additional scientific calculator families require their own reviewed specification profiles and evidence.

## Verify and update

Run `python3 tests/validate_m5_math_reference.py` from the repository root for snapshot/hash and Python/JavaScript vector checks. Run `python3 scripts/check_m5_math_release_authority.py` separately to verify the recorded user-directed release decision against the exact source, files, hashes and Apache scope. This checks record consistency, not independent legal execution or scientific approval.

Reference payloads are immutable. Propose corrections through ICSN review with a new version, source pin, hashes, vectors, compatibility notes and license scope. The legacy overwrite command is disabled to protect release immutability; new versions require their own source-release record. Private manifests, commercial sample receipts and dependent tests listed in the manifest remain excluded.

## Independent adoption and registered operation

Apache software permissions remain independent of M5 registration, credentials and Cyrus obligations. Cyrus applies only to expressly designated constitutional materials. Activating a sovereign account through the TitleChain Registry establishes its registered operating context, applicable Cyrus Protocol obligations and ICSN namespace within its verified scope. Independent standards participation and software reuse do not require that activation.

M5's internal ecosystem is operating and internally activated, as clarified by management. External agency/government activation remains separate. Simulations are identified as simulations. This reference profile's release status is distinct from internal ecosystem operation.

## Express software grant

All ten reference files, including the mathematical specification and M5Nash software/schema/vectors, are Apache-2.0 as recorded in SOURCE-RELEASE-AUTHORIZATION.json. No Cyrus conditions are added to them. Separately designated constitutional material retains its own terms.
