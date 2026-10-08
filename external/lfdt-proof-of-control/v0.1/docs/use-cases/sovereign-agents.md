---
industry: cross-sector (applies uniformly wherever an OSARA-compliant agent is deployed: enterprise, government, or individual use)
use_case: An agent built to the OSARA (Open Sovereign Agent Reference Architecture) standard acts on behalf of its owner, taking actions with real consequences.
claimed_tier: 4
---

# OSARA-Compliant Agents: A Proof-of-Control Mapping

## Scenario
An owner (an individual, an enterprise, or a government body) deploys an agent
built to the OSARA reference architecture. The agent acts on the owner's
behalf: initiating a payment, deleting a record, or committing to a
contractual term. The same question arises regardless of sector: was this the
owner's genuine agent, did the owner actually authorize this specific action,
and had the agent been altered after it left the owner's control. What
differs by industry is the consequence of getting the answer wrong (a cleared
payment, a lost record, a binding commitment). What does not differ is the
mechanism OSARA compliance uses to answer it, which is why this mapping
applies identically across sectors rather than being reworked per industry.
## Claimed tier: Tier 4
An agent claiming OSARA compliance is claiming Tier 4 on its core control
properties. OSARA requires that no action can be taken without a valid
signature from a private key held exclusively in the owner's hardware
Authorization Device (OAD), that any detected tampering triggers automatic
lockdown rather than a logged alert, and that moving the agent to a new host
is itself gated: the destination runtime must verify the container hash and
the owner's signed manifest, and confirm the audit log chain is unbroken,
before the agent is permitted to start. All three are self-enforcing,
fail-closed behaviors, not after-the-fact checks. That is the bar Tier 4
requires, and it is also what "OSARA-compliant" is meant to certify.
## Why not one tier down?
At Tier 3, an auditor could reproduce the agent's hash-chained log and
independently confirm, after the fact, that an action was unauthorized, that
the agent had been tampered with, or that a migrated container had been
altered in transit. That confirmation still arrives too late for actions with
irreversible consequences: a payment has cleared, a record is gone, a
commitment is made, or a tampered agent has already started running on its
new host under the owner's authority. OSARA's design choice, refusing the
action outright when a valid OAD signature is absent, locking the agent down
the moment integrity checks fail, and refusing to let a migrated agent start
until its hash and signature verify, is what closes that gap. A system that
only logs the failure for later review, however faithfully, is a Tier 3
system, not a Tier 4 one, regardless of how open or well-documented its logs
are.
## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 3 | OSARA mandates that identity, audit, encryption, and gateway components be open source, so an agent's origin and configuration are independently reproducible and inspectable. This is strong, but provenance itself is not required to be fail-closed. |
| Authorization | 4 | No action executes without a valid signature from the OAD-held key. Absent that signature, the action is refused, not flagged. This is the domain OSARA compliance rests on most heavily. |
| Security      | 4 | Continuous integrity measurement (IMA) detects unauthorized modification and triggers automatic lockdown and a sealed forensic snapshot, rather than an after-the-fact alert. |
| Identity      | 4 | The agent's key never leaves the OAD, so spoofing or impersonation is structurally prevented rather than merely detectable later. |
| Privacy       | 3 | Agent memory is encrypted at rest with an owner-derived key and stored in an open, portable format the host cannot read; strong and independently verifiable, though not itself required to be fail-closed. |
| Portability   | 4 | OSARA's Agent Migration and Integrity Protocol gates the migration itself, not just the ability to migrate. Before the agent is allowed to start on the destination host, the runtime must recompute the container hash, verify the owner's OAD signature on it, and check the audit log chain end to end. If any check fails, the container is rejected outright and the agent does not start. Verification happens before authorization to run, not after, so this is fail-closed rather than after-the-fact confirmation. |
## Notes / open questions
- The overall Tier 4 claim rests on Authorization, Security, Identity, and
  Portability, which is exactly the set OSARA's OAD, IMA, and Agent Migration
  and Integrity Protocol are built to satisfy: each blocks the risky action
  outright rather than only logging it. Provenance and Privacy sit at Tier 3
  because OSARA's open source and at-rest encryption guarantees are
  independently reproducible but not themselves gating a specific action the
  way authorization, tamper response, and migration are.
- Because this mapping is a property of OSARA's architecture rather than of
  any deployment context, it holds the same way in finance, healthcare,
  government, or personal use. Industry-specific risk changes what the
  consequence of failure looks like, not which tier OSARA compliance is
  certifying.
- Open question: whether a closed-source implementation of the same OAD, IMA,
  and migration mechanisms could still claim Tier 4 on Authorization,
  Security, Identity, and Portability while remaining at a lower tier on
  Provenance, since OSARA's own conformance model currently ties all of this
  to an open source requirement.
- REF: https://elkordym.github.io/osara-open-standard/
- Submitted to AAI-Society/openverification as [pull request #2](https://github.com/AAI-Society/openverification/pull/2) by GitHub @elkordym, and ported here when the use-case corpus moved into this repository unchanged. It was written to the v1 template, before the threat vocabulary and the v2 sections existed, and still needs that retrofit: threat tags, the scope section, and the residual-trust section.
