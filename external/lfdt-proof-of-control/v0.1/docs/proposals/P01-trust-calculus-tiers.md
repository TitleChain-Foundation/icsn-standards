# Proposal: normative changes to C8, C10.2 and C7.4 from P01 (Trust Calculus)

**Date:** 2026-08-10 · **Status:** proposal only, with one conclusion superseded on 2026-08-30 (see the Owner note below). No file under `ov-poc-standard/` has been edited by this proposal.

**Source of the findings**

* `research/Trust Calculus Attestation Research.md` — the completed P01 research (§3 formalism, §5 validation, §6 tier re-derivation, §7 standards consequences).
* `docs/parallax-outcomes.md` — what building the `parallax` tool established, and the corrections it forced on P01. **Where the two disagree, the outcomes doc governs**, because it records measured tool output rather than desk analysis.

**Targets:** `0.1/en/0x10-C08-Verifiability-Tiers.md`, `0.1/en/0x10-C10-Conformance-and-Disclosure.md` (C10.2), `0.1/en/0x10-C07-Evidence-Generation-and-Properties.md` (C7.4).

---

## The evidence base, and its limits — read before weighing any change below

Everything here rests on **five self-authored deployment descriptions and no real-world system** (`parallax-outcomes.md`, amendment 4). What the tool measured:

* The **five-party Intel TDX residual trust set is derivable from the deployment description**, not hardcoded — verified by collapsing a principal in the input and watching the count track it. **Exactly one of the five (the collateral authority) has a bounded detection latency; the other four are silent and permanent.** That asymmetry is P01's central empirical claim and it holds.
* **Σ₂ (TDX) and Σ₄ (ZK rollup) are genuinely incomparable** — five disjoint assumptions on each side, same claim, and confirmed not to be an artifact of the encoding.
* **The hybrid TEE+ZK design's two layers share a build pipeline**; an independent-pipelines variant correctly reports nothing (negative control).
* **Anchoring is a trade, not a pure gain**: it converts log-operator trust into a bounded detection window and silently ingests a consensus-execution-fidelity assumption. Both appear in the manifest.

What the tool did **not** establish, and what the research doc overstates:

* **Incomparability is narrower than "trust sets come out incomparable."** Of twelve ordered pairs across the four non-hybrid examples, eight are refused (they establish different propositions) and four are `Incomparable` — **two unordered pairs, Σ₁/Σ₃ and Σ₂/Σ₄** (`parallax-outcomes.md`, amendment 3). Only Σ₂/Σ₄ is separately vouched as non-artifactual.
* No real deployment, no independent encoder, no third-party audit of any manifest.

So "settled by measurement" below always means *settled by the tool, on self-authored inputs*. It is enough to refute a universal claim the standard currently makes — one counterexample does that — and it is **not** enough to install a new ordering, a new tier taxonomy, or a machine-readable schema as normative. The proposal is shaped accordingly: it **deletes false claims and adds disclosure**, and marks everything structural `[WG-INPUT NEEDED]`.

---

> **Owner note, 2026-08-30 — Tier 3 is named Trust-minimized, and P01's naming conclusion is superseded.**
>
> **Superseded:** the two places where this proposal concludes that "Independently verifiable" is
> already the correct name for Tier 3 (the *What replaces it* paragraph below, and item 3 under the
> alternative names considered). The name is **Trust-minimized**, by Owner decision 2026-08-28,
> ratified with the working group.
>
> **Why the naming conclusion does not carry, even though the finding does.** A tier name in a
> published standard is a procurement term as well as a description. "Independently verifiable" is
> claimable by an independent verification organisation, and any Tier 2 operator can truthfully say <!--aais-allow-->
> they have an independent auditor. A name that a Tier 2 system can claim cannot mark the binary
> threshold. That is a different test from the one this proposal applies, and it is the one that
> governs the published name.
>
> **What is not superseded, and is adopted.** The central finding stands and is now reflected in the
> chapter: every mechanism this standard admits leaves a non-empty residual trust set; two
> deployments in different mechanism families can be incomparable; and no ranking metric survives.
> C8's Tier 3 cell now enumerates the parties a Tier 3 claim still depends on rather than asserting
> that the trusted party is removed, and the chapter's open-items box carries the finding. P2, P3 and
> P4 are the substance of that change. The disclosure obligation is the part of this proposal that
> should land as normative text.
>
> **The tension this leaves, stated rather than hidden.** "Trust-minimized" is a name, not a claim
> that trust is rankable or removed, and read as a claim it would assert the thing this research
> refutes. C8 therefore states the residual trust set in the same table cell as the name, so the two
> are read together. Anyone proposing to lean on the name as an argument should read this proposal
> first.
>
> Ratifying the disclosure requirement, including the proposed 8.1.9, remains open working-group
> business. Nothing in this note closes it.

---

## The central finding

**Tier 3 does not eliminate trust.** Every mechanism the standard admits leaves a non-empty residual trust set; the sets of two deployments in different mechanism families can be incomparable under set inclusion; and no candidate ranking metric survives (cardinality equates one opaque silicon vendor with ten transparent witnesses; collusion cost is adversary-relative; set inclusion does not hold) — research §6.1. The ladder conflates two properties that come apart: **public verifiability** (anyone may check, with published tools) and **trust independence** (no party's honesty is essential) — research §1, P01 "Why it matters". Hardware attestation and ZK proofs buy the first and leave the second largely intact.

**What replaces it:** a residual trust *disclosure* obligation. Tiers survive as a coarse summary of *how* evidence is produced and checked, not as a claim about how much trust remains and not as a comparison between two deployments in different families. On this reading the tier name should describe public verifiability rather than trust removal. *(Superseded 2026-08-30 as to the name itself: see the Owner note above. The point about what the name should describe stands.)* It is the rationale cells and the threshold prose that assert trust removal, and those are what this proposal changes.

This is not a novel objection to the standard. The cross-model paper review already recorded it independently — `docs/reviews/paper-review-round3-crossmodel.md`, findings B1, B5, and consolidated finding 1: *"Tiers should be defined by which trust assumptions remain, distinguishing public verifiability from trust independence. This is a normative change to the standard, not a wording fix."* P01 supplies the mechanism and the measurement that review lacked. <!--aais-allow-->

## Summary of proposed changes

| # | Where | Kind | Confidence |
| :--: | --- | --- | --- |
| P1 | C8 Control Objective | Weaken a claim | Judgement `[WG-INPUT NEEDED]` |
| P2 | C8 four-tier table, "What makes it this tier", Tier 3 | Delete a false claim | Settled by measurement |
| P3 | C8 four-tier table, "Who you must trust", Tier 3 | Correct an incomplete list | Settled by measurement |
| P4 | C8 binary-threshold paragraph | Weaken an implicature | Defect settled; wording judgement |
| P5 | C8 authenticated-documentation vs. cryptographic-evidence table, right cell | Correct a false claim | Settled by measurement |
| P6 | C8.1.2 | Add parties; refine the cap test | Clause (a) settled; clause (b) `[WG-INPUT NEEDED]` |
| P7 | C8.1.7 | Add anchoring's ingested assumptions | Settled by measurement |
| P8 | New C8.1.9 + C8.1 auditor evidence | Add a requirement | Judgement, low-risk |
| P9 | C8.3 prose | Delete the word "trustless" | Editor's fix |
| P10 | New C10.2.3 + auditor evidence | Add a requirement (detection latency) | Settled by measurement; Level is a judgement |
| P11 | New C10.2.4 + auditor evidence | Add a requirement (shared dependencies) | Settled by measurement; Level is a judgement |
| P12 | C7.4.1 | Extend to composition | Settled by measurement |

---

# P1 — C8 Control Objective

**Where:** `0x10-C08-Verifiability-Tiers.md`, "## Control Objective", first paragraph.

**Current text**

> Grade every piece of evidence by how independently it can be verified — that is, how much you must trust to believe it — and draw the yes-or-no line that makes the category procurable. Verifiability is a four-tier scale, not a spectrum and not a maturity model. A system has Proof-of-Control when, and only when, its evidence reaches Tier 3 or Tier 4.

**Proposed text**

> Grade every piece of evidence by how independently it can be verified — that is, by who must be trusted to believe it and whether their dishonesty would ever become publicly visible — and draw the yes-or-no line that makes the category procurable. Verifiability is a four-tier scale, not a spectrum and not a maturity model. A system has Proof-of-Control when, and only when, its evidence reaches Tier 3 or Tier 4.
>
> The Tier is a summary of how evidence is produced and checked. It is not a measure of how much trust remains: **every mechanism this standard admits leaves a residual trust set, at every Tier**, and two deployments in different mechanism families may have residual trust sets that cannot be ranked against each other at all. What must be trusted is carried by the trust-assumption disclosure ([C10.2](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md)), not by the Tier number. A higher Tier says the evidence is checkable by more parties with less privilege; it does not say fewer parties are trusted, and a Tier never licenses a comparison of two systems' trust assumptions.

**Why:** the phrase "how much you must trust" presupposes a scalar quantity that orders deployments. Research §6.1 shows every candidate metric fails, and `parallax` measured two unordered pairs among four examples — Σ₁/Σ₃ and Σ₂/Σ₄ (`parallax-outcomes.md`, amendment 3) — so the ordering is not merely unproven but has counterexamples. The rest of the paragraph, including the binary threshold and the Tier-3-or-4 rule for Proof-of-Control, is untouched: nothing in the research refutes the existence of a meaningful line, only the claim that positions above it are trust-free or mutually comparable.

**Confidence:** the *defect* is settled — the current clause states a total order that has counterexamples. The *replacement* demotes the Tier from primary claim to summary, which is a positioning decision for the chapter and for the glossary entries that inherit it. `[WG-INPUT NEEDED]`, and it belongs with [Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md) issue 6.

---

# P2 — the four-tier table, "What makes it this tier", Tier 3

**Where:** `0x10-C08-Verifiability-Tiers.md`, "## The Four Tiers" table, row **What makes it this tier**.

**Current text** (whole row, verbatim)

> `| **What makes it this tier** | Their word | A third party vouches | The trusted party is removed | Enforcement is built in; it cannot run if integrity breaks |`

**Proposed text**

> `| **What makes it this tier** | Their word | A third party vouches | The evidence is produced by the mechanism and checkable by anyone with published tools; the parties that remain essential are disclosed, not removed | Enforcement is built in; it cannot run if integrity breaks |`

**Why:** "The trusted party is removed" is the sentence the research refutes, and it is the only cell in the table that asserts trust removal. A Tier 3 Intel TDX deployment retains a five-party residual trust set — silicon vendor, provisioning/collateral service, quoting enclave, cloud operator, reference-value publisher — derived mechanically from the deployment description rather than assumed (research §5.1; `parallax-outcomes.md`, "What the implementation confirmed"). A Tier 3 ZK rollup retains ceremony, compiler, constraint auditor and settlement layer (research §5.1). Note in particular that **the cloud operator remains essential under TDX** via measurement injection at boot, so even the narrower reading "the *operator* is removed" is false for the standard's own flagship Tier 3 example. What survives is exactly the distinction research §1 draws: Tier 3 delivers public verifiability, not trust independence.

**Confidence:** **settled by measurement.** One counterexample suffices to refute a universal claim, and there are two disjoint ones. The replacement wording is drafting; the deletion is not optional.

---

# P3 — the four-tier table, "Who you must trust", Tier 3

**Where:** same table, row **Who you must trust**.

**Current text** (whole row, verbatim)

> `| **Who you must trust** | The operator | A third party, or the root-keeper | The cryptographic mechanism (mathematical or distributed assumptions) | The network protocol or continuous mathematical constraints |`

**Proposed text**

> `| **Who you must trust** | The operator | A third party, or the root-keeper | The mechanism's soundness, and the parties its soundness depends on — silicon vendor, provisioning and collateral service, reference-value publisher, setup ceremony, circuit or firmware toolchain, log operator, settlement layer — as enumerated in the disclosure | The network protocol or continuous mathematical constraints |`

**Why:** "the cryptographic mechanism" names an abstraction, not a party, and reading it as the complete answer is what makes the Tier 3 column look trust-free. Every element added above appeared in a computed residual trust set for a Tier 3 mechanism (research §5.1, Σ₂ and Σ₄). Two are additions the standard nowhere names today and that appeared in *every* hardware and ZK manifest: the **reference-value publisher** and the **build/circuit toolchain** — and they are the pair the hybrid finding turns on (research §5.2; `parallax-outcomes.md`).

**Confidence:** **settled by measurement** for the membership of the list. Whether a table cell is the right place for a seven-item list, versus a pointer to C10.2, is drafting.

---

# P4 — the binary-threshold paragraph

**Where:** `0x10-C08-Verifiability-Tiers.md`, paragraph immediately below the four-tier table.

**Current text**

> The binary threshold falls between Tier 2 and Tier 3: below it, authenticated documentation (you still trust a party); above it, evidence produced by the mechanism itself. Below the line sit compliance frameworks, audit processes, contractual assurances, traditional security controls, and any cryptographic record whose integrity still depends on trusting a party — all valuable, none of them Proof-of-Control.

**Proposed text**

> The binary threshold falls between Tier 2 and Tier 3: below it, authenticated documentation, whose integrity rests on a party the operator selects and whose dishonesty leaves no public trace; above it, evidence produced by the mechanism itself, checkable with published tools by parties the operator does not select. Above the line you still trust parties — the disclosure names them — but they are not the party making the claim, and the evidence does not require their cooperation to check. Below the line sit compliance frameworks, audit processes, contractual assurances, traditional security controls, and any cryptographic record whose integrity still depends on trusting the party that produced it — all valuable, none of them Proof-of-Control.

**Why:** the parenthetical "(you still trust a party)" as the distinguishing feature of the *below* case implies the *above* case trusts no party. Research §1 and §6.1 refute that, and P2's evidence is the same evidence. The proposed text preserves the threshold and relocates its defining test onto two properties the research supports and that `parallax` computes: **who selects the trusted party** and **whether their dishonesty is publicly detectable**. Note the last clause's small tightening — "trusting a party" to "trusting the party that produced it" — without which the sentence, read literally after this correction, would put Tier 3 below the line too.

**Confidence:** the defect is **settled by measurement**; the two-property restatement of the threshold is a **judgement call** that goes to the heart of [Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md) issue 6 question 1 ("Is the defining test for the Tier-2-to-Tier-3 line — *no single trusted party* (not the operator, and not a third-party root of trust such as a certificate authority, a chip vendor, or a trusted setup) — the correct one, or is a more precise formulation needed?"). `[WG-INPUT NEEDED]`. The research's answer to that question is: **no, and here is a counterexample** — but the replacement test is the working group's to ratify, and it should be ratified alongside the cryptography review under issue 6.

---

# P5 — the authenticated-documentation vs. cryptographic-evidence table

**Where:** `0x10-C08-Verifiability-Tiers.md`, the two-column table below the threshold paragraph, right-hand cell.

**Current text** (right cell, verbatim)

> The cryptographic mechanism generates evidence as a byproduct of execution itself — a ZK proof, a TEE attestation report, a consensus timestamp, a verifiable computation proof. Trust required: the cryptographic mechanism is sound.

**Proposed text**

> The cryptographic mechanism generates evidence as a byproduct of execution itself — a ZK proof, a TEE attestation report, a consensus timestamp, a verifiable computation proof. Trust required: the mechanism is sound **and** the parties its soundness rests on behave as assumed — for a TEE report, the silicon vendor, its provisioning service, the quoting enclave, the host that measures firmware, and whoever publishes the reference values; for a ZK proof, the setup ceremony, the circuit compiler, whoever established that the constraints are complete, and the settlement layer the proof is checked on. These are enumerated per claim in the trust-assumption disclosure ([C10.2](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md)).

**Why:** "Trust required: the cryptographic mechanism is sound" is the compressed form of the Tier 3 error and sits directly opposite a left cell that correctly names its trusted party. The two example lists are the computed sets for Σ₂ and Σ₄ (research §5.1), reproduced by the tool from the deployment descriptions.

**Confidence:** **settled by measurement.**

---

# P6 — C8.1.2, the trust analysis and the Tier-2 cap

**Where:** `0x10-C08-Verifiability-Tiers.md`, requirement **8.1.2**.

**Current text**

> `| **8.1.2** | **Verify that** each claim's register entry includes a written trust analysis naming every party that must be trusted for the evidence to hold (operator, signer, CA, chip vendor, ceremony participants), and that the assigned Tier is consistent with that list — any single trusted party caps the claim at Tier 2. | 1 |`

**Proposed text**

> `| **8.1.2** | **Verify that** each claim's register entry includes a written trust analysis naming every party that must be trusted for the evidence to hold (operator, signer, CA, chip vendor, provisioning or collateral service, reference-value publisher, build or circuit toolchain, ceremony participants), and that the assigned Tier is consistent with that list — a claim is capped at Tier 2 where any named party is one the operator selects, contracts, or controls, or where a single named party's dishonesty would defeat the evidence with no publicly detectable trace. | 1 |`

**Why — clause (a), the parenthetical.** The **reference-value publisher** and the **build or circuit toolchain** appear in every computed Tier 3 manifest and are absent from the standard's list. They are also the two the hybrid finding turns on: a TEE-plus-ZK design marketed as defence in depth shared both across its layers, so one build-pipeline compromise corrupts the MRTD baseline and the circuit constraints at once (research §5.2; confirmed by tool with a negative control, `parallax-outcomes.md`). A trust analysis that omits them cannot surface that.

**Why — clause (b), the cap.** "Any single trusted party caps the claim at Tier 2" is unsatisfiable above Tier 2 as literally written, because **every** deployment the calculus was run on has a non-empty residual trust set, Tier 3 examples included (research §3, §5.1). Read strictly, no claim could ever be registered above Tier 2; read as intended, the requirement is silently doing work the text does not state. The proposed replacement makes the intended test explicit using the two discriminators the research supports and `parallax` computes: **operator selection** (which is what actually separates authenticated documentation from mechanism-generated evidence) and **detection latency** (the asymmetry the tool measured — exactly one of TDX's five assumptions is checked on a schedule; four are silent and permanent).

**Confidence:** clause (a) is **settled by measurement**. Clause (b): the defect is settled — the current test is unsatisfiable as written — but the replacement is a **judgement call** and the same call as P4. `[WG-INPUT NEEDED]`, tied to issue 6. Do not apply clause (b) without P4; applied separately they will drift apart.

---

# P7 — C8.1.7, anchoring

**Where:** `0x10-C08-Verifiability-Tiers.md`, requirement **8.1.7**.

**Current text**

> `| **8.1.7** | **Verify that** claims resting on a vendor-rooted attestation service are either registered at Tier 2, or composed with independent anchoring (e.g., attestation reports committed to a public transparency log with independent monitors) before being registered at Tier 3 — with the vendor trust assumption on the disclosure in both cases. | 3 |`

**Proposed text**

> `| **8.1.7** | **Verify that** claims resting on a vendor-rooted attestation service are either registered at Tier 2, or composed with independent anchoring (e.g., attestation reports committed to a public transparency log with independent monitors) before being registered at Tier 3 — with the vendor trust assumption on the disclosure in both cases, and, where anchoring is used, the assumptions the anchor itself introduces on the disclosure alongside it: log-operator non-equivocation with its detection window, and, where the anchor is a ledger, that ledger's consensus execution fidelity. | 3 |`

**Why:** anchoring is presented in the current text as the step that lifts a vendor-rooted claim to Tier 3, and the requirement is already honest that the vendor assumption survives. What it does not say is that anchoring is **a trade, not a pure gain**: it converts log-operator trust into a bounded detection window *and silently ingests a consensus-execution-fidelity assumption*, both of which the tool showed appearing in the manifest (`parallax-outcomes.md`, "What the implementation confirmed"; research §5.2, "Settlement Layer Dependency Ingestion"). A deep reorganization rolls back published attestation evidence. Anchoring also removes **none** of the five TDX assumptions — it makes the *history* publicly auditable while the *measurement* still rests on the same chain.

**Confidence:** **settled by measurement.** This is an addition to a disclosure obligation the requirement already imposes, not a new gate, so it is also the lowest-risk change in this proposal.

---

# P8 — new C8.1.9, and the C8.1 auditor-evidence line

**Where:** `0x10-C08-Verifiability-Tiers.md`, C8.1 requirement table, appended after 8.1.8.

**Current text:** none — this is an addition.

**Proposed text** (new row)

> `| **8.1.9** | **Verify that** no Tier 3 or Tier 4 claim is described — in the claim register, the conformance statement, or public product claims — as removing, eliminating, or operating without trust dependencies, and that each Tier 3+ register entry instead cites the disclosure lines ([C10.2](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md)) naming the parties that remain essential. | 1 |`

**Also amend — auditor evidence.** Current text, verbatim:

> **Auditor evidence:** 8.1.1–8.1.3 — the claim register; recompute the tier for three sampled claims from their trust analyses. 8.1.4 — claims-review sign-off vs. current public claim text. 8.1.5 — the recorded independent verification run; repeat it yourself. 8.1.6 — register entries for after-the-fact mechanisms. 8.1.7 — anchoring configuration and a validated anchor proof. 8.1.8 — locate, install, and run the published verifier as an outsider. <!--aais-allow-->

Proposed replacement:

> **Auditor evidence:** 8.1.1–8.1.3 — the claim register; recompute the tier for three sampled claims from their trust analyses. 8.1.4 — claims-review sign-off vs. current public claim text. 8.1.5 — the recorded independent verification run; repeat it yourself. 8.1.6 — register entries for after-the-fact mechanisms. 8.1.7 — anchoring configuration and a validated anchor proof; confirm the log-operator and settlement-layer assumptions appear on the disclosure. 8.1.8 — locate, install, and run the published verifier as an outsider. 8.1.9 — search the register, the statement and the public claim text for "trustless", "no trusted party", "zero trust assumptions" and equivalents; any hit against a Tier 3+ claim is a finding. Follow one Tier 3+ entry to its disclosure lines and confirm they exist. <!--aais-allow-->

**Why:** P2–P5 remove the trust-elimination claim from the standard's own prose. 8.1.9 stops implementers from re-introducing it in theirs, which is the failure mode with commercial consequences — research §1 identifies "trustless" marketing as the field-wide problem, and P01 notes the same conflation runs through confidential-computing and ZK product claims generally. It is modelled directly on **8.1.4**, which already polices the phrase "Proof-of-Control" at Level 1 by the same method, so it adds a check to an existing review rather than a new process.

**Confidence:** **judgement call**, though a low-risk one. The research settles that the claim being prohibited is false; whether the standard should police implementers' vocabulary a second time is an editorial policy question, and 8.1.4 is the precedent that says yes.

---

# P9 — C8.3 section prose

**Where:** `0x10-C08-Verifiability-Tiers.md`, "## C8.3 Chain Integrity and Self-Enforcement (Tier 4)", introductory paragraph.

**Current text**

> Tier 4 is where verification is continuous and built into operation: the system produces trustless evidence as it runs and cannot operate unless its integrity holds. A component may operate at a lower tier internally — a proprietary model or a piece of silicon can sit at Tier 1 or 2 on its own — as long as its *interactions* with other systems meet Proof-of-Control.

**Proposed text**

> Tier 4 is where verification is continuous and built into operation: the system produces mechanism-generated evidence as it runs and cannot operate unless its integrity holds. Tier 4 constrains *when* evidence is checked and what happens when the check fails; like Tier 3, it leaves a residual trust set, which the disclosure carries. A component may operate at a lower tier internally — a proprietary model or a piece of silicon can sit at Tier 1 or 2 on its own — as long as its *interactions* with other systems meet Proof-of-Control.

**Why:** "trustless" is the exact word the research refutes, and it is the only occurrence in the normative text of the standard (the other hits are in review documents quoting the paper). Self-enforcement is a property of *enforcement timing* — the system halts without a valid proof — and is orthogonal to how many parties are trusted; a Tier 4 system gating on a Groth16 proof still trusts the ceremony. The added sentence prevents the reader from inferring that the Tier 4 rung completes a progression toward trustlessness.

**Confidence:** the word deletion is an **editor's fix** — settled, and it should be applied regardless of what happens to the rest of this proposal. The added sentence is drafting.

---

# P10 — new C10.2.3, detection latency

**Where:** `0x10-C10-Conformance-and-Disclosure.md`, C10.2 requirement table, appended after 10.2.2.

**Current text:** none — this is an addition.

**Proposed text** (new row)

> `| **10.2.3** | **Verify that** each disclosed assumption records a detection latency — the maximum time between a breach of the assumption and the appearance of evidence of that breach that a relying party could check — stated either as a bounded interval together with the mechanism that bounds it (collateral refresh, log anchoring period, gossip convergence, audit cycle), or explicitly as undetectable where no such mechanism exists. | 2 |`

**Also amend — auditor evidence.** Current text, verbatim:

> **Auditor evidence:** 10.2.1 — reconcile the disclosure against the mechanism list; any mechanism without a disclosure line is a finding. 10.2.2 — category tags present and drawn from the defined set.

Proposed replacement:

> **Auditor evidence:** 10.2.1 — reconcile the disclosure against the mechanism list; any mechanism without a disclosure line is a finding. 10.2.2 — category tags present and drawn from the defined set. 10.2.3 — for one bounded assumption, check the stated interval against the configured refresh or anchoring period in the running system; for one assumption marked undetectable, confirm no monitor is claimed for it elsewhere in the statement.

**Why:** this is P01's central empirical claim and the one `parallax` confirmed most directly. On the standard's flagship Tier 3 mechanism, **exactly one of the five residual assumptions has a bounded detection latency (the collateral service, ~12 h); the other four are silent and permanent** (`parallax-outcomes.md`, "What the implementation confirmed"; research §5.1, P01's fourth column). That asymmetry is invisible in the disclosure as C10.2 stands today, and it is the single most decision-relevant fact in it: the C10.2 example table's "Healthcare AI agent on Azure" row currently reads *"Hardware supply-chain risk; single-vendor trust dependency, mitigated by Azure's controls and Intel's attestation"*, which describes as mitigated a set of assumptions four-fifths of which have no detection mechanism at all. Latency is also the one quantity in the calculus that is genuinely computable from a deployment description and comparable across implementations without ranking them.

**Confidence:** **settled by measurement** that the quantity exists, is derivable, and varies materially within a single mechanism's trust set. The **Level 2 assignment is a judgement call** — an argument exists for Level 1 (it is a field on a Level 1 disclosure) and for Level 3 (it is what a Tier 3 claim's honesty rests on). `[WG-INPUT NEEDED]` on the Level only. Note also that this proposal does **not** ask for latency to be aggregated into a per-claim figure or used to order claims; see "What I do not propose" below.

---

# P11 — new C10.2.4, shared dependencies across mechanisms

**Where:** `0x10-C10-Conformance-and-Disclosure.md`, C10.2 requirement table, appended after P10's 10.2.3.

**Current text:** none — this is an addition. It qualifies **10.2.1**, whose current text is:

> `| **10.2.1** | **Verify that** the disclosure lists, per claim, each residual trust assumption with the assumption's subject (named vendor, hardware element, mathematical assumption, or ceremony) — matched one-to-one against the mechanisms in the claim register. | 1 |`

**Proposed text** (new row; 10.2.1 unchanged)

> `| **10.2.4** | **Verify that** where a claim rests on two or more mechanisms, any party or component both depend on is disclosed once and marked as shared, naming the mechanisms it is shared by — so that a layered design is not presented as independent layers when one party's failure defeats all of them. | 2 |` <!--aais-allow-->

**Also amend — auditor evidence.** Append to the line as amended by P10:

> 10.2.4 — for one claim using two or more mechanisms, list each mechanism's assumed parties separately and intersect them; any principal in the intersection that is not marked shared is a finding.

**Why:** 10.2.1's "matched one-to-one against the mechanisms" is a per-mechanism reconciliation, and it is exactly the shape that hides the finding `parallax` was built to produce. A hybrid TEE-plus-ZK design, marketed as defence in depth, was found to share an upstream build pipeline and reference-value provider across both layers: one compromise corrupts the MRTD baseline and the circuit constraints simultaneously, and no party had noticed (research §5.2; reproduced by the tool with an independent-pipelines negative control that correctly reports nothing, `parallax-outcomes.md`). Under 10.2.1 alone, such a design produces two tidy per-mechanism disclosure blocks, both complete, with the shared party appearing in each and the sharing appearing nowhere.

**Confidence:** **settled by measurement**, including the negative control — the strongest single result in the evidence base, and the one that most clearly could not have been reached by reading. The Level assignment is a judgement call; Level 2 matches 10.2.2's machine-comparability rung.

---

# P12 — C7.4.1, the transparent property

**Where:** `0x10-C07-Evidence-Generation-and-Properties.md`, requirement **7.4.1**.

**Current text**

> `| **7.4.1** | **Verify that** the published trust-assumption disclosure ([C10.2](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md)) lists, for each evidence mechanism in use, every party, hardware element, and mathematical assumption that must hold for the evidence to be believed. | 1 |`

**Proposed text**

> `| **7.4.1** | **Verify that** the published trust-assumption disclosure ([C10.2](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md)) lists, for each evidence mechanism in use and for the composition of mechanisms where more than one is used, every party, hardware element, software toolchain, and mathematical assumption that must hold for the evidence to be believed — including assumptions introduced by anchoring or composition rather than by any single mechanism. | 1 |`

**Also note (no change proposed):** the C7.4 section sentence *"Enterprises, insurers, and regulators can see exactly what must still be trusted"* is correct as written and is, in fact, the property the whole of this proposal is trying to make true. It needs no edit.

**Why:** two gaps, both measured. (i) "for each evidence mechanism in use" is per-mechanism and therefore cannot express an assumption that belongs to the *composition* — the shared build pipeline (research §5.2) and the settlement-layer fidelity that anchoring ingests (research §5.2, `parallax-outcomes.md`) are both of that kind. (ii) "party, hardware element, and mathematical assumption" has no slot for a **software toolchain**, yet the compiler or circuit arithmetizer appears in every ZK manifest and the build pipeline in every hybrid one (research §3.2 ZK rule, §5.1 Σ₄).

**Confidence:** **settled by measurement.** This is the minimal edit that makes C7.4 able to state what C10.2 will now be required to disclose; it is the enabling change for P11 and should travel with it.

---

# What I do **not** propose changing, and why

Being explicit about this matters more than the changes above, because the research doc's own §7 over-reaches in four places, and because two things the working group might expect to be under attack are in fact strengthened by this research.

**1. The binary threshold stays.** The research refutes a *total order over tiers*; it does not refute the existence of a meaningful line between evidence whose integrity rests on its producer and evidence produced by the mechanism. Both `parallax`-measured unordered pairs (Σ₁/Σ₃, Σ₂/Σ₄) are pairs of *different mechanism families*, which is precisely where the standard's own text does not claim an ordering is decision-relevant. **Do not read this proposal as an argument to abolish the threshold**; issue 6 remains open on its own terms.

**2. C8.1.5, 8.1.6 and 8.1.8 are unchanged and, if anything, vindicated.** These are the public-verifiability requirements — the recorded outsider verification run, the after-the-fact-checkability rule, the published, NDA-free verifier. Research §1 splits public verifiability from trust independence and finds that **public verifiability is the real property Tier 3 delivers**. These three requirements are the ones that test for it. They should be treated as the essential content of Tier 3 once the trust-removal claim is deleted, not weakened alongside it.

**3. C8.2 (Mechanism-to-Requirement Fit) is untouched.** Research §7.1 is headed *"Textual Revisions for C8.1–C8.3"* and proposes "C8.2 (Tier 3 Revision)" — but **C8.2 in the actual standard is Mechanism-to-Requirement Fit and has nothing to do with Tier 3.** §7.1 assumes C8.1/C8.2/C8.3 map onto tiers 1-2/3/4, which they do not. That mis-mapping invalidates §7.1 as a set of instructions; the findings underneath it are sound and are carried above, re-targeted at the sections that actually make the claims. Nothing in the research bears on 8.2.1 or 8.2.2.

**4. C8.3.1–8.3.5 are untouched.** The research says nothing about interaction inventories, proof-gated halts, availability analysis, or far-end enforcement. Only the word "trustless" in the section's prose is in scope (P9).

**5. I reject the research's proposed tier renames.** Research §7.1 and P01's "Consequence for the standard" propose renaming Tiers 1–2 to *Unmonitored / Unbounded-Latency Attestation*, Tier 3 to *Publicly Verifiable / Hardware-Anchored Attestation*, and Tier 4 to *Multi-Domain Bounded-Detection Attestation*. Three objections, and the third is fatal:
   * "Hardware-Anchored" over-fits to the TDX example. Σ₄, a ZK rollup, is a Tier 3 mechanism with no hardware anchor at all. The name should describe what the research says Tier 3 actually is. *(Superseded 2026-08-30: the name is Trust-minimized. See the Owner note near the top.)*
   * Merging Tiers 1 and 2 into one latency-defined rung discards the operator's-word / third-party-vouches distinction, which is information a relying party uses and which the research nowhere criticizes.
   * **The research's own data refutes its latency-based ordering.** Every one of Σ₁–Σ₄ contains at least one assumption with unbounded detection latency (research §5.1: Σ₁ all ∞; Σ₂ four ∞; Σ₃ non-collusion ∞; Σ₄ three ∞). Order the four by worst-case Δ and they tie at ∞. A latency-ordered ladder collapses on the very examples offered to justify it. Detection latency is worth **disclosing per assumption** (P10); it is not a ranking metric, and P01's suggestion that "tiers become ordered by detection latency and domain diversity" should be dropped from the paper as well as from the standard.

**6. I do not propose making the Residual Trust Manifest schema normative.** Research §7.2 gives a concrete JSON-LD schema for C7.4/C10.2. It is a good starting point and matches the fields P10 and P11 require, but it has been exercised on five self-authored deployments by one author, with no independent encoder and no real-world system (`parallax-outcomes.md`, amendment 4). Standardizing a wire format on that basis would be premature. **Recommendation:** submit research §7.2 as a candidate to the working group under [Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md) **issue 7** (the standardized disclosure format, currently undefined), where it can sit alongside Bob Blessing-Hartley's mechanism-by-trust-category matrix and the draft category set. `[WG-INPUT NEEDED]`. Note that the six draft categories (Hardware, Mathematical, Ceremony, Vendor, Implementation, Distributed) have no slot for a **toolchain/reference-value** assumption, which the measurements say is the most commonly shared one — that is a concrete input to issue 7 independent of whether the schema is adopted.

**7. I do not propose the research's new obligation "C10.3 (Automated Trust Evaluation)", and the id is already taken.** Research §7.3 and P01 propose that verifier software accept a local trust policy and mechanically reject a manifest exceeding it. Two problems:
   * **Id collision.** C10.3 in the standard is *Continuously Monitored Operation* (10.3.1–10.3.7). Any adoption would need a fresh id — C10.4 — and the research text must not be carried over word for word.
   * **The evidence is thin, and what exists is a cautionary tale.** A policy-evaluation implementation exists in `parallax`, and one of the five Critical findings against it was `Policy` without `deny_unknown_fields`: *"a one-letter typo silently disabling the gate; `check` exits 0"* (`parallax-outcomes.md`). A trust-policy gate that fails open is worse than no gate, and that is what a first implementation produced. If the working group takes this up, the requirement should carry the mitigation the tool ended up with — **reject unknown keys in the policy surface** — as normative text, not as advice.
   `[WG-INPUT NEEDED]`. My recommendation is to defer it until a manifest format exists (issue 7) and at least one manifest has been produced by someone other than its author.

---

# Knock-on edits implied but not drafted here

Listed for completeness; each quotes text that P1–P12 would make inconsistent, and none is drafted because they sit outside the three target files.

* **`0x90-Appendix-A_Glossary.md`, "Proof-of-Control"** — *"like a public notary for your agents' actions, except no one has to trust the notary."* This is the plain-language form of the claim P2 deletes. It is the most publicly visible sentence in the standard carrying it.
* **`0x90-Appendix-A_Glossary.md`, "Verifiability Tiers" and "Open Verification"** — both define the scale as grading *"how much you must trust to believe it"*; they inherit P1 directly. "Open Verification" additionally asserts *"Verification is open when what you must trust is a mechanism anyone can verify rather than a party"*, which P2's evidence contradicts as stated.
* **`0x93-Appendix-D_Open-Issues.md`, issue 6** — should record P01's answer to question 1 (the *no single trusted party* test has counterexamples and is unsatisfiable as literally written) and add a third question: what the tier ladder claims about two deployments in different mechanism families, given measured unordered pairs.
* **`mappings/confidential-computing.md`** — carries the Tier-2 caveat for vendor-rooted attestation and is the natural home for P7's anchoring-ingests-assumptions point.
* **`0x10-C10-Conformance-and-Disclosure.md`, the C10.2 example table** — the Azure/TDX row describes as *"mitigated by Azure's controls and Intel's attestation"* a set of assumptions four of five of which have no detection mechanism; and the cross-border ZK-STARK row's *"Trusts collision-resistant hash functions only"* omits the circuit toolchain and constraint-completeness assumptions that research §3.2's ZK rule attaches to every proof system. Illustrative, not normative, but it is where readers will look first.

# Incidental, non-normative

The four-tier table in C8 has a malformed header: the header row carries four cells (`| **Assertion — Tier 1** | … | **Self-enforcing — Tier 4** |`) while the separator row carries five and every body row carries five (a row label plus four). The header is missing its leading empty label cell. P2 and P3 rewrite body rows of this table and would inherit the defect; worth fixing in the same pass, but it is a rendering bug, not a normative change.
