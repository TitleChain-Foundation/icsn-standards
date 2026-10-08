# Proposal: institutional-result boundary after effect binding

*Date:* 2026-09-09 · *Status:* proposal only. No normative file is edited by this proposal.

*Submitted by:* Ricardo Crespo — N’KEMBA, Institutional Evidence & Reconstruction

*Related proposal:* P02-effect-binding.md

---

## Finding

P02 correctly distinguishes request/message binding from effect binding at the endpoint.

A further boundary remains after effect binding:

*an evidenced external effect does not necessarily establish the operative institutional result.*

An external action may be technically executed and evidenced, while the institution later rejects, corrects, reverses, supersedes or replaces the decision, document or action on which that effect was based.

The institutional question is therefore not only:

> What effect did the endpoint execute?

It may also be:

> Which document version, human or institutional authority, decision and subsequent correction ultimately became operative?

This proposal does not ask Proof-of-Control to perform institutional reconstruction.

It asks the standard to preserve the semantic boundary between technical effect evidence and later institutional state.

---

## Proposed boundary

Proof-of-Control evidence SHOULD NOT imply institutional finality merely because an action or external effect is evidenced.

Where available, an evidence model SHOULD permit stable downstream references to:

- the operative document and version;
- authority applicable at the relevant time;
- institutional adoption or rejection;
- correction, revocation or supersession;
- subsequent replacement decisions or actions; and
- evidence of the result that ultimately became operative.

An original action or effect record SHOULD remain valid historical evidence even when a later institutional record supersedes its operative significance.

---

## Auditor evidence

A downstream assessor should be able to distinguish:

1. action evidenced;
2. external effect evidenced;
3. institutional adoption not yet evidenced;
4. action or decision subsequently corrected or superseded; and
5. the later result, if any, that became institutionally operative.

The existence, integrity or verification of evidence at stages 1 or 2 should not silently establish stages 3–5.

---

## Controlled test motivating the proposal

N’KEMBA ran a controlled synthetic multi-source reconstruction test using deliberately out-of-order evidence.

The test included:

- an initially authorized EUR 48,700 payment instruction;
- technical evidence of that instruction;
- a later documentary correction;
- explicit supersession of the first decision;
- a second authorized instruction for EUR 47,900;
- independent evidence that EUR 48,700 was not settled; and
- independent evidence that EUR 47,900 was settled.

The reconstruction preserved the first instruction as valid historical evidence while identifying the corrected EUR 47,900 result as operative.

The controlled integration test returned *10/10 PASS* against its predefined checks.

### Limits

This was a synthetic controlled test, not a live institutional deployment and not a Proof-of-Control conformance claim.

It demonstrates the semantic distinction motivating this proposal.

No proprietary N’KEMBA reconstruction method, scoring rule or internal schema is disclosed here.

---

## Relationship to P02

P02 addresses the gap:

*authorized request → executed effect*

This proposal begins after that boundary:

*executed effect → operative institutional result*

The two are complementary.

Effect binding can establish what an endpoint did under its stated conditions.

It does not by itself establish:

- whether the institution adopted that result;
- which documentary version governed;
- whether an authorized person later corrected or superseded it;
- which decision remained operative; or
- what the institution ultimately recorded as the consequential result.

---

## Interoperability principle

*Tamper-evidence ≠ completeness.*

*Action evidence ≠ effect evidence.*

*Effect evidence ≠ institutional finality.*

Proof-of-Control can remain authoritative for the evidence layer it covers while exposing stable hooks for downstream institutional reconstruction systems.
