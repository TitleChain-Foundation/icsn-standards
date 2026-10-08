# Proof-of-Control crosswalk (RFC 0002)

[`crosswalk-poc-v0.1.json`](crosswalk-poc-v0.1.json) maps every requirement of the
[LFDT Proof-of-Control Standard v0.1](../../external/lfdt-proof-of-control/README.md) to
[RFC 0002](../../rfcs/0002-proof-of-control-legal-entity-agent-profile.md).

| Field | Meaning |
| --- | --- |
| `profile_disposition` | `ADOPTED` — required unchanged by the profile. `ADOPTED_AND_EXTENDED` — required unchanged and extended by the LE requirements listed in `extended_by`. |
| `m5_implementation.status` | Status of the M5 implementation, which is **implementation-specific, external, and subject to separate terms**. Recorded only where checked against code; otherwise `NOT_ASSESSED`. |

Current totals: 127 requirements adopted, 26 extended; M5 has 9 `PARTIAL`, 1 `GAP`, and 117
`NOT_ASSESSED`.

Regenerate with `python3 scripts/build_poc_crosswalk.py`.
`python3 tests/validate_proof_of_control_profile.py` checks that the snapshot is unmodified,
the crosswalk is current and complete, and RFC 0002's requirement tables match it.
