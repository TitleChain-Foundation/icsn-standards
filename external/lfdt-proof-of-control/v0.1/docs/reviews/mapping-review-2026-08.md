# Independent Review of the Coverage Coding Sheet
<!--aais-record-->

**Date:** August 2026 · **Reviewer:** automated (OpenAI Codex, `gpt-5.1-codex`), one independent pass per framework · **Subject:** [`mappings/coding_sheet.csv`](../../mappings/coding_sheet.csv) at 125 requirements x 8 frameworks = 1,000 coded rows

## Why this exists

The [mapping rubric](../../mappings/rubric.md) calls for two independent coders per framework with Cohen's kappa reported. That study has not been run. The sheet is seed coding by a single coder who also wrote the requirements, which is the weakest possible arrangement: the person most likely to read a framework generously is the person who wants the gap to be real.

This review is not that study. It is one automated pass per framework, asked to find miscodings in both directions and to mark its own confidence. It does not replace the two-coder protocol and no kappa is computed. What it does is give the working group a concrete list to argue with.

## What it found

**192 proposed changes** (180 marked high-confidence) and **96 clause-citation errors**.

| Framework | Proposed changes | Citation errors |
| --- | ---: | ---: |
| OWASP AISVS | 40 | 13 |
| CSA AARM | 33 | 13 |
| Zero Trust (NIST SP 800-207) | 27 | 15 |
| ISO/IEC 42001 | 20 | 6 |
| SOC 2 | 19 | 17 |
| EU AI Act | 19 | 12 |
| NIST AI RMF | 18 | 12 |
| MITRE ATLAS | 16 | 8 |

Direction of the proposed changes:

| Change | Rows | Effect on coverage |
| --- | ---: | --- |
| PM to NM | 91 | reduces |
| EM to PM | 51 | neutral |
| NM to PM | 37 | raises |
| EM to NM | 10 | reduces |
| PM to PM | 3 | neutral |

The net effect of applying everything would be about 64 fewer covered rows out of 1,000, and 9 to 15 points off most frameworks' coverage. **That direction flatters this standard** — lower external coverage means a wider gap for Proof-of-Control to fill — which is a reason for more scrutiny of the downgrades, not less. The review also proposes 37 upgrades where it says the sheet missed a real clause, so it is not uniformly harsh.

## Findings verified independently

These four were checked against the sheet itself or against published framework sources, not taken on the reviewer's word.

### 1. Most citations do not name an auditable clause

A reader cannot check a mapping against "AISVS C12" — that is a chapter of dozens of requirements, and AISVS numbers its requirements `Cx.y.z`. Counting citations that contain a clause-like identifier against those that are only a label or chapter heading:

| Framework | Clause-level | Label only | Share label-only |
| --- | ---: | ---: | ---: |
| CSA AARM | 0 | 60 | 100% |
| OWASP AISVS | 8 | 70 | 90% |
| Zero Trust (NIST SP 800-207) | 30 | 23 | 43% |
| ISO/IEC 42001 | 45 | 27 | 38% |
| SOC 2 | 53 | 15 | 22% |
| MITRE ATLAS | 32 | 6 | 16% |
| EU AI Act | 65 | 0 | 0% |
| NIST AI RMF | 75 | 0 | 0% |

CSA AARM and OWASP AISVS are the worst: essentially none of their citations point at something a reviewer could look up. Stock strings appear across many unrelated requirements — `AISVS C12` on 24 rows, `AISVS C9` on 13, `CSA conformance regime` on 8, `Tenets 3, 4, 6; PEP (§3)` on 8.

### 2. The sheet was coded in blocks, not per requirement

**661 of 1,000 rows carry a rationale that is repeated verbatim on four or more rows.** One rationale covers 26 rows. This is the mechanical signature of section-level coding, and it means the per-requirement granularity the sheet appears to have is partly an illusion: requirements about human oversight, tool-schema validation, credential issuance and path-aware authorization have all inherited the same sentence.

### 3. Every Exact match was contested

All 61 EM ratings in the sheet were challenged by the review. That is worth sitting with. EM means *equivalent in scope and intent*, and this standard's entire thesis is that no existing framework requires operator-independent, mechanism-generated evidence. If the thesis is right, the Exact column should be nearly empty — so a sheet with 61 exact matches was arguing against its own paper.

The clearest case is C10.1, flagged independently by three reviewers. Those requirements describe a conformance statement naming Proof-of-Control's own domains, tiers and evidence streams. No external framework can be *equivalent in scope and intent* to that, because the artifact is defined by this standard. A SOC 2 system description and a management assertion are report elements, not a claim register with tier declarations.

### 4. The MITRE ATLAS coding used a stale mitigation set

The sheet cites AML.M0005, M0007, M0014 and M0015. Checking the current ATLAS mitigation list confirms it also contains **AML.M0023 AI Bill of Materials**, **AML.M0024 AI Telemetry Logging**, **AML.M0025 Maintain AI Dataset Provenance**, and the agent-specific **AML.M0026 / M0027 / M0028** permission-configuration mitigations. All were absent.

This matters because an AI Bill of Materials is close to the same idea as PoC's Agent Bill of Materials (C1.2), and the sheet was citing *Sanitize Training Data* for those rows instead. Correcting it **raises** ATLAS coverage, which is the opposite of the self-serving direction — good evidence the review is doing real work rather than pattern matching toward a wider gap.

## What was applied, and what was not

**Applied (31 rows).** Only changes that could be verified without taking the reviewer's word on a framework's contents:

* The 24 C10.1 Exact ratings on EU AI Act, ISO/IEC 42001 and SOC 2 — verifiable by reading   the PoC requirement text, since the artifact described is PoC-specific.
* 7 MITRE ATLAS rows citing mitigation identifiers confirmed to exist and confirmed absent   from the sheet.

**Not applied (161 rows).** Everything that turns on what a framework's clause actually says — in particular the 91 proposed PM-to-NM downgrades, which carry the coverage numbers and which move them in the direction that flatters this standard. Those need a human with the source document open. They are recorded here so the working group can work through them, and the remaining Exact ratings on OWASP AISVS (16), CSA AARM (13) and Zero Trust (8) should be the first item on that agenda.

## Reproducing this

The prompt, output schema, runner and consolidator are in
[`mappings/review/`](../../mappings/review):

```bash
./mappings/review/run_review.sh              # all eight frameworks, in parallel
python3 mappings/review/consolidate.py       # triage the results
```

The prompt asks for miscodings in both directions, demands a specific clause for every proposal, and instructs the reviewer to mark confidence `low` rather than invent a clause number. Fabricated citations are the obvious failure mode of this method; the ATLAS check above is the spot-check that gave some confidence it was not happening here, and it is the kind of check anyone repeating this should run before believing any of it.

## The honest summary

The coverage percentages in the README and in Table 3 of the paper are **seed-quality estimates with a known upward bias**, and this review is evidence for that rather than a correction of it. The paper already says one coder is not a study; what it did not say, and now does, is that the Exact column was almost certainly wrong and the citations were largely unauditable. Treat the direction of these numbers as informative and the specific values as provisional until the two-coder study in the rubric is actually run.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) — **[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
