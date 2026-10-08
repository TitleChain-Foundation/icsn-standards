# Proof-of-Control Regulatory & Framework Mapping Rubric

Mappings between Proof-of-Control requirements and external framework clauses are coded using
three categories, following the coding methodology established by
[HAARF](https://github.com/Task-force-for-AI-agents-in-Healthcare/haarf).

## Match Type Definitions

### EM — Exact Match

The Proof-of-Control requirement directly corresponds to a specific clause in the external framework, with
equivalent scope, intent, and level of specificity.

**Criteria:**

* Same subject matter and intent
* Comparable specificity and actionability
* Direct traceability between requirement and clause

**Example 1:** Proof-of-Control C4.1.3 (out-of-scope actions blocked at the interception gateway, rejection
evidenced) → CSA AARM runtime action interception (approve / modify / defer / deny at the action
boundary). Both mandate enforcement at a runtime gateway with a recorded decision.

**Example 2:** Proof-of-Control C10.1.4 (conformance statement contents) → SOC 2 system description and
management assertion. Both require a published, structured claim naming the system, its scope,
and the controls asserted.

### PM — Partial Match

The Proof-of-Control requirement addresses the same general domain as a framework clause, but differs in
scope, specificity, or in Proof-of-Control's defining constraint: **operator-independent,
mechanism-generated evidence**. The external framework addresses the topic but not with the same
granularity, or its evidence remains operator-produced (Tier 1–2 in Proof-of-Control terms).

**Criteria:**

* Overlapping subject matter with differences in scope or depth
* The framework requires the *control*, but not openly verifiable *evidence* of it
* A general principle maps to a specific Proof-of-Control implementation, or vice versa

**Example 1:** Proof-of-Control C7.2.1 (evidence written within the executing transaction) → EU AI Act
Article 12 (automatic recording of events). The Act requires contemporaneous logging; it does
not require the record to be mechanism-generated or verifiable without trusting the operator.

**Example 2:** Proof-of-Control C4.1.2 (every action evaluated against granted permissions, decision
evidenced) → NIST SP 800-207 per-request access evaluation. Zero Trust requires the evaluation;
Proof-of-Control additionally requires the evaluation to leave tamper-evident, openly verifiable
evidence.

### NM — No Match

The Proof-of-Control requirement addresses a domain not covered by the external framework, or the framework
has no analogous provision.

**Criteria:**

* No corresponding clause in the framework
* The framework does not address this domain
* The requirement represents a need specific to Proof-of-Control (most often: evidence gradability, the binary
  threshold, or trust-assumption disclosure)

**Example 1:** Proof-of-Control C8.1.4 (Proof-of-Control claimed only at Tier 3+) → EU AI Act: no match. No
existing framework grades evidence by how independently it can be verified.

**Example 2:** Proof-of-Control C7.4.1 (standardized residual trust-assumption disclosure) → SOC 2: no
match. SOC 2 discloses subservice organizations and complementary controls, but has no analog
for disclosing the cryptographic, hardware, and ceremony assumptions behind evidence.

## Coding Instructions

1. For each Proof-of-Control requirement, identify the most relevant clause(s) in the target framework.
2. Assign EM, PM, or NM based on the criteria above.
3. Record a brief rationale explaining the match decision.
4. When multiple clauses partially match, select the strongest match and note alternatives.
5. When in doubt between PM and NM, default to NM (conservative coding).
6. The unit of coding is the individual requirement (`C<chapter>.<section>.<requirement>`), as
   enumerated in [`checklist/poc-checklist.csv`](../checklist/poc-checklist.csv).

## Coverage Computation

Coverage percentage per framework = (EM + PM) / total Proof-of-Control requirements × 100.

Only EM and PM contribute to coverage; NM indicates a gap where the external framework does not
address the Proof-of-Control requirement. Reproduce the numbers with:

```bash
python3 mappings/compute_coverage.py
```

**Reading the numbers:** coverage here measures how much of *Proof-of-Control* an external
framework already addresses — not the reverse. A low percentage is not a criticism of the
framework; it usually means the framework governs a different object (organizations, models,
risk processes) than Proof-of-Control's object (openly verifiable evidence of agent execution). The
NM gap is, by design, the standard's reason to exist.

## Coding Protocol (required for published coverage figures)

The current sheet is single-coder seed data. Before coverage figures are cited outside this
repository, the working group applies a two-coder protocol:

1. **Two independent coders** per framework, working from the corpus document and this rubric,
   blind to each other's codings. At least one coder per framework SHOULD NOT be an author of
   the requirements being coded (adversarial coding).
2. **Inter-rater reliability** reported per framework as Cohen's κ over the three-category
   scale; κ < 0.6 triggers rubric clarification and re-coding rather than adjudication alone.
3. **Adjudication** of disagreements by a third coder, with the resolution recorded in the
   sheet's rationale column.
4. **Requirement-level granularity** replacing the current section-level inheritance.
5. **Reverse mapping** published alongside: requirements each framework imposes that
   Proof-of-Control does not cover, so the comparison is two-directional.

## Coding Status

> **[WG-INPUT NEEDED] — draft seed coding.** The current
> [`coding_sheet.csv`](coding_sheet.csv) is a single-coder seed draft
> (`coder_id = seed-01`), coded at section granularity and expanded to requirement rows. The
> working group must validate row-level codings, add second-coder review, and record
> inter-coder agreement before the coverage numbers are cited outside this repository.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
