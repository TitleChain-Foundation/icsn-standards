# Crosswalk: Confidential Computing (TEEs)

**Framework type:** Mechanism (Trusted Execution Environments; Confidential Computing
Consortium)
**Relationship:** Confidential Computing is a mechanism; Proof-of-Control is a property. TEE
attestation is one valid mechanism for delivering Proof-of-Control — not the property itself.
See [Section 8](../docs/standards-landscape.md).

## The Relationship

Confidential Computing protects data in use inside a Trusted Execution Environment and produces
a hardware-signed attestation that code ran untampered. Under this standard, TEE attestation is
one valid mechanism for delivering Proof-of-Control, primarily in the **Security** domain, but
on its own it does not cover Identity, Portability, Authorization, or the full record of what
the agent did, and it carries no conformance framework.

Confidential Computing is to Proof-of-Control what a deadbolt is to a home-security standard:
real and worth having, but not the system. Complementary, not competitive; the Confidential
Computing Consortium is a natural partner.

## Tier Placement Caveat

A TEE attestation whose root of trust is the chip vendor's attestation service sits at **Tier 2**
on the Verifiability Tiers — a party is still being trusted
([Section 6](../0.1/en/0x10-C08-Verifiability-Tiers.md), the binary threshold). Deployments
using TEEs toward a Tier 3+ claim must disclose the residual hardware and vendor trust
assumptions in the standardized disclosure format — for example the Healthcare-on-Azure
deployment in the trust-assumption disclosure example
([Section 7](../0.1/en/0x10-C10-Conformance-and-Disclosure.md)): trusts Intel silicon manufacturing and Azure
physical security; hardware supply-chain risk; single-vendor trust dependency.

Note also the mechanism-fit rule: a TEE attestation of the execution environment is silent on
the model weights loaded into it. Conformance judges mechanism-to-requirement fit, not just
mechanism presence.

## Where TEEs Appear in the Standard

| Location | Use |
| --- | --- |
| MAESTRO L1 | Model integrity at inference (weights in a protected enclave match signed manifest) |
| MAESTRO L2 | Privacy compliance attestation (PII processing in an isolated, policy-enforcing environment) |
| MAESTRO L4 | Runtime environment attestation (Intel TDX, AMD SEV-SNP, ARM CCA) |
| MAESTRO L5 | Tamper-evident logging and telemetry within a protected boundary |
| By-domain mapping | Privacy: TEEs, local-only inference enclaves as source mechanism |

## Status

> **[INSERT]** — detail lives in the companion crosswalk tab, to be merged here.
> **[WG-INPUT NEEDED] — volunteer needed to develop out the crosswalk.**
> [Sign up at advancedaisociety.org](https://advancedaisociety.org/) to contribute.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
