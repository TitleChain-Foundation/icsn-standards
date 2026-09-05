# Credentialed Authority Registry

> **Status:** Public reference model.

The Credentialed Authority Registry represents which legal entities, humans, roles, credential issuers, and delegated agents are currently authorized for a defined function.

## Core rule

Identity persists; operating authority is current-state dependent.

A registry record may establish:

- legal entity and jurisdiction;
- accountable M5HUM/legal principal;
- role/appointment;
- credential issuer and credential state;
- signing/delegation authority;
- asset/issue/system scope;
- permitted capabilities;
- effective/expiry time;
- good-standing requirements;
- revocation/suspension state; and
- provenance/evidence references.

## M5AGT relationship

Only a currently authorized principal may delegate a capability to an M5AGT, and the agent receives no greater authority than the intersection of the principal's current authority, delegated scope, jurisdiction, policy, approvals, and time window.

## Revocation

If a person leaves an organization, loses an appointment/license, changes roles, or has a credential suspended/revoked, the affected capability must become non-executable while historical evidence remains preserved.

This registry is a technical authority model. It does not itself issue a government license, professional registration, or regulated status.
