# Ricardian Service Contracts for M5isYOU Roles

> **Status: Public Review Draft for the people's review. This specification is not legal, tax, employment, securities or payments advice.**

## Three synchronized representations

An M5isYOU service engagement may be expressed as one Ricardian contract with:

1. `agreement.md` — human-readable terms;
2. `agreement.jsonld` — machine-readable meaning; and
3. `execution.json` — explicitly permitted executable actions.

All representations must carry the same contract identifier, version and content digest. A conflict rule must identify which human-readable terms control. Executable code may not silently change the legal agreement.

## Formation

1. The provider chooses which role, capability and credential claims to disclose from their M5POD.
2. A prospective client selects `Request services` or proposes a scope.
3. The provider's wallet prepares service terms, price, milestones and permitted payment routes.
4. Both parties review the human-readable agreement.
5. Each party signs the same content digest.
6. Execution begins only after required approvals and conditions are satisfied.

No wallet may issue binding terms or move funds merely because someone viewed or selected a profile.

## Account and payment readiness

IAM activation is the first account step for teachers, attendees and prospective service providers in the initial program. A person may then join the BOM waitlist. A BOM waitlist entry is not an activated account and cannot receive payments.

Before a contract selects an M5 payment route, the execution layer must verify that the required account is active and supported without publishing account identifiers. Depending on the person's separately approved pathway, settlement may use an activated BOM account, an eligible BOU relationship, or an existing or newly registered entity using a BOB pathway. These choices do not arise automatically from a class, profile or service request.

## Required service terms

- parties or pairwise identifiers;
- role and service description;
- deliverables and acceptance criteria;
- schedule and milestones;
- rate, fixed price or other pricing method;
- currency, fees and tax responsibility;
- intellectual-property and license terms;
- confidentiality and permitted data use;
- cancellation, refund and dispute terms;
- governing law or agreed dispute process where applicable;
- invoice and payment route;
- agent authority limits; and
- the activated account type or external payment route required for settlement, without exposing private account identifiers; and
- signatures, timestamps, version and content digest.

## Execution permissions

Automation may prepare an offer, generate an invoice, request milestone review, provide notifications, verify a receipt and record holder-approved completion evidence.

Automation must obtain explicit approval before it:

- accepts or changes contractual terms;
- discloses another credential or personal attribute;
- changes scope, price, deadline or payment route;
- releases escrow or transfers value;
- delegates work to another person or agent; or
- publishes completion evidence.

## Payment adapters

The contract defines the obligation; a payment adapter fulfills it. Possible adapters include stablecoin wallets, ACH or bank connectors, and marketplace integrations with payment service providers. Provider names are implementation options, not endorsements or guaranteed integrations.

Each adapter must expose common states such as `requested`, `authorized`, `processing`, `settled`, `failed`, `refunded` and `disputed`. Sensitive payment credentials must never be stored in a public contract or repository.

## Invoices and receipts

Invoices should reference the contract and milestone, state currency and amount, identify the chosen payment route, and remain distinguishable from proof of payment. A receipt records settlement evidence without unnecessarily publishing wallet addresses, bank information or personal identity.
