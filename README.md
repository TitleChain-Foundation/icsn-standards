# ICSN Standards

**Open specifications, RFCs, schemas, conformance work, and public infrastructure for human-rooted identity and accountable digital systems.**

[![Release](https://img.shields.io/github/v/release/TitleChain-Foundation/icsn-standards?display_name=tag)](https://github.com/TitleChain-Foundation/icsn-standards/releases)
[![License](https://img.shields.io/badge/license-asset--level-blue)](LICENSE.md)
[![Discussions](https://img.shields.io/github/discussions/TitleChain-Foundation/icsn-standards)](https://github.com/TitleChain-Foundation/icsn-standards/discussions)

ICSN is the public standards program of the [TitleChain Foundation](https://github.com/TitleChain-Foundation). It develops implementation-neutral ways to preserve human authority, limit delegated machine authority, and make identity, credentials, provenance, and digital systems portable and reviewable.

## Constitutional stewardship

TitleChain Foundation is designed for stewardship, not acquisition.

Its constitutional model is anchored by the **TitleChain Sovereign Purpose Trust**, a Wyoming purpose-trust structure designed under its governing framework for a maximum term of one thousand years. The purpose is to preserve a human-first digital framework across generations while separating constitutional stewardship from commercial operation.

The public commitments include:

- human authority remains the root of consequential digital authority;
- privacy, meaningful consent, portability, recovery, and the right to exit;
- no sponsor, donor, vendor, implementation, or founder buys unilateral standards control through funding or adoption;
- no forced vendor lock-in or coercive surveillance as a condition of ordinary participation; and
- M5 and other implementations remain separate from the standards process.

Read [Trust Stewardship and the Non-Capture Principle](TRUST-AND-NON-CAPTURE.md). The public summary does not replace the Trust instrument, Foundation governing documents, or applicable law.

**Fund the commons. Never own the commons.**

## Get involved

- Read [current priorities](ROADMAP.md).
- Review [open issues](https://github.com/TitleChain-Foundation/icsn-standards/issues), including `good first issue` and `help wanted` work.
- Ask questions or propose early ideas in [Discussions](https://github.com/TitleChain-Foundation/icsn-standards/discussions).
- Follow the [participation pathway](PARTICIPATE.md) and [contribution guide](CONTRIBUTING.md).
- Review the [RFC index](rfcs/README.md) or start with the [RFC template](rfcs/0000-template.md).

Do not place private identity data, credentials, personal contact details, wallet information, private keys, or confidential business information in a public issue, discussion, or pull request.

## Standards scope

Current work includes:

- **Human authority** — proof of life, presence, intent, and authority connected to defined digital actions.
- **Accountable agents** — narrow, purpose-bound, auditable, time-limited, and revocable delegation.
- **Portable identity and credentials** — selective disclosure, recovery, provenance, and the right to exit.
- **Sovereign networks** — interoperable registries and coordination without surrendering local authority.
- **Security and privacy** — threat analysis, data minimization, synchronization safety, and resilient recovery.
- **Conformance** — schemas, test vectors, implementation guidance, and reference implementations.

These are research and standards directions. They do not imply endorsement by a government, regulator, international organization, standards body, company, or community.

## Standards process

Proposals advance through **Draft**, **Candidate**, **Stable**, and **Deprecated** stages under [open governance](GOVERNANCE.md).

Material changes begin with public discussion and an RFC. Stable status requires documented review, security and privacy analysis, conformance criteria, implementation evidence, and an affirmative decision by authorized standards stewards.

Publication in this repository does not by itself make a proposal a Foundation standard.

## Public infrastructure: IAM at no charge to the individual

The Foundation's first activation commitment is a human-controlled IAM identity origin offered at no charge to the individual and designed to preserve that no-charge foundational access over time.

IAM is **optional** for standards participation. You do not need an IAM account to read, review, contribute to, fork, or independently implement ICSN work.

The two public entry points are deliberately separate:

1. **Free IAM:** [m5bank.app](https://m5bank.app/) — the no-charge foundational identity-origin account.
2. **Program enrollment:** [m5member.netlify.app](https://m5member.netlify.app/) — the separate M5Member enrollment/activation pathway through which an eligible participant progresses toward her **M5BankofMe account** and the applicable M5 program experience.

Free IAM does not require program enrollment, and neither IAM nor M5 enrollment is required to participate in ICSN standards.

Read the [Public Infrastructure Commitment](PUBLIC-INFRASTRUCTURE-COMMITMENT.md) and the first scaled activation initiative for [up to 100,000 women-led ventures](initiatives/100K-WOMEN-LED-VENTURES.md).

## Repository map

| Area | Start here |
| --- | --- |
| RFCs and specifications | [`rfcs/`](rfcs/README.md) |
| Schemas and validation | [`schemas/`](schemas/) and [`scripts/validate_repository.py`](scripts/validate_repository.py) |
| Constitutional stewardship | [TRUST-AND-NON-CAPTURE.md](TRUST-AND-NON-CAPTURE.md) and [`constitutional/mission-lock.yaml`](constitutional/mission-lock.yaml) |
| Public infrastructure | [PUBLIC-INFRASTRUCTURE-COMMITMENT.md](PUBLIC-INFRASTRUCTURE-COMMITMENT.md) |
| 100K women-led venture initiative | [`initiatives/100K-WOMEN-LED-VENTURES.md`](initiatives/100K-WOMEN-LED-VENTURES.md) |
| M5AgentClub first-100 activation | [`initiatives/M5AGENTCLUB-FIRST-100-ACTIVATION.md`](initiatives/M5AGENTCLUB-FIRST-100-ACTIVATION.md) |
| M5Brain reference architecture | [`initiatives/M5BRAIN-REFERENCE-ARCHITECTURE.md`](initiatives/M5BRAIN-REFERENCE-ARCHITECTURE.md) |
| Activation outcome graph | [`initiatives/M5ACTIVATION-OUTCOME-GRAPH.md`](initiatives/M5ACTIVATION-OUTCOME-GRAPH.md) |
| Team and extended ecosystem | [TEAM-AND-ECOSYSTEM.md](TEAM-AND-ECOSYSTEM.md) |
| Governance | [GOVERNANCE.md](GOVERNANCE.md) |
| Contributions | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Participation | [PARTICIPATE.md](PARTICIPATE.md) |
| Security reporting | [SECURITY.md](SECURITY.md) |
| Licensing | [LICENSE.md](LICENSE.md) and [license matrix](LICENSES/LICENSE-MATRIX.md) |
| Releases | [CHANGELOG.md](CHANGELOG.md) and [release checklist](RELEASE-CHECKLIST.md) |
| Sponsorship | [SPONSORS.md](SPONSORS.md) and [SPONSOR-IMPACT.md](SPONSOR-IMPACT.md) |

## First-100 reference activation

The first-100 M5AgentClub program is a reference activation environment, not a requirement for ICSN participation.

**M5Brain** is the member-controlled knowledge, memory, relationship, and context layer used by the M5 Freedom Office and authorized native M5Agents. **Pamela is Reference Member 0001** for extracting a portable Freedom Office Core, and the first 100 test whether that reference pattern is repeatable.

Skool is used as a classroom/community interface for M5AgentClub. It is intentionally not the member's IAM, Passport, M5Brain, credential store, or economic record.

Sponsors may support activations and receive aggregate impact measures while individual evidence remains controlled by the member.

## Implementation neutrality

M5 is one implementation and activation environment that may help test the architecture. It is not required for participation, and it does not define the standard by itself.

GitHub participation, Foundation governance, commercial services, account onboarding, employment, credentials, cohort participation, and investment are separate relationships governed by their own processes and terms.

## Support the work

Sponsorship helps fund:

- independent development and maintenance of public specifications and RFCs;
- security and privacy review;
- documentation, conformance criteria, test vectors, and reference implementations;
- open-source tooling and public infrastructure;
- release engineering; and
- contributor coordination that keeps the work accessible.

Sponsorship does **not** purchase influence over standards decisions, governance authority, conformance status, ownership of the commons, or access to private participant information.

Everyday supporters can **[sponsor the TitleChain Foundation through GitHub](https://github.com/sponsors/TitleChain-Foundation)** with a monthly or one-time payment. Public monthly levels range from individual support through institutional, infrastructure, development-acceleration, and strategic-infrastructure sponsorship.

Organizations may also apply to sponsor a named area such as standards, security, reference implementations, developer infrastructure, releases, education, cohort activation, accessibility, compute, public infrastructure, or ecosystem integration. Custom organizational pricing is discussed privately and documented according to scope, duration, deliverables, reporting, recognition, independence, and privacy boundaries. **[Discuss an organizational sponsorship](mailto:hello@titlechainfoundation.org?subject=ICSN%20Organizational%20Sponsorship)**.

See [SPONSORS.md](SPONSORS.md) for the complete policy.

## Licensing

This repository uses explicit asset-level licensing. Apache 2.0 and CC BY 4.0 apply only to materials expressly carrying those designations. The Cyrus Purpose-Bound Constitutional Commons License 1.0 is a public-review draft and applies only where expressly designated. Other material remains reserved unless stated otherwise.

The repository validation utility at [`scripts/validate_repository.py`](scripts/validate_repository.py) is expressly designated **Apache-2.0** so the public workspace contains an unambiguous open-source software contribution.

Review [LICENSE.md](LICENSE.md), the [license matrix](LICENSES/LICENSE-MATRIX.md), and the designation attached to an asset before reuse.

## Project records

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Governance](GOVERNANCE.md)
- [Changelog](CHANGELOG.md)
- [Citation](CITATION.cff)
