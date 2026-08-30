# RFC 0001: Hardware Onboarding Standard — Device Title & Fleet Provisioning

- **Status:** Draft
- **Authors:** Satonaka (Pamela Norton), TitleChain Foundation
- **Created:** 2026-08-26
- **Discussion:** https://github.com/TitleChain-Foundation/icsn-standards/discussions/33
- **Implementation evidence:** none yet — this RFC precedes any pilot deployment

## Summary

This RFC extends the existing IAM → BOM/BOU/BOB account-activation pattern (see [M5isYOU.md](../M5ISYOU.md) and [MEMBERSHIP-AND-ROLES.md](../MEMBERSHIP-AND-ROLES.md)) to physical hardware. It defines how a device, and each of its separable components, receives a TitleChain title bound to an activated identity, and how M5 members building in the commons move from identity activation to being issued trusted, repairable hardware under one onboarding flow. It uses Framework's product line as an illustrative pilot case because its component architecture is unusually legible for this purpose — not as an endorsement or exclusive vendor selection.

## Problem and affected communities

M5 members currently have an account-activation pathway (IAM, then BOM/BOU/BOB) but no standard that connects an activated identity to the hardware it operates from. This affects:

- **Engineering contributors**, who need a repeatable way to be issued a machine whose provenance, components, and software image are verifiable rather than ad hoc.
- **Business members (BOB)**, who need a pattern for tokenizing their own device fleets the way [M5BankBusiness_Equity_M5Ledger.md's M5CapTable pattern](https://github.com/satonakaoshimoto/M5Ecosystem) already covers equity — that pattern lives on the M5Ecosystem side and has no public commons equivalent for physical assets.
- **Hardware vendors** whose products are built around component-level repairability and provenance (the case this RFC uses Framework to illustrate) but who have no public standard describing how to become a credentialed hardware partner.
- **The Foundation itself**, which needs a defensible, repeatable procurement and issuance pattern before committing budget to a contributor hardware fleet.

## Goals and non-goals

### Goals

- Define a device/component title hierarchy that binds to an activated IAM identity.
- Require that no device title issue without an active IAM account, and no fleet/business device title issue without an active BOB account.
- Describe a vendor-neutral hardware-partner onboarding path, illustrated with one pilot case.
- Keep device secrets, identity documents, and private keys out of every published or on-chain record — titles carry signed hashes and credential references only.

### Non-goals

- This RFC does not define the private M5Ecosystem issuance implementation (DID resolver internals, custody execution, attestation signing service). Those remain M5Ecosystem-controlled per [M5ECOSYSTEM-APPROVAL-BOUNDARY.md](../M5ECOSYSTEM-APPROVAL-BOUNDARY.md).
- This RFC does not certify, endorse, or exclusively select Framework or any vendor. A conformant implementation may use any hardware whose components can be individually titled.
- This RFC does not define the financial or tokenomics treatment of hardware assets — that is a separate proposal, parallel to the existing M5CapTable equity pattern.

## Terminology

- **IAM** — Identity Activated Member. The root identity status required before any account or device title can go active.
- **BOM** — Bank of Me. An individual member's personal account.
- **BOU** — Bank of Us. A shared or cohort account.
- **BOB** — Bank of Business. A business-entity account; the tier a hardware vendor partner (e.g., Framework) would onboard into.
- **Root device title** — the top-level TitleChain record for a physical device, anchored to its owner/custodian DID.
- **Component title** — a title for a separable, individually serialized part of a device (mainboard, storage, compute/graphics module, expansion card).
- **Software/agent title** — a title recording a signed image hash and SBOM hash authorizing a specific software release to run on a titled device.

## Specification

### Account gating

1. A root device title MUST NOT be issued to an identity whose `iam_status` is not `active`.
2. A fleet or business-issued device title MUST NOT be issued unless the custodian's `bom_status` (individual) or BOB account status is `active`.
3. Component titles MUST reference a valid, non-revoked root device title.

### Title hierarchy

| TitleChain object | Example provenance fields | Lifecycle event |
|---|---|---|
| Root device title | Device serial, owner DID, custodian DID, issuance date, warranty, location policy, device public key | "Issued to [member]" |
| Mainboard title | Mainboard serial, firmware measurement, CPU/NPU profile, prior device linkage | "Transferred from Device A to Device B" |
| Compute-module title | Module serial, model, memory, driver/firmware attestation, workload authorization profile | "Authorized for regulated inference workload" |
| Storage title | Storage serial, encryption key *reference* (never the key), capacity, wipe certificate, custody status | "Sanitized and reassigned" |
| Expansion-card title | Card ID, port policy, device assignment | "Added to field node" |
| Software/agent title | Signed image hash, SBOM hash, policy version, agent identity, permitted data classes | "Released to verified compute fleet" |
| Service history record | Repair ticket, technician DID, replaced-part lineage, signed test result | "Battery replaced; prior battery retired" |

### What a title MUST NOT contain

A title MUST NOT contain a raw identity document, a government identifier (e.g., an SSN), a chip serial usable to fingerprint a person without consent, a private key, or any device secret. Where a device is linked to a personal credential chain (e.g., phone → licensed-credential → titled asset), only a signed hash or credential reference travels on any published record or ledger; the underlying document or identifier is held off-chain under the holder's own consent-based control, per [M5isYOU's holder-ownership principle](../M5ISYOU.md#holder-ownership-and-approval).

### Onboarding flow

1. **Claim identity** — `username@bankof.me` and/or ENS identity; IAM request submitted.
2. **IAM activation** — `iam_status → active` after credential validation.
3. **Open an account** — BOM (personal) and, if building as a company, BOB (business).
4. **Select hardware from an approved program** — see the illustrative Framework fleet tiers below; a conformant program may substitute any vendor whose components are individually titleable.
5. **Issue the root device title and component titles** per the hierarchy above.
6. **Sign and release the software image** — SBOM hash and signed image hash recorded as the software/agent title before release to the verified fleet.
7. **Record lifecycle events** — repairs, part swaps, transfers, and revocations append to service history; they do not overwrite prior records.

## Human rights, consent and inclusion

- No person is required to hold IAM, BOM, or BOB status to read or implement this standard.
- A device title issued to an individual documents *the device's* provenance, not a claim about the person's worth, identity, or employment status.
- Where a personal identity credential chain (phone, license-linked credential, computer) is used to illustrate the pattern, the holder's affirmative approval is required before any specific instance is published, consistent with M5isYOU's holder-ownership rule. This RFC illustrates the pattern using the Foundation's first IAM+BOM+BOB activation, published with that holder's approval; it does not publish the holder's underlying identity documents or device identifiers.
- Component-level repairability (the property this RFC uses Framework to illustrate) directly serves accessibility and economic-inclusion goals: lower entry cost via DIY/refurbished tiers, and no forced hardware replacement cycle.

## Privacy and security

- **Threat actors:** a compromised device, a coerced custodian, a supply-chain-tampered component, an attacker attempting to correlate device titles back to a real-world identity.
- **Trust boundaries:** the public title (this standard) carries only hashes and references; the private credential/document store and signing keys remain inside M5Ecosystem-controlled systems, outside this repository's boundary.
- **Data minimization:** titles record what changed and when, not raw identifiers. Storage titles explicitly reference (not embed) encryption keys.
- **Revocation:** component titles support explicit revocation events (e.g., "Sanitized and reassigned," "prior battery retired") so a compromised or decommissioned component cannot silently retain authorization.
- **Correlation risk:** because a device title is bound to a DID, a poorly scoped implementation could let an observer correlate a member's device fleet to their identity across contexts. Implementations MUST support selective disclosure of title records rather than a single public device registry.
- **Failure modes:** loss of the custodian's signing key must have a documented recovery path (out of scope for this RFC; tracked as an open question below) that does not require re-exposing the original identity documents.

## Sovereignty and governance

This RFC does not create Foundation authority over a member's own devices; it defines a shared format for provenance and custody records that a member, a business account, or the Foundation may choose to use. Jurisdictional treatment of hardware ownership, warranty, and repair rights is governed by applicable local law and is not altered by holding a TitleChain device title. No implementation of this standard grants the implementer standards authority, per [GOVERNANCE.md](../GOVERNANCE.md)'s independence clause.

## M5Agent and automation impact

- [x] No. This RFC does not create or materially affect automated authority.

Automated systems may assist with SBOM-hash computation and firmware-measurement capture during issuance (step 5–6 above), but MUST NOT independently decide whether a title issues, transfers, or is revoked — those remain human/steward decisions per [M5AGENT_OPERATIONS.md](../M5AGENT_OPERATIONS.md).

## Interoperability and migration

- Depends on the existing IAM/BOM/BOU/BOB account-activation pathway (M5isYOU, MEMBERSHIP-AND-ROLES.md) already defined in this repository.
- Depends on M5Ecosystem-controlled identity/credential tooling (DID resolver, verifiable-credential issuance) for actual title issuance — that binding does not yet exist and is listed as an open gap below.
- Parallels, but does not depend on, the M5CapTable equity-tokenization pattern used for cap-table assets on the M5Ecosystem side.

## Conformance

An implementation conforms to this RFC if it can demonstrate, for at least one issued device:

1. A root device title bound to an active IAM identity's DID.
2. At least one component title independently traceable to the root title.
3. A software/agent title recording a signed image hash prior to the device's release to service.
4. At least one recorded lifecycle event (transfer, repair, or revocation) that does not overwrite prior history.
5. No raw identity document, government identifier, private key, or device secret present in any published title record.

## Reference implementations

None deployed yet. This RFC is published before any pilot deployment. [`initiatives/HARDWARE-FLEET-PILOT.md`](../initiatives/HARDWARE-FLEET-PILOT.md) sketches one illustrative implementation — a small contributor fleet issuance (illustrative sizing only, not a committed budget) using Framework hardware as one example of a component-legible vendor — to make the title hierarchy concrete for review. It is explicitly non-normative; no single vendor or implementation defines this RFC.

## Alternatives considered

- **Asset-tag/serial tracking without titles:** simpler, but does not produce a portable, verifiable, custody-transferable record, and does not support component-level lifecycle events.
- **Vendor-proprietary device management (MDM) as the system of record:** rejected because it concentrates provenance inside a single vendor's platform, contrary to this repository's non-capture principle.
- **Treating the whole device as a single non-decomposed title:** simpler, but loses the ability to record component-level repair and replacement — the primary reason a repairable-hardware philosophy is worth standardizing around at all.

## Open questions

- What is the recovery path when a custodian loses their signing key, without requiring re-disclosure of the original identity documents?
- Should a business-issued (BOB) fleet title and a personally-issued (BOM) device title share one schema, or diverge where employment/equipment-return terms differ from personal ownership?
- What conformance evidence is sufficient for a hardware vendor to be recognized as a credentialed M5BankofBusiness hardware partner, and who reviews that evidence?
- Should the title hierarchy's "compute-module title" fields differ for CPU-integrated vs. discrete/removable modules (relevant for laptops without a separable graphics module)?

## Decision record

- 2026-08-26 — Initial Draft opened for public review.
