# M5 Bridge Proof Requirements

> **Status:** Public requirements profile derived from the M5 reference bridge circuit. This document specifies proof goals; it does not represent that every referenced cryptographic routine is production-complete.

A cross-network transfer proof should establish, at minimum:

1. **Unbroken provenance** from the relevant origin/current state.
2. **Asset lock/encumbrance state** sufficient to prevent an unauthorized duplicate transfer or rehypothecation.
3. **Actor authority** using a current credential/delegation proof tied to an accountable principal.
4. **Source-state inclusion** against an authoritative source-chain/state root.
5. **Destination reservation/acceptance** sufficient to prevent ambiguous destination state.
6. **Bridge-event integrity** committing to the asset, source/destination, time, amount/quantity where relevant, and policy context.
7. **Distinct source/destination identifiers** and supported route policy.
8. **Evidence receipt** linking the proof to the TitleChain provenance and M5Canon decision.

## Privacy

Private witness data may include provenance paths, credentials, Merkle proofs, and reservation evidence; public inputs should expose only what is necessary to verify the transfer.

## Authority boundary

A cryptographically valid bridge proof does not by itself establish legal title, securities-law compliance, transfer-agent authority, or recipient eligibility. Those states remain inputs to the M5Canon/authoritative-record process.
