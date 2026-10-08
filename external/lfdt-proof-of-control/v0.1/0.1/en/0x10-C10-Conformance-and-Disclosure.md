# C10 Conformance and Trust-Assumption Disclosure

## Control Objective

Grade how thoroughly a claim of meeting this standard was checked, and make residual trust visible and comparable. Conformance is a separate axis from the Verifiability Tiers: the [binary threshold](0x10-C08-Verifiability-Tiers.md) decides whether a system is Proof-of-Control-conformant at all; the conformance stages grade how that conformance was established, and by whom.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../images/diagrams/conformance-stages-dark.svg">
    <img alt="The three conformance stages: Self-Declared, Third-Party Assessed, Continuously Monitored, with trust-assumption disclosure required at every stage" src="../../images/diagrams/conformance-stages-light.svg" width="880">
  </picture>
</p>

There are three conformance stages. They are named, never numbered:

| Stage | Who checks | Peer certifications at a comparable bar |
| --- | --- | --- |
| **Self-Declared** | The operator attests, in a standardized conformance statement | CSA STAR Level 1, SLSA Level 1, PCI DSS SAQ |
| **Third-Party Assessed** | An accredited assessor examines the system and confirms conformance | CSA STAR Level 2, Common Criteria EAL, FIPS 140 validation, SOC 2 |
| **Continuously Monitored** | Conformance is verified on an ongoing basis rather than at a single point in time | CSA STAR Level 3, NIST Continuous Monitoring, EU Cybersecurity Act |

Until the accredited-assessor body is established, a system is described as *placed* at a conformance stage, not *certified* (see [Governance](../../docs/governance.md)).

---

## C10.1 Conformance Claims

An implementation may make claims in a subset of the six domains; for each domain it claims, it produces evidence for the verifiable facts it asserts.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **10.1.1** | **Verify that** the published conformance statement names its stage — Self-Declared, Third-Party Assessed, or Continuously Monitored — and, for the latter two, identifies the assessor or monitoring regime. | 1 |
| **10.1.2** | **Verify that** the statement lists the domains claimed (of C1–C6), and that domains not listed appear nowhere in the operator's Proof-of-Control marketing for the system. | 1 |
| **10.1.3** | **Verify that** every verifiable fact asserted in the statement resolves to at least one evidence stream in the claim register — no asserted fact without a register entry. | 1 |
| **10.1.4** | **Verify that** the statement contains all required fields: system identification (name, version, environment); domains claimed; per-claim evidence properties met and Tier reached; mechanisms used; and the trust-assumption disclosure. | 1 |
| **10.1.5** | **Verify that** the statement cites the exact version of this standard (e.g., v0.1) and the date of the claim. | 1 |
| **10.1.6** | **Verify that** the statement defines the system boundary (components, environments, interfaces in scope) and the classes of in-scope agent actions, and enumerates excluded action classes with a stated rationale for each exclusion. | 1 |
| **10.1.7** | **Verify that** the statement and its per-claim data are published in a documented, machine-readable format (schema available), so assessors and insurers can compare claims across implementations programmatically. | 2 |
| **10.1.8** | **Verify that** the declared system inventory is reconciled on a defined schedule against automated discovery from operational and observability streams, and that undeclared agent deployments surface as recorded findings rather than remaining shadow systems. *(Research-driven addition — see [Appendix D, issue 12](0x93-Appendix-D_Open-Issues.md).)* | 2 |

**Auditor evidence:** 10.1.1–10.1.5 — the published statement checked field-by-field against the template; sample three asserted facts into the claim register. 10.1.6 — the boundary/scope section; test one excluded action class against the deployed system to confirm the exclusion is real, not evasive. 10.1.7 — retrieve the machine-readable statement and validate it against its schema. 10.1.8 — the discovery tooling configuration and reconciliation reports; seed a test agent outside the declared inventory and confirm it surfaces as a finding.

---

## C10.2 Trust-Assumption Disclosure

Disclosure operationalizes the [Transparent property](0x10-C07-Evidence-Generation-and-Properties.md): it turns a binary yes-or-no into a risk-differentiable profile, which is what makes conformance claims comparable across implementations and useful to the insurers and regulators pricing residual risk. Example — three deployments, all conformant at the Third-Party Assessed stage, with materially different risk profiles:

| Deployment | Trust assumptions | Residual risk |
| --- | --- | --- |
| Healthcare AI agent on Azure | TEE-based (Intel TDX). Trusts Intel silicon manufacturing and Azure physical security. | Hardware supply-chain risk; single-vendor trust dependency, mitigated by Azure's controls and Intel's attestation. |
| Cross-border payment agent | ZK-STARK proofs with transparent setup. Trusts collision-resistant hash functions only; no hardware dependency. | Narrowest trust base, mathematical assumptions only; higher compute cost, no single-entity dependency. |
| Supply-chain verification agent | Groth16 ZK proofs with a multi-party ceremony. Trusts that at least 1 of 47 ceremony participants was honest, and the BN254 curve. | Ceremony trust distributed; well-studied assumptions; moderate residual risk from ceremony integrity. |

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **10.2.1** | **Verify that** the disclosure lists, per claim, each residual trust assumption with the assumption's subject (named vendor, hardware element, mathematical assumption, or ceremony) — matched one-to-one against the mechanisms in the claim register. | 1 |
| **10.2.2** | **Verify that** each disclosed assumption is tagged with one of the defined categories (draft set: Hardware, Mathematical, Ceremony, Vendor, Implementation, Distributed), so disclosures are machine-comparable across implementations. | 2 |

**Auditor evidence:** 10.2.1 — reconcile the disclosure against the mechanism list; any mechanism without a disclosure line is a finding. 10.2.2 — category tags present and drawn from the defined set.

> **[WG-INPUT NEEDED]** — the standardized disclosure format itself is not yet defined; the
> working group must fix a finite set of trust-assumption categories. See
> [Appendix D](0x93-Appendix-D_Open-Issues.md), issue 7.

---

## C10.3 Continuously Monitored Operation

An agent is not something you certify once: a point-in-time check cannot cover a system whose behavior is decided in the moment. These requirements are the working group's starting point for making "on an ongoing basis" concrete enough to certify against.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **10.3.1** | **Verify that** evidence is retained in a store meeting the tamper-evident requirements of [C7.3](0x10-C07-Evidence-Generation-and-Properties.md), with the store's chain-verification results available to the assessor. | 2 |
| **10.3.2** | **Verify that** evidence generation covers every in-scope action rather than a sample — demonstrated by reconciling gateway action counts against evidence-record counts over an audit window, with zero unexplained difference. | 4 |
| **10.3.3** | **Verify that** an automated validator checks each evidence record against its claimed Tier's requirements within the defined validation window, and that validator results are themselves logged. | 4 |
| **10.3.4** | **Verify that** validation failures and coverage gaps raise alerts to a monitored destination within the bounded window defined in the claim, with alert-to-acknowledgment times tracked. | 4 |
| **10.3.5** | **Verify that** the monitoring pipeline itself is re-assessed by a third party on a defined cycle (e.g., annually), and the re-assessment report is available to relying parties. | 4 |
| **10.3.6** | **Verify that** proof coverage — evidence-covered in-scope actions divided by total in-scope actions — is computed on a defined schedule and published with the claim, so coverage decay is visible rather than silent. | 3 |
| **10.3.7** | **Verify that** automated validators used to monitor multi-step execution are evaluated for structured-trace parsing competence (schema and argument validation over tool-call trajectories), not only natural-language safety performance, and that the evaluation results are available to the assessor. *(Research-driven addition — see [Appendix D, issue 12](0x93-Appendix-D_Open-Issues.md).)* | 3 |

**Auditor evidence:** 10.3.1 — chain-verification results for the store. 10.3.2 — run the count reconciliation yourself over a sample window. 10.3.3 — validator configuration and result logs. 10.3.4 — alert records with acknowledgment timestamps. 10.3.5 — the most recent re-assessment report. 10.3.6 — the coverage metric's definition, computation job, and published values. 10.3.7 — the validator's structured-trace evaluation report (e.g., against a trajectory benchmark), including parsing-accuracy metrics on corrupted tool-call sequences.

> **[WG-INPUT NEEDED]** — the operational requirements for the Continuously Monitored stage
> (minimum cadence, automated versus human validation, incident response and suspension) are not
> yet defined. See [Appendix D](0x93-Appendix-D_Open-Issues.md), issue 8.

---

## References

* [CSA STAR](https://cloudsecurityalliance.org/star) · [SLSA levels](https://slsa.dev/spec/v1.0/levels) · [FIPS 140](https://csrc.nist.gov/projects/cryptographic-module-validation-program) — peer assurance ladders
* [Appendix A — Glossary](0x90-Appendix-A_Glossary.md): conformance, conformance stage
* AI Trust OS (Bandara et al., 2026) — telemetry-first discovery and zero-trust metadata probes, the basis for 10.1.8; TraceSafe-Bench (Chen et al., 2026) — validator structured-trace competence, the basis for 10.3.7 ([research basis](../../docs/research-basis.md))
* Crosswalks: [SOC 2](../../mappings/soc-2.md), [EU AI Act](../../mappings/eu-ai-act.md)
* Companion: [Governance](../../docs/governance.md) — the certification and assessor body; [Roadmap](../../docs/roadmap.md) — Phase-by-Phase readiness for each stage
