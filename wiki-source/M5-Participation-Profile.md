# M5 Participation Profile

> **Publication status:** Adopted Version 1.0  
> **Adopted by:** TitleChain Foundation authorized governance body  
> **Effective date:** 2026-08-28  
> **Last reviewed:** 2026-08-28  
> **Next scheduled review:** 2027-08-28  
> **Legal review:** Approved for publication by authorized counsel on 2026-08-28.

## 1. Purpose

This profile defines baseline eligibility, identity, wallet, credential, authority, notice, and accountability requirements for persons, organizations, agencies, workers, agents, applications, devices, and services operating within a designated M5 participation environment.

Its purpose is to establish attributable, revocable, privacy-aware, and auditable participation. It is an implementation-specific participation profile, not a requirement that all ICSN implementations use M5 accounts or wallets.

## 2. Participation eligibility

No person, organization, agency, worker, agent, application, device, service, wallet, or external signing endpoint is eligible to operate in a designated M5 participation environment unless the applicable participant has:

1. An active M5Member account or active registered M5 Agency or Organization account
2. An active M5Wallet registered to, controlled by, or properly delegated by the applicable M5Member, agency, or organization
3. Current credentials, verification status, and permissions required for the requested activity
4. An active, authenticated, and monitored M5Member Notice Channel
5. No unresolved suspension, revocation, restriction, legal hold, security restriction, or other status that prohibits the activity
6. Accepted the applicable terms, policies, and disclosures required for that participation category

Eligibility is activity-specific. Eligibility for one activity does not automatically authorize another activity.

## 3. M5Member account

An M5Member account is the accountable participation relationship for an eligible individual or authorized organizational representative.

It MUST be associated with:

- A unique participant identifier
- Current credential status
- Approved authentication method or methods
- An M5Wallet relationship
- An M5Member Notice Channel
- Applicable recovery and security controls
- Accepted terms, policies, and required disclosures

An M5Member account does not by itself establish legal identity, legal agency, legal authority, citizenship, residency, creditworthiness, financial-institution status, ownership, beneficial ownership, or regulatory eligibility.

## 4. M5Wallet requirement

An active credentialed M5Wallet is required for participation in the designated M5 environment. An M5Wallet serves as a technical authority and accountability anchor for authorized activities, subject to the applicable scope, credential status, policy, and verification requirements.

An M5Wallet may support:

- Authentication and account binding
- Credential holding and presentation
- Signing and authorization
- Controlled association with external wallets or supported signing endpoints
- Agent authorization and revocation
- Asset, title, record, or transaction authority references
- Notices, receipts, audit events, and status records
- Recovery and continuity controls

An M5Wallet MUST NOT be represented as proof, by itself, of legal ownership, beneficial ownership, legal title, custody, authority to transfer, payment finality, regulatory compliance, or the truth of an underlying claim.

## 5. M5POD and M5Vault

An eligible M5Member may maintain an M5POD and M5Vault for member-controlled records, credentials, keys, recovery materials, permissions, communications, and supported digital-asset relationships.

Sensitive information SHOULD remain in the M5POD, M5Vault, or another authorized controlled repository. Public or broadly replicated systems SHOULD contain only the minimum information necessary for integrity, status, authorization, provenance, discovery, or verification.

## 6. External wallets and cold storage

An eligible M5Member may register or associate a supported external wallet, cold-storage wallet, hardware wallet, Bitkey, multisignature arrangement, custody account, or other supported signing endpoint with the member’s M5Wallet, M5POD, or M5Vault.

Registration requires an approved proof-of-control or relationship-verification method appropriate to the asset type and risk level. Methods may include:

- A cryptographic signature
- Supported device attestation
- Verified custodian confirmation
- Multi-party authorization
- Another approved method appropriate to the relationship and risk level

Registration establishes only the verified relationship stated in the record, such as technical control, declared ownership, delegated authority, custody relationship, or authorized use.

Private keys, seed phrases, recovery secrets, or equivalent authentication secrets MUST NOT be submitted to, stored in, or requested by an M5 participation environment except through an expressly approved, secure, separately governed custody or recovery process.

## 7. M5 Agents

An M5 Agent is a digital agent, automated workflow, software process, or authorized service acting through an M5 participation environment.

Every M5 Agent MUST be associated with:

- A responsible active M5Member or registered M5 Agency or Organization
- An active M5Wallet relationship
- A unique agent identifier
- Defined authority scope
- Effective start time and expiration or review condition
- Current status and revocation method
- Applicable policies and risk controls
- A defined audit and receipt policy

The Responsible Sponsor is accountable for sponsoring, configuring, supervising, reviewing, and revoking its M5 Agents, subject to applicable law, contract, platform policy, technical controls, and the actions of other responsible parties.

An M5 Agent MUST NOT:

- Act outside its authorized scope
- Use authority after expiration, suspension, or revocation
- Re-delegate authority unless expressly authorized
- Misrepresent itself as a human or legally authorized representative
- Circumvent required confirmation, authentication, policy, fraud, compliance, or audit controls

## 8. Agency and organization participation

An agency, business, cooperative, institution, public body, nonprofit, professional practice, service provider, or other organization is eligible only if registered as an active M5 Agency or Organization and if it maintains required credentials, wallet relationships, authorized-representative records, Notice Channel, and policy status.

The organization MUST maintain current records of authorized officers, administrators, workers, contractors, and M5 Agents.

Organization registration does not automatically authorize every employee, contractor, affiliate, officer, owner, consultant, or agent. Each acting person or M5 Agent MUST have the applicable current role, credential, wallet association, delegation, scope, and status.

## 9. M5Member Notice Channel

Each eligible M5Member and registered M5 Agency or Organization MUST maintain at least one active M5Member Notice Channel.

It is an authenticated, durable communication pathway for service notices, security alerts, authority changes, credential-status events, recovery events, policy notices, and other designated communications.

The Notice Channel may include:

- Secure direct message
- In-platform inbox
- Verified email
- Verified mobile channel
- Secure portal
- Physical mailing address
- Another approved method

A notice is not presumed legally effective merely because it was sent through an M5Member Notice Channel. Legal effectiveness, service of process, delivery, consent, receipt, and evidentiary treatment depend on applicable law, contract, jurisdiction, notice type, delivery method, and requirements of the sending authority.

## 10. Suspension, revocation, and ineligibility

The operator of a designated M5 participation environment may suspend, restrict, revoke, or terminate participation eligibility in accordance with applicable terms, policy, law, security requirements, fraud controls, legal process, sanctions requirements, or risk-management procedures.

Any action should be scoped, documented, and communicated to the extent lawful and appropriate.

## Related policies

- [Home](Home)
- [What Is M5Bank?](What-Is-M5Bank)
- [Human-First Technology and Due Process](Human-First-Technology-and-Due-Process)
- [M5 Participation Profile](M5-Participation-Profile)
- [Foundation and ICSN Non-Custody and Data Non-Access Policy](Foundation-and-ICSN-Non-Custody-and-Data-Non-Access-Policy)
- [M5 Due Notice and Credentialed Authority Policy](M5-Due-Notice-and-Credentialed-Authority-Policy)
- [M5 Credential Trust and Issuer Registry](M5-Credential-Trust-and-Issuer-Registry)
- [M4-M5 Registered Service Provider Pathway](M4-M5-Registered-Service-Provider-Pathway)
- [ICSN-0014: Universal Value and Digital-Asset Classification](ICSN-0014-Universal-Value-and-Digital-Asset-Classification)
