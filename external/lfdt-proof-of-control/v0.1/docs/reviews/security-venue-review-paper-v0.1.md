# Peer Review: Proof-of-Control paper (v0.1 draft)
<!--aais-record-->

*Simulated review in the style of a top-tier security venue program committee
(IEEE S&P / USENIX Security / CCS). Prepared as an internal red-team exercise on
[`paper/main.tex`](../../paper/main.tex) before submission. Not an actual venue review.*

> **Disposition: all findings addressed** (commit `b2fd54c`). This review was written against
> the 111-requirement draft; the specification now carries 116 requirements, with C7.1.4/C7.1.5
> (complete mediation), C7.3.3 (non-equivocation), C7.6.6 (bounded anchoring), and C8.3.5
> (halt outside operator control) added in response. The paper gained a formal adversary model
> and security analysis, an explicit Tier-4 construction, honest scoping (no implementation
> claimed), a reframed gap analysis with a two-coder κ protocol, a rebuilt comparison table, a
> reduced author list, and corrected citations. Numbers quoted below reflect the reviewed
> version. See [Appendix D, issue 13](../../0.1/en/0x93-Appendix-D_Open-Issues.md).

**Overall merit: 2/5 (Reject — resubmit after major revision)**
**Novelty 3/5 · Technical depth 2/5 · Presentation 4/5 · Reviewer confidence 4/5**

## Summary of the submission

The paper identifies a "Verifiability Gap" for autonomous agents and proposes Proof-of-Control:
a requirements catalogue (111 requirements across six domains), a four-tier evidence-grading
scale with a binary threshold, and a reference architecture that intercepts agent lifecycle
events, evaluates policy inside a TEE, and emits Entity Attestation Tokens over a signed Merkle
chain. Evaluation consists of a coverage mapping of the authors' own requirements against eight
external frameworks, plus a stated (not measured) 15 ms latency budget.

## Strengths

* **S1.** Real, timely, well-motivated problem. The separation of *enforcement* (what an agent
  may do) from *operator-independent evidence* (what it did) is under-served, and the
  "who must you trust to believe it" tier framing is clean and communicable.
* **S2.** The binary threshold is a sound standardization move, and the determinism boundary is
  honest — the paper explicitly declines to claim output correctness. Stated limitations are
  unusually candid.
* **S3.** Presentation quality well above average: figures, schema exegesis, and the
  claim-by-claim table are excellent.

## Major weaknesses

| # | Weakness | Required fix |
| :---: | --- | --- |
| **W1** | **No implementation, no measurement.** The 15 ms/step figure is a *budget*, not a result. Enclave transitions, per-step signing, and snapshot canonicalization all have measurable, contested costs; none are measured. Disqualifying at a systems-security venue on its own. | Build the reference implementation; report latency/throughput distributions on a real multi-step agent workload, broken out by component. |
| **W2** | **Snapshot-integrity gap (TOCTOU).** The *host* — which the threat model says may be compromised — constructs the canonical snapshot the enclave evaluates. The enclave attests "I correctly evaluated *a* snapshot," not "this snapshot describes the action that then executed." An operator can present snapshot X while dispatching action Y unless the effect channel (tool/network I/O) is mediated inside the TCB. The paper *requires* no-bypass but never places that enforcement inside the trust boundary or analyzes it. This is the difference between a tamper-evident diary and a reference monitor; the paper claims the latter's properties with the former's architecture. | Either move effect mediation inside the TCB and analyze it, or explicitly scope the claim and state the residual assumption. |
| **W3** | **Log security argument is informal and misses classic attacks.** No formal model, game, or reduction. Merkle "omission detection" via monotonic indices only works for a verifier obtaining tokens independently: suffix withholding (truncation) and fork/equivocation (split-view) defeat it — which is why Certificate Transparency needs gossip and consistency proofs. Anchoring cadence vs. attack window is never analyzed. | Formalize the properties; analyze truncation and split-view; specify gossip/consistency and anchoring cadence. |
| **W4** | **Tier 4 is asserted, not constructed.** The flagship "cannot run unless integrity holds" claim has no protocol: no halt mechanism, no TCB definition, no argument against an operator patching out the halt. Relatedly, Table 2's "zero-trust (hardware-anchored)" overclaims, since hardware attestation roots at a chip vendor — a party the paper's own C8.1.7 correctly caps at Tier 2. | Give a construction and security argument for Tier 4; resolve the vendor-root/Tier-3 tension rigorously rather than by disclosure alone. |
| **W5** | **The coverage study is not an evaluation.** It measures how much of *the authors' own* requirement set eight frameworks cover, single-coder, section-granularity, no second coder, no inter-rater reliability. The metric's direction guarantees a favorable result, making "the gap is the standard's reason to exist" circular. | ≥2 independent coders, report Cohen's/Fleiss' κ, adversarial coding by non-authors of the requirements, and the reverse mapping (what those frameworks require that PoC misses). |
| **W6** | **Citation integrity.** A Reddit thread is the technical reference for the Merkle-chain audit log — a load-bearing mechanism. Several central references (AI Trust OS, TraceSafe-Bench, SCR-Bench, Web 7.0 VTCs, MindXO) have no venue, DOI, or full author list, and the `.bib` self-marks them `[verify]`. Quantitative claims (33.6%, 96.5%, 71.8%, ρ=0.79) rest on these. | Verify and cite properly, or remove the dependent quantitative claims. |

## Additional concerns

* **A1. Threat-model formalism.** No adversary defined in the standard idiom (capabilities,
  corruption model, oracles). A bullet list is below venue bar.
* **A2. Privacy proof obligations.** For the ZK path in C2, state the relation proven, the setup
  assumption, and the leakage profile; "ZKP" as a category label is insufficient given the
  paper's own tier rules make setup provenance decisive.
* **A3. Path-aware authorization under-specified.** What is the state-tracking abstraction, and
  what is its false-positive/utility cost? A monitor that blocks legitimate workflows is not
  deployable; no utility measurement is offered.
* **A4. Unfair comparison construction.** Table 2 compares PoC (standard, hypothetical
  implementation) against three deployed mechanisms on axes the standard defines. Compare instead
  against the closest real systems (CSA AARM, ACS, confidential-computing audit pipelines,
  CT-style transparency logs) on shared axes.
* **A5. Author list.** 32 authors drawn from an organization's board and advisory roster, on a
  paper with no implementation, reads as a governance document rather than a research
  contribution; the footnote noting consent is still being collected is itself a submission red
  flag.
* **A6. Venue fit.** As written this is a standards/position paper — better placed at a workshop
  (SaTML, AISec, IEEE SPW) or an SDO track. The main-track version needs W1–W5 resolved.

## Questions for the authors

1. What exactly is inside the TCB — is tool I/O mediated inside the enclave, and if not, how is
   snapshot-to-effect binding enforced against a compromised host (W2)?
2. What is the concrete Tier-4 halt mechanism, and what prevents an operator from disabling it?
3. What anchoring cadence and gossip/consistency mechanism defend against truncation and
   split-view attacks (W3)?
4. Measured overhead on a realistic multi-step agent workload, broken out by enclave transition,
   policy evaluation, signing, and canonicalization?
5. How is vendor-rooted TEE attestation reconciled with the Tier-3 "no single trusted party" test
   without circularity?

## Disposition

Reject as a main-track security paper: the contribution is currently a well-presented standards
proposal, not a validated system. The path to acceptance is concrete — implement and measure
(W1), close or scope the snapshot-binding gap (W2), formalize the log argument (W3), construct
Tier 4 (W4), redo the coverage study with multiple coders and κ (W5), fix citations (W6). W1–W3
alone would make this a strong systems paper.

## Implications for the standard (not just the paper)

Three review findings are defects in the **specification**, not merely the write-up, and are
recommended to the working group:

1. **Snapshot-to-effect binding (W2)** — C7.1 requires the gateway be out-of-band and
   bypass-free, but does not require the *effect channel* to be mediated within the same trust
   boundary as policy evaluation. Without it, a compromised host satisfies the letter of C7.1
   while evidencing a different action than it performs. Candidate new requirement in C7.1.
2. **Split-view and truncation resistance (W3)** — C7.3/C7.6 make alteration and omission
   detectable *within* a chain, but nothing requires cross-verifier consistency (gossip) or a
   bounded anchoring interval, so an operator can show divergent histories to different relying
   parties. Candidate new requirements in C7.3, plus a defined maximum anchoring interval.
3. **Tier-4 construction (W4)** — C8.3 states self-enforcement as an outcome to test but never
   requires the halt mechanism to reside outside operator control. Candidate strengthening of
   C8.3.3.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
