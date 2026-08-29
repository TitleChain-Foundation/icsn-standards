#!/usr/bin/env python3
"""Validate the adopted M5 governance package and publishable wiki source."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = sorted((ROOT / "docs" / "governance").glob("*.md"))
WIKI = sorted((ROOT / "wiki-source").glob("*.md"))
STATUS = "> **Publication status:** Adopted Version 1.0"
DATE = "> **Effective date:** 2026-08-28"
AUTHORITY = "> **Adopted by:** TitleChain Foundation authorized governance body"
REVIEW = "> **Legal review:** Approved for publication by authorized counsel on 2026-08-28."

errors: list[str] = []

if len(DOCS) != 8:
    errors.append(f"expected 8 governance documents, found {len(DOCS)}")
if len([p for p in WIKI if not p.name.startswith("_")]) != 9:
    errors.append("expected Home plus 8 wiki policy pages")

for path in [ROOT / "docs" / "index.md", *DOCS, *[p for p in WIKI if not p.name.startswith("_")]]:
    body = path.read_text()
    for required in (STATUS, DATE, AUTHORITY, REVIEW):
        if required not in body:
            errors.append(f"{path.relative_to(ROOT)} missing: {required}")
    if re.search(r"Counsel Review Draft|not yet been adopted", body, re.I):
        errors.append(f"{path.relative_to(ROOT)} contains obsolete draft status")

wiki_names = {p.stem for p in WIKI}
for path in WIKI:
    body = path.read_text()
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
        if "://" not in target and target.split("#", 1)[0] not in wiki_names:
            errors.append(f"{path.name} has unresolved wiki link: {target}")

for path in [ROOT / "docs" / "index.md", *DOCS]:
    body = path.read_text()
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
        if "://" in target or target.startswith("#"):
            continue
        candidate = (path.parent / target.split("#", 1)[0]).resolve()
        if not candidate.exists():
            errors.append(f"{path.relative_to(ROOT)} has unresolved repository link: {target}")

combined = "\n".join(p.read_text() for p in DOCS)
for secret_pattern in (
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"\b(?:seed phrase|recovery phrase)\s*[:=]\s*\S+",
):
    if re.search(secret_pattern, combined, re.I):
        errors.append(f"possible secret matched pattern: {secret_pattern}")

if errors:
    raise SystemExit("\n".join(f"ERROR: {item}" for item in errors))
print(f"OK: validated {len(DOCS)} governance documents and {len(WIKI)} wiki files")
