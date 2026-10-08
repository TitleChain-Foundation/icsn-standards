# C3 Portability

## Control Objective

Produce verifiable evidence of continuity and control across vendors, platforms, and environments. Agents create value by crossing boundaries — and every boundary an agent crosses is a place where evidence of what it did can go missing. This domain covers cross-cloud migration, multi-vendor interoperability, and evidence that data and agent operations maintained integrity across system boundaries.

*Verifiable facts: boundary crossings (organizational, jurisdictional, compute).*

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../images/diagrams/c3-portability-dark.svg">
    <img alt="Two attestation domains with their evidence chains, bound by a signed linking record so no unverifiable gap exists at the boundary" src="../../images/diagrams/c3-portability-light.svg" width="900">
  </picture>
</p>

---

## C3.1 Boundary-Crossing Evidence

Every crossing recorded; integrity maintained through it.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.1.1** | **Verify that** each organizational, jurisdictional, and compute boundary crossing writes an execution-record entry identifying the source environment, destination environment, and what crossed (data digests, agent state, credentials). | 1 |
| **3.1.2** | **Verify that** integrity of data and agent state is checked at the destination side of each crossing — digest recomputed or signature validated — and that the check result is recorded on both sides. | 2 |

**Auditor evidence:** 3.1.1 — boundary-crossing log entries for a sampled cross-system workflow; reconcile source and destination entries. 3.1.2 — a matched pair of crossing records with the destination-side integrity check; force one integrity failure in test and confirm it is recorded.

---

## C3.2 Cross-Environment Continuity

Evidence must survive the migration it describes.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.2.1** | **Verify that** evidence generated before a cross-cloud or cross-vendor migration remains validatable after it: keys, reference values, and verification tooling for the old environment stay published for the retention period. | 2 |
| **3.2.2** | **Verify that** when evidence crosses attestation domains, a signed linking record binds the last record of the source chain to the first record of the destination chain, so an external verifier can confirm there is no gap. | 3 |
| **3.2.3** | **Verify that** a documented cross-jurisdiction review determines, per jurisdiction pair, what each evidence artifact discloses, and that artifacts exceeding the destination's permitted disclosure are transformed (re-proven, redacted) before transfer. | 3 |

**Auditor evidence:** 3.2.1 — validate one pre-migration evidence artifact today, using only published materials. 3.2.2 — walk one source→destination chain link as an outsider. 3.2.3 — the jurisdiction disclosure matrix and one transformed-artifact example.

> **[WG-INPUT NEEDED]** — whether an unbroken cryptographic evidence chain across attestation
> domains belongs in this domain, as a fifth evidence property, or as a domain of its own; and
> whether evidence continuity includes evidence *disclosure* continuity. See
> [Appendix D](0x93-Appendix-D_Open-Issues.md), issue 3.

---

## References

* Crosswalks: [AIUC-1 cross-platform auditing](../../mappings/aiuc-1.md) — Portability-domain external alignment target
* Source architectural mechanisms under mapping: Agent Resource Discovery Spec, Open Handshakes ([mappings/README](../../mappings/README.md))
* [Appendix D — Open Working-Group Issues](0x93-Appendix-D_Open-Issues.md)
