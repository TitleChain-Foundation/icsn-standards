# Core M5Stack Contributor Credentialing

> **Status: Implementation governance reference — non-normative to ICSN public standards.**

## Purpose

ICSN standards work can be publicly reviewed and contributed to according to applicable repository rules and licenses.

The **core and hardened M5Stack implementation is different**.

Production M5 code may include restricted architecture, security-sensitive components, private member infrastructure, production integrations, and other implementation material that requires an attributable and accountable software supply chain.

## Public participation

An M5POD is not required to read public specifications, review public documentation, participate in public issues or discussions, review RFCs, propose implementation-neutral standards changes, review public schemas/reference material, or contribute to expressly public/open-source components where permitted.

## M5Bank member access

M5Bank membership may provide access to designated review, testing, participation, or activation environments according to the member's permissions.

Membership alone does not grant write access to restricted source code or production systems.

## Credentialed core contribution

Anyone materially contributing code to the **core M5 implementation** must be credentialed into the M5Stack.

Required foundation:

**M5Member + active validated M5POD + contributor credential + authorized role**

```text
Human
  ↓
IAM
  ↓
M5Member
  ↓
Active M5POD
  ↓
Verified Contributor Credential
  ↓
Repository / Role Authorization
  ↓
Contribution
  ↓
Review + Testing + Security Controls
  ↓
Approved Merge
```

The M5POD is the human identity and authority root from which developer credentials, repository permissions, signing authority, attestations, and production-development permissions may be issued.

## Production / hardened code

Production or security-hardened code must come through credentialed contributors with an active M5POD and authorized development role.

Access remains:

- role-based;
- least-privilege;
- repository-specific;
- revocable;
- attributable;
- auditable; and
- subject to applicable contribution, security, licensing, review, and testing requirements.

This requirement is especially important for:

- identity and authentication;
- M5POD;
- wallet infrastructure;
- cryptography and key management;
- authorization;
- agent authority;
- M5Ledger;
- M5Canon;
- TitleChain production integrations;
- M5-OS;
- M5-OpenAPI production adapters;
- financial and settlement integrations;
- NationChain / TribalChain infrastructure;
- production registries;
- deployment infrastructure; and
- other restricted M5Stack components.

## Principle

> **The standards can be reviewed by anyone.**
>
> **The production M5Stack cannot be anonymously altered.**
>
> **Anyone materially contributing to the core or hardened M5 implementation must be attributable to a validated M5Member identity through an active M5POD and an authorized contributor role.**
