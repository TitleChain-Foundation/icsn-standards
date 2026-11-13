<!-- SPDX-License-Identifier: Apache-2.0 -->
# RFC 0003: M5-MATH — Versioned Mathematical Specifications and Conformance

- **Status:** Draft; proposed RFC number, subject to editor allocation
- **Created:** 2026-11-13
- **Discussion:** PR 83
- **Implementation evidence:** [M5-MATH reference](../external/m5-math/README.md)

## Summary

M5-MATH defines mathematical specifications and reproducibility requirements maintained through the ICSN standards process. Each release identifies its version, reference implementations, test vectors and applicable licenses. M5Labs calculators identify the M5-MATH version they implement. Updates advance through ICSN review and adoption under [GOVERNANCE.md](../GOVERNANCE.md).

This RFC proposes that structure. It does not declare the initial profile Candidate or Stable, or every M5 calculator conformant.

## Problem and affected communities

Calculator authors, scientific referees and independent implementers need stable definitions, reproducible examples and explicit version compatibility. A moving software branch alone cannot identify the mathematical rules applied to a result. The specification must be independently implementable without requiring the M5 runtime or registered services.

## Specification

The terms MUST, SHOULD and MAY express requirements within this proposed profile.

1. A release MUST identify the specification version, ICSN maturity status, exact source revision, file hashes, reference implementations, test-vector version and license scope. Draft, Candidate, Stable and Deprecated follow ICSN governance.
2. Published release artifacts MUST be immutable. Corrections create a new version with a changelog; they MUST NOT silently replace a prior artifact or normalize historical signed bytes.
3. A calculator claiming conformance MUST identify the profile/version implemented, algorithm and parameter versions, input provenance, units, precision, rounding, exceptional-input handling and the test results supporting that claim. It MUST NOT claim conformance beyond the tested profile.
4. A release MUST distinguish normative requirements from illustrative implementation code. An independent implementation MAY use different code while satisfying the same normative outputs and error behavior.
5. Conformance vectors MUST cover valid inputs, boundaries and invalid inputs. Where Python and JavaScript references exist, their common supported domain MUST produce equivalent canonical outputs. A digest demonstrates integrity, not scientific validity or issuer authority.
6. An update MUST identify changed requirements, compatibility effects, new vectors, migration guidance and review evidence. A M5Labs change may propose an ICSN update; it MUST NOT automatically change an adopted standard.
7. Stable adoption MUST have the recorded steward decision and review evidence required by ICSN governance. Scientific referee approval, where required for a scientific result or calculator, is separately scoped to that work and version.

## Initial reference profile

The candidate M5-MATH-001 v0.1.0 snapshot records source revision `ac68847627795dfee226d302f8e57fa62a21fdca`. It covers canonical JSON/hashing, value-receipt validation and the proposed M5Nash calculation with Python/JavaScript vectors. Its existing payload remains unchanged. M5Nash weights remain PROPOSED without economic consequences in this reference profile; this does not describe every operational M5 system.

Sharpe–Rivin, Rivin–Jones and other M5Labs calculator families MAY propose additional profiles. This RFC does not claim their formulas, data or conformance have already been incorporated into this snapshot.

## Public adoption, licensing and registered operation

Anyone may independently implement and adopt the published specification and software under their stated licenses. Apache software retains its applicable patent permissions and is not subject to extra Cyrus, registration or membership conditions. Cyrus governs only expressly designated constitutional materials. Papers, datasets, model weights and marks retain their separately stated terms. The [license matrix](../LICENSES/LICENSE-MATRIX.md) and exact release notices identify scope; a proposed designation is not an effective release grant.

Activating a sovereign account through the TitleChain Registry establishes its registered operating context, activates the applicable Cyrus Protocol obligations and registers its ICSN namespace for the person, entity, cooperative, agency or government, within the authority actually verified for that account. This registered-service relationship is separate from independent software adoption or standards participation.

M5 is operating internally, including transaction, transfer, tokenization and internally authorized M5-CV workflows, as clarified by management. External agency/government M5-CV activation remains separate. Simulation results retain their simulation labels. Neither a calculation nor standards adoption issues an external credential or establishes legal authority.

## Human rights, consent and inclusion

Independent implementation and standards participation require no paid operating account. Reference inputs MUST exclude private identity, patient, wallet, credential and company financial records unless separately authorized for publication. Public vectors SHOULD use synthetic examples with documented limits. Accessibility, portability and accountable human review remain applicable to consequential scientific uses.

## Privacy, security and automation

A conforming mathematical result is not an authorization to execute a transaction. Agents may calculate and propose results; consequential effects require their separate scoped authority and human approvals. Implementers MUST identify unsupported inputs and invalid or unavailable evidence rather than silently substitute a favorable result. Conformance materials MUST NOT publish secrets or imply that a sample key is a live trust root.

## Alternatives and tradeoffs

Keeping only a moving implementation snapshot gives weaker version and compatibility guarantees. Automatically adopting every calculator update would bypass review. A versioned specification with separate reference artifacts adds explicit release work while allowing independent implementations and deliberate compatibility decisions.

## Review and acceptance

Editors confirm numbering and completeness; reviewers assess mathematical requirements, vector coverage, licenses, privacy/security and independent implementability. The initial snapshot has an explicit user-directed Apache release record binding its source, files and hashes. Release-record checks remain separate from adopting this RFC's standards structure. Candidate and Stable decisions are recorded through ICSN governance.
