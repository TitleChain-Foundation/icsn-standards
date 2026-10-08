# M5-MATH-001 — Provable, Deterministic, Public Math

**Status:** Draft for review · **Version:** 0.1.0
**Machine-readable manifest:** [`packages/m5-math/M5-MATH-MANIFEST.json`](../../packages/m5-math/M5-MATH-MANIFEST.json)
**Related:** M5-CRP-001 Cryptographic Resilience and Algorithm Agility Profile

## 1. Purpose

M5 prices, splits, holds, refunds, registers, and scores. Every one of those
steps is math, and every one must be provable, deterministic, and visible to
anyone. M5-MATH-001 requires that:

1. every calculation is written down once, exactly, in the manifest;
2. the same inputs give the same outputs and hashes on every machine;
3. anyone can recompute a published receipt or score without trusting M5.

## 2. Rules

- **Integers in published units.** Money is in micros (one millionth of a
  currency unit); rates are basis points; scores are whole numbers. No
  floating point in approved math.
- **Every rounding rule is stated.** Fees round down (never overcharge),
  the CCF-5 floor rounds up (never below 5%), and splits use largest
  remainder so totals are exact.
- **Two implementations, one set of vectors.** Calculations marked
  `PYTHON_JS` have a Python and a JavaScript implementation held to the same
  published test vectors, byte for byte.
- **Receipts and scores cite their rules.** Each M5 Value Receipt records the
  SHA-256 of the math manifest and every rule file it was computed under.
- **Status before consequence.** `PROPOSED` math is computed and published
  but has no economic effect until approved. `APPROVED` math is in force.
- **Additive versions.** A change is a new version; earlier versions stay
  published (M5-CRP-001 §18).
- **Research is evidence, not policy.** New research, including the OpenAI
  Oct. 6, 2026 mathematics release, may prompt review but never directly
  changes approved math (M5-CRP-001 §16). No family in that release defines
  reputation weights, and none is used as a basis for M5 math.

## 3. Canonical hashing (MATH-CANONICAL-HASH)

Every published hash is SHA-256 (FIPS 180-4) over canonical JSON: keys
sorted, no whitespace, UTF-8, whole numbers as integers within ±(2^53−1),
other numbers as plain decimal strings (never exponent notation). The rule
exists so JavaScript and Python, and any future language, produce identical
bytes. Values outside the portable range are rejected rather than hashed
differently.

## 4. What the manifest covers

| Area | Calculations | Status |
| --- | --- | --- |
| Fees and splits | Fee from BPS, CCF-5 floor, standard split, agency payouts, ZIP pool | APPROVED |
| Settlement | Hold windows, refunds | APPROVED |
| Evidence | Canonical hash, event chain, receipt verification | DRAFT |
| M5Nash | Decay, component score, M5Score, signals | PROPOSED |
| PAINE | Holder-note common-sense check | DRAFT |
| Legacy | Odea waterfall (floating point), Lightlocker simulated rates | LEGACY |

The manifest gives each one's exact formula, units, rounding,
implementations, vectors, and dependencies.

## 5. M5Nash Score (PROPOSED)

M5Nash is the scoring agent, GREEN computes and records the score, and PAINE
checks holder notes before they become evidence. A wallet is scored without
its owner's name.

- **Decay.** Each signal's weight halves every 30 days if good and every 180
  days if bad, so mistakes are remembered longer than successes. Weights use
  32-bit fixed point with published integer constants.
- **Component score (Beta reputation).**
  `floor(1000 × (G + 1) / (G + B + 2))`, where G and B are the decayed weights
  of good and bad signals. No evidence gives exactly 500, the neutral score
  in the M5Nash specification.
- **M5Score.** `floor(Σ weight × component / 10000)`, on a 0–1000 scale. The
  database's 0–100 `m5nash_score` is M5Score ÷ 10.

| Component | Weight | Evidence |
| --- | ---: | --- |
| Settlement reliability | 30% | Releases, non-delivery refunds |
| Attestation integrity | 20% | Verified active business, credentials |
| Information symmetry | 15% | Upheld claims, holder notes vs. listing |
| Reciprocity | 15% | Buyer ratings on released sales |
| Externality | 10% | Costs pushed onto others (no source yet) |
| Governance participation | 10% | Voting and DUNA engagement (no source yet) |

Weights favor evidence that is hardest to fake. Ratings count only from the
buyer of a released sale, one per sale, and a single sale can never count
twice toward the same component. Trust-tier thresholds are not set.

### Inspiration: cooperation that benefits both sides

M5Nash takes its name from a game-theory idea: when two parties can trade, each can do better
by cooperating than by acting alone, and the best outcome is one where neither side can gain
by defecting. The concepts are the Nash equilibrium and the Nash bargaining solution, from
John F. Nash Jr.'s published work (*The Bargaining Problem*, Econometrica, 1950;
*Non-Cooperative Games*, Annals of Mathematics, 1951). M5Nash is an independent M5 method.
M5, M5Capital Holdings LLC, TitleChain Foundation, and the TitleChain Sovereign Purpose Trust
are not affiliated with, sponsored by, or endorsed by Dr. Nash's estate or any person or entity
that represents his work.

The M5 stack builds that idea into the transaction itself, so cooperation is the profitable
choice:

- **Every trade also pays the community.** The CCF-5 floor sends 5% of collected M5 fee
  revenue to the seller's local community pool, and to up to two approved agencies in that
  ZIP code, so each sale benefits the seller's community as well as the two parties.
- **Both sides are protected.** The settlement hold and adjudication release funds only after
  delivery and refund the buyer if delivery fails. Two strangers can trust each other enough to
  trade, because neither can walk away with the other's value.
- **Cooperation is remembered, and defection is remembered longer.** M5Nash weights
  settlement reliability and reciprocity most heavily. A bad signal keeps half its weight for
  180 days and a good one for 30, so a single breach costs more than a single success earns.
  In a repeated game, that makes keeping one's word the better strategy.

These are design incentives. The CCF-5 percentages and the M5Nash weights are policy choices
published in M5-MATH-001, not values derived from a bargaining formula.

## 6. Verify it yourself

```bash
# Recompute every published vector and hash in Python
python -m pytest tests/test_m5_math_manifest.py tests/test_m5nash_score.py

# Recompute them independently in JavaScript, and verify sample receipts
node --test packages/m5-math/m5-math.test.js

# Confirm a rule file is the one a receipt cites
shasum -a 256 packages/m5-math/M5-MATH-MANIFEST.json
```

`packages/m5-math/receipt-verify.js` checks any receipt from its own
contents: the split hash, that costs and distributions add up, the CCF-5
floor, and that agency payouts sum to the Commons share.

## 7. Open items

- Trust-tier thresholds (PLATINUM through WATCH) need approval.
- Externality and governance participation have no evidence sources yet.
- Settlement, refund, event-chain and PAINE math have Python
  implementations only.
- Settlement events identify their actor but are not yet cryptographically
  signed; signing should follow an M5-CRP-001 named profile.
- Odea's waterfall still uses floating point and should move to micros.
