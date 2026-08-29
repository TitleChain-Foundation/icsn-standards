# M5 Credential Trust and Issuer Registry

> **Publication status:** Adopted Version 1.0  
> **Adopted by:** TitleChain Foundation authorized governance body  
> **Effective date:** 2026-08-28  
> **Last reviewed:** 2026-08-28  
> **Next scheduled review:** 2027-08-28  
> **Legal review:** Approved for publication by authorized counsel on 2026-08-28.

## 1. Purpose and limits

The M5 Credential Trust and Issuer Registry defines a technical and governance process for evaluating credentials used to establish participant identity, organization status, agency authority, professional role, public-office role, court authority, tribal authority, asset-related authority, and other authorized participation roles.

Credential verification does not equal unlimited authority. A credential may establish that a subject holds a stated role or status; it does not authorize every action associated with that role.

## 2. Required authority evaluation

Each requested action MUST be evaluated against:

- The issuer
- Credential status
- Credential subject
- Credential scope
- Asserted jurisdiction
- Requested action
- Applicable law or contract
- Affected relationship
- Relevant security, privacy, and risk requirements

## 3. Credential categories

A designated M5 environment may recognize these categories, subject to published trust rules:

- Individual identity credential
- Organization-registration credential
- Public-agency role credential
- DMV, licensing, or equivalent credential
- Court, tribunal, clerk, marshal, sheriff, or authorized-officer credential
- Tribal government, tribal court, registry, or authorized tribal credential
- Professional credential
- M5 Agency or Organization credential
- Digital-asset authority credential

Recognition of a category does not imply that every issuer, credential, or claimed authority in that category is accepted.

## 4. Issuer-registry requirements

An issuer registry entry SHOULD include:

- Legal name
- Issuing jurisdiction
- Credential type
- Public verification endpoint or method
- Credential-status or revocation method
- Signature, key, or verifying-method information
- Scope of recognized claims
- Effective and review dates
- Contact and escalation information
- Known reliance restrictions

## 5. Status, revocation, and compromise

A relying system SHOULD verify a credential’s status at a time appropriate to the risk of the requested action.

The registry MUST provide a documented approach for expired, suspended, revoked, superseded, compromised, disputed, or unverifiable issuer records and credentials.

## 6. High-impact requests

A credentialed request involving a wallet restriction, asset transfer, custody change, legal process, disclosure of protected information, major authority change, or agent restriction MUST undergo enhanced review by the independently responsible provider or authority that has lawful power to consider the request.

Neither the Foundation nor ICSN gains access to member data or value through registry participation or credential verification.

## 7. Reliance limits

Registry inclusion, credential verification, or a status result does not constitute:

- Legal advice
- A guarantee
- A government determination
- A finding of authority
- A finding of identity
- A warranty of credential accuracy
- An endorsement of the issuer
- A determination of legal rights

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
