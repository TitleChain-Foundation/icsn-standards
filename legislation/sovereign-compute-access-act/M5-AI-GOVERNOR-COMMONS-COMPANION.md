<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# The M5 AI Governor Commons - Draft v1 Technical Companion

**Draft v1 - published September 13, 2026, for public review and comment.**

This companion describes proposed technical work that the legislation builds
toward. The four identifiers below are Draft v1 proposal identifiers; they are
not represented as adopted ICSN standards or as documents currently published
in this repository. The repository's [governance process](../../GOVERNANCE.md)
requires Draft, Candidate, Stable, and Deprecated maturity labels, and
publication alone does not confer Stable status.

Submitted alongside the Sovereign Compute Access Act by the Founder of M5Capital Holdings LLC / M5 Economics, on behalf of TitleChain Foundation and ICSN.

---

## What this is

The M5 AI Governor Commons is a public draft standard for governing AI providers, agents, plugins, MCP servers, connectors, and metered tools — built so that authority, privacy, budgets, evidence, and accountability stay with the person or organization using them, regardless of which AI provider they use.

The core design rule: **models and plugins are capabilities, not principals.** Authority originates with a person or legally accountable entity and stays portable when providers change.

## The four standards documents

- **M5-AIGOV-001** — Provider and plugin governance standard. Establishes one policy boundary between a principal, their agent, and any external AI provider or tool, so an application never has to surrender its governance model when it changes providers.
- **M5-AIMOD-001** — Proposed resident local/open-weight model and hardware standard. Defines how a private compute environment (an "M5POD") could select a local, open-weight resident model based on measured hardware capability. It informs sections 104 and 105(d) of the Sovereign Compute Access Act and is intended as a compatibility contract rather than a dependency on one model family.
- **M5-AISPACE-001** — Spatial, embodied, experiential, sensor, world-model, and physical-action governance. Extends the same governance boundary to world models, robotics, wearables, and other physical/experiential AI, introducing a "Human Experience Boundary" so that a model gaining access to more senses does not thereby gain more sovereignty over the person using it.
- **M5-AIPROV-001** — Sovereign provider identity standard. Defines how a commercial AI provider is represented inside the network as a bound service identity (e.g., "M5-OpenAI") rather than an anonymous API endpoint — both the requesting account and the provider's service account are separately, bilaterally governed.

## How this connects to the Act

Section numbers match the [official bill text](OFFICIAL-TEXT.md).

| Act provision | Standard it draws on |
|---|---|
| Sec. 104 — Registered Sovereign Node (BYOD) | M5-AIMOD-001 hardware classification (M5-H0→H5) and the ICSN Hardware Onboarding Standard (RFC 0001) |
| Sec. 105 — Transparency and Disclosure Registry | M5-AIGOV-001 provider/plugin manifest and governance-receipt schemas |
| Sec. 105(d) — Spatial/world-model classification | M5-AISPACE-001's existing multi-axis governance approach for physical/experiential AI |
| Sec. 103 — Vendor and chip neutrality | M5-AIMOD-001's explicit design rule against single-model-family lock-in |

## Proposed governance principles

1. Public standards text states the current canonical specification, not internal QA history.
2. The core remains vendor-neutral.
3. Provider-specific volatility belongs in manifests and adapters, not in the standard itself.
4. Privacy, authority, and evidence requirements take precedence over convenience.
5. The M5POD is the reference sovereign enforcement container for M5-conformant use — not a requirement for outside parties to read, critique, or independently implement the open protocol.
6. No model or plugin is treated as an independent principal.
7. Material normative changes require a version change and public rationale.

## Related repository publication status

The ICSN standards repository is public and includes:

- A formal standards process (Draft → Candidate → Stable → Deprecated) documented in GOVERNANCE.md.
- An explicit public/private boundary statement: the repository contains no private member identity data, credentials, wallet information, private keys, confidential evidence, or private M5Ecosystem registry records.
- A real repository map spanning architecture, RFCs, schemas, conformance tests, methodology, datasets, and multiple public-review initiatives — including a hardware endpoint trust and telemetry workstream, and a public comment thread on SEC Transfer Agent Rules (File No. S7-2026-30).
- Explicit "implementation neutrality" language: M5 is one reference implementation and activation environment, not a requirement for participation, and does not define the standard by itself.
- Existing sponsor and funding infrastructure already in the repo: SPONSORS.md, SPONSOR-IMPACT.md, and COHORT-FUNDING-AND-CONTRIBUTOR-REWARDS.md.

**When citing this to Congress or funders:** cite the repository as live public infrastructure — that claim now holds up. But check the maturity label on any *specific* document you reference (Draft RFC vs. Stable standard) before representing it as adopted; the repository's own README is explicit that publication alone does not make a proposal a Stable standard.

## What contribution looks like once public

The Commons is designed to accept: provider adapters, pricing/caching corrections, privacy and retention critiques, threat models, government/institutional requirements, conformance tests, MCP/plugin examples, local/private AI profiles, and accessibility improvements — through GitHub Issues and pull requests, so proposed changes remain reviewable and attributable.
