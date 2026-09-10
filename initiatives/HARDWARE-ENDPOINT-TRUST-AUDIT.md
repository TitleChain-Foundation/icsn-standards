<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Hardware Endpoint Trust & Telemetry Audit

> **Public Review Draft — not standards text.**
> This initiative proposes a vendor-neutral, reproducible public-interest research method. It is not a product certification, legal conclusion, security advisory, regulatory finding, or claim that all devices from a manufacturer behave alike.

[Start with the visual project hub](hardware-endpoint-trust/README.md).

## Purpose

A person can own a physical device without being able to independently verify all of the software, telemetry, advertising, discovery, sensor, or update behavior attached to that device.

This project asks:

> **Once a device is owned and activated, what can an ordinary owner or authorized reviewer independently observe about what it discovers, stores, transmits, or changes — and does that behavior vary with consent, operating state, connectivity, or firmware?**

The work should help owners, engineers, privacy researchers, hardware reviewers, manufacturers, regulators, economists, and public-interest organizations evaluate the same evidence using the same structured test states.

## Relationship to RFC 0001

[RFC 0001 — Hardware Onboarding Standard](../rfcs/0001-hardware-onboarding-standard.md) covers:

- accountable device ownership/custody;
- root-device and component title;
- software and SBOM evidence;
- lifecycle events;
- authority;
- privacy.

This initiative extends the public research surface without replacing the RFC.

```text
M5IAM → TCID/M5HUM
  → owner/custodian authority
  → device title + component provenance
  → firmware/software evidence
  → consent/policy state
  → observable endpoint behavior
  → privacy-filtered evidence
  → independent replication
```

M5/TitleChain may be used as one reference architecture for provenance and evidence lineage. It does not define a required benchmark outcome.

## Initial reference case

The initial public reference case is the September 2026 Gamers Nexus / Level1Techs investigation of LG smart TVs and subsequent public reporting and vendor response.

The Commons must preserve the difference between:

- a researcher's observation;
- a researcher's interpretation;
- a manufacturer's explanation or dispute;
- a regulator's finding or agreement;
- an independently reproduced result.

The initial reference case does **not** establish that every LG device, every smart TV, or every device of a particular class behaves identically.

See the maintained [reference source record](hardware-endpoint-trust/SOURCES.md).

## Research questions

1. What network relationships exist before optional data-sharing consent?
2. What changes after explicit opt-in?
3. What changes after opt-out?
4. What observable behavior persists in idle or standby states?
5. What is retained locally while WAN connectivity is unavailable?
6. What changes when connectivity returns?
7. What changes after firmware/software updates?
8. What other local devices or services does the endpoint attempt to discover?
9. Which observed destinations appear related to update, diagnostics, advertising, measurement, content, cloud, CDN, or unknown services?
10. Can another authorized tester reproduce the same result?

## Test-state matrix

| Test state | Primary question |
| --- | --- |
| Fresh setup | What happens before optional consent? |
| Consent ON | What changes after explicit opt-in? |
| Consent OFF | What stops, continues, or appears after opt-out? |
| Active | What occurs during ordinary intended use? |
| Idle | What occurs without active interaction? |
| Standby / display off | What remains observable while the device appears inactive? |
| WAN disconnected | What remains local while Internet connectivity is unavailable? |
| WAN reconnected | Does observable network behavior change after reconnection? |
| Post-update | Did behavior, endpoints, or disclosure materially change? |
| Factory reset | Does the baseline reproduce? |

## Observation model

A public observation should contain only the minimum information needed to reproduce or evaluate the claim.

### Device/environment

- manufacturer
- product family/model
- firmware/OS version
- device class
- jurisdiction/country
- test date
- pseudonymous lab/contributor identifier

### State

- consent state
- operating state
- WAN connectivity state
- firmware/update state
- test profile identifier

### Observable behavior

Examples include:

- DNS destination categories;
- outbound destination/service categories;
- local-network discovery behavior;
- protocols observed;
- telemetry timing/frequency metadata;
- sensor-access indicators where legitimately observable;
- local artifacts on the tester's own device where lawfully obtained;
- advertising/analytics relationships;
- changes following opt-out;
- changes following firmware update.

### Evidence

- privacy-filtered evidence reference;
- cryptographic hash;
- test method version;
- reproduction count;
- independent reproduction count;
- vendor response/correction;
- unresolved questions.

## Evidence-status vocabulary

Every material finding must use one or more explicit statuses:

| Status | Meaning |
| --- | --- |
| `observed` | Directly recorded in an authorized test |
| `inferred` | Interpretation based on observed evidence |
| `vendor_stated` | Public or direct vendor explanation |
| `regulator_stated` | Statement or requirement from a regulator/public authority |
| `independently_reproduced` | A separate tester reproduced the observation |
| `disputed` | A material interpretation is contested |
| `unresolved` | Evidence is insufficient to resolve the question |

A public summary must never collapse `observed` and `inferred`.

## Privacy and safety boundary

This is a **defensive, owner-controlled measurement project**.

Contributors must test only:

- devices they own; or
- devices/networks they are expressly authorized to test.

Public evidence must not include:

- private conversations;
- credentials;
- private keys;
- raw identity documents;
- household MAC addresses or stable hardware identifiers unless irreversibly transformed for the test;
- unrelated browsing history;
- unrelated local traffic;
- other people's data;
- secrets or exploit material.

The initial public method should prefer ordinary-owner, non-invasive observations such as privacy-filtered DNS, flow metadata, documented settings/state changes, and reproducible state comparisons.

Unauthorized access, bypassing device security, covert interception of third-party traffic, exploitation, or destructive testing are outside this public initiative.

## Comparative reporting rules

Do not publish a comparative ranking until:

- at least three device models or vendors are represented;
- the same method version is used;
- state definitions are comparable;
- limitations are documented;
- at least one material observation has independent reproduction.

Never infer manufacturer-wide behavior from one device.

## Manufacturer participation

Manufacturers should be able to:

- identify factual errors;
- explain intended functionality;
- supply public technical documentation;
- identify firmware-specific differences;
- reproduce the test;
- challenge interpretation with evidence;
- submit corrected or updated disclosure language.

A vendor response does not automatically override an observation. An observation does not automatically override a documented vendor explanation. Both should remain attributable.

## Economic Capture Eval integration

This initiative provides evidence inputs for the `hardware_endpoint_capture` scenario family.

Dimensions:

- ownership/control gap
- consent asymmetry
- data extraction
- cross-device reach
- monetization linkage
- offline persistence
- disclosure divergence
- revocability
- update drift
- replicability

The Eval score is a research indicator, not a legal or moral conclusion.

## Suggested public artifacts

- this initiative
- measurement method
- observation schema
- test-run schema
- score schema
- sanitized examples
- dataset publication rules
- conformance fixtures
- public Discussion
- scoped Issues for privacy, schema, replication, and evidence review

## Help wanted

- hardware / embedded systems
- network measurement
- DNS / protocol analysis
- privacy engineering
- cybersecurity review
- consumer-protection research
- statistics and reproducibility
- schema / interoperability
- technical writing
- manufacturers willing to provide corrections or replication evidence

## First-pilot acceptance criteria

- one vendor-neutral observation schema;
- one test-run schema;
- one documented non-invasive method;
- one privacy/redaction policy;
- at least three device models or vendors before comparative claims;
- at least one independently reproduced material observation;
- vendor-response field on public findings;
- no PII, private conversations, credentials, secrets, or unrelated household traffic in public evidence;
- explicit separation among observed, inferred, vendor-stated, regulator-stated, disputed, and reproduced evidence;
- Public Review status until the Foundation's normal governance process advances it.

## Working principle

> **Own the device. Verify the behavior. Publish only what can be reproduced without exposing the people around it.**
