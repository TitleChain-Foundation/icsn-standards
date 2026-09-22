<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Synthetic Examples

![Hardware endpoint trust public review](../assets/public-review/hardware-endpoint-trust.svg)

Examples show proposed record shapes and support validation. They are not
credentials, production records, vendor findings, real measurements, legal
conclusions, or proof of deployment.

## Hardware endpoint trust examples

| Example | Schema |
| --- | --- |
| [Observation](hardware-endpoint-observation.synthetic.json) | [Observation schema](../schemas/hardware-endpoint-observation.schema.json) |
| [Test run](hardware-endpoint-test-run.synthetic.json) | [Test-run schema](../schemas/hardware-endpoint-test-run.schema.json) |
| [Capture score](hardware-endpoint-capture-score.synthetic.json) | [Capture-score exchange schema](../schemas/hardware-endpoint-capture-score.schema.json) |

All hardware examples use fictional manufacturers, models, identifiers, and
placeholder hashes. Do not present them as measured results.

## Article 12 CER control example

| Example | Schema |
| --- | --- |
| [Shared-control transaction snapshot](article-12-cer-control-state.synthetic.json) | [Article 12 CER control state](../schemas/article-12-cer-control-state.schema.json) |

The example is entirely synthetic. It intentionally leaves title, notice,
transfer authority, approvals, and applicable-law review unresolved even though
all four CER-control proofs are marked established. Its M5Canon decision is
therefore `HOLD`.
