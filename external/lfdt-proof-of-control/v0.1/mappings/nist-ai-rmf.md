# Crosswalk: NIST AI RMF

| | |
| --- | --- |
| **Framework type** | AI risk-management / governance framework (NIST) |
| **Corpus version** | AI RMF 1.0 (NIST AI 100-1, January 2023) — [access](https://www.nist.gov/itl/ai-risk-management-framework) · [corpus provenance](corpus/README.md) |
| **Relationship** | Complementary — Proof-of-Control produces the runtime evidence that makes RMF-aligned controls verifiable |
| **Coding status** | Draft seed coding, single coder — [rubric](rubric.md) |

## The Relationship

NIST AI RMF governs how organizations identify, measure, and manage AI risk through its four functions (GOVERN, MAP, MEASURE, MANAGE). Governance frameworks tell an organization *what to manage*; they do not, by themselves, produce open evidence of what an agent did that holds when the operator is the threat. Proof-of-Control produces the evidence the RMF consumes: the openly verifiable, tamper-evident record that lets an RMF-aligned control be *verified* by a party that need not trust the operator.

This is visible in the mapping below: the RMF has the **highest coverage of any coded framework, yet zero exact matches** — it asks for nearly every control Proof-of-Control verifies, and never for operator-independent evidence of them. That pattern is the binary threshold, seen from the outside.

**NIST AI 100-2** (Adversarial Machine Learning taxonomy) is, separately, one of the three threat catalogs the Proof-of-Control threat model draws from ([Appendix C](../0.1/en/0x92-Appendix-C_Threat-Model.md)), alongside [MITRE ATLAS](mitre-atlas.md) and the [OWASP Top 10s](owasp.md).

## Requirement-Level Mapping

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 59%** of the 127 Proof-of-Control requirements (0 exact matches, 75 partial matches, 52 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 5/5 | Partial | MAP 2.3; GOVERN 1.6 | MAP function calls for provenance and documentation of models; no cryptographic binding |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 4/4 | Partial | MAP 2.3; MEASURE 2.8 | MAP/MEASURE cover data documentation and lineage practices; no hash-linked custody chain |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Compute-substrate attestation not addressed |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Privacy-preserving provenance not addressed |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 3/3 | Partial | MEASURE 2.10 | MEASURE privacy risk and GOVERN accountability cover access recording; no used-vs-disclosed evidence model |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 5/5 | Partial | GOVERN 1.1; MANAGE 1.3 | GOVERN/MANAGE address privacy values and controls; runtime enforcement evidence not required |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 3/3 | Partial | MEASURE 2.10 | RMF profiles reference privacy-enhancing technologies; no verifiable-evidence requirement |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 0/2 | None | — | Evidence-store handling of protected data not addressed |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 0/2 | None | — | Boundary-crossing evidence not addressed |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | Evidence continuity across environments not addressed |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 8/8 | Partial | GOVERN 2.1; GOVERN 3.2 | GOVERN roles/authority and MANAGE controls cover authority definition; no evidenced per-action evaluation |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 0/4 | None | — | Delegation chains not addressed |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 4/4 | Partial | GOVERN 2.1; GOVERN 4.1 | GOVERN accountability requires attributable actors; no cryptographic principal binding |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 0/2 | None | — | Inter-agent identity not addressed |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 4/4 | Partial | MEASURE 2.7 | MEASURE secure-and-resilient characteristic covers environment integrity aims; attestation not required |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 3/3 | Partial | MEASURE 2.7 | Secure-and-resilient characteristic covers isolation expectations generally |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 0/5 | None | — | Key lifecycle not addressed (delegated to security control catalogs) |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | No action-interception evidence concept |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 2/4 | Partial | MEASURE 2.8; MANAGE 4.1 | MEASURE documentation and test records are contemporaneous practices; no mechanism-generated evidence. Not reached: 7.2.3, 7.2.4. |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 4/5 | Partial | MEASURE 2.8 | Traceability and documentation expectations; records remain operator-produced. Not reached: 7.3.5. |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 1/1 | Partial | GOVERN 4.2; MAP 4.1 | Transparency and documentation of limitations align with disclosure; no standardized trust-assumption format |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 2/2 | Partial | MEASURE 2.5 | RMF's validity/reliability framing distinguishes measured facts from aspirations; no claims-discipline requirement |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 6/6 | Partial | MANAGE 2.3; MANAGE 4.1 | MANAGE incident response and monitoring cover failure handling; fail-closed evidence gating not addressed |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 1/5 | Partial | GOVERN 4.2 | Documentation expectations; no machine-readable evidence format. Not reached: 7.7.2, 7.7.3, 7.7.4, 7.7.5. |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No evidence-verifiability grading |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcing execution concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 3/3 | Partial | MAP 1.1 | MAP requires system context/scope mapping; not per-claim stack location |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | Per-layer evidence coverage not addressed |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 8/8 | Partial | GOVERN 4.2 | GOVERN transparency artifacts and RMF profiles resemble scoped claims; no standardized statement |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 2/2 | Partial | MANAGE 1.4 | MANAGE requires documenting residual risk; not categorized trust assumptions |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 7/7 | Partial | MANAGE 4.1 | MANAGE continuous monitoring aligns in intent; per-action near-real-time validation not specified |

### Gap Analysis (what this framework does not cover)

* **C1.3 Compute Substrate Provenance** — Compute-substrate attestation not addressed
* **C1.4 Privacy-Preserving Provenance** — Privacy-preserving provenance not addressed
* **C2.4 Evidence Handling for Protected Data** — Evidence-store handling of protected data not addressed
* **C3.1 Boundary-Crossing Evidence** — Boundary-crossing evidence not addressed
* **C3.2 Cross-Environment Continuity** — Evidence continuity across environments not addressed
* **C4.2 Delegation** — Delegation chains not addressed
* **C5.2 Inter-Agent Identity** — Inter-agent identity not addressed
* **C6.3 Cryptographic Key Lifecycle** — Key lifecycle not addressed (delegated to security control catalogs)
* **C7.1 Generation at the Action Boundary** — No action-interception evidence concept
* **C7.2 The Contemporaneous Property** — partially reached; no provision for 7.2.3, 7.2.4: Not addressed
* **C7.3 The Tamper-Evident Property** — partially reached; no provision for 7.3.5: No log-consistency requirement
* **C7.7 The Interoperable Property** — partially reached; no provision for 7.7.2, 7.7.3, 7.7.4, 7.7.5: Canonicalization unaddressed
* **C8.1 Tier Placement** — No evidence-verifiability grading
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcing execution concept
* **C9.2 Layer Coverage** — Per-layer evidence coverage not addressed

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

## Peer Assurance Ladder

| Proof-of-Control Stage | NIST peer |
| --- | --- |
| Continuously Monitored | NIST Continuous Monitoring |

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
