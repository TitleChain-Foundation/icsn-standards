# Findings against the standard, from building the tools

**Date:** 2026-08-10 · **Source:** the tooling programme. Its companion documents, `TOOLING.md` and `parallax-outcomes.md`, were not published with this file and are cited below by name only.

Eight defects in `ov-poc-standard` found while designing and building the compliance
tools. Each was found by trying to *produce* or *check* an evidence record, not by
reading the specification — which is the same method that put three requirements into
the standard in the first place, and the same method
building `parallax` (recorded in the unpublished `parallax-outcomes.md`) used to correct P01.

This file exists because these are the programme's actual output to the standard, and
until now they lived only in commit messages and design prose.

| # | Where | Defect | Severity |
| :--: | --- | --- | --- |
| 1 | `schema/vectors/positive/hardware-attested.json` | `measurement` cannot be an Intel TDX MRTD | **blocking** |
| 2 | `schema/poc-evidence.schema.json` `$defs.digest` | the pattern does not tie the algorithm tag to the length | **blocking** |
| 3 | `poc_claims.chain_head` | the chain covers three fields, leaving most of the record unprotected | **blocking** |
| 4 | `poc_claims.step_index` / `chain_head` | two sequences over the same records, and no statement of which chain | high |
| 5 | `poc_claims.interception_point` | the enum has no value for C7.1.2's "during" | high |
| 6 | `poc_claims.agbom_digest` | the schema and the reference implementation already disagree | high |
| 7 | C1.2.2 | requires a link nobody can compute | high |
| 8 | top-level `nonce` | required, and nothing in the ecosystem issues one | high |

---

## 1. The `hardware-attested` vector's `measurement` cannot be an MRTD

**What it says.** `submods.attestation.measurement` is *"Measurement of the evaluated
code identity, compared against a published reference value (C8.1.7)."* The positive
vector carries:

```
"measurement": "sha-256:a1d0bdcf12b227dbe4347ce7a24a9a385a92369cd671fc1deaf9d2f7bb35cb81"
```

**Why it is wrong.** That is 64 hex characters — **32 bytes**. An Intel TDX MRTD is
**48 bytes**, SHA-384. The vector's `platform` is `INTEL_TDX`. So the standard's own
strongest positive vector carries a value that cannot be the measurement it claims to
be, and any implementation that copied its shape inherits the error.

**How it was found.** Designing T5, the offline path that would compare a record's
`measurement` against the reference values a `parallax` deployment names. The comparison
has to know how many bytes it is comparing.

**What should change.** Either the vector is corrected to a 96-hex `sha-384:` value, or
the field's description states that it is a platform-opaque digest whose mapping to a
hardware register is deployment-specific — in which case the comparison C8.1.7 asks for
is not mechanically checkable and the standard should say so. The programme has taken
the first reading; a verifier refusing any other shape under `INTEL_TDX` is what makes
the field mean something.

## 2. The `digest` pattern does not tie the tag to the length

**What it says.**

```
^(sha-256|sha-384|sha-512|sha3-256):[0-9a-f]{64,128}$
```

**Why it is wrong.** The algorithm tag and the length are independent. `sha-384:`
followed by 64 hex characters validates. So does `sha-256:` followed by 128. A record
can declare one algorithm and carry a digest of a different width, and every stage of
`validate.py` passes it.

This is the same defect class as finding 1 and it is the reason finding 1 was not caught
by the schema: the vector's own value is well-formed under this pattern.

**How it was found.** Reading the pattern to decide what T5 should refuse.

**What should change.** Split the alternation so each tag carries its own length —
`sha-256:[0-9a-f]{64}`, `sha-384:[0-9a-f]{96}`, `sha-512:[0-9a-f]{128}`,
`sha3-256:[0-9a-f]{64}`. This is a pure tightening; no currently-correct record is
rejected by it.

## 3. `chain_head` covers three fields, not the record

**What it says.**

> `chain_head` — `H(previous_head || canonical_snapshot_hash || verdict)`. Sequential
> integrity for a verifier replaying the whole history.

**Why it is wrong.** It chains three values. Every other field of the record is outside
the chain: `step_index`, `target_resource`, `policy_bundle_hash`, `path_summary_hash`,
`agbom_digest`, `agent_id`, `initiating_user`, `interception_point`, `merkle_root`,
`tree_size`, `iat`, `nonce`. Any of them can be altered without breaking a single link.

"Sequential integrity for a verifier replaying the whole history" is not what this
provides. It provides sequential integrity for the snapshot digest and the verdict.

**How it was found.** Writing `ephemeris`'s chain module, where the decision is what to
feed the hash. Extending with the **whole record digest** is strictly stronger and costs
nothing, because the digest is already computed for the Merkle leaf.

**What should change.** Define `chain_head = H(previous_head || H(canonical_record))`.
The cost is zero and the property becomes the one the prose already claims.

## 4. `step_index` and `chain_head` are two sequences and the standard names one

**What it says.** `step_index` is *"Monotonic per agent, starting at 0, with no gaps."*
`chain_head` is `H(previous_head || …)` — and nothing says which chain `previous_head`
belongs to.

**Why it is wrong.** Under a per-agent log the two agree. Under a global log they do
not: the chain's predecessor is some other agent's record, so `step_index` and chain
position are different sequences over the same records. An implementer choosing a global
log — which is the better choice for unlinkability, since membership in a shared chain
distinguishes nobody — has no guidance at all.

**How it was found.** Designing `ephemeris`'s topology trait, which implements a global
chain, per-agent chains, and per-agent trees with joint anchoring. The ambiguity is
invisible until you build more than one.

**What should change.** State the log granularity, or state that it is a deployment
choice and require the conformance claim to declare which. P08 is the paper that would
recommend one, and it is unwritten; until then, the standard should at least say that
the choice exists.

## 5. `interception_point` has no value for C7.1.2's "during"

**What it says.** C7.1.2 requires evidence at three points — *"request received
(before), effect performed (during), and result returned (after)"* — each independently <!--aais-allow-->
signed and linkable to the same action ID. The `interception_point` enum offers eight
values:

```
TASK_INITIALIZATION · CONTEXT_ASSEMBLY · PLAN_GENERATION · PRE_CALL_TOOL_INVOCATION
POST_CALL_TOOL_RESULT · MEMORY_WRITE · SUBAGENT_DELEGATION · TASK_COMPLETION
```

**Why it is wrong.** `PRE_CALL_TOOL_INVOCATION` and `POST_CALL_TOOL_RESULT` are before
and after. There is no during. A conforming implementation cannot express the middle
record of the three C7.1.2 requires, so it either omits it and fails a Level 3
requirement, or reuses a before/after value and produces two records that claim the same
interception point.

There is a second problem underneath. An interception gateway **cannot witness an
effect**. It witnesses a dispatch. A record claiming "effect performed" from a component
that only knows it forwarded a request is an overclaim, and the requirement as written
invites it.

**How it was found.** Designing T3, which has to emit the three records from a reverse
proxy.

**What should change.** Either add an enum value meaning *dispatched* — not *performed* —
or amend C7.1.2 so the middle record's meaning matches what an interception point can
accurately observe. The programme's tools emit a `record_phase` and an explicit
`observed = "request_dispatched"` under `additionalProperties`, which works and should
not have to be an extension.

## 6. `agbom_digest`: the schema and the reference implementation disagree

**What it says.** The schema: *"Digest of the agent bill of materials **in force for this
step** (C1.2)."*

The reference implementation, `impl/poc/core.py`:

```python
# digest of the agent bill of materials (C1.2) -- a fixed value here,
# since the reference agent's composition does not change at runtime
self.agbom_digest = agbom_digest or sha256(canonical({
    "agbom": "poc-ref-agent", "version": "1.0",
}))
```

computed once in `AttestingEnvironment.__init__` and emitted unchanged in every record.

**Why it is wrong.** These are the standard's two normative artifacts and they specify
different fields. The schema requires a per-step value; the implementation ships a
per-process constant. The comment is candid about it, which is to its credit, but a
reader taking the implementation as the reference gets the static reading and a reader
taking the schema gets the runtime one.

The schema's reading is the harder and the more useful one, and C1.2.1 already requires
its input half at **Level 1** — *"each input that steers agent behavior (prompts,
retrieved documents, memory reads, tool outputs) is recorded at ingestion."* The
requirement is written. The mechanism is missing.

**How it was found.** Designing `spectrum`, which had to decide what value goes in the
field.

**What should change.** Decide which reading is normative and make the other match. If
the runtime reading stands, the reference implementation needs a composition register
and the standard needs to say what `agbom_digest` means at `TASK_INITIALIZATION`, where
by definition no runtime composition has occurred yet.

## 7. C1.2.2 requires a link nobody can compute

**What it says.**

> **1.2.2** Verify that input records are hash-linked to the execution records of the
> actions **they influenced**, forming a custody chain a reviewer can walk from origin
> to action. — Level 2

**Why it is wrong.** Influence is why-provenance. No production system can determine
which retrieved chunk steered a decision; attribution in retrieval-augmented generation
is an open research area. The closest tractable relation is *was present in the
context*, which is an over-approximation including every document the model ignored.

So any implementer meeting C1.2.2 today is meeting a weaker requirement and calling it
that one. The requirement is Level 2, not Level 3, which means it is expected of ordinary
conformance.

**How it was found.** Designing `spectrum`, which records what entered the composition
and had to state explicitly that it must never name that influence.

**What should change.** Restate the requirement as presence — *inputs present in the
context at the time of the action are hash-linked to that action's execution record* —
which is checkable, honest, and still useful. If the standard wants influence, it should
say that the mechanism does not exist and grade it accordingly.

## 8. `nonce` is required and nobody issues one

**What it says.** `nonce` is in the top-level `required` array. Its description:
*"Relying-party challenge. Binds the token to one request and defeats replay (C7.1.4)."*

**Why it is wrong.** No relying party challenges an agent action anywhere in this
ecosystem today. Nothing issues a nonce. So every record anyone emits is either
schema-invalid, or carries a value the producer generated for itself — and a challenge
minted by the party being challenged defeats no replay at all.

The second case is the dangerous one, because the record validates. The field is
present, `validate.py` passes it, and the property it exists to provide is absent.

**How it was found.** An early draft of `ephemeris`'s design made exactly this mistake —
it listed `nonce` among the fields the log adds. Catching it required asking who the
relying party is when the artifact is a record rather than a handshake.

**What should change.** The standard should say who issues the challenge and how it
reaches the attester. The programme's answer is an **epoch** published by the relying
party and folded into `report_data[32..64]`, which costs one quote per refresh interval
rather than one per connection, and which makes C7.2.3's declared interval and the
enforced interval the same number. Whatever the answer, a required field that nothing
can supply accurately is worse than an optional one.

---

## What these have in common

Six of the eight are invisible to `validate.py`, and that is not a criticism of the
validator. They are defects in what the fields **mean**, and a schema checks shape.

Findings 1, 3, 4, 5 and 8 were each found by trying to build the thing that produces or
checks the field — and every one of them produces a record that **validates cleanly while
failing to carry the property the field exists to provide**. That is the same defect
shape `parallax` documented across five criticals (in the unpublished `parallax-outcomes.md`, under "The defect pattern worth carrying to transit and occultation"):
correct code implementing a subtly wrong specification, producing a confident wrong
answer rather than an error.

Finding 6 is different and worth noting separately: it is the standard disagreeing with
itself. Two normative artifacts, two readings, and nothing that would ever detect the
divergence, because no test compares the schema's prose to the implementation's
behaviour.

## Status

None of these have been filed upstream. They should be, and this file is the draft.
