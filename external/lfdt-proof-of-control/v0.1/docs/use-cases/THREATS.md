# Threat vocabulary for use-case submissions

This is the controlled vocabulary for the `threats:` field in a use-case
submission. Tag every threat the deployment exercises, using the slug in the
first column.

The middle column tells you what a Proof-of-Control claim addresses for that
threat, which is what the tier-by-domain table has to argue about. The right
column is the source for the "What Proof-of-Control does not verify here"
section: copy the out-of-scope entries for the threats you tagged, then add
anything specific to your deployment.

A tag is not a claim. Tagging `audit-tampering` says the deployment is exposed
to it, not that the deployment defends against it.

---

## Instruction and goal manipulation

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `prompt-injection` | Prompt injection / goal hijacking | Crafted input redirects the agent's objective | Gates and records the out-of-bounds action the injection attempts; evidence of what the agent did | The injection itself; an in-bounds harmful action is a safety question |
| `bent-goals` | Poisoned or bent goals | A clean model pursues a silently altered goal | Attests the integrity of the goal specification; evidence that the goal which ran is the goal authorized | A subtly wrong objective that never alters the specification |
| `system-prompt-leakage` | System prompt leakage | The agent discloses its own instructions | Not addressed; can record that an output occurred | Whether the model discloses its own instructions |

## Memory, knowledge, and supply chain

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `memory-poisoning` | Memory and context poisoning | Contaminated memory steers future decisions | Verifies provenance of memory writes and reads; evidence of lineage; gates unattested sources | A validly sourced but misleading note |
| `rag-weakness` | Vector, embedding or retrieval weakness | Poisoned retrieval corrupts what informs a decision | Provenance of retrieved data; evidence of what informed the decision | The relevance or quality of what was retrieved |
| `model-poisoning` | Training-time data or model poisoning | Backdoors or bias baked in before deployment | Verifies which model and weights ran, as attested provenance | The training process itself, which is pre-deployment |
| `supply-chain-poisoning` | Poisoned supply chain, tools or MCP | Compromised tools, models or servers enter the stack | Attests which weights, tools and artifacts loaded; unattested artifacts cannot be admitted | Whether an attested artifact is itself trustworthy upstream |

## Identity, authority, and inter-agent trust

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `identity-abuse` | Identity and privilege abuse or spoofing | An agent claims authority it was not granted | Cryptographic identity; binds every action to a principal; verifiable delegation chain | Credential theft or social engineering at the human level |
| `context-blind-authorization` | Context-blind authorization | An in-scope call made in the wrong context | Verifies the authorization decision and boundary adherence; records that the boundary held | Whether the authorized boundary was correctly defined |
| `excessive-agency` | Excessive agency or over-permission | The agent can do more than its task needs | Evidences what authority was exercised and whether actions stayed in bounds; gates over-scope | Whether the grant was too broad |
| `insecure-inter-agent-comms` | Insecure inter-agent communication | Forged, unauthenticated or unsanctioned agent-to-agent messages | Verifies message authenticity and integrity; binds messages to signed identities; evidences the delegation chain | Latency or performance cost of evidence at boundaries |

## Tools, actions, and effects

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `tool-misuse` | Tool misuse | A legitimate tool used for an unintended, harmful purpose | Evidences every tool call and its arguments; gates disallowed calls | A valid in-scope call that is ill-advised |
| `unexpected-code-execution` | Unexpected code execution | The agent runs code in an unintended context | Evidences code-execution calls and gates them by authorization | Malice within permitted execution, which needs sandboxing |
| `unsafe-actuation` | Unsafe actuation | The agent drives a device or action outside its envelope | Gates and records actuation within a signed envelope | Whether a within-envelope action is sound, and whether the envelope was set correctly |
| `improper-output-handling` | Improper output handling | Unvalidated output triggers a downstream exploit | Evidences the output and where it flowed | Validating and sanitizing the output, which is the consuming system's job |

## Data exposure

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `data-exfiltration` | Sensitive data exfiltration | Protected data leaves its boundary | Evidences data access and boundary crossings; gates unauthorized egress | Covert side-channel exfiltration; whether the privacy policy itself is adequate |

## Autonomy, drift, and lifecycle

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `autonomy-creep` | Autonomy creep | The agent's autonomy quietly expands | Evidences the signed autonomy envelope and every change; gates out-of-envelope actions | Quality degradation within the envelope |
| `behavioral-drift` | Rogue agents or behavioral drift | Sustained drift into misaligned behavior | Produces the attributable evidence trail that makes drift detectable and demonstrable after the fact | Detecting the misaligned pattern itself |
| `scope-creep-lifecycle` | Scope creep and lifecycle | Unreviewed change, or the wrong risk classification | Signed passport and change-control evidence; gates unreviewed changes | Whether the classification is correct |

## Record integrity and resilience

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `audit-tampering` | Audit tampering | A compromised host, or the agent itself, rewrites the record | Records are tamper-evident and generated by the mechanism at execution, rather than narrated by the operator | Insider compromise at the silicon level, disclosed through trust assumptions |
| `cascading-failure` | Cascading failure or fail-open | One failure propagates, or the system defaults to allow | Evidences failure and deny events; at the top level the system fails closed | Preventing propagation across a multi-agent system, which is architecture |
| `coverage-decay` | Coverage decay | Defenses pass once, then rot | Continuous self-verification; an ongoing rather than point-in-time record | Discovering new attack classes, which is red-teaming |
| `evidence-repudiation` | Evidence repudiation | The operator denies an action occurred | Cryptographic evidence is openly verifiable and non-repudiable | Disputes about the meaning or significance of an action, rather than whether it occurred |
| `trust-opacity` | Trust opacity | Residual trust is invisible and incomparable | Trust-assumption disclosure makes residual trust visible and comparable | Eliminating all trust assumptions; the standard requires disclosure, not elimination |

## Human oversight and disclosure

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `approval-fatigue` | Human-agent trust exploitation or approval fatigue | The agent games human oversight | Evidences the raw, true intent presented for approval, and the approval decisions | The human fatigue and social engineering itself |
| `undisclosed-ai` | Undisclosed AI or absent consent | The agent acts with no disclosure or consent | Verifiable consent and disclosure record; gates on consent | Whether the disclosure content was adequate |

## Output quality and availability

| Slug | Threat | What it is | What Proof-of-Control addresses | Out of scope |
|---|---|---|---|---|
| `misinformation` | Misinformation or hallucination | Confident, wrong output | Not addressed | Whether the output is correct; correctness is a range, not a point |
| `hidden-bias` | Hidden bias | Bias buried in the agent's decisions | Not addressed; can preserve a tamper-evident record of verdicts for a separate review | Assessing or correcting fairness, which is validation |
| `unbounded-consumption` | Unbounded consumption | Runaway resource use or cost | Evidences consumption and calls; a budget or rate cap set as a boundary can gate | Availability defense, which is mostly infrastructure |

---

## A threat with no coverage at any tier

One failure sits outside every row above. Where an operator asserts a control
that was never wired into the execution path, nothing is violated, because
nothing enforces it, and no evidence is produced either way. Silence is
indistinguishable from compliance.

A tier does not close this. Raising the tier strengthens the evidence for
controls that produce evidence, and an undeclared control produces none. If
your use case turns on this failure, say so in the notes rather than claiming
a tier that does not reach it.
