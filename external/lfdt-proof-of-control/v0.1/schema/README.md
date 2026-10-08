# The Evidence Claim Set — Schema, Canonical Form, Test Vectors

This directory is the machine-readable half of the specification. Chapter
[C7](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) says in prose what
an Evidence token must contain; these files say it in a form a second
implementation can be checked against.

That distinction is the point. A claim set described only in prose produces
implementations that all believe they conform and none of which interoperate.

## What is here

| File | What it is |
| --- | --- |
| [`poc-evidence.cddl`](poc-evidence.cddl) | The normative shape, in CDDL — the form an IETF EAT profile is written in. Covers the evidence token, the dispatch capability, and the published anchor. |
| [`poc-evidence.schema.json`](poc-evidence.schema.json) | The same claim set as JSON Schema, for JWT-based deployments. |
| [`canonicalization.md`](canonicalization.md) | The exact bytes a digest or signature commits to. **Read this before implementing anything.** |
| [`validate.py`](validate.py) | A three-layer validator: structure, canonical form, semantics. No dependency beyond `jsonschema`; RFC 8785 is implemented inline so the normative behaviour is readable in one place. |
| [`cbor_profile.py`](cbor_profile.py) | The CWT/CBOR rendering and a round-trip proof that it carries the same claim set as the JSON one. |
| [`vectors/`](vectors) | Signed test vectors: positive, negative, and canonical-form. |

## Run it

```bash
python3 schema/validate.py --vectors          # every published vector
python3 schema/cbor_profile.py                # JSON <-> CBOR equivalence
python3 schema/validate.py token.json --key <hex>
python3 schema/validate.py --canonical t.json # canonical bytes and digest
```

Current state:

```
16 passed, 0 failed          (4 positive, 10 negative, 2 canonical-form)
4 identical, 0 differing     (JSON <-> CBOR round trip)
```

The reference implementation's own output is validated against this schema as
part of [`impl/tests/test_core.py`](../impl/tests/test_core.py), so the schema
and the implementation cannot drift apart without a test failing.

## The claim set

Grouped by where each claim comes from. Full definitions are in the CDDL.

**Standard, from the surrounding RFCs** — `iss`, `iat` (RFC 8392); `nonce`,
`eat_profile`, `submods` (RFC 9711). A verifier that does not recognise the
profile URI must not interpret the Proof-of-Control claims at all.

**Who and what** — `agent_id`, `initiating_user`, `agbom_digest`. The agent
instance, the principal on whose authority it acts, and the composition of the
agent at the moment it acted.

**Where in the lifecycle** — `interception_point`, one of the eight hooks of
C7.1, and `step_index`, monotonic from zero with no gaps.

**What the log commits to** — `chain_head`, `merkle_root`, `tree_size`. The
chain is what a bulk verifier replays; the tree is what lets an auditor check
one record without fetching the rest (C7.3.4).

**What was decided and why it can be re-derived** — `policy_bundle_hash`,
`target_resource`, `canonical_snapshot_hash`, `path_summary_hash`, `verdict`,
`reason`. The snapshot digest is the one the relying party recomputes; a
mismatch means the executed action is not the evidenced one.

**How to check it** — `alg`, and the attestation submodule's `platform` and
`measurement`.

## Three things worth knowing before you implement

**Digests are algorithm-tagged.** `sha-256:9f86d0…`, never a bare hex string. A
verifier handed an untagged digest must reject it rather than assume SHA-256 —
assuming the algorithm is precisely how a hash migration goes wrong, and the
failure is silent.

**The claim set contains no floating-point numbers.** Number formatting is the
hardest part of any canonicalization scheme, so the profile sidesteps it
entirely: `iat` is integer seconds, and ordering comes from `step_index`.
Snapshots carry application data and therefore do need full RFC 8785, including
its number rules.

**Absent is not empty.** An optional claim that does not apply is omitted — not
present as `""`, `{}`, or `null`. Those are four different byte strings and
therefore four different digests.

## The negative vectors

Each breaks exactly one rule, so that a validator which rejects it demonstrates
one specific check. **Rejecting a vector for the wrong reason is not a pass** —
a validator that throws on `duplicate-key.json` because it could not parse the
file has not shown it detects duplicate keys.

| Vector | Must be rejected because |
| --- | --- |
| `missing-policy-bundle-hash` | a verdict that cannot be re-derived is not evidence |
| `untagged-digest` | the hash algorithm must never be guessed |
| `wrong-profile` | claims must not be read under an unknown profile |
| `bad-interception-point` | an unrecognised hook makes coverage unassessable |
| `tree-size-too-small` | a record must be a leaf of the tree it names |
| `modify-unbound` | MODIFY must commit to the action that actually runs |
| `uppercase-hex-extension` | extension claims are open, so canonicalization is the only defence |
| `float-timestamp` | the claim set forbids floating point |
| `bad-signature` | a claim altered after signing |
| `duplicate-key` | one file that means ALLOW to one parser and DENY to another |

`duplicate-key.json` is the one worth dwelling on. It is a single artifact that
a last-wins parser reads as `ALLOW` and a first-wins parser reads as `DENY`. If
the relying party and the auditor disagree about which they are, an operator can
show each the answer it wants to see and neither can tell.

## Provisional claim keys

The CBOR claim keys are a **provisional** private-use allocation. Final keys are
subject to IANA registration through the Internet-Draft in the specification
roadmap. Do not treat the integers as stable. The round-trip property
demonstrated by `cbor_profile.py` is what is being asserted here, not the
specific values.

## The test key is published

`vectors/manifest.json` contains a private key seed. That is deliberate — the
vectors are worthless if you cannot re-sign them. It signs nothing but test
vectors. Never use it for anything else.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
