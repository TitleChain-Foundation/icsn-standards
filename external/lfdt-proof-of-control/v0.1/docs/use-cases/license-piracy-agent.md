---
industry: software-publishing
use_case: Previously flagged threat actor deploys AI agents to bulk-purchase and pirate software licenses at scale
business_impact: Revenue loss and inability to enforce prior bad actor history across synthetic agent identities
submission_type: scenario
claimed_tier: 3
threats:
  - identity-abuse
  - tool-misuse
  - undisclosed-ai
---
# Known Threat Actor Using Agents to Scale License Fraud Under New Identities

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
A threat actor previously identified for using bots to bulk-purchase software
licenses and resell pirated copies now deploys AI agents to do the same at
scale, cycling through synthetic identities to evade prior flagging. Each
agent presents a new, unconnected identity. The software publisher has no
mechanism to link the new agent identities to the known bad actor's
accountability chain — the prior violation history is invisible because the
actor's Responsible Party identity is not cryptographically bound to the
agents being deployed.

## Claimed tier: Tier 3
Tier 3 requires that the Responsible Party behind any agent be independently
verifiable by the software publisher, without relying on the actor's
self-reported identity. This allows prior violation history to attach to the
accountability chain regardless of how many synthetic identities are cycled
through. Any party — publisher, platform, enforcement body — can verify the
chain without privileged access to the publisher's internal fraud database.

## Why not one tier down?
At Tier 2, a third-party fraud auditor can check whether a given agent is
linked to a known bad actor — but only with privileged access to the
publisher's internal records and with the auditor's cooperation. This is
too slow and too dependent on platform cooperation to be operationally
useful for real-time purchase enforcement. Tier 3 makes the Responsible
Party chain independently verifiable at the point of transaction.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 3    | The Responsible Party behind any purchasing agent must be independently verifiable, regardless of synthetic identity cycling |
| Privacy       | 2    | Purchaser identity verification is standard; open publication of identity records is not required |
| Portability   | 2    | Fraud records should be portable across platforms; full open verifiability not required for this use case |
| Authorization | 2    | Purchase authorization is legitimate in isolation; the risk is identity laundering, not authorization scope |
| Identity      | 3    | Agent identity must be cryptographically bound to a Responsible Party whose history is independently verifiable |
| Security      | 2    | Standard platform security controls apply; the risk here is identity, not access control |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `identity-abuse` | Each agent presents a fresh synthetic identity, so the authority to purchase is claimed under a Responsible Party the publisher cannot connect to the known actor |
| `tool-misuse` | The publisher's ordinary purchase and licensing flow is used as designed, at scale, to acquire licenses for resale as pirated copies |
| `undisclosed-ai` | The agents transact without disclosing that they are agents or who stands behind them, so the publisher prices and approves each order as an unconnected buyer |

## What Proof-of-Control does not verify here
- **Whether a purchase should be refused.** Every individual order in this
  scenario is a valid, in-scope call. Proof-of-Control evidences the call and
  the Responsible Party behind it. The decision to decline a buyer is the
  publisher's fraud policy, not a verification outcome.
- **Whether an attested Responsible Party is trustworthy.** Binding an agent to
  a verifiable Responsible Party makes history attachable. It says nothing
  about whether that party is honest, and a first-time actor with a clean chain
  looks identical to a legitimate buyer.
- **The quality of the identity behind the Responsible Party.** The chain is
  worth exactly what the enrollment behind it is worth. A weak organizational
  proofing process produces verifiable credentials for a fictitious company.
- **Whether the disclosure was adequate.** Proof-of-Control can gate on a
  disclosure and record that one was made. It does not assess whether what was
  disclosed told the publisher anything useful.
- **What happens to the software afterwards.** Redistribution, key sharing and
  resale occur outside the deployment. Nothing in this claim follows a license
  once it has been legitimately issued.
- **Detection is after the fact at Tier 3.** The chain is verifiable at the
  point of transaction, and this claim does not refuse the sale on its own.

## Residual trust assumptions to disclose
- **Root of credential issuance for Responsible Party identity.** Which
  authority proofs an organization or individual before issuing the credential
  the agents chain to, and to what assurance level. If a `did:web` anchored to
  a domain is accepted, the reader is trusting domain control as a proxy for
  organizational identity, and domains are cheap.
- **Uniqueness at enrollment.** That the issuing authority prevents one actor
  from enrolling repeatedly under different organizational identities. Without
  it, identity laundering moves up a layer rather than stopping, and the whole
  argument fails quietly.
- **Attestation chain.** Version, freshness window and revocation policy,
  including whether a Responsible Party credential revoked by one issuer is
  visible to publishers relying on another.
- **Transparency log monitors.** Who monitors the log that makes prior history
  checkable across publishers, and what happens if the monitor set lapses.
- **Portability of violation history.** That a record of prior violations
  attaches to the Responsible Party rather than to one publisher's internal
  database, and that other publishers will honour it. This is a governance
  assumption, not a cryptographic one.
- **Agent to Responsible Party binding.** Any point where a signing key held by
  an agent is assumed to still be under the control of the Responsible Party
  that enrolled it, including keys that have been delegated onward.

## Notes / open questions
- This use case does not yet have a canonical public incident in the AI agent
  context. The bot-based version of this attack is well-documented; the agent
  version is an emerging threat pattern.
- Open question: what is the minimum Responsible Party verification required
  to satisfy Tier 3 here? did:web anchored to a real organization, or
  something stronger?
- Reasonable to argue Tier 2 if the publisher is willing to accept
  third-party fraud scoring as sufficient; Tier 3 is appropriate if the
  publisher needs to act without auditor cooperation.
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
