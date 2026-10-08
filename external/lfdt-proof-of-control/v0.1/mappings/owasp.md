# Crosswalk: OWASP (AISVS, Agentic Top 10, LLM Top 10, AIVSS)

| | |
| --- | --- |
| **Framework type** | Verification standard, threat catalogs, and scoring system (OWASP) |
| **Corpus version** | AISVS v1.0 (June 2026) — [access](https://github.com/OWASP/AISVS) · [corpus provenance](corpus/README.md) |
| **Relationship** | Threat source for the Proof-of-Control threat model; Security-domain alignment target; AISVS is the structural model for this repository |
| **Coding status** | Draft seed coding, single coder (AISVS is the coded document) — [rubric](rubric.md) |

## The Relationship

**OWASP AISVS** is a community-driven catalogue of testable security requirements for AI-enabled systems. The relationship follows the standard's general pattern: AISVS defines *which controls* an AI system should implement and how to test them; Proof-of-Control defines what *openly verifiable evidence* that those controls held at execution must be, graded on the Verifiability Tiers. AISVS has the most exact matches of any coded framework (agentic tool authorization, model supply chain, sandboxing) because it is the closest in spirit — testable, implementable requirements — while its evidence model (operator-run logging and monitoring) still sits below the binary threshold. An AISVS-verified system can additionally claim Proof-of-Control when its control evidence reaches Tier 3+.

**The Top 10s and AIVSS.** The OWASP Top 10 for LLM Applications and the Top 10 for Agentic Applications are two of the three threat catalogs (with [MITRE ATLAS](mitre-atlas.md) and NIST AI 100-2) from which the 29-threat Proof-of-Control threat model is drawn ([Appendix C](../0.1/en/0x92-Appendix-C_Threat-Model.md)). AIVSS appears in the by-domain mapping as a source architectural mechanism for the **Security** domain: it scores AI vulnerability severity, while Proof-of-Control produces the runtime evidence that the corresponding controls held.

## Requirement-Level Mapping (against AISVS v1.0)

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 62%** of the 127 Proof-of-Control requirements (16 exact matches, 63 partial matches, 48 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 5/5 | Exact | AISVS C6 | C6 supply chain requires model provenance, signing and verification comparable in scope and specificity |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 4/4 | Partial | AISVS C1; C8 | C1 training-data traceability and C8 memory provenance cover lineage; no custody chain to the action record |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Substrate attestation not addressed |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Privacy-preserving provenance not addressed |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 3/3 | Partial | AISVS C5; C12 | C5 access control and C12 monitoring cover access logging; no used-vs-disclosed evidence model |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 5/5 | Partial | AISVS C1 | Data-governance requirements touch consent and minimization; runtime enforcement evidence not central |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | ZK/selective-disclosure mechanisms not addressed |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 0/2 | None | — | Evidence-store minimization not addressed |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 0/2 | None | — | Boundary-crossing evidence not addressed |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | Evidence continuity not addressed |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 8/8 | Exact | AISVS C9 | C9 agentic security requires tool authorization, schema validation and least-privilege comparable in scope |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 4/4 | Partial | AISVS C9.4 | C9.4 agent identity and credential requirements partially cover delegation validity |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 4/4 | Partial | AISVS C5; C9.4 | C9.4 agent identity credentials and rotation; principal-to-agent intent binding is specific to Proof-of-Control |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 2/2 | Partial | AISVS C9; C10 | C9/C10 inter-agent and MCP security cover authenticated agent communication |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 4/4 | Partial | AISVS C4 | C4 infrastructure requirements cover environment hardening; attestation evidence not required |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 3/3 | Exact | AISVS C4; C9 | C4/C9 sandboxing requirements for code execution match isolation-proof scope |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 5/5 | Partial | AISVS C4; C5 | C4/C5 key-management expectations; evidence-key custody is specific to Proof-of-Control |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 5/5 | Partial | AISVS C9 | C9 requires mediated tool access; out-of-band evidence-emitting gateway is specific to Proof-of-Control |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 3/4 | Partial | AISVS C12; AISVS C6 | C12 logging requires event-time records; operator-produced. Not reached: 7.2.3. |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 5/5 | Partial | AISVS C12 | C12 log protection; mechanism-generated tamper-evidence not required |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 0/1 | None | — | No trust-assumption disclosure |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 0/2 | None | — | No determinism-boundary analog |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 6/6 | Partial | AISVS C12 | C12 monitoring/alerting covers pipeline failures; fail-closed evidence gating not required |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 3/5 | Partial | AISVS C12; AISVS C6; AISVS C3 | Structured logging expected; no published claim-set schema. Not reached: 7.7.2, 7.7.4. |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No evidence-verifiability grading |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcement concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | No stack-location fields for claims |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 3/3 | Partial | AISVS C12 | C12 expects monitoring coverage across components; not layer-matched evidence |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 0/8 | None | — | Verification levels exist but no conformance-statement regime |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 0/2 | None | — | No trust-assumption disclosure |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 7/7 | Partial | AISVS C12 | C12 continuous monitoring aligns in intent; not tier-validated per-action evidence |

### Gap Analysis (what this framework does not cover)

* **C1.3 Compute Substrate Provenance** — Substrate attestation not addressed
* **C1.4 Privacy-Preserving Provenance** — Privacy-preserving provenance not addressed
* **C2.3 Privacy-Preserving Verification Mechanisms** — ZK/selective-disclosure mechanisms not addressed
* **C2.4 Evidence Handling for Protected Data** — Evidence-store minimization not addressed
* **C3.1 Boundary-Crossing Evidence** — Boundary-crossing evidence not addressed
* **C3.2 Cross-Environment Continuity** — Evidence continuity not addressed
* **C7.2 The Contemporaneous Property** — partially reached; no provision for 7.2.3: No attestation freshness requirement
* **C7.4 The Transparent Property** — No trust-assumption disclosure
* **C7.5 The Determinism Boundary** — No determinism-boundary analog
* **C7.7 The Interoperable Property** — partially reached; no provision for 7.7.2, 7.7.4: Canonicalization unaddressed
* **C8.1 Tier Placement** — No evidence-verifiability grading
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcement concept
* **C9.1 Locating Evidence on the System Surface** — No stack-location fields for claims
* **C10.1 Conformance Claims** — Verification levels exist but no conformance-statement regime
* **C10.2 Trust-Assumption Disclosure** — No trust-assumption disclosure

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
