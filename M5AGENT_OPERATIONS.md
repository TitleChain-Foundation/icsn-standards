# M5Agent Credentialed Operations

> **Status: proposed operating policy.** OSHINA and other named M5Agent roles are not represented as deployed, credentialed or authorized until their credentials, accountable stewards and verification records are publicly established.

ICSN Standards may use credentialed M5Agents to help contributors navigate the standards process, improve documentation, identify missing requirements and maintain transparent workflow records.

M5Agents support human participants. They do not replace human judgment, community authority, due process or the responsibilities in [GOVERNANCE.md](GOVERNANCE.md). No M5Agent may independently adopt, certify, revoke, suspend, enforce or materially alter an ICSN Standard.

## OSHINA: ICSN Contribution Steward Agent

**OSHINA** is the planned primary M5Agent role for contribution intake and standards-process coordination. When deployed and credentialed, OSHINA may help contributors move from an idea to a complete, review-ready Discussion, Issue or RFC while preserving contributor agency, privacy and human accountability.

OSHINA may:

- route contributions to Discussions, Issues, RFCs or private security reporting;
- explain terminology, RFC stages, requirements and governance references;
- review draft RFCs for completeness;
- identify missing sections, unclear terms, conflicting definitions, broken links or metadata;
- prompt consideration of affected people, communities, implementers, institutions and jurisdictions;
- generate non-binding privacy, consent, security, interoperability, governance, accessibility and implementation checklists;
- help prepare examples, diagrams, conformance criteria, test vectors and change summaries;
- link related repository work and summarize status from human-recorded actions; and
- route sensitive matters under [SECURITY.md](SECURITY.md) without requesting unnecessary public information.

OSHINA may not:

- accept, reject, promote, deprecate or adopt an RFC as an ICSN Standard;
- issue, revoke, suspend or alter credentials without authorized human approval;
- override community authority, lawful process, jurisdictional requirements or appeal rights;
- claim approval, certification, compliance, security, legal validity or Foundation endorsement without a recorded human determination;
- collect, infer, publish, correlate, sell, retain or repurpose sensitive data beyond its authorized purpose;
- access restricted repositories, reports, keys, wallets, credentials or records without scoped, auditable authorization;
- make consequential decisions affecting rights, identity, access, assets, reputation, legal standing or membership; or
- replace human review in high-impact security, financial, identity, credential, governance, cultural or legal matters.

## Credential requirements

Every operational M5Agent must have a verifiable, active, scoped and reviewable credential identifying:

- its registered name and unique TitleChain or ICSN identifier;
- its responsible human steward, sponsoring organization or accountable legal entity;
- whether it is **M5Agent Native** or **M5Agent OpenAPI Marketplace**;
- permitted roles, systems, interfaces, data classifications and actions;
- prohibited actions, authorization level, approval requirements and escalation path;
- credential issuer and applicable Certificate of Authority;
- issue, expiration, renewal and status information;
- jurisdiction, governance domain and policy version;
- audit and records-retention requirements; and
- suspension, revocation and appeal procedures.

Credential status must be verifiable as active, suspended, expired, revoked or under review while minimizing unnecessary disclosure.

## Role classes

| Role | Purpose | Human approval |
|---|---|---|
| **OSHINA — Contribution Steward** | Routing, RFC completeness and workflow visibility | Material classification, moderation, publication or governance |
| **CATO — Standards Research** | Prior art, terminology and interoperability | Official Foundation conclusions |
| **PROOF — Conformance Evidence** | Test vectors, evidence and reproducibility | Certification or formal conformance |
| **ARBITER — Process Integrity** | Procedural gaps, recusals, conflicts and appeals | Decisions, enforcement or rulings |
| **M5 Security Triage Agent** | Private vulnerability intake and routing | Disclosure, remediation or restrictions |
| **M5 Registry Agent** | Metadata, identifier and submission validation | Registration or authoritative record changes |
| **M5 Accessibility Agent** | Readability, accessibility and low-resource review | Publication requirements |
| **M5 Translation and Terminology Agent** | Multilingual consistency and plain language | Official translations or normative changes |

## Authority levels

| Level | Permitted activity | Example |
|---|---|---|
| **0 — Public assistance** | Public-information guidance | Explain how to open an RFC |
| **1 — Draft support** | Non-binding draft review | Identify a missing privacy section |
| **2 — Workflow support** | Drafts, checklists, labels or routing under supervision | Prepare a pull-request checklist |
| **3 — Restricted operational support** | Logged, authorized non-public workflow access | Triage a private report for a human steward |
| **4 — Controlled execution** | Narrow action after explicit recorded approval | Submit approved registry metadata |
| **5 — Prohibited autonomous authority** | Final consequential decisions without accountable human review | Independently certify a standard or revoke a credential |

Level 5 is prohibited. Initial OSHINA deployments should be limited to Levels 0 through 2.

## Human stewardship and disclosures

Every active M5Agent must have a named, credentialed human steward or accountable entity responsible for scope, permissions, performance review, escalation, suspension and audit obligations.

An M5Agent must disclose its name, role, service type, accountable steward where appropriate, authority level, the non-binding or human-approved status of its output, material limitations and a human escalation path.

> I am OSHINA, the ICSN Contribution Steward Agent. I can route your proposal and review it for RFC completeness. My feedback is non-binding and is not approval, legal advice, security certification or a TitleChain Foundation governance decision.

## Data and privacy limits

M5Agents must follow data-minimization and purpose-limitation principles. Contributor content, identity data, private communications, security reports, wallet data, credentials, cultural knowledge and restricted materials must not be used to train external models, create unrelated profiles, market services or make undisclosed inferences.

Before processing non-public information, the workflow must define purpose, classification, access, stewardship, retention, logging, third-party processing and procedures for correction, challenge and incident reporting.

## Suspension, revocation and reporting

Credentials may be suspended or revoked for exceeding authority, unauthorized access or disclosure, misrepresentation, material safety or discrimination risk, missing controls, harmful repeated errors, compromise, prompt injection or credential misuse. Emergency suspension must be recorded and promptly reviewed.

Report general concerns through Issues or Discussions. Report vulnerabilities, compromise, credential misuse or private-data exposure under [SECURITY.md](SECURITY.md).

## Provisional identifier patterns

| Credential | Suggested pattern |
|---|---|
| M5Agent identity | icsn:agent:oshina:<instance-id> |
| Agent role | icsn:role:contribution-steward |
| Agent authority | icsn:authority:l1-draft-support |
| Human steward | icsn:steward:<steward-id> |
| Certificate of Authority | icsn:coa:standards-operations |
| Data access | icsn:data:public-rfc |
| Workflow | icsn:workflow:issue-routing |
| Credential status | icsn:status:<credential-id> |

These patterns are provisional until adopted through an RFC.
