# M5 Open Standards Alignment

The M5 stack is designed as an implementation-neutral interoperability architecture. M5 components can map to, transport, reference, or validate information expressed through established external standards while preserving a separate authority layer for identity, consent, jurisdiction, credentials, restrictions, approvals, revocation, and authoritative state.

“Aligned,” “compatible,” and “supported” do not mean certified, endorsed, formally partnered, or fully conformant unless a separate public record expressly documents that status. External standards organizations, official registries, applicable law, regulated providers, and legally authoritative records remain controlling.

## Identity, credentials, and delegated authority

| Standard or specification | Illustrative M5 use | Reference |
|---|---|---|
| W3C Verifiable Credentials Data Model 2.0 | Portable credential claims, issuer/holder/verifier roles, credential status, and evidence | https://www.w3.org/TR/vc-data-model-2.0/ |
| W3C Decentralized Identifiers Core | Portable identifier references where appropriate | https://www.w3.org/TR/did-core/ |
| OAuth 2.0 and OpenID Connect/Federation | Delegated access, authentication, metadata, and multilateral trust | https://openid.net/wg/connect/specifications/ |
| Web Authentication and FIDO | Phishing-resistant authentication and hardware-backed credentials | https://www.w3.org/TR/webauthn-3/ |

Authentication or possession of a key does not by itself create legal authority. M5Canon evaluates current role, credential status, jurisdiction, purpose, scope, restrictions, approvals, expiry, and revocation before consequential execution.

## Financial messaging and payment interoperability

| Standard or specification | Illustrative M5 use | Reference |
|---|---|---|
| ISO 20022 | Structured financial messages and regulated-rail adapters | https://www.iso20022.org/ |
| Global Legal Entity Identifier System | Cross-references to authoritative legal-entity identifiers | https://www.gleif.org/en/about-lei/introducing-the-legal-entity-identifier-lei |
| x402 | Optional HTTP-native machine-payment adapter | https://github.com/x402-foundation/x402/tree/main/specs |
| OpenAPI Specification | Portable and reviewable service-interface descriptions | https://spec.openapis.org/oas/latest.html |

M5Pay is intended to be rail-, asset-, provider-, ledger-, wallet-, and protocol-agnostic. It may translate and route an already-authorized instruction to an eligible external rail, but it does not create authority, determine legal classification, become a custodian, or displace the regulated provider responsible for payment, settlement, or recordkeeping.

## Agent, data, and tool interoperability

| Standard or specification | Illustrative M5 use | Reference |
|---|---|---|
| Model Context Protocol | Portable tool and context interfaces for bounded agents | https://modelcontextprotocol.io/specification/ |
| Solid technical reports | Portable personal-data stores and member-controlled data boundaries | https://solidproject.org/TR/ |
| JSON and cryptographic web formats | Structured policy, receipts, credentials, signatures, and evidence exchange | https://www.rfc-editor.org/standards |

An agent or tool endpoint may execute only within authority received from an accountable human or legal entity. It may not issue its own authority, expand its scope, waive required approval, or treat successful execution as proof of authorization.

## Open technology and standards corridors

The broader M5 Sovereign Web Map organizes fifteen standards and ecosystem corridors spanning open-source governance, agentic AI, data portability, hardware, compute, finance, privacy, climate reporting, public-good governance, and decentralized title:

https://m5bank.app/m5-sovereign-web-map.html

Names and logos shown on that map are standards, ecosystem, or candidate-corridor references unless a formal partnership or certification is separately announced and supported by a public record.

## TitleChain-authored public specifications

TitleChain Foundation publishes its own reference architectures, schemas, RFCs, governance materials, conformance concepts, and implementation examples for public review at:

https://github.com/TitleChain-Foundation/icsn-standards

TitleChain-authored materials are proposed public reference standards. They do not replace external standards, official registries, applicable law, or the responsibilities of regulated institutions.
