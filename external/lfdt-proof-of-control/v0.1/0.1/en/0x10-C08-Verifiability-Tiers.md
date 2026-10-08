# C8 Verifiability Tiers and the Binary Threshold

## Control Objective

Grade every piece of evidence by how independently it can be verified — that is, by who must be trusted to believe it and whether their dishonesty would ever become publicly visible — and draw the yes-or-no line that makes the category procurable. Verifiability is a four-tier scale, not a spectrum and not a maturity model. A system has Proof-of-Control when, and only when, its evidence reaches Tier 3 or Tier 4.

> **[DRAFT] — actively in progress.** This chapter is being worked on with the working group.

> **[WG-INPUT NEEDED] — open items on the Tiers.**
> 1. **Tier 2's name and definition** — reconciliation in progress (Patrick, Mostafa).
> 2. **Tier 4 and human authority** — does the required human authorization belong in the Tier 4 root-of-trust cell?
> 3. **The Tier 1 evidence floor** — does Tier 1 require a timestamped, attributed log, or stay pure assertion?
> 4. **"Every execution interval"** — a canonical definition is needed: per action, per clock tick, or per state transition.
> 5. **Key revocation and enforcement-point tamper-evidence at Tier 4** — missing by acknowledgment.
> 6. **Adoption weight** — is conformance light enough to adopt, and does it map to cyber-insurance underwriting?
> 7. **Cross-jurisdictional accountability at Tier 4** — needs a mechanism or softer language.
> 8. **The binary threshold** is the standard's most consequential definition and its most-scrutinized point. It needs dedicated cryptography and blockchain review before ratification, coordinated through [Appendix D](0x93-Appendix-D_Open-Issues.md) issue 6.
>
> **Tier 3's name is settled.** It is *Trust-minimized*, by Owner decision 2026-08-28. The retired candidate "Independently verifiable" was dropped because an independent verification organisation can claim it, and any Tier 2 operator can claim they have an independent auditor.

> **[WG-INPUT NEEDED] — the Tier is a summary, not a measure of remaining trust.**
> P01's trust calculus establishes that **every mechanism this standard admits leaves a
> residual trust set, at every Tier**, and that two deployments in different mechanism
> families may have residual trust sets that cannot be ranked against each other at all.
> The cells asserting that Tier 3 removes the trusted party have been corrected below,
> because a universal claim with counterexamples is simply false. What has **not** been
> decided is the framing that replaces it: whether the Tier is demoted from the primary
> claim to a coarse summary, with what must be trusted carried by the trust-assumption
> disclosure ([C10.2](0x10-C10-Conformance-and-Disclosure.md)) instead; and whether the
> Tier-2/Tier-3 test is restated as **who selects the trusted party** and **whether their
> dishonesty is publicly detectable**. Both belong with
> [Appendix D](0x93-Appendix-D_Open-Issues.md) issue 6, question 1, and should be ratified
> alongside the cryptography review rather than taken as an editorial fix.
>
> The evidence base is five self-authored deployment descriptions and no real-world
> system. That is enough to refute a universal claim — one counterexample does it, and
> there are two disjoint ones — and it is not enough to install a new ordering or a new
> taxonomy.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../images/diagrams/tier-ladder-dark.svg">
    <img alt="The four Verifiability Tiers with the binary threshold between Tier 2 and Tier 3: below it authenticated documentation, above it mechanism-generated evidence" src="../../images/diagrams/tier-ladder-light.svg" width="720">
  </picture>
</p>

## The Four Tiers

*Tiers 1 and 2 mean you trust a party. Tiers 3 and 4 are open verification, and where Proof-of-Control begins.*

| | **Tier 1 · Assertion** *(their word)* | **Tier 2 · Attestation** *(a third party vouches)* | **Tier 3 · Trust-minimized** *(anyone can verify)* | **Tier 4 · Self-enforcing** *(it cannot run otherwise)* |
| --- | --- | --- | --- | --- |
| **Who you must trust** | The operator | A third party or qualified auditor | The mechanism's soundness, and the parties its soundness depends on: silicon vendor, provisioning and collateral service, reference-value publisher, setup ceremony, circuit or firmware toolchain, log operator, settlement layer, as enumerated in the disclosure | The protocol itself: continuous constraints, anchored in external hardware roots of trust |
| **How it is verified** | Not verified; asserted | An auditor verifies, with privileged access | Anyone can verify, no privileged access | Execution is gated by cryptographic proofs; verification is continuous and automated |
| **When it is verified** | Never, or only when questioned | After the fact, sampled | After the fact, but by anyone | Before every execution interval: no proof, no write |
| **What happens on integrity break** | Nothing, the system runs regardless | Detected in audit, after the fact | Detected by anyone, and the system can still run | MUST NOT execute until the integrity condition holds again |
| **Accountability** | Operator, self-attested | Named human and institution, bound to policy | The same authority, externally verifiable without trusting the operator or their auditors | An accountable person whose authorization is un-bypassable |

**Proof-of-Control begins at Tier 3.** Below that line a party still vouches for the evidence; above it, nobody vouches for it: anyone can verify it directly, and the parties its soundness rests on are named in the disclosure. That is the difference between third-party verification and open verification: a certifier attesting to your conformance is Tier 2, because you still have to trust the certifier, while at Tier 3 and above anyone can verify the evidence without trusting the operator or their certifier.

**Tiers 1 and 2 are human verification; Tiers 3 and 4 are mechanical.** Someone asserts, or a party attests. Above the line, verification is binary and cryptographic and takes no human judgment. That line, human against mechanical, is the same binary threshold between Tier 2 and Tier 3, and it is why only Tiers 3 and 4 keep pace with AI-speed offense.

**The tiers grade the evidence, not the controls.** They measure how independently control adherence can be verified. They do not measure whether the controls were adequate. A Tier 4 system can have poorly chosen controls that are still perfectly enforced.

**Residual trust must be disclosed.** All systems at Tier 3 and Tier 4 MUST document their residual mathematical, hardware, or distributed trust assumptions in the standardized disclosure format ([C10.2](0x10-C10-Conformance-and-Disclosure.md)).

**Chain integrity.** Where a use case requires Tier 4, every system in the interaction chain MUST attest up to Tier 4 for the interactions they share. A component MAY operate at a lower tier internally, as long as it preserves the integrity of the Tier 4 interactions. Requirements at C8.3 below.

### Cryptography is a mechanism, not a tier

A centralized Merkle tree is cryptographic and sits at Tier 2, because you still trust whoever controls the root. Cryptography counts toward Tiers 3 and 4 only when no central party vouches for the evidence. What separates Tiers 3 and 4 from Tier 2 is who must be taken at their word, not the presence of mathematics.

A cryptographic mechanism drops from Tier 4 for either of two reasons. You still have to trust a party, which puts it at Tier 2, or you can only verify it after the fact rather than it enforcing itself, which is Tier 3.

**Cryptographic, and you still trust a party (Tier 2):**

* An operator publishing a hash of its own data. It establishes that the data matches that hash, and they chose what to hash and could swap it.
* A system signing its own logs or outputs with its own key. You trust the key-holder not to lie or backdate.
* Traditional PKI: a certificate signed by a certificate authority. Trust is rooted in the CA.
* A permissioned or consortium blockchain. Cryptographic and ledger-based, and the validators are controlled.
* A zero-knowledge proof with a trusted setup run by one party. Whoever ran the setup could forge.
* A trusted execution environment attestation whose root of trust is the chip vendor's attestation service.
* A centralized or private Merkle tree. Cryptographic, and you trust whoever controls the root.

**Cryptographic and openly verifiable, and not yet Tier 4:**

* A public, append-only transparency log with independent monitors. Anyone can verify it, and it detects tampering after the fact rather than stopping the system. Tier 3.
* A public blockchain commitment anyone can verify. Openly verifiable, and point-in-time, and it does not gate operation. Tier 3.
* A zero-knowledge proof with a trustless setup, produced on demand. Anyone can verify it, and if the system can run without producing it, verification is not enforced. Tier 3.

Tier 4 is where verification is continuous and built into operation: the system produces evidence as it runs and cannot operate unless its integrity holds.

### The binary threshold

The first question the standard answers is whether a system has Proof-of-Control. That yes-or-no is the Binary evidence property, drawn on the Verifiability Tiers, and it falls at one place: the boundary between Tier 2 and Tier 3.

Below the line, at Tiers 1 and 2, the evidence is authenticated documentation. You still have to trust a party: the operator's word at Tier 1, or a signer or qualified auditor at Tier 2. A signed operator log is Tier 2. This is not Proof-of-Control. Below the line also sit compliance frameworks, audit processes, contractual assurances, and traditional security controls. All valuable, none of them Proof-of-Control.

**What the line requires:** evidence you can verify without having to trust any single party. Trusting the operator is the obvious way to fail this and it is not the only one. Trusting any designated party fails it too. A certificate you can only believe by trusting a certificate authority, or an attestation rooted in a vendor's own service, is below the line.

**Why binary matters.** The category does not exist until a buyer can ask a yes-or-no question. "Does your AI have Proof-of-Control?" is procurable. "How far along the trust-minimization spectrum is your AI?" is not. Every standard that created a category used a binary threshold.

| Authenticated documentation (Tiers 1–2, not Proof-of-Control) | Cryptographic evidence (Tiers 3–4, Proof-of-Control) |
| --- | --- |
| The system operator produces logs or records, then signs them. The signature establishes that the log has not been altered after creation; it does not establish that the log accurately reflects what happened. Trust required: that the operator produced the log faithfully. | The cryptographic mechanism generates evidence as a byproduct of execution itself: a ZK proof, a TEE attestation report, a consensus timestamp, a verifiable computation proof. Trust required: the mechanism is sound **and** the parties its soundness rests on behave as assumed. For a TEE report, the silicon vendor, its provisioning service, the quoting enclave, the host that measures firmware, and whoever publishes the reference values; for a ZK proof, the setup ceremony, the circuit compiler, whoever established that the constraints are complete, and the settlement layer the proof is verified on. These are enumerated per claim in the trust-assumption disclosure ([C10.2](0x10-C10-Conformance-and-Disclosure.md)). |

**Mechanism selection must match the control's evidentiary requirement.** A claimed control's evidence MUST actually evidence the domain it is offered for. Requirements at C8.2 below.

### What a Tier 3 claim does not give you

Tier 4 guarantees the record is whole. Because a Tier 4 gate is "no proof, no write," an action cannot execute without producing evidence, so the absence of evidence means the action did not happen.

At Tier 3, you can verify that the records you have were not tampered with, and you are not guaranteed the record is complete. An agent could act off-record. Read Tier 3 as *the evidence you can see is trustworthy*, not *you can see every action*.

---

## C8.1 Tier Placement

Placement is set by how much you must trust, not by whether cryptography is used. The worked examples are above, under *Cryptography is a mechanism, not a tier*.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **8.1.1** | **Verify that** the claim register records an assigned Tier (1–4) for every claim, with no unassigned entries. | 1 |
| **8.1.2** | **Verify that** each claim's register entry includes a written trust analysis naming every party that must be trusted for the evidence to hold (operator, signer, CA, chip vendor, ceremony participants), and that the assigned Tier is consistent with that list — any single trusted party caps the claim at Tier 2. | 1 |
| **8.1.3** | **Verify that** claims whose trust analysis names a single trusted party — operator-signed logs, single-party trusted setups, vendor-rooted attestations, centralized Merkle trees, permissioned ledgers — are registered at Tier 2 or below. | 1 |
| **8.1.4** | **Verify that** the words "Proof-of-Control" appear in the conformance statement and marketing claims only for claims registered at Tier 3 or 4, confirmed by the documented claims review. | 1 |
| **8.1.5** | **Verify that** for each Tier 3+ claim, an external party can obtain the evidence and complete verification using only published materials — demonstrated by a recorded verification run performed without operator credentials. | 3 |
| **8.1.6** | **Verify that** claims whose evidence is verifiable only after the fact — transparency logs with independent monitors, on-demand proofs the system can run without producing — are registered at Tier 3, and Tier 4 is registered only where verification gates operation. | 1 |
| **8.1.7** | **Verify that** claims resting on a vendor-rooted attestation service are either registered at Tier 2, or composed with independent anchoring (e.g., attestation reports committed to a public transparency log with independent monitors) before being registered at Tier 3 — with the vendor trust assumption on the disclosure in both cases. | 3 |
| **8.1.8** | **Verify that** the verification procedure and tooling for each Tier 3+ claim are published (public repository or equivalent), versioned, and usable without an NDA, license negotiation, or operator-issued credentials. | 3 |

**Auditor evidence:** 8.1.1–8.1.3 — the claim register; recompute the tier for three sampled claims from their trust analyses. 8.1.4 — claims-review sign-off vs. current public claim text. 8.1.5 — the recorded independent verification run; repeat it yourself. 8.1.6 — register entries for after-the-fact mechanisms. 8.1.7 — anchoring configuration and a validated anchor proof. 8.1.8 — locate, install, and run the published verifier as an outsider. <!--aais-allow-->

---

## C8.2 Mechanism-to-Requirement Fit

The rule that prevents conformance gaming: conformance judges mechanism-to-requirement fit, not just mechanism presence.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **8.2.1** | **Verify that** the claim register maps each claimed control to its mechanism and to the specific verifiable fact it evidences, using the mechanism's "what it proves" scope from [Appendix B](0x91-Appendix-B_Proof-Mechanism-Inventory.md) — and that no mapping pairs a mechanism with a domain outside that scope (e.g., an encryption control offered for the Identity domain). | 1 |
| **8.2.2** | **Verify that** the mapping distinguishes signing-time claims from runtime claims: no artifact-integrity mechanism (signature at rest) is mapped to a runtime-behavior fact, and no environment attestation is mapped to a claim about the model weights loaded into it. | 1 |

**Auditor evidence:** 8.2.1 — the control→mechanism→fact mapping; check three rows against Appendix B scopes. 8.2.2 — search the mapping for signing-time mechanisms attached to runtime facts.

---

## C8.3 Chain Integrity and Self-Enforcement (Tier 4)

Tier 4 is where verification is continuous and built into operation: the system produces evidence as it runs, verifiable without privileged access and cannot operate unless its integrity holds. A component may operate at a lower tier internally — a proprietary model or a piece of silicon can sit at Tier 1 or 2 on its own — as long as its *interactions* with other systems meet Proof-of-Control.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **8.3.1** | **Verify that** where a use case is designated Tier 4, an interaction inventory lists every system in the chain, and each listed system's shared interactions carry Tier 4 evidence — confirmed per interaction, not per system. | 4 |
| **8.3.2** | **Verify that** components operating internally below Tier 4 interact with the chain only through interfaces that produce Tier 4 evidence, per the interaction inventory. | 4 |
| **8.3.3** | **Verify that** operation is mechanically gated on proof validity: in test, invalidating the proof chain (or withholding a required proof) halts the system's in-scope actions. | 4 |
| **8.3.4** | **Verify that** the claim documents the availability impact of proof-gated operation — expected halt conditions, recovery procedure, and maximum tolerable outage — and that the recovery procedure has been exercised. | 4 |
| **8.3.5** | **Verify that** the halt is enforced outside the operator's control — for example, relying parties refuse requests lacking a valid, action-bound capability, so absence of valid evidence blocks execution at the far end rather than depending on an operator-side flag that a compromised host could disable. | 4 |

**Auditor evidence:** 8.3.1–8.3.2 — the interaction inventory; sample two interactions and validate their evidence tier. 8.3.3 — the halt test record; re-run it. 8.3.5 — the enforcement point's configuration; disable the operator-side halt in test and confirm the relying party still refuses unattested requests. 8.3.4 — the availability analysis and the recovery-exercise report.

> **[WG-INPUT NEEDED]** — the binary threshold is the standard's most consequential definition
> and its most-scrutinized point; the working group must ratify it with dedicated cryptography
> and blockchain review, including impossibility results being formalized by researchers
> coordinated by Hart Montgomery (CTO, Linux Foundation Decentralized Trust). See
> [Appendix D](0x93-Appendix-D_Open-Issues.md), issue 6.

---

## References

* [Appendix A — Glossary](0x90-Appendix-A_Glossary.md): Verifiability Tiers, Tier, binary threshold terms
* [Appendix B — Proof-Mechanism Inventory](0x91-Appendix-B_Proof-Mechanism-Inventory.md): the mechanisms that produce Tier 3–4 evidence
* [Certificate Transparency](https://certificate.transparency.dev/) — the public transparency-log pattern
* Crosswalks: [Confidential Computing](../../mappings/confidential-computing.md) (Tier-2 caveat for vendor-rooted attestation), [SOC 2](../../mappings/soc-2.md)
