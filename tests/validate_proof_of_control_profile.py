#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the Proof-of-Control snapshot, RFC 0002, and its crosswalk.

1. The vendored LFDT Proof-of-Control snapshot is byte-identical to its
   upstream manifest, with no files added or removed.
2. The crosswalk matches scripts/build_poc_crosswalk.py and covers exactly the
   snapshot's requirements.
3. Every LE requirement in RFC 0002 appears in the crosswalk with the same
   level and extended requirements, and vice versa.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "external" / "lfdt-proof-of-control"
RFC = ROOT / "rfcs" / "0002-proof-of-control-legal-entity-agent-profile.md"
CROSSWALK = ROOT / "conformance" / "proof-of-control" / "crosswalk-poc-v0.1.json"
LE_ROW = re.compile(r"^\| \*\*(LE\d\.\d)\*\* \| .+ \| (\d) \| ([\d., ]+) \|$")


def check_snapshot(errors: list[str]) -> None:
    for manifest_path in sorted(SNAPSHOT.glob("UPSTREAM-*.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        version = manifest["version_label"]
        base = SNAPSHOT / version
        if manifest.get("modified") is not False:
            errors.append(f"{manifest_path.name}: snapshot must be declared unmodified")
        expected = manifest["files"]
        actual = {
            path.relative_to(base).as_posix()
            for path in base.rglob("*")
            if path.is_file()
        }
        for extra in sorted(actual - set(expected)):
            errors.append(f"{version}: file not in upstream manifest: {extra}")
        for missing in sorted(set(expected) - actual):
            errors.append(f"{version}: upstream file missing: {missing}")
        for path in sorted(actual & set(expected)):
            digest = "sha256:" + hashlib.sha256((base / path).read_bytes()).hexdigest()
            if digest != expected[path]:
                errors.append(f"{version}: modified upstream file: {path}")


def check_crosswalk(errors: list[str]) -> dict:
    spec = importlib.util.spec_from_file_location(
        "build_poc_crosswalk", ROOT / "scripts" / "build_poc_crosswalk.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    built = module.build()
    committed = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    if committed != built:
        errors.append("crosswalk is stale: run python3 scripts/build_poc_crosswalk.py")
    checklist = json.loads(module.CHECKLIST.read_text(encoding="utf-8"))
    poc_ids = [item["id"] for item in checklist]
    crosswalk_ids = [item["poc_id"] for item in committed["requirements"]]
    if crosswalk_ids != poc_ids:
        errors.append("crosswalk must list every PoC requirement exactly once, in order")
    statuses = set(committed["status_values"]["m5_implementation"])
    for item in committed["requirements"]:
        if item["m5_implementation"]["status"] not in statuses:
            errors.append(f"{item['poc_id']}: invalid M5 status")
        if item["m5_implementation"]["status"] != "NOT_ASSESSED" and not item["m5_implementation"]["note"]:
            errors.append(f"{item['poc_id']}: assessed status needs a note")
    return committed


def check_rfc(errors: list[str], crosswalk: dict) -> None:
    rows = {}
    for line in RFC.read_text(encoding="utf-8").splitlines():
        match = LE_ROW.match(line)
        if match:
            le_id, level, extends = match.groups()
            rows[le_id] = (int(level), [item.strip() for item in extends.split(",")])
    listed = {item["id"]: (item["level"], item["extends"]) for item in crosswalk["le_requirements"]}
    if rows != listed:
        for le_id in sorted(set(rows) | set(listed)):
            if rows.get(le_id) != listed.get(le_id):
                errors.append(f"{le_id}: RFC table {rows.get(le_id)} != crosswalk {listed.get(le_id)}")
    count = re.search(r"adds \*\*(\d+) requirements\*\*", RFC.read_text(encoding="utf-8"))
    if not count or int(count.group(1)) != len(listed):
        errors.append("RFC summary must state the number of LE requirements")


def main() -> int:
    errors: list[str] = []
    check_snapshot(errors)
    crosswalk = check_crosswalk(errors)
    check_rfc(errors, crosswalk)
    if errors:
        print("Proof-of-Control profile validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"Proof-of-Control profile validation passed: snapshot unmodified, "
        f"{len(crosswalk['requirements'])} PoC requirements mapped, "
        f"{len(crosswalk['le_requirements'])} LE requirements consistent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
