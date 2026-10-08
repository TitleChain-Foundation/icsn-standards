---
industry: cloud-services
use_case: AI agent authenticates and acts using stolen user credentials
business_impact: Mass data exfiltration and regulatory breach liability
submission_type: scenario
claimed_tier: 4
threats:
  - identity-abuse
  - excessive-agency
  - data-exfiltration
  - trust-opacity
---
# Account Takeover Agent Operating on Stolen Credentials

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario
Following a credential breach — as occurred across 165+ enterprise
organizations in the 2024 Snowflake campaign — an attacker uses stolen
usernames and passwords to authenticate an AI agent into a cloud environment.
Because the platform treats valid credentials as sufficient proof of identity,
the agent operates with the legitimate user's full permissions. By the time
anomalous activity is detected, data has already been exfiltrated. No
cryptographic delegation chain exists to distinguish the attacker's agent
from the legitimate user's agent.

Reference: https://www.cybersecuritydive.com/news/100-snowflake-customers-attacked/718454/

## Claimed tier: Tier 4
Credential theft demonstrates that authentication alone cannot be the
authorization gate. Tier 4 is required because the failure mode is not
detectable in time to prevent harm — exfiltration completes before anomaly
detection fires. The system must be fail-closed: an agent with no valid
delegation chain rooted in the legitimate account holder must be unable to
execute, not merely flagged after the fact.

Whether this reaches Tier 4 in practice depends on where the chain is rooted
and how the keys are held. The delegation root must be an identity-proofed
account holder, and the delegation signing key must be holder-controlled
(device-bound, hardware-backed, non-exportable). If the platform holds or
escrows the delegation key and exercises it on the user's behalf after
login, stolen credentials yield valid delegations — the delegation gate
collapses back into the authentication gate, and the claim degrades to
Tier 2.

## Why not one tier down?
At Tier 3, the unauthorized access is independently verifiable after the
fact — auditors can confirm the agent used stolen credentials. But
verification after exfiltration does not undo the breach. The 2024 Snowflake
incidents show that weeks can pass between initial compromise and detection.
Tier 4 closes this by making execution mechanically impossible without a
valid, cryptographically-rooted delegation credential. Stolen passwords
produce no valid chain; the agent cannot act.

## Tier by domain
| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 4    | Must be impossible — not just detectable — for an agent to act without a verifiable delegation chain rooted in the legitimate principal |
| Privacy       | 3    | Data access patterns must be independently auditable to support breach investigation and regulatory response |
| Portability   | 1    | Not a primary risk domain for this use case |
| Authorization | 4    | Credential possession must not be sufficient for authorization; cryptographic delegation must be required for execution |
| Identity      | 4    | Identity of agent and its human principal must be cryptographically bound; stolen credentials confer no agent authority |
| Security      | 4    | Security controls must be fail-closed; no execution without valid chain, regardless of authentication state |

## Threats exercised
| Threat | What it looks like here |
|---|---|
| `identity-abuse` | An attacker authenticates an agent with stolen passwords, so the agent acts under a principal that never delegated to it |
| `excessive-agency` | The agent inherits the compromised account's full permission set rather than the narrow scope any one task needs |
| `data-exfiltration` | Customer records leave the cloud environment in bulk during the window before anomaly detection fires |
| `trust-opacity` | Whether the Tier 4 claim holds turns on key custody, which a relying party cannot see unless it is disclosed |

## What Proof-of-Control does not verify here
- **The credential theft itself.** Proof-of-Control binds execution to a
  delegation chain; it does nothing to stop passwords being phished, reused or
  bought. Social engineering at the human level stays out of scope, and this
  scenario begins after the credentials are already lost.
- **Whether the legitimate grant was the right size.** If the account holder's
  own delegation is broader than the task needs, an agent acting inside it
  produces no violation. Proof-of-Control evidences what authority was
  exercised, not whether granting it was wise.
- **Covert exfiltration paths.** Gating covers the egress channels the
  deployment mediates. Side channels, out-of-band copies taken from a
  compromised host, and data encoded into otherwise permitted traffic are not
  covered. Nor does Proof-of-Control assess whether the policy defining
  "protected" is adequate in the first place.
- **That the SSO or identity provider issuing the human session is sound.** The
  gate verifies a delegation chain. It does not audit the federation that
  produced the login the chain is anchored beside.
- **Residual trust is disclosed, not eliminated.** Tier 4 makes the remaining
  trust nameable and comparable. It does not make the deployment trust-free.

## Residual trust assumptions to disclose
- **Root of credential issuance.** Who identity-proofed the account holder at
  enrollment, and to what assurance level. Every claim below inherits the
  integrity of that enrollment, and a delegation chain rooted in credential
  possession rather than a proofed identity collapses back to Tier 2.
- **Key custody.** That the delegation signing key is holder-controlled,
  device-bound, hardware-backed and non-exportable. A reader trusts both the
  attestation asserting this and the secure-element vendor behind it. Platform
  escrow of that key voids the claim.
- **Attestation chain.** Its version, freshness window and revocation policy. A
  stale or unrevoked attestation is indistinguishable from a current one to a
  verifier that does not check both.
- **Transparency log monitors.** Who monitors the log, and what happens if the
  monitor set lapses. An unwatched log can equivocate without detection.
- **Machine identity linkage.** Any point where the attestation of the agent
  runtime and the attestation of its host are assumed to describe the same
  machine, since nothing in the evidence itself proves that pairing.
- **Federation boundaries.** Any place a federated assertion is accepted in
  place of a delegation, which reintroduces exactly the
  authentication-as-authorization collapse this use case exists to name.

## Notes / open questions
- This use case is the clearest argument for Tier 4 in the enterprise space.
  The Snowflake precedent is well-documented and the harm pattern
  (detection lag, exfiltration volume) is established.
- Tier 4 here is conditional on key custody architecture. Platform-held or
  escrowed delegation keys reduce this to Tier 2 regardless of chain
  cryptography. The standard should require key custody disclosure as part
  of the Transparent property for this class of use case.
- Open question: how does a Tier 4 delegation chain interact with SSO and
  federated identity systems that currently treat authentication as
  authorization? This is an architectural gap the standard should address.
- Submitted to AAI-Society/openverification as [pull request #5](https://github.com/AAI-Society/openverification/pull/5) by GitHub @rosalyncurato, one of eight scenarios drawn from conversations with CISOs, fraud leaders and business leaders, brought to the v2 template by GitHub @H0BB5, and ported here when the use-case corpus moved into this repository, with the domain rows put in the canonical order and nothing else changed.
