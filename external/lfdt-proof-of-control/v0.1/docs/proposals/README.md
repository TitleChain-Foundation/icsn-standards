# Proposals from the research programme

The [research roadmap](https://github.com/AAI-Society/poc-research-roadmap) exists to
answer questions this standard currently settles by assertion, by convention, or not at
all. Three of its papers are done — P01 trust calculus, P02 effect binding, P05
unlinkable identity — each with a shipped tool, and a fourth stream of findings came out
of building compliance tooling against the standard itself.

This directory holds what that work says the standard should change. It is **proposals**,
not adopted text.

| File | Source | Changes | Needing WG ratification |
| --- | --- | :--: | :--: |
| [`P01-trust-calculus-tiers.md`](P01-trust-calculus-tiers.md) | P01 · `parallax` | 12 | 9 |
| [`P02-effect-binding.md`](P02-effect-binding.md) | P02 · `transit` | 10 | 11 |
| [`P05-unlinkable-identity.md`](P05-unlinkable-identity.md) | P05 · `occultation` | 13 | 20 |
| [`tooling-findings.md`](tooling-findings.md) | building `poc-audit`, `ephemeris`, `spectrum` | 8 defects | — |

## What has already been applied, and what has not

The dividing line is **whether the standard currently says something untrue**.

**Applied in this branch**, because a universal claim with a counterexample is simply
false and no ratification makes it true again:

* The four-tier table no longer says Tier 3 means *"the trusted party is removed."* A
  Tier 3 Intel TDX deployment retains a five-party residual trust set, and the cloud
  operator is one of them — so even the narrow reading "the *operator* is removed" fails
  for the standard's own flagship example.
* *"The cryptographic mechanism"* and *"the cryptographic mechanism is sound"* now name
  the parties that soundness rests on, because an abstraction is not a party.
* The word *"trustless"* no longer appears as a claim in normative text. It survives
  only in *"trustless setup"* (C8), the standard name for a setup ceremony nobody has
  to trust, which is correct and stays.
* C1.2.2 asks for inputs **present in the context at evaluation time** rather than inputs
  that **influenced** an action. Influence is why-provenance and nobody can compute it;
  every implementer meeting the old wording was meeting the new one under a stronger name.
* Two schema defects that concealed each other — see
  [`tooling-findings.md`](tooling-findings.md) findings 1 and 2.

**Not applied**, and marked `[WG-INPUT NEEDED]` where it lands in the text:

* Demoting the Tier from the primary claim to a coarse summary, with what must be trusted
  carried by the C10.2 disclosure instead. This is a positioning decision for the chapter.
* Restating the Tier-2/Tier-3 test as *who selects the trusted party* and *whether their
  dishonesty is publicly detectable*. Goes to [Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md)
  issue 6, question 1.
* Everything in P02 and P05 above the level of a wording fix — including the restated
  Theorem 1, the endpoint-qualification profile, and the identity-profile discriminator
  that would make `agent_id` conditionally forbidden rather than optional.

## The evidence base, and its limit

P01's findings rest on **five self-authored deployment descriptions and no real-world
system**. That is enough to refute a universal claim — one counterexample does it — and
it is **not** enough to install a new ordering, a new tier taxonomy, or a machine-readable
manifest schema as normative. The proposals are shaped to that limit: they delete false
claims and add disclosure obligations, and they mark every structural change for the
working group.

Two proposals argue *against* their own source. P01's rejects the research paper's
proposed tier renames, on the ground that all four worked examples contain an
unbounded-latency assumption, so a latency-ordered ladder ties them all at infinity — the
research's own data refutes its own ordering. P05's declines to make `agent_id` optional,
on the ground that optionality makes a missing identifier indistinguishable from a
pipeline failure.

Where a proposal rests on cryptography nobody can deploy today — two of `occultation`'s
five priced layers are modelled stubs with no security, and its BBS+ is real but not
interoperable — it is labelled `[MODELLED — NOT IMPLEMENTABLE TODAY]` rather than written
as though it were available.
