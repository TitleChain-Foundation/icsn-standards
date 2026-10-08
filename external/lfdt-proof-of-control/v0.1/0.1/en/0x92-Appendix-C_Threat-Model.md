# Appendix C: Threat Model (normative)

This appendix states, for each known agent threat, what Proof-of-Control defends against and what is explicitly out of scope. The threats are 27 catalogued classes drawn from the established agent-threat catalogs — MITRE ATLAS, NIST AI 100-2, and the OWASP Top 10s for LLM and Agentic Applications, which converge on the same core threat classes — plus two evidence-model threats, evidence repudiation and trust opacity, from the MAESTRO threat-modeling work, plus three composition-and-observability threats added from 2026 research (SCR-Bench, TraceSafe-Bench, AI Trust OS — see the [research basis](../../docs/research-basis.md); draft additions, working group to ratify).

Threats marked "not addressed" are the honest edge of the claim, and they match the determinism boundary ([C7.5](0x10-C07-Evidence-Generation-and-Properties.md)): Proof-of-Control verifies what an agent did, not whether the output was correct, fair, or wise.

## The Threat Landscape

Left unverified, agent behavior can go wrong in a wide range of known ways, grouped into families:

| Family | Threat | What it is |
| --- | --- | --- |
| Instruction and goal manipulation | Prompt injection / goal hijacking | Crafted input redirects the agent's objective |
| Poisoned / bent goals | A clean model pursues a silently altered goal |
| System prompt leakage | The agent discloses its own instructions |
| Memory, knowledge, and supply chain | Memory & context poisoning | Contaminated memory steers future decisions |
| Vector / embedding / RAG weakness | Poisoned retrieval corrupts what informs a decision |
| Training-time data / model poisoning | Backdoors or bias baked in before deployment |
| Poisoned supply chain / tools / MCP | Compromised tools, models, or MCP servers enter the stack |
| Identity, authority, and inter-agent trust | Identity & privilege abuse / spoofing | An agent claims authority it was not granted |
| Context-blind authorization | An in-scope call made in the wrong context |
| Excessive agency / over-permission | The agent can do more than its task needs |
| Insecure inter-agent communication | Forged or unauthenticated agent-to-agent messages |
| Tools, actions, and effects | Tool misuse | A legitimate tool used for an unintended, harmful purpose |
| Skill composition risk *(2026 research)* | Individually benign skills become dangerous when composed: capability flow, trust transfer, authorization blur |
| Unexpected code execution | The agent runs code in an unintended context |
| Unsafe actuation | The agent drives a device or action unsafely |
| Improper output handling | Unvalidated output triggers a downstream exploit |
| Data exposure | Sensitive info / PHI exfiltration | Protected data leaves its boundary |
| Autonomy, drift, and lifecycle | Shadow / undeclared agents *(2026 research)* | Agents deployed outside the governed inventory, invisible to oversight |
| Autonomy creep | The agent's autonomy quietly expands |
| Rogue agents / behavioral drift | Sustained drift into misaligned behavior |
| Scope creep / lifecycle | Unreviewed change or the wrong risk classification |
| Record integrity and resilience | Trajectory-monitor parsing failure *(2026 research)* | Validators miss unsafe tool trajectories they cannot structurally parse |
| Audit tampering | A compromised host rewrites the record |
| Cascading failures / fail-open | One failure propagates, or the system defaults to allow |
| Coverage decay / resilience | Defenses pass once, then rot |
| Human oversight and disclosure | Human-agent trust exploitation / approval fatigue | The agent games human oversight |
| Undisclosed AI / consent | The agent acts with no disclosure or consent |
| Output quality and availability | Misinformation / hallucination | Confident, wrong output |
| Hidden bias | Bias buried in the agent's decisions |
| Unbounded consumption / DoS | Runaway resource use or cost |

## Coverage: What Proof-of-Control Defends Against

*Coverage key: Full · Strong · Partial · Not addressed. Coverage rates how much of the threat the evidence reaches; the two detail columns say exactly what it reaches and where the boundary is.*

| Threat | Coverage | What Proof-of-Control defends against | Out of scope |
| --- | --- | --- | --- |
| Prompt injection / goal hijacking | Partial | Gates and records the out-of-bounds action the injection attempts; evidence of what the agent did | The injection itself; an in-bounds harmful action is a safety question |
| Poisoned / bent goals | Strong | Attests the integrity of the goal specification; evidence the goal that ran is the goal authorized | A subtly wrong objective that never alters the spec |
| System prompt leakage | Not addressed | Can record that an output occurred | Whether the model discloses its own instructions |
| Memory & context poisoning | Strong | Verifies provenance of memory writes and reads; evidence of lineage; gates unattested sources | A validly sourced but misleading note |
| Vector / embedding / RAG weakness | Partial | Provenance of retrieved data; evidence of what informed the decision | The relevance or quality of what was retrieved |
| Training-time data / model poisoning | Strong | Verifies which model and weights ran (attested provenance) | The training process itself, which is pre-deployment |
| Poisoned supply chain / tools / MCP | Strong | Attests which weights, tools, and artifacts loaded; unattested cannot be admitted | Whether an attested artifact is itself trustworthy upstream |
| Identity & privilege abuse / spoofing | Strong | Cryptographic identity; binds every action to a principal; verifiable delegation chain | Credential theft or social engineering at the human layer |
| Context-blind authorization | Strong | Verifies the authorization decision and boundary adherence; records that the boundary held | Whether the authorized boundary was correctly defined |
| Excessive agency / over-permission | Strong | Evidences what authority was exercised and whether actions stayed in bounds; gates over-scope | Whether the grant was too broad |
| Insecure inter-agent communication | Strong | Verifies message authenticity and integrity; binds messages to signed identities; evidences the delegation chain | Latency or performance cost of evidence at boundaries |
| Tool misuse | Strong | Evidences every tool call and its arguments; gates disallowed calls | A valid in-scope call that is ill-advised |
| Skill composition risk *(2026 research)* | Partial | Evidences the activated execution path and the context carried between invocations; path-aware authorization (C4.1.7–4.1.8) gates capability flow and trust transfer | The semantic safety of a composed path whose every step stays within authorized bounds |
| Unexpected code execution | Partial | Evidences code-execution calls and gates them by authorization | Malice within permitted execution, which needs sandboxing |
| Unsafe actuation | Partial | Gates and records actuation within a signed safety envelope | Whether a within-envelope action is safe, and whether the envelope was set correctly |
| Improper output handling | Partial | Evidences the output and where it flowed | Validating and sanitizing the output, which is the consuming system's job |
| Sensitive info / PHI exfiltration | Strong | Evidences data access and boundary crossings; gates unauthorized egress | Covert side-channel exfiltration; whether the privacy policy itself is adequate |
| Shadow / undeclared agents *(2026 research)* | Strong | Scope declaration reconciled against automated discovery (C10.1.8); undeclared deployments surface as recorded findings | Agents outside the organization's observability perimeter entirely |
| Autonomy creep | Strong | Evidences the signed autonomy envelope and every change; gates out-of-envelope actions | Quality degradation within the envelope |
| Rogue agents / behavioral drift | Partial | Produces the attributable evidence trail that makes drift detectable and provable after the fact | Detecting the misaligned pattern itself |
| Scope creep / lifecycle | Strong | Signed passport and change-control evidence; gates unreviewed changes | Whether the classification is correct |
| Trajectory-monitor parsing failure *(2026 research)* | Partial | Requires validators to be evaluated for structured-trace parsing competence (C10.3.7); validator results are themselves evidenced | The parsing competence of third-party trajectory-monitor products themselves |
| Audit tampering | Full | Records are tamper-evident, generated by the mechanism at execution, not operator-narrated | Insider compromise at the silicon layer, disclosed via trust assumptions |
| Cascading failures / fail-open | Partial | Evidences failure and deny events; at the top tier the system fails closed | Preventing propagation across a multi-agent system, which is architecture |
| Coverage decay / resilience | Strong | Continuous self-verification; an ongoing rather than point-in-time record | Discovering new attack classes, which is red-teaming |
| Human-agent trust exploitation / approval fatigue | Partial | Evidences the raw, true intent presented for approval and the approval decisions | The human fatigue and social engineering itself |
| Undisclosed AI / consent | Strong | Verifiable consent and disclosure record; gates on consent | Whether the disclosure content was adequate |
| Misinformation / hallucination | Not addressed | Nothing; correctness is out of scope | Whether the output is correct; correctness is a range, not a point |
| Hidden bias | Not addressed | Can preserve a tamper-evident record of verdicts for a separate review | Assessing or correcting fairness, which is validation |
| Unbounded consumption / DoS | Partial | Evidences consumption and calls; a budget or rate cap set as a boundary can gate | Availability defense, which is mostly infrastructure |
| Evidence repudiation | Full | Cryptographic evidence is openly verifiable and non-repudiable; the operator cannot deny an action occurred | Disputes about the meaning or significance of an action, only whether it occurred |
| Trust opacity | Strong | Trust-assumption disclosure makes residual trust visible and comparable | Eliminating all trust assumptions; the standard requires disclosure, not elimination |

Four rows read "not addressed" or record-only — system-prompt leakage, misinformation, hidden bias, and the semantic half of several others. Naming them is what keeps the standard credible: Proof-of-Control shows what happened, not whether it was right.

## References

* [MITRE ATLAS](https://atlas.mitre.org/) · [NIST AI 100-2](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) · [OWASP GenAI Security Project](https://genai.owasp.org/)
* SCR-Bench (Xie et al., 2026), TraceSafe-Bench (Chen et al., 2026), AI Trust OS (Bandara et al., 2026) — sources for the three research-driven threat rows ([research basis](../../docs/research-basis.md))
* Crosswalks: [MITRE ATLAS](../../mappings/mitre-atlas.md), [OWASP](../../mappings/owasp.md), [MAESTRO](../../mappings/maestro.md)
