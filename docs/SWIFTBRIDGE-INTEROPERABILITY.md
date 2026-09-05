# SwiftBRIDGE Interoperability

> **Status:** M5 reference interoperability architecture.

**SwiftBRIDGE** is the TitleChain/M5 protocol name for mapping legacy financial-institution identifiers and account/routing relationships into jurisdiction-aware M5 institutional/account references without discarding the original authoritative identifier.

```text
legacy institution identifier
BIC | LEI | ABA | IBAN | other authoritative reference
        ↓
SwiftBRIDGE crosswalk
        ↓
TitleChain / JNR entity + jurisdiction resolution
        ↓
M5 institutional/account context
        ↓
M5HUM / role / credential resolution
        ↓
Six-Gate authority check
        ↓
authorized message / execution adapter
```

## Purpose

The bridge allows old and new infrastructure to coexist during migration. A legacy identifier remains attributable to its issuing/authoritative system while M5 can resolve the corresponding entity, jurisdiction, account context, and permitted digital action.

## Transfer-agent relevance

For a transfer-agent or regulated-institution workflow, entity resolution can occur before a human or M5AGT is allowed to operate. This makes it possible to establish:

1. the known legal entity;
2. the accountable M5HUM or lawful principal;
3. the current role/appointment;
4. the applicable jurisdiction;
5. the exact allowed function; and
6. the evidence required for the action.

## Boundary

SwiftBRIDGE is not the SWIFT network and does not imply SWIFT, BIS, bank, regulator, or government endorsement/integration. It is an M5 interoperability/crosswalk layer. The separately named **M5 Global Index and Exchange** is the public economic-intelligence/index-data layer; it is not SwiftBRIDGE.
