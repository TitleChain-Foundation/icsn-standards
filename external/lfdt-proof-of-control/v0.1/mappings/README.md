# Framework Mappings

Proof-of-Control cross-references existing standards and frameworks rather than replacing them:
it is what produces the evidence, alongside them. This directory holds the mapping in two
complementary forms, following the reproducible coverage methodology established by
[HAARF](https://github.com/Task-force-for-AI-agents-in-Healthcare/haarf):

1. **Quantitative coverage mapping** — every one of the 127 Proof-of-Control requirements coded against each
   external framework as Exact Match / Partial Match / No Match, with reproducible coverage
   percentages.
2. **Qualitative crosswalks** — one narrative document per framework explaining the
   relationship, the complementary halves, and the tier-placement caveats.

## How the Mapping Works

| File | What it is |
| --- | --- |
| [`rubric.md`](rubric.md) | The EM / PM / NM match-type definitions, coding instructions, and the coverage formula |
| [`coding_sheet.csv`](coding_sheet.csv) | Row-level coding: 127 requirements × 8 frameworks = 1,016 coded rows with rationales |
| [`compute_coverage.py`](compute_coverage.py) | Validates the sheet and reproduces the coverage percentages and the chart below |
| [`corpus/README.md`](corpus/README.md) | Provenance of the external framework documents (title, version, access URL) |
| [`../docs/reviews/mapping-review-2026-08.md`](../docs/reviews/mapping-review-2026-08.md) | Independent review of all 1,000 rows: what was corrected, what was deferred, and why |
| [`review/`](review) | The cross-model audit: prompt, output schema, runner, and consolidator — so the pass can be repeated or contradicted |

```bash
python3 mappings/compute_coverage.py          # reproduce the numbers
python3 mappings/compute_coverage.py --inject # rewrite the tables in both READMEs
python3 mappings/compute_coverage.py --svg    # regenerate the coverage chart
python3 tools/generate_crosswalks.py          # rebuild the per-framework crosswalk pages
```

## Auditing the coding with a different model

The requirements and this coding sheet were produced by the same party. That is a structural
weakness in any coverage mapping: whoever decides that a framework does not already cover a
requirement is the party that wrote the requirement. The [rubric](rubric.md) calls for two
independent human coders with Cohen's kappa; that study has not been run. <!--aais-allow-->

What can be run cheaply is a **cross-model audit** — ask a model from a different vendor to
review every row, with no access to the original reasoning:

```bash
./mappings/review/run_review.sh              # all eight frameworks, in parallel
python3 mappings/review/consolidate.py       # triage the results
```

The output is a **triage list, not a patch.** The failure mode is fabrication: a model asked for
a clause citation will produce a plausible-looking one, and a fabricated citation is worse than
none because it survives casual review. Three controls address it, and they are where the value
of the exercise lies:

1. **An acceptance rule fixed in advance.** Apply a change only if it can be verified *without*
   trusting the reviewer about a framework's contents. In the 2026 pass this admitted 31 of 192
   proposals.
2. **Check which way the errors point.** If every proposed correction happens to favour your
   standard, that is a finding about the audit, not about the sheet. The 2026 pass proposed 37
   changes that *raised* external coverage, which is why the rest were taken seriously.
3. **Spot-check one factual claim against a published source.** The 2026 pass reported that the
   MITRE ATLAS coding drew on a superseded mitigation set; that was checkable against published
   ATLAS content, and it held.

See [the 2026 review](../docs/reviews/mapping-review-2026-08.md) for what this found and what
was deliberately left unapplied.

## Coverage Results

> **[WG-INPUT NEEDED] — draft seed coding** (single coder, section-granularity, unvalidated;
> see [rubric.md](rubric.md#coding-status)). Numbers will move as the working group ratifies
> row-level codings.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../images/diagrams/mapping-coverage-dark.svg">
    <img alt="Coverage of the 127 Proof-of-Control requirements by external framework" src="../images/diagrams/mapping-coverage-light.svg" width="740">
  </picture>
</p>

Each of the 127 requirements is coded against each framework with one of three **match types**
(defined in the [rubric](rubric.md)):

* **EM · Exact Match** — the framework has a clause equivalent in scope and intent.
* **PM · Partial Match** — the framework covers the same topic, but not at the same depth —
  most often because it requires the *control* without requiring operator-independent
  *evidence* that the control held.
* **NM · No Match** — the framework has no analogous provision.

> **These numbers are seed-quality and biased upward.** An independent review of all 1,000
> coded rows found 192 proposed changes and 96 unauditable citations, and challenged every
> one of the 61 Exact ratings. The clearest errors are corrected; the changes that turn on a
> framework's exact wording are recorded, not applied, because they move coverage in the
> direction that flatters this standard. See
> [the review](../docs/reviews/mapping-review-2026-08.md) before citing any figure below.

<!-- BEGIN GENERATED COVERAGE -->

**Coverage = (EM + PM) / 127 requirements.** Only exact and partial matches count; the NM column is the gap only Proof-of-Control fills.

| Framework | Exact (EM) | Partial (PM) | None (NM) | Coverage |
| --- | :---: | :---: | :---: | :---: |
| [OWASP AISVS](owasp.md) | 16 | 63 | 48 | **62%** |
| [NIST AI RMF](nist-ai-rmf.md) | 0 | 75 | 52 | **59%** |
| [ISO/IEC 42001](iso-iec-42001.md) | 0 | 72 | 55 | **57%** |
| [SOC 2](soc-2.md) | 0 | 68 | 59 | **54%** |
| [EU AI Act](eu-ai-act.md) | 0 | 65 | 62 | **51%** |
| [CSA AARM](csa-aarm.md) | 1 | 55 | 71 | **44%** |
| [Zero Trust (NIST SP 800-207)](zero-trust.md) | 8 | 46 | 73 | **43%** |
| [MITRE ATLAS](mitre-atlas.md) | 0 | 38 | 89 | **30%** |

<!-- END GENERATED COVERAGE -->

**Reading the numbers.** Coverage measures how much of *Proof-of-Control* each framework
already addresses — not the reverse, and not framework quality. Two patterns matter:

* **The PM band is wide and the EM band is nearly empty.** Existing frameworks require most of
  the *controls* Proof-of-Control verifies, but almost never require *operator-independent,
  mechanism-generated evidence* that the controls held. That is the exact gap between Tier 2 and
  Tier 3 — the binary threshold. Five of the eight frameworks now have **zero** exact matches,
  and the [2026 review](../docs/reviews/mapping-review-2026-08.md) challenged every one of the
  remaining 37 — so treat any EM here as unconfirmed.
* **The NM gap concentrates in C7/C8/C10.** No coded framework grades evidence by how
  independently it can be verified (C8), requires trust-assumption disclosure (C7.4/C10.2), or <!--aais-allow-->
  reaches self-enforcing execution (C8.3). The NM gap is, by design, the standard's reason to
  exist.

## Qualitative Crosswalks

| Framework | Type | Relationship to Proof-of-Control | Crosswalk |
| --- | --- | --- | --- |
| MAESTRO (CSA) | Agent threat-modeling framework | Adopted as the System surface (Axis 2) — an axis of the standard, not a coverage target | [maestro.md](maestro.md) |
| CSA AARM | Runtime enforcement standard | Complementary half: AARM enforces, Proof-of-Control evidences | [csa-aarm.md](csa-aarm.md) |
| CSA AI Controls Matrix (AICM) | Control catalog | Crosswalk maintained separately by WG decision | [csa-aicm.md](csa-aicm.md) |
| OWASP (Agentic Top 10, LLM Top 10, AIVSS, AISVS) | Threat catalogs & verification standard | Threat source for the Proof-of-Control threat model; Security-domain alignment target | [owasp.md](owasp.md) |
| MITRE ATLAS | Adversarial threat catalog | Threat source for the Proof-of-Control threat model | [mitre-atlas.md](mitre-atlas.md) |
| NIST AI RMF (& AI 100-2) | Risk-governance framework | Proof-of-Control produces the evidence that makes its requirements verifiable | [nist-ai-rmf.md](nist-ai-rmf.md) |
| ISO/IEC 42001 | AI management system standard | Complementary; supplies the V&V vocabulary Proof-of-Control uses | [iso-iec-42001.md](iso-iec-42001.md) |
| SOC 2 | Organizational attestation | Proof-of-Control is SOC-2-grade in role, with a cryptographic stage SOC 2 never had | [soc-2.md](soc-2.md) |
| EU AI Act | Regulation | Proof-of-Control evidence lets the Act be enforced against evidence, not filings | [eu-ai-act.md](eu-ai-act.md) |
| Zero Trust (NIST SP 800-207; Anthropic Zero Trust for AI Agents) | Security architecture / vendor framework | Zero Trust enforces at runtime; Proof-of-Control shows openly that control held | [zero-trust.md](zero-trust.md) |
| Confidential Computing (TEEs) | Mechanism | One valid mechanism for delivering Proof-of-Control, not the property itself | [confidential-computing.md](confidential-computing.md) |
| AIUC-1 | AI audit / certification framework | Portability-domain alignment target (cross-platform auditing) | [aiuc-1.md](aiuc-1.md) |

## The By-Domain Mapping (working view)

For each domain of verification, the architectural mechanisms that produce the evidence and the
external standards to align with — classified by domain (proposed by Jim Schwoebel of Quome) and
being developed as a graph (led by David Thomson of Tesseract):

| Domain | Source architectural mechanism | Targets for external alignment |
| --- | --- | --- |
| Provenance | *working group to complete* | *to complete* |
| Privacy | TEEs, local-only inference enclaves | HIPAA / HAARF data governance, [EU AI Act](eu-ai-act.md) conformance |
| Portability | Agent Resource Discovery Spec, Open Handshakes | [AIUC-1](aiuc-1.md) cross-platform auditing |
| Authorization | Cryptographic hash chains, ZKML | [SOC 2 Type II](soc-2.md) (proving runtime execution matched policy) |
| Identity | W3C CID, WIMSE / IETF AI-Auth | HAARF audit logs, CSA Vanta Agent Trust Controls |
| Security | [OWASP AIVSS](owasp.md), SSF / CAEP | [OWASP Top 10 for Agentic AI](owasp.md), [NIST AI RMF](nist-ai-rmf.md) |

## Contributing

* **Validate the seed coding:** the highest-value contribution right now. Pick a framework,
  obtain the corpus document ([corpus/README.md](corpus/README.md)), re-code the rows in
  [`coding_sheet.csv`](coding_sheet.csv) per the [rubric](rubric.md), and open a PR with your
  `coder_id`. Second coders enable inter-coder agreement statistics.
* **Extend the corpus:** code a pending framework (AIUC-1, CSA AICM, OWASP Agentic Top 10,
  IEEE 7000-series, HAARF) end-to-end.
* **Improve a crosswalk:** several qualitative crosswalks are marked
  **[WG-INPUT NEEDED] — volunteer needed**.

To take any of these on, join a working group:
**[advancedaisociety.org](https://advancedaisociety.org/)**.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
