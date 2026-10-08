# Mapping Corpus Provenance

This directory documents the external framework sources used for the Proof-of-Control coverage
mapping. The documents themselves are not redistributed (copyright); instead we provide
citations, versions, and access instructions so reviewers can independently obtain the same
corpus and reproduce the coding.

## Coded Source Documents

### 1. EU AI Act (`EU_AI_Act`)

* **Title:** Regulation (EU) 2024/1689 — Artificial Intelligence Act
* **Version:** Official Journal of the European Union, 12 July 2024
* **Access:** <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>

### 2. NIST AI Risk Management Framework (`NIST_AI_RMF`)

* **Title:** Artificial Intelligence Risk Management Framework (AI RMF 1.0)
* **Version:** NIST AI 100-1, January 2023 (with the Generative AI Profile, NIST AI 600-1)
* **Access:** <https://www.nist.gov/itl/ai-risk-management-framework>

### 3. ISO/IEC 42001 (`ISO_42001`)

* **Title:** Information technology — Artificial intelligence — Management system
* **Version:** ISO/IEC 42001:2023
* **Access:** <https://www.iso.org/standard/81230.html>

### 4. SOC 2 (`SOC_2`)

* **Title:** AICPA Trust Services Criteria (security, availability, processing integrity,
  confidentiality, privacy)
* **Version:** 2017 TSC with 2022 revised points of focus
* **Access:** <https://www.aicpa-cima.com/resources/download/trust-services-criteria>

### 5. OWASP AISVS (`OWASP_AISVS`)

* **Title:** OWASP Artificial Intelligence Security Verification Standard
* **Version:** v1.0 (June 2026)
* **Access:** <https://github.com/OWASP/AISVS>

### 6. MITRE ATLAS (`MITRE_ATLAS`)

* **Title:** MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems),
  techniques and mitigations
* **Version:** Living catalog, as accessed August 2026
* **Access:** <https://atlas.mitre.org/>

### 7. CSA AARM (`CSA_AARM`)

* **Title:** Cloud Security Alliance — Autonomous Action Runtime Management (contributed by
  Vanta)
* **Version:** v1.0 (R1–R9; the GitHub repository metadata reports 2.0 — discrepancy noted)
* **Access:** <https://aarm.dev/spec> (specification text, CC BY 4.0) and
  <https://github.com/aarm-dev/aarm> (source). The CSA working-group page carries no
  specification text, so it is not a corpus source for this coding.

### 8. Zero Trust Architecture (`NIST_SP_800_207`)

* **Title:** NIST Special Publication 800-207 — Zero Trust Architecture
* **Version:** August 2020
* **Access:** <https://csrc.nist.gov/pubs/sp/800/207/final>

## Pending Corpus (not yet coded)

These frameworks have qualitative crosswalks in [`mappings/`](../) but no row-level coding yet —
volunteers welcome ([sign up at advancedaisociety.org](https://advancedaisociety.org/)):

| Framework | Status |
| --- | --- |
| AIUC-1 | Corpus access pending; Portability-domain alignment target ([aiuc-1.md](../aiuc-1.md)) |
| CSA AI Controls Matrix (AICM) | Ken Huang's crosswalk to be merged ([csa-aicm.md](../csa-aicm.md)) |
| CSA MAESTRO | Adopted as the System surface (an axis of the standard, not a coverage target) — [maestro.md](../maestro.md) |
| Anthropic Zero Trust for AI Agents | Vendor framework, May 2026 ([zero-trust.md](../zero-trust.md)) |
| Confidential Computing (CCC) | Mechanism, not a clause-coded framework ([confidential-computing.md](../confidential-computing.md)) |
| OWASP Agentic Top 10 / AIVSS, IEEE 7000-series, IMDRF, HAARF | Candidate additions raised by the working group |

## Reproduction Instructions

1. Obtain each document from the URLs above (or your organization's standards library).
2. Use [`mappings/rubric.md`](../rubric.md) for the EM/PM/NM match-type definitions.
3. The row-level coding is in [`mappings/coding_sheet.csv`](../coding_sheet.csv); requirement
   IDs come from [`checklist/poc-checklist.csv`](../../checklist/poc-checklist.csv).
4. Run `python3 mappings/compute_coverage.py` to reproduce the coverage percentages (the script
   also validates that every requirement is coded exactly once per framework).
