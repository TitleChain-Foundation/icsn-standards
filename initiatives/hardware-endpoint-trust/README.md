<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Hardware Endpoint Trust & Telemetry Audit

![Hardware Endpoint Trust and Telemetry Audit](../../assets/public-review/hardware-endpoint-trust.svg)

**Status: Public Review Draft — not an adopted standard, deployed test lab,
product certification, security advisory, regulator finding, or vendor
determination.**

> **You bought the hardware. Can you independently verify what it actually
> does?**

This is the visual front door to a vendor-neutral, owner-controlled research
project. It compares observable endpoint behavior across declared consent,
operating, connectivity, and firmware states, then asks whether another
authorized tester can reproduce the result without exposing the people or
devices around it.

## Three connected layers

| Layer | Question | Maintained source |
| --- | --- | --- |
| Device title and provenance | What is the device, who controls it, and what components and software are present? | [RFC 0001](../../rfcs/0001-hardware-onboarding-standard.md) |
| Illustrative fleet planning | How could titled, modular hardware support a proposed contributor fleet? | [Hardware Fleet Pilot](../HARDWARE-FLEET-PILOT.md) |
| Endpoint behavior and verification | What does an owned device observably do, and can the result be reproduced? | [Hardware Endpoint Trust Audit](../HARDWARE-ENDPOINT-TRUST-AUDIT.md) |

The three layers are complementary. The audit does not replace RFC 0001, and
neither initiative is evidence that a pilot or test lab has been deployed.

## Explore the project

| Start with | Purpose |
| --- | --- |
| [Public initiative](../HARDWARE-ENDPOINT-TRUST-AUDIT.md) | Scope, evidence vocabulary, privacy boundary, comparative rules, and participation |
| [Measurement method](../../methodology/HARDWARE-ENDPOINT-MEASUREMENT-METHOD.md) | Fresh setup through consent, standby, offline/reconnect, and update testing |
| [Observation schema](../../schemas/hardware-endpoint-observation.schema.json) | One privacy-preserving observed or attributed claim |
| [Test-run schema](../../schemas/hardware-endpoint-test-run.schema.json) | One authorized run across declared states |
| [Capture-score exchange schema](../../schemas/hardware-endpoint-capture-score.schema.json) | Draft evidence exchange for the separately governed Economic Capture Eval |
| [Synthetic examples](../../examples/README.md#hardware-endpoint-trust-examples) | Non-production records that exercise all three schemas |
| [Dataset publication rules](../../datasets/hardware-endpoint-trust/README.md) | Minimum disclosure, redaction, evidence, and removal requirements |
| [Initial reference sources](SOURCES.md) | Researcher, secondary-reporting, vendor, and regulator statements kept distinct |
| [Validation tool](../../tests/validate_hardware_endpoint_package.py) | Draft 2020-12 schema and example validation |

## Evidence states

Every material statement must remain attributable as `observed`, `inferred`,
`vendor_stated`, `regulator_stated`, `independently_reproduced`, `disputed`, or
`unresolved`. A viral headline is not a measured finding. One device is not an
entire manufacturer.

## First public challenge: Can you reproduce it?

Test only hardware and networks you own or are explicitly authorized to test.
Change one state at a time. Publish the method version, limitations, and only
the minimum privacy-filtered evidence needed for review. Do not publish private
conversations, credentials, stable household identifiers, unrelated traffic,
other people's data, exploit instructions, or unreported vulnerability details.

Comparative reporting is not ready until equivalent tests cover at least three
device models or vendors and at least one material observation has independent
reproduction.
