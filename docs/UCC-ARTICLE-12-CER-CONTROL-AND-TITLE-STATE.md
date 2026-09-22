<!-- SPDX-License-Identifier: LicenseRef-CYRUS-PCCL-1.0 -->

# UCC Article 12 CER Control and Title State

> **Status:** Public Review Draft. This proposed canonical mapping has not advanced to Candidate or Stable status. It does not determine that a record is a controllable electronic record (CER), that a person has control, that a purchaser qualifies for statutory protections, or that any transaction has legal effect. Article 12 and related Article 9 provisions as enacted in the applicable jurisdiction, other applicable law, governing agreements, authoritative records, and the facts control.

This mapping keeps human or legal-principal authority, rights in underlying property, legal title, CER control, claims, notice, secured-interest filings, and transfer authority independently attributable and reviewable.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, and **SHOULD NOT** are normative requirements for conforming implementations of this profile.

## Canonical state-separation rule

**CONTROL answers who can exercise the CER.**

**TITLE STATE answers what legal/economic rights exist.**

**AUTHORITY answers who may cause the next state change.**

**NOTICE/CLAIMS answers what burdens or competing rights were known at that moment.**

**EVIDENCE proves what was true, by whom, and when.**

A conforming implementation MUST represent these as separate, evidence-linked states and MUST NOT use one as a proxy for another.

## Canonical model

```text
M5HUM / LEGAL PRINCIPAL
        ↓
IDENTITY + CREDENTIAL + AUTHORITY
        ↓
UNDERLYING ASSET / RIGHT
        ↓
TITLECHAIN TITLE / RIGHT STATE
  ├─ origin / provenance
  ├─ authoritative title source
  ├─ owner / right holder
  ├─ liens / claims
  ├─ encumbrances
  ├─ obligations
  ├─ restrictions
  ├─ notices
  ├─ standing
  └─ verified by / when
        ↓
DIGITAL REPRESENTATION / CER
        ↓
ARTICLE 12 CONTROL STATE
  ├─ BENEFIT
  ├─ EXCLUDE
  ├─ TRANSFER
  └─ IDENTIFY
        ↓
SHARED / DELEGATED CONTROL ANALYSIS
        ↓
TRANSFER AUTHORITY
        ↓
M5CANON SIX GATES
        ↓
TRANSACTION-BOUNDARY SNAPSHOT
  ├─ title state
  ├─ CER control state
  ├─ claims / encumbrances
  ├─ notice state
  ├─ filing / secured-interest state
  ├─ approvals
  ├─ jurisdiction + applicable enactment
  ├─ authoritative record update
  └─ timestamp + evidence receipt
```

## Normative non-inference rule

> **TitleChain/M5 MUST NOT infer legal title, ownership of underlying property, or transfer authority solely from possession of a private key, wallet access, token ownership, ledger state, or technical satisfaction of an Article 12 CER-control test.**

A conforming implementation MUST keep the following state dimensions separate and MUST preserve the evidence and applicable-law basis for each conclusion:

1. legal title or rights in the underlying asset or right;
2. control of the CER;
3. property claims in the CER;
4. claims, liens, encumbrances, and obligations affecting underlying property;
5. notice relevant to purchaser status or other legal analysis;
6. Article 9 filing and secured-interest state;
7. transfer authority; and
8. authoritative-record update and reconciliation state.

## Four-part CER control proof

An Article 12 control determination under the applicable enactment of UCC §12-105 MUST record four separate proof results rather than one undifferentiated key-possession result:

| Proof | Required question |
| --- | --- |
| `BENEFIT` | Can the asserted controller avail itself of substantially all benefit from the electronic record? |
| `EXCLUDE` | Does the asserted controller have the legally relevant exclusive power to prevent others from availing themselves of substantially all benefit? |
| `TRANSFER` | Does the asserted controller have the legally relevant exclusive power to transfer control to another person? |
| `IDENTIFY` | Does the system enable the asserted controller to be readily identified as the person having the relevant powers? |

Each proof MUST have its own status and evidence references. `control_status` MUST NOT be `ESTABLISHED` unless all four proof statuses are `ESTABLISHED` under the applicable enactment and facts.

The four proofs MUST be evaluated for each asserted controlling person; proofs held by different people MUST NOT be aggregated to manufacture control for any one person. A record-wide status of `ESTABLISHED` requires at least one identified person with an independently supported four-part determination.

Cryptographic key possession, signing capability, wallet access, token balance, or ledger designation MAY be evidence relevant to one or more proofs. None is conclusive by itself.

## Shared, delegated, and through-person control

A conforming implementation MUST support direct, shared, delegated, custodian, transfer-agent, and through-another-person arrangements. It MUST identify each relevant person and evaluate which powers that person can exercise independently, jointly, conditionally, or not at all. Shared exercise does not automatically defeat statutory exclusivity; the implementation MUST evaluate exclusivity under the applicable enactment, including any retained power of a transferor or other statutory limitation, rather than infer the answer from signer count.

A multisignature threshold, custodian relationship, transfer-agent function, recovery arrangement, smart-contract role, or other technical configuration MUST NOT be reduced to “who holds a key.” The legal relationship, agreement, authority, revocation state, system rules, and applicable enactment remain relevant. Control through another person MUST record the other person, the asserted controlling person, the acknowledgement that control is exercised on the controlling person's behalf, supporting evidence, and any retained transferor power relevant to exclusivity. It MUST NOT silently be represented as direct unilateral control.

## Control, title, and claims

CER control and title are independent states. A finding of CER control MUST NOT be promoted into a finding that the controller acquired a right, what right was acquired, ownership of underlying property, or authority to transfer. Those questions generally depend on other law and facts.

Claims in a CER and claims affecting an underlying payment right, performance obligation, asset, security, title record, or other property MUST be modeled separately. A qualifying-purchaser analysis concerning property claims in a CER MUST NOT be represented as extinguishing or resolving claims against underlying property.

When the requirements of applicable law are independently established, the machine record MAY state that a qualifying purchaser takes the rights it acquired in the CER free of a property claim in the CER. The record MUST identify the purchaser, value, good-faith, and notice determinations and MUST limit the stated effect to the acquired CER rights. It MUST NOT extend that effect to an underlying payment right, performance obligation, asset, title, lien, encumbrance, or other property claim.

## Notice

Notice MUST be a first-class, evidence-linked TitleChain state. A qualifying-purchaser analysis MUST record the applicable notice standard, the asserted purchaser's notice status, the evaluation time, and supporting evidence.

An Article 9 financing-statement filing MUST NOT, by itself, be treated as notice of a property claim in the CER. This rule does not erase the filing, determine its validity, or resolve its relevance under other law.

## Filing, control, and title separation

A conforming implementation MUST independently track:

- filing and secured-interest state;
- CER control state; and
- legal title or underlying-right state.

A control-based priority conclusion under an applicable enactment of UCC §9-326A MUST NOT be represented as title, ownership of underlying property, or general transfer authority. Likewise, a filing does not itself establish CER control, and CER control does not itself establish that an authoritative title record was updated.

## M5Canon transaction boundary

The Article 12 state is an input to, not a substitute for, the [M5Canon Six-Gate model](M5CANON-SIX-GATE-AUTHORITY-AND-TRANSFER-CONTROL.md). Before a consequential transfer or authoritative update, the transaction-boundary snapshot MUST bind:

- the current title/right state and authoritative source;
- the four-part CER-control result;
- shared/delegated control analysis;
- separate CER and underlying-property claims;
- notice and filing/secured-interest states;
- transfer authority and required approvals;
- jurisdiction, enacted text/version, and legal-review status;
- all six M5Canon gate results;
- requested authoritative-record update; and
- timestamped evidence receipt.

Missing, stale, disputed, or inapplicable legal-state evidence MUST fail closed or route to accountable review. A technically valid transaction MUST NOT overwrite a contrary or unresolved authoritative state.

## Machine-readable record

The canonical exchange shape is [`article-12-cer-control-state.schema.json`](../schemas/article-12-cer-control-state.schema.json). The [synthetic shared-control snapshot](../examples/article-12-cer-control-state.synthetic.json) demonstrates an established technical/control assessment while title and transfer authority remain unresolved and the M5Canon decision remains `HOLD`.
