<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Hardware Endpoint Measurement Method

**Status:** Public Review Draft  
**Scope:** Defensive, owner-controlled, non-invasive endpoint measurement.

## 1. Goal

Create repeatable evidence about observable endpoint behavior under defined states without compromising a device, bypassing security controls, collecting unrelated household traffic, or exposing private data.

## 2. Preconditions

A tester must have authority over:

- the device under test; and
- the network or isolated test environment used for measurement.

Do not test third-party devices or traffic without explicit authorization.

## 3. Preferred environment

Use an isolated or dedicated test network where practical.

The environment should:

- contain only the minimum devices needed for the test;
- avoid real personal communications;
- avoid unrelated production/work systems;
- use synthetic names/data where possible;
- record time accurately;
- record firmware/software versions;
- identify the test method version.

## 4. Safe evidence sources

The first public method is limited to ordinary-owner observations such as:

- device settings and consent screens;
- privacy-filtered DNS query logs;
- aggregate or privacy-filtered network-flow metadata;
- local discovery protocol metadata;
- documented device status/indicator changes;
- logs or files legitimately available to the owner on the device;
- vendor disclosures and public documentation;
- firmware/version identifiers.

Do not include public instructions for exploiting vulnerabilities, defeating encryption, bypassing access controls, or intercepting other people's private communications.

## 5. State sequence

Each test run should declare which states were used.

Recommended sequence:

1. factory-reset or documented baseline, when practical;
2. fresh setup before optional consent;
3. consent ON;
4. normal active use;
5. idle;
6. standby/display off;
7. consent OFF;
8. WAN disconnected;
9. WAN reconnected;
10. firmware/software update, if one occurs;
11. post-update repeat.

A tester may run a subset, but must not imply untested states were evaluated.

## 6. Observation window

For each state record:

- state start time;
- state end time;
- test action;
- intended user interaction;
- environmental changes;
- observed destination categories;
- local discovery categories;
- event counts or timing metadata;
- evidence references.

Avoid publishing stable identifiers when a category or salted test-local pseudonym is sufficient.

## 7. Destination categorization

When a network destination is observed, classify it conservatively:

- vendor core service
- update
- content delivery
- diagnostics/crash
- advertising
- measurement/analytics
- voice/cloud
- smart-home/discovery
- third-party service
- unknown

A category is an `inferred` field unless the role is directly documented by an authoritative source.

## 8. Local-device discovery

Record only the fact and type of discovery behavior necessary for reproduction.

Prefer:

- protocol name;
- target class/count;
- timing;
- whether discovery changes by consent or operating state.

Do not publish the names, addresses, stable identifiers, or activity of unrelated household devices.

## 9. Offline/reconnect test

A valid offline/reconnect test must record:

- the exact WAN state;
- whether the local network remained available;
- the duration;
- what was observed locally;
- what changed after WAN restoration.

Do not claim that locally retained data was later transmitted unless that transmission is directly observed and attributable.

## 10. Sensor-related observations

Sensor claims require a higher evidence threshold.

Separate:

- sensor capability;
- sensor configuration;
- local processing;
- stored artifact;
- network transmission;
- vendor disclosure;
- researcher inference.

Do not publish private audio, video, or conversations. Use synthetic test stimuli where a sensor test is necessary and lawful.

## 11. Consent comparison

For ON/OFF comparisons:

- capture the consent disclosure/version;
- record the state before changing consent;
- change only the relevant setting where possible;
- repeat the same test action;
- compare the same observation window;
- document what changed and what did not.

"Opt-out had no effect" is not valid unless the same measured behavior was compared under controlled equivalent states.

## 12. Firmware/update drift

Before and after an update record:

- previous version;
- new version;
- update date;
- relevant disclosure/version;
- same test profile;
- material behavior differences.

A difference is not automatically proof that the update caused the behavior. Use `inferred` until reproduced or otherwise established.

## 13. Evidence package

Each test run should produce:

- one `hardware-endpoint-test-run` JSON record;
- one or more `hardware-endpoint-observation` JSON records;
- privacy-filtered evidence files when publication is appropriate;
- hashes for published evidence;
- method version;
- redaction statement.

## 14. Replication

An independent replication should:

- use the same method version;
- identify device/firmware independently;
- repeat equivalent states;
- avoid copying the original researcher's interpretation into the observation;
- publish its own evidence hash and limitations.

## 15. Reporting

Public summaries must say:

- what was tested;
- what was not tested;
- what was directly observed;
- what was inferred;
- whether the vendor has responded;
- whether an independent replication exists;
- material limitations.

## 16. Prohibited public evidence

Do not publish:

- passwords/tokens;
- private keys;
- raw private conversations;
- unredacted household identifiers;
- unrelated browsing data;
- third-party traffic content;
- personal location history;
- identity documents;
- exploit payloads or bypass steps.

## 17. Conformance target for the pilot

A pilot method is ready for comparative public use when:

- schemas validate;
- redaction review passes;
- at least two independent testers can execute it;
- the same test state produces interpretable evidence across at least three device models/vendors;
- known limitations are documented.
