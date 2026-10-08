---
industry: consumer-lending
use_case: AI assisting credit decisions on loan applications
submission_type: scenario
claimed_tier: 4
threats:
  - model-poisoning
  - supply-chain-poisoning
  - scope-creep-lifecycle
  - behavioral-drift
  - identity-abuse
  - data-exfiltration
  - hidden-bias
  - evidence-repudiation
---

# AI-assisted consumer credit decisioning

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A lender uses an AI model to score loan applications and issue approve or deny
decisions. Applicants have a legal right to the reasons behind an adverse
decision, and an unapproved or drifted model must never be the one that decides
a live application. If verification is weak, a model other than the approved one
can issue a real decision to a real applicant, and the lender only finds out, if
ever, after the fact.

## Claimed tier: Tier 4

Credit decisions are legally consequential and acted on immediately, so
detection after the fact is not enough: a wrong decision has already reached the
applicant. Tier 4 makes serving **fail-closed**. Before any decision is issued,
a live verification establishes that the exact approved model, in its approved
configuration, is what will serve. If that verification fails, no decision is
issued, so an unapproved model never reaches an applicant in the first place.

## Why not one tier down?

Tier 3 gives open weights, reproducible evaluations, and an audit log, so you
can establish *after the fact* which model ran on a given application. That is
detection, not prevention: an unapproved or drifted model can still issue a live
decision before any audit reaches it, and by then the applicant has been
approved or denied.

**Reversibility.** For a legally consequential decision the applicant has
already relied on, that lag is the failure that matters. An adverse decision
cannot be withdrawn from someone who has already been told. Tier 4 closes it by
refusing to serve unless the live attestation of model and configuration passes,
so the wrong model is blocked at issuance rather than flagged later.

**Completeness.** At Tier 3 a decision issued outside the instrumented path
leaves no record, and its absence is not informative. Read a Tier 3 claim here
as "the decisions you can see were served by the approved model", rather than
"these are all the decisions". A supervisor asking whether any applicant was
scored by an unapproved model cannot be answered with the first sentence.

## Tier by domain

The overall Tier 4 is driven by Provenance and Authorization, the two domains
where a fail-closed gate is required. Portability barely matters here, which is
expected; the claimed tier reflects the highest bar the risky domains impose,
rather than an average across all six.

| Domain | Tier | Why |
|---|---|---|
| Provenance | 4 | A live gate verifies which model and configuration is about to serve, and blocks issuance if it is not the approved one. This is the driver. |
| Privacy | 2 | Sensitive financial personal data, regulated; handled by data controls and third-party assessment rather than an enforcement gate. |
| Portability | 1 | Whether the decision is portable across systems is not what makes it verifiable; self-reported. |
| Authorization | 4 | Only the approved model in the approved configuration is permitted to serve; anything else means the decision cannot be issued. |
| Identity | 3 | Each issued decision binds to an accountable model and operator identity. |
| Security | 3 | An adversarial setting, since applicants game scores. Pipeline integrity is openly verifiable and not fully fail-closed on every vector. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `model-poisoning` | A model other than the approved one, or a drifted version of it, scoring a live application |
| `supply-chain-poisoning` | An unattested artifact entering the serving path between approval and issuance |
| `scope-creep-lifecycle` | A configuration change reaching production without passing the approval it was classified under |
| `behavioral-drift` | The approved model's behavior moving away from what it was evaluated on |
| `identity-abuse` | A decision reaching an applicant with no accountable model or operator behind it |
| `data-exfiltration` | Regulated financial personal data crossing a boundary during scoring |
| `hidden-bias` | Bias in the decisions themselves, which this deployment is exposed to and which no tier addresses |
| `evidence-repudiation` | A dispute over an adverse decision in which the lender and the applicant hold different accounts of what served |

## What Proof-of-Control does not verify here

- **Whether the approved model is fair, well-aligned, or trained on good data.**
  Tier 4 establishes that the approved model served. It does not establish that
  approving it was right. Those are settled at earlier stages, in evaluation and
  red-teaming, and remain necessary.
- **Bias in the decisions.** Assessing or correcting fairness is validation, and
  the standard does not reach it. A tamper-evident record of the verdicts
  supports a separate review, and it is not that review.
- **Whether the approval threshold or the scoring policy was the right one.**
  That judgment belongs to the lender and its regulator.
- **Whether an attested artifact is trustworthy upstream.** Attestation
  establishes which weights and configuration loaded, and says nothing about
  their provenance before that point.
- **Covert side-channel exfiltration** of applicant data, and whether the
  privacy policy governing that data is adequate.
- **Whether the reasons given for an adverse decision are accurate or adequate.**
  The record shows which model issued the decision, not whether the explanation
  attached to it is sound.

## Residual trust assumptions to disclose

- The attestation chain at the serving host, with its version, freshness and
  revocation policy.
- The approval process that decides which model and configuration count as
  approved, and who can change that list.
- Custody of the signing keys, and what an operator with access to them could do
  to a record that is otherwise tamper-evident.
- The monitor set for any transparency log, and what happens if monitors lapse.

## Notes / open questions

- Tier 4 here means the serving gate is **fail-closed and attested**, rather
  than that the model computation is verified with zero-knowledge methods.
  <!--aais-allow--> Proving the inference itself (zkML) was raised as not
  currently feasible; this example deliberately relies on attested, fail-closed
  serving plus an audit log, and not on a proof of the computation.
- Originally submitted by Mo Sadek (GitHub @SomeGuyNamedMo) in
  [AAI-Society/openverification#1](https://github.com/AAI-Society/openverification/pull/1), before the threat vocabulary and the
  v2 template existed. Retrofitted by the Society in
  [AAI-Society/openverification#12](https://github.com/AAI-Society/openverification/pull/12), with the scenario, the tier argument
  and the domain reasoning unchanged from the original, and ported here when the
  use-case corpus moved into this repository.
