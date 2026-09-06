# ICSN Standards

**Open specifications, schemas, conformance work, and public infrastructure for human-rooted identity, accountable agents, title/provenance, jurisdiction-aware digital systems, and portable economic evidence.**

ICSN is the public standards program of the TitleChain Foundation. It publishes implementation-neutral standards and clearly labeled M5 reference architectures so governments, transfer agents, financial institutions, engineers, statisticians, economists, researchers, and other reviewers can inspect how identity, authority, title, transfer, and machine action can remain attributable and auditable as records move from paper to digital systems.

## See the public architecture

[![M5POD private member stack rooted in ICSN open standards, human identity, and member authority](assets/public-review/m5pod-stack.png)](assets/public-review/README.md)

**Help build the public commons for the digital-asset edge economy.** Open the [SEC public-review board](https://github.com/orgs/TitleChain-Foundation/projects/2/views/2), review the [featured architecture visuals](assets/public-review/README.md), join [Foundation Discussion 19](https://github.com/orgs/TitleChain-Foundation/discussions/19), or track deadline progress in the [SEC public-review milestone](https://github.com/TitleChain-Foundation/icsn-standards/milestone/2). The public economic-data work concerns privacy-preserving, provenance-aware indicators and methodologies under open review; it is not represented as an official statistic, regulated benchmark, or deployed service.

> **The M5 architecture makes AI operationally useful without allowing AI, credentials, wallets, employees, contractors, APIs, or third-party systems to become unaccountable sources of authority.**

## Canonical public architecture

The public M5 reference path is:

```text
M5IAM
  ↓
TCID / M5HUM
  ↓
M5POD — private identity + evidence
  ↓
M5-CV / SOPHIA — capability + role + credential state
  ↓
M5AGT — bounded delegated agent
  ↓
M5Canon Six-Gate control
  ↓
M5MST asset minting / TitleChain registration on WyomingChain.eth
  ↓
evidence + reconciliation + audit
```

A wallet, token, API key, AI model, or namespace is never the source of its own legal or operational authority.

## Start here

| Area | Public reference |
| --- | --- |
| Human identity and authority | [`docs/M5IAM-M5HUM-AUTHORITY-ARCHITECTURE.md`](docs/M5IAM-M5HUM-AUTHORITY-ARCHITECTURE.md) |
| M5-CV / SOPHIA capability graph | [`docs/M5-CV-SOPHIA-CAPABILITY-ARCHITECTURE.md`](docs/M5-CV-SOPHIA-CAPABILITY-ARCHITECTURE.md) |
| Six-Gate authority control | [`docs/M5CANON-SIX-GATE-AUTHORITY-AND-TRANSFER-CONTROL.md`](docs/M5CANON-SIX-GATE-AUTHORITY-AND-TRANSFER-CONTROL.md) |
| M5MST asset minting + TitleChain registration | [`docs/M5MST-ASSET-MINTING-AND-TITLECHAIN-REGISTRATION.md`](docs/M5MST-ASSET-MINTING-AND-TITLECHAIN-REGISTRATION.md) |
| Transfer-agent reference architecture | [`docs/TRANSFER-AGENT-DIGITAL-ASSET-REFERENCE-ARCHITECTURE.md`](docs/TRANSFER-AGENT-DIGITAL-ASSET-REFERENCE-ARCHITECTURE.md) |
| Jurisdiction naming + resolution | [`docs/JURISDICTION-NAMING-RESOLUTION.md`](docs/JURISDICTION-NAMING-RESOLUTION.md) |
| SwiftBRIDGE interoperability | [`docs/SWIFTBRIDGE-INTEROPERABILITY.md`](docs/SWIFTBRIDGE-INTEROPERABILITY.md) |
| M5 Global Index and Exchange | [`docs/M5-GLOBAL-INDEX-AND-EXCHANGE.md`](docs/M5-GLOBAL-INDEX-AND-EXCHANGE.md) |
| L0–L8 + ZK dependencies | [`architecture/M5-L0-L8-ZK-REFERENCE-ARCHITECTURE.md`](architecture/M5-L0-L8-ZK-REFERENCE-ARCHITECTURE.md) |
| Bridge proof requirements | [`docs/M5-BRIDGE-PROOF-REQUIREMENTS.md`](docs/M5-BRIDGE-PROOF-REQUIREMENTS.md) |
| Certificate-of-title examples | [`docs/CERTIFICATE-OF-TITLE-MULTI-PARTY-EXAMPLES.md`](docs/CERTIFICATE-OF-TITLE-MULTI-PARTY-EXAMPLES.md) |
| DUNA commons governance | [`docs/DUNA-COMMONS-GOVERNANCE-ROADMAP.md`](docs/DUNA-COMMONS-GOVERNANCE-ROADMAP.md) |
| Ricardian three-part standard | [`docs/RICARDIAN-THREE-PART-AGREEMENT-STANDARD.md`](docs/RICARDIAN-THREE-PART-AGREEMENT-STANDARD.md) |
| Credentialed authority registry | [`docs/CREDENTIALED-AUTHORITY-REGISTRY.md`](docs/CREDENTIALED-AUTHORITY-REGISTRY.md) |
| Economic architecture | [`wiki-source/M5-Economic-Architecture-and-Roadmap.md`](wiki-source/M5-Economic-Architecture-and-Roadmap.md) |
| RFCs | [`rfcs/`](rfcs/) |
| Schemas | [`schemas/`](schemas/) |

## M5 actor, asset, and origination codes

- **M5HUM — Human Principal.** Credentialed human sovereign. Every M5AGT is accountable to a named M5HUM.
- **M5AGT — Autonomous Agent.** AI agent acting on behalf of a human. It cannot exceed the M5HUM's permissions.
- **M5AST — Asset Token.** Real-world asset-backed token with one of five M1–M5 tiers on WyomingChain.eth.
- **M5MST — Asset Minting.** Asset-minting event or TitleChain registration on WyomingChain.eth.

An M5MST event records minting or registration; it does not itself grant transfer authority. Mint authority and transfer authority are separate capabilities.

## M5 asset/economic classification

The internal M5 asset/economic state model is separate from the M5Bank account stack and separate from external legal classification:

| State | Meaning |
| --- | --- |
| **M1** | Money + Utility |
| **M2** | Commodities |
| **M3** | Titled / Unique / Collectible RWA |
| **M4** | Financial Wrapper |
| **M5** | Jurisdictional Security-State Profile |

## Repository map

| Area | Public reference |
| --- | --- |
| Regulatory public records | [SEC Transfer Agent Rules — File No. S7-2026-30](regulatory/sec/s7-2026-30/README.md) |
| Public reference artifacts | [Appendix B artifacts and recommendation map](docs/PUBLIC-REFERENCE-ARTIFACTS.md) |
| Visual architecture overview | [Sovereign M5POD system diagram](architecture/rendered/m5-sovereign-stack.svg) and [accessible description](architecture/M5POD-MEMBER-ACTIVATION-ALT-TEXT.md) |
| RFCs and specifications | [`rfcs/`](rfcs/README.md) |
| Schemas and validation | [`schemas/`](schemas/) and [`scripts/validate_repository.py`](scripts/validate_repository.py) |
| Constitutional stewardship | [TRUST-AND-NON-CAPTURE.md](TRUST-AND-NON-CAPTURE.md) and [`constitutional/mission-lock.yaml`](constitutional/mission-lock.yaml) |
| Public infrastructure | [PUBLIC-INFRASTRUCTURE-COMMITMENT.md](PUBLIC-INFRASTRUCTURE-COMMITMENT.md) |
| 100K women-led venture initiative | [`initiatives/100K-WOMEN-LED-VENTURES.md`](initiatives/100K-WOMEN-LED-VENTURES.md) |
| M5AgentClub first-100 activation | [`initiatives/M5AGENTCLUB-FIRST-100-ACTIVATION.md`](initiatives/M5AGENTCLUB-FIRST-100-ACTIVATION.md) |
| M5Brain reference architecture | [`initiatives/M5BRAIN-REFERENCE-ARCHITECTURE.md`](initiatives/M5BRAIN-REFERENCE-ARCHITECTURE.md) |
| Activation outcome graph | [`initiatives/M5ACTIVATION-OUTCOME-GRAPH.md`](initiatives/M5ACTIVATION-OUTCOME-GRAPH.md) |
| M5POD activation architecture | [`docs/M5POD-MEMBER-ACTIVATION-ARCHITECTURE.md`](docs/M5POD-MEMBER-ACTIVATION-ARCHITECTURE.md) and [`architecture/`](architecture/) |
| Consent and authorization review drafts | [`docs/M5-ACTIVATION-CONSENT-AUTHORIZATION-MAP.md`](docs/M5-ACTIVATION-CONSENT-AUTHORIZATION-MAP.md) |
| Hardware fleet pilot seeking review and sponsorship | [`initiatives/HARDWARE-FLEET-PILOT.md`](initiatives/HARDWARE-FLEET-PILOT.md) |
| Team and extended ecosystem | [TEAM-AND-ECOSYSTEM.md](TEAM-AND-ECOSYSTEM.md) |
| Governance | [GOVERNANCE.md](GOVERNANCE.md) |
| Adopted M5 member-authority governance | [docs/index.md](docs/index.md) |
| Contributions | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Work by skill | [CONTRIBUTOR-PATHWAYS.md](CONTRIBUTOR-PATHWAYS.md) |
| Participation | [PARTICIPATE.md](PARTICIPATE.md) |
| Security reporting | [SECURITY.md](SECURITY.md) |
| Licensing | [LICENSE.md](LICENSE.md) and [license matrix](LICENSES/LICENSE-MATRIX.md) |
| Releases | [CHANGELOG.md](CHANGELOG.md) and [release checklist](RELEASE-CHECKLIST.md) |
| Sponsorship and sharing | [SPONSORS.md](SPONSORS.md), [SPONSOR-IMPACT.md](SPONSOR-IMPACT.md), and the [social share kit](campaigns/SOCIAL-SHARE-KIT.md) |

## Implementation neutrality

M5 is one implementation and activation environment that may help test the architecture. It is not required for participation, and it does not define the standard by itself.

GitHub participation, Foundation governance, commercial services, account onboarding, employment, credentials, cohort participation, and investment are separate relationships governed by their own processes and terms.

Read [M5Ecosystem Approval Boundary](M5ECOSYSTEM-APPROVAL-BOUNDARY.md) for the separate approval and licensing rules for restricted implementations, production systems, credentials, and private member or partner material.

M4/M5 state does not erase the underlying M1/M2/M3 title/right record. M5 labels do not create a legal conclusion; applicable law and authoritative legal/regulatory determinations remain controlling.

## Public/private boundary

This repository does **not** contain private member identity data, credentials, wallet information, private keys, confidential evidence, production secrets, or private M5Ecosystem registry records.

Public standards participation does not require an M5 account. M5 is a reference implementation and activation environment used to test and demonstrate the public architecture.

## Standards process

Proposals advance through **Draft**, **Candidate**, **Stable**, and **Deprecated** under [`GOVERNANCE.md`](GOVERNANCE.md). Publication alone does not make a proposal a Stable standard.

## Licensing

This repository uses asset-level licensing. Review [`LICENSE.md`](LICENSE.md) and the applicable license designation before reuse.

## Get involved

Start with [PARTICIPATE.md](PARTICIPATE.md) for an introduction to the Foundation and ways to help. Use the Foundation's public Discussions, Issues, RFC process, and [contributor pathways](CONTRIBUTOR-PATHWAYS.md) to review the work. For the SEC transfer-agent comment, use the [public artifact and recommendation map](docs/PUBLIC-REFERENCE-ARTIFACTS.md) to choose the relevant review thread.

Every public artifact identifies its maturity. **Public Review Draft** and **Draft RFC** material is open for review; it is not an adopted standard, production deployment, credential, authorization, or representation of regulatory approval. Do not post private identity data, credentials, account information, keys, or confidential evidence in public channels.
