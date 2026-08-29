# ICSN-0014: Universal Value and Digital-Asset Classification

> **Publication status:** Adopted Version 1.0  
> **Adopted by:** TitleChain Foundation authorized governance body  
> **Effective date:** 2026-08-28  
> **Last reviewed:** 2026-08-28  
> **Next scheduled review:** 2027-08-28  
> **Legal review:** Approved for publication by authorized counsel on 2026-08-28.

**Version:** 1.0.0  
**Category:** Interoperability and classification framework

## Abstract

This document proposes a machine-readable classification framework for supported digital-asset relationships, value units, issuer references, authority references, jurisdiction or policy routing, and asset-class metadata.

It does not create a currency, legal tender, security, commodity, deposit, stored-value product, payment instrument, money-transmission authorization, tax classification, regulatory exemption, property right, or governmental recognition.

## 1. Purpose

The framework is intended to enable interoperable identification and policy-aware handling of digital records and supported digital-asset relationships across national, state, tribal, local, institutional, cooperative, private, and community contexts.

The framework is proposed as an ICSN/M5 taxonomy. It is not an official global currency code, government code, ISO code, or a representation that a named authority has issued, approved, guaranteed, or accepted a referenced unit.

## 2. M1–M5 identifier format

A proposed M1–M5 identifier may use the following structure:

```text
M5:[Authority]:[Jurisdiction]:[Asset-Class]:[Unit]:[Series]:[Instance]
```

The identifier identifies a proposed classification and routing reference. It MUST NOT be interpreted as proof that a unit is officially issued, legally recognized, redeemable, transferable, regulated, insured, approved, or accepted by the authority named in the code.

## 3. Required classification elements

A conforming classification record MUST include:

- Unique classification identifier
- Asserted issuing or governing authority
- Asserted jurisdiction or policy-routing reference
- Asset or value class
- Unit or instrument identifier
- Governing terms or policy reference
- Applicable version
- Current status
- Verification or issuer reference
- Risk and legal-disclosure category

## 4. Disclosure requirement

Any implementation presenting an M1–M5 identifier to a participant MUST disclose, where applicable, whether the referenced asset, unit, record, or relationship is:

- Government-issued
- Government-recognized
- Privately issued
- Redeemable or non-redeemable
- Custodial or self-custodied
- Transferable or non-transferable
- Subject to eligibility or geographic restrictions
- Subject to securities, commodities, banking, payments, consumer-protection, tax, sanctions, privacy, or other legal considerations

## 5. No official-status implication

An implementation MUST NOT use an M1–M5 identifier, authority reference, flag, seal, jurisdiction name, governmental identifier, tribal identifier, or agency reference in a manner that falsely implies endorsement, issuance, legal-tender status, governmental approval, regulatory clearance, official affiliation, or sovereign guarantee.

## 6. Governing-law and jurisdiction references

A jurisdiction field identifies an asserted governing-law, policy-routing, or administrative reference.

It does not by itself determine exclusive jurisdiction, legal situs, ownership, custody, priority, enforceability, tax treatment, or regulatory status.

## 7. Foundation and ICSN limitations

TitleChain Foundation and ICSN do not issue, custody, control, transact, redeem, exchange, settle, guarantee, or value any asset, unit, or relationship referenced by this classification framework.

## Related policies

- [Home](Home)
- [What Is M5Bank?](What-Is-M5Bank)
- [Human-First Technology and Due Process](Human-First-Technology-and-Due-Process)
- [M5 Participation Profile](M5-Participation-Profile)
- [Foundation and ICSN Non-Custody and Data Non-Access Policy](Foundation-and-ICSN-Non-Custody-and-Data-Non-Access-Policy)
- [M5 Due Notice and Credentialed Authority Policy](M5-Due-Notice-and-Credentialed-Authority-Policy)
- [M5 Credential Trust and Issuer Registry](M5-Credential-Trust-and-Issuer-Registry)
- [M4-M5 Registered Service Provider Pathway](M4-M5-Registered-Service-Provider-Pathway)
- [ICSN-0014: Universal Value and Digital-Asset Classification](ICSN-0014-Universal-Value-and-Digital-Asset-Classification)
