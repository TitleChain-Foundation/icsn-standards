#!/usr/bin/env python3
"""Inject the requirement-level mapping tables into the crosswalk pages.

Reads mappings/coding_sheet.csv and checklist/poc-checklist.json, and rewrites
the block between the GENERATED markers in each coded crosswalk page:

    <!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->
    ...
    <!-- END GENERATED MAPPING -->

Edit the coding sheet, not the generated block. Usage::

    python3 tools/generate_crosswalks.py
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = {
    "EU_AI_Act": "eu-ai-act.md",
    "NIST_AI_RMF": "nist-ai-rmf.md",
    "ISO_42001": "iso-iec-42001.md",
    "SOC_2": "soc-2.md",
    "OWASP_AISVS": "owasp.md",
    "MITRE_ATLAS": "mitre-atlas.md",
    "CSA_AARM": "csa-aarm.md",
    "NIST_SP_800_207": "zero-trust.md",
}

CHAPTER_FILES = {
    "C1": "0x10-C01-Provenance.md", "C2": "0x10-C02-Privacy.md",
    "C3": "0x10-C03-Portability.md", "C4": "0x10-C04-Authorization.md",
    "C5": "0x10-C05-Identity.md", "C6": "0x10-C06-Security.md",
    "C7": "0x10-C07-Evidence-Generation-and-Properties.md",
    "C8": "0x10-C08-Verifiability-Tiers.md",
    "C9": "0x10-C09-System-Surface-MAESTRO.md",
    "C10": "0x10-C10-Conformance-and-Disclosure.md",
}

BEGIN = "<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->"
END = "<!-- END GENERATED MAPPING -->"
BADGE = {"EM": "Exact", "PM": "Partial", "NM": "None"}


def section_sort_key(sec):
    ch, s = sec[1:].split(".")
    return (int(ch), int(s))


def main():
    reqs = json.loads((ROOT / "checklist" / "poc-checklist.json").read_text(encoding="utf-8"))
    sections = {}
    sec_reqs = defaultdict(list)
    for r in reqs:
        sections[r["section"]] = r["section_title"]
        sec_reqs[r["section"]].append(r["id"])

    rows = list(csv.DictReader(open(ROOT / "mappings" / "coding_sheet.csv", encoding="utf-8")))
    # fw -> section -> [rows]. Coding is per REQUIREMENT, not per section: a
    # section can hold a mix, and collapsing it to one row (as this generator
    # once did, by last-write-wins) let a single uncovered requirement flip a
    # whole section to "None". Sections are summarized below, not overwritten.
    by_fw = defaultdict(lambda: defaultdict(list))
    counts = defaultdict(lambda: defaultdict(int))
    for row in rows:
        by_fw[row["source_framework"]][row["poc_section"]].append(row)
        counts[row["source_framework"]][row["match_type"]] += 1

    total = len(reqs)
    for fw, page in PAGES.items():
        c = counts[fw]
        cov = round(100 * (c["EM"] + c["PM"]) / total)
        lines = [
            BEGIN,
            "",
            f"**Coverage: {cov}%** of the {total} Proof-of-Control requirements "
            f"({c['EM']} exact matches, {c['PM']} partial matches, {c['NM']} not covered), computed per "
            f"the [mapping rubric](rubric.md) from the row-level "
            f"[coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group "
            f"validation.* To change this table, edit the coding sheet and run "
            f"`python3 tools/generate_crosswalks.py`.",
            "",
            "**How to read the Match column** ([full rubric](rubric.md)): "
            "**Exact** — the framework has a clause equivalent in scope and intent. "
            "**Partial** — the framework covers the topic, but not with Proof-of-Control's "
            "operator-independent evidence (or not at the same depth). "
            "**None** — the framework has no analogous provision. Where a section "
            "holds a mix, the badge shows the strongest match present and the "
            "**Covered** column shows how many of its requirements are matched at "
            "all — so a section reading *Partial 3/5* has two requirements this "
            "framework does not reach.",
            "",
            "| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |",
            "| --- | :---: | :---: | :---: | --- | --- |",
        ]
        gaps = []
        RANK = {"EM": 2, "PM": 1, "NM": 0}
        for sec in sorted(by_fw[fw], key=section_sort_key):
            sec_rows = by_fw[fw][sec]
            ids = sec_reqs[sec]
            chapter = sec.split(".")[0]
            link = f"[{sec} {sections[sec]}](../0.1/en/{CHAPTER_FILES[chapter]})"

            best = max(sec_rows, key=lambda r: RANK[r["match_type"]])
            matched = [r for r in sec_rows if r["match_type"] != "NM"]
            unmatched = [r for r in sec_rows if r["match_type"] == "NM"]
            n_total, n_matched = len(sec_rows), len(matched)

            # every distinct clause cited anywhere in the section, not just the
            # one that happened to sort last
            clauses = []
            for r in sec_rows:
                cl = r["framework_clause"].strip()
                if cl and cl != "—" and cl not in clauses:
                    clauses.append(cl)
            clause_text = "; ".join(clauses) if clauses else "—"

            rationale = best["rationale"].rstrip()
            if unmatched and matched:
                missing = ", ".join(r["poc_requirement_id"] for r in unmatched)
                if not rationale.endswith((".", ";", "!", "?")):
                    rationale += "."
                rationale += f" Not reached: {missing}."

            if not matched:
                gaps.append((sec, sections[sec], best["rationale"], None))
            elif unmatched:
                gaps.append((sec, sections[sec],
                             unmatched[0]["rationale"],
                             [r["poc_requirement_id"] for r in unmatched]))

            lines.append(
                f"| {link} | {n_total} | {n_matched}/{n_total} | "
                f"{BADGE[best['match_type']]} | {clause_text} | {rationale} |"
            )
        lines += [
            "",
            "### Gap Analysis (what this framework does not cover)",
            "",
        ]
        if gaps:
            for sec, title, rationale, partial_ids in gaps:
                if partial_ids:
                    ids_txt = ", ".join(partial_ids)
                    lines.append(
                        f"* **{sec} {title}** — partially reached; "
                        f"no provision for {ids_txt}: {rationale}")
                else:
                    lines.append(f"* **{sec} {title}** — {rationale}")
        else:
            lines.append("* No gaps at section level.")
        lines += [
            "",
            "*Coding granularity is the individual requirement; the section rows above "
            "summarize the requirements beneath them. Where a section is coded uniformly "
            "the summary is exact, and where it is mixed the Covered column and the gap "
            "list name what is missing. Row-level detail is in the "
            "[coding sheet](coding_sheet.csv). This is seed coding by a single coder and "
            "has not yet had the second-coder pass the [rubric](rubric.md) requires.*",
            "",
            END,
        ]
        block = "\n".join(lines)

        path = ROOT / "mappings" / page
        text = path.read_text(encoding="utf-8")
        pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
        if not pattern.search(text):
            raise SystemExit(f"{page}: GENERATED markers not found")
        path.write_text(pattern.sub(lambda _: block, text), encoding="utf-8")
        print(f"{page}: injected mapping ({cov}% coverage, {len(by_fw[fw])} sections)")


if __name__ == "__main__":
    main()
