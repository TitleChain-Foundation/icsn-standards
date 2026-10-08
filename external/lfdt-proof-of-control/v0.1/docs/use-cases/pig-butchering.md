---
industry: financial-services
use_case: Pig butchering scam — scammer-controlled agent operates on victim-provided credentials to drain accounts
business_impact: Irreversible account losses and platform liability for unauthorized agent execution
submission_type: scenario
claimed_tier: 4
threats:
  - identity-abuse
  - approval-fatigue
  - undisclosed-ai
  - trust-opacity
---
# Pig Butchering: Socially Engineered Credential Handoff Enabling Rogue Agent

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
A victim is socially engineered over weeks into trusting a fraudulent
"investment advisor" — the pattern known as pig butchering. The FBI's
Operation Level Up (2024) identified over 8,100 victims of such schemes,
with estimated losses exceeding $285M in the first year of the operation
alone. The victim voluntarily hands over account credentials. The scammer
deploys an agent that drains the account using those credentials. The
platform cannot distinguish this agent from the legitimate account holder's
own agent because credentials were provided willingly — there is no breach
signal to detect.

Reference: https://www.fbi.gov/how-we-can-help-you/victim-services/national-crimes-and-victim-resources/operation-level-up

## Claimed tier: Tier 4
The distinctive challenge here is that the credential transfer was voluntary.
Standard fraud signals (unusual login location, brute force patterns) are
absent. Only a cryptographic delegation chain rooted in the legitimate account
holder's verified identity can distinguish an authorized agent from a
scammer's agent operating on gifted credentials. This must be enforced at
execution — a scammer's agent presents no valid chain and cannot act.

Whether this use case actually reaches Tier 4 depends on two architectural
conditions, not just the presence of a delegation chain:

1. **Where the chain is rooted.** The root must be a verified identity bound
   to the legitimate account holder (e.g., identity-proofed at enrollment),
   not merely to whoever holds the account credentials. A chain rooted in
   credential possession inherits the same weakness as the credentials — a
   scammer who obtains credentials could mint a valid-looking chain.

2. **How the signing keys are held.** If the account holder's delegation
   signing key is held client-side (device-bound, hardware-backed, or
   biometrically gated on the holder's own device), a scammer with
   credentials cannot issue delegations. If the key is held or escrowed by
   the platform and exercised on the user's behalf after login, the
   delegation gate collapses back into the authentication gate — and the
   use case degrades to Tier 2, since trust returns to the operator.

Tier 4 holds only when both conditions are met: identity-proofed root,
non-exportable holder-controlled keys, and fail-closed execution.

## Why not one tier down?
At Tier 3, independent verification confirms after the fact that the agent
lacked a valid delegation chain from the legitimate account holder. But the
account is already drained. Pig butchering victims often do not discover the
fraud until withdrawal is blocked or the scammer disappears — by then the
harm is irreversible. Tier 4's fail-closed enforcement prevents execution
entirely: no valid chain, no action.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 4    | Agent must be provably traceable to a delegation chain rooted in the legitimate account holder, not just the credential holder |
| Privacy       | 2    | Standard financial privacy controls apply; the risk domain here is authorization, not data exposure |
| Portability   | 1    | Not a primary risk domain for this use case |
| Authorization | 4    | Voluntary credential sharing must not confer agent authorization; delegation must be cryptographically separate from authentication |
| Identity      | 4    | The legitimate account holder's identity must be cryptographically bound to any agent authorized to act on their behalf |
| Security      | 4    | Execution must be gated; detection after voluntary credential transfer is insufficient |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `identity-abuse` | The scammer's agent acts under the victim's account, holding credentials that were handed over rather than stolen, and no delegation the account holder ever issued |
| `approval-fatigue` | Weeks of cultivated trust are the attack. Where a delegation ceremony exists, the victim is walked through it by someone they believe is advising them |
| `undisclosed-ai` | The victim consents to an "investment advisor" and not to an autonomous agent draining the account; what acts is never disclosed for what it is |
| `trust-opacity` | The Tier 4 claim stands or falls on where the chain is rooted and who holds the signing key, neither of which a victim or a regulator can see unless disclosed |

## What Proof-of-Control does not verify here
- **The persuasion.** This is a social attack and the manipulation is entirely
  out of scope. Proof-of-Control does not detect grooming, assess a
  relationship, or judge whether a person is being deceived at the moment they
  act.
- **A delegation the victim was talked into issuing.** If the scammer walks the
  victim through the ceremony from their own device and keys, the resulting
  chain is cryptographically valid and the agent acts in bounds. Verification
  covers control, not the quality of the judgement behind a grant. Conformance
  here must not be read as anti-fraud certification.
- **Whether the disclosure or the warning worked.** The claim gates on consent
  and records it. It does not establish that the victim understood what they
  authorized, or that a cooling-off prompt was noticed.
- **Whether a cap or scope was set sensibly.** A grant capped too high is still
  a grant, and an agent spending inside it produces no violation.
- **Recovery of funds.** Fail-closed enforcement prevents an unauthorized agent
  from executing. Where a valid delegation existed, the transfers settle and
  nothing in this claim reverses them.
- **Residual trust is disclosed, not eliminated.** Tier 4 narrows the blast
  radius of successful manipulation. It does not remove the manipulation, and
  it does not remove the parties a reader still has to trust.

## Residual trust assumptions to disclose
- **Root of credential issuance.** That the delegation chain is rooted in an
  identity-proofed account holder rather than in whoever holds the account
  credentials, and the assurance level of that proofing. A chain rooted in
  credential possession lets a scammer with gifted credentials mint a
  valid-looking delegation, and the claim degrades to Tier 2.
- **Key custody.** That the signing key is client-side, device-bound,
  hardware-backed or biometrically gated on the holder's own device, and
  non-exportable. Platform-held or escrowed keys exercised on the user's behalf
  after login collapse the delegation gate back into the authentication gate.
  This is the single disclosure that decides whether the claim means anything.
- **Attestation chain.** Version, freshness window and revocation policy, and
  how fast a delegation is revoked once a victim reports the fraud. Pig
  butchering victims often discover the fraud late, so the practical exposure
  is measured in that lag, not in the revocation mechanism.
- **Transparency log monitors.** Who monitors the log, and what happens if the
  monitor set lapses, given that the absence of a valid delegation is the
  evidence distinguishing a scammer's agent from the holder's own.
- **Device and machine binding.** Any point where the attestation of the
  holder's device and the attestation of the signing environment are assumed to
  describe the same machine, including a device the scammer has been granted
  remote access to.
- **The intervention layer.** Warnings, cooling-off periods and scoped or
  capped grants are what convert higher friction into fewer losses. They are
  policy choices sitting outside the cryptography, and a reader is trusting the
  platform to have made them well.

## Notes / open questions
- This use case exposes a foundational gap: most financial platforms treat
  authentication (proving you have the credentials) as equivalent to
  authorization (proving you are the legitimate account holder authorizing
  an agent). Proof of Control separates these.
- The voluntary nature of the credential transfer makes behavioral anomaly
  detection largely ineffective, which is why this is a strong Tier 4 case.
- Tier 4 here is conditional on key custody architecture. Platform-held or
  escrowed delegation keys reduce this to Tier 2 regardless of chain
  cryptography. The standard should require key custody disclosure as part
  of the Transparent property for this class of use case.
- This is fundamentally a social attack, which makes it one of the hardest
  cases in the set. The humans are part of the system, and legitimate intent
  is genuinely present: the victim *wants* to give the scammer access at the
  moment they do it. No verification tier can prevent a persuaded account
  holder from being persuaded. What Tier 4 changes is the mechanics of what
  persuasion can yield. Handing over credentials no longer hands over agent
  authority — the scammer must instead get the victim to actively issue a
  delegation from their own verified identity and holder-controlled keys.
  That is a higher-friction, more explicit act ("authorize this agent to
  move funds") that creates a natural intervention point for warnings,
  cooling-off periods, and scoped/capped grants. PoC narrows the blast
  radius of successful manipulation; it does not eliminate manipulation.
- Boundary for the working group: if the scammer socially engineers the
  victim through the delegation ceremony itself, the resulting chain is
  cryptographically valid. The standard verifies control, not the quality
  of the human judgment behind a grant — worth stating explicitly so PoC
  conformance is not misread as anti-fraud certification.
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
