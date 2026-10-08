# Section 8 — Mapping to Existing Standards (informative)

***This section answers:*** *How does it relate to existing standards? — The standards mapping,
classified by domain and still in progress: the AARM and CSA complementary halves, plus NIST AI
RMF, ISO/IEC 42001, SOC 2, OWASP, the EU AI Act, and others, cross-referenced, not replaced.*

> **[DRAFT] — mapping in progress.** The working group has begun mapping how Proof-of-Control
> relates to existing standards and efforts, and that work is ongoing. This section holds the
> current state; the full mapping will be inserted as it matures. Per-framework crosswalks live
> in the repository's [`mappings/`](../mappings/README.md) directory.

Proof-of-Control cross-references existing efforts rather than replacing them. The field is full
of valuable work, governance frameworks, control catalogs, attestation regimes, and vendor
toolkits, and almost none of it produces open evidence of what an agent did that holds
when the operator is the threat. Proof-of-Control is what produces the evidence, alongside these
efforts and feeds them.

## How We Are Classifying the Mapping

The working group is classifying the mapping by domain of verification (an approach proposed by
Jim Schwoebel of Quome) and mapping it as a graph (led by David Thomson of Tesseract), which
reads more simply than an effort-by-effort list: for each domain, it shows the architectural
mechanisms that produce the evidence and the external standards to align with.

| Domain | Source architectural mechanism | Targets for external alignment |
| --- | --- | --- |
| Provenance | *working group to complete* | *to complete* |
| Privacy | TEEs, local-only inference enclaves | HIPAA / HAARF data governance, [EU AI Act](../mappings/eu-ai-act.md) conformance |
| Portability | Agent Resource Discovery Spec, Open Handshakes | [AIUC-1](../mappings/aiuc-1.md) cross-platform auditing |
| Authorization | Cryptographic hash chains, ZKML (Jim's "Verifiability" row, to reconcile) | [SOC 2 Type II](../mappings/soc-2.md) (proving runtime execution matched policy) |
| Identity | W3C CID, WIMSE / IETF AI-Auth | HAARF audit logs, CSA Vanta Agent Trust Controls (who authorized the agent?) |
| Security | [OWASP AIVSS](../mappings/owasp.md), SSF / CAEP | [OWASP Top 10 for Agentic AI](../mappings/owasp.md), [NIST AI RMF](../mappings/nist-ai-rmf.md) |

## Where Proof-of-Control Sits in the Verifiable-AI Landscape

Verifiable AI is the part of AI Security concerned with evidence of what AI systems did: a
territory within the established AI Security category, spanning several areas, each verifying a
different question. Knowing which area answers which question prevents confusion about what the
standard covers.

| Area | The question it answers | When it applies |
| --- | --- | --- |
| Cryptographic inference (ZKML) | Which model actually ran? | Point-in-time, per inference |
| Confidential computing (TEEs) | Was the data protected? | Runtime, during execution |
| Formal verification | What can the system do? | Pre-deployment |
| Mechanistic interpretability | Why did it produce this? | Pre-deployment and research |
| Content provenance (C2PA) | Where did content originate? | Point-in-time, per artifact |
| Identity and credentials | Who authorized what? | Runtime |
| Governance architecture | What controls apply? | Pre-deployment and ongoing |
| **Proof-of-Control** | **Can anyone verify what it did?** | **At and after execution; continuous at the top Stage; the evidence outlives the event** |

Cryptographic inference proofs (ZKML) verify that a specific model processed specific data. They
answer "did I get the model I paid for?" (players include Modulus Labs, Ritual, Giza).
Confidential computing (TEEs) verifies that code ran in a secure, isolated hardware environment,
answering "was my data protected from the infrastructure operator?" (NVIDIA, Microsoft Azure,
Google Cloud, Intel). Formal verification establishes what a model is mathematically bounded to
do, answering "can I guarantee this system never violates this property?" (Axiom, Harmonic, AWS
Automated Reasoning, Theorem). Mechanistic interpretability reveals what happens inside the model
when it decides, answering "why did it produce this output?" (Goodfire, Anthropic's
interpretability team). Content provenance (C2PA) verifies the origin and edit history of media;
identity and credentials verify who authorized what; governance architecture provides structural
controls. Each is real, each is valuable, each answers a different question.

The standard does not try to standardize all of these. It addresses the one question no other
standard currently answers: can you produce verifiable evidence of what your AI system did at
runtime, generated at the moment of execution and verifiable by any third party?

Two boundaries matter. Formal verification establishes what a system *can* do and
interpretability reveals *how it works*; Proof-of-Control shows what it *did* do. A system can be
formally verified and lack Proof-of-Control, and vice versa. They answer different questions for
different stakeholders at different points in the lifecycle. And cryptographic inference proofs,
TEE attestation, consensus timestamps, and verifiable computation are *mechanisms* that can
deliver Proof-of-Control; the standard defines the *property* those mechanisms must produce
(binary, contemporaneous, tamper-evident, transparent), not which mechanism to use. A mature
governance posture may combine formal verification for pre-deployment bounds, interpretability
for model understanding, and Proof-of-Control for evidence of what the system actually did. They
are complementary; the standard addresses the part no one else is standardizing.

## Comparing to Peer Certifications

Every category-defining standard used a binary threshold and a small ladder of assurance. The
Proof-of-Control Stages sit alongside familiar peers, which is the credibility anchor for the
design.

| Proof-of-Control Stage | Peer certifications at a comparable bar |
| --- | --- |
| Self-Declared | CSA STAR Level 1, SLSA Level 1, PCI DSS SAQ |
| Third-Party Assessed | CSA STAR Level 2, Common Criteria EAL, FIPS 140 validation, SOC 2 |
| Continuously Monitored | CSA STAR Level 3, NIST Continuous Monitoring, EU Cybersecurity Act |

## How This Differs from SOC 2

SOC 2 attests that an organization's controls exist and were tested by an auditor; it is
institutional assurance about the organization. Proof-of-Control is openly verifiable
evidence of what the system actually did. SOC 2 answers "did the organization implement the
controls it said it would?"; Proof-of-Control answers "did the AI system operate within its
defined control boundaries, and can anyone verify?" The two are complementary: Proof-of-Control
is SOC-2-grade in role, with a cryptographic Stage SOC 2 never had, and an insurer or buyer can
require it the way they already require SOC 2 or ISO 27001. It does not replace SOC 2; it fills
a gap SOC 2 was not designed to address for AI agents. See the
[SOC 2 crosswalk](../mappings/soc-2.md). **[INSERT]**
**[WG-INPUT NEEDED] Volunteer needed to develop out the crosswalk.**

## The AARM Complementary Mapping: Enforcement and Evidence

CSA's AARM (Autonomous Action Runtime Management, contributed by Vanta) defines runtime
enforcement: it intercepts agent actions at the boundary and approves, modifies, defers, or
denies them. Proof-of-Control defines the open, tamper-evident evidence of what the agent
did. Enforcement and evidence are complementary halves of agentic assurance, designed to compose,
and Proof-of-Control is not a competing runtime control. See the
[AARM crosswalk](../mappings/csa-aarm.md).

| AARM (runtime enforcement) | Proof-of-Control (open evidence) |
| --- | --- | --- |
| Question | What may the agent do at the action boundary? | What did the agent actually do, and can anyone verify it? |
| When | At execution, before the action | At execution, producing evidence of the action |
| Trust | Operator-run enforcement and audit trail | Independent, tamper-evident, verifiable by others |
| Role | The enforcement half | The evidence half |
| Scope | Agent actions inside one deployment (the runtime gateway) | System-wide and portable, across vendors, systems, and jurisdictions |
| Certifiable? | Yes; a vendor-neutral CSA standard with a conformance regime and independent review | Yes; the standard, plus forthcoming independent certification |

Where they meet: AARM mints the tamper-evident receipt at the runtime gateway inside one
deployment; Proof-of-Control carries that evidence outward and makes it openly verifiable
across organizations, for an auditor, insurer, or regulator. AARM enforces and records;
Proof-of-Control shows, openly, what the system did.

## Zero Trust for AI Agents

Zero Trust tells you how to set the controls on an AI agent correctly so a breach is contained.
Proof-of-Control gives an outside party evidence that those controls were honored. Zero Trust
enforces control at runtime; Proof-of-Control shows, openly, that control held afterward.
Complementary, not competing. See the [Zero Trust crosswalk](../mappings/zero-trust.md).

Adopting Zero Trust does not give you Proof-of-Control. Anthropic's Zero Trust for AI Agents
tells you how to set the controls on an agent so a breach is contained; it does not produce
open, portable evidence that those controls were honored. Anthropic's own incident
write-ups describe data leaving through a permitted path, where the preventive controls had
nothing anomalous to catch. Enforcing control at runtime and showing, openly, that control
held afterward are different jobs, and the second is the gap this standard closes.

| Anthropic Zero Trust for AI Agents | Proof-of-Control |
| --- | --- | --- |
| What is it? | A vendor-published security framework for deploying agents (May 2026) | A standard and technical foundation for openly verifiable evidence of what AI systems did |
| What it answers | "Did we set the controls correctly?" | "Can an outside party verify the controls were honored?" |
| When it acts | Mostly at provisioning and identity time; preventive. Its top tier adds continuous authorization | At and after execution; evidentiary. The evidence outlives the event |
| Scope | Agent deployments | System-wide, not model-only |
| Certifiable? | No; explicitly guidance, not assurance | Yes; the standard, plus forthcoming independent certification |

**[WG-INPUT NEEDED] Volunteer needed to develop out the crosswalk.**

## How This Differs from Confidential Computing

Confidential Computing is a mechanism; Proof-of-Control is a property. Confidential Computing
protects data in use inside a Trusted Execution Environment and produces a hardware-signed
attestation that code ran untampered. Under this standard, TEE attestation is one valid mechanism
for delivering Proof-of-Control, primarily in the Security domain, but on its own it does not
cover Identity, Portability, Authorization, or the full record of what the agent did, and it
carries no conformance framework. Confidential Computing is to Proof-of-Control what a deadbolt
is to a home-security standard: real and worth having, but not the system. Complementary, not
competitive; the Confidential Computing Consortium is a natural partner. See the
[Confidential Computing crosswalk](../mappings/confidential-computing.md). **[INSERT]**
**[WG-INPUT NEEDED] Volunteer needed to develop out the crosswalk.**

## MAESTRO in the Mapping

MAESTRO (CSA) is adopted as the System surface in [Section 5](../0.1/en/0x10-C09-System-Surface-MAESTRO.md). In
the mapping it is both the framework we build on for locating evidence in the stack and part of
CSA's broader agentic-security work, alongside the AI Controls Matrix and AARM, to which
Proof-of-Control is complementary: control objectives and enforcement on one side, open
evidence on the other. See the [MAESTRO crosswalk](../mappings/maestro.md). **[INSERT]**

## The Efforts Being Mapped

The working group is mapping Proof-of-Control against, among others: NIST AI RMF, ISO/IEC 42001,
the CSA AI Controls Matrix, MAESTRO, AARM, the IEEE 7000-series, SOC 2, the EU AI Act, zero-trust
architecture (NIST SP 800-207), Anthropic's Zero Trust for AI Agents, confidential computing
(TEEs), vendor toolkits (Microsoft Agent Governance Toolkit, Mastercard Verifiable Intent, Ping
Identity, KYA), agent observability tooling, AIUC-1, the OWASP Top 10 for Agentic AI and AIVSS,
CSA Vanta Agent Trust Controls, and the Agent Resource Discovery Specification. Each answers a
real need; Proof-of-Control cross-references them rather than competing. The per-framework
crosswalks are maintained in [`mappings/`](../mappings/README.md).

> **[WG-INPUT NEEDED]** — whether David Thomson's graph view complements or replaces the
> by-domain table above, once ready.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
