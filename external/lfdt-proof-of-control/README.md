# LFDT Proof-of-Control Standard — pinned upstream snapshot

This folder holds an **unmodified** copy of
[Open Verification: the Proof-of-Control Standard for Agents](https://github.com/LFDT-ProofOfControl/ov-poc-standard),
stewarded by the [Advanced AI Society](https://advancedaisociety.org/) and developed as a
Linux Foundation Decentralized Trust community lab.

| | |
| --- | --- |
| Snapshot | [`v0.1/`](v0.1/README.md) — Working Draft v0.1 (public comment until October 30, 2026) |
| Upstream commit | `b8fb01277873d4c176d6cefd5f5e172ae1c3e2c7` (2026-10-07) |
| File manifest | [`UPSTREAM-v0.1.json`](UPSTREAM-v0.1.json) — SHA-256 of every file |
| License | [Apache License 2.0](v0.1/LICENSE.md), © Advanced AI Society and the Proof-of-Control contributors |
| Trademark | "Proof-of-Control Certified" is a protected certification mark. TitleChain Foundation does not use it, and nothing here grants a right to use it. |

## How TitleChain Foundation uses it

- **The snapshot is never edited here.** `tests/validate_proof_of_control_profile.py` fails if
  any file differs from the upstream manifest. Corrections and proposals go upstream, to the
  [ov-poc-standard repository](https://github.com/LFDT-ProofOfControl/ov-poc-standard) or its
  public-comment process.
- **TitleChain additions live elsewhere.**
  [RFC 0002](../../rfcs/0002-proof-of-control-legal-entity-agent-profile.md) is a profile that
  adopts every Proof-of-Control requirement and adds requirements for agents acting for a legal
  entity under an accountable human. Its
  [crosswalk](../../conformance/proof-of-control/README.md) maps all 127 v0.1 requirements.
- **Refreshing the snapshot.** Run
  `python3 scripts/sync_lfdt_proof_of_control.py --source <clone> --commit <sha> --version <label>`
  and update the crosswalk to the new requirement set in the same pull request.

TitleChain Foundation is not the steward of this standard and makes no conformance or
certification claim by including it.
