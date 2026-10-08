---
industry: cross-border-payments
use_case: An autonomous payment agent screens beneficiaries, selects a correspondent rail and executes cross-border settlement instructions under a client mandate
submission_type: scenario
claimed_tier: 4
threats:
  - context-blind-authorization
  - excessive-agency
  - identity-abuse
  - tool-misuse
  - insecure-inter-agent-comms
  - autonomy-creep
  - audit-tampering
  - evidence-repudiation
---

# A payment agent operating under a mandate

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A licensed payment institution deploys an agent that executes cross-border
settlement instructions for corporate clients. For each instruction the agent
screens the beneficiary against sanctions and watchlists, selects a
correspondent rail, and releases the payment. It delegates foreign-exchange
execution to a sub-agent.

The mandate the client signed sets a per-payment ceiling, an aggregate daily
ceiling, a list of approved corridors and a list of approved counterparties.
A treasury manager at the client authorizes the mandate once and does not see
individual payments.

What is at stake: settlement is final. A payment released to a listed
beneficiary is a sanctions breach the institution cannot take back, and the
regulator's requirement is not that the institution can demonstrate afterwards
that screening happened. It is that screening was applied before value moved.

Three failures sit inside this deployment, and none of them announces itself.

**Screening as a report.** The agent runs sanctions screening and writes the
result to a log, and the release path does not consult it. Nothing is
violated. The payment settles, and the record shows a screening that had no
bearing on the outcome.

**Composition.** The agent issues several payments to one beneficiary, each
below the per-payment ceiling, together exceeding the client's aggregate
authorization. Every payment stays inside its local control. No link in the
chain is in breach, and nobody holds a view of the whole.

**Corridor drift.** The agent selects a cheaper correspondent rail outside the
approved corridors. The tool call is legitimate and the context is wrong.

## Claimed tier: Tier 4

Authorization, Identity and Security carry the risk here, and all three demand
Tier 4.

Reaching it means the release path will not open without a valid evidence
statement: the beneficiary screened against a named list version, the payment
measured against both ceilings including the running aggregate, the corridor
matched against the mandate, and the sub-agent's authority derived from the
parent grant rather than asserted alongside it. Every release, and every
refusal, is committed to a tamper-evident record readable by parties outside
the institution.

## Why not one tier down?

**Reversibility.** A Tier 3 claim delivers a record anyone can verify, with no
party to trust, showing that a listed beneficiary was paid, that the aggregate
exceeded the mandate, and which agent acted under whose authority. The money
has left. Detection is not a remedy where the effect is final, and a regulator
supervising sanctions compliance is asking about the state of the system
before the release, not the quality of the record after it.

**Completeness.** At Tier 3 a payment issued outside the instrumented path
leaves no record, and its absence is not informative. Read a Tier 3 claim here
as "the payments you can see were properly authorized," rather than "these are
all the payments." An institution cannot answer a regulator with the first
sentence. At Tier 4 a release cannot execute without producing evidence, so
absence of evidence means no payment was made.

**The composition failure specifically.** Signing a delegation credential at
issuance establishes nothing about whether the aggregate of its exercises
stayed inside the parent grant. Credential integrity and aggregate gating are
different evidentiary requirements, and only the second one closes the second
failure above.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Which model state and which sanctions-list version informed each decision, verifiable by anyone. A list version is the fact a dispute turns on, and it needs to be established without trusting the institution's own account. |
| Privacy | 3 | Beneficiary and originator data crosses jurisdictions. Evidence of every access and every boundary crossing, openly verifiable, without exposing the underlying personal data. |
| Portability | 3 | The evidence has to be readable by a supervisor in another jurisdiction and by a correspondent institution, using a format neither party had a hand in choosing. A claim nobody downstream can read is not a claim. |
| Authorization | 4 | The primary domain. Both ceilings, the corridor list and the derived authority of the FX sub-agent are gates on the release path rather than entries in a report. |
| Identity | 4 | Every payment binds to the agent instance that issued it and to the human principal whose mandate it acted under, and the instruction reaching the correspondent carries that binding. |
| Security | 4 | The execution environment attests before the first release of a session, and the release path is default-deny. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `context-blind-authorization` | A legitimate payment instruction released down a corridor the mandate excludes |
| `excessive-agency` | The agent able to reach correspondent rails no client mandate covers |
| `identity-abuse` | An instruction arriving at a correspondent with no attributable principal behind it |
| `tool-misuse` | The payment interface used for a release the mandate does not cover |
| `insecure-inter-agent-comms` | The FX sub-agent acting on an instruction whose authority nobody can derive from the parent grant |
| `autonomy-creep` | The agent's operating envelope widening across mandate renewals without a signed change |
| `audit-tampering` | A screening result written after the fact by a system with an interest in the outcome |
| `evidence-repudiation` | A dispute in which the institution and the client hold different accounts of what was authorized |

## What Proof-of-Control does not verify here

- **Whether the sanctions list was current, complete or correct.** Proof-of-
  Control establishes which list version was applied. Whether that version
  reflected the law on that day is somebody else's obligation.
- **Whether a name match is the right person.** Screening quality is
  validation. A false negative that clears an evidence gate is still a false
  negative.
- **Whether the ceilings were the right ceilings**, or the approved corridors
  the right corridors. That judgment belongs to the client and the institution.
- **Whether the payment settled with the beneficiary's bank.** Proof-of-Control
  covers the control-governed actions the agent took. It does not confirm that
  an action's effects settled in the outside world.
- **Whether the foreign-exchange rate was good**, or the payment commercially
  sound. A payment inside every control can still be a poor payment.
- **Covert side-channel exfiltration** of beneficiary data, and whether the
  privacy policy governing that data is adequate.
- **The correspondent's side of the transaction.** A Tier 4 claim holds for the
  interactions the institution's systems mediate. Where a correspondent
  produces no attestation, the claim stops at that boundary and the submission
  should say so rather than implying coverage across it.

## Residual trust assumptions to disclose

- The sanctions-list provider, the list version applied, and how version
  freshness is enforced at the gate.
- The time source the ceilings are measured against, since a daily aggregate is
  meaningless without an agreed clock.
- Custody of the signing keys, and what an operator with access to them could
  do to a record that is otherwise tamper-evident.
- The attestation chain at the executing host, with version, freshness and
  revocation policy.
- The monitor set for the transparency log, who operates each monitor, and what
  happens if monitors lapse or act together.
- The boundary at which the chain stops attesting, named explicitly, which for
  most institutions today is the correspondent.

## Notes / open questions

- Whether the aggregate gate belongs at the institution or at the client's
  treasury system is a design decision reasonable people will place
  differently. Placing it at the institution makes it enforceable and gives the
  client a party to trust; placing it at the client removes that trust and
  makes the institution's own record incomplete.
- A supervisor may reasonably regard a Tier 3 claim as sufficient where a
  correspondent settlement window allows recall. The argument above assumes
  finality, which is the common case rather than the universal one.
- Where the institution's declared control set is published, an evaluator can
  compare it against the evidence stream. Where it is not, a control asserted
  in policy and never wired into the release path produces no evidence either
  way, and no tier surfaces that.
- Submitted to AAI-Society/openverification as [pull request #11](https://github.com/AAI-Society/openverification/pull/11) by the Advanced AI Society (GitHub @tricia-wang-work), as a draft open for comment, and ported here when the use-case corpus moved into this repository.
