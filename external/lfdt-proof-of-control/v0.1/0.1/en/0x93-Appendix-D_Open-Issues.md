# Appendix D: Open Working-Group Issues (not yet normative)

The questions below are under active working-group discussion. They are recorded here so the draft reflects the live debate, and they carry no normative force until resolved. Every open decision in the standard is marked `[WG-INPUT NEEDED]` and points here. **To weigh in, join a working group at [advancedaisociety.org](https://advancedaisociety.org/).**

## Issue 1 — Identity and Authorization Overlap

Whether identity-binding is owned by the Identity domain ([C5](0x10-C05-Identity.md)) or by Authorization ([C4](0x10-C04-Authorization.md)), with Identity as an input. (Working-group lean: Authorization owns it, Identity as an input.) The delegation-and-authority binding described in the contribution under issue 4 bears directly on this.

> "I recommend we keep Authorization separated using Identity as an input to it. Identity
> provides the authenticated principal. Authorization evaluates the runtime context and action
> boundaries."

## Issue 2 — Anonymity and Pseudonymity

Whether the standard supports verifiable-but-unlinkable identity binding as an implementer-selectable option, and how. Positions range from full traceability to a principal, to pseudonymity with identity escrow that can be pierced under defined conditions (for example a subpoena). Design intent is that the implementer can select the option that fits the use case. This issue emerged directly from the contribution under issue 4.

> "I strongly advocate for verifiable unlinkability so enterprises can deploy agents without
> disclosing customer PII or corporate identities to third-party vendors. The best way to secure
> information is to not hand it out unnecessarily. :-)"

## Issue 3 — Portability: Evidence Continuity Across Boundaries

Bob Blessing-Hartley raises whether an unbroken cryptographic evidence chain across attestation domains (for example a cross-cloud migration, where each side is tamper-evident but no link exists between them) belongs in the Portability domain ([C3](0x10-C03-Portability.md)), as a fifth evidence property, or as a domain of its own. (Raised separately by Advait Patel.) When evidence crosses a vendor or jurisdictional boundary, the disclosure footprint of that evidence changes: a ZK proof valid in one jurisdiction may reveal more than is permitted when surfaced in another. Is it worth scoping early whether evidence continuity includes evidence *disclosure* continuity?

> "When an agent moves across clouds or vendor boundaries, I believe the evidence chain must
> remain unbroken."

## Issue 4 — Working-Group Contribution, Bob Blessing-Hartley (verbatim; the source of issues 1 and 2)

> "As drummond.reed@gmail.com pointed out, pure anonymity makes accountability impossible. If an
> agent goes rogue or commits fraud, and there is zero cryptographic link back to a principal,
> the system breaks down. I think we need to separate/clarify these concepts:
>
> Privacy (Data Minimization): The agent only reveals the minimum necessary information to
> complete a task. (e.g., Proving the principal is over 18, without revealing their exact
> birthdate or name). I hate this example, it is so tired but it is one everyone understands.
>
> Pure Anonymity: An agent's actions cannot be linked to the principal, or even to other actions
> taken by the same agent. Drummond is right, this leads to no control at all.
>
> Pseudonymity (Unlinkability): The agent acts under an identifier that is not inherently tied
> to a real-world human, but can be linked back to the principal under specific,
> cryptographically enforced conditions.
>
> Here are some examples where Unlinkability is of value:
>
> Anti-Price Discrimination: A procurement agent negotiating prices for a massive enterprise. If
> the seller knows the agent belongs to Apple or Google, the price goes up.
>
> Whistleblowing / Investigative Agents: Agents deployed to gather data on government or
> corporate malfeasance or human rights abuses.
>
> Healthcare & Research Data: Agents acting on behalf of patients to negotiate data-sharing
> agreements for clinical trials. The authorization must be legally binding, but the principal's
> identity must remain completely shielded from the data consumer. I did some work on a system
> that never (or has not yet!) gone live doing precisely this. <!--aais-allow-->
>
> Micro-transactions & Web Browsing: Agents paying for paywalled articles or services on behalf
> of a user. The vendor needs to know the token is valid, but shouldn't be able to build a <!--aais-allow-->
> surveillance profile of the human's reading habits. I am a big fan of, if I had paid for a
> service, I should not be the product.
>
> How this is accomplished should be flexible, not technology bound, per se. As Drummond pointed
> out, Identity Escrow is a valid one (When I am in the ZK mindspace I call these disclosure
> packages.) Escrow requires trust of a set of people which means people need to know what they
> are buying into and who can disclose what, to whom. ZKP directly enables "verifiable but
> unlinkable identity binding." Using ZKPs, a principal can issue a delegation credential to an
> agent. When the agent acts, it presents a ZKP to the relying party that mathematically proves:
> "I have been authorized by a legitimate, verified principal who holds the required
> credentials." The proof validates the authority without ever revealing the identifier of the
> principal. Peer decentralized DIDs are also an interesting approach.
>
> So… The Verifiable Unlinkability scenario ends up the most technically complex aspect of this
> because two things need to be proved:
>
> Delegated authority from a legitimate principal
>
> An agent has to prove that it holds the private keys to execute the action being performed.
>
> This is where ZKP becomes the proof of control. Instead of handing over the delegation token
> from the "principal", the agent runs a cryptographic algorithm locally to generate a ZKP which
> asserts to the verifier of an action:
>
> I, the agent, (feels weird using the pronoun "I") have a valid delegation signature from a
> trusted issuer/principal.
>
> That issuer/principal meets your requirements (for example they are a qualified investor)
>
> I, the thing that is communicating with you with the identity DID:xyz mathematically control
> the specific private key delegated to this capability.
>
> Note that there are actually multiple phases to this, I have only touched upon the ZKP piece.
> On a high level the flow is 1. Delegation to Agent, 2. Handshake with Verifier (maybe using a
> peer DID), 3. The ZKP stuff above and finally 4. the verifier checks the math and says all
> good and there is not a drop of traceable footprint for data brokers to consume."

## Issue 5 — A Possible Fifth Evidence Property

Continuity across boundaries, credited to Advait Patel, who wants it added to the four evidence properties in [C7](0x10-C07-Evidence-Generation-and-Properties.md):

> "The four properties are clean but I think one is missing in practice. Evidence continuity
> across boundaries."

## Issue 6 — The Binary Threshold

The binary threshold ([C8](0x10-C08-Verifiability-Tiers.md)) is the standard's most consequential definition and its most-scrutinized point, and the working group must review and ratify it with dedicated cryptography and blockchain review. There are many impossibility results pertaining to controlling or verifying agentic behavior that can be derived through computational complexity theory, and certain verifications are going to be extremely expensive; careful care must be taken to ensure that a binary definition is efficiently achievable. Two questions in particular:

1. Is the defining test for the Tier-2-to-Tier-3 line — *no single trusted party* (not the operator, and not a third-party root of trust such as a certificate authority, a chip vendor, or a trusted setup) — the correct one, or is a more precise formulation needed?
2. Does the authenticated-documentation vs. mechanism-generated-evidence distinction hold under adversarial scrutiny across the mechanism families (zero-knowledge proofs, TEE attestation, transparency logs, verifiable computation, consensus systems)?

Additional research on the binary threshold, from a cryptographic and complexity-theoretic perspective, is being done by a group of researchers with an academic background, coordinated and led by Hart Montgomery, CTO of the Linux Foundation Decentralized Trust. The goals are twofold: first, prove impossibility results around proof of control so that it is known (or formalized) what is achievable and what is not; and second, develop basic formal definitions and frameworks so that systems can be built and classified rigorously.

One concrete case the standard must address: AI-powered validation tools that analyze, score, and verify code or data quality before deployment. These tools produce detailed evidence of what was validated, verifiable by third parties.

## Issue 7 — The Standardized Disclosure Format

The trust-assumption disclosure format ([C10.2](0x10-C10-Conformance-and-Disclosure.md)) is not yet defined. The working group must fix a finite set of trust-assumption categories so disclosures are comparable across implementations. Bob Blessing-Hartley proposed a two-dimensional matrix of privacy-enhancing mechanisms (ZK, FHE, TEE-based confidential compute, MPC) against trust category (trusted setup, hardware-vendor attestation, and so on). A draft set of categories exists as a starting point: Hardware, Mathematical, Ceremony, Vendor, Implementation, and Distributed. The working group can ratify, refine, or replace it.

## Issue 8 — Continuously Monitored Operational Requirements

"On an ongoing basis" ([C10.3](0x10-C10-Conformance-and-Disclosure.md)) has to be made concrete enough to certify against. Three questions in particular: (1) minimum monitoring cadence — how continuous "continuous" must be, real-time and event-driven, or a bounded interval such as hourly or daily, and whether it varies by domain or by Verifiability Tier; (2) automated versus human — what must be machine-validated as the system runs versus periodically re-assessed by a person; (3) incident response — what is expected when monitoring detects a control failure, a broken trust assumption, or a gap in evidence, including notification, remediation, and whether conformance is suspended until the issue is resolved.

## Issue 9 — Standards-Mapping Volunteers

Volunteers are needed to develop out the crosswalks for [SOC 2](../../mappings/soc-2.md), [Zero Trust](../../mappings/zero-trust.md), and [Confidential Computing](../../mappings/confidential-computing.md); and the working group must decide whether David Thomson's graph view complements or replaces the by-domain mapping table ([mappings/README](../../mappings/README.md)).

## Issue 10 — Schedule Ratification

The roadmap schedule ([docs/roadmap.md](../../docs/roadmap.md)) is the working target, ratified by the working group at kickoff; the dates for the separate Certification and assessor-body track are still to be set. The detailed appeals procedure and conflict-of-interest disclosure format are also to be finalized ([docs/governance.md](../../docs/governance.md)).

## Issue 11 — CISO Review Referrals

The [CISO review of v0.1.4](../../docs/reviews/ciso-review-v0.1.4.md) applied twelve findings
directly as requirements (C2.4, C4.1.6, C6.3, C7.2.2, C7.6, C8.1.7–8.1.8, C8.3.4,
C10.1.6–10.1.7, C10.3.6) and referred four questions to the working group:

1. **Incident response beyond alerting** — whether conformance is suspended on a detected
   control failure (extends issue 8; the review recommends the suspension model).
2. **Third-party dependency inventory** — whether the conformance statement should enumerate the
   external services and subprocessors the agent crosses into.
3. **Verifier-side denial of service** — whether economic limits on verification (proof size,
   cost per verification) should be a disclosure item, so "anyone can verify" holds in practice.
4. **Insider threat at the silicon/HSM layer** — currently handled via trust-assumption
   disclosure; flagged for the cryptography review under issue 6.

## Issue 12 — Research-Driven Additions (2026 Literature)

Four requirements and three threat-model rows were added from the 2026 verifiable-control
literature synthesized in [docs/research-basis.md](../../docs/research-basis.md), and carry
draft status until the working group ratifies them against the primary sources:

* **C4.1.7** (path-aware authorization context) and **C4.1.8** (no trust transfer into approval
  state) — from SCR-Bench (Xie et al.): capability-flow, trust-transfer, and
  authorization-confusion composition attacks succeed against artifact-level vetting.
* **C10.1.8** (inventory reconciled against automated discovery) — from AI Trust OS (Bandara et
  al.): shadow AI eliminated by parsing observability streams.
* **C10.3.7** (validator structured-trace parsing competence) — from TraceSafe-Bench (Chen et
  al.): guardrail efficacy correlates with structural parsing, not NL safety tuning. <!--aais-allow-->
* Threat rows: skill composition risk, shadow/undeclared agents, trajectory-monitor parsing
  failure ([Appendix C](0x92-Appendix-C_Threat-Model.md)).
* Also to decide: whether Verifiable Trust Circles (proposed in the Web 7.0 / did7:web7 specification, built on W3C VC Data Model 2.0 with Data Integrity Proof Sets) enter the mechanism inventory
  permanently ([Appendix B](0x91-Appendix-B_Proof-Mechanism-Inventory.md)), and whether the
  citations verify against the primary literature.

## Issue 13 — Security-Review Findings (paper red-team)

A [security-venue-style peer review](../../docs/reviews/security-venue-review-paper-v0.1.md) of
the companion paper identified three defects in the **specification** (not merely the write-up),
now addressed as draft requirements pending working-group ratification:

* **Execution fidelity / complete mediation** — attestation proves a snapshot was evaluated, not
  that the evaluated snapshot describes the action that executed. New **C7.1.4** requires the
  effect channel to be mediated in the same trust boundary (enclave-terminated egress,
  capability-bound dispatch, or attested-path mediation), and **C7.1.5** forbids claiming
  executed-action evidence without it.
* **Equivocation and truncation** — hash chaining detects alteration and in-chain omission but
  not split-view or head truncation. New **C7.3.3** requires gossip, witness co-signing, or
  consensus anchoring; new **C7.6.6** requires a declared maximum anchoring interval (which
  bounds the undetectable truncation window) with alerting on a missed deadline.
* **Tier-4 halt authority** — C8.3 tested self-enforcement but did not require the halt to sit
  outside operator control. New **C8.3.5** requires far-end enforcement (relying parties refusing
  requests without a valid action-bound capability).

Open questions for the working group: what maximum anchoring interval is defensible per risk
class; whether capability-bound dispatch (which requires relying-party cooperation) should be
mandatory rather than one option among three at Tier 4; and the utility cost of path-aware
authorization, which is unmeasured.

---

*To weigh in on any open issue, join a working group at
**[advancedaisociety.org](https://advancedaisociety.org/)**.*
