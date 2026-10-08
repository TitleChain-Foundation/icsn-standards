# Crosswalk: EU AI Act

| | |
| --- | --- |
| **Framework type** | Regulation (European Union) |
| **Corpus version** | Regulation (EU) 2024/1689, OJ 12 July 2024 — [access](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) · [corpus provenance](corpus/README.md) |
| **Relationship** | Complementary — Proof-of-Control evidence lets the Act be enforced against evidence rather than filings |
| **Coding status** | Draft seed coding, single coder — [rubric](rubric.md) |

## The Relationship

Rules for AI agents are only as strong as what they can verify. A regulation that asks an operator to attest that its agent behaved rests on assertion; one that can require openly verifiable evidence of what the agent did rests on proof. The Act's high-risk regime already demands the *practices* Proof-of-Control evidences — automatic event recording (Art. 12), technical documentation (Art. 11), human oversight (Art. 14), conformity assessment (Art. 43) — but its records remain operator-produced. Proof-of-Control is what would let a market-surveillance authority check an Art. 12 log without trusting the party that wrote it.

Concretely: regulators today cannot verify that a high-risk system operated within authorized parameters ([the Verifiability Gap](../docs/why-verification-matters.md)); Proof-of-Control evidence at Tiers 3–4 is verifiable by a regulator without privileged access. The Proof-of-Control conformance stages give a graded assessment ladder a conformity-assessment regime can reference, and in the by-domain mapping the Act is the external alignment target for the **Privacy** domain.

## Requirement-Level Mapping

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 51%** of the 127 Proof-of-Control requirements (0 exact matches, 65 partial matches, 62 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 5/5 | Partial | Art. 11; Annex IV | Art 11/Annex IV technical documentation identifies the model and versions; no cryptographic digest binding or signed manifests |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 4/4 | Partial | Art. 10 | Art 10 data governance covers data provenance practices; no hash-linked custody chain to the action record |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | No provision on compute-substrate identification or attestation |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | No provision on privacy-preserving provenance evidence |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 3/3 | Partial | Art. 12 | Art 12 automatic event recording covers data-access logging; used-vs-disclosed distinction and non-exposure of content not required |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 5/5 | Partial | Art. 10 | Art 10 data governance plus GDPR interplay covers purpose/consent obligations; runtime enforcement evidence not required |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | No provision on ZK proofs, selective disclosure, or commitments |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 0/2 | None | — | No provision reconciling erasure obligations with tamper-evident records |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 0/2 | None | — | No boundary-crossing evidence provision |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | No cross-environment evidence-continuity provision |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 8/8 | Partial | Art. 9; Art. 14 | Art 14 human oversight and Art 9 risk controls require authority limits and oversight; gateway-blocked rejection evidence not required |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 0/4 | None | — | No delegation-chain provisions |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 4/4 | Partial | Art. 12; Art. 50 | Art 12 traceability and Art 50 disclosure touch actor identification; no cryptographic principal-to-agent binding |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 0/2 | None | — | No inter-agent identity provisions |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 4/4 | Partial | Art. 15 | Art 15 accuracy/robustness/cybersecurity requires environment controls; attestation vs golden values not required |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 3/3 | Partial | Art. 15 | Art 15 cybersecurity covers isolation expectations generally; no proof-of-isolation requirement |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 0/5 | None | — | No key-lifecycle provisions |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | No action-interception or evidence-at-boundary concept |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 2/4 | Partial | Art. 12 | Art 12 requires automatic recording of events over the lifetime; no operator-independent time anchoring. Not reached: 7.2.3, 7.2.4. |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 5/5 | Partial | Art. 12; Art. 19; Art. 12 | Art 12/19 logging and retention imply record integrity; evidence remains operator-produced (Tier 1 in Proof-of-Control terms) |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 1/1 | Partial | Art. 13 | Art 13 transparency to deployers discloses capabilities and limitations; no trust-assumption disclosure |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 0/2 | None | — | No determinism-boundary or claims-discipline provision |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 6/6 | Partial | Art. 19 | Art 19 log retention covers retention duty; fail-closed and omission-detectability not addressed |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 1/5 | Partial | Art. 11; Annex IV | Technical documentation must be machine-processable for authorities; no evidence-token schema. Not reached: 7.7.2, 7.7.3, 7.7.4, 7.7.5. |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No evidence-verifiability grading concept |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-to-requirement fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcing execution concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | No system-surface location requirement |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | No per-layer evidence coverage requirement |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 5/8 | Partial | Art. 43; Art. 47; Annex V, point 7; Art. 47; Annex V; Art. 11 and Annex IV; Art. 47; Annex V, point 8; Art. 11; Annex IV, sections 1–2; Art. 47(1) | The Act provides conformity-assessment routes and an EU declaration; Annex V identifies a notified body and certificate only where applicable. It does not require one of Proof-of-Control's three named stages or identify a continuous-monitoring regime in the statement. Not reached: 10.1.2, 10.1.3, 10.1.8. |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 2/2 | Partial | Art. 13 | Art 13 requires disclosing limitations and residual risks to deployers; not categorized trust assumptions |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 7/7 | Partial | Art. 72 | Art 72 post-market monitoring requires ongoing surveillance; not per-action evidence validation |

### Gap Analysis (what this framework does not cover)

* **C1.3 Compute Substrate Provenance** — No provision on compute-substrate identification or attestation
* **C1.4 Privacy-Preserving Provenance** — No provision on privacy-preserving provenance evidence
* **C2.3 Privacy-Preserving Verification Mechanisms** — No provision on ZK proofs, selective disclosure, or commitments
* **C2.4 Evidence Handling for Protected Data** — No provision reconciling erasure obligations with tamper-evident records
* **C3.1 Boundary-Crossing Evidence** — No boundary-crossing evidence provision
* **C3.2 Cross-Environment Continuity** — No cross-environment evidence-continuity provision
* **C4.2 Delegation** — No delegation-chain provisions
* **C5.2 Inter-Agent Identity** — No inter-agent identity provisions
* **C6.3 Cryptographic Key Lifecycle** — No key-lifecycle provisions
* **C7.1 Generation at the Action Boundary** — No action-interception or evidence-at-boundary concept
* **C7.2 The Contemporaneous Property** — partially reached; no provision for 7.2.3, 7.2.4: Logging duties do not reach attestation staleness
* **C7.5 The Determinism Boundary** — No determinism-boundary or claims-discipline provision
* **C7.7 The Interoperable Property** — partially reached; no provision for 7.7.2, 7.7.3, 7.7.4, 7.7.5: Canonicalization unaddressed
* **C8.1 Tier Placement** — No evidence-verifiability grading concept
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-to-requirement fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcing execution concept
* **C9.1 Locating Evidence on the System Surface** — No system-surface location requirement
* **C9.2 Layer Coverage** — No per-layer evidence coverage requirement
* **C10.1 Conformance Claims** — partially reached; no provision for 10.1.2, 10.1.3, 10.1.8: No AI Act provision requires a declaration to list Proof-of-Control domains C1–C6 or prohibits unlisted domains from appearing in Proof-of-Control marketing.

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

## Peer Assurance Ladder

| Proof-of-Control Stage | EU peer |
| --- | --- |
| Continuously Monitored | EU Cybersecurity Act (comparable assurance bar) |

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
