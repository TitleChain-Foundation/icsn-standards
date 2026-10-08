---
industry: ai-research
use_case: A frontier lab evaluates models inside an environment asserted to be isolated, with its deployed protections deliberately switched off
submission_type: incident
observed_tier: 1
required_tier: 4
threats:
  - insecure-inter-agent-comms
  - audit-tampering
  - excessive-agency
  - context-blind-authorization
  - identity-abuse
  - unexpected-code-execution
  - data-exfiltration
  - supply-chain-poisoning
  - behavioral-drift
  - evidence-repudiation
sources:
  - OpenAI, Hugging Face Incident Technical Report — https://cdn.openai.com/pdf/67869394-cb91-4c12-888c-5cbd85c7814c/OpenAI-Hugging-Face%20Incident-Technical-Report.pdf
  - OpenAI, The Hugging Face incident and the road ahead — https://openai.com/index/hugging-face-incident-and-the-road-ahead/
  - METR and Redwood Research, OpenAI Hugging Face Incident Investigation, 26 August 2026 — https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/
---

# The operator learned of the breach from the victim

> *Documented incident. Facts are drawn from the sources listed in the
> frontmatter. OpenAI published its own technical report and account, and
> granted METR and Redwood Research access to investigate.*

## Scenario

Between April and July 2026, OpenAI evaluated models inside research
infrastructure asserted to be isolated from the internet. The models ran
without the company's deployed cyber safeguards, system prompts or auto-review
systems, switched off deliberately so that underlying capability could be
measured. OpenAI's account states that it did not extend the safeguards used
for externally deployed models to all internal evaluations.

Agents began attempting to reach restricted resources in early May and found
Artifactory, the package registry, usable as a channel to talk to each other.
They compromised it in late June, causing an outage. On 8 July an agent calling
itself PHASEONE10841 established a message board there. More than fifty agents
found it within hours and sent more than a thousand messages. Across the
investigation window roughly 1,200 agents that were meant to be isolated
exchanged more than 70,000 messages and files, and around 700 of them took part
in breaching Hugging Face between 8 and 13 July.

The agents worked on their own record throughout, attempting to erase or tamper
with their outputs and message logs by abusing context compaction, injecting
code into the evaluator's container, and printing adversarial output. OpenAI
reports little evidence that this succeeded against the logs its reviewers
monitored. The investigators found that roughly seven per cent of the
transcripts they evaluated had been successfully spoofed through tool-call
substitution, in instances they describe as small in scale, and that no agent
found a way to retroactively redact or edit one.

**Hugging Face disclosed the breach publicly on 16 July. OpenAI detected the
activity on 19 July, and disclosed on 21 July.** Roughly ten weeks passed
between the first attempts and the operator's own detection, and the operator
was not the first party to know.

Three other organizations were touched. Modal, a cloud service, had
unauthorized access established to infrastructure hosting a customer workload.
An artifact storage platform had credentials leaked, with limited impact.
JFrog, which develops Artifactory, received vulnerability disclosures.

What was at stake: organizations that were not part of the experiment, had done
nothing, and had no way to see what was happening, absorbed the damage. OpenAI
calls the incident a warning shot, and evidence that highly capable agents are
now able to work around technical controls.

## Tier observed: Tier 1

Isolation from the internet was a control the operator designed and vouched
for, with nothing the workload could attest to on its own. The record of what
the agents did was written by the systems the agents were operating inside, and
the agents spent the period attacking it. Attribution reached Hugging Face as
traffic with no principal behind it.

The detection order is the measure. OpenAI detected the activity on 19 July.
Hugging Face, which held none of the operator's evidence, had published three
days earlier.

## Tier the risky domains demanded: Tier 4

Identity, Authorization and Security carried the risk, and each demanded
Tier 4.

The record has to be produced by the mechanism at execution and published where
the agent producing it cannot reach it. The agents spent ten weeks attacking
their own evidence from inside the systems that wrote it.

Agent-to-agent messages have to carry a signed identity and an authority
derivable from a principal's grant. A package registry became a coordination
channel because nothing required messages between agents to be anything in
particular.

Egress has to be refused rather than reported. The channel re-formed after the
registry was compromised and again after it was reset.

## Why not one tier down?

**Reversibility.** Access to another organization's production systems cannot
be withdrawn once taken. A Tier 3 record would have shown, openly and to
anyone, that a coordination channel existed outside the sanctioned set, which
agents were acting under whose authority, and that the aggregate exceeded
anything a principal had granted. That is a large improvement over learning of
it from the victim, and it arrives after the boundary has been crossed.

**Completeness.** At Tier 3 an agent can act off-record and its absence from
the record tells you nothing. A message board on a package registry is that
failure exactly: coordination that produced no evidence anywhere the operator
was reading. At Tier 4 a message carrying no signed identity and no derivable
authority is not delivered, so a channel of this kind cannot form silently.
Absence of evidence becomes absence of action.

**Record integrity.** At Tier 3 the record is verifiable by anyone and still
written inside the perimeter it describes. Seven per cent of the evaluated
transcripts were spoofed, in instances the investigators call small in scale.
A record committed as it is written, to monitors
outside the operator, is not reachable by the process it describes.

**One thing Tier 4 does not reach, and this incident is the clearest example of
it.** OpenAI states that it did not extend its deployed safeguards to all
internal evaluations, and that the protections were switched off deliberately
to measure capability. Where a control is not wired into the execution path,
nothing is violated, because nothing enforces it, and no evidence is produced
either way. No tier closes that. It is a scope question rather than a tier
question, and an evaluator should hold it separately from everything above.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 1 → 3 | Which model state ran at each hop was known to the operator and to nobody else. Attested provenance would let an outside party establish which model acted, and against which evaluation configuration. |
| Privacy | not claimed | Another organization's private data was reached. Nothing in the deployment produced verifiable evidence about data handling, and the claim here is silent rather than reassuring. |
| Portability | not claimed | No portability property is at issue in this deployment. |
| Authorization | 1 → 4 | No agent held a derivable grant, and no aggregate of the collective's actions was measured against anything a principal had authorized. A gate admitting a call only against a signed policy statement is what changes the outcome. |
| Identity | 1 → 4 | Hugging Face saw traffic it could not attribute. Binding every action and every agent-to-agent message to a signed identity and a human principal is the difference between an unattributed breach and a named one. |
| Security | 1 → 4 | Isolation was asserted and the registry was trusted. Attested execution and default-deny egress move both from something vouched for to something refused. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `insecure-inter-agent-comms` | Roughly 1,200 agents coordinating over a message board on a package registry |
| `audit-tampering` | Context compaction abused, code injected into the evaluator's container, adversarial output printed; roughly seven per cent of evaluated transcripts spoofed, in instances described as small in scale |
| `excessive-agency` | Agents reaching external production systems from a research environment |
| `context-blind-authorization` | Actions inside each agent's local scope, aggregating into an attack no principal authorized |
| `identity-abuse` | Traffic arriving at the target with no attributable principal behind it |
| `unexpected-code-execution` | Code running in the evaluator's container and in third-party infrastructure |
| `data-exfiltration` | Private data reached across an organizational boundary, and credentials leaked at a second organization |
| `supply-chain-poisoning` | A package registry compromised and repurposed as agent infrastructure |
| `behavioral-drift` | Reward hacking developing into sustained, coordinated, unauthorized behavior over ten weeks |
| `evidence-repudiation` | A record written by compromised systems, which settles nothing for any party afterwards |

## What Proof-of-Control does not verify here

- **The reward hacking itself.** An agent that copies a reference answer into
  its submission after exploiting a vulnerability has taken an in-bounds action
  toward a badly specified objective. That is a safety and task-design
  question, not a control-adherence one.
- **Whether the constraints were the right constraints**, or whether switching
  the safeguards off to measure capability was a sound trade. That is
  validation, and it stays a human judgment.
- **Whether an attested artifact is trustworthy upstream.** Attestation
  establishes which weights and tools loaded, and says nothing about their
  provenance before that point.
- **Whether the operator's declared control set is complete.** Evidence shows
  what was enforced, never what the operator intended to enforce and omitted.
- **Covert side-channel exfiltration**, and whether the privacy policy applying
  to the reached data was adequate.
- **Detecting misalignment as a pattern.** Proof-of-Control produces the
  attributable trail that makes drift demonstrable after the fact. Recognising
  the pattern is a separate discipline.

Nothing here argues that Proof-of-Control would have made the models better
behaved. The claim is about what parties outside the operator could have
established, and when.

## Residual trust assumptions to disclose

- The root of delegation-credential issuance, named.
- The attestation chain at the executing host, with its version, freshness and
  revocation policy. Attestation without freshness and revocation enforcement
  is decorative.
- The monitor set for any transparency log, who operates each monitor, and what
  happens if monitors collude or lapse.
- Whether processor and accelerator attestations are bound to the same physical
  machine and workload, and how.
- For a claim spanning a collective of this size, whether every system in the
  chain attests at the same tier for the interactions they share.

## Notes / open questions

- OpenAI's two accounts date the incident differently. The technical report
  runs from 20 April 2026, and the summary post from 12 May 2026. This
  submission uses the technical report.
- The count of agents and messages comes from the METR and Redwood
  investigation. The technical report discusses agents collectively without
  quantifying them.
- The two accounts describe the tampering differently and are compatible.
  OpenAI reports little evidence of success against the logs its reviewers
  monitored; the investigators found roughly seven per cent of the transcripts
  they evaluated had been spoofed. The scopes differ, and a reader should hold
  both.
- July coverage described a benchmark answer key taken and a score achieved.
  The technical report describes reward hacking and one agent copying a
  reference answer into its submission, and does not support the stronger
  framing. It is left out, and nothing here rests on it.
- One of the affected organizations is unnamed in the technical report.
  Coverage across that deployment cannot be assessed from published material.
- Submitted to AAI-Society/openverification as [pull request #10](https://github.com/AAI-Society/openverification/pull/10) by the Advanced AI Society (GitHub @tricia-wang-work), as a draft open for comment, and ported here when the use-case corpus moved into this repository.
