# M5POD Member Activation Architecture

> **Status: Public Review Draft / non-normative M5 implementation reference.**
>
> This document does not change an adopted ICSN standard or represent that the described activation workflow is deployed.

## Purpose

Define the journey from public Foundation entry through controlled activation into a member-controlled M5POD without collapsing preview, waitlist, application, identity, membership, pairing or operational states.

## Actors

- **Visitor** — reviews public information.
- **Prospective member** — may save a place using approved minimum information.
- **Applicant** — enters the controlled application/cohort workflow.
- **IAM holder** — has completed the applicable IAM activation state.
- **M5Member** — admitted under the applicable member process.
- **M5POD holder** — M5Member with an activated and paired M5POD.
- **Native M5Agent** — canonically defined M5 agent acting only under bounded authority.
- **External model/service** — replaceable computational/service provider.
- **Foundation** — public commons / standards / program entry role.
- **Accountable operator** — operator responsible for a defined activation function.

## State model

`SCAN_ONLY` → `PLACE_SAVED` → `APPLICATION_STARTED` → `APPLICATION_SUBMITTED` → `APPROVED` → `IAM_IN_PROGRESS` → `IAM_ACTIVATED` → `M5POD_PAIRING` → `M5POD_ACTIVATED` → `VERIFIED_OPERATIONAL`

Independent lifecycle states:
`SUSPENDED`, `REVOKED`, `WITHDRAWN`, `DELETED`, `RECOVERY_IN_PROGRESS`, `RECOVERED`.

State transitions require an accountable operator, current policy, an auditable event, and any required human approval. Recovery restores only the state and authority that remain valid; it does not silently restore revoked rights or expired grants.

## State boundaries

A saved place, email address, phone number, state/jurisdiction selection, walkthrough completion or ordinary website session is not IAM activation.

Foundation participation, M5Bank membership, IAM activation, M5POD pairing, device binding, communications access, account-context activation and passport/capability evidence are separate.

## Public preview

`titlechainfoundation.org` → public information → `m5podactivationdemo.netlify.app` → scan-only walkthrough → later controlled application/cohort workflow.

The walkthrough must not imply activation of a member account, IAM credential, M5POD, wallet, passport or cohort place merely because the user viewed or completed the demo.

## System context and diagrams

The [Sovereign M5POD system diagram](../architecture/rendered/m5-sovereign-stack.svg) shows the commons, human-authority root, private M5POD, semantic-intelligence, network, storage, platform, and legal/governance boundaries. Its maintained source is [`architecture/m5-sovereign-stack.mmd`](../architecture/m5-sovereign-stack.mmd), with [PNG](../architecture/rendered/m5-sovereign-stack.png), [PDF](../architecture/rendered/m5-sovereign-stack.pdf), and an [accessible description](../architecture/M5POD-MEMBER-ACTIVATION-ALT-TEXT.md).

The state model above is the focused activation journey. It is intentionally documented as reviewable text rather than represented as a second diagram that could be mistaken for the sovereign system architecture.

## Accountable boundaries

| Boundary | Responsible function | Public evidence | Must remain private |
| --- | --- | --- | --- |
| Public explanation and preview | Foundation communications and program entry | Current public pages, status language, aggregate availability | Contact details beyond approved minimum data |
| Application and approval | Authorized cohort or membership operator | Process version, decision status, appeal/correction route | Application contents and identity evidence |
| IAM activation | Authorized identity/credential operator | Privacy-filtered status and policy version | Identity documents, biometrics, recovery secrets |
| Device binding and M5POD pairing | Authorized technical operator under member approval | Device class, attestation status, privacy-filtered receipt | Device identifiers, keys, M5POD contents |
| Operational use | Member and specifically authorized delegates | Selectively disclosed capability or provenance evidence | Private data, prompts, agent memory, wallet and communication contents |

## Data classes

- Public
- Minimum contact
- Private identity
- Private M5POD
- Credential
- Recovery
- Restricted operational
- Public provenance evidence

Private member data, credentials, wallet addresses, device identifiers, recovery material, M5POD contents and controlled data-room materials must not be placed in the public repository.

## Human authority

Agents cannot acquire external authority merely because the human has authenticated.

Consequential actions require current authority under M5Canon and any required fresh human approval.

Identity proof, membership, device possession, agent provenance, or successful authentication does not by itself authorize data access, disclosure, signing, payment, transfer, credential issuance, or title change.

## Rights and lifecycle controls

Support private draft, affirmative approval, correction, export, selective disclosure, withdrawal, suspension, revocation, deletion and recovery.

See the [Activation, Consent, Semantic and Authorization Map](M5-ACTIVATION-CONSENT-AUTHORIZATION-MAP.md) for the proposed cross-issue mapping to #45 and #46. Consent and authorization review remain incomplete until qualified reviewers record findings and conformance evidence.
