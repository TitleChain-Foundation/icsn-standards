#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Vendor an unmodified, pinned snapshot of the LFDT Proof-of-Control Standard.

Copies every tracked file of LFDT-ProofOfControl/ov-poc-standard at one commit
into external/lfdt-proof-of-control/<version>/ and writes UPSTREAM.json with the
commit and the SHA-256 of every file. The snapshot is never edited here; changes
belong upstream, and TitleChain additions live in RFC 0002 and its crosswalk.

Usage:
  python3 scripts/sync_lfdt_proof_of_control.py --source /path/to/ov-poc-standard \
      --commit <sha> --version v0.1
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_REPO = "https://github.com/LFDT-ProofOfControl/ov-poc-standard"


def tracked_files(source: Path, commit: str) -> list[str]:
    output = subprocess.check_output(
        ["git", "-C", str(source), "ls-tree", "-r", "--name-only", commit], text=True
    )
    return sorted(line for line in output.splitlines() if line)


def file_bytes(source: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(source), "show", f"{commit}:{path}"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    commit = subprocess.check_output(
        ["git", "-C", str(args.source), "rev-parse", args.commit], text=True
    ).strip()
    committed_at = subprocess.check_output(
        ["git", "-C", str(args.source), "show", "-s", "--format=%cI", commit], text=True
    ).strip()
    target = ROOT / "external" / "lfdt-proof-of-control" / args.version
    if target.exists():
        shutil.rmtree(target)
    files = {}
    for path in tracked_files(args.source, commit):
        data = file_bytes(args.source, commit, path)
        destination = target / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        files[path] = "sha256:" + hashlib.sha256(data).hexdigest()
    upstream = {
        "name": "Open Verification: the Proof-of-Control Standard for Agents",
        "repository": UPSTREAM_REPO,
        "commit": commit,
        "committed_at": committed_at,
        "version_label": args.version,
        "license": "Apache-2.0",
        "copyright": "Advanced AI Society and the Proof-of-Control contributors",
        "steward": "Advanced AI Society (Proof-of-Control Lab, Linux Foundation Decentralized Trust community lab)",
        "trademark_notice": "\"Proof-of-Control Certified\" is a protected certification mark. This snapshot grants no right to use it.",
        "modified": False,
        "files": files,
    }
    (target.parent / f"UPSTREAM-{args.version}.json").write_text(
        json.dumps(upstream, indent=2) + "\n", encoding="utf-8"
    )
    print(f"vendored {len(files)} files at {commit[:12]} into {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
