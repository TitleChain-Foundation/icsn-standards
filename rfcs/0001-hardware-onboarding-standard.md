# RFC 0001: Hardware Onboarding Standard — Device Title & Fleet Provisioning

- **Status:** Draft
- **Authors:** Satonaka (Pamela Norton), TitleChain Foundation
- **Created:** 2026-08-26
- **Implementation evidence:** none yet — this RFC precedes pilot deployment

## Summary

This RFC extends the human-rooted M5 reference sequence to physical hardware:

```text
M5IAM → TCID/M5HUM → owner/custodian authority → TitleChain device title → component lifecycle evidence
```

A device and each separable component may receive a TitleChain record bound to an authorized owner/custodian reference while private identity documents, keys, and sensitive device secrets remain outside public records.

## Goals

- Define a root-device/component title hierarchy.
- Bind issuance to an accountable identity/entity and current authority.
- Preserve provenance across repair, transfer, reassignment, and retirement.
- Keep secrets and raw identity data out of published title records.
- Remain vendor-neutral and repairability-friendly.

## Title hierarchy

| Object | Example evidence | Lifecycle event |
| --- | --- | --- |
| Root device title | serial/reference, owner/custodian ref, issue date, device key ref | issued / transferred |
| Mainboard title | serial, firmware measurement, prior device linkage | moved between devices |
| Compute-module title | model, firmware/driver attestation, workload profile | authorized / revoked |
| Storage title | serial, encryption-key reference, wipe certificate | sanitized / reassigned |
| Expansion title | component ID and assignment | added / removed |
| Software/agent title | signed image hash, SBOM hash, policy version, agent ref | released / revoked |
| Service history | repair ticket, technician authority, replaced-part lineage | append-only service event |

## Privacy

No public title should contain raw identity documents, government identifiers, private keys, secrets, or unnecessary correlatable identifiers. Private evidence remains holder-controlled; published records carry only the minimum references/proofs needed for provenance and verification.

## Authority

Issuance, transfer, repair certification, software release, and revocation are distinct capabilities. An M5AGT may assist only within a current delegation and the Six-Gate control model.

## Conformance

A conforming implementation can demonstrate a root title, at least one component title, software/SBOM evidence where applicable, an append-only lifecycle event, and absence of prohibited private data from the published record.
