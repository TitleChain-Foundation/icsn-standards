# Ricardian Three-Part Agreement Standard

> **Status:** Public reference model.

A digitally executable legal or operational agreement should keep three synchronized representations distinct:

1. **Human-readable legal terms** — the terms a person or authorized entity can read, review, and agree to.
2. **Machine-readable structured meaning** — normalized fields describing parties, rights, restrictions, jurisdiction, approvals, timing, and state.
3. **Separately bounded executable code or instructions** — only those operations the agreement explicitly permits.

```text
HUMAN TERMS
     ↕
MACHINE-READABLE MEANING
     ↕
BOUNDED EXECUTION
```

All three representations should share the same agreement identifier, version, and content digest.

## Conflict rule

Executable code must not silently alter or supersede the controlling human-readable legal terms, applicable law, or a legally authoritative registry/transfer-agent record.

## Restrictive legends and transfers

For transfer-agent and digital-asset workflows, machine-readable restrictive legends and transfer conditions should be bound to the **Title Rights & Provenance Record** and referenced by the Ricardian agreement where applicable.

The executable layer may enforce a restriction or prepare an authorized state change only after the required M5Canon authority checks pass.

## Evidence

A conforming implementation should be able to prove which version of the human terms, machine representation, and executable instructions governed a specific action and which approvals/evidence authorized that action.
