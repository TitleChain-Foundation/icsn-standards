# M5IAM → M5HUM Human Authority Architecture

> **Status:** Public reference architecture.

M5 begins with an accountable human or lawful entity, not with a wallet, token, AI model, application, or network.

```text
M5IAM
  ↓
TCID / M5HUM
  ↓
M5POD
  ↓
M5-CV / SOPHIA
  ↓
M5AGT — bounded delegated authority
  ↓
M5Canon — deterministic policy + authority evaluation
  ↓
authorized action + evidence
```

## M5IAM

**M5IAM** is the identity-and-access floor of the M5 reference implementation. It establishes the human identity relationship before higher personal, group, business, institutional, or governance account contexts are activated.

The reference account sequence is additive:

```text
000-IAM      Identity & Access Management
001-M5BOM    Bank of Me
002-M5BOU    Bank of Us
003-M5BOB    Bank of Business
004-M5BOI    Bank of Institutions
005-M5BOG    Bank of Government / Governance
```

These account contexts are separate from the M1–M5 asset/economic classification model.

## TCID / M5HUM

**M5HUM — Human Principal** is the canonical type code for a credentialed human sovereign. A TCID identifies that human root inside the M5 reference implementation. Every M5AGT is accountable to a named M5HUM.

A system should be able to resolve who is accountable, which identity evidence established the relationship, which jurisdiction applies, which roles/credentials are current, what has expired or been revoked, and what may be delegated.

## M5POD

The **M5POD** is the holder-controlled private evidence/data layer. Public standards carry only the minimum proofs, references, or selective presentations needed for a purpose; private identity and evidence remain private.

## M5-CV / SOPHIA

**M5-CV** is the member-controlled capability/contribution record. **SOPHIA** is the shared role, skill, learning, and credential vocabulary. Neither creates identity or operational authority by itself.

## M5AGT

**M5AGT — Autonomous Agent** identifies an AI agent acting on behalf of a human under delegated authority. It cannot exceed the M5HUM's permissions.

```text
effective_agent_authority <= current_principal_authority
```

An M5AGT cannot self-grant authority, extend an expired credential, waive a restriction, or continue under a revoked delegation.

A consequential agent action should resolve to an accountable M5HUM/legal entity, role, credential, purpose, jurisdiction, operation, asset/entity scope, required approval, effective/expiry time, revocation state, policy version, and evidence receipt.
