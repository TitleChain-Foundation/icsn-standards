---
industry: financial-services
use_case: Deepfake video or biometric used to pass liveness checks and authorize agent access
business_impact: High-value fraudulent transfers with no recoverable authorization trail
submission_type: scenario
claimed_tier: 3
threats:
  - identity-abuse
  - approval-fatigue
  - evidence-repudiation
---
# Deepfake Biometric Bypass Authorizing Agent Financial Transfers

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
In January 2024, a finance worker at engineering firm Arup was deceived by
AI-generated deepfakes of his CFO and colleagues on a video call, transferring
$25.6M across 15 transactions before discovering the fraud. As biometric
liveness checks expand to agent authentication flows, the same technique
applies: a deepfaked biometric session passes the liveness check, the platform
issues an authorization token, and an agent executes consequential actions
under that token. The biometric check verified an image, not a legitimate
principal's intent.

Reference: https://www.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk

## Claimed tier: Tier 3
Biometric authentication proves that a face passed a liveness check — it does
not prove that the legitimate account holder authorized a specific agent to
act. Tier 3 is required because in the aftermath of a deepfake incident, the
institution, the account holder, and investigators must be able to
independently verify whether a legitimate delegation existed for the disputed
transfers — without relying on the platform's own session logs, which show
only that authentication "succeeded." A spoofed biometric session produces a
passed liveness check but no independently verifiable delegation record; that
absence is itself the evidence that distinguishes fraud from authorized
activity, and it must be checkable by any party without privileged access.

## Why not one tier down?
At Tier 2, an auditor with privileged access can review the platform's
authentication and session logs — but those logs show a successful biometric
check and a valid-looking authorization token. The deepfake produced exactly
the records a legitimate session would produce. Operator-held logs therefore
cannot distinguish the fraud, and in a dispute the account holder is left
contesting the platform's own records. Tier 3 closes this by making the
delegation record independently verifiable and cryptographically separate
from the authentication event: anyone can check whether a valid delegation
rooted in the legitimate principal existed for those transfers, without the
platform's cooperation.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 3    | Whether a transfer was rooted in a legitimate principal's delegation must be independently verifiable, not inferred from session logs |
| Privacy       | 2    | Standard financial privacy controls apply |
| Portability   | 1    | Not a primary risk domain for this use case |
| Authorization | 3    | The delegation record must be cryptographically separate from the spoofable authentication event and checkable by any party in a dispute |
| Identity      | 3    | The binding between the legitimate account holder and any authorized agent must be independently verifiable, not dependent on biometric liveness |
| Security      | 2    | Liveness detection and session security remain necessary controls, but third-party assessment of those controls is sufficient |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `identity-abuse` | A synthetic face passes the liveness check, and the token issued on the strength of it lets an agent act as a principal who authorized nothing |
| `approval-fatigue` | The Arup pattern: a finance worker is walked through approvals by what appears to be his CFO and colleagues, so human oversight is present and defeated |
| `evidence-repudiation` | After the transfers, the account holder and the institution have only the platform's own session logs, which record a successful check either way |

## What Proof-of-Control does not verify here
- **Whether the biometric was real.** Liveness and presentation-attack
  detection are the deployment's problem and remain necessary. Proof-of-Control
  does not inspect the video, score the artefact, or tell a genuine face from a
  generated one. It relocates the question so that passing the check is no
  longer sufficient to move money.
- **The social engineering itself.** The deception on the call, the pressure
  applied to the finance worker, and the human trust it exploited are all out
  of scope. Proof-of-Control evidences the intent that was presented for
  approval and the approval decisions taken; it does not judge why a person
  approved.
- **Whether an approval was well-judged.** A delegation issued by the genuine
  account holder under manipulation is cryptographically valid. Verification
  covers control, not the quality of the judgement behind a grant.
- **What a disputed action meant.** Proof-of-Control settles whether a
  delegation existed for the transfers and who it was rooted in. Arguments
  about the significance of an action, or about liability for it, sit outside
  the record.
- **Recovery.** At Tier 3 the record is verifiable after the fact. The funds
  have still moved, and nothing in this claim reverses a settled transfer.

## Residual trust assumptions to disclose
- **Root of credential issuance.** The identity-proofing performed at account
  enrollment, and its assurance level. The delegation record is only as
  meaningful as the enrollment it is rooted in, and enrollment here is
  typically the same biometric pipeline the attack targets.
- **Separation of the delegation key from the biometric session.** That the
  signing key is held by the account holder on their own device and is not
  released, escrowed or exercised by the platform on the strength of a passed
  liveness check. If a passed check mints the delegation, the two events are
  not separate and the claim degrades.
- **Attestation chain.** Its version, freshness window and revocation policy,
  including how quickly a delegation is revoked once fraud is reported and what
  the window before revocation permits.
- **Transparency log monitors.** Who watches the log that makes the absence of
  a delegation checkable, and what an evaluator should conclude if the monitor
  set lapses. Absence of a record is the load-bearing evidence in this
  scenario, so an unmonitored log undermines the central argument.
- **Device and machine binding.** Any point where the attestation of the
  holder's device and the attestation of the signing environment are assumed to
  describe the same machine.
- **Hardware roots.** Where TEE-bound or secure-element keys are relied on, the
  reader is trusting the silicon vendor's attestation root and its revocation
  practice.

## Notes / open questions
- This use case makes the strongest case for separating authentication
  (who you appear to be) from authorization (what you have delegated an
  agent to do). These are architecturally separate problems that current
  platforms often conflate.
- Reasonable to argue Tier 4 for high-value transfer thresholds, where
  post-facto verification is too late and execution should be mechanically
  gated on a valid delegation credential — the Arup pattern ($25.6M across
  15 transactions in one session) is the argument for that stricter stance.
  As with the pig-butchering case, a Tier 4 claim would additionally depend
  on where the delegation chain is rooted and how the signing keys are held.
- Open question: does hardware-attested identity (TEE-bound keys) satisfy
  the delegation requirement, or is a separate cryptographic delegation
  layer always required?
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
