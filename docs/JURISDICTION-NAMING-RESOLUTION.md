# ICSN Jurisdiction Naming & Resolution Registry (JNR)

> **Status:** Public reference architecture.

JNR is the open jurisdiction naming/resolution layer of the TitleChain/M5Global architecture. It is designed to resolve technical namespace references to authoritative jurisdictional, governmental, regulatory, treaty, registry, and entity sources while preserving provenance.

The M5 reference implementation maintains an inventory of **170+ jurisdiction-chain ENS namespaces** used as technical resolution references across nation, state/province, territory, tribal/Indigenous, and related jurisdiction contexts.

## Resolution model

```text
technical namespace / identifier
        ↓
JNR jurisdiction reference
        ↓
official / authoritative source
        ↓
entity / role / credential / legal state
        ↓
TitleChain provenance relationship
        ↓
M5Canon policy evaluation
```

JNR may reference ENS-compatible namespaces, verified DNS, TitleChain identifiers, government/regulator identifiers, LEIs, treaty/intergovernmental references, and future naming systems.

## Critical boundary

An ENS or TitleChain namespace does **not** create sovereignty, governmental recognition, agency authority, court jurisdiction, treaty status, or control of an official DNS name. Official government DNS names, including `.gov`, are separate external references.

The public purpose is resolution and provenance: **who/what is acting, under whose authority, in which jurisdiction, over which rights, and with what evidence.**
