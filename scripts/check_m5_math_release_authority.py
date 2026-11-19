#!/usr/bin/env python3
"""Check release-record consistency; this is not a legal-signature verifier."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
paths = sorted((root / "external/m5-math").glob("UPSTREAM-*.json"))
errors = []
if not paths:
    errors.append("no source manifest found")
for path in paths:
    record = json.loads(path.read_text())
    reference = record.get("authorization_record")
    if record.get("release_status") != "AUTHORIZED" or not isinstance(reference, str):
        errors.append(f"{path.name}: authorized release record missing")
        continue
    target = (root / reference).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        errors.append(f"{path.name}: invalid release record path")
        continue
    authorization = json.loads(target.read_text())
    if authorization.get("source_commit") != record.get("commit") or authorization.get("scope") != record.get("files"):
        errors.append(f"{path.name}: release revision/file scope mismatch")
    if not authorization.get("record_id") or not authorization.get("basis"):
        errors.append(f"{path.name}: release decision reference missing")
if errors:
    raise SystemExit("PUBLICATION HOLD: " + "; ".join(errors))
print("Release decision, source revision and exact file/hash/license scope match; not independent legal certification.")
