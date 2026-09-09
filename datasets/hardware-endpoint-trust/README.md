<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Hardware Endpoint Dataset Publication Rules

**Status:** Public Review Draft.

## Purpose

The dataset layer exists to publish reproducible, privacy-preserving endpoint observations — not raw household surveillance data.

## Allowed public data

- device manufacturer/model and firmware version;
- device class;
- test date;
- method version;
- declared consent/operating/connectivity states;
- destination/service **categories**;
- protocol categories;
- redacted or aggregate event counts/timing;
- privacy-filtered evidence hashes;
- source/document references;
- reproduction status;
- limitations;
- vendor response/correction.

## Do not publish

- passwords, tokens, private keys;
- private audio/video/conversations;
- raw household MAC addresses;
- personal browsing history;
- unrelated IP traffic;
- stable identifiers that permit unnecessary household correlation;
- identity documents;
- third-party content;
- precise personal location unless strictly required and approved;
- exploit code, security bypass instructions, or unreported vulnerability details.

## Redaction rule

If a field is not necessary to reproduce the public claim, remove it.

Prefer:

```text
"3 unrelated phone-class devices discovered"
```

over publishing their names, MAC addresses, IP addresses, or owners.

## Evidence storage

Public evidence should be minimized and hashed.

Where a larger raw artifact is necessary for qualified review, retain it in an appropriately controlled review environment and publish only the privacy-filtered derivative plus hash/provenance.

## Dataset maturity

Dataset records may be:

- `draft`
- `reviewed`
- `reproduced`
- `superseded`
- `withdrawn`

A record can remain historically available after correction if the correction is clearly linked and privacy obligations permit retention.

## Correction process

Manufacturers and reviewers should be able to submit:

- corrected device/firmware metadata;
- endpoint/service attribution corrections;
- documentation;
- replication evidence;
- evidence that a behavior changed after firmware update.

Corrections should append provenance rather than silently rewrite prior claims.
