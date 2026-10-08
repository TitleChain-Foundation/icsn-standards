# Crosswalk: ISO/IEC 42001

| | |
| --- | --- |
| **Framework type** | AI management system standard (ISO/IEC) |
| **Corpus version** | ISO/IEC 42001:2023 — [access](https://www.iso.org/standard/81230.html) · [corpus provenance](corpus/README.md) |
| **Relationship** | Complementary — Proof-of-Control evidences that declared AIMS controls held at execution; Proof-of-Control borrows its verification/validation vocabulary |
| **Coding status** | Draft seed coding, single coder — [rubric](rubric.md) |

## The Relationship

ISO/IEC 42001 defines the management system (AIMS) through which an organization governs its AI: policies, roles, documented information, impact assessment, and continual improvement. Like other management-system standards, it establishes *that controls exist and are managed*; Proof-of-Control supplies the open, tamper-evident evidence that those controls *held at execution*, verifiable by a party that need not trust the operator. An organization certified to 42001 can use Proof-of-Control evidence to demonstrate — with mechanism-generated records rather than management assertion — that its declared controls operated as designed.

**Verification, not validation.** Proof-of-Control adopts the systems-engineering distinction as used by ISO/IEC 42001 and IEEE: *verification* asks whether the system was built and run right (did it execute within authorized boundaries — Proof-of-Control delivers this); *validation* asks whether it was the right system (whether the boundaries and outputs were the correct choice — a human responsibility). See [C7.5](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md).

## Requirement-Level Mapping

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 57%** of the 127 Proof-of-Control requirements (0 exact matches, 72 partial matches, 55 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 5/5 | Partial | Annex A.4; Cl. 7.5 | Annex A resources/data controls require model documentation and versioning; no digest binding |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 4/4 | Partial | Annex A.7 | Data management controls cover provenance and quality records; no hash-linked custody |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Substrate attestation not addressed |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Privacy-preserving provenance not addressed |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 3/3 | Partial | Annex A.7; Cl. 7.5 | AIMS records and data management cover access documentation; no evidence-content constraints |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 5/5 | Partial | Annex A.5; Annex A.7 | Data management and impact-assessment controls cover purpose and consent obligations |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | Cryptographic privacy mechanisms not addressed |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 0/2 | None | — | Erasure-vs-immutability reconciliation not addressed |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 0/2 | None | — | Boundary-crossing evidence not addressed |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | Evidence continuity not addressed |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 8/8 | Partial | Annex A.9 | Human oversight and resource-authority controls; no evidenced per-action evaluation |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 0/4 | None | — | Delegation chains not addressed |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 4/4 | Partial | Cl. 5.3; Annex A.3 | Roles, responsibilities and accountability controls; no cryptographic binding |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 0/2 | None | — | Inter-agent identity not addressed |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 4/4 | Partial | Cl. 8 (via ISO/IEC 27001 alignment) | Security controls via ISO 27001 alignment cover environment integrity; attestation not required |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 0/3 | None | — | Isolation proof not addressed |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 5/5 | Partial | ISO/IEC 27001 cryptographic controls (adjunct) | 27001-aligned cryptographic control expectations (key management) without evidence-key specificity |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | No action-interception concept |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 2/4 | Partial | Cl. 7.5.3 | Documented-information controls require contemporaneous records; operator-produced. Not reached: 7.2.3, 7.2.4. |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 4/5 | Partial | Cl. 7.5.3 | Records control protects integrity of documented information; not mechanism-generated. Not reached: 7.3.4. |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 1/1 | Partial | Annex A.8 | Transparency and reporting controls; no trust-assumption format |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 2/2 | Partial | Cl. 9.1 | 42001 adopts the verification/validation distinction Proof-of-Control builds on; no claims-review requirement |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 6/6 | Partial | Cl. 7.5.3 | Records retention and control of documented information; fail-closed not addressed |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 2/5 | Partial | Cl. 7.5.2; Cl. 8.1 (A.8 cryptography) | Documented information must have suitable format and identification; not a validatable schema. Not reached: 7.7.2, 7.7.4, 7.7.5. |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No verifiability grading |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcement concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 3/3 | Partial | Cl. 4.3 | AIMS scoping requires defining system boundaries; not per-claim layer fields |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | Layer-matched evidence not addressed |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 5/8 | Partial | Cl. 4.3; Cl. 6.1.3 d); Cl. 7.5.2; Cl. 7.5.3; Cl. 4.3 | Scope and the statement of applicability provide partial management-system conformance documentation, but do not require Proof-of-Control’s three claim stages or identification of an assessor/monitoring regime. Not reached: 10.1.3, 10.1.7, 10.1.8. |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 2/2 | Partial | Cl. 6.1; Statement of Applicability | Statement of applicability and risk treatment disclose residuals; not categorized trust assumptions |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 7/7 | Partial | Cl. 9.2–9.3; Cl. 10 | Internal audit and continual improvement provide ongoing checking; not per-action validation |

### Gap Analysis (what this framework does not cover)

* **C1.3 Compute Substrate Provenance** — Substrate attestation not addressed
* **C1.4 Privacy-Preserving Provenance** — Privacy-preserving provenance not addressed
* **C2.3 Privacy-Preserving Verification Mechanisms** — Cryptographic privacy mechanisms not addressed
* **C2.4 Evidence Handling for Protected Data** — Erasure-vs-immutability reconciliation not addressed
* **C3.1 Boundary-Crossing Evidence** — Boundary-crossing evidence not addressed
* **C3.2 Cross-Environment Continuity** — Evidence continuity not addressed
* **C4.2 Delegation** — Delegation chains not addressed
* **C5.2 Inter-Agent Identity** — Inter-agent identity not addressed
* **C6.2 Isolation and Confidential Execution** — Isolation proof not addressed
* **C7.1 Generation at the Action Boundary** — No action-interception concept
* **C7.2 The Contemporaneous Property** — partially reached; no provision for 7.2.3, 7.2.4: No attestation refresh requirement
* **C7.3 The Tamper-Evident Property** — partially reached; no provision for 7.3.4: Records control does not reach proof structure
* **C7.7 The Interoperable Property** — partially reached; no provision for 7.7.2, 7.7.4, 7.7.5: Canonicalization unaddressed
* **C8.1 Tier Placement** — No verifiability grading
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcement concept
* **C9.2 Layer Coverage** — Layer-matched evidence not addressed
* **C10.1 Conformance Claims** — partially reached; no provision for 10.1.3, 10.1.7, 10.1.8: ISO/IEC 42001 does not require every published verifiable fact to resolve to an evidence stream in a claim register.

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
