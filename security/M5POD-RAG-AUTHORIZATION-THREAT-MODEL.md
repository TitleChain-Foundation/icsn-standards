# M5POD RAG Authorization Threat Model

> **Status: Draft for security/privacy review.**
> **Issue:** #46

## Protected assets

Private M5POD data, credentials, consent state, task grants, agent authority, account-context boundaries, source documents, chunks, embeddings, summaries, caches, agent memory, tool/API permissions, transaction/title authority, provenance evidence and recovery state.

## Trust boundaries

1. human ↔ IAM
2. IAM ↔ M5Canon
3. M5Canon state ↔ semantic graph
4. semantic graph ↔ LINA
5. LINA ↔ authorization adapter
6. authorization engine ↔ RLS
7. RLS ↔ vector retrieval
8. retrieval ↔ agent/model
9. agent ↔ MCP/API/tool
10. action ↔ provenance/evidence

## Threat matrix

| Threat | Minimum control |
|---|---|
| Confused deputy | explicit task + context binding |
| Agent impersonation | canonical native-agent identity + provenance |
| Tuple tampering | authorized projection pipeline + audit |
| Stale authorization | persistent Canon state + freshness checks |
| Revocation race | fail-closed for sensitive/shared access |
| Cross-context leakage | explicit M1–M5 context isolation |
| Overbroad object listing | scoped list/query authorization |
| Cache leakage | lineage-aware invalidation |
| Embedding leakage | authorized storage scope + RLS |
| Summary leakage | derivative lineage + re-evaluation |
| Prompt injection | documents treated as untrusted; tool auth separate |
| Tool escalation | operation-specific permissions |
| MCP confused authority | discovery/invoke/read/write/disclose separated |
| Offline stale grants | bounded offline policy + freshness rules |
| Recovery abuse | recovery does not restore revoked authorization |
| Compromised device | device binding + revocation + re-auth |
| Compromised agent | separate agent identity + task scope |
| Service-role bypass | privileged-path review + isolation |
| DB view/function bypass | security-definer review + tests |
| Logging leakage | structured redaction / no-content receipts |
| Provenance over-disclosure | privacy-filtered receipt schema |
| Canon drift | version pinning + conformance |
| LINA drift | native-agent provenance + Canon-version binding |

Security and privacy reviewers must approve the threat model and executed conformance evidence before pilot deployment.
