# M5Canon Six-Gate Machine-Readable Reference Package

> **Status:** Public Review Draft

This package makes the existing M5Canon authority controls directly implementable without requiring an external developer to infer how the public artifacts fit together.

## Core rule

```text
effective_agent_authority <= current_principal_authority
```

An M5AGT cannot self-grant authority, enlarge delegated scope, extend an expired credential, waive a restriction, bypass required approval, or continue under revoked authority.

## Control path

```text
accountable principal
        ↓
G1 principal identity
        ↓
G2 current role + credential + delegation
        ↓
G3 jurisdiction
        ↓
G4 deterministic policy
        ↓
G5 required accountable approval
        ↓
G6 evidence / audit anchor
        ↓
M5 Authorization Decision Receipt
        ↓
bounded activation
```

## Existing public artifacts

This package is an integration layer over the Foundation's existing public reference artifacts:

- `docs/M5CANON-SIX-GATE-AUTHORITY-AND-TRANSFER-CONTROL.md`
- `docs/M5IAM-M5HUM-AUTHORITY-ARCHITECTURE.md`
- `docs/CREDENTIALED-AUTHORITY-REGISTRY.md`
- `schemas/credentialed-authority-registry.schema.json`
- `schemas/m5-cv-capability-profile.schema.json`
- `schemas/m5-consent-event.schema.json`
- `schemas/m5-authorization-decision-receipt.schema.json`
- `M5AGENT_OPERATIONS.md`

The existing authorization-decision receipt remains the final per-action receipt. This package adds a canonical gate-by-gate evaluation object explaining how that decision was reached.

## Gate mapping

| Gate | Deterministic question | Primary evidence/input |
|---|---|---|
| G1 — Principal identity | Who is the accountable human or lawful legal principal? | M5IAM / TCID / M5HUM reference |
| G2 — Role + credential | Is the exact role, credential, appointment and delegation current and in scope? | Credentialed Authority Registry; M5-CV may support capability evidence but does not create authority |
| G3 — Jurisdiction | Which jurisdiction and authoritative source govern the requested operation? | jurisdiction reference plus authoritative source |
| G4 — Deterministic policy | Does the action satisfy current state, policy, restrictions, delegation and scope? | policy version, consent state, asset/entity state and transfer restrictions |
| G5 — Accountable approval | Is required human/entity approval present, current and attributable? | approval reference / consent or approval event |
| G6 — Evidence/audit anchor | Can the decision and activation be reconstructed later? | authorization decision receipt plus provenance/evidence anchors |

## Fail-closed behavior

The requested capability MUST NOT activate if a required identity, credential, standing, jurisdiction, policy, approval or audit requirement is missing, stale, expired, revoked, suspended, disputed where policy requires resolution, or outside delegated scope.

## Privacy boundary

The public evaluation object should contain references, hashes, pseudonymous identifiers or selectively disclosed evidence rather than raw PII, private M5POD contents, private keys, prompts, model memory or regulated records.
