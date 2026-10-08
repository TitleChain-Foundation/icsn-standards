---
industry: business-operations
use_case: An owner's AI agent pays an approved vendor invoice; the executing provider is replaced mid-task, and the authority and receipts must survive the switch.
submission_type: scenario
claimed_tier: 3
threats:
  - context-blind-authorization
  - excessive-agency
  - evidence-repudiation
---

# Provider replacement under a live mandate

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

Mara runs a small distribution business. She gives her AI agent a signed, bounded
mandate: pay invoice INV-2041 to Acme Supply, $4,800, due October 3, and only after
the delivery-confirmation photo is logged. Nothing else. The mandate lives with an
independent receiver, not with the agent or its provider: every action the agent
takes is checked against the mandate at the boundary, and each check produces a
receipt Mara or an auditor can verify with published tooling.

Halfway through, Mara's agent provider has an outage. The task moves to a different
provider's agent, which resumes from the last accepted checkpoint. The new agent
never received Mara's mandate directly. It inherits the checkpoint and the
receiver's receipts, nothing more. (This pattern has a controlled demonstration in
APPROVED_JOB_LIVE_001: a partial checkpoint produced by one provider, continued by
another from that exact checkpoint with the agreement digest unchanged and
acceptance decided by the receiver rather than the successor — a local harness
run; no real payment was involved.)

Then the hard case. The payment executes at the bank, but the closure record — the
receiver's confirmation that the effect settled and the mandate is spent — never
arrives. Mara revokes the mandate minutes after the payment, before confirmation
returns. Out-of-mandate actions stopped at the boundary with the receipt preserved
likewise has a controlled demonstration (CREDENTIAL_OVERREACH_CONTAINMENT_ENFORCED:
a valid credential used outside its mandate was stopped with zero effects and the
STOP receipt kept — a sandbox-local run; no real consequence was at stake.)
Neither demonstration involved a real bank payment or real money; the settlement
step in this scenario is hypothetical.

This scenario separates three things the standard currently treats together:

1. **Detecting that a closure record is missing** — 7.6.2: the sequence gap tells
   the verifier a record is absent.
2. **Stopping subsequent actions** while evidence cannot be generated — 7.6.3:
   fail-closed refusal by the gateway.
3. **Reconciling whether the original effect occurred** — the payment shows as
   authorized, the bank feed says the money moved, but no closure record exists.
   Nothing between Level 2 and Level 4 requires this reconciliation, yet it is the
   step that decides what happens next: until the effect is reconciled, the mandate
   must treat the payment as pending — never as failed — and an unresolved outcome
   must not authorize a blind retry, which would risk paying the invoice twice.

## Claimed tier: Tier 3

The claim turns on whether Mara or an auditor can verify, without trusting either
provider, that the payment was inside the mandate she actually signed. The mandate,
the authorization receipts, and the sequence chain are checkable with published
tooling; no trusted party must be believed. The provider switch is the point: at
the moment the executing provider changes, any trust placed in the old provider is
worthless, and the new provider has earned none.

## Why not one tier down?

Tier 2 asks the auditor to trust a third party — typically the operator or an
attestor. Here the operator changed mid-task, and the new operator's attestation
covers a mandate it never received. There is no third party left to trust that is
not one of the two providers. Two tests confirm the placement. Reversibility: money
that has settled cannot be un-sent; detection after the fact is not a remedy, and
it still leaves the closure gap open. Completeness: Tier 3 verifies the records
held were not altered, but does not guarantee the record is whole — which is
exactly why the missing closure record is the case this scenario is built around.
Tier 4 would require that an action cannot execute without producing evidence; the
payment settles on rails outside the evidence boundary, so the gateway can refuse
to authorize but cannot make the absence of a closure record mean the effect did
not happen. Tier 4 is not satisfiable for effects that settle outside the boundary.

## Tier by domain

| Domain | Tier | Why |
| --- | --- | --- |
| Provenance | 2 | Which provider and model ran each step is attested by the providers; no outsider-verifiable mechanism is claimed. |
| Privacy | 1 | Invoice details are captured in queryable records; identifying fields are redacted from receipts shared with auditors. |
| Portability | 3 | The provider-to-provider crossing carries the most risk; the mandate and receipts cross in a schema-defined, signed form the new provider cannot forge. |
| Authorization | 3 | Every action is checked against the mandate by the receiver, and each check is evidence verifiable without trusting the agent or its provider. |
| Identity | 2 | Which agent and which principal ran each step is attested; the successor agent's identity is bound to the continuation. |
| Security | 2 | The agent's signing-key lifecycle is attested; key custody is disclosed, not trust-minimized. |

## Threats exercised

| Threat | What it looks like here |
| --- | --- |
| `context-blind-authorization` | The successor agent inherits execution context but not the mandate. An authorization that traveled with the conversation instead of the mandate would let it pay the wrong invoice or the wrong amount. |
| `excessive-agency` | After Mara revokes the mandate, the successor agent must not complete the payment. The revocation has to reach the receiver before the next authorized action. |
| `evidence-repudiation` | After the provider switch, the old provider could deny what its agent did, or the new provider could deny the inherited checkpoint. The receipts are non-repudiable evidence of which actions were authorized. |

## What Proof-of-Control does not verify here

Verification is not validation. Proof-of-Control shows what the agent did and
whether each action stayed within the mandate. It does not show whether the
invoice was legitimate, whether the delivery photo actually showed the goods,
whether Mara's mandate terms were wise, whether the authorized boundary was
correctly defined, whether the grant was too broad, disputes about what the
payment meant rather than whether it occurred — or, the gap this scenario is built
to surface, whether the bank settled the payment when the closure record is
missing.

## Residual trust assumptions to disclose

The receiver's key custody and how fast revocation propagates to it; the device
that signed Mara's mandate; the bank's payment feed as the source of "the effect
completed"; the schema and canonicalization the receipts use (C7.7) — verifier and
receiver must parse the same bytes; and the monitor set that would notice a missing
anchor or an unreconciled gap.

## Notes / open questions

- Question for the maintainers: should the standard require — plausibly as a Level
  3 requirement — that when an effect is claimed but its closure record is missing,
  the system must reconcile whether the effect occurred before the mandate is
  closed or any retry is authorized? The current text conclusively supports
  detection (7.6.2) and refusal of subsequent actions (7.6.3), but I could not find
  a requirement covering reconciliation. If one exists, this scenario misreads it
  and I welcome the correction.
- Separate question for the working group: whether continuity of authority and
  evidence across a provider boundary belongs in C7.7 (the Interoperable Property)
  or as the fifth evidence property noted in Appendix D, issue 5. This scenario's
  Tier 3 claim depends on continuity, but the property-count question is
  independent of the reconciliation question above.
