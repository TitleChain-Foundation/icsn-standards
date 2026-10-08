---
industry: e-commerce
use_case: AI shopping agent completes purchases on behalf of a consumer
business_impact: Increased chargebacks and fraud liability
submission_type: scenario
claimed_tier: 3
threats:
  - excessive-agency
  - autonomy-creep
  - unbounded-consumption
  - evidence-repudiation
---
# Consumer Shopping Agent Exceeds Authorized Purchase Scope

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
A consumer authorizes their AI shopping agent to purchase a specific item
under $200. The agent expands its search parameters, finds a "better" option,
and charges $340 to a saved payment card without re-authorization. The
consumer disputes the charge. The retailer and payment processor have no
cryptographic record of what the agent was actually authorized to do — only
the agent's own logs, which the operator controls.

## Claimed tier: Tier 3
Reaching Tier 3 requires that the delegation credential binding the agent to
its authorized spend scope be independently verifiable — not just logged by
the platform. Any party (consumer, retailer, payment processor, regulator)
must be able to confirm what the agent was authorized to do without relying
on the operator's word or privileged access to internal systems.

## Why not one tier down?
At Tier 2, a third-party auditor can check whether the agent stayed within
scope — but only with privileged access to platform logs. Those logs are
produced by the same operator being questioned. In a dispute, this is
circular: the consumer cannot independently verify the authorization record
without trusting the platform. Tier 3 removes that dependency. The
authorization credential is verifiable by the consumer, the card network, or
a regulator without any cooperation from the platform.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 3    | Must be independently verifiable which agent acted and under whose authorization, without relying on platform logs |
| Privacy       | 2    | Purchase data is sensitive but third-party audit of authorization records is sufficient; open publication not required |
| Portability   | 1    | Not a primary risk domain for this use case |
| Authorization | 3    | Spend scope and delegation must be cryptographically bound and checkable by any party in a dispute |
| Identity      | 3    | Consumer must be able to prove the agent acting was the one they authorized, not a spoofed or substituted agent |
| Security      | 2    | Transport and session security is sufficient; no need for self-enforcing execution constraints at this tier |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `excessive-agency` | The agent holds a saved payment card and can charge it for more than the one item and the one price the consumer authorized |
| `autonomy-creep` | The agent widens its own search parameters and substitutes a "better" option, taking a decision the consumer never delegated |
| `unbounded-consumption` | The $200 cap is the boundary that should have gated the transaction, and a $340 charge crosses it without a re-authorization step |
| `evidence-repudiation` | In the chargeback dispute the only account of what the agent was permitted to do is the operator's own logs, so the consumer is contesting the platform's record with nothing of their own |

## What Proof-of-Control does not verify here
- **Whether the purchase was a good one.** The substituted item may genuinely
  be better. Proof-of-Control evidences what the agent was authorized to do and
  what it did; it does not price-check, compare products, or judge whether the
  consumer would have approved had they been asked.
- **Whether the authorized scope was set sensibly.** A $200 cap the consumer
  set carelessly is still the cap. Proof-of-Control shows the boundary held or
  did not. It does not tell you the boundary was the right one, and a purchase
  inside an over-generous grant produces no violation.
- **The merchant's and processor's own handling.** The evidence establishes
  what the agent was permitted to charge. Whether the retailer captured the
  right amount, or the processor settled it correctly, is outside the record.
- **Delivery and fulfilment.** Verification covers the authorization and the
  transaction. Whether the item arrives, matches its description, or is
  returnable is not something a delegation credential speaks to.
- **What a disputed charge meant.** The record settles whether the agent held a
  valid grant for $340. Liability for the overcharge, and whether the consumer
  is made whole, are commercial and regulatory questions.
- **Prevention.** At Tier 3 the credential is checkable by any party after the
  fact. The card has still been charged, and this claim does not refuse the
  transaction at the moment it is attempted.

## Residual trust assumptions to disclose
- **Root of credential issuance.** Who issued the consumer's identity and the
  delegation credential binding the agent to a spend scope, and how the
  consumer was proofed. A credential minted by the shopping platform on the
  strength of a logged-in session leaves the consumer relying on the same party
  they are disputing.
- **Key custody.** Whether the consumer holds the signing key for their own
  grants, or the platform issues delegations on their behalf. If the platform
  holds it, the independent verifiability the Tier 3 claim rests on is
  cosmetic.
- **Attestation chain.** Version, freshness window and revocation policy,
  including how a reduced or withdrawn spend cap reaches an agent mid-session
  and what the propagation window permits.
- **Transparency log monitors.** Who monitors the log a card network or
  regulator would check, and what happens if the monitor set lapses. An
  unmonitored log can present different histories to the consumer and the
  platform, which is exactly the dispute this use case is trying to settle.
- **Agent to consumer binding.** Any point where the agent instance presenting
  a credential is assumed to be the instance the consumer authorized, including
  after an update, a migration or a restart on different infrastructure.
- **Scope semantics.** That "under $200" means the same thing to the consumer,
  the agent and the retailer: per item or per basket, before or after tax,
  shipping and currency conversion. The cryptography binds a number, and the
  parties are trusted to agree on what the number counts.

## Notes / open questions
- Reasonable to argue Tier 4 if the use case involves high-value purchases or
  financial services context where fail-closed enforcement (agent cannot
  execute if credential is invalid) is warranted.
- The line between Tier 3 and Tier 4 here turns on whether detection after
  the fact is tolerable — for a $340 overcharge, it may be; for a $34,000
  one, it may not.
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
