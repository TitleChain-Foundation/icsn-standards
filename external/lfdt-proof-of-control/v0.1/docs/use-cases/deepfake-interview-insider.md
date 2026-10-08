---
industry: technology
use_case: Threat actor uses deepfake identity to pass hiring process and gain insider system access
business_impact: Persistent agent-level insider access that survives human threat actor detection
submission_type: scenario
claimed_tier: 4
threats:
  - identity-abuse
  - excessive-agency
  - scope-creep-lifecycle
  - trust-opacity
---
# Nation-State Actor Uses Deepfake to Gain Insider Agent Access

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
In July 2024, KnowBe4 unknowingly hired a North Korean operative who used
an AI-generated identity to pass four video interviews and background checks.
Upon receiving a company laptop, the operative immediately attempted to install
malware. In an agentic environment, the same vector produces a worse outcome:
once hired, the operative is a legitimate employee record in the HR system
and identity provider, and the platform does not gate what a credentialed
employee is permitted to do — provisioning agents is within the normal
authority their role confers. The threat actor provisions and delegates to
internal AI agents whose authority derives from that employee record,
embedding persistent access into automated workflows that survive the
operative's own detection and termination. The registration authority the
agents chain back to — the employer's own HR and identity systems — is
exactly the system the fraudulent identity has already defeated.

Reference: https://blog.knowbe4.com/how-a-north-korean-fake-it-worker-tried-to-infiltrate-us

## Claimed tier: Tier 4
Employment onboarding must not automatically confer agent authorization.
The structural problem is where the root of trust sits: if the delegation
chain is rooted in the employee record, then the employer — whose hiring
and identity-proofing process has already been defeated — is vouching for
itself. That is a Tier 2 root of trust at best, and in this scenario it is
a compromised one. Tier 4 requires that the trust anchor sit outside the
employment record entirely: agent provisioning must chain to an
independently verified organizational identity (identity-proofed
enrollment, holder-controlled keys, an anchor external to the HR/IdP
stack), and enforcement must be fail-closed — an agent whose chain roots
only in employment status cannot execute. A threat actor who defeats the
hiring process gains an employee record, but no valid root, and therefore
no agents.

## Why not one tier down?
At Tier 3, an investigation can independently verify that an agent was
provisioned by a threat actor using a fraudulent identity — after malware
is deployed or data is exfiltrated. The KnowBe4 incident was discovered
within 25 minutes of the laptop being powered on; in an agentic workflow,
agents provisioned before detection continue operating after the human
threat actor is locked out. And because the employee record is the very
artifact the fraud produced, independent verification that chains back to
that record verifies nothing — it confirms a fraudulent registration as
valid. Tier 4 closes both gaps: the root of trust is anchored outside the
defeated registration system, and agents cannot be provisioned or operated
without a chain to that external anchor.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 4    | Agent provisioning must be cryptographically traceable to a trust anchor outside the employer's HR/IdP stack, not to employment records the fraud produced |
| Privacy       | 2    | Standard data access controls apply; the risk domain here is agent provisioning, not data exposure |
| Portability   | 1    | Not a primary risk domain for this use case |
| Authorization | 4    | Employment must not confer agent authorization; delegation must chain to independently verified identity and be enforced at execution |
| Identity      | 4    | The identity of anyone provisioning agents must be verified against a root of trust external to the registration system the deepfake defeated |
| Security      | 4    | Agent provisioning must be fail-closed; a fraudulently onboarded employee must be unable to provision persistent agents |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `identity-abuse` | A fraudulent identity passes hiring and becomes an employee record, so every agent chaining to that record claims an authority the organization never knowingly granted |
| `excessive-agency` | Provisioning agents falls inside the normal authority the role confers, so the operative gets agent-creation rights nobody decided to give them |
| `scope-creep-lifecycle` | Agent provisioning happens as an implicit consequence of role assignment, with no change-control step and no review of what is being created |
| `trust-opacity` | The claim's strength depends entirely on where the trust anchor sits, which is invisible to a reader unless the deployment states it |

## What Proof-of-Control does not verify here
- **Whether the hiring process was defeated.** Proof-of-Control does not
  identity-proof job applicants, detect a generated face across four video
  interviews, or validate a background check. It assumes the registration
  system can fail and asks that agent authority not depend on it.
- **Whether the external anchor is itself sound.** Moving the root of trust
  outside the HR and identity-provider stack removes the circularity. It
  replaces it with a different party to trust, whose enrollment practice is not
  something the evidence can attest to.
- **Whether the role's grant was appropriate.** Once provisioning rights are
  inside a role, an agent created under them is in bounds. Proof-of-Control
  evidences the authority exercised, not whether the role should have carried
  it.
- **Whether a change was classified correctly.** Change-control evidence shows
  that a provisioning event was reviewed and by whom. It does not judge whether
  the reviewer understood the risk or graded it right.
- **The malware, and anything inside a permitted envelope.** An operative
  acting through agents that hold a valid chain, doing things those agents are
  permitted to do, produces clean evidence. This claim narrows what a
  fraudulent hire can reach; it does not make them harmless.
- **Residual trust is disclosed, not removed.** Tier 4 makes the anchor's
  location nameable and comparable. It does not eliminate the need to trust it.

## Residual trust assumptions to disclose
- **Root of credential issuance, and its independence.** Which organizational
  identity authority anchors agent provisioning, and the demonstration that it
  is genuinely external to the HR and identity-provider stack being protected.
  A chain that terminates in the employee record inherits the integrity of the
  hiring process and is worth no more than it.
- **Enrollment assurance at that anchor.** How the organization itself was
  identity-proofed to the external authority, and by whom.
- **Key custody for provisioning authority.** That the keys authorizing agent
  creation are holder-controlled and non-exportable, and are not reissued
  automatically on the strength of an employment record.
- **Attestation chain.** Version, freshness window and revocation policy, and
  specifically the propagation time between an employee's termination and the
  revocation of every agent chained to them. Agents that outlive the human are
  the whole point of this scenario, so that interval is the exposure.
- **Transparency log monitors.** Who monitors the provisioning log, and what
  happens if the monitor set lapses. A provisioning event that nobody observes
  is functionally unreviewed.
- **Machine identity linkage.** Any point where an attestation of the agent
  runtime and an attestation of the host it runs on are assumed to describe the
  same machine, including agents that persist across host replacement.

## Notes / open questions
- The root-of-trust placement is the crux: a delegation chain rooted in the
  employee record inherits the integrity of the hiring process, which is the
  attack surface in this scenario. The standard should require that Tier 4
  claims for provisioning authority disclose where the trust anchor sits and
  demonstrate it is independent of the registration system being protected.
- Related: agent provisioning rights should themselves be treated as a
  delegatable permission requiring Tier 4 verification, not an implicit
  consequence of role assignment.
- The KnowBe4 case is the best-documented public incident for this pattern;
  the agentic extension is currently hypothetical but architecturally
  straightforward.
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
