# Appendix E: Audit Checklist (generated)

> **Generated file — do not edit by hand.** Rebuild with `python3 tools/generate_checklist.py` after changing any requirement chapter. Machine-readable exports live in [`checklist/`](../../checklist).

Tick items as you close them out; each chapter's *Auditor evidence* notes say what to collect and what to test per requirement. Levels are cumulative and align 1:1 with the Verifiability Tiers — clearing every Level 1–3 item in the claimed domains is the minimum for a Proof-of-Control claim ([Using Proof-of-Control](0x03-Using-Proof-of-Control.md)).

**Level key:** L1 Recorded · L2 Attested · L3 Trust-minimized · L4 Self-Enforcing / Continuous

## Coverage Matrix

| Chapter | L1 | L2 | L3 | L4 | Total |
| --- | :---: | :---: | :---: | :---: | :---: |
| [C1 Provenance](0x10-C01-Provenance.md) | 3 | 6 | 4 | — | **13** |
| [C2 Privacy](0x10-C02-Privacy.md) | 3 | 7 | 2 | 1 | **13** |
| [C3 Portability](0x10-C03-Portability.md) | 1 | 2 | 2 | — | **5** |
| [C4 Authorization](0x10-C04-Authorization.md) | 2 | 7 | 3 | — | **12** |
| [C5 Identity](0x10-C05-Identity.md) | 1 | 3 | 2 | — | **6** |
| [C6 Security](0x10-C06-Security.md) | 2 | 6 | 3 | 1 | **12** |
| [C7 Evidence Generation and Properties](0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 8 | 13 | 1 | **28** |
| [C8 Verifiability Tiers and the Binary Threshold](0x10-C08-Verifiability-Tiers.md) | 7 | — | 3 | 5 | **15** |
| [C9 System Surface (MAESTRO)](0x10-C09-System-Surface-MAESTRO.md) | 3 | 2 | 1 | — | **6** |
| [C10 Conformance and Trust-Assumption Disclosure](0x10-C10-Conformance-and-Disclosure.md) | 7 | 4 | 2 | 4 | **17** |
| **All chapters** | **35** | **45** | **35** | **12** | **127** |

## Requirements by Level

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../images/diagrams/checklist-levels-dark.svg">
    <img alt="127 requirements by level: 35 at Level 1 (Recorded),  45 at Level 2 (Attested),  35 at Level 3 (Trust-minimized),  12 at Level 4 (Self-Enforcing / Continuous)" src="../../images/diagrams/checklist-levels-light.svg" width="620">
  </picture>
</p>

## C1 Provenance

### C1.1 Model and Artifact Provenance

- [ ] **1.1.1** `L1` — **Verify that** every execution record includes the cryptographic digest (e.g., SHA-256) of the model weights and serving configuration that produced the output, not only a product or version name.
- [ ] **1.1.2** `L2` — **Verify that** at model load time the digest of the deployed weights is compared against a signed model manifest, and that each comparison result (pass or fail) is written to the execution record.
- [ ] **1.1.3** `L2` — **Verify that** the signature chain over model artifacts — base weights, fine-tuning steps, serving config — validates end-to-end using signing keys enrolled in a maintained list of authorized providers, and that chain-validation failures block deployment.
- [ ] **1.1.4** `L2` — **Verify that** the artifact-admission control rejects models, tools, and plugins that lack a valid attestation, and that each rejection event is recorded with the artifact identifier and reason.
- [ ] **1.1.5** `L3` — **Verify that** model supply-chain provenance is published in a standard, externally verifiable attestation format (e.g., SLSA provenance / in-toto), so a party outside the organization can validate the build chain without operator assistance.
### C1.2 Input and Data Lineage

- [ ] **1.2.1** `L1` — **Verify that** each input that steers agent behavior (prompts, retrieved documents, memory reads, tool outputs) is recorded at ingestion with a source identifier and timestamp.
- [ ] **1.2.2** `L2` — **Verify that** input records are hash-linked to the execution records of the actions whose context they were present in at evaluation time, forming a custody chain a reviewer can walk from origin to action.
- [ ] **1.2.3** `L2` — **Verify that** each transformation applied to data feeding the agent (chunking, embedding, redaction, enrichment) appends an entry to a hash-linked, append-only log naming the process, its version, and digests of input and output.
- [ ] **1.2.4** `L3` — **Verify that** training-data lineage and licensing attestations for the model in use are obtainable by an external verifier, and that the conformance claim links to them.
### C1.3 Compute Substrate Provenance

- [ ] **1.3.1** `L2` — **Verify that** the execution record identifies the compute environment that ran the workload (host or cluster identity, environment image digest).
- [ ] **1.3.2** `L3` — **Verify that** substrate identity is backed by a hardware or remote attestation report that a party outside the organization can validate against published reference values.
### C1.4 Privacy-Preserving Provenance

- [ ] **1.4.1** `L1` — **Verify that** provenance records retain digests, commitments, or redacted derivations of payloads — not raw payloads — wherever the data handled is subject to minimization requirements.
- [ ] **1.4.2** `L3` — **Verify that** an external verifier can confirm a provenance claim about confidential inputs (e.g., via hash comparison or selective disclosure) without being shown the underlying data.

*Auditor evidence for these items: see [C1](0x10-C01-Provenance.md).*

## C2 Privacy

### C2.1 Data-Access Evidence

- [ ] **2.1.1** `L1` — **Verify that** every data read and write performed by the agent is recorded with the data-store identifier, record or object reference, operation type, and timestamp.
- [ ] **2.1.2** `L2` — **Verify that** privacy evidence records contain identifiers, digests, or classifications of the data touched — never the protected content itself — and that a periodic scan of the evidence store confirms this.
- [ ] **2.1.3** `L1` — **Verify that** each execution record distinguishes data *used* by the agent from data *disclosed* to an output, tool, or third party, as separate fields a reviewer can query.
### C2.2 Policy and Consent Enforcement

- [ ] **2.2.1** `L2` — **Verify that** each data access is evaluated against the applicable consent record before execution, and that the evaluation result — including denials — is written to the execution record.
- [ ] **2.2.2** `L2` — **Verify that** each data access records the declared purpose it was made under, and that accesses whose purpose does not match the data's permitted purposes are blocked and logged.
- [ ] **2.2.3** `L2` — **Verify that** agent data queries are constrained (by scope, field allow-lists, or query rewriting) to the data required for the task, and that the constraint configuration and its enforcement events are recorded.
- [ ] **2.2.4** `L2` — **Verify that** license and data-residency constraints are encoded as machine-enforced rules (e.g., region pinning, license tags), and that rule evaluations at execution are recorded.
- [ ] **2.2.5** `L2` — **Verify that** where deidentified data is used, the deidentification step logs the method and version applied, and re-identification attempts (joins against restricted sources) are blocked and logged.
### C2.3 Privacy-Preserving Verification Mechanisms

- [ ] **2.3.1** `L3` — **Verify that** where evidence at Tier 3 would re-leak protected inputs, the implementation substitutes a zero-knowledge proof of policy adherence, a selective disclosure, or a commitment — and that an external verifier can validate it without seeing the inputs.
- [ ] **2.3.2** `L3` — **Verify that** consent records are committed to (hashed and anchored) at the time consent is captured, so a later consent record can be proven unaltered and not backdated.
- [ ] **2.3.3** `L4` — **Verify that** computations over confidential inputs produce a proof of correct execution (verifiable computation) that gates the release of the result.
### C2.4 Evidence Handling for Protected Data

- [ ] **2.4.1** `L1` — **Verify that** evidence retained beyond the execution window contains only derived or minimized forms of protected data (hashes, commitments, selective disclosures), enforced by the evidence-pipeline schema rather than by convention.
- [ ] **2.4.2** `L2` — **Verify that** a documented procedure reconciles data-subject deletion requests with tamper-evident evidence — e.g., crypto-shredding encrypted payloads while retaining hash-bound proofs — and that at least one executed deletion demonstrates the chain remains verifiable afterward.

*Auditor evidence for these items: see [C2](0x10-C02-Privacy.md).*

## C3 Portability

### C3.1 Boundary-Crossing Evidence

- [ ] **3.1.1** `L1` — **Verify that** each organizational, jurisdictional, and compute boundary crossing writes an execution-record entry identifying the source environment, destination environment, and what crossed (data digests, agent state, credentials).
- [ ] **3.1.2** `L2` — **Verify that** integrity of data and agent state is checked at the destination side of each crossing — digest recomputed or signature validated — and that the check result is recorded on both sides.
### C3.2 Cross-Environment Continuity

- [ ] **3.2.1** `L2` — **Verify that** evidence generated before a cross-cloud or cross-vendor migration remains validatable after it: keys, reference values, and verification tooling for the old environment stay published for the retention period.
- [ ] **3.2.2** `L3` — **Verify that** when evidence crosses attestation domains, a signed linking record binds the last record of the source chain to the first record of the destination chain, so an external verifier can confirm there is no gap.
- [ ] **3.2.3** `L3` — **Verify that** a documented cross-jurisdiction review determines, per jurisdiction pair, what each evidence artifact discloses, and that artifacts exceeding the destination's permitted disclosure are transformed (re-proven, redacted) before transfer.

*Auditor evidence for these items: see [C3](0x10-C03-Portability.md).*

## C4 Authorization

### C4.1 Authority and Scope Enforcement

- [ ] **4.1.1** `L1` — **Verify that** the authority granted to the agent — the permission set, its scope, and its expiry — is written to the execution record before the first action executes under it.
- [ ] **4.1.2** `L1` — **Verify that** every action is evaluated against the granted permission set at execution time, and that the evaluation record names the permission matched (or the denial reason) for each action.
- [ ] **4.1.3** `L3` — **Verify that** actions outside the granted scope are blocked at the interception gateway — not merely flagged — and that each block writes a rejection record with the attempted action and its parameters.
- [ ] **4.1.4** `L2` — **Verify that** tool-call parameters are validated against the registered tool schema at execution time, that out-of-schema calls are rejected, and that the validated parameter digest is stored in the execution record.
- [ ] **4.1.5** `L2` — **Verify that** agent credentials are issued per task with scope and expiry bound to that task (e.g., short-lived tokens), and that no standing broad-scope credential is available to the agent at runtime.
- [ ] **4.1.6** `L2` — **Verify that** each human approval or override writes a record containing the approver's authenticated identity, the exact content presented for approval, the decision, and its timestamp.
- [ ] **4.1.7** `L2` — **Verify that** authorization evaluation is path-aware: the evaluated context for each invocation includes parameters and state carried from upstream invocations in the same execution path, so that a composed sequence of individually authorized calls cannot silently exceed the authority of its steps. *(Research-driven addition — see [Appendix D, issue 12](0x93-Appendix-D_Open-Issues.md).)*
- [ ] **4.1.8** `L2` — **Verify that** outputs of diagnostic, advisory, or audit tools cannot raise the authorization state of subsequent actions: approval thresholds are evaluated against the original grant, not against accumulated execution context. *(Research-driven addition — see [Appendix D, issue 12](0x93-Appendix-D_Open-Issues.md).)*
### C4.2 Delegation

- [ ] **4.2.1** `L2` — **Verify that** each action's signed authorization token is cryptographically validated (signature, expiry, audience, scope) before execution, and that validation results are recorded.
- [ ] **4.2.2** `L2` — **Verify that** each hop in a delegation chain carries the delegator's signature, and that the full chain validates back to the originating principal before the delegated authority is exercised.
- [ ] **4.2.3** `L3` — **Verify that** the delegation mechanism structurally prevents a delegate's permission set from exceeding the delegator's (scope intersection on issuance), and that attempted escalations are rejected and recorded.
- [ ] **4.2.4** `L3` — **Verify that** where the delegation chain is confidential, the relying party receives a proof of policy-compliant delegation (e.g., ZK credential presentation) it can validate without seeing the chain.

*Auditor evidence for these items: see [C4](0x10-C04-Authorization.md).*

## C5 Identity

### C5.1 Agent and Principal Binding

- [ ] **5.1.1** `L1` — **Verify that** every execution record carries the agent instance identifier and the principal identifier on whose behalf the action ran, so any sampled action resolves to a named principal.
- [ ] **5.1.2** `L2` — **Verify that** the agent authenticates with a cryptographic credential (certificate, key pair, or DID) validated before actions execute, and that credential-validation events are recorded.
- [ ] **5.1.3** `L2` — **Verify that** each agent tool call carries a delegation token (short-lived OAuth/JWT, W3C verifiable credential, or capability URL) issued by or on behalf of the principal, cryptographically linking the call to the principal's grant.
- [ ] **5.1.4** `L3` — **Verify that** the agent's identity credential is bound to an attested execution environment (key held in the attested enclave or TPM), so the credential cannot be exercised from an environment that fails attestation.
### C5.2 Inter-Agent Identity

- [ ] **5.2.1** `L2` — **Verify that** agent-to-agent messages are signed by the sending agent's credential, and that receivers reject and log unsigned or invalidly signed messages.
- [ ] **5.2.2** `L3` — **Verify that** the receiving party can validate sender identity and message integrity using published key material, without contacting the sender's operator.

*Auditor evidence for these items: see [C5](0x10-C05-Identity.md).*

## C6 Security

### C6.1 Execution Environment Integrity

- [ ] **6.1.1** `L1` — **Verify that** the conformance claim enumerates the security controls it declares (by identifier), and that each declared control is mapped to a named evidence stream that shows it operating — no declared control without a corresponding evidence source.
- [ ] **6.1.2** `L1` — **Verify that** every tool invocation is written to the execution record with the tool identifier, the full argument set (or its digest where arguments are sensitive), the result status, and a timestamp.
- [ ] **6.1.3** `L2` — **Verify that** the runtime environment produces a signed attestation report (TEE or remote attestation) at startup and on configuration change, and that reports are automatically compared against maintained golden reference values, with mismatches alerting and recorded.
- [ ] **6.1.4** `L3` — **Verify that** hardware-rooted attestation (TPM/GPU/CPU endorsement) covers each component named as a dependency by a higher-layer control in the claim's control-to-evidence mapping.
### C6.2 Isolation and Confidential Execution

- [ ] **6.2.1** `L2` — **Verify that** generated code and un-sanitized external tools execute in a sandbox (container, microVM, or enclave) whose isolation configuration is recorded per execution, and that sandbox-escape attempts surface as recorded security events.
- [ ] **6.2.2** `L3` — **Verify that** workloads classified as sensitive run in confidential-compute environments whose attestation an external party can validate against published reference values.
- [ ] **6.2.3** `L4` — **Verify that** where on-chip compliance enforcement is claimed, the hardware mechanism gates execution (not merely reports), and its attestation is continuously validated during operation.
### C6.3 Cryptographic Key Lifecycle

- [ ] **6.3.1** `L2` — **Verify that** evidence-signing and attestation keys are generated in and non-exportable from hardware-backed key management (HSM or equivalent), per the key inventory.
- [ ] **6.3.2** `L2` — **Verify that** each evidence-producing key has a documented rotation schedule, that rotations occur on schedule, and that each rotation writes a signed record linking the old and new key identities.
- [ ] **6.3.3** `L2` — **Verify that** the documented key-compromise procedure includes revocation, identification of all evidence signed by the affected key (queryable by key ID), re-grading of affected claims, and notification of relying parties — and that the procedure has been exercised at least annually.
- [ ] **6.3.4** `L2` — **Verify that** every evidence record and capability identifies the signature algorithm used, and that the conformance claim declares a cryptographic migration path — so a verifier knows what to check and an operator can change algorithms without invalidating already-published evidence.
- [ ] **6.3.5** `L3` — **Verify that** where the declared evidence retention period ([C7.6.5](0x10-C07-Evidence-Generation-and-Properties.md)) extends beyond the period for which the signature scheme is projected to remain unforgeable, the implementation uses a post-quantum or hybrid signature scheme (e.g., FIPS 204 ML-DSA), or re-anchors and re-signs retained evidence under a current scheme before the projection lapses. Evidence is only worth what its signature is worth at the moment it is examined.

*Auditor evidence for these items: see [C6](0x10-C06-Security.md).*

## C7 Evidence Generation and Properties

### C7.1 Generation at the Action Boundary

- [ ] **7.1.1** `L3` — **Verify that** all agent tool and effect invocations are routed through an Action Interception Gateway that runs as a separate process or service from the agent — the agent has no network or credential path to its tools that bypasses the gateway.
- [ ] **7.1.2** `L3` — **Verify that** for each intercepted action the gateway emits evidence records at three points — request received (before), effect performed (during), and result returned (after) — each independently signed and linkable to the same action ID.
- [ ] **7.1.3** `L3` — **Verify that** the architecture makes evidence emission a precondition of action release: the gateway does not forward the action to the tool until the *before* record is durably written.
- [ ] **7.1.4** `L3` — **Verify that** the effect channel is mediated within the same trust boundary as policy evaluation, by at least one of: (a) the credentials and transport for the effect are held inside the attesting environment, which emits the request itself; (b) the mechanism releases a single-use capability cryptographically bound to the evaluated snapshot digest and target resource, which the relying party checks before executing; or (c) egress is confined to an attested enforcement point that admits only requests carrying matching evidence. The conformance claim states which.
- [ ] **7.1.5** `L1` — **Verify that** the claim does not assert that evidence describes executed actions unless 7.1.4 is met — a system evidencing evaluation but not mediating the effect channel may claim Tier 1–2 only.
### C7.2 The Contemporaneous Property

- [ ] **7.2.1** `L1` — **Verify that** each evidence record is written within the executing transaction of the action it describes — not batch-reconstructed later — and carries the capture timestamp of the event itself.
- [ ] **7.2.2** `L3` — **Verify that** evidence timestamps are anchored to a source outside the operator's control — an RFC 3161 timestamp authority, transparency-log inclusion proof, or consensus time — at least once per defined anchoring interval.
- [ ] **7.2.3** `L3` — **Verify that** the conformance claim states a maximum **attestation refresh interval** — the longest period, or the largest number of actions, for which evidence may rest on a hardware measurement taken before them — and that the mechanism refreshes within it or refuses to continue.
- [ ] **7.2.4** `L3` — **Verify that** the hardware attestation cryptographically **binds the evidence signing key**: the key's digest appears in the attested report body (TDX `REPORTDATA`, SEV-SNP `REPORT_DATA`, or equivalent), so that a verifier establishes *this key ran inside this measured environment* rather than receiving a measurement and a key that merely arrived together.
### C7.3 The Tamper-Evident Property

- [ ] **7.3.1** `L2` — **Verify that** evidence records are hash-chained or Merkle-anchored so that modifying, inserting, or reordering any record invalidates the chain, and that chain verification runs on a defined schedule with results recorded.
- [ ] **7.3.2** `L3` — **Verify that** evidence records are signed by keys held by the generating mechanism (gateway, enclave, or logging service) that operator and agent identities cannot access, per the key-custody configuration.
- [ ] **7.3.3** `L3` — **Verify that** the implementation resists equivocation (presenting divergent histories to different relying parties) by at least one of: cross-verifier consistency checking (gossip), a witness quorum co-signing chain roots, or anchoring to a ledger with single-history consensus — and that the mechanism is named in the claim.
- [ ] **7.3.4** `L3` — **Verify that** the evidence log is structured so a verifier can establish that a **single named record** is present in the log committed to by a published root, without retrieving the rest of the log — by an inclusion proof against an append-only Merkle tree ([RFC 6962](https://www.rfc-editor.org/rfc/rfc6962)) or equivalent — and that the proof, the tree size it is taken against, and the published root are all obtainable by the verifier.
- [ ] **7.3.5** `L3` — **Verify that** a published root is checked for **append-only consistency** against previously published roots, by a consistency proof or equivalent, and that the verification procedure compares the recomputed root against the anchored value rather than only against a step count or record count.
### C7.4 The Transparent Property

- [ ] **7.4.1** `L1` — **Verify that** the published trust-assumption disclosure ([C10.2](0x10-C10-Conformance-and-Disclosure.md)) lists, for each evidence mechanism in use, every party, hardware element, and mathematical assumption that must hold for the evidence to be believed.
### C7.5 The Determinism Boundary

- [ ] **7.5.1** `L1` — **Verify that** every field in the evidence schema records an observable execution fact (identifier, digest, timestamp, decision result) — the schema contains no field asserting quality, correctness, or intent.
- [ ] **7.5.2** `L1` — **Verify that** the conformance statement and public product claims describe the evidence only as execution facts, and that a documented claims review (legal or compliance sign-off) confirms no claim of output correctness, fairness, or model intent is attributed to Proof-of-Control.
### C7.6 Evidence Custody and Resilience

- [ ] **7.6.1** `L2` — **Verify that** evidence-pipeline failures (write errors, signing errors, store unavailability) raise a monitored alert and are themselves written as failure events to a secondary durable log.
- [ ] **7.6.2** `L2` — **Verify that** evidence records carry per-source monotonic sequence numbers (or equivalent chaining), so a verifier can detect a missing record from the sequence gap alone.
- [ ] **7.6.3** `L4` — **Verify that** when evidence cannot be generated at the claimed Tier, in-scope actions are refused by the gateway until the pipeline recovers — demonstrated by a fail-closed test on the evidence store.
- [ ] **7.6.4** `L2` — **Verify that** the evidence store enforces role-based access, and that every read of evidence writes its own access record (who, what, when).
- [ ] **7.6.5** `L1` — **Verify that** the retention period for evidence is stated in the conformance claim, configured in the store's retention policy, and at least as long as the period the claim covers.
- [ ] **7.6.6** `L3` — **Verify that** the chain root is anchored externally within a declared maximum interval, that the interval is stated in the claim (it bounds the window in which head truncation is undetectable), and that a missed anchoring deadline raises an alert.
### C7.7 The Interoperable Property

- [ ] **7.7.1** `L2` — **Verify that** the evidence claim set is defined by a **machine-readable schema** covering every field, published where a verifier can obtain it, and that the deployed implementation's own output validates against it.
- [ ] **7.7.2** `L2` — **Verify that** the schema declares a single **canonical serialization** — fixing key ordering, number formatting, string escaping, digest case, and the meaning of an absent field — and states exactly which bytes each digest and signature covers.
- [ ] **7.7.3** `L2` — **Verify that** every digest and signature carries an explicit **algorithm identifier**, and that a verifier presented with an unidentified digest rejects it rather than assuming an algorithm.
- [ ] **7.7.4** `L3` — **Verify that** conformance to the canonical form is demonstrated against **published test vectors including negative cases**, and that each negative vector is rejected for the reason it was written to test.
- [ ] **7.7.5** `L2` — **Verify that** a parser rejects duplicate object keys rather than resolving them last-wins, so that one evidence artifact cannot mean different things to different readers.

*Auditor evidence for these items: see [C7](0x10-C07-Evidence-Generation-and-Properties.md).*

## C8 Verifiability Tiers and the Binary Threshold

### C8.1 Tier Placement

- [ ] **8.1.1** `L1` — **Verify that** the claim register records an assigned Tier (1–4) for every claim, with no unassigned entries.
- [ ] **8.1.2** `L1` — **Verify that** each claim's register entry includes a written trust analysis naming every party that must be trusted for the evidence to hold (operator, signer, CA, chip vendor, ceremony participants), and that the assigned Tier is consistent with that list — any single trusted party caps the claim at Tier 2.
- [ ] **8.1.3** `L1` — **Verify that** claims whose trust analysis names a single trusted party — operator-signed logs, single-party trusted setups, vendor-rooted attestations, centralized Merkle trees, permissioned ledgers — are registered at Tier 2 or below.
- [ ] **8.1.4** `L1` — **Verify that** the words "Proof-of-Control" appear in the conformance statement and marketing claims only for claims registered at Tier 3 or 4, confirmed by the documented claims review.
- [ ] **8.1.5** `L3` — **Verify that** for each Tier 3+ claim, an external party can obtain the evidence and complete verification using only published materials — demonstrated by a recorded verification run performed without operator credentials.
- [ ] **8.1.6** `L1` — **Verify that** claims whose evidence is verifiable only after the fact — transparency logs with independent monitors, on-demand proofs the system can run without producing — are registered at Tier 3, and Tier 4 is registered only where verification gates operation.
- [ ] **8.1.7** `L3` — **Verify that** claims resting on a vendor-rooted attestation service are either registered at Tier 2, or composed with independent anchoring (e.g., attestation reports committed to a public transparency log with independent monitors) before being registered at Tier 3 — with the vendor trust assumption on the disclosure in both cases.
- [ ] **8.1.8** `L3` — **Verify that** the verification procedure and tooling for each Tier 3+ claim are published (public repository or equivalent), versioned, and usable without an NDA, license negotiation, or operator-issued credentials.
### C8.2 Mechanism-to-Requirement Fit

- [ ] **8.2.1** `L1` — **Verify that** the claim register maps each claimed control to its mechanism and to the specific verifiable fact it evidences, using the mechanism's "what it proves" scope from [Appendix B](0x91-Appendix-B_Proof-Mechanism-Inventory.md) — and that no mapping pairs a mechanism with a domain outside that scope (e.g., an encryption control offered for the Identity domain).
- [ ] **8.2.2** `L1` — **Verify that** the mapping distinguishes signing-time claims from runtime claims: no artifact-integrity mechanism (signature at rest) is mapped to a runtime-behavior fact, and no environment attestation is mapped to a claim about the model weights loaded into it.
### C8.3 Chain Integrity and Self-Enforcement (Tier 4)

- [ ] **8.3.1** `L4` — **Verify that** where a use case is designated Tier 4, an interaction inventory lists every system in the chain, and each listed system's shared interactions carry Tier 4 evidence — confirmed per interaction, not per system.
- [ ] **8.3.2** `L4` — **Verify that** components operating internally below Tier 4 interact with the chain only through interfaces that produce Tier 4 evidence, per the interaction inventory.
- [ ] **8.3.3** `L4` — **Verify that** operation is mechanically gated on proof validity: in test, invalidating the proof chain (or withholding a required proof) halts the system's in-scope actions.
- [ ] **8.3.4** `L4` — **Verify that** the claim documents the availability impact of proof-gated operation — expected halt conditions, recovery procedure, and maximum tolerable outage — and that the recovery procedure has been exercised.
- [ ] **8.3.5** `L4` — **Verify that** the halt is enforced outside the operator's control — for example, relying parties refuse requests lacking a valid, action-bound capability, so absence of valid evidence blocks execution at the far end rather than depending on an operator-side flag that a compromised host could disable.

*Auditor evidence for these items: see [C8](0x10-C08-Verifiability-Tiers.md).*

## C9 System Surface (MAESTRO)

### C9.1 Locating Evidence on the System Surface

- [ ] **9.1.1** `L1` — **Verify that** every entry in the claim register carries a populated layer field identifying the MAESTRO layer (1–7) its evidence covers.
- [ ] **9.1.2** `L1` — **Verify that** the conformance statement names the framework filling the System surface (MAESTRO today) and its version.
- [ ] **9.1.3** `L1` — **Verify that** the claim-register validation (schema check or intake review) rejects claim entries with a missing or invalid layer field, and that rejections are recorded.
### C9.2 Layer Coverage

- [ ] **9.2.1** `L2` — **Verify that** tamper-evident logging (a Layer 5 control per [Appendix B](0x91-Appendix-B_Proof-Mechanism-Inventory.md)) is deployed and covering every system named in the claim's scope, as shown by the log-source inventory.
- [ ] **9.2.2** `L2` — **Verify that** for each claim, the evidence is generated at the layer where the control is enforced, matching the layer listed for that control in [Appendix B](0x91-Appendix-B_Proof-Mechanism-Inventory.md) — e.g., runtime attestation evidenced at L4, delegation chains at L7.
- [ ] **9.2.3** `L3` — **Verify that** claims spanning multiple layers aggregate their per-layer evidence into a hash-linked bundle referencing each layer's records, so the cross-layer claim is verifiable as one artifact.

*Auditor evidence for these items: see [C9](0x10-C09-System-Surface-MAESTRO.md).*

## C10 Conformance and Trust-Assumption Disclosure

### C10.1 Conformance Claims

- [ ] **10.1.1** `L1` — **Verify that** the published conformance statement names its stage — Self-Declared, Third-Party Assessed, or Continuously Monitored — and, for the latter two, identifies the assessor or monitoring regime.
- [ ] **10.1.2** `L1` — **Verify that** the statement lists the domains claimed (of C1–C6), and that domains not listed appear nowhere in the operator's Proof-of-Control marketing for the system.
- [ ] **10.1.3** `L1` — **Verify that** every verifiable fact asserted in the statement resolves to at least one evidence stream in the claim register — no asserted fact without a register entry.
- [ ] **10.1.4** `L1` — **Verify that** the statement contains all required fields: system identification (name, version, environment); domains claimed; per-claim evidence properties met and Tier reached; mechanisms used; and the trust-assumption disclosure.
- [ ] **10.1.5** `L1` — **Verify that** the statement cites the exact version of this standard (e.g., v0.1) and the date of the claim.
- [ ] **10.1.6** `L1` — **Verify that** the statement defines the system boundary (components, environments, interfaces in scope) and the classes of in-scope agent actions, and enumerates excluded action classes with a stated rationale for each exclusion.
- [ ] **10.1.7** `L2` — **Verify that** the statement and its per-claim data are published in a documented, machine-readable format (schema available), so assessors and insurers can compare claims across implementations programmatically.
- [ ] **10.1.8** `L2` — **Verify that** the declared system inventory is reconciled on a defined schedule against automated discovery from operational and observability streams, and that undeclared agent deployments surface as recorded findings rather than remaining shadow systems. *(Research-driven addition — see [Appendix D, issue 12](0x93-Appendix-D_Open-Issues.md).)*
### C10.2 Trust-Assumption Disclosure

- [ ] **10.2.1** `L1` — **Verify that** the disclosure lists, per claim, each residual trust assumption with the assumption's subject (named vendor, hardware element, mathematical assumption, or ceremony) — matched one-to-one against the mechanisms in the claim register.
- [ ] **10.2.2** `L2` — **Verify that** each disclosed assumption is tagged with one of the defined categories (draft set: Hardware, Mathematical, Ceremony, Vendor, Implementation, Distributed), so disclosures are machine-comparable across implementations.
### C10.3 Continuously Monitored Operation

- [ ] **10.3.1** `L2` — **Verify that** evidence is retained in a store meeting the tamper-evident requirements of [C7.3](0x10-C07-Evidence-Generation-and-Properties.md), with the store's chain-verification results available to the assessor.
- [ ] **10.3.2** `L4` — **Verify that** evidence generation covers every in-scope action rather than a sample — demonstrated by reconciling gateway action counts against evidence-record counts over an audit window, with zero unexplained difference.
- [ ] **10.3.3** `L4` — **Verify that** an automated validator checks each evidence record against its claimed Tier's requirements within the defined validation window, and that validator results are themselves logged.
- [ ] **10.3.4** `L4` — **Verify that** validation failures and coverage gaps raise alerts to a monitored destination within the bounded window defined in the claim, with alert-to-acknowledgment times tracked.
- [ ] **10.3.5** `L4` — **Verify that** the monitoring pipeline itself is re-assessed by a third party on a defined cycle (e.g., annually), and the re-assessment report is available to relying parties.
- [ ] **10.3.6** `L3` — **Verify that** proof coverage — evidence-covered in-scope actions divided by total in-scope actions — is computed on a defined schedule and published with the claim, so coverage decay is visible rather than silent.
- [ ] **10.3.7** `L3` — **Verify that** automated validators used to monitor multi-step execution are evaluated for structured-trace parsing competence (schema and argument validation over tool-call trajectories), not only natural-language safety performance, and that the evaluation results are available to the assessor. *(Research-driven addition — see [Appendix D, issue 12](0x93-Appendix-D_Open-Issues.md).)*

*Auditor evidence for these items: see [C10](0x10-C10-Conformance-and-Disclosure.md).*

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) — **[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
