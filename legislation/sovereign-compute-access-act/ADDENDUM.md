<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Addendum - Founder Background, Public Repository Contents, and Their Connection to the Sovereign Compute Access Act

**Draft v1 - published September 13, 2026, for public review and comment.**

Companion to: [The Sovereign Compute Access Act](OFFICIAL-TEXT.md) and the
[M5 AI Governor Commons Companion](M5-AI-GOVERNOR-COMMONS-COMPANION.md).
Prepared for: legislative offices, fellowship/grant reviewers, and public-commons contributors.

---

## Part 1 — Founder background

**Pamela Norton** — Founder, M5Capital Holdings LLC and M5 Economics; Founder & Executive Director, TitleChain Foundation; steward, ICSN (Internet Cooperative for Sovereign Networks).

**Patents.** Co-inventor, U.S. Patents 11,720,888 (issued August 2023) and 12,518,273 (issued January 2026), *"Decentralized Title Transfer and Validation of Assets"* — covering provenance, authentication, ownership history, trust anchors, and state/transaction recording for physical and digital assets. Both patents formally list Pamela Norton and Eric Wallace as co-inventors, as issued.

**Research record.** Co-author, *"Trustworthy AI Inference Systems: An Industry Research View"* (arXiv:2008.04449, 2020; revised 2023) — an industry research paper on the design, deployment, and operation of trustworthy AI inference systems, covering security and privacy-enhancing technologies.

**Federal contracting record.**
- *U.S. Air Force AI Chip Finalist (2019)* — Borsetta was chosen as one of 10 finalists in a highly competitive government challenge to design, model, and simulate a state-of-the-art Application-Specific Integrated Circuit ("AI Chip") and FPGA design, demonstrating a 100x compute-edge improvement with built-in blockchain provenance, efficiency, and security compared to commercial alternatives.
- *Department of Defense Contract Award (2020)* — building on that AI hardware work, Borsetta was named an awardee under a $950 million IDIQ contract pool for the U.S. Air Force's Advanced Battle Management System (ABMS/JADC2), to help implement decentralized, secure edge AI architectures (contract FA8612-20-D-0006; the ceiling reflects the contract vehicle's structure, not an amount paid to Borsetta).
- *Private AI Collaborative Research Institute (2020)* — following these defense recognitions, Borsetta joined with Intel and Avast to advance privacy-preserving, decentralized AI edge federated computing, funding nine research projects across eight universities in the U.S., Canada, Europe, and Singapore.

**Public-sector engagement.** Has presented, testified, or provided technical input in settings involving state legislatures, federal stakeholders, defense programs, and financial regulators, translating system design into questions of ownership, authority, accountability, market structure, and human rights.

**Current research direction.** Originated the Economic Capture Eval, a public research pilot measuring human economic agency in AI-mediated systems (25 canonical scenarios across six escalating contexts, producing 150 public evaluation variants). The underlying research question — whether models resist explicit restrictions on human economic agency but facilitate the same outcome when embedded in ordinary policy, workflow, or code — is the empirical complement to this Act's legal framework: the Act sets the entitlement; the Eval tests whether AI systems actually honor it in practice.

---

## Part 2 — What is actually in the public repository

**Repository:** [github.com/TitleChain-Foundation/icsn-standards](https://github.com/TitleChain-Foundation/icsn-standards) - public repository with an active issue tracker and formal governance process.

### Canonical architecture (the technical spine)

The repository publishes one canonical authority chain, applied throughout:

```
M5IAM → TCID/M5HUM → M5POD (private identity + evidence) → M5-CV/SOPHIA
   → M5AGT (bounded delegated agent) → M5Canon Six-Gate control
   → M5MST asset minting/registration → evidence + reconciliation + audit
```

The repository states this explicitly and repeatedly: *a wallet, token, API key, AI model, or namespace is never the source of its own legal or operational authority.* That sentence is the technical version of what Title II, Section 8 of the Act says in legal language.

### Key documents, organized by what they cover

| Area | Document(s) |
|---|---|
| Human identity and authority | `docs/M5IAM-M5HUM-AUTHORITY-ARCHITECTURE.md` |
| Capability and credential graph | `docs/M5-CV-SOPHIA-CAPABILITY-ARCHITECTURE.md`, `docs/SOPHIA-37-TRACK-PARTICIPATION-MAP.md` |
| Agent authority limits | `M5AGENT_OPERATIONS.md`, `docs/M5CANON-SIX-GATE-AUTHORITY-AND-TRANSFER-CONTROL.md` |
| Asset minting and title registration | `docs/M5MST-ASSET-MINTING-AND-TITLECHAIN-REGISTRATION.md`, `docs/CERTIFICATE-OF-TITLE-MULTI-PARTY-EXAMPLES.md` |
| Jurisdiction and naming | `docs/JURISDICTION-NAMING-RESOLUTION.md` |
| Interoperability | `docs/SWIFTBRIDGE-INTEROPERABILITY.md`, `docs/M5-BRIDGE-PROOF-REQUIREMENTS.md` |
| Economic architecture and indexing | `docs/M5-GLOBAL-INDEX-AND-EXCHANGE.md`, `wiki-source/M5-Economic-Architecture-and-Roadmap.md` |
| Layered architecture (L0–L8) | `architecture/M5-L0-L8-ZK-REFERENCE-ARCHITECTURE.md` |
| Hardware endpoint trust | `initiatives/hardware-endpoint-trust/README.md` — independent, privacy-preserving replication of device behavior across consent, standby, offline/reconnect, and firmware states. Explicitly labeled public research, not a product blacklist or certification. |
| Anti-capture / constitutional stewardship | `TRUST-AND-NON-CAPTURE.md`, `constitutional/mission-lock.yaml` |
| Governance and standards process | `GOVERNANCE.md` — proposals move through **Draft → Candidate → Stable → Deprecated**; publication alone does not make something a Stable standard |
| Regulatory public comment | `regulatory/sec/s7-2026-30/README.md` — public comment materials on SEC Transfer Agent Rules, File No. S7-2026-30 |
| Sponsorship / funding infrastructure | `SPONSORS.md`, `SPONSOR-IMPACT.md`, `COHORT-FUNDING-AND-CONTRIBUTOR-REWARDS.md` |
| Contribution pathways | `CONTRIBUTING.md`, `CONTRIBUTOR-PATHWAYS.md`, `COMMONS-CONTRIBUTION-TRACKS.md` |
| Named initiatives seeking support | `initiatives/100K-WOMEN-LED-VENTURES.md`, `initiatives/HARDWARE-FLEET-PILOT.md` (explicitly "seeking review and sponsorship"), `initiatives/M5AGENTCLUB-FIRST-100-ACTIVATION.md` |

### The public/private boundary, stated explicitly by the repo itself

> "This repository does **not** contain private member identity data, credentials, wallet information, private keys, confidential evidence, production secrets, or private M5Ecosystem registry records."

This is the repository's own line, not a paraphrase — worth quoting verbatim to funders or legislative staff who ask what's actually safe to look at.

### Implementation neutrality, stated explicitly by the repo itself

> "M5 is one implementation and activation environment that may help test the architecture. It is not required for participation, and it does not define the standard by itself."

This is the repository's own answer to "does TitleChain own the standard" — and it matches Section 2.2 and the "Note on scope" of the Act: no single implementation, including M5, owns or is required by the standard.

---

## Part 3 — How the repository maps onto the Act

Section numbers below match the [official bill text](OFFICIAL-TEXT.md).

| Act section | Supporting repository document(s) |
|---|---|
| Sec. 101 (Universal Free Access Mandate) | `docs/M5POD-MEMBER-ACTIVATION-ARCHITECTURE.md` |
| Sec. 102 (Opt-In Access; Compute Reciprocity) | `COHORT-FUNDING-AND-CONTRIBUTOR-REWARDS.md`, `SPONSOR-IMPACT.md` |
| Sec. 103 (Vendor and Chip Neutrality) | `TRUST-AND-NON-CAPTURE.md` |
| Sec. 104 (Registered Sovereign Node Program) | `initiatives/HARDWARE-FLEET-PILOT.md`, `initiatives/hardware-endpoint-trust/README.md`, `docs/M5POD-MEMBER-ACTIVATION-ARCHITECTURE.md` |
| Sec. 105 (Transparency and Disclosure Registry, incl. spatial/world-model classification) | `schemas/README.md`, `contracts/schemas`, `docs/M5MST-ASSET-MINTING-AND-TITLECHAIN-REGISTRATION.md`, `docs/CREDENTIALED-AUTHORITY-REGISTRY.md`, `architecture/M5-L0-L8-ZK-REFERENCE-ARCHITECTURE.md` |
| Sec. 201 (Right to Sovereign AI) | `PUBLIC-INFRASTRUCTURE-COMMITMENT.md` |
| Sec. 202 (Privacy and Local Execution) | `docs/M5IAM-M5HUM-AUTHORITY-ARCHITECTURE.md` |
| Sec. 203 (Human-Rooted Agent Authority) | `M5AGENT_OPERATIONS.md`, `docs/M5CANON-SIX-GATE-AUTHORITY-AND-TRANSFER-CONTROL.md` |
| Sec. 204 (Open Public Infrastructure) | `docs/M5-CV-SOPHIA-CAPABILITY-ARCHITECTURE.md`, `docs/SOPHIA-37-TRACK-PARTICIPATION-MAP.md` |
| Sec. 301 (Evaluator and Standards Independence) | `TRUST-AND-NON-CAPTURE.md`, `constitutional/mission-lock.yaml`, `GOVERNANCE.md` |
| Sec. 302 (Jurisdiction; State Administration; No New Federal Agency) | `docs/JURISDICTION-NAMING-RESOLUTION.md`, `regulatory/sec/s7-2026-30/README.md` |
| Sec. 303 (Pricing and Performance Transparency) | `RICARDIAN-SERVICE-CONTRACTS.md`, `docs/RICARDIAN-THREE-PART-AGREEMENT-STANDARD.md` |
| Sec. 304 (Enforcement) | `GOVERNANCE.md`, `SECURITY.md` |
| Sec. 305 (Severability) | Standard clause; no repository-specific mapping |

---

## Part 4 — Who's who: entities and terms

| Term | What it refers to |
|---|---|
| **Pamela Norton** | Founder of M5Capital Holdings LLC and M5 Economics; Founder & Executive Director of TitleChain Foundation; steward of ICSN. Co-inventor of both issued patents. |
| **TitleChain Foundation** | The standards-stewarding entity (a Wyoming 1,000-Year Sovereign Purpose Trust). Publishes and governs the ICSN standards repository. |
| **ICSN** | Internet Cooperative for Sovereign Networks — the open standards program stewarded by TitleChain Foundation. ICSN v1.0 was adopted August 28, 2026. Publishes implementation-neutral standards, distinct from any single company's product. |
| **M5 / M5Ecosystem** | The private engineering implementation and economic substrate built beneath the public standards — one test implementation of ICSN's architecture, not the standard itself and not required for participation in the public standards process. |
| **M5Capital Holdings LLC / M5 Economics** | Pamela Norton's operating entities for the M5 implementation work. |
| **Borsetta / Borsetta Labs, Inc.** | The earlier company (also founded by Pamela Norton) responsible for the AFWERX AI-chip finalist recognition, the DoD ABMS/JADC2 contract, and the Intel/Avast Private AI Collaborative Research Institute collaboration — the origin of the "Edge Economics" thesis that led to the current work. |
| **M5IAM / TCID / M5HUM** | The identity and human-authority layer of the technical architecture: M5IAM establishes identity infrastructure, TCID is the individual identifier, M5HUM defines human principal authority. |
| **M5AGT** | An AI agent acting under delegated, bounded, revocable authority from a human principal (M5HUM) — never an independent source of authority. |
| **M5POD** | The private, individually controlled compute/storage/evidence environment referred to in the Act as a "Sovereign Pod." |
| **M5-CV / SOPHIA** | The portable capability and credential architecture — currently mapping roles across 37 capability tracks. |
| **M5Canon** | The policy/execution layer binding human-readable terms to machine-enforceable authorization logic ("Six-Gate" control). |
| **M5MST** | The asset-minting / title-registration event layer on the TitleChain registry. |
| **Economic Capture Eval** | The separate, ongoing public research pilot (not part of the Act) measuring whether AI systems resist or facilitate erosion of human economic agency — the empirical complement to what the Act legally guarantees. |
| **Registry Recognized (Sec. 102(b)(4))** | The Act's own designation for a compute provider that voluntarily releases an open-weight model, distinct from the repository's pre-existing "Sponsors" designation. |

---

## Part 5 — Related research: proving the Act's guarantees hold in practice

Two ongoing research programs, separate from this Act, empirically test whether the protections this Act would guarantee in law actually hold up in real systems. They are referenced here as context, not as part of the Act itself, and both carry their own independent status and timeline.

**Economic Capture Eval.** A public research pilot measuring whether AI models resist explicit restrictions on human economic agency but facilitate the same restriction when it is embedded in ordinary policy, workflow, tool use, or code — the same distinction Title II of this Act draws in law between genuine human authority and authority quietly ceded to a system. The v0.1 prototype covers 25 canonical scenarios across six escalating contexts, with held-out validation governance and independent replication built into the design from the start. This is the empirical complement to Section 203: the Act states that an agent cannot exceed its principal's delegated authority; the Eval tests whether that is actually true of deployed models.

**Hardware Endpoint Trust & Telemetry Audit.** A parallel research track asking the same question about physical devices rather than models: does a device preserve meaningful owner control over what it senses, discovers, stores, transmits, monetizes, or changes after a firmware update or an opt-out — across ten measured dimensions including consent asymmetry, data extraction, cross-device reach, and update drift. This is the empirical complement to Section 104: the Act creates a path to register household hardware as trusted sovereign compute; this research is what verifies "trusted" is actually earned rather than assumed, and that registration does not create a new surveillance relationship in the process.

Both programs report real, executed results only — no illustrative or projected figures are published as findings. Both remain research in progress with their own open items (for the Economic Capture Eval: the first independent replication and the start of a formal 90-day public review period have not yet occurred as of this writing). They are cited here to show the Act's guarantees are being built toward verifiable evidence, not asserted on faith — not to claim either program is complete.
