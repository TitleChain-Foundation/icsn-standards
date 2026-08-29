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
RECORD_ID = "TCF-GOV-M5-2026-08-28-01"

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
    if path.name != "_Sidebar.md":
        expected_links = wiki_names - {"_Sidebar"}
        actual_links = {
            target.split("#", 1)[0]
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", body)
            if "://" not in target
        }
        missing_links = expected_links - actual_links - {path.stem}
        if missing_links:
            errors.append(
                f"{path.name} missing navigation links: {sorted(missing_links)}"
            )

source_to_wiki = {
    "01-foundation-icsn-non-custody-data-non-access-policy.md": "Foundation-and-ICSN-Non-Custody-and-Data-Non-Access-Policy.md",
    "02-m5-participation-profile.md": "M5-Participation-Profile.md",
    "03-human-first-technology-due-process.md": "Human-First-Technology-and-Due-Process.md",
    "04-m5-due-notice-credentialed-authority-policy.md": "M5-Due-Notice-and-Credentialed-Authority-Policy.md",
    "05-m5-credential-trust-issuer-registry.md": "M5-Credential-Trust-and-Issuer-Registry.md",
    "06-m4-m5-registered-service-provider-pathway.md": "M4-M5-Registered-Service-Provider-Pathway.md",
    "07-icsn-0014-universal-value-digital-asset-classification.md": "ICSN-0014-Universal-Value-and-Digital-Asset-Classification.md",
    "08-what-is-m5bank.md": "What-Is-M5Bank.md",
}
for source_name, wiki_name in source_to_wiki.items():
    source = (ROOT / "docs" / "governance" / source_name).read_text().rstrip()
    published = (ROOT / "wiki-source" / wiki_name).read_text().rstrip()
    if not published.startswith(source):
        errors.append(f"{wiki_name} has drifted from canonical source {source_name}")

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

license_matrix = (ROOT / "LICENSES" / "LICENSE-MATRIX.md").read_text()
for designation in (
    "`docs/governance/*.md` | All Rights Reserved",
    "`wiki-source/*.md` | All Rights Reserved",
):
    if designation not in license_matrix:
        errors.append(f"license matrix missing designation: {designation}")

publication_record = (
    ROOT / "docs" / "publication-records" / f"{RECORD_ID}.md"
)
if not publication_record.exists():
    errors.append(f"missing publication record: {RECORD_ID}")
elif "a4e6e95844b133780952d2543b38400bde5796c7" not in publication_record.read_text():
    errors.append("publication record does not identify the verified v1.0 commit")

if errors:
    raise SystemExit("\n".join(f"ERROR: {item}" for item in errors))
print(f"OK: validated {len(DOCS)} governance documents and {len(WIKI)} wiki files")
