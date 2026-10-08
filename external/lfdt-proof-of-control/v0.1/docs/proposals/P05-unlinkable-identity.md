# Proposal: normative changes to C5 Identity for accountable unlinkability

**Status:** proposal only. Nothing under `/ov-poc-standard/` has been edited.
**Source research:** P05 — *Verifiable Unlinkability in Autonomous Agent Ecosystems* (`research/Accountable Unlinkable Agent Identity.md`)
**Supporting tool:** `occultation` (`bench --composed`, `pool`, `anonymity`, `occultation-gateway`)
**Targets:** `0.1/en/0x10-C05-Identity.md`, `0.1/en/0x10-C02-Privacy.md`, `0.1/en/0x10-C07-Evidence-Generation-and-Properties.md`, `0.1/en/0x10-C10-Conformance-and-Disclosure.md`, `schema/poc-evidence.schema.json`, `schema/poc-evidence.cddl`
**Resolves (partly):** Appendix D, issue 2 — *Anonymity and Pseudonymity*

---

## 0. The finding this proposal exists to answer

C5.1.1 requires every execution record to carry a persistent agent identifier and a principal
identifier. `poc-evidence.schema.json` makes `agent_id` and `initiating_user` non-optional members of
the required list in `pocClaims`. Under an unlinkable identity design there is no persistent agent
identifier to carry, and disclosing the principal to the relying party is the exact thing the design
exists to prevent.

**This is not a gap that better engineering closes.** It is a requirement that is structurally
unsatisfiable under a design the standard elsewhere says it wants — C5.2 carries a
`[WG-INPUT NEEDED]` asking for "verifiable-but-unlinkable identity binding as an implementer-selectable
option, and how", and Appendix D issue 2 records the working group's intent that the implementer be
able to select it.

`poc-audit` distinguishes this case from every other failure. Under `--profile unlinkable` it reports
`CANNOT HOLD` on the `agent_id` and `initiating_user` rows — *structurally unsatisfiable here*, which
is a different verdict from `UNCHECKED` ("we did not look") and from `ASSERTED` ("we looked and found
nothing behind it"). A standard that produces `CANNOT HOLD` findings on its own Level 1 requirements,
for a design it invited, has a specification defect rather than an implementation defect.

**The answer this proposal gives:** C5 gains an implementer-selectable **Unlinkability Profile** in
which C5.1.1 is *suspended* — not weakened, not made best-effort — and replaced by a session pseudonym
with declared, and at higher Levels cryptographically enforced, escrowed accountability. The standard
today has **no mechanism for suspending a requirement**, so that mechanism has to be introduced first
(change 1), and the schema consequence has to be a **discriminator**, not an optionality relaxation
(change 11). Section 3 states the schema answer concretely and says exactly what it costs.

### Confidence vocabulary used throughout

| tag | meaning |
| --- | --- |
| **measurement-settled** | a number or a failure was measured or derived by arithmetic over published figures; the conclusion does not depend on judgement |
| **measurement-settled (mechanism), illustrative (magnitude)** | the effect is real and reproduced by a working implementation, but the input corpus is synthetic |
| **judgement call** | a defensible design choice with alternatives; the working group can decide differently without contradicting any evidence |
| **`[MODELLED — NOT IMPLEMENTABLE TODAY]`** | rests on a component that exists only as a stub with no security whatsoever |

---

## 1. Change P05-01 — introduce the profile mechanism (new §C5.0)

**Where:** new section `C5.0 Identity Profiles`, inserted before C5.1 in `0x10-C05-Identity.md`.

**Current text:** *none.* The word "profile" appears nowhere in the requirement text of the standard
except as `eat_profile` (a URI in the evidence schema) and as prose in C10.2. There is no existing
construct by which one requirement is switched off and another substituted.

**Proposed text:**

> ## C5.0 Identity Profiles
>
> Two identity profiles are defined. Every evidence record is produced under exactly one of them, and
> the profile is declared in the record itself. A profile does not lower a requirement; it names which
> requirements apply and which are **suspended** — replaced, one for one, by a substitute requirement
> that carries its own Level and its own auditor evidence. A suspended requirement is never reported
> as met.
>
> | Profile | Token | Requirements in force |
> | --- | --- | --- |
> | **Identified** (default) | `identified` | C5.1.1–C5.1.4, C5.2.1–C5.2.2 as written |
> | **Unlinkable** | `unlinkable` | C5.1.1 **suspended**, replaced by C5.1.1-U and C5.3.1; C5.1.2–C5.1.4 and C5.2.2 as amended below; C5.1.6–C5.1.7 additionally in force |
>
> | # | Description | Level |
> | :--------: | --- | :---: |
> | **5.0.1** | **Verify that** every evidence record declares its identity profile in a field covered by the record's signature, and that a verifier presented with an unrecognised profile token rejects the record rather than defaulting to either profile. | 1 |
> | **5.0.2** | **Verify that** the conformance statement names every identity profile in force and maps each in-scope action class ([C10.1.6](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md)) to exactly one profile, and that a sampled record's declared profile matches the profile its action class is mapped to. | 1 |
> | **5.0.3** | **Verify that** for each suspended requirement the claim register records the suspension, the substitute requirement, and the Tier the substitute reaches — so a suspension is visible in the register rather than appearing as an absent claim. | 1 |
>
> **Auditor evidence:** 5.0.1 — decode a sampled record; confirm the profile field is inside the signed
> canonical form (re-verify the signature with the field altered; it must fail). Present a record
> carrying an unknown profile token to the published verifier; it must reject. 5.0.2 — the action-class
> to profile mapping in the statement, reconciled against sampled records from two different action
> classes. 5.0.3 — the claim register's suspension entries.

**Why:** The research's recommendation §1 ("Introduce the C5-Unlinkability Profile (C5-UP)") asks for
exactly this split — a `C5-Identified Profile (Default)` and a `C5-Unlinkability Profile` — but treats
the profile construct as though the standard already had one. The standard has no profile construct. Appendix D issue 2 records
the design intent ("the implementer can select the option that fits the use case"); a selector needs
somewhere to be recorded and something to check it against. `occultation`'s standard map states the
same point from the implementation side: *"An identity profile that suspends `C5.1.1`… it is a
requirement a profile must **suspend**, and the standard has no mechanism for that today."*

**Confidence:** judgement call. That *a* mechanism is required is settled by the `CANNOT HOLD` verdict;
the shape of it — per-record declaration rather than per-deployment, two profiles rather than a
capability set, suspension recorded in the claim register — is a design choice. Per-record was chosen
because one agent legitimately acts identified internally and unlinkably toward a vendor within a
single deployment, which a per-deployment flag cannot express. `[WG-INPUT NEEDED]` on whether a third
"pseudonymous-but-linkable" profile (stable pseudonym per relying party, no cross-RP unlinkability) is
worth defining; it is much cheaper than the unlinkable profile and covers Appendix D issue 4's
anti-price-discrimination case without any of the cryptography in changes 3, 5 and 8.

---

## 2. Change P05-02 — suspend C5.1.1 and substitute C5.1.1-U

**Where:** `0x10-C05-Identity.md`, requirement **5.1.1**.

**Current text (verbatim):**

> | **5.1.1** | **Verify that** every execution record carries the agent instance identifier and the principal identifier on whose behalf the action ran, so any sampled action resolves to a named principal. | 1 |

and, from the auditor-evidence line for C5.1:

> **Auditor evidence:** 5.1.1 — sampled records resolved to principals via the identity system.

**Proposed text:**

> | **5.1.1** | **Verify that** under the Identified profile every execution record carries the agent instance identifier and the principal identifier on whose behalf the action ran, so any sampled action resolves to a named principal. Under the Unlinkable profile this requirement is **suspended** and C5.1.1-U applies in its place; a record declaring the Unlinkable profile MUST NOT carry either identifier, and a verifier MUST reject a record that carries both a profile of `unlinkable` and an agent or principal identifier. | 1 |
> | **5.1.1-U** | **Verify that** under the Unlinkable profile every execution record carries a **session pseudonym** — an identifier that is stable within one session and unpredictably distinct across sessions and across relying parties — together with the identifier of the **opening policy** under which that pseudonym can be resolved to a principal, and that the opening policy is published and names who may request an opening, on what authority, and within what time. | 1 |
> | **5.1.1-E** | **Verify that** the opening capability asserted by C5.1.1-U is exercised end to end at least once against a sampled session, resolving the pseudonym to a named principal, and that the exercise is itself recorded. | 2 |
>
> **Auditor evidence (replacing the 5.1.1 line):** 5.1.1 — for Identified records, sampled records
> resolved to principals via the identity system; attempt to validate a record declaring `unlinkable`
> that also carries `agent_id` (should be rejected). 5.1.1-U — the published opening policy; confirm two
> records from different sessions carry unrelated pseudonyms and that neither resolves to a principal
> with the material a relying party holds. 5.1.1-E — the record of a completed opening, performed in
> test if not in production, and the evidence record that opening itself produced.

**Why:** The research's threat model defines *Session Unlinkability* and *Cross-RP Unlinkability* as
the properties the profile must deliver, and *Verifiable Tracing ("When It Matters")* as the
accountability that survives them — "under a legally valid threshold authorization, the Escrow
Authority can execute an opening algorithm, producing a publicly verifiable proof of correct opening
without compromising the unlinkability of un-escrowed sessions." Appendix D issue 4 is explicit that
the answer is pseudonymity, not anonymity: *"pure anonymity makes accountability impossible… an
identifier that is not inherently tied to a real-world human, but can be linked back to the principal
under specific, cryptographically enforced conditions."*

The Level split is deliberate and is the uncomfortable part. At **Level 1** the opening capability is a
*declared policy* — an operator's word, not a cryptographic guarantee. C5.1.1-E at **Level 2** demands
it be demonstrated once rather than merely asserted. The cryptographic version is C5.3.1 at Level 3
(change 8), and it is the one nobody can build today. Under [C8.1.2](../../0.1/en/0x10-C08-Verifiability-Tiers.md)
an accountability claim resting on a declared policy names a single trusted party and therefore **caps
at Tier 2** — it is not Proof-of-Control. Stating that plainly is better than pricing the Level 1 row
at Level 3 and leaving low-Level unlinkable deployments with no accountability requirement at all.

**Confidence:** judgement call on the Level split and on the definition of "session". Settled on the
substance: some substitute is required, because C5.1.1 as written produces `CANNOT HOLD`.
`[WG-INPUT NEEDED]` on the session boundary — per relying party, per task, per time window, or per
delegation token. This choice sets the granularity of *everything downstream*: the ephemeral chain of
change 10, the `step_index` reset of change 11, and the scope an opening warrant can name under
C5.3.3.

---

## 3. Change P05-03 — the schema consequence, stated concretely

**Where:** `schema/poc-evidence.schema.json`, `$defs.pocClaims`; and `schema/poc-evidence.cddl`, the
`poc-evidence` map.

**Current text (verbatim, JSON Schema):**

```json
      "required": [
        "agent_id", "initiating_user", "agbom_digest", "interception_point",
        "step_index", "chain_head", "merkle_root", "tree_size",
        "policy_bundle_hash", "target_resource", "canonical_snapshot_hash",
        "path_summary_hash", "verdict", "alg"
      ],
```
```json
        "agent_id": {
          "type": "string",
          "minLength": 1,
          "description": "Stable identifier for the agent instance (C5.1.1). A DID is RECOMMENDED."
        },
        "initiating_user": {
          "type": "string",
          "minLength": 1,
          "description": "The principal on whose authority the agent acts (C5.1.2). Delegation chains are represented by a chain of tokens, not by a list here."
        },
```

**Current text (verbatim, CDDL):**

```
  -70001 => agent-id,
  -70002 => principal-id,
```

### What NOT to do

**Do not remove `agent_id` and `initiating_user` from `required`.** Optionality is the obvious fix and
it is the wrong one, for four reasons that are worth naming because they are not obvious:

1. **It weakens every identified record.** Today a verifier rejects a record with no `agent_id`. Made
   optional, it must accept it and decide out of band whether that was acceptable — which is precisely
   the security-relevant judgement a schema exists to remove from the verifier's discretion.
2. **It leaves absence undefined.** `canonicalization.md` rule 7 says *"Absent is not empty. An optional
   claim that does not apply is omitted."* — and C7.7.2 requires the schema declare "the meaning of an
   absent field". "The field is optional" is not a meaning. A missing `agent_id` would be
   indistinguishable between *deliberately unlinkable* and *pipeline dropped it*.
3. **It makes a downgrade invisible.** A record produced by an identified deployment whose identity
   plumbing silently failed is schema-valid and reads identically to a deliberate unlinkable record.
4. **It gives `poc-audit` nothing to key on.** The `CANNOT HOLD` verdict exists precisely to distinguish
   structural impossibility from an unchecked field; optionality collapses the two back together.

### What to do: a required discriminator, and conditional *prohibition*

**Proposed change, JSON Schema:**

Add `identity_profile` to `pocClaims.required` — **required in every record, under both profiles** —
and make the two identifier fields conditionally **forbidden**, not conditionally optional:

```json
      "required": [
        "identity_profile", "agbom_digest", "interception_point",
        "step_index", "chain_head", "merkle_root", "tree_size",
        "policy_bundle_hash", "target_resource", "canonical_snapshot_hash",
        "path_summary_hash", "verdict", "alg"
      ],
```
```json
        "identity_profile": {
          "enum": ["identified", "unlinkable"],
          "description": "Which C5.0 identity profile produced this record. Covered by the signature. A verifier that does not recognise the value MUST reject the record (C5.0.1)."
        },
        "session_pseudonym": {
          "type": "string", "minLength": 16,
          "description": "Stable within one session, unpredictably distinct across sessions and relying parties (C5.1.1-U). Unlinkable profile only."
        },
        "opening_policy_id": {
          "type": "string", "format": "uri",
          "description": "The published policy under which this pseudonym can be resolved to a principal (C5.1.1-U). Unlinkable profile only."
        },
        "escrow_tag": {
          "$ref": "#/$defs/hex",
          "description": "Threshold encryption of the true agent identity under the escrow public key, with its NIZK (C5.3.1). Unlinkable profile, Level 3."
        },
```
```json
      "allOf": [
        { "if":   { "properties": { "identity_profile": { "const": "identified" } },
                    "required": ["identity_profile"] },
          "then": { "required": ["agent_id", "initiating_user"],
                    "not": { "anyOf": [ {"required": ["session_pseudonym"]},
                                        {"required": ["escrow_tag"]} ] } } },
        { "if":   { "properties": { "identity_profile": { "const": "unlinkable" } },
                    "required": ["identity_profile"] },
          "then": { "required": ["session_pseudonym", "opening_policy_id"],
                    "not": { "anyOf": [ {"required": ["agent_id"]},
                                        {"required": ["initiating_user"]} ] } } }
      ],
```

**Proposed change, CDDL:** allocate `-70014 => identity-profile`, `-70015 => session-pseudonym`,
`-70016 => opening-policy-id`, `-70017 => escrow-tag` in the same provisional range, and express the
two shapes as a CDDL choice so `-70001`/`-70002` and `-70015`/`-70016` are mutually exclusive rather
than both optional. The two renderings must stay structurally equivalent, which the file already
requires.

**Why this is not the weakening:**

- Under `identified`, **nothing changes.** `agent_id` and `initiating_user` remain required and a record
  lacking either is still rejected. Reason (1) above is answered directly.
- Absence acquires a declared meaning: under `unlinkable` the fields are **forbidden**, so their absence
  is a positive statement, not a silence. C7.7.2 is satisfiable again.
- The discriminator sits inside the signed canonical form, so the regime a record was produced under
  cannot be inferred, stripped, or retro-fitted without invalidating the signature.
- Old verifiers **fail closed**: a pre-change verifier applying the current `required` list to an
  unlinkable record rejects it for the missing `agent_id`. That is the correct direction of failure.

**The residual honesty:** the discriminator is chosen by the record's *producer*. An operator who wants
to hide can stamp `unlinkable` on records that could have carried identifiers, and no schema can stop
that. What catches it is C5.0.2 plus the conformance statement's action-class-to-profile map: a record
whose declared profile differs from the profile its action class is mapped to is a **divergence**, and
`poc-audit` should report `DIVERGES` on it — two parties who must agree producing different values —
not `CANNOT HOLD`. That check is only as good as the action-class map, which is prose. It is a
meaningful improvement over optionality and it is not a proof.

**Confidence:** measurement-settled that optionality is insufficient (the four failure modes are
properties of the current schema text and canonicalization rules, checkable by reading them).
Judgement call on the field names, on `minLength: 16`, and on using `if`/`then` rather than a
`oneOf` over two closed sub-schemas.

**Also, editorially:** `initiating_user`'s description cites **(C5.1.2)**. C5.1.2 is about credential
authentication; the requirement mandating the principal identifier is **C5.1.1**. The CDDL comment
repeats the same mis-citation. Worth fixing in the same pass.

---

## 4. Change P05-04 — C5.1.2 under the Unlinkable profile

**Where:** `0x10-C05-Identity.md`, requirement **5.1.2**.

**Current text (verbatim):**

> | **5.1.2** | **Verify that** the agent authenticates with a cryptographic credential (certificate, key pair, or DID) validated before actions execute, and that credential-validation events are recorded. | 2 |

**Proposed text:** keep 5.1.2 unchanged and add a scoped sentence:

> Under the Unlinkable profile, "validated" means the relying party verified a zero-knowledge
> presentation of a credential issued by a recognised issuer, and the recorded validation event MUST
> record the issuer and the presentation's verification outcome **without** recording any value that
> identifies the presenting agent across sessions.

**Why:** C5.1.2's own auditor evidence asks for a "credential inventory and validation logs, including
one failed validation" — an inventory keyed by agent is exactly the dossier the profile exists to
prevent. The research's Unlinkable Agent Credential Layer supplies the substitute: BBS+ presentations
where "every derivation of the BBS+ signature incorporates a fresh blinding factor, [so] two
presentations derived from the identical underlying credential are statistically unlinkable."

**Confidence:** judgement call on wording; measurement-settled that a per-agent validation log defeats
the profile (that is the Log Operator Correlation adversary in the research's threat model, and it is
the same failure `occultation-gateway` designs against — "a tool that warns a relying party it is
quietly building a profile of its counterparties must not build that profile itself").

---

## 5. Change P05-05 — C5.1.3, the delegation token becomes a delegation *proof*

**Where:** `0x10-C05-Identity.md`, requirement **5.1.3**.

**Current text (verbatim):**

> | **5.1.3** | **Verify that** each agent tool call carries a delegation token (short-lived OAuth/JWT, W3C verifiable credential, or capability URL) issued by or on behalf of the principal, cryptographically linking the call to the principal's grant. | 2 |

**Proposed text:**

> | **5.1.3** | **Verify that** each agent tool call carries a delegation token (short-lived OAuth/JWT, W3C verifiable credential, or capability URL) issued by or on behalf of the principal, cryptographically linking the call to the principal's grant. Under the Unlinkable profile, the call instead carries a **zero-knowledge presentation** proving that the agent holds a delegation credential signed by a recognised issuer, that the credential's authorization scope covers this call, and that the presenter controls the delegated key — disclosing only the attributes the relying party's stated policy requires. | 2 |
> | **5.1.3-U** | **Verify that** the presentation format used under the Unlinkable profile has **published test vectors including negative cases** ([C7.7.4](../../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md)) and that the implementation passes them, so an independent verifier can validate a presentation without the issuer's implementation. | 3 |

**Why:** This is exactly the mechanism Appendix D issue 4 asks for, in the contributor's own terms —
the agent proves *"I have a valid delegation signature from a trusted issuer/principal; that
issuer/principal meets your requirements; I… mathematically control the specific private key delegated
to this capability"*. The research supplies the primitive (BBS+ over BLS12-381 with selective
disclosure).

**5.1.3-U is the gate, and it is the essential part of this change.** `occultation` implements real
BBS+ against `draft-irtf-cfrg-bbs-signatures` — forged signatures fail, tampered proofs fail,
undisclosed attributes stay undisclosed, each asserted by test — but it is **"not validated against the
draft's test vectors, so its wire encoding will not interoperate with another BBS+ implementation."**
The standard already demands published test vectors with negative cases at C7.7.4. Today no BBS+
presentation profile satisfies that for this schema. Without 5.1.3-U, C5.1.3 under the Unlinkable
profile is a requirement that two conformant implementations can both meet and still fail to talk to
each other, which is the interoperability failure C7.7 exists to prevent.

**Confidence:** measurement-settled that interoperability is currently absent (stated as a limitation
by the only implementation). Judgement call that the profile should be gated on it at Level 3 rather
than declared non-claimable until vectors exist. `[WG-INPUT NEEDED]` on whether to publish a BBS+
presentation profile for the Proof-of-Control evidence schema or to normatively reference an external one once
`draft-irtf-cfrg-bbs-signatures` stabilises.

---

## 6. Change P05-06 — C5.1.4 and the anonymity set that is not there

**Where:** `0x10-C05-Identity.md`, requirement **5.1.4**; new **5.1.5**.

**Current text (verbatim):**

> | **5.1.4** | **Verify that** the agent's identity credential is bound to an attested execution environment (key held in the attested enclave or TPM), so the credential cannot be exercised from an environment that fails attestation. | 3 |

and:

> 5.1.4 — key-custody configuration; attempt credential use from an unattested environment in test (should fail).

**Proposed text:** 5.1.4 unchanged, plus a new requirement:

> | **5.1.5** | **Verify that** under the Unlinkable profile the operator measures, on a defined schedule, the **anonymity set** its attestation evidence induces — the number of hosts in the fleet indistinguishable from one another on the platform configuration fields a relying party can read out of a verified quote — and that the measurement, the minimum set size, the number of singletons, and the attributes doing the splitting are recorded and disclosed under [C10.2](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md). | 3 |
> | **5.1.6** | **Verify that** the deployment declares a minimum anonymity set size below which it will not present unlinkable credentials, and that a host whose platform configuration falls below it is either withheld from unlinkable operation or moved to a configuration that is not. | 4 |
>
> **Auditor evidence:** 5.1.5 — the scheduled measurement's output for the current fleet; recompute the
> partition yourself from the fleet's quote collateral. 5.1.6 — the declared minimum, and one recorded
> instance of a host being withheld or remediated.

**Why:** C5.1.4 binds the credential to the attested environment — and the binding *leaks*. TDX quote
collateral is itself a fingerprint, so two agents on different patch levels are separable **even under
perfect anonymous attestation**, before any credential is presented. `occultation anonymity` on a
120-host fleet after six weeks of ordinary drift — "a patch wave 60% done, a rack that missed two
maintenance windows, one machine rebuilt last week" — partitions 71 / 34 / 11 / 3 / 1: effective set
size 52.73, entropy 1.470 bits, **one host alone on its configuration**. Nothing exotic happened. The
unlinkability the rest of this proposal buys is worth nothing on that host.

Two corrections that the specification text must inherit, because the research gets them wrong:

- The research and the desk study describe the attestation fingerprint as "TDX module version, CPU SVN,
  PCE SVN, microcode revision, QE identity, PCS chain". Measured against `dcap-qvl` 0.6 there is **no
  `pce_svn` and no `microcode`** on any report type — PCE SVN lives in the PCK certificate extension,
  not the report body, and microcode revision is not exposed as a field at all. The real list is
  `fmspc`, `tee_tcb_svn` (`+ tee_tcb_svn2` on TDX 1.5), `mr_seam`, `mr_signer_seam`, `seam_attributes`,
  `td_attributes`, `xfam` for TDX; `fmspc`, `cpu_svn`, `attributes`, `misc_select`, `isv_prod_id`,
  `isv_svn` for SGX. 5.1.5 should not enumerate fields in normative text; it should say "the platform
  configuration fields a relying party can read out of a verified quote" and leave the list to the
  attestation technology.
- An anonymity set counted over *sessions* is an **upper bound on anonymity, never a measurement of
  it**: one counterparty replaying one attestation twelve times is indistinguishable from twelve
  agents sharing a configuration, and telling them apart requires retaining the correlation the
  measurement exists to refuse to build.

**Confidence:** measurement-settled (mechanism), illustrative (magnitude). The partitioner is real and
the field list is measured against a real DCAP verifier; the 120-host fleet is a **synthetic,
hand-authored fixture, not telemetry from any live deployment**. The mechanism — ordinary patch drift
fragments the anonymity set to singletons — is not in doubt. The specific numbers are an illustration
and must not be written into normative text.

The **minimum set size** in 5.1.6 is a pure judgement call, and the only comparable constants in the
tool are labelled as judgement calls at their definitions (`MIN_MEANINGFUL_SESSIONS = 10`,
`MIN_SALT_ROTATION = 1s`). `[WG-INPUT NEEDED]` on the value, and on whether the standard should name
one at all rather than requiring the deployment to declare and justify its own.

---

## 7. Change P05-07 — the composed-path budget, and mandatory pre-computation

**Where:** `0x10-C05-Identity.md`, new **5.1.7** and **5.1.8**.

**Current text:** *none.* No requirement in C5 constrains the latency of identity verification, and
nothing anywhere requires that presentation and verification be assessed together.

**Proposed text:**

> | **5.1.7** | **Verify that** the deployment's stated per-action latency budget is assessed against the **sum** of credential presentation and credential verification measured as a single composed path — not against either phase in isolation — and that the measurement is taken on the deployment's own hardware with the pre-computation pool in its production configuration. | 2 |
> | **5.1.8** | **Verify that** where the budget is met only with pre-computed presentation material, the deployment records the pool's configured depth and refill rate, its measured exhaustion behaviour under the burst rate the deployment is sized for, and the response latency at exhaustion — and that this is disclosed under [C10.2](../../0.1/en/0x10-C10-Conformance-and-Disclosure.md) as a mechanism the claim depends on. | 3 |
>
> **Auditor evidence:** 5.1.7 — the composed-path measurement run; repeat it yourself on the deployment's
> hardware and confirm the reported figure is present-plus-verify, not one phase. 5.1.8 — the pool
> configuration, the burst test's output, and the disclosure entry naming pre-computation as a essential
> mechanism.

**Why — this is the correction the desk study needs, and it is measurement-settled.**

The research says, in its conclusion: *"Core presentation operations consume ~13.8 ms, remaining within
the 15 ms processing SLA enforced by modern enterprise agent platforms."* Verification is separately
priced at 4.2 ms and separately marked "Fully Compatible". **Each phase was assessed against the budget
alone; each looked acceptable; an action pays for both.**

```
naive (no pool, no cached pairings)     13.80 ms   4.20 ms  18.00 ms  MISSES by 3.00 ms
cached pairings only                    13.80 ms   1.10 ms  14.90 ms  MARGINAL — 0.10 ms spare
pre-computation pool + cached pairings   2.80 ms   1.10 ms   3.90 ms  fits, 11.10 ms spare
```

18 ms against a 15 ms budget. The middle row is the more instructive failure: 14.9 ms is *under* the
limit by 100 µs, with nothing left for the application, the network, or writing the evidence record —
and calling that a pass is how the original error was made twice. **The mistake is in the addition, not
in the silicon**; faster hardware changes nothing about the arithmetic.

Only one composition fits, and it is the one depending on a pool of pre-computed blinding factors. That
turns a performance property into a **security precondition**, which is why 5.1.7 mandates the composed
measurement rather than assuming it and why 5.1.8 forces the pool into the disclosure.

**Two things the specification must not do:**

- **It must not name 15 ms, 13.8 ms, or 2.8 ms in normative text.** The budget belongs to the
  deployment. And the pooled figure is not a measurement: **no command in `occultation` measures a
  pooled presentation's online phase.** The 2.8 ms is an estimate — two hash-to-scalar operations —
  and is "almost certainly too low: it implies a 99% reduction where the desk study's own pooled
  figure implies 80%." A specification that hard-coded it would enshrine an unmeasured number.
- **It must not assume the escrow tag is free.** The 13.8 ms presentation figure *already includes*
  4.6 ms of threshold-ElGamal ciphertext plus DLEQ proof construction — the published breakdown sums
  to 13.80 ms across five phases, of which escrow is 4.60 ms. Arithmetic on the published figures:
  unlinkability **without** accountability costs ≈ 9.2 ms present + 4.2 ms verify = **13.4 ms, which
  fits 15 ms naively**. It is the *accountability*, not the unlinkability, that breaks the budget. That
  is a materially different framing from the research's, and it means an implementer who quietly drops
  the escrow tag gets a comfortable budget and no accountability — which is precisely the failure mode
  C5.1.1-U and C5.3.1 exist to make visible.

**Confidence:** measurement-settled on the composition error and on the three compositions above (all
three are arithmetic over the research's own published figures, and the tool prints them labelled
`PUBLISHED — not measured on this stack`). Measurement-settled on the escrow decomposition (arithmetic
over the research's own micro-architectural breakdown: 12.9 + 74.3 + 792.6 + 8,320.0 + 4,600.0 µs).
The 2.8 ms pooled online figure is explicitly **`ESTIMATED`** and is the reason 5.1.7 requires the
deployment to measure rather than to cite.

---

## 8. Change P05-08 — blinding-factor non-reuse, and what exhaustion leaks

**Where:** `0x10-C05-Identity.md`, new **5.1.9** and **5.1.10**.

**Current text:** *none.*

**Proposed text:**

> | **5.1.9** | **Verify that** the presentation implementation cannot reuse a blinding factor across two presentations — enforced by the implementation rather than by configuration, with no operator-settable option to permit it — and that the property is demonstrated by a test that attempts reuse and fails. | 2 |
> | **5.1.10** | **Verify that** the behaviour on pre-computation pool exhaustion is declared (the only admissible behaviour is to delay the presentation), that the resulting delay under the deployment's sized burst is measured and recorded, and that the deployment states whether that delay is observable to the relying party and what it discloses about the agent's load. | 3 |

**Why:** Reuse is not a degradation of unlinkability; **it hands over the credential.** Two
presentations sharing one blinding factor carry the same `Abar` and `D`, so a relying party links them
on sight — and because the two transcripts carry different challenges over the same commitments, the
witness falls out by subtraction:

```
e    = (ê₁ − ê₂) / (c₁ − c₂)
m_j  = (m̂_j₁ − m̂_j₂) / (c₁ − c₂)
```

The signature scalar and every undisclosed attribute, recovered by anyone who sees both. `occultation`'s
test suite performs that extraction against known values rather than asserting it. This is why 5.1.9
demands the property be structural rather than configurable: an operator facing a latency SLA and an
empty pool has an obvious and catastrophic shortcut, and a config flag is not a defence against it.

5.1.10 covers the cost of the only other option. Stalling is not free: at a 3.5× overload the pool
empties after 89 requests and every one of the remaining 9,911 waits; the delay does not plateau, it
grows for as long as the burst lasts (8.33× idle-response added per successive stall, peaking at
82,591× amplification over a 2 s window). **An observer reads the agent's load, and the burst's
duration, off response latency alone.** That is a side channel the design has to answer for, and the
desk study never asked the question.

**Confidence:** measurement-settled. The witness-extraction algebra is executed by a test against known
values, not asserted. The exhaustion figures come from a real pool implementation, though the arrival
process is simulated and the online-cost input is the `ESTIMATED` figure from change 7 — so the
*shape* (unbounded growth, load-observable) is settled and the specific amplification number is
configuration-dependent, which is why 5.1.10 requires the deployment to measure its own.

---

## 9. Change P05-09 — C5.2.2 has no sender identity to validate

**Where:** `0x10-C05-Identity.md`, requirement **5.2.2**, and the `[WG-INPUT NEEDED]` block below C5.2.

**Current text (verbatim):**

> | **5.2.2** | **Verify that** the receiving party can validate sender identity and message integrity using published key material, without contacting the sender's operator. | 3 |

and:

> > **[WG-INPUT NEEDED]** — anonymity and pseudonymity: whether the standard supports
> > verifiable-but-unlinkable identity binding as an implementer-selectable option, and how. See
> > [Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md), issues 2 and 4.

**Proposed text:**

> | **5.2.2** | **Verify that** the receiving party can validate sender identity and message integrity using published key material, without contacting the sender's operator. Under the Unlinkable profile, "sender identity" is the sender's **issuer group**: the receiver validates, from published issuer key material alone and without contacting the sender's operator, that the message was signed by a member of a named group and that its integrity holds — and the receiver MUST NOT be able to determine which member. | 3 |

and replace the `[WG-INPUT NEEDED]` block with a pointer to the new C5.0, retaining an issue marker
only for the questions this proposal leaves open (listed in §13).

**Why:** Under unlinkability there is no persistent sender identity to validate, so C5.2.2 as written is
the second requirement in structural tension with the profile. The research's Anonymous Hardware
Attestation Layer supplies the group-membership substitute, and the framing generalises: the receiver
learns *membership*, not *member*. This is also the requirement `occultation` was built to answer — it
is the `[WG-INPUT NEEDED]` marked against C5.2 in the standard today.

**Confidence:** judgement call. Rewriting "sender identity" as "issuer group" is one of at least two
defensible readings; the other is to suspend 5.2.2 outright under the profile, as C5.1.1 is suspended.
Group validation is proposed because it preserves something a receiver can actually check, which
suspension does not. `[WG-INPUT NEEDED]`.

---

## 10. Change P05-10 — C5.3 Accountable Opening `[MODELLED — NOT IMPLEMENTABLE TODAY]`

**Where:** `0x10-C05-Identity.md`, new section `C5.3 Accountable Opening`.

**Current text:** *none.*

**Proposed text:**

> ## C5.3 Accountable Opening
>
> Under the Unlinkable profile, accountability is not the absence of a link — it is a link that exists
> and can only be followed under declared conditions by parties who cannot act alone.
>
> | # | Description | Level |
> | :--------: | --- | :---: |
> | **5.3.1** | **Verify that** each record produced under the Unlinkable profile carries an **escrow tag** encrypting the agent's true identity under a threshold public key, together with a zero-knowledge proof that the tag encrypts an identity bound to the credential presented for that action — so that a relying party can confirm an opening is *possible* without learning who. | 3 |
> | **5.3.2** | **Verify that** the escrow key is generated by a distributed key-generation ceremony among independently controlled authorities, that no assembled private key exists at rest or in memory at any point, that opening requires t of n authorities, and that the ceremony transcript is published. | 3 |
> | **5.3.3** | **Verify that** an opening is **scope-bound**: the authorization names specific sessions, and opening one session yields no capability to open any other session by the same agent — demonstrated by attempting a second opening with the material produced by the first (should fail). | 3 |
> | **5.3.4** | **Verify that** every opening emits a receipt to a publicly monitored append-only log naming the legal authorization, the session opened, and the participating authorities' proofs, so that the volume and targeting of openings are externally observable. | 3 |
> | **5.3.5** | **Verify that** each authority holds its share in non-exportable hardware and that the authorities are independently controlled — different organisations, and where the opening policy claims it, different jurisdictions — with the independence claim evidenced rather than asserted. | 4 |
>
> **Auditor evidence:** 5.3.1 — validate one escrow tag's proof yourself with the published verifier;
> confirm it reveals no identity. 5.3.2 — the DKG transcript and each authority's custody attestation.
> 5.3.3 — the second-opening attempt and its failure. 5.3.4 — the public log; count openings over the
> claim period and reconcile against the opening register. 5.3.5 — the independence evidence
> (ownership, control, jurisdiction) per authority.

**Why:** The research's Governance section is the strongest part of it and its four principles map
one-to-one onto 5.3.2–5.3.5: no single point of failure or surveillance; public unmasking
transparency; anti-scope-creep cryptographic scoping ("decrypting one session identifier provides zero
mathematical leverage to unmask prior or subsequent transactions"); hardware-enforced judicial
rulesets. The Clipper Chip precedent it cites — "vulnerable centralized key depositories, fragile
operational controls, and a lack of transparency" — is the reason 5.3.4 is a requirement rather than
an operational nicety: without an observable opening volume, a threshold scheme is a bulk-surveillance
capability with extra steps.

**`[MODELLED — NOT IMPLEMENTABLE TODAY]`.** This must be stated in the standard, not only here.
Threshold ElGamal escrow exists in the only supporting implementation as `ModelledThresholdElGamal`, a
stub that "carries the correct interface and a representative cost profile" and provides **"no
anonymity, no soundness, no confidentiality, and no accountability."** Four independent barriers exist
to stop it being mistaken for the real thing, including that a valid verdict is *unreachable* from it.
The same applies to the ECDAA layer underneath change 9's group validation (`ModelledEcdaa`, same
status). **No one can build C5.3.1 today**, and the same is true of any anonymous hardware attestation
requirement. Nothing in this section may be cited as met by any deployment until a real
implementation exists; the research's cost figures for it (4.6 ms of the 13.8 ms presentation) come
from a stub and are indicative only.

**Confidence:** judgement call throughout — `t`, `n`, the jurisdiction requirement, and the Level
assignments. The *unimplementability* is measurement-settled: it is asserted by the implementation's
own tests. `[WG-INPUT NEEDED]` on `t`-of-`n` and on whether the standard names a minimum `n` or
requires only that it be declared and justified.

---

## 11. Change P05-11 — C7.3.1 and the evidence chain that links everything

**Where:** `0x10-C07-Evidence-Generation-and-Properties.md`, requirement **7.3.1**.

**Current text (verbatim):**

> | **7.3.1** | **Verify that** evidence records are hash-chained or Merkle-anchored so that modifying, inserting, or reordering any record invalidates the chain, and that chain verification runs on a defined schedule with results recorded. | 2 |

**Proposed text:**

> | **7.3.1** | **Verify that** evidence records are hash-chained or Merkle-anchored so that modifying, inserting, or reordering any record invalidates the chain, and that chain verification runs on a defined schedule with results recorded. Under the [Unlinkable identity profile](../../0.1/en/0x10-C05-Identity.md), the chain MAY be decoupled into per-session chains whose roots are published to the transparency log under re-randomizable commitments, provided that (a) tamper-evidence within each session is unchanged, (b) inclusion remains verifiable in zero knowledge, and (c) the conformance statement records that **cross-session completeness is not externally verifiable under this structure**. | 2 |
> | **7.3.6** | **Verify that** where per-session chains are used, the operator retains an internal reconciliation that accounts for every session against the sessions its gateway initiated, and that this reconciliation is available to an assessor even though it is not available to a relying party. | 3 |

**Why:** A global, linear, publicly anchored chain is, in the research's words, "an absolute worst-case
scenario for privacy: a permanent, ordered, cryptographically bound record of all historical
operations". Its recommendation §2 proposes ephemeral session chains with Pedersen-commitment
publication, and that mechanism does break cross-session linkability.

**What it surrenders has to be written down.** A global chain proves *no action was deleted*. Decoupled
per-session chains prove no action was deleted **within a session**, and a whole session can be omitted
without any external observer detecting it. That interacts directly with C7.6.2 (per-source monotonic
sequence numbers, so a verifier detects a missing record from the sequence gap alone) and C10.3.2
(reconcile gateway action counts against evidence-record counts with zero unexplained difference).
Both remain satisfiable *by the operator, to an assessor* — the enterprise is hiding from relying
parties, not from itself — and both become unsatisfiable *by an external verifier*. Clause (c) and
7.3.6 make that split explicit rather than letting a Tier 3 completeness claim quietly rest on a
structure that cannot support it externally.

**Confidence:** measurement-settled that the trade-off exists (it is a property of the structure, not
an implementation detail). Judgement call on placing the burden in a conformance-statement disclosure
plus an assessor-visible reconciliation, rather than forbidding decoupling at Level 3+.
`[WG-INPUT NEEDED]` on whether a session-count commitment — periodically publishing the number of
sessions opened, without their contents — recovers enough external completeness to be worth requiring;
the research does not consider it and nothing has measured what it would leak.

---

## 12. Change P05-12 — C2.3, the ZK path C2 specified and never built

**Where:** `0x10-C02-Privacy.md`, requirement **2.3.1**; new **2.3.4**.

**Current text (verbatim):**

> | **2.3.1** | **Verify that** where evidence at Tier 3 would re-leak protected inputs, the implementation substitutes a zero-knowledge proof of policy adherence, a selective disclosure, or a commitment — and that an external verifier can validate it without seeing the inputs. | 3 |

**Proposed text:** 2.3.1 unchanged; add:

> | **2.3.4** | **Verify that** where an agent transacts with a third party under the Unlinkable identity profile, no persistent identifier of the agent, the principal, or the execution hardware crosses to that third party — enumerated as a checked list rather than asserted — and that what does cross is a selective disclosure or zero-knowledge presentation of only the attributes the third party's stated policy requires. | 2 |

**Why:** The research's recommendation §3 asks C2 to "mandate that agents operating under C5-UP omit
persistent identifiers (`initiating_user`, static `agent_id`, physical hardware serials) during
third-party interactions". C2.3.1 already names the mechanism — a ZK proof, a selective disclosure, a
commitment — but only as a *substitute for leaky evidence at Tier 3*, and only where the evidence
would re-leak. It does not say that identity itself is such a case, and nothing in C2 currently
requires that identifiers stay behind. 2.3.4 closes that at Level 2, where the data-minimisation
obligation actually bites, rather than at Tier-3-only.

The "enumerated as a checked list" clause is essential and comes from the measurement: the
hardware identifier is the one people forget, and platform configuration crosses the boundary in the
attestation whether or not anyone intended it to (change 6). Note also `occultation-gateway`'s finding
that a JSON stream of verified findings "carries the full platform configuration, in cleartext… one
record per request. Wire that stream into a log store and you hold a timestamped platform fingerprint
per request, joinable against whatever `agent_id` or token your access log already has." **Retaining
the measurement stream is retaining the dossier.** 2.3.4's enumeration should include the telemetry
the privacy machinery itself emits.

**Confidence:** judgement call on Level 2 and on the enumeration requirement. Measurement-settled that
the hardware channel is real and is missed by the obvious reading (that is change 6's finding, and the
gateway's own JSON surface demonstrates the self-inflicted version of it).

---

## 13. Change P05-13 — C10.1.4, the claim must name the profile

**Where:** `0x10-C10-Conformance-and-Disclosure.md`, requirement **10.1.4**.

**Current text (verbatim):**

> | **10.1.4** | **Verify that** the statement contains all required fields: system identification (name, version, environment); domains claimed; per-claim evidence properties met and Tier reached; mechanisms used; and the trust-assumption disclosure. | 1 |

**Proposed text:**

> | **10.1.4** | **Verify that** the statement contains all required fields: system identification (name, version, environment); domains claimed; **the identity profile or profiles in force and the action classes mapped to each**; per-claim evidence properties met and Tier reached; **every requirement suspended by a profile and the substitute in force for it**; mechanisms used; and the trust-assumption disclosure. | 1 |

**Why:** A verifier's capabilities differ by profile — what it can check, what it must accept on the
operator's word, and what it can never establish alone are all different under the Unlinkable profile.
A conformance statement that does not name the profile is not comparable with one that does, which
defeats C10's stated purpose of making claims "comparable across implementations and useful to the
insurers and regulators pricing residual risk". The research's recommendation §4 asks for the same
thing. The second addition — suspended requirements named in the statement, not only in the register —
is what stops a suspension reading as a silently absent claim.

**Confidence:** judgement call on wording; the requirement itself follows directly from change 1.

---

## 14. Open questions requiring working-group ratification

| # | Question | Where it bites |
| :--: | --- | --- |
| 1 | `[WG-INPUT NEEDED]` Is a third **pseudonymous-but-linkable** profile worth defining (stable per-RP pseudonym, no cross-RP unlinkability)? It is dramatically cheaper and covers most of Appendix D issue 4's motivating cases. | change 1 |
| 2 | `[WG-INPUT NEEDED]` What is a **session**? Per relying party, per task, per time window, per delegation token. Sets the granularity of the pseudonym, the ephemeral chain, `step_index`, and the scope an opening warrant can name. | changes 2, 10, 11 |
| 3 | `[WG-INPUT NEEDED]` Does the **escrow tag bind to the action or only to the session**? If only to the session it is fully pre-computable off the online path, which is worth ~4.6 ms of a 15 ms budget; if it binds to the action it is not, and change 7's arithmetic changes. The research does not say. Nothing has measured what pre-computed tags reused within a session leak. | changes 7, 10 |
| 4 | `[WG-INPUT NEEDED]` `t`-of-`n` for escrow, and whether the standard names a minimum `n` and a jurisdiction-diversity requirement or requires only that they be declared and justified. | change 10 |
| 5 | `[WG-INPUT NEEDED]` Minimum anonymity set size, and whether the standard names a value at all. Every comparable constant in the supporting tool is labelled a judgement call by its own author. | change 6 |
| 6 | `[WG-INPUT NEEDED]` Should C5.2.2 be **rewritten to group validation** or **suspended outright** under the profile? | change 9 |
| 7 | `[WG-INPUT NEEDED]` Does a periodic **session-count commitment** recover enough external completeness to be worth requiring alongside decoupled chains? Unstudied and unmeasured. | change 11 |
| 8 | `[WG-INPUT NEEDED]` Publish a BBS+ presentation profile for the Proof-of-Control evidence schema, or normatively reference an external one once `draft-irtf-cfrg-bbs-signatures` stabilises? Until one exists, C7.7.4 cannot be satisfied for presentations. | change 5 |

---

## 15. What rests on cryptography nobody can deploy today

Stated separately so it cannot be missed, because the research does not distinguish these cases and
its conclusion asserts the whole architecture is "computationally viable".

**Unimplementable today — no security whatsoever exists behind these:**

- **All of C5.3 (changes 10)**, and any Level-3 reading of C5.1.1-U's cryptographic accountability.
  Threshold ElGamal escrow is `ModelledThresholdElGamal` — a stub with "no anonymity, no soundness, no
  confidentiality, and no accountability", from which a valid verdict is structurally unreachable. Its
  4.6 ms cost contribution is a stub's cost profile, not a measurement of working cryptography.
- **Anonymous hardware attestation**, which change 9's issuer-group reading of C5.2.2 depends on and
  which the research's ECDAA layer assumes. `ModelledEcdaa`, same status. **This means C5.2.2 under the
  Unlinkable profile has no implementable substitute today** — the honest interim position may be
  suspension (question 6) rather than the group-validation rewrite proposed.
- **SPSEQ-UC** and **ul-PCS**, named by the research, are not implemented anywhere in the supporting
  work and have no cost figures behind them beyond citation.
- **zk-STARK** proof paths are measured **incompatible** with the budget outright (238 ms generation,
  12 ms verification, ~45 KB) and should not appear in any C5 requirement.

**Real but not interoperable — buildable, not yet composable across vendors:**

- **BBS+ presentations (change 5).** Genuine cryptography with genuine, test-asserted security
  properties, but "not validated against the draft's test vectors, so its wire encoding will not
  interoperate with another BBS+ implementation". Change 5's gating requirement 5.1.3-U exists for
  exactly this and should not be dropped.
- **The whole request path.** No deployed component verifies a credential presentation. The gateway
  that measures linkability "verifies quotes, not credentials, and no BBS+ code runs in its request
  path". C5.1.3 under the Unlinkable profile currently has no reference verifier.

**Deployable today, and independent of all of the above:** <!--aais-allow-->

- **Changes 1, 2 (Level 1–2), 3, 6, 7, 8, 12, 13.** The profile mechanism, the schema discriminator, the
  anonymity-set measurement, the composed-path budget, the non-reuse and exhaustion requirements, the
  C2 identifier-omission requirement, and the conformance-statement fields need no unbuilt cryptography.
  Changes 6, 7 and 8 in particular are backed by working implementations and are the parts of this
  proposal that would catch real defects in a deployment built next quarter.

**The summary the working group should carry away:** the cost of unlinkability has been measured, the
leak has been measured, and the accountability half — the part that makes unlinkability acceptable to
the standard at all — exists only as a stub. The research is ahead of what anyone can deploy, and the
specification should adopt the profile mechanism and the measurement requirements now while marking
the escrow requirements as not-yet-claimable.
