# Crosswalk: SOC 2

| | |
| --- | --- |
| **Framework type** | Organizational controls attestation (AICPA Trust Services Criteria) |
| **Corpus version** | 2017 TSC with 2022 revised points of focus — [access](https://www.aicpa-cima.com/resources/download/trust-services-criteria) · [corpus provenance](corpus/README.md) |
| **Relationship** | Complementary — Proof-of-Control is SOC-2-grade in role, with a cryptographic stage SOC 2 never had |
| **Coding status** | Draft seed coding, single coder — [rubric](rubric.md) |

## The Relationship

SOC 2 attests that an organization's controls exist and were tested by an auditor; it is institutional assurance about the organization. Proof-of-Control is openly verifiable evidence of what the *system* actually did.

| | SOC 2 | Proof-of-Control |
| --- | --- | --- |
| Question answered | "Did the organization implement the controls it said it would?" | "Did the AI system operate within its defined control boundaries, and can anyone verify?" |
| Subject | The organization | The agent system's execution |
| Evidence | Auditor-tested controls, point-in-time or over a period | Mechanism-generated, tamper-evident, contemporaneous execution evidence |
| Trust required | The auditor and the operator's records | The mechanism and the parties it rests on (Tiers 3–4) |

An insurer or buyer can require Proof-of-Control the way they already require SOC 2 or ISO 27001 — SOC 2 became effectively mandatory through the insurance and procurement chain, the dynamic Proof-of-Control is built to activate for agents ([Insurance is the forcing function](../docs/why-verification-matters.md)). The strongest structural parallel is the claim artifact itself: the SOC 2 system description and management assertion are the direct ancestor of the Proof-of-Control conformance statement (an exact match in the mapping below).

## Requirement-Level Mapping

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 54%** of the 127 Proof-of-Control requirements (0 exact matches, 68 partial matches, 59 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 5/5 | Partial | CC8.1 | CC8 change management and system-component inventory identify what runs; no model digests or signed manifests |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 0/4 | None | — | Data lineage/custody chains not addressed |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Substrate attestation not addressed |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Privacy-preserving provenance not addressed |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 3/3 | Partial | CC6.1; P-series | CC6/CC7 access logging and privacy criteria cover access records; no used-vs-disclosed model |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 5/5 | Partial | P2.1; P4.1 | Privacy criteria P-series require consent, purpose limitation and retention controls at the organizational level |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | Cryptographic privacy mechanisms not addressed |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 2/2 | Partial | P4.2–P4.3 | P4 disposal and retention criteria address deletion; no reconciliation with tamper-evident chains |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 0/2 | None | — | Boundary-crossing evidence not addressed |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | Evidence continuity not addressed |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 8/8 | Partial | CC6.1–CC6.3 | CC6 logical access requires authorization controls; no evidenced per-action gateway decisions |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 0/4 | None | — | Delegation chains not addressed |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 4/4 | Partial | CC6.1–CC6.2 | CC6 identification and authentication of users/systems; no principal-to-agent binding |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 0/2 | None | — | Inter-agent identity not addressed |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 4/4 | Partial | CC7.1–CC7.2 | CC6/CC7 operations monitoring cover control operation; attestation vs reference values not required |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 0/3 | None | — | Isolation proof not addressed |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 5/5 | Partial | CC6.1 | CC6.1 encryption and key management expectations; not evidence-key custody |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | No interception-gateway concept |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 2/4 | Partial | CC7.2 | CC7.2 audit logging is contemporaneous; operator-produced. Not reached: 7.2.3, 7.2.4. |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 5/5 | Partial | CC7.2 | Log protection expectations; signatures/chains not required and operator remains trusted |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 0/1 | None | — | No trust-assumption disclosure analog |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 0/2 | None | — | No determinism-boundary analog |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 6/6 | Partial | CC7.3–CC7.5 | CC7 monitoring and incident handling cover pipeline failures; omission-detectability not addressed |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | No evidence-format requirement |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No verifiability grading |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcement concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | No stack-location requirement |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 3/3 | Partial | CC7.2 | CC7 expects logging coverage of in-scope systems; not layer-matched evidence |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 7/8 | Partial | Management assertion; SOC 2 system description; SOC 2 system description; Management assertion; SOC 2 examination evidence; Management assertion; SOC 2 report period/date; CC7.2; CC8.1 | A SOC 2 engagement includes management's assertion and a scoped system description, but does not require the claim to declare one of Proof-of-Control's stages or name a continuous-monitoring regime. Not reached: 10.1.7. |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 2/2 | Partial | Subservice organizations & CUECs | Subservice-organization and complementary-control disclosures are a partial analog to trust-assumption disclosure |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 7/7 | Partial | Type II operating-effectiveness period | Type II covers a period with operating effectiveness; not per-action near-real-time validation |

### Gap Analysis (what this framework does not cover)

* **C1.2 Input and Data Lineage** — Data lineage/custody chains not addressed
* **C1.3 Compute Substrate Provenance** — Substrate attestation not addressed
* **C1.4 Privacy-Preserving Provenance** — Privacy-preserving provenance not addressed
* **C2.3 Privacy-Preserving Verification Mechanisms** — Cryptographic privacy mechanisms not addressed
* **C3.1 Boundary-Crossing Evidence** — Boundary-crossing evidence not addressed
* **C3.2 Cross-Environment Continuity** — Evidence continuity not addressed
* **C4.2 Delegation** — Delegation chains not addressed
* **C5.2 Inter-Agent Identity** — Inter-agent identity not addressed
* **C6.2 Isolation and Confidential Execution** — Isolation proof not addressed
* **C7.1 Generation at the Action Boundary** — No interception-gateway concept
* **C7.2 The Contemporaneous Property** — partially reached; no provision for 7.2.3, 7.2.4: Not addressed
* **C7.4 The Transparent Property** — No trust-assumption disclosure analog
* **C7.5 The Determinism Boundary** — No determinism-boundary analog
* **C7.7 The Interoperable Property** — No evidence-format requirement
* **C8.1 Tier Placement** — No verifiability grading
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcement concept
* **C9.1 Locating Evidence on the System Surface** — No stack-location requirement
* **C10.1 Conformance Claims** — partially reached; no provision for 10.1.7: SOC 2 does not require that the statement or per-claim data be publicly published in a documented machine-readable schema or be programmatically comparable across implementations.

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

## Peer Assurance Ladder

| Proof-of-Control Stage | SOC 2 peer |
| --- | --- |
| Third-Party Assessed | SOC 2 (alongside CSA STAR Level 2, Common Criteria EAL, FIPS 140 validation) |

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
