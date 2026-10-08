# M5-MATH-001 public reference — implementation-specific

This folder holds an **unmodified** copy of the public parts of M5-MATH-001, *Provable,
Deterministic, Public Math*, from the M5 implementation. It lets anyone read the exact rules and
recompute M5 evidence (canonical hashes, value receipts, and Nash scores) without trusting M5.

> **Implementation-specific.** This is M5 material, published under the M5Ecosystem Approval
> Boundary. It is not a TitleChain Foundation standard, and including it does not advance any
> standard's status under `GOVERNANCE.md`.

| | |
| --- | --- |
| Snapshot | [`0.1.0/`](0.1.0/docs/standards/M5-MATH-001.md) — M5-MATH-001 v0.1.0, Draft for review |
| Upstream commit | `9c1bc47085ba4405912c15703a75439d860a1fa9` (M5Ecosystem, private) |
| File manifest | [`UPSTREAM-0.1.0.json`](UPSTREAM-0.1.0.json) — SHA-256 and license of every file |
| Copyright | © 2026 M5Capital Holdings, Inc. |
| Licenses | Mixed; see below and [`NASH-NOTICE.md`](NASH-NOTICE.md) |

## What is included

| Files | What they do | License |
| --- | --- | --- |
| `core/m5_canonical.py`, `packages/m5-math/canonical.js`, `vectors/canonical-hash.vectors.json` | MATH-CANONICAL-HASH: canonical JSON and SHA-256, in Python and JavaScript, held to the same vectors | Apache-2.0 |
| `packages/m5-math/receipt-verify.js` | Recomputes an M5 Value Receipt's split hash and verifies that its amounts add up, the CCF-5 floor, and agency payouts | Apache-2.0 |
| `schemas/transactions/m5-value-receipt.schema.json` | M5 Value Receipt schema v1.4.0 | Apache-2.0 |
| `docs/standards/M5-MATH-001.md` | The written rules | Apache-2.0, except section 5 (Nash M5Score), All Rights Reserved |
| `core/nash_score.py`, `packages/m5-math/nash-score.js`, `nash-weights.json`, `vectors/nash-score.vectors.json` | Nash M5Score method, weights, and vectors (status PROPOSED, no economic consequences) | **All Rights Reserved, including patent rights.** Readable and recomputable; no license to implement. |

## What is not included

Files that hold private commercial wallet-split shares stay in M5Ecosystem: the full
machine-readable math manifest, the sample receipts, and the tests that depend on them. They are
listed under `excluded` in the upstream manifest. Links to them from `M5-MATH-001.md` do not
resolve here. The CCF-5 Community Commons floor itself (5% of collected M5 fee revenue, rounded
up to the micro) is public and appears in the receipt schema and verifier.

## Verify it yourself

```bash
python3 tests/validate_m5_math_reference.py
```

The test confirms every file is byte-identical to the upstream manifest. It then recomputes
every canonical-hash and Nash vector in Python and, when Node.js 18 or later is installed, in
JavaScript. Continuous integration runs both.

## How TitleChain Foundation uses it

- **The snapshot is never edited here.** Corrections go to M5Ecosystem and arrive as a new
  pinned version, run with
  `python3 scripts/sync_m5_math_reference.py --source <clone> --commit <sha>`.
- **Commons standards stay implementation-neutral.** TitleChain standards may cite these rules
  as one implementation's published method, for example for Proof-of-Control evidence that
  carries computed values (RFC 0002, LE5). They do not require M5.
