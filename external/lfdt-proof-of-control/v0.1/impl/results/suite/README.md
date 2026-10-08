# The benchmark suite on real hardware

The paper's latency tables were measured on an Apple M2 Max with the enclave as
an in-process object. `impl/tdx/run_on_gcp.sh` later measured what attestation
costs — the quote, the key binding, the trust-domain overhead on one pipeline
step — but the suite behind the published tables never ran on the hardware.

This directory is that run. `impl/tdx/run_suite_on_gcp.sh` executes all five
benchmarks inside a real Intel TDX trust domain (`td/`) and again on an
identical `c3-standard-4` with TDX off (`control/`), so the trust-domain cost is
separated from the platform change rather than confounded with it.

**These files do not replace `impl/results/`.** Those are the laptop numbers the
paper cites, and overwriting them would silently restate published figures.

## What it found

| component | laptop (M2 Max) | c3 control | c3 TD | TD vs control |
| --- | ---: | ---: | ---: | ---: |
| canonicalization + digest | 3.72 µs | 6.30 µs | 6.64 µs | +5.4% |
| policy evaluation | 0.37 µs | 0.89 µs | 1.02 µs | +14.6% |
| Ed25519 signing | 84.25 µs | 36.26 µs | 37.03 µs | +2.1% |
| chain append | 0.73 µs | 1.23 µs | 1.38 µs | +12.2% |
| **end-to-end gateway step** | **201.47 µs** | **152.31 µs** | **160.05 µs** | **+5.1%** |
| throughput | 4,963/s | 6,565/s | 6,248/s | −4.8% |

**1. The caveat was wrong in direction.** The paper says the software model
leaves out the cost of crossing into a real enclave, so "the real number will be
bigger." End to end it is *smaller* — 160 µs against 201 — because a Xeon
Platinum 8481C signs Ed25519 in 36 µs where the M2 Max took 84. The trust domain
does cost extra, and that cost is real, but it is swamped by the platform
difference and the honest summary is that the laptop number was conservative
overall rather than optimistic.

**2. Trust-domain overhead corroborates the attestation experiment.** This run
puts the end-to-end penalty at **+5.1%**. `bench_tdx.py`, measuring a different
quantity by a different method on a separate pair of instances, put it at
**+6.2%** (162.33 µs vs 152.88 µs). Two independent measurements agreeing to
about a percentage point is the strongest evidence in this repository for the
claim that running inside a trust domain is nearly free.

**3. Everything that is not a timing is bit-identical.** `frontier.json` and
`merkle.json` differ in **no** value between TD and control, and in `bench.json`
only throughput moves — the 42.2% false-rejection rate, the detection rates and
every utility figure are identical across laptop, control and TD. Those results
are properties of the workload model and the data structures, not of the
machine, and re-running them on hardware neither confirms nor threatens them. It
does establish that they are hardware-independent, which the paper previously
had to assume.

**4. Signing is not the bottleneck, and it is less of one than published.**
At 37 µs of a 160 µs step, Ed25519 is 23% of the cost here against 42% on the
laptop.

## Provenance

Both hosts: `c3-standard-4`, `us-central1-a`, Ubuntu 24.04, kernel
`6.17.0-1022-gcp`, Python 3.12.3. TD reports `cpu: Intel TDX` and
`tdx_guest_detected: true`; the control reports the Xeon model string and
`false`. Instances are created and deleted by the script, including on failure.

## Two traps this run hit, both worth keeping

**A benchmark read another's output.** `bench_ops.py` reads
`results/bench_pq.json`. The first version of the runner executed `bench_ops`
before `bench_pq`, and since `bench_pq.json` ships inside the tarball,
`bench_ops` silently folded an Apple M2 Max measurement into a table labelled as
this machine's. The runner now runs `bench_pq` first, and deletes every shipped
result before starting, so a file that exists afterwards was necessarily
produced on that host.

**A failed benchmark still produced a fetched file.** On the first attempt
`bench_ops` failed on both hosts, and the fetch step retrieved `ops.json`
anyway — byte-identical to the shipped laptop copy, and indistinguishable in the
output directory from a real measurement. Deleting the shipped results before
the run closes this too: a failed benchmark now leaves nothing to fetch.

Both are the same defect the rest of this repository exists to catch: not a
crash, but a confident wrong answer that looks exactly like a right one.

## What still is not measured

No hostile host. Google operates the hypervisor under both instances, so this
shows the construction runs on hardware that claims to resist a hostile host,
not that the resistance holds. SEV-SNP and ARM CCA are unmeasured entirely.
