# M5 L0–L8 + ZK Reference Architecture

> **Status:** Public architecture map derived from the M5Ecosystem dependency model. This page describes architectural dependency, not deployment or certification status.

```text
L0 (Constitution) ← all layers depend on constitutional governance
  ├── L1 (Identity) ← L2, L3, L4, L8 depend on identity resolution
  │   └── L2 (Data Sovereignty) ← L3, L6 depend on sovereign data pods
  │       └── L6 (Sovereign AI) ← L8 depends on agent services
  ├── L3 (M5Wallet) ← L4, L5, L8 depend on wallet primitives
  │   └── L5 (Economics) ← L8 depends on settlement + exchange
  ├── L4 (CA Engine) ← L5, L8 depend on authority/compliance checks
  │   └── Defensive Security ← anomaly detection + tamper evidence
  ├── L7 (Node Network) ← L2, L6 depend on infrastructure
  │   └── QCaaS ← optional proof acceleration
  └── ZK (Zero Knowledge) ← L1/L4 may use selective proofs
      ├── Keelung DSL → compiler → R1CS → proof systems
      ├── M5 circuits → notary, credential, license, bridge proofs
      └── optional acceleration backends
```

## Layer roles

- **L0 Constitution** — deterministic governance/policy root and change-control boundary.
- **L1 Identity** — M5IAM, TCID/M5HUM, DID/VC resolution.
- **L2 Data Sovereignty** — M5POD and holder-controlled private data/evidence.
- **L3 M5Wallet** — key/wallet primitives and approved transaction interfaces.
- **L4 CA Engine** — credentialed authority, role, jurisdiction, policy, approval, and revocation evaluation.
- **L5 Economics** — M5 asset/economic state, M5-OMI, ledger, settlement and public indicator interfaces.
- **L6 Sovereign AI** — M5AGT services downstream of identity/authority, never the authority root.
- **L7 Node Network** — compute/storage/network infrastructure and replaceable adapters.
- **L8 Product Suite** — user/business/institution applications built on the lower layers.
- **ZK** — selective proof/confidentiality module used where it reduces disclosure without eliminating accountability.

## Design rule

A higher layer may not silently manufacture authority that the lower identity, credential, jurisdiction, and policy layers do not provide.
