---
industry: enterprise-software
use_case: Legitimately deployed AI agent accesses data its human principal is not permitted to view
business_impact: Silent compliance violations and regulatory exposure with no detectable access breach
submission_type: scenario
claimed_tier: 2
threats:
  - excessive-agency
  - context-blind-authorization
  - data-exfiltration
---
# Authorized Agent Inheriting Permissions Beyond Its Human Principal's Clearance

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
A sales representative's AI agent, attempting to personalize an outreach
email, queries a customer's financial risk profile — data the sales rep
themselves has no clearance to view. The agent is legitimately provisioned
and uses valid credentials. The platform's access controls govern human
sessions but were not designed to constrain agent queries derived from those
sessions. The sales rep never sees the data directly; the agent uses it to
generate a recommendation. No access control violation is logged because the
agent's credentials are valid.

## Claimed tier: Tier 2
The core failure here is that the organization cannot see the problem at all:
its own access logs report only valid credentialed queries, so self-review
(Tier 1) reports a clean state. Tier 2 requires that an independent third
party — an auditor or compliance assessor with privileged access — can
evaluate whether agent permission scopes are actually bounded by each
principal's clearance, examining the delegation records and access mappings
directly rather than accepting the organization's own attestation. Because
this is an internal governance failure where the organization is both the
operator and the primary party at risk, third-party evaluation is the
proportionate bar: it surfaces the scope mismatch without requiring the
authorization records to be publicly verifiable.

## Why not one tier down?
At Tier 1, the organization self-attests that agents inherit their
principals' permissions. But this scenario exists precisely because that
attestation is wrong in a way the organization cannot detect: the credentials
are valid, no violation is logged, and internal review confirms a policy that
is not actually enforced. Self-reporting cannot surface a failure mode that
produces no internal signal. Tier 2 closes this by putting an independent
evaluator in front of the actual delegation scopes and access mappings, where
the mismatch between stated policy and effective agent permissions is
directly observable.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 2    | An auditor must be able to trace which agent queried which data under which principal's session, using privileged access to platform records |
| Privacy       | 2    | Whether restricted data categories are reachable by under-cleared agents must be independently assessed, as internal logs cannot reveal it |
| Portability   | 1    | Not a primary risk domain for this use case |
| Authorization | 2    | Third-party evaluation of delegation scopes against principal clearance levels is the load-bearing check for this failure mode |
| Identity      | 2    | The agent-to-principal binding must be evaluable by an assessor, not merely asserted by the platform |
| Security      | 1    | Standard internal access controls apply; no elevated verifiability claim is needed on this domain |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `excessive-agency` | The agent's effective permission set is wider than the sales rep's own clearance, so it can reach data its principal cannot |
| `context-blind-authorization` | The financial risk profile query is a valid call for the agent's credentials, made in a context (an outreach email for an uncleared rep) where it should not be permitted |
| `data-exfiltration` | Restricted data crosses a clearance boundary into a sales workflow, without leaving the organization and without tripping any access control |

## What Proof-of-Control does not verify here
- **Whether the authorized boundary was drawn correctly.** This is the sharpest
  limit at Tier 2. Proof-of-Control can show that an agent's queries stayed
  inside its granted scope and that the scope is what the delegation records
  say. It cannot tell you that scope should have been bounded by the
  principal's clearance in the first place. That judgement is the assessor's.
- **Whether the grant was too broad.** Over-permission is visible in the
  records once someone compares them against clearance levels. Nothing in the
  evidence flags it on its own.
- **Whether the data classification is right.** If the financial risk profile
  is not labelled as restricted, no boundary is crossed as far as the
  deployment is concerned, and the records will look clean.
- **The downstream use of what the agent retrieved.** Proof-of-Control
  evidences the access and where the data flowed. It does not follow the
  recommendation the agent generated into the email, the CRM, or the rep's
  head.
- **Controls that were asserted but never wired in.** The stated policy here is
  that agents inherit their principals' permissions. If that policy exists only
  in a document and nothing in the execution path enforces it, no evidence is
  produced either way, and silence is indistinguishable from compliance. No
  tier closes that gap. See the closing section of THREATS.md.

## Residual trust assumptions to disclose
- **Root of credential issuance.** The corporate identity provider that issues
  both the rep's session and the agent's service credential. It is the sole
  root here, and it is the same system whose scoping behaviour is in question.
- **The clearance record itself.** That the HR or entitlements system holding
  each principal's clearance level is accurate and current. An assessor
  comparing agent scope against clearance is trusting that source completely.
- **The assessor.** At Tier 2 a reader trusts the independent evaluator's
  access, competence and independence, and trusts that the sample of
  delegation records they examined was representative. There is no
  cryptographic record they can re-derive without that cooperation.
- **Attestation freshness and revocation.** How quickly a clearance change or a
  revoked delegation propagates to the agents already provisioned under it, and
  what a long propagation window permits in the meantime.
- **Binding of agent to principal.** Any point where the agent's service
  credential and the rep's session are assumed to represent the same principal,
  since that link is what the whole clearance argument rests on.
- **Retrieval layers outside the access-control path.** Where a vector store or
  cache holds material derived from restricted sources, a reader is trusting
  that its contents were scoped at write time, because query-time controls will
  not see it.

## Notes / open questions
- Reasonable people may place this higher. The Tier 3 argument: in a
  regulatory investigation, operator-held records may be insufficient and
  independently verifiable authorization records would be needed. The Tier 4
  argument: the violation has already occurred once the query executes, so
  detection is inherently too late and the delegation constraint ("an agent
  cannot be granted more than its principal holds") should be enforced
  fail-closed at execution. Regulated sectors (financial services,
  healthcare) likely justify those stricter stances; Tier 2 is the
  proportionate claim for general enterprise contexts.
- Contrast with the adjacent use case (rogue internal agent accessing PII,
  Tier 3): that scenario anticipates a breach investigation where
  operator-held records lack evidentiary weight. This one is an internal
  governance gap where the organization is the primary party at risk. The
  two are deliberately tiered differently to calibrate that boundary.
- This use case still illustrates why authentication and authorization must
  be architecturally separated: the agent is authenticated, and its
  authorization scope is the failure point.
- Open question: how does this interact with agentic systems that use RAG
  or vector databases, where data retrieval scope is not governed by
  traditional access controls?
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
