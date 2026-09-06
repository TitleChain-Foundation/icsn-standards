# Transfer-Agent Digital-Asset Reference Architecture

> **Status:** Public reference architecture for agency, transfer-agent, issuer, and infrastructure review. It does not authorize TitleChain Foundation to perform a regulated transfer-agent function.

## Problem

As securities records move from paper and proprietary databases to electronic/DLT systems, the infrastructure must distinguish:

- the underlying right/security;
- the legally authoritative ownership record;
- a token/digital representation;
- the human/entity authorized to instruct;
- an agent acting for that principal;
- restrictive legends and holder eligibility;
- jurisdiction and current professional/entity authority; and
- execution/settlement evidence.

## Reference flow

```text
KNOWN LEGAL ENTITY / ISSUER / INSTITUTION
TitleChain Registry + official identifiers + SwiftBRIDGE/JNR crosswalk
                    ↓
ACCOUNTABLE HUMAN / LEGAL PRINCIPAL
M5IAM → TCID / M5HUM
                    ↓
CURRENT ROLE + CREDENTIAL
SOPHIA / Credentialed Authority Registry
                    ↓
M5CANON SIX GATES
identity | credential | jurisdiction | policy | approval | evidence
                    ↓
TITLECHAIN TITLE / RIGHT RECORD
source + provenance + restrictions + lifecycle
                    ↓
REGISTERED TRANSFER AGENT'S LEGALLY AUTHORITATIVE RECORD
                    ↓
AUTHORIZED ACTION
mint/register | propose | approve | transfer | restrict | correct
                    ↓
EXECUTION / SETTLEMENT RAIL
                    ↓
SIGNED EVIDENCE + RECONCILIATION
```

## Pre-activation of M5AGT

A transfer-agent M5AGT should not become executable merely because an API key, wallet, or model exists. Before activation the system should establish the entity, accountable principal, role, credential/appointment, jurisdiction, permitted functions, issue/asset scope, limits, approval requirements, expiry, revocation, and audit policy.

This design reduces rogue-agent exposure by preventing the agent from becoming the source of its own authority.

## Origination

M5MST is the asset-minting event or TitleChain registration on WyomingChain.eth. It records who was authorized to mint/register the M5AST and the source/title evidence supporting that event. Mint authority remains separate from transfer authority.

## Transfer

A transfer event should independently determine who may instruct, propose, approve, and execute; which restrictions/legends apply; whether the recipient/venue is eligible; which authoritative record controls the ownership update; and what evidence proves completion.

## Correction and revocation

Identity persists while roles, appointments, employment, licenses, delegations, and good standing may expire or be revoked. The architecture should make the affected operational capability inert without erasing historical evidence.

## Boundary

TitleChain/ICSN provide open reference standards, provenance, resolution, schemas, and conformance models. They do not displace a registered transfer agent's legally authoritative Master Securityholder File or confer transfer-agent registration.
