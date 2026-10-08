# Proof-of-Control — Reference Implementation

A working implementation of the evidence pipeline specified in
[`0.1/en/`](../0.1/en): action interception, path-aware policy evaluation,
hash-chained signed evidence, capability-bound dispatch, anchoring, gossip, and
open verification — with an attack harness and benchmarks.

```bash
cd impl
python3 tests/test_core.py        # 22 correctness tests
python3 attacks/run_attacks.py    # 11 attack scenarios, with and without the requirement
python3 bench/bench.py            # latency, scaling, verification, utility
python3 bench/bench_pq.py         # post-quantum signature comparison
python3 bench/bench_frontier.py   # the declassification frontier
python3 bench/bench_ops.py        # deep scaling, anchoring interval, batching, retention
python3 bench/bench_merkle.py     # inclusion and consistency proofs vs chain replay

# on a real Intel TDX confidential VM (creates and deletes two GCP instances):
./tdx/run_on_gcp.sh

cd ..
python3 schema/validate.py --vectors   # the published evidence test vectors
python3 schema/cbor_profile.py         # JSON <-> CBOR rendering equivalence
```

Requires Python 3.11+ and `cryptography` (Ed25519). Results are written to
[`results/`](results).

## What is real and what is modelled

**Real:** the protocol and every check in it. Ed25519 signing and verification,
SHA-256 hash chaining with monotonic sequence indices, canonical serialization,
policy evaluation over a bounded path summary, capability minting and
verification at the relying party, anchoring, gossip-based equivocation
detection, and fail-closed behaviour when the evidence pipeline is unavailable.
The attack harness executes real attacks against real defenses.

**Modelled:** the hardware TEE. No Intel TDX / AMD SEV-SNP machine was available,
so `AttestingEnvironment` is an in-process object whose signing key is never
returned by any method and whose "measurement" is a digest of the policy engine
identity and bundle. This reproduces the *protocol structure* the security
arguments depend on — which is what the theorems are about — but it does **not**
reproduce hardware isolation.

**Consequence for the numbers:** reported latencies exclude enclave transition
costs. A real TEE deployment adds an enclave round trip per evaluated step. The
measurements below are therefore a *lower bound* on end-to-end latency and an
accurate measure of the software components (canonicalization, policy
evaluation, signing, chaining, verification). We state this rather than
extrapolating a TEE overhead we did not measure.

## Results

Measured on Apple M2 Max, Python 3.11.11, single core; 5,000 iterations after
200 warm-up steps.

### Per-step latency

| Component | Mean | p95 | p99 |
| --- | ---: | ---: | ---: |
| Canonicalization + digest | 3.72 µs | 4.21 µs | 8.00 µs |
| Policy evaluation (path-aware) | 0.37 µs | 0.46 µs | 1.12 µs |
| Ed25519 signing | 84.25 µs | 97.96 µs | 110.12 µs |
| Chain append + Merkle root | 0.73 µs | 0.92 µs | 3.71 µs |
| **End-to-end gateway step** | **201.47 µs** | **230.58 µs** | **254.75 µs** |

Throughput: **4,963 steps/s** on one core. The end-to-end figure exceeds the sum
of components because a gateway step signs twice (evidence token and
capability) and serializes the token for the store. Signing dominates: ~87% of
the step. The design target is 15 ms per intercepted step; the software pipeline
uses **1.3% of that budget** (74× headroom), which is the margin available for
enclave transitions in a hardware deployment.

### Scaling with path length — the bounded-summary claim

| Path length | Bounded summary | Naive full-path re-evaluation |
| ---: | ---: | ---: |
| 10 | 0.250 µs | 6.04 µs |
| 100 | 0.250 µs | 65.42 µs |
| 1,000 | 0.208 µs | 655.60 µs |
| 5,000 | 0.208 µs | 3,374.65 µs |

Per-step cost with the bounded summary is **flat** across a 500× increase in
path length, confirming the O(|Π| + B) claim; the naive baseline is linear in
path length and would exhaust the 15 ms budget at roughly 22,000 steps.

### Independent verification

| Records | Total | Per record |
| ---: | ---: | ---: |
| 100 | 19.05 ms | 190.50 µs |
| 1,000 | 191.88 ms | 191.88 µs |
| 5,000 | 966.39 ms | 193.28 µs |

Verification is linear and dominated by Ed25519 verification. A verifier can
check a 5,000-step agent history in under a second, using only published keys
and reference values.

### Utility cost of path-aware authorization — and where we fooled ourselves

With no way to clear an accumulated label, the path-aware monitor refuses **42%** of perfectly
legitimate work. That is label creep, exactly as the information-flow literature predicts.

Our first version of this experiment then reported that adding a declassification point took
false rejections to **0%** — but that result was flattering, because only *benign* workflows were
allowed to declassify. A real attacker uses whatever declassification points exist.
`bench_frontier.py` fixes that: declassification is available to whoever reaches it, and the
monitor sees only that a redaction step occurred.

| Declassification | False rejections | Attacks blocked |
| --- | ---: | ---: |
| None (coverage 0) | 44.8% | 71.7% |
| Unverified, full coverage | 0.0% | **0.0%** |
| Verified, full coverage | 0.0% | **100.0%** |

**Unverified declassification is a straight trade, not a fix**: 1.60 points of detection lost for
every point of false-rejection relief, with no knee anywhere on the curve. **Verified**
declassification — where only a trusted redaction tool clears the label, and it really removes
the content — improves both quantities at once, because a genuine redaction defeats the
exfiltration it was supposed to launder.

The requirement-level conclusion: a deployment mandating path-aware authorization must specify
not only *where* declassification happens but *how the monitor verifies it*. Declassification by
annotation measurably destroys the detection the mechanism exists to provide.

Sweeping the bounded-summary label bound B from 1 to 16 made no difference on these workloads —
a null result, reported as one.

### Operational parameters, measured

**Deep scaling.** The bounded summary stays flat at 0.21–0.25 µs from 10 to 50,000 steps; naive
re-evaluation reaches 33.5 ms at 50,000 and crosses the 15 ms budget near 22,000 steps.

**Anchoring interval Δ.** One publication costs 85.7 µs; the gateway sustains ~4,989 actions/s.
Exposure and overhead are exactly inverse:

| Δ | Actions in the blind window | Publishing overhead |
| --- | ---: | ---: |
| 1 ms | 5 | 8.6% |
| 1 s | 4,989 | 0.0086% |
| 1 min | 299,316 | 0.00014% |
| 1 h | 17,958,964 | 0.0000024% |

So the choice is arithmetic: decide how many actions you could tolerate an adversary concealing,
divide by your action rate.

**Batch signing.** Signing one root per 128 actions is **64× cheaper per action** (85.7 µs →
1.3 µs; 11,663 → 745,573 actions/s), leaving actions uncovered by a signature for at most 170 µs.
That window is a second exposure parameter and belongs beside Δ in the conformance claim — not a
knob to turn as far as it goes.

**Retention.** A 1,000-agent fleet at 100 actions/agent/day, kept 7 years: 0.34 TB classically,
2.75 TB post-quantum in the JSON rendering — or **1.37 TB in the CBOR rendering**, because CBOR
carries signatures and digests as bytes rather than as hex text. Choosing the encoding saves more
than choosing the signature scheme costs.

## Post-quantum signing

Evidence is only worth what its signature is worth *when someone examines it*, which for audit
and litigation may be a decade after the fact. A scheme that becomes forgeable in 2035
retroactively destroys evidence about actions taken today, so this is a first-order concern for
an evidence standard rather than a checkbox.

**The chain is already fine.** Grover buys a square root on preimage search, so SHA-256 keeps
~128-bit security: the hash chain, sequence numbering, and anchoring survive unchanged. Only the
signatures migrate.

| Scheme | Signature | Public key | Record | Per million actions |
| --- | ---: | ---: | ---: | ---: |
| Ed25519 (classical) | 64 B | 32 B | 1,336 B | 1.34 GB |
| ML-DSA-44 (FIPS 204) | 2,420 B | 1,312 B | 10,760 B | 10.76 GB |
| ML-DSA-65 (FIPS 204) | 3,309 B | 1,952 B | 14,316 B | 14.32 GB |
| Hybrid Ed25519 + ML-DSA-44 | 2,484 B | 1,344 B | 11,016 B | 11.02 GB |

The cost is **size, not speed**: signatures grow 38×, and since the chain stores one per action,
records grow about 8×. Switching from JSON to CBOR halves every one of these figures. That is a storage and bandwidth bill, not a cryptography problem. Hybrid
costs 64 bytes more than ML-DSA alone and covers you either way, which makes it the sensible
default during transition.

> **Timing caveat.** Ed25519 here is C-backed; ML-DSA is a pure-Python reference implementation.
> The measured ML-DSA times (tens of ms) are an artifact of that and are **not** representative —
> optimized ML-DSA is competitive with Ed25519, and verification is fast. Do not cite timing
> comparisons from this benchmark. The size figures are implementation-independent and do
> transfer.

Requirements added as a result: **C6.3.4** (algorithm identified in every record; migration path
declared) and **C6.3.5** (post-quantum or hybrid signing, or scheduled re-signing, where
retention outlives the scheme).

## Proving one record without fetching the log

The evidence log began as a hash chain, and a chain has a hole in it that only
shows up when you ask an auditor's question. "Was this one action in the log?"
has no cheap answer: you fetch every record from the beginning and rehash the
lot. Certificate Transparency solved this in 2013 with an append-only Merkle
tree, and the specification cites CT throughout, so adopting its structure was
overdue rather than novel.

`bench_merkle.py` measures what the tree buys.

### Checking one record

| Log size | Chain replay | Inclusion proof | Speedup | Proof size | Bytes fetched (chain) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 8 µs | 1.87 µs | 4× | 128 B | 12 kB |
| 1,000 | 672 µs | 4.20 µs | 160× | 320 B | 1.2 MB |
| 10,000 | 6,903 µs | 5.67 µs | 1,217× | 448 B | 12.3 MB |
| 100,000 | 69,941 µs | 7.01 µs | **9,972×** | 544 B | **122.7 MB** |

Verifying an inclusion proof at 100,000 records costs 7 µs and 1.8 kB of
transfer. Replaying the chain to learn the same fact costs 70 ms and 123 MB —
about **69,000× more data** — and that ratio keeps growing, because one cost is
linear and the other is logarithmic.

For a year of a 1,000-agent fleet (36.5 million records, tree depth 26),
checking a single sampled action costs 2 kB against 44.8 GB. Replaying a chain
costs the same whether you wanted to check one record or a million; proofs cost
what you actually asked for.

### What it costs the agent

| Log size | Chain append | Tree append + root | Added | As a share of one signature |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 0.712 µs | 2.793 µs | 2.08 µs | 2.4% |
| 10,000 | 0.680 µs | 3.202 µs | 2.52 µs | 3.0% |
| 100,000 | 0.715 µs | 3.957 µs | 3.24 µs | 3.8% |

The tree costs 2–3 microseconds per action against the 85 microseconds a
signature already costs. A structure that helps the auditor at the agent's
expense would be a bad trade; this one is close to free.

### The defect this experiment found

Building the consistency proofs surfaced a real bug in this implementation's
verifier, now scenario **A9** in the attack harness.

Every other attack assumes the adversary cannot sign. But the operator running
the enclave *can* — that is what operator-controlled infrastructure means. Given
the key, an operator can alter a record in the middle of the log, recompute
every subsequent chain link, and re-sign the whole history. The result has
exactly the right length, every signature verifies, and every link matches.
Replaying it finds nothing, because there is nothing internally wrong with it.

The only thing that contradicts a rewritten history is a root published *before*
the rewrite. Our verifier compared the anchor's **step count** and never its
**root**, so it accepted the forgery. Comparing the anchored root catches it:

```
without: replaying the rewritten history finds nothing wrong
         (verifier says: chain verified: 8 records)
with:    history rewritten: the chain presented at step 8 has head
         058366468ce1, but accf0a8d3043 was anchored
```

This became requirement **C7.3.5**, whose wording — "compares the recomputed
root against the anchored value rather than only against a step count" — exists
because we made exactly that mistake.

## On real Intel TDX hardware

Everything above models the enclave in-process. [`tdx/run_on_gcp.sh`](tdx/run_on_gcp.sh)
runs the same pipeline inside a real Intel TDX trust domain on GCP, with an identical
non-confidential instance as the control so trust-domain cost is isolated rather than
confounded with a change of CPU.

```bash
./impl/tdx/run_on_gcp.sh [PROJECT] [ZONE]   # creates two VMs, deletes them on exit
```

**The key binding works.** A quote proves a measured environment exists; it says nothing about
which signing key belongs to it. We put the digest of the evidence public key into TDX
`REPORTDATA`, so the hardware signature covers the measurement *and* the key. Measured: an
8,000-byte DCAP quote, real MRTD `c1ee9c16e3af...`, commits to our key and rejects one we did
not attest. That is requirement **C7.2.4**.

**The cost is not where we expected it.**

| | Measured | Relative |
| --- | ---: | ---: |
| Software pipeline, TDX off (control) | 152.88 us | - |
| Software pipeline, inside the TD | 162.33 us | +6.2% |
| **Trust-domain overhead** | **9.45 us** | **6.2%** |
| **One hardware quote** | **39.5 ms** | **4,180x the overhead** |

Running *inside* a trust domain is nearly free. Producing a *quote* costs 39.5 ms, which is
2.6x the entire 15 ms per-action budget on its own. Per-action attestation is not expensive, it
is impossible; every deployment amortizes:

| Quote every | Cost per step |
| ---: | ---: |
| 1 action | 39,666 us |
| 10 actions | 4,113 us |
| 100 actions | 557 us |
| 1,000 actions | 202 us |

**Which creates an exposure window.** Actions after a quote rest on a measurement taken before
them; if the measured code changed in between, their evidence attests an environment that is no
longer the one that ran. Same shape as the anchoring interval, and now requirement **C7.2.3**:
declare a maximum attestation refresh interval, refresh within it, or stop.

**What it does not show.** The protocol runs on real hardware and the binding holds. It does not
demonstrate resistance to a hostile host - we did not compromise a hypervisor, and Google runs
the one underneath. Nor does it make the evidence trust-free: to believe a measurement, a
verifier still accepts Intel, Intel's certification service, the quoting enclave, Google, and
whoever publishes reference values. Anchoring makes the *history* auditable; it does not
establish the *measurement*.

## Two defects this round's review found

Both were live in the implementation, both are fixed, and both are now regression-tested.

**A10: the binding check failed open.** `RelyingParty` performed check (iv) of Theorem 1 by
calling a *snapshot probe* — a callback that recomputes the digest of the full evaluated
snapshot — and returned "match" when no probe was configured. But the snapshot commits to the
path summary and step index, which are enclave state no independent endpoint can see, so a probe <!--aais-allow-->
requires a callback into the enclave and essentially nobody could supply one. The result: an
endpoint with `enforce=True` that checked signature, measurement, resource and nonce would still
execute a substituted action, and report success.

A security check whose default is *accept when unconfigured* is worse than no check, because it
reports that it worked. The fix gives the relying party something it can recompute unaided — the
capability now carries `action_digest`, a digest of the action alone — and refuses outright when
it has neither that nor a probe.

**A11: the capability and the evidence record were not cross-bound.** They were two
independently signed objects that happened to agree on a snapshot digest. Nothing tied one ticket
to one record, so an auditor reconciling executed actions against evidence could be shown a valid
ticket beside a record it was never issued with, and the arithmetic would balance. The capability
now commits to `step_index` and `evidence_digest`, and `Verifier.verify_capability_binding()`
checks the pair.

## Schema conformance

The claim set now has a machine-readable definition, a canonical form, and
published test vectors in [`../schema`](../schema): CDDL for the CWT/CBOR
rendering, JSON Schema for the JWT rendering, and a validator that checks
structure, canonicalization, and the semantic rules a schema cannot express.

`tests/test_core.py` runs the evidence this implementation emits through that
validator, so the schema and the implementation cannot drift apart silently.

The two renderings round-trip to identical claim sets, and CBOR is **48%
smaller** — digests and signatures travel as bytes instead of as hex text. That
matters more than it sounds: switching encoding saves more storage than
post-quantum signatures cost.

## Attack harness

Each scenario runs with and without the relevant requirement.

| # | Attack | Without the requirement | With it |
| --- | --- | --- | --- |
| A1 | Snapshot substitution | Succeeds: evidence attests a benign action while a malicious one executes | Refused: action does not match evidenced snapshot |
| A2 | Log alteration | Succeeds against unsigned operator logs | Detected: invalid signature at record 2 |
| A3 | Omission of a step | Succeeds: dropped step is indistinguishable from one that never happened | Detected: sequence gap at step 3 |
| A4 | Head truncation | Succeeds: truncated prefix is internally consistent | Detected: anchor covers 8 steps, 5 presented |
| A5 | Split-view / equivocation | Succeeds: each verifier's chain is internally consistent | Detected: divergent roots at index 3 |
| A6 | Path-composition escalation | Succeeds: read and egress each within grant | Blocked: egress after confidential read |
| A7 | Capability replay | Succeeds without single-use semantics | Refused: nonce replay |
| A8 | Evidence-pipeline failure | Succeeds: system keeps acting while logging is down | Refused: FAIL_CLOSED, failure recorded |
| A9 | Mid-history rewrite by a key-holding operator | Succeeds: the rewritten history replays perfectly, because the operator recomputed every link | Detected: presented head does not match the anchored root |
| A10 | Substitution past an unconfigured mediation check | Succeeds: endpoint verifies signature, measurement, resource and nonce, then executes a different request | Refused: capability carries an action digest the endpoint recomputes unaided; refuses when it cannot |
| A11 | Capability paired with the wrong evidence record | Succeeds: both objects verify independently, so reconciliation balances | Detected: capability commits to its record's step index and digest  <!--aais-allow--> |

A1 is the empirical form of Proposition 1 in the paper: without a check binding
the executed request to the evidenced snapshot, the adversary wins with
probability 1 — here, on the first attempt.

## Layout

```
impl/
├── poc/core.py            the pipeline: snapshot, policy, chain, evidence,
│                          gateway, relying party, anchor, gossip, verifier
├── attacks/run_attacks.py 8 attack scenarios, with/without each requirement
├── bench/bench.py         B1 latency · B2 scaling · B3 verification · B4 utility
├── bench/bench_pq.py      post-quantum signature comparison (size and cost)
├── bench/bench_frontier.py the declassification frontier (verified vs not)
├── bench/bench_ops.py     deep scaling · anchoring Δ · batching · retention
├── bench/bench_merkle.py  inclusion proofs · consistency proofs · hot-path cost
├── poc/merkle.py          RFC 6962 append-only tree: inclusion and consistency
├── tests/test_core.py     22 correctness tests mapped to requirement IDs
└── results/               attacks.json, bench.json (regenerated by the scripts)
```

## Limitations

1. **No hardware TEE**, as described above; enclave transition cost is unmeasured.
2. **Single-process**, so network and IPC costs between gateway, enclave, and
   relying party are excluded.
3. **Synthetic workloads.** The utility measurement uses a randomized workflow
   model, not traces from a production agent; the qualitative result
   (label creep, fixed by declassification) is robust, the specific 42.2% is
   workload-dependent.
4. **Python**, so absolute latencies are conservative; a Rust/WASM policy engine
   would be faster, and the relative component breakdown is the result that holds.
5. **Pure-Python ML-DSA**, so post-quantum *timings* are unrepresentative; the size results are not affected.
6. **No ZK path.** The privacy-preserving evidence options of C2.3 are specified
   but not implemented here.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
