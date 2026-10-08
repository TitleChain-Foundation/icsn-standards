#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Vendor the public M5-MATH-001 reference from M5Ecosystem, unmodified.

Copies an approved file list from a pinned M5Ecosystem commit into
external/m5-math/<version>/, keeping upstream paths, and writes
UPSTREAM-<version>.json with each file's SHA-256 and license.

Files that carry private commercial wallet-split shares are never copied;
they are listed under "excluded" with the reason.

Usage:
    python3 scripts/sync_m5_math_reference.py --source ~/path/to/M5Ecosystem --commit <sha>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "external" / "m5-math"
VERSION = "0.1.0"

APACHE = "Apache-2.0"
NASH = "LicenseRef-CYRUS-PCCL-1.0"
MIXED = "Apache-2.0 except section 5 (Nash M5Score), LicenseRef-CYRUS-PCCL-1.0"

FILES = {
    "core/m5_canonical.py": APACHE,
    "packages/m5-math/canonical.js": APACHE,
    "packages/m5-math/receipt-verify.js": APACHE,
    "packages/m5-math/vectors/canonical-hash.vectors.json": APACHE,
    "schemas/transactions/m5-value-receipt.schema.json": APACHE,
    "docs/standards/M5-MATH-001.md": MIXED,
    "core/nash_score.py": NASH,
    "packages/m5-math/nash-score.js": NASH,
    "packages/m5-math/nash-weights.json": NASH,
    "packages/m5-math/vectors/nash-score.vectors.json": NASH,
}

EXCLUDED = {
    "packages/m5-math/M5-MATH-MANIFEST.json": "contains private commercial wallet-split shares",
    "packages/m5-math/m5-math.test.js": "depends on sample receipts that contain private wallet-split shares",
    "packages/m5-math/package.json": "private package metadata",
    "tests/test_m5_math_manifest.py": "verifies the private manifest",
    "tests/test_nash_score.py": "private test suite; the commons test recomputes the same vectors",
}


def git(source: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(source), *args], check=True, capture_output=True
    ).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()

    commit = git(args.source, "rev-parse", args.commit).decode().strip()
    committed_at = git(args.source, "show", "-s", "--format=%cI", commit).decode().strip()

    base = DEST / VERSION
    if base.exists():
        shutil.rmtree(base)
    files = {}
    for path, license_id in FILES.items():
        data = git(args.source, "show", f"{commit}:{path}")
        target = base / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        files[path] = {
            "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
            "license": license_id,
        }

    manifest = {
        "name": "M5-MATH-001 public reference (implementation-specific)",
        "repository": "M5Ecosystem (private)",
        "commit": commit,
        "committed_at": committed_at,
        "version_label": VERSION,
        "copyright": "TitleChain Sovereign Purpose Trust (TitleChain Foundation); licensed by M5Capital Holdings LLC",
        "approval_boundary": "Implementation-specific M5 material, published under the M5Ecosystem Approval Boundary. It is not a TitleChain standard and does not advance any standard's status.",
        "nash_notice": "The Nash files are licensed under the Cyrus Purpose-Bound Constitutional Commons License 1.0, designated in LICENSES/CYRUS-COMMONS-REGISTER.csv. The Nash scoring process is covered by U.S. Patent Nos. 11,720,888 and 12,518,273 (continuation), owned by Pamela Norton and exclusively licensed to the TitleChain Sovereign Purpose Trust, and is a Designated Method under the TitleChain Patent Pledge. See NASH-NOTICE.md.",
        "modified": False,
        "files": dict(sorted(files.items())),
        "excluded": EXCLUDED,
    }
    (DEST / f"UPSTREAM-{VERSION}.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Vendored {len(files)} files from {commit[:12]} into {base.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
