# Research Basis: 2026 Verifiable-Control Literature

*This companion maps recent academic and architectural research onto the standard: what each
finding validates, what gap it exposes, and what the standard did about it. Sources are cited as
reported in the contributed research synthesis; the working group should verify citations
against the primary literature as part of ratification.*
*[WG-INPUT NEEDED] — the requirement and threat-model additions sourced here are draft; see
[Appendix D, issue 12](../0.1/en/0x93-Appendix-D_Open-Issues.md).*

## Summary: What the Literature Establishes

2026 research converges on the standard's founding claim: attestation-based compliance —
questionnaires, static documentation, point-in-time audits, self-declaration — structurally
fails for probabilistic, multi-agent runtimes. True proof-of-control requires continuous,
machine-verifiable operational evidence. That is the [binary threshold](../0.1/en/0x10-C08-Verifiability-Tiers.md)
argued from the telemetry side.

## Finding-by-Finding Disposition

| # | Finding | Source | What it means for Proof-of-Control | Disposition |
| :---: | --- | --- | --- | --- |
| R1 | **Telemetry-first governance**: compliance as an always-on operating layer — zero-trust telemetry boundaries, ephemeral read-only metadata probes, no ingress of payloads or PII | AI Trust OS (Bandara et al.) | Validates the evidence-minimization requirements ([C2.4](../0.1/en/0x10-C02-Privacy.md), [C7.6](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md)) and the Continuously Monitored stage; its "falsifiable compliance narrative" is the conformance statement made machine-verifiable ([C10.1.7](../0.1/en/0x10-C10-Conformance-and-Disclosure.md)) | Validates existing requirements  <!--aais-allow--> |
| R2 | **Shadow AI discovery**: agents parsing observability streams (LangSmith, Datadog) auto-register undocumented AI systems — you cannot govern what you have not discovered | AI Trust OS (Bandara et al.) | Exposed a scope-gaming gap the CISO review's boundary declaration (C10.1.6) only half closed: a *declared* boundary must be *reconciled* against discovered reality | New requirement **C10.1.8**; new threat "Shadow / undeclared agents" ([Appendix C](../0.1/en/0x92-Appendix-C_Threat-Model.md)) |
| R3 | **Mid-trajectory attack surface**: the primary security surface is inside multi-step tool-calling sequences, not NL inputs/outputs; guardrail efficacy correlates with structural trace parsing (ρ = 0.79 with JSON-validation competence), near zero with NL jailbreak benchmarks; general-purpose reasoners beat dedicated guardrails | TraceSafe-Bench (Chen et al.), 12 risk categories | Validates evidence generation *before, during, and after* tool invocation (C7.1.2) and the interception-boundary architecture; exposes a monitoring-competence gap — a validator that cannot parse structured traces silently under-detects | New requirement **C10.3.7** (validator structured-trace competence); new threat "Trajectory-monitor parsing failure" <!--aais-allow--> |
| R4 | **Skill Composition Risk**: individually benign skills become dangerous when composed — capability flow (0% → 33.6% ASR under composition), trust transfer (>96.5% ASR on 4 of 5 backends), authorization blur (+71.8% risky approvals under contextual contamination); artifact-level vetting is structurally blind to path-level risk | SCR-Bench (Xie et al.) | The strongest challenge to the standard: C4 evaluated each action against its grant, but a *sequence* of individually authorized calls could exceed the authority of its steps. Empirically grounds the existing "context-blind authorization" threat and demands path-aware evaluation | New requirements **C4.1.7** (path-aware authorization context) and **C4.1.8** (no trust transfer into approval state); new threat "Skill composition risk" |
| R5 | **Verification bandwidth economics**: as execution cost falls toward zero, verification becomes the economic bottleneck; scaling agents without scaling verification capacity guarantees systemic failure | Catalini, Hui & Wu | Already the economic core of [Why Verification Matters](why-verification-matters.md); the "verification bandwidth" framing strengthens the case for machine-verifiable evidence over human review | Already cited (Section 2) |
| R6 | **Decentralized identity beyond pairwise**: DIDs alone cannot assert authority; N-party Verifiable Trust Circles (W3C VC Data Model 2.0, Data Integrity Proof Sets) enable composable multi-party governance and membership proofs | Web 7.0 / did7:web7 specification | Extends the C5 identity mechanism set beyond pairwise delegation tokens — relevant to multi-agent chains (C8.3) and the anonymity/pseudonymity open issue (Appendix D, issue 2) | Mechanism added to [Appendix B](../0.1/en/0x91-Appendix-B_Proof-Mechanism-Inventory.md); references in C5 |
| R7 | **Supply-chain control planes**: AI Service Passports and identity-anchored provenance (Catena-X AI Service KIT; EU DSSC data spaces) convert subjective trustworthiness into verifiable cross-organizational provenance | Catena-X; EU DSSC | Live deployment pattern for the C1 provenance chain and C3 portability across administrative domains; the "signed passport" the threat model references, operationalized | References in C1/C3 |
| R8 | **KRI operationalization**: Risk → KRI → Metric → Automated Test → Observability Signal → Threshold → Enforcement Action → Board Evidence, bridging ISO 42001 / NIST AI RMF / EU AI Act to runtime | MindXO Enterprise AI KRI Taxonomy | The enterprise-side consumption pattern for Proof-of-Control evidence: Proof-of-Control supplies the evidence at the "Observability Signal → Board Evidence" end of the chain; complements the adopter roadmap's success metrics | Referenced here and in the [roadmap](roadmap.md) context |
| R9 | **Disclosure ≠ control**: narrative and financial disclosure signals governance awareness but does not prove controls operate | Governance literature (2026) | Restates the standard's core distinction — Tier 1–2 documentation vs Tier 3–4 evidence — from the disclosure side | Validates the binary threshold |

## The Five-Layer Synthesis, Mapped to the Standard

The literature's integrated "proof-of-control stack" corresponds chapter-for-chapter to the
standard — independent convergence on the same architecture:

| Research layer | Standard's counterpart  <!--aais-allow--> |
| --- | --- |
| Telemetry-first discovery (probes, observability extraction, shadow-AI elimination) | [C10.1.6/C10.1.8](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) scope + discovery reconciliation; [C7](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) evidence pipeline |
| Decentralized identity & authority (DIDs, trust circles, service passports) | [C5](../0.1/en/0x10-C05-Identity.md) identity binding; [C4.2](../0.1/en/0x10-C04-Authorization.md) delegation; [C1](../0.1/en/0x10-C01-Provenance.md) provenance |
| Trajectory-aware execution monitoring (structural parsing competence) | [C7.1](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) before/during/after evidence; [C10.3](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) validators |
| Path-aware skill/context vetting (composition state tracking) | [C4.1.7–4.1.8](../0.1/en/0x10-C04-Authorization.md) path-aware authorization |
| Economic verification layer (KRIs mapped to regulation) | [C10.3.6](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) coverage metrics; [mappings/](../mappings/README.md) regulatory coverage  <!--aais-allow--> |

## What the Standard Adds That the Literature Does Not

The synthesis describes *architectures* for continuous verification; the standard contributes
what none of the surveyed work standardizes: the **Verifiability Tiers** (who must be trusted to
believe the telemetry — an AI Trust OS probe is still Tier 2 if you must trust its operator),
the **binary threshold** as a procurable yes/no, **trust-assumption disclosure**, and a
**conformance regime**. Telemetry answers "what happened"; the Tiers answer "why should anyone
outside the organization believe it."

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
