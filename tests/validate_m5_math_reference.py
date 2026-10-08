#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the vendored M5-MATH-001 public reference.

1. The snapshot is byte-identical to its upstream manifest, with no files
   added or removed, and no excluded (private) file is present.
2. Every file carries a license designation. The Nash files are designated
   under the Cyrus license, each with a Cyrus Commons Register entry whose
   hash matches the file.
3. Nash weights are PROPOSED with no economic consequences.
4. The Python reference reproduces every canonical-hash and Nash vector.
5. If Node.js 18+ is available, the JavaScript twin reproduces the same
   vectors byte for byte (required in CI).
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "external" / "m5-math"
CYRUS = "LicenseRef-CYRUS-PCCL-1.0"
REGISTER = {
    row["repository_path"]: row["hash"]
    for row in csv.DictReader(
        (ROOT / "LICENSES" / "CYRUS-COMMONS-REGISTER.csv").read_text(encoding="utf-8").splitlines()
    )
    if row["license"] == CYRUS
}
NASH_FILES = {
    "core/nash_score.py",
    "packages/m5-math/nash-score.js",
    "packages/m5-math/nash-weights.json",
    "packages/m5-math/vectors/nash-score.vectors.json",
}

NODE_CHECK = r"""
import { readFileSync } from "fs";
import { join } from "path";
import { pathToFileURL } from "url";
const base = process.argv[1];
const pkg = join(base, "packages", "m5-math");
const load = (name) => import(pathToFileURL(join(pkg, name)).href);
const { canonicalJson, canonicalSha256 } = await load("canonical.js");
const { computeM5Score, decayWeight, loadWeights } = await load("nash-score.js");
const vectors = (name) => JSON.parse(readFileSync(join(pkg, "vectors", name), "utf-8"));
const errors = [];
for (const c of vectors("canonical-hash.vectors.json").cases) {
  if (canonicalJson(c.value) !== c.canonical_json) errors.push(`canonical json: ${c.name}`);
  if (canonicalSha256(c.value) !== c.sha256) errors.push(`canonical sha256: ${c.name}`);
}
const nash = vectors("nash-score.vectors.json");
for (const v of nash.decay) {
  const factor = loadWeights().decay.daily_factor_q32[String(v.half_life_days)];
  if (decayWeight(v.age_days, factor) !== BigInt(v.weight_q32)) errors.push(`decay ${v.half_life_days}d @ ${v.age_days}`);
}
for (const c of nash.cases) {
  const record = computeM5Score({
    subject: "wallet:sample-seller",
    signals: c.signals,
    asOf: c.as_of,
    previousRecordHash: c.previous_record_hash,
  });
  if (record.m5score !== c.expected.m5score) errors.push(`m5score: ${c.name}`);
  if (record.record_hash !== c.expected.record_hash) errors.push(`record_hash: ${c.name}`);
}
console.log(JSON.stringify(errors));
"""


def check_snapshot(errors: list[str]) -> list[Path]:
    bases = []
    for manifest_path in sorted(SNAPSHOT.glob("UPSTREAM-*.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        version = manifest["version_label"]
        base = SNAPSHOT / version
        bases.append(base)
        if manifest.get("modified") is not False:
            errors.append(f"{manifest_path.name}: snapshot must be declared unmodified")
        expected = manifest["files"]
        actual = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
        for extra in sorted(actual - set(expected)):
            errors.append(f"{version}: file not in upstream manifest: {extra}")
        for missing in sorted(set(expected) - actual):
            errors.append(f"{version}: upstream file missing: {missing}")
        for path in sorted(actual & set(expected)):
            digest = "sha256:" + hashlib.sha256((base / path).read_bytes()).hexdigest()
            if digest != expected[path]["sha256"]:
                errors.append(f"{version}: modified upstream file: {path}")
            license_id = expected[path].get("license", "")
            if not license_id:
                errors.append(f"{version}: no license designation: {path}")
            if path in NASH_FILES:
                if license_id != CYRUS:
                    errors.append(f"{version}: Nash file must be designated {CYRUS}: {path}")
                repo_path = (base / path).relative_to(ROOT).as_posix()
                if REGISTER.get(repo_path) != digest:
                    errors.append(f"{version}: no matching Cyrus Commons Register entry: {repo_path}")
        for excluded in manifest.get("excluded", {}):
            if (base / excluded).exists() or excluded in expected:
                errors.append(f"{version}: excluded private file is present: {excluded}")
    if not bases:
        errors.append("no UPSTREAM-*.json manifest found")
    return bases


def check_python(base: Path, errors: list[str]) -> None:
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(base))
    try:
        from core.m5_canonical import canonical_json, canonical_sha256
        from core.nash_score import NashSignal, compute_m5score, decay_weight, load_weights
    finally:
        sys.path.pop(0)

    vectors = base / "packages" / "m5-math" / "vectors"
    canonical = json.loads((vectors / "canonical-hash.vectors.json").read_text(encoding="utf-8"))
    for case in canonical["cases"]:
        if canonical_json(case["value"]) != case["canonical_json"]:
            errors.append(f"python canonical json: {case['name']}")
        if canonical_sha256(case["value"]) != case["sha256"]:
            errors.append(f"python canonical sha256: {case['name']}")
    for value in (2**53, -(2**53), float("nan"), float("inf")):
        try:
            canonical_json(value)
            errors.append(f"python canonical json accepted unportable value {value!r}")
        except ValueError:
            pass

    weights = load_weights()
    if weights.get("status") != "PROPOSED" or weights.get("economic_consequences_enabled") is not False:
        errors.append("nash-weights.json must be PROPOSED with economic_consequences_enabled false")

    def at(text: str) -> datetime:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))

    nash = json.loads((vectors / "nash-score.vectors.json").read_text(encoding="utf-8"))
    for item in nash["decay"]:
        factor = weights["decay"]["daily_factor_q32"][str(item["half_life_days"])]
        if decay_weight(item["age_days"], factor) != item["weight_q32"]:
            errors.append(f"python decay {item['half_life_days']}d @ {item['age_days']}")
    for case in nash["cases"]:
        signals = [
            NashSignal(s["subject"], s["component"], s["polarity"], at(s["at"]), s["source_ref"])
            for s in case["signals"]
        ]
        record = compute_m5score(
            subject="wallet:sample-seller",
            signals=signals,
            as_of=at(case["as_of"]),
            previous_record_hash=case["previous_record_hash"],
        )
        if record["m5score"] != case["expected"]["m5score"]:
            errors.append(f"python m5score: {case['name']}")
        if record["record_hash"] != case["expected"]["record_hash"]:
            errors.append(f"python record_hash: {case['name']}")


def check_node(base: Path, errors: list[str]) -> bool:
    node = shutil.which("node")
    if not node:
        if os.environ.get("CI"):
            errors.append("node is required in CI to verify the JavaScript twin")
        return False
    result = subprocess.run(
        [node, "--input-type=module", "-e", NODE_CHECK, str(base)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        errors.append(f"node verification failed: {result.stderr.strip()}")
        return True
    errors.extend(f"javascript {item}" for item in json.loads(result.stdout.strip().splitlines()[-1]))
    return True


def main() -> int:
    errors: list[str] = []
    bases = check_snapshot(errors)
    ran_node = False
    for base in bases:
        check_python(base, errors)
        ran_node = check_node(base, errors) or ran_node
    if errors:
        print("M5-MATH-001 reference validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    suffix = "Python and JavaScript" if ran_node else "Python (Node.js not found; JavaScript skipped)"
    print(f"M5-MATH-001 reference validation passed ({suffix}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
