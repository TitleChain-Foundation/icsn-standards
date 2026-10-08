# Crosswalk: Zero Trust (NIST SP 800-207; Anthropic Zero Trust for AI Agents)

| | |
| --- | --- |
| **Framework type** | Security architecture (NIST SP 800-207); vendor deployment framework (Anthropic, May 2026) |
| **Corpus version** | NIST SP 800-207, August 2020 (the coded document) — [access](https://csrc.nist.gov/pubs/sp/800/207/final) · [corpus provenance](corpus/README.md) |
| **Relationship** | Complementary — Zero Trust enforces control at runtime; Proof-of-Control shows openly that control held |
| **Coding status** | Draft seed coding, single coder; Anthropic framework not yet coded — [rubric](rubric.md) |

## The Relationship

Zero Trust tells you how to set the controls on an AI agent correctly so a breach is contained; Proof-of-Control gives an outside party evidence that those controls were honored. The architecture's Policy Enforcement Point mediates every access the way Proof-of-Control's Action Interception Gateway does — the exact match in the mapping below — but 800-207 never requires the enforcement to leave operator-independent evidence, which is where every partial match ends.

Adopting Zero Trust does not give you Proof-of-Control. Anthropic's Zero Trust for AI Agents tells you how to set controls so a breach is contained; its own incident write-ups describe data leaving through a *permitted* path, where preventive controls had nothing anomalous to catch. Enforcing control at runtime and showing, openly, that control held afterward are different jobs.

| Anthropic Zero Trust for AI Agents | Proof-of-Control |
| --- | --- | --- |
| What it answers | "Did we set the controls correctly?" | "Can an outside party verify the controls were honored?" |
| When it acts | Mostly at provisioning and identity time; preventive | At and after execution; evidentiary — the evidence outlives the event |
| Certifiable? | No; explicitly guidance, not assurance | Yes; the standard, plus forthcoming independent certification |

## Requirement-Level Mapping (against NIST SP 800-207)

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 43%** of the 127 Proof-of-Control requirements (8 exact matches, 46 partial matches, 73 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 0/5 | None | — | Artifact provenance outside ZTA scope |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 0/4 | None | — | Outside scope |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Outside scope |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Outside scope |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 3/3 | Partial | PEP logging (§3) | Policy enforcement point logging records resource access; no evidence-content model |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 5/5 | Partial | Policy Engine (§3) | Policy engine evaluates per-request context including data policies |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | Not addressed |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 0/2 | None | — | Not addressed |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 2/2 | Partial | Tenets 2–3 (§2.1) | No implicit trust across boundaries; every crossing is re-evaluated, though not evidenced for third parties |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | Evidence continuity not addressed |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 8/8 | Exact | Tenets 3, 4, 6; PEP (§3) | Per-request access evaluation at the PEP with least privilege matches authority-and-scope enforcement |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 4/4 | Partial | Tenet 4 | Dynamic authorization covers authority scoping; delegation chains not addressed |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 4/4 | Partial | Tenet 6 | Strong authentication of all subjects and devices; principal-to-agent intent binding not addressed |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 2/2 | Partial | Tenet 2 | Mutual authentication between services covers inter-agent message authenticity |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 4/4 | Partial | Tenet 5 | Device posture and integrity monitoring inform access decisions; not openly verifiable |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 0/3 | None | — | Isolation proof not addressed |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 0/5 | None | — | Key lifecycle not addressed at this level |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 5/5 | Partial | PEP (§3) | The PEP mediates all access like the interception gateway; evidence emission is not required |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 3/4 | Partial | Tenet 7; Sec. 3.3; Tenet 5 | Continuous monitoring produces execution-time logs; operator-produced. Not reached: 7.2.4. |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | Tamper-evidence of records not required |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 0/1 | None | — | Not addressed |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 0/2 | None | — | Not addressed |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 6/6 | Partial | Deny-by-default posture (§2) | Deny-by-default posture parallels fail-closed; evidence-pipeline gating unspecified |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 1/5 | Partial | Sec. 5.4 | Cryptographic agility discussed for the enterprise; not for evidence records. Not reached: 7.7.1, 7.7.2, 7.7.4, 7.7.5. |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No verifiability grading |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcement concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | Not addressed |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | Not addressed |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 0/8 | None | — | No conformance-claim regime |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 0/2 | None | — | Not addressed |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 7/7 | Partial | Tenet 7; CDM integration | Continuous diagnostics and mitigation align with continuous-operation intent |

### Gap Analysis (what this framework does not cover)

* **C1.1 Model and Artifact Provenance** — Artifact provenance outside ZTA scope
* **C1.2 Input and Data Lineage** — Outside scope
* **C1.3 Compute Substrate Provenance** — Outside scope
* **C1.4 Privacy-Preserving Provenance** — Outside scope
* **C2.3 Privacy-Preserving Verification Mechanisms** — Not addressed
* **C2.4 Evidence Handling for Protected Data** — Not addressed
* **C3.2 Cross-Environment Continuity** — Evidence continuity not addressed
* **C6.2 Isolation and Confidential Execution** — Isolation proof not addressed
* **C6.3 Cryptographic Key Lifecycle** — Key lifecycle not addressed at this level
* **C7.2 The Contemporaneous Property** — partially reached; no provision for 7.2.4: No attestation report-data binding requirement
* **C7.3 The Tamper-Evident Property** — Tamper-evidence of records not required
* **C7.4 The Transparent Property** — Not addressed
* **C7.5 The Determinism Boundary** — Not addressed
* **C7.7 The Interoperable Property** — partially reached; no provision for 7.7.1, 7.7.2, 7.7.4, 7.7.5: Out of scope
* **C8.1 Tier Placement** — No verifiability grading
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcement concept
* **C9.1 Locating Evidence on the System Surface** — Not addressed
* **C9.2 Layer Coverage** — Not addressed
* **C10.1 Conformance Claims** — No conformance-claim regime
* **C10.2 Trust-Assumption Disclosure** — Not addressed

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
