# Peer Review, Round 2: Proof-of-Control paper (post-revision)
<!--aais-record-->

*Second-round simulated review in the style of a top-tier security venue, conducted on the
revised [`paper/main.tex`](../../paper/main.tex) (22 pp., 116 requirements) after the
[round-1 findings](security-venue-review-paper-v0.1.md) were addressed. Not an actual venue
review.*

> **Disposition: all findings addressed.** R1 — Definitions 1–2, Theorem 1 (execution fidelity,
> reduced to EUF-CMA + collision resistance), Proposition 1 (necessity of mediation), and
> Theorem 2 (equivocation detectable and attributable) added with proof sketches. R2 — new
> "Relation to information-flow control" section citing Denning, Goguen & Meseguer, Myers &
> Liskov, JFlow, Sabelfeld & Myers, HiStar, and Flume, stating four precise differences and
> inheriting the label-creep prediction. R3 — new deployability section grounding
> capability-bound dispatch in the capability literature and macaroons, with an incremental
> adoption path and an honest residual gap. R4 — new path-state and complexity section: bounded
> path summary as a fold, O(|Π| + B) per step, with the expressiveness limit stated. R5 — Δ
> guidance table by action class. R6 — all seven provenance-weak citations removed from the
> paper; claims re-grounded in verifiable literature. R7 — standards integration and roadmap
> moved to appendices.

**Overall merit: 3/5 (borderline — accept at a workshop or systematization track; still
below the bar for a main-track systems-security paper)**
**Novelty 3/5 · Technical depth 3/5 (was 2) · Presentation 5/5 · Confidence 4/5**

## What this paper now is

A **specification-and-security-analysis paper**: it defines a standard, states an adversary
model, identifies two attacks its own architecture does not resist without additional
requirements, derives those requirements, and maps the result against existing frameworks. That
is a coherent and honest genre — closest to a standards/SoK contribution. It is **not** a
systems paper, and it now says so.

## Round-1 findings: disposition

| Finding | Status | Note |
| --- | --- | --- |
| W1 no implementation/measurement | **Disclosed, not fixed** | Correctly reframed as design targets with an explicit scope statement. Honest, but still the binding constraint on venue. |
| W2 snapshot substitution | **Fixed** | New §5.4 names the attack, ties it to reference-monitor theory, and gives three mediation options with their differing residual trust. Now the paper's strongest technical contribution. |
| W3 split-view / truncation | **Fixed** | P3/P4 state precisely what fails; bounded anchoring interval Δ and gossip/witness/consensus requirements added. |
| W4 Tier-4 assertion | **Fixed** | §7.3 gives a construction (capability-bound dispatch, far-end enforcement) and resolves the vendor-root tension by grading trust structure rather than mechanism. |
| W5 coverage study | **Fixed as framing** | Reframed as descriptive gap analysis with four stated limitations plus a two-coder κ protocol in the rubric. The study itself is still single-coder. |
| W6 citation integrity | **Partially fixed** | Reddit citation removed; real literature added. Seven weak-provenance sources remain in use (21 instances). |
| A1 threat-model formalism | **Fixed** | Adversary capabilities and assumptions A1/B1/C1/D1 now explicit. |
| A2–A6 | **Fixed** | Privacy proof obligations, path-aware utility cost, comparison table, author list (32→4), venue/status statement. |

## Remaining weaknesses

**R1. The security properties are argued, not proven.** P1–P4 are stated in prose with
justification sentences ("holds under A1, B1, C1"). There are no definitions, no games, no
theorem/proof environments anywhere in the paper. For a venue that publishes this kind of
analysis, at minimum P2 and P4 deserve formal statements: define the experiment in which
$\mathcal{A}$ wins by producing an accepted token whose committed snapshot does not correspond
to the executed effect, and show that the capability-bound construction reduces winning to
forging a signature. The material is close to formalizable; it simply has not been formalized.

**R2. Missing literature: information-flow control.** The paper's motivating example — an agent
reads confidential records at step $i$ and makes an outbound request at step $j$ — is a
textbook information-flow problem, and the paper cites no IFC work (Denning; Myers \& Liskov;
Jif; HiStar/Flume; taint-tracking). This matters twice: a reviewer will read "path-aware
authorization" as decades-old IFC rediscovered under a new name unless the paper distinguishes
them, and IFC's known results (the label-creep/utility problem, the difficulty of declassification)
directly predict the utility cost the paper flags as unmeasured. Adding this framing would
*strengthen* the contribution by inheriting known results; omitting it looks like a gap in
scholarship.

**R3. The Tier-4 construction's deployability assumption is under-examined.** Capability-bound
dispatch is the only option surviving a fully compromised host, and it requires *every relying
party* to verify capabilities. That is a large ecosystem ask — arguably the reason such
architectures do not exist today — and the paper gives it three sentences. What fraction of
realistic tool endpoints (SaaS APIs, databases, payment rails) can be made to verify? What is
the incremental path? This is the central adoption question and deserves its own analysis.

**R4. Path-aware evaluation has no complexity treatment.** $\Pi$ takes the full partial path
$\mathcal{A}^{*}$ as an argument. What is the state representation, does it grow unboundedly, and
what is the per-step cost as paths lengthen? Given the paper's own <15 ms budget, an evaluation
cost that scales with path length is a design problem, not a detail.

**R5. Δ is qualitative.** The truncation window is bounded by the anchoring interval, but the
paper offers no guidance on choosing Δ against a risk class, nor the anchoring-cost tradeoff it
acknowledges. One worked example (e.g., payment authorization at Δ = 1 s vs. batch reporting at
Δ = 1 h) would make the parameter actionable.

**R6. Provenance-weak citations persist.** `xie2026scr` (4×), `policiesonpaths2026` (4×),
`bandara2026`, `chen2026tracesafe`, `web7vtc`, `catenax2026`, `mindxo2026` still carry no venue,
DOI, or full author list. The prose now hedges them, which is the right instinct, but a reviewer
will still ask why unverifiable sources appear at all when verifiable substitutes exist for most
of these claims.

**R7. Length and dual identity.** At 22 pages the paper is long for most security venues, and it
still serves two masters: it argues for adoption of a standard *and* analyzes a system. The
standards-integration roadmap (§10.1–10.2) is the most obviously cuttable material for a
research venue and the most valuable for an SDO audience — evidence that two documents may be
hiding inside one.

## Verdict by venue

| Venue | Outcome |
| --- | --- |
| IEEE S&P / USENIX Security / CCS main track | **Reject** — no implementation, no formal proofs, no measured evaluation |
| SoK / systematization track | **Borderline accept** — with R1 (formalize) and R2 (IFC) addressed |
| Workshop (SaTML, AISec, IEEE SPW, WEIS for the economics framing) | **Accept** — good fit as written |
| SDO submission (ISO/IEC SC 42, IETF RATS) | **Strong** — this is the audience the document is actually built for |
| arXiv preprint | **Ready**, subject to co-author consent and citation cleanup |

## The single highest-value next step

Build the reference implementation and measure it. Every remaining weakness except R2 is either
resolved by, or reframed around, having a working system: R1 gets a concrete artifact to prove
about, R3 gets an integration story with real endpoints, R4 and R5 become measurements rather
than open questions, and W1 disappears. A paper reporting *"we built the enclave-resident policy
engine, mediated the effect channel, and here is the latency distribution and the utility cost
of path-aware authorization on AgentDojo/ToolEmu"* is a main-track systems paper. The present
document is the specification that such a paper would implement.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
