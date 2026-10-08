# CLAUDE.md

Guidance for Claude Code and other AI assistants working in this repository. Read this before editing any file.

## What this repository is

The normative home of the Proof-of-Control Standard. Chapters **C1 to C10** in `0.1/en/` are normative and under change control. Everything in `docs/` is informative: it explains and motivates the standard and adds no requirements. Do not treat informative material as binding, and do not file normative change proposals against it.

## Terminology, and it is not negotiable

These words carry specification weight: using the wrong one changes what a claim means.

| Word | What it grades or locates | Range |
| --- | --- | --- |
| **Tier** | The evidence: how independently it can be verified | 1 to 4 |
| **Level** | The requirements: what an assessor tests for | 1 to 4, aligned one to one with the Tiers |
| **Stage** | The audit: how thoroughly a claim was assessed | **Named, never numbered.** Self-Declared, Third-Party Assessed, Continuously Monitored |
| **Layer** | Position in the MAESTRO stack | 1 to 7. This is the only legitimate use of the word |
| **Phase** | Rollout on the roadmap | 1 to 3 |

**An unqualified number always means a Tier.**

### The four Verifiability Tiers

**Tier 1 Assertion** · **Tier 2 Attestation** · **Tier 3 Trust-minimized** · **Tier 4 Self-enforcing**

Proof-of-Control is Tiers 3 and 4. The binary threshold falls between Tier 2 and Tier 3.

**Retired tier names, never use:** "Independently verifiable" and "Openly verifiable" for Tier 3. Both were dropped because an independent verification organisation can claim them, and any Tier 2 operator can truthfully say they have an independent auditor. A name a Tier 2 system can claim cannot mark the threshold.

### The four evidence properties

Binary · **contemporaneous** · tamper-evident · transparent. *Contemporaneous* is the one most often dropped, and it has its own normative subsection.

### The six domains

Provenance · Privacy · Portability · Authorization · Identity · Security.

## Word discipline

| Rule | Why |
| --- | --- |
| **"Prove" and "proof" only for mathematics, cryptography, and the name Proof-of-Control.** Elsewhere: evidence, verifiable, demonstrated, shown | A signature or a zero-knowledge proof proves something. Runtime evidence of what an agent did does not |
| **"Verify", never "check" or "checkable"**, for Proof-of-Control verification. Other senses of check survive | Removed 2026-08-07 |
| **"Open", not "independent"**, when describing our own evidence. *Independent* means independent of the operator, and an independent auditor is still a party you trust, which is Tier 2. *Open* means no party to trust at all | This distinction is the standard's central claim |
| **"Tamper-evident", never "tamper-proof"** | We deliver detection, not impossibility |  <!--aais-allow-->
| **Never "layer" for verification.** Layer belongs to MAESTRO | |
| **Never "guardrails"**. Say defined controls | |  <!--aais-allow-->
| **Never "the only way" or similar absolutes** | Unfalsifiable |  <!--aais-allow-->
| **Spell out "Advanced AI Society" and "Proof-of-Control"** in prose. File and folder names are exempt | |
| **No negative contractions** anywhere: write *do not*, *cannot*, *will not* | |
| **Em dashes only where grammatically correct** | Owner preference |

**Retired, never use:** Trustworthiness Scale · Provability Gap · Proof-of-Control Spectrum · "the new SOC 2" · "verifiable control".  <!--aais-allow-->

## Scope discipline

The standard verifies **adherence, not adequacy**. It shows whether the controls held, never whether they were the right controls. It is verification, not validation. Do not write copy that implies the standard judges whether a control was wise, whether a system is secure, or whether a model's output is correct.

## Working rules

**Never hand-edit a generated artifact to match its source.** `images/diagrams/`, `checklist/`, and `0.1/en/0x94-Appendix-E_Audit-Checklist.md` are produced by `tools/generate_diagrams.py` and `tools/generate_checklist.py`. `docs/use-cases/COVERAGE.md` and the coverage block in `docs/use-cases/README.md` are produced by `tools/generate_use_case_coverage.py`. Change the generator and re-run it. If two files disagree about a number, regenerate the source of truth rather than editing one to match the other.

**Do not add, remove, or reword a normative requirement in a pull request that also does editorial work.** Normative changes need working-group consensus. Open them as a proposal in `docs/proposals/` instead, following `P01-trust-calculus-tiers.md` as the pattern.

**Keep sweeps reviewable.** A terminology rename and a substantive correction belong in separate pull requests, even when they touch the same file.

**Dated records are not edited.** Anything under `docs/reviews/`, change logs, and dated proposals record what was decided at a point in time. Add a dated note beside an entry rather than rewriting it.

**Say what changed and why it is verifiable** in every pull request description. For a normative change, name the requirement and the evidence an assessor would collect.

## Open questions you may run into

Several passages carry `[WG-INPUT NEEDED]`. Those mark decisions the working group has not made. Do not resolve one in a pull request. If your change depends on one, say so in the description and leave the tag in place.

## Where to look first

* `0.1/en/0x03-Using-Proof-of-Control.md` — how the Tiers, Levels and Stages fit together
* `0.1/en/0x10-C08-Verifiability-Tiers.md` — the Tiers and the binary threshold
* `0.1/en/0x93-Appendix-D_Open-Issues.md` — what is still open
* `CONTRIBUTING.md` — how to send a change
* `docs/` — the informative companions
