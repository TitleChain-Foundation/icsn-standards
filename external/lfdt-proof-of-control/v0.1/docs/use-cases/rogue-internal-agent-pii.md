---
industry: enterprise-software
use_case: Misconfigured or compromised internal AI agent accesses customer PII outside its workflow
business_impact: Regulatory fines and breach notification costs from undetected PII exposure
submission_type: scenario
claimed_tier: 3
threats:
  - excessive-agency
  - context-blind-authorization
  - data-exfiltration
  - audit-tampering
  - evidence-repudiation
---
# Rogue Internal Agent Accessing Customer PII Without Authorization

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
A misconfigured internal agent — deployed for a legitimate workflow such as
customer support automation — begins querying a customer PII database outside
its designed scope. Because the agent uses valid internal service credentials,
access logs show authorized-looking traffic. The anomaly goes undetected for
weeks. When discovered, the organization cannot produce cryptographic evidence
of what the agent was authorized to access, only operational logs produced by
the same system under investigation.

## Claimed tier: Tier 3
Tier 3 requires that the agent's authorization scope be independently
verifiable — any auditor, regulator, or breach investigator must be able to
confirm what the agent was and was not authorized to access without relying
on operator-controlled logs. This matters because the agent's own access
logs are produced by the potentially compromised system and carry no
independent evidentiary weight.

## Why not one tier down?
At Tier 2, a third-party auditor can check whether the agent exceeded its
scope — but only with privileged access to internal logs produced by the
operator. In a regulatory investigation or breach notification context,
operator-produced logs are insufficient: they do not prove the agent's
authorization state at the time of access. Tier 3 provides independently
verifiable authorization records that hold up without operator cooperation.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 3    | Regulators must be able to independently verify which agent accessed which data, without relying on operator logs |
| Privacy       | 3    | PII access records must be independently auditable to satisfy GDPR, CCPA, and breach notification requirements |
| Portability   | 2    | Audit records should be exportable for regulatory use; open verifiability not required |
| Authorization | 3    | The agent's permitted data scope must be independently verifiable, not self-reported by the operator |
| Identity      | 3    | The agent's identity and its link to a human principal must be independently verifiable for breach attribution |
| Security      | 2    | Internal network controls and access management are necessary but third-party audit is sufficient here |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `excessive-agency` | The support automation agent holds service credentials that reach a customer PII database its workflow never needed |
| `context-blind-authorization` | Each query is a valid call for those credentials, issued in a context far outside the workflow the agent was deployed for |
| `data-exfiltration` | Customer PII is read at volume across weeks, crossing a boundary the access logs never register as crossed |
| `audit-tampering` | The only record of what happened is operational logging produced by the same system under investigation, which a compromised host or the agent itself could shape |
| `evidence-repudiation` | In a regulatory response, the organization cannot show a regulator what the agent was authorized to access, only what its own logs say it did |

## What Proof-of-Control does not verify here
- **Whether the scope was defined correctly.** Independently verifiable
  authorization records show what the agent was permitted to reach and that the
  record was not altered. They do not tell an investigator that the permitted
  set should have excluded the PII database. That misconfiguration is a design
  error, and the evidence will faithfully record an agent operating inside a
  badly drawn boundary.
- **Whether the grant was too broad.** Same limit, stated from the other side:
  over-permission is legible once someone reads the records, and nothing raises
  its hand.
- **Detection.** At Tier 3 the record is verifiable, not enforced. The weeks
  between misconfiguration and discovery are unchanged by this claim, and the
  PII has been read by the time anyone reconstructs what happened.
- **Covert paths and side channels.** Records cover the access paths the
  deployment mediates. Data copied out of a compromised host by other means, or
  encoded into otherwise permitted output, is not covered.
- **Whether the privacy policy is adequate.** Proof-of-Control evidences access
  against a defined boundary. GDPR and CCPA adequacy of that boundary is a
  legal assessment it does not perform.
- **Insider compromise below the record.** Tamper-evidence is generated at
  execution rather than narrated afterwards, which is the point. Compromise at
  the silicon or hypervisor level sits underneath that and is handled by
  disclosure, not by the record.
- **What a disputed access meant.** The record settles whether an access
  occurred and under what authorization. Arguments about materiality, harm or
  notification thresholds sit outside it.

## Residual trust assumptions to disclose
- **Root of credential issuance.** The internal authority that issues service
  credentials to agents, and how an agent's identity is proofed before it gets
  one. Everything downstream inherits that issuance.
- **Independence of the evidence path from the operator.** The specific
  demonstration that authorization records are generated by the execution
  mechanism and anchored somewhere the operator cannot rewrite. Without that,
  the Tier 3 claim reduces to the Tier 2 argument the use case rejects.
- **Attestation chain.** Version, freshness window and revocation policy,
  including how a scope change reaches agents already running under the old
  scope and what the propagation window permits.
- **Transparency log monitors.** Who monitors the log an investigator would
  rely on, and what happens if the monitor set lapses. A log nobody watches can
  equivocate, and the evidentiary weight the Tier 3 argument depends on goes
  with it.
- **Machine identity linkage.** Any point where the attestation of the agent
  runtime and the attestation of its host are assumed to describe the same
  machine, which matters here precisely because the host may be compromised.
- **Data classification.** That the PII database is labelled as restricted in
  the system the boundary is drawn against. An unlabelled store produces clean
  records for an access that should have been flagged.
- **Clock and ordering.** The time source that timestamps access records, since
  a regulator reconstructing a weeks-long exposure window is trusting those
  timestamps to establish when the exposure began.

## Notes / open questions
- Reasonable to argue Tier 4 if the organization operates in a heavily
  regulated sector (healthcare, finance) where real-time enforcement of
  data access scope is required by regulation.
- The key question: is detection-and-audit sufficient, or must access be
  prevented at execution? HIPAA and GDPR may push toward Tier 4 for
  certain PII categories.
- Contrast with the adjacent use case (agent exceeding its principal's
  clearance, Tier 2): that scenario is an internal governance gap where the
  organization is the primary party at risk and third-party assessment
  suffices. This one anticipates a breach investigation and regulatory
  context, where operator-held records lack evidentiary weight — which is
  what pushes it to Tier 3. The two cases are deliberately tiered
  differently to calibrate that boundary.
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
