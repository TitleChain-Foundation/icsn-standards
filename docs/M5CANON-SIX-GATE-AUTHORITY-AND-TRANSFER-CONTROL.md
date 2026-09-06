# M5Canon Six-Gate Authority and Transfer Control

> **Status:** Public reference control model. The M5 implementation uses these gates as deterministic preconditions for consequential state changes. Implementation status and conformance evidence must be evaluated separately.

The purpose of the Six-Gate model is to prevent a wallet, credential, API key, or autonomous agent from becoming the source of its own authority.

```text
KNOWN HUMAN / ENTITY
       ↓
G1 — PRINCIPAL IDENTITY
       ↓
G2 — ROLE + CREDENTIAL
       ↓
G3 — JURISDICTION
       ↓
G4 — DETERMINISTIC POLICY
       ↓
G5 — REQUIRED ACCOUNTABLE APPROVAL
       ↓
G6 — EVIDENCE / AUDIT ANCHOR
       ↓
AUTHORIZED STATE CHANGE
```

## Gate 1 — Principal identity

Resolve the accountable human/legal principal. In the M5 reference implementation this is the TCID/M5HUM relationship rooted in M5IAM.

## Gate 2 — Role and credential

Verify the exact credential, role, appointment, employer/issuer relationship, skill/capability requirement, and current status required for the action. SOPHIA and the Credentialed Authority Registry provide the reference vocabulary/data model.

## Gate 3 — Jurisdiction

Resolve the applicable jurisdiction and authoritative source. The M5 reference implementation uses JNR/USC and external legal/regulatory references. A technical namespace does not create legal authority.

## Gate 4 — Deterministic policy

M5Canon evaluates current asset/entity state, delegation, restrictions, authorized supply, legends, limits, policy version, and other deterministic preconditions. It enforces authoritative state; it does not manufacture a legal conclusion.

## Gate 5 — Required accountable approval

Where a human, issuer, board, transfer agent, custodian, regulator, or other accountable authority must approve, the action cannot proceed until the required approval is present and current.

## Gate 6 — Evidence / audit anchor

The resulting decision/state change must create a tamper-evident, attributable receipt recording the principal, agent if any, purpose, jurisdiction, policy version, approvals, timestamps, and provenance. The M5 implementation may use MILNER and external notarization/anchoring mechanisms.

## Fail-closed rule

If identity, credential, standing, jurisdiction, policy, approval, or audit requirements are missing, stale, expired, revoked, or out of scope, the requested capability does not activate.

## Transfer-agent use

A transfer-agent profile can apply the gates before an agent is permitted to propose, approve, or execute a transfer, place/remove a legend, correct a record, or perform another scoped function. The registered transfer agent or other legally accountable actor remains responsible for the legally authoritative record and regulated function where applicable.
