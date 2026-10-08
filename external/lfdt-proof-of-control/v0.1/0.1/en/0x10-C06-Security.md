# C6 Security

## Control Objective

Produce verifiable evidence of system integrity and access-control enforcement. This domain covers hardware attestation, runtime integrity verification, confidential compute, on-chip compliance, and evidence that security controls held during execution.

*Verifiable facts: integrity of the execution environment and that controls held; tools invoked.*

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../images/diagrams/c6-security-dark.svg">
    <img alt="The execution environment attests its measurement to an independent verifier against published reference values; evidence-signing keys live in an HSM" src="../../images/diagrams/c6-security-light.svg" width="900">
  </picture>
</p>

---

## C6.1 Execution Environment Integrity

Evidence that the environment the agent ran in is the environment that was authorized, and that the declared controls held while it ran.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **Verify that** the conformance claim enumerates the security controls it declares (by identifier), and that each declared control is mapped to a named evidence stream that shows it operating — no declared control without a corresponding evidence source. | 1 |
| **6.1.2** | **Verify that** every tool invocation is written to the execution record with the tool identifier, the full argument set (or its digest where arguments are sensitive), the result status, and a timestamp. | 1 |
| **6.1.3** | **Verify that** the runtime environment produces a signed attestation report (TEE or remote attestation) at startup and on configuration change, and that reports are automatically compared against maintained golden reference values, with mismatches alerting and recorded. | 2 |
| **6.1.4** | **Verify that** hardware-rooted attestation (TPM/GPU/CPU endorsement) covers each component named as a dependency by a higher-layer control in the claim's control-to-evidence mapping. | 3 |

**Auditor evidence:** 6.1.1 — the control-to-evidence mapping table; pick two declared controls and pull their evidence streams. 6.1.2 — sampled tool-call records reconciled against downstream system logs. 6.1.3 — attestation reports, the golden-value register and its change history, and one recorded mismatch alert (test it). 6.1.4 — the dependency list and per-component attestation coverage.

---

## C6.2 Isolation and Confidential Execution

Proof of process isolation is required whenever agents execute generated code or interact with un-sanitized external tools.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **Verify that** generated code and un-sanitized external tools execute in a sandbox (container, microVM, or enclave) whose isolation configuration is recorded per execution, and that sandbox-escape attempts surface as recorded security events. | 2 |
| **6.2.2** | **Verify that** workloads classified as sensitive run in confidential-compute environments whose attestation an external party can validate against published reference values. | 3 |
| **6.2.3** | **Verify that** where on-chip compliance enforcement is claimed, the hardware mechanism gates execution (not merely reports), and its attestation is continuously validated during operation. | 4 |

**Auditor evidence:** 6.2.1 — sandbox configuration per sampled execution; a recorded escape-attempt event from testing. 6.2.2 — validate one confidential-compute attestation independently. 6.2.3 — demonstrate in test that execution halts when the on-chip check fails. <!--aais-allow-->

---

## C6.3 Cryptographic Key Lifecycle

Every mechanism in this standard ultimately rests on keys. A signing key with no rotation schedule and no compromise-recovery path silently converts mechanism-generated evidence back into operator-trusted evidence.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.3.1** | **Verify that** evidence-signing and attestation keys are generated in and non-exportable from hardware-backed key management (HSM or equivalent), per the key inventory. | 2 |
| **6.3.2** | **Verify that** each evidence-producing key has a documented rotation schedule, that rotations occur on schedule, and that each rotation writes a signed record linking the old and new key identities. | 2 |
| **6.3.3** | **Verify that** the documented key-compromise procedure includes revocation, identification of all evidence signed by the affected key (queryable by key ID), re-grading of affected claims, and notification of relying parties — and that the procedure has been exercised at least annually. | 2 |
| **6.3.4** | **Verify that** every evidence record and capability identifies the signature algorithm used, and that the conformance claim declares a cryptographic migration path — so a verifier knows what to check and an operator can change algorithms without invalidating already-published evidence. | 2 |
| **6.3.5** | **Verify that** where the declared evidence retention period ([C7.6.5](0x10-C07-Evidence-Generation-and-Properties.md)) extends beyond the period for which the signature scheme is projected to remain unforgeable, the implementation uses a post-quantum or hybrid signature scheme (e.g., FIPS 204 ML-DSA), or re-anchors and re-signs retained evidence under a current scheme before the projection lapses. Evidence is only worth what its signature is worth at the moment it is examined. | 3 |

**Auditor evidence:** 6.3.1 — key inventory with HSM attributes; confirm non-exportability settings. 6.3.2 — rotation schedule vs. actual rotation records; verify one old-to-new linking record. 6.3.3 — the procedure document and the most recent exercise report; run a query for evidence by key ID. 6.3.4 — sampled records carrying an algorithm identifier, plus the declared migration path. 6.3.5 — compare the declared retention period against the scheme's projected viability; if retention is longer, confirm PQ/hybrid signing or an executed re-signing cycle.

---

## References

* [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/) and OWASP AIVSS — Security-domain alignment targets
* [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — Security-domain external alignment target
* [FIPS 204 ML-DSA](https://csrc.nist.gov/pubs/fips/204/final) · [FIPS 205 SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final) — post-quantum signatures for long-lived evidence (C6.3.5); measured cost in [`impl/`](../../impl/README.md#post-quantum-signing)
* [MITRE ATLAS](https://atlas.mitre.org/)
* Crosswalks: [Confidential Computing](../../mappings/confidential-computing.md), [MAESTRO L4 runtime attestation](0x91-Appendix-B_Proof-Mechanism-Inventory.md), [OWASP](../../mappings/owasp.md), [NIST AI RMF](../../mappings/nist-ai-rmf.md)
