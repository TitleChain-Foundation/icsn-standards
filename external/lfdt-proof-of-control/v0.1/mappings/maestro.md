# Crosswalk: MAESTRO (Cloud Security Alliance)

**Framework type:** Agent-specific threat-modeling framework
**Relationship:** Adopted — MAESTRO is the framework filling the Proof-of-Control System surface
(Axis 2) today. See [Section 5](../0.1/en/0x10-C09-System-Surface-MAESTRO.md).

## What MAESTRO Is

MAESTRO is a seven-layer model of the agent stack (Layer 1 to Layer 7), authored by
Proof-of-Control co-chair Ken Huang. It is the first agent-specific threat-modeling framework and
the most complete published map of the agent stack; it is actively adopted by industry and is
already part of the Cloud Security Alliance's agentic-security work.

## How Proof-of-Control Uses It

The question of *where in the system* is permanent; the framework that answers it can change.
Every conformant Proof-of-Control claim MUST locate its evidence on the System surface: which
layer of the system the evidence is about. The axis is normative and pluggable; MAESTRO fills it
today, and other agent-surface frameworks — or industry-specific iterations of MAESTRO — may be
recognized as the field matures.

MAESTRO is also a threat source: the two evidence-model threats in the Proof-of-Control threat
model — evidence repudiation and trust opacity — come from the MAESTRO threat-modeling work
([Section 4](../0.1/en/0x92-Appendix-C_Threat-Model.md)).

## The Layer Mapping

| MAESTRO layer | Covers | Example controls (see [Section 5](../0.1/en/0x10-C09-System-Surface-MAESTRO.md)) |
| --- | --- | --- |
| L1 — Foundation Model Security | Base model, weights, serving logic, fine-tuned variants, behavioral policies | Model provenance verification; adversarial robustness attestation; model integrity at inference |
| L2 — Data Operations Security | Ingestion, preprocessing, embeddings, vector DBs, RAG, retraining logs | Data provenance chain; RAG hardening; privacy compliance attestation; vector store integrity |
| L3 — Agent Framework Security | Agent loop and orchestration: planning, tool selection, workflows, memory, coordination | Objective constraint verification; tool schema formal verification; workflow safety; memory integrity |
| L4 — Deployment & Infrastructure Security | APIs, containers, orchestration, networks, secrets, hardware/TEEs | Runtime environment attestation; secret management; network segmentation proofs; hardware integrity; federated verification (MPC) |
| L5 — Evaluation & Observability | Monitoring, logging, evaluation, forensics | Tamper-evident logging; evaluation integrity; anomaly-detection integrity; telemetry security |
| L6 — Security, Governance & Compliance | Policies, access control models, change management, regulatory compliance | Access control policy verification; policy-as-code; compliance audit evidence; change management |
| L7 — Agent Ecosystem Security | Users, other agents, marketplaces, registries, external services | Agent identity verification; marketplace/registry integrity; third-party vetting; delegation chains; reputation integrity |

## Relationship in the Broader Mapping

In the standards mapping, MAESTRO is both the framework Proof-of-Control builds on for locating
evidence in the stack, and part of CSA's broader agentic-security work — alongside the
[AI Controls Matrix](csa-aicm.md) and [AARM](csa-aarm.md) — to which Proof-of-Control is
complementary: control objectives and enforcement on one side, open evidence on the other.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
