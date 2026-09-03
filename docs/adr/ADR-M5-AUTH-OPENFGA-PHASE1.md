# ADR — Phase 1 M5 Authorization: LINA + Semantic Graph + OpenFGA + RLS

- **Status:** Proposed
- **Issue:** #46

## Context

M5 must prevent authenticated principals, agents, RAG systems, MCP tools and applications from accessing data merely because IAM has succeeded.

## Decision

1. IAM/TCID establishes identity/authentication.
2. M5Canon defines canonical consent, authority and lifecycle semantics.
3. Persistent Canon-governed state stores grants, approvals, purpose, expiry and revocation.
4. The M5 Sovereign Semantic Graph represents entities, relationships, account context, resource lineage, provenance and policy applicability.
5. LINA, a native M5Agent, resolves semantic meaning and projects applicable authorization state.
6. OpenFGA is the Phase 1 relationship-authorization engine.
7. PostgreSQL/Supabase RLS is an independent data-layer enforcement boundary.
8. pgvector/RAG retrieval executes only within authorized RLS/object scope.
9. TitleChain/M5 provenance records privacy-filtered decision and lifecycle evidence.

## LINA boundary

LINA may interpret, resolve and compile semantics.

LINA may not rewrite Canon, create human authority, self-grant capabilities, replace deterministic enforcement, or make final consequential allow/deny decisions from probabilistic model output.

## Vendor neutrality

Orbitalys may be a reference semantic-graph implementation. OpenFGA may be the Phase 1 authorization engine. Both remain replaceable behind stable M5 interfaces.

## Contextual tuples

Request-specific contextual tuples may represent ephemeral facts. They must not be the sole source of truth for revocation-sensitive consent, task authority, expiry, withdrawal or deletion state.

## Pre-retrieval enforcement

Authorization occurs before data enters model context.

## Risks

- semantic graph synchronization bugs
- stale authorization projections
- revocation propagation lag
- graph-to-FGA compiler errors
- service-role/RLS bypass
- derivative-lineage gaps

These require conformance tests, observability and fail-closed behavior.

## Rollout gate

This proposal must not advance to a participant-data pilot until:

1. the authorization model and RLS policies are versioned and independently reviewed;
2. the conformance matrix has executed evidence for deny-by-default, context isolation, revocation, derivative invalidation, tool separation, and fresh human approval;
3. privacy-filtered decision receipts can be inspected without exposing protected content;
4. synchronization lag and stale-projection limits are measured; and
5. security and privacy reviewers approve the threat model and evidence.

## Rollback and failure behavior

- Authorization projection or semantic-graph failure must fail closed for protected access.
- A rollback must pin the last approved Canon, graph-projection, authorization-model, and RLS-policy versions as one compatible set.
- Revoked or expired authority must not be restored by rollback, cache recovery, offline replay, or account recovery.
- Operators must be able to disable affected retrieval, tool, or agent paths without disabling correction, appeal, export, or other required human-rights functions.

## Observability

Monitor policy-version mismatch, stale projections, denied and indeterminate decisions, RLS bypass attempts, derivative invalidation lag, revocation propagation, high-impact approval freshness, and decision-receipt generation. Logs and metrics must not contain protected source content, retrieved chunks, prompts, credentials, private identifiers, or agent memory.
