# M5 Activation, Consent, Semantic and Authorization Map

> **Status: Proposed, non-normative M5 implementation mapping for issues #42, #45 and #46.**
>
> M5Canon, LINA, a semantic graph, OpenFGA, PostgreSQL/Supabase RLS, and TitleChain are proposed implementation components. Public ICSN requirements must remain independently implementable.

```text
ACTIVATION STATE
#42
        ↓
RIGHTS / CONSENT
#45
        ↓
M5CANON
canonical meaning + lifecycle state
        ↓
M5 SOVEREIGN SEMANTIC GRAPH
entities + relationships + lineage + policy context
        ↓
LINA
native M5 semantic-policy orchestrator
        ↓
M5 AUTHORIZATION INTERFACE
        ↓
OPENFGA / FUTURE AUTHORIZATION ENGINE
        ↓
POSTGRESQL / SUPABASE RLS
        ↓
AUTHORIZED RETRIEVAL / TOOL / ACTION
        ↓
TITLECHAIN / M5 PRIVACY-FILTERED PROVENANCE
```

## M5Canon

Defines canonical meaning for consent, purpose, jurisdiction, operation, delegation, duration, approval, correction, retention, revocation and deletion.

## M5 Sovereign Semantic Graph

Represents humans, organizations, agents, tasks, account contexts, resources, assets, lineage, derivatives, policy applicability and provenance.

Orbitalys may serve as a reference implementation; the architecture remains implementation-neutral.

## LINA

LINA is a native M5Agent originating from the M5 core engine / M5Canon.

LINA resolves semantic context, applicable Canon policy, M1–M5 account context, task/agent/resource relationships, derivative lineage, expiry/revocation state and fresh-human-approval requirements.

LINA projects canonical semantics into authorization-engine representations.

LINA does not become the source of authority, rewrite her own Canon, self-grant capability or use probabilistic output as the final consequential allow/deny decision.

## Native M5Agent provenance

```text
M5 CORE ENGINE
      ↓
M5Canon
      ↓
Canonical Agent Definition
      ↓
Versioned Agent Manifest
      ↓
Approved Release
      ↓
Provenance Record
      ↓
Activated Native M5Agent
      ↓
Current Human-Authorized Task
      ↓
Agent Action
      ↓
Action Receipt
```

Authentic native-agent origin does not imply standing authority.

## Context isolation

Organizational authority must not flow backward into a human's private M1/M5POD environment without an explicit current grant.

## Derivative lineage

Source authority changes must be able to trigger re-evaluation/invalidation of chunks, embeddings, summaries, caches, agent memory and other derivatives.

## Review and evidence status

- Activation states and boundaries are published for public review under issue #42.
- The controlled consent source is not published; the [public review packet](../reviews/consent-v0.4/REVIEW-README.md) and [draft consent-event schema](../schemas/m5-consent-event.schema.json) support issue #45.
- The [proposed authorization ADR](adr/ADR-M5-AUTH-OPENFGA-PHASE1.md), [threat model](../security/M5POD-RAG-AUTHORIZATION-THREAT-MODEL.md), [draft decision-receipt schema](../schemas/m5-authorization-decision-receipt.schema.json), and [unexecuted conformance matrix](../conformance/m5-authorization/TEST-MATRIX.md) support issue #46.
- Qualified privacy, security, accessibility, governance, and counsel review remains outstanding. Publication of these drafts is not approval or conformance evidence.
