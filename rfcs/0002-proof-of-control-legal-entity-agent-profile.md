# RFC 0002: Proof-of-Control Profile for Legal-Entity Agents Under an Accountable Human

- **Status:** Draft
- **Authors:** Pamela Norton (TitleChain Foundation)
- **Created:** 2026-10-08
- **Base standard:** [LFDT Proof-of-Control Standard, Working Draft v0.1](../external/lfdt-proof-of-control/README.md) (commit `b8fb012`)
- **Crosswalk:** [`conformance/proof-of-control/`](../conformance/proof-of-control/README.md)
- **Discussion:** to be opened
- **Implementation evidence:** see [Reference implementations](#reference-implementations)
- **License:** Apache License 2.0, so this profile can be contributed upstream unchanged

## Summary

The Proof-of-Control Standard (PoC) defines verifiable evidence of what an AI agent did. It
traces every action to *a* principal. In practice the principal is usually a legal entity,
such as a company, cooperative, trust or public body, and the entity acts through a natural
person who is accountable for what its agents do.

This profile adopts **all 127 PoC v0.1 requirements unchanged** and adds **22 requirements**
for that common case: agents acting for a legal entity under an accountable human. It
separates the three parties, keeps identity stable when keys change, allows pseudonymous
agents that remain accountable, keeps protected evidence in a store the principal controls,
requires that every computed value be published and reproducible, and puts consequential
actions behind human approval and reversible settlement.

## Problem and affected communities

PoC v0.1 asks that every action resolve to "a named principal" (5.1.1). Three questions
follow that the draft leaves open, and that PoC's own Appendix D lists as open issues:

1. **Who is the principal?** A company cannot sign anything; a person signs for it. Recording
   only the company loses who exercised authority; recording only the person loses on whose
   behalf. Appendix D issue 1 asks whether that binding belongs to Identity or Authorization.
2. **Can an agent be pseudonymous and still accountable?** Appendix D issue 2 asks for
   verifiable-but-unlinkable binding with defined conditions for disclosure.
3. **Does evidence survive a change of provider?** Appendix D issue 3 asks for unbroken
   evidence across boundaries.

Small businesses, cooperatives, and public bodies are affected most: they run agents through
third-party platforms, rotate staff, change vendors, and need evidence that outlives all three.

## Goals and non-goals

### Goals

- Adopt PoC v0.1 in full, so a TitleChain-profile claim is always also a PoC claim.
- Add requirements, in PoC's format and level scheme, for the legal-entity and
  accountable-human case.
- Map every PoC requirement in a machine-readable crosswalk that a test keeps complete.
- Offer the additions upstream as answers to Appendix D issues 1–3.

### Non-goals

- Replacing, forking, or editing PoC. The vendored snapshot is never modified here.
- Using or implying the "Proof-of-Control Certified" mark.
- Making any one implementation normative.

## Terminology

Requirements language follows RFC 2119/8174. PoC's glossary applies. In addition:

- **Legal-entity principal:** the organization on whose behalf an agent acts.
- **Accountable human of record:** the natural person who, at the time a grant is issued,
  holds the role authority to act for the legal entity and issues or approves the agent's
  grant.
- **Role authority:** the entity's evidence that a person may act for it in a defined scope,
  such as a certificate of authority, board resolution, or registered officer role.
- **Principal-controlled store:** an evidence store whose keys and contents are controlled by
  the principal rather than the agent operator or platform.
- **Computation manifest:** a published, machine-readable list of every formula an evidence
  record computes, with units, rounding, and parameter digests.

Consistent with PoC's editorial rule, what an agent did is *evidenced* or *shown*; "prove" is
reserved for cryptographic proofs.

## Specification

A conforming implementation MUST meet every PoC v0.1 requirement at its claimed Level and
every requirement below at or under that Level. Levels follow PoC: 1 Recorded, 2 Attested,
3 Verifiable, 4 Enforced.

### LE1 Three-party principal binding

*Extends C5.1 and C4.2. Answers Appendix D issue 1: Identity supplies the three
authenticated parties; Authorization evaluates the chain between them.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE1.1** | **Verify that** every execution record carries the agent instance identifier, the legal-entity principal identifier, the accountable human of record's identifier, and a reference to the role authority linking that human to the entity. | 1 | 5.1.1 |
| **LE1.2** | **Verify that** before a grant is issued, the accountable human's role authority for the entity is validated as current for the scope granted, and the validation result is written to the execution record. | 2 | 4.1.1, 5.1.2 |
| **LE1.3** | **Verify that** the delegation chain runs human → entity role → agent, that each hop carries the delegator's signature, and that the agent's scope is the intersection of the human's role authority and the entity's grant. | 2 | 4.2.2, 4.2.3 |
| **LE1.4** | **Verify that** no record names an agent as the originating principal or as the accountable human, and that an agent cannot issue a delegation exceeding the authority it was granted. | 1 | 4.2.3 |
| **LE1.5** | **Verify that** the accountable human or the entity can revoke an agent's authority at any time without the consent of the agent or its provider, that revocation is recorded, and that it applies to every subsequent action. | 2 | 4.1.2 |
| **LE1.6** | **Verify that** when the accountable human's role authority ends, every grant they issued is revoked or reaffirmed by a successor within a declared interval, with records linking the predecessor and successor grants. | 2 | 4.2.2 |

**Auditor evidence:** LE1.1 — sampled records resolve to an agent, an entity, and a person with
role authority. LE1.2 — a grant record preceded by a role-authority validation, and one rejected
grant from an expired role. LE1.3 — walk one chain from agent to person to entity. LE1.4 — search
records for agents in principal fields; attempt an over-scope sub-delegation in test. LE1.5 —
revoke in test and confirm the next action is refused. LE1.6 — end a role in test and confirm
grants are revoked or reaffirmed within the interval.

### LE2 Identity survives key change

*Extends C5.1.2 and C6.3.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE2.1** | **Verify that** rotating or migrating the key of an agent, accountable human, or entity leaves its identifier unchanged, and that a signed record links the predecessor and successor keys. | 2 | 6.3.2 |
| **LE2.2** | **Verify that** possession of a compromised key cannot by itself transfer title or control, change an entity role, or create a delegation, and that recovery requires approval records from the accountable human and the entity. | 2 | 6.3.3 |
| **LE2.3** | **Verify that** verification results distinguish evidence valid at event time, evidence produced under an algorithm since deprecated, and evidence signed by a key compromised after the event, and that deprecated evidence remains verifiable. | 2 | 6.3.4, 6.3.5 |

**Auditor evidence:** LE2.1 — a rotation record and an unchanged identifier across it. LE2.2 —
attempt a title or role change with a stolen test key and confirm refusal. LE2.3 — verify one
record before and after deprecating its algorithm.

### LE3 Pseudonymous, accountable agents

*Answers Appendix D issue 2 as an implementer-selectable option.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE3.1** | **Verify that**, where pseudonymity is selected, relying parties receive a stable pseudonymous subject identifier together with evidence of a valid delegation from a verified entity (for example a zero-knowledge or selective-disclosure presentation), and never the entity's or human's identifiers. | 3 | 4.2.4 |
| **LE3.2** | **Verify that** the link from pseudonym to entity and accountable human is held in the principal-controlled store, that the conditions for disclosing it are listed in the trust-assumption disclosure, and that each disclosure is recorded. | 2 | 10.2.1 |
| **LE3.3** | **Verify that** any reputation or risk score about a pseudonymous subject is computed by a method published under LE5 and is disclosed with the evidence records it rests on. | 2 | 7.5.1 |

**Auditor evidence:** LE3.1 — validate one presentation without learning the entity. LE3.2 — the
disclosure-conditions entry and a recorded test disclosure. LE3.3 — recompute one score from its
cited evidence with the published method.

### LE4 Principal-controlled evidence and exit

*Extends C1.4, C2.4, and C3. Answers Appendix D issue 3.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE4.1** | **Verify that** protected source records remain in the principal-controlled store and that evidence shared with operators or relying parties carries only identifiers, digests, or commitments. | 2 | 1.4.1, 2.1.2, 2.4.1 |
| **LE4.2** | **Verify that** the principal can export a complete verification bundle (evidence, public keys and reference values, verifier version, and computation manifest) and verify it offline without the original operator. | 2 | 3.2.1, 8.1.5 |
| **LE4.3** | **Verify that** moving the agent or its evidence to a new provider writes a signed linking record joining the last record of the old chain to the first record of the new one. | 3 | 3.2.2 |

**Auditor evidence:** LE4.1 — scan shared evidence for protected content. LE4.2 — verify an
exported bundle on an offline machine. LE4.3 — walk one linking record across a migration.

### LE5 Deterministic, published computation

*Extends C7.2, C7.7, and C10.1.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE5.1** | **Verify that** every value an evidence record computes (a fee, split, score, or deadline) is defined in a published, machine-readable computation manifest with formula, units, and rounding, and that each record cites the digest of the manifest and of every parameter file used. | 2 | 7.7.1, 10.1.5 |
| **LE5.2** | **Verify that** a time-triggered event is timestamped at the deadline it fires on rather than when it was processed, so that replaying the same history produces byte-identical records. | 2 | 7.2.1 |
| **LE5.3** | **Verify that** the canonical serialization admits only number forms that every supported language represents identically and rejects all others. | 2 | 7.7.2, 7.7.4 |
| **LE5.4** | **Verify that** each manifest computation has at least two separate implementations held to one set of published vectors, including negative vectors. | 3 | 7.7.4 |

**Auditor evidence:** LE5.1 — recompute one record's values from the cited manifest and confirm
the digests. LE5.2 — process the same history at two different times and compare records.
LE5.3 — submit an out-of-range integer and a non-finite number and confirm rejection. LE5.4 —
run both implementations against the vectors.

### LE6 Consequential actions

*Extends C4.1.6 and C7.3.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE6.1** | **Verify that** actions changing title or control state, entity roles, or delegations, or moving value above a declared threshold, require an approval record from the accountable human, and that an agent's approval is never accepted in its place. | 2 | 4.1.6 |
| **LE6.2** | **Verify that** value-moving actions settle through a reversible hold with published release, refund, and dispute rules; that a refund reverses the hold rather than recovering funds from payees; and that the hold's event log is hash-chained. | 2 | 7.3.1 |
| **LE6.3** | **Verify that** every automated response (a policy denial, a deadline refund, a release) records the rule that produced it and the party entitled to trigger it. | 1 | 4.1.2 |

**Auditor evidence:** LE6.1 — attempt a role change approved only by an agent and confirm
refusal. LE6.2 — refund a held transaction in test and confirm no payee was debited. LE6.3 —
sampled automated events name their rule and trigger.

## Human rights, consent and inclusion

The profile keeps a person answerable for every consequential agent action while allowing that
person and their entity to stay pseudonymous to counterparties (LE3). Protected records stay
with the principal (LE4), and the principal can leave a provider without losing their evidence.
These matter most to individuals, small businesses, and communities with the least leverage
over platforms. An agent is never treated as an independent principal (LE1.4), consistent with
human-rooted agent authority.

## Privacy and security

Threats addressed beyond PoC v0.1: impersonation of an entity by a former officer (LE1.2, LE1.6),
authority laundering through sub-delegation (LE1.3, LE1.4), key theft used to seize title or roles
(LE2.2), correlation of pseudonymous agents (LE3.1), vendor lock-in of evidence (LE4.2), and
silent changes to computed values (LE5.1). Residual assumptions are disclosed under PoC C10.2,
including the conditions for piercing pseudonymity (LE3.2).

## Sovereignty and governance

Role authority comes from the entity's own governance, and the profile does not decide who may
act for an entity. Jurisdiction-specific disclosure limits follow PoC 3.2.3. This RFC is a
Foundation proposal; its additions are offered to the PoC working groups and do not alter the
upstream standard.

## M5Agent and automation impact

- [ ] No. This RFC does not create or materially affect automated authority.
- [x] Yes. This RFC affects automated or agent-based operations.

1. Any agent acting for a legal entity.
2. Applies equally to M5Agent Native and OpenAPI Marketplace agents.
3. The accountable human of record and the legal-entity principal (LE1).
4. Role authority plus a signed, scope-intersected delegation (LE1.2–LE1.3).
5. Actions within the granted scope, evaluated per PoC C4.
6. LE6.1 actions: title or control changes, role or delegation changes, value above threshold.
7. Acting as a principal, approving its own consequential actions, or exceeding its grant.
8. Identifiers, digests, and commitments in shared evidence; protected content in the
   principal-controlled store (LE4.1).
9. As listed under Privacy and security, plus PoC Appendix C.
10. Revocation (LE1.5), succession (LE1.6), hash-chained holds (LE6.2), PoC retention (7.6.5).
11. Each automated response names its rule (LE6.3); disputes follow the hold's published rules
    (LE6.2).

## Interoperability and migration

The profile is additive: every PoC claim remains valid, and a TitleChain-profile claim cites both
PoC v0.1 and this RFC. When PoC publishes a new version, the snapshot is refreshed and the
crosswalk updated in the same change. Any LE requirement that PoC adopts upstream is retired here
and marked as such in the crosswalk.

## Conformance

A conformance statement under this profile MUST:

1. meet PoC C10 in full, citing PoC v0.1 and RFC 0002;
2. list the LE requirements met, at the claimed Level;
3. publish the crosswalk status of the implementation for every PoC requirement.

`tests/validate_proof_of_control_profile.py` checks that the vendored snapshot is unmodified,
that the crosswalk covers exactly the 127 PoC v0.1 requirements, and that every LE requirement
names PoC requirements that exist.

## Reference implementations

No implementation is normative. One implementation is mapped in the crosswalk, labeled
**implementation-specific, external, and subject to separate terms** per the
[M5Ecosystem Approval Boundary](../M5ECOSYSTEM-APPROVAL-BOUNDARY.md):

| Profile concept | M5 implementation (implementation-specific) |
| --- | --- |
| Accountable human of record | M5HUM / TCID human root |
| Legal-entity principal | M5 business or institutional entity account (BOB/BOI/BOG) |
| Role authority | M5-CV role and Certificate of Authority |
| Principal-controlled store | M5POD |
| Computation manifest (LE5) | M5-MATH-001 manifest, receipts citing its SHA-256 |
| Reversible hold (LE6.2) | CCF-5 settlement hold with hash-chained events |
| Pseudonymous scoring (LE3.3) | M5Nash Score over wallet identifiers (weights PROPOSED) |

The crosswalk records M5 status only where it was checked against code; all other entries are
`NOT_ASSESSED`.

## Disclosure of interest

The author is on the founding team of the Proof-of-Control initiative and has commercial
interests in the M5 implementation mapped above. Consistent with the Proof-of-Control governance
document, this interest is disclosed here and in any upstream contribution, and the author will
follow the working group's recusal practice on decisions that would directly favor M5.
