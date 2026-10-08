#!/usr/bin/env python3
"""Compute external-framework coverage of Proof-of-Control from the coding sheet.

Coverage per framework = (EM + PM) / total PoC requirements x 100
(see mappings/rubric.md for the EM/PM/NM definitions).

Usage::

    python3 mappings/compute_coverage.py
    python3 mappings/compute_coverage.py --markdown       # print the README table
    python3 mappings/compute_coverage.py --inject         # write it into both READMEs
    python3 mappings/compute_coverage.py --svg            # regenerate the coverage chart
    python3 mappings/compute_coverage.py --sheet mappings/coding_sheet.csv

The script also validates the sheet against checklist/poc-checklist.json:
every requirement must be coded exactly once per framework.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DISPLAY_NAMES = {
    "EU_AI_Act": "EU AI Act",
    "NIST_AI_RMF": "NIST AI RMF",
    "ISO_42001": "ISO/IEC 42001",
    "SOC_2": "SOC 2",
    "OWASP_AISVS": "OWASP AISVS",
    "MITRE_ATLAS": "MITRE ATLAS",
    "CSA_AARM": "CSA AARM",
    "NIST_SP_800_207": "Zero Trust (NIST SP 800-207)",
}

CROSSWALKS = {
    "EU_AI_Act": "eu-ai-act.md",
    "NIST_AI_RMF": "nist-ai-rmf.md",
    "ISO_42001": "iso-iec-42001.md",
    "SOC_2": "soc-2.md",
    "OWASP_AISVS": "owasp.md",
    "MITRE_ATLAS": "mitre-atlas.md",
    "CSA_AARM": "csa-aarm.md",
    "NIST_SP_800_207": "zero-trust.md",
}

def _diagram_kit():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from generate_diagrams import SVG, THEMES
    return SVG, THEMES


def load(sheet_path: Path):
    with open(sheet_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    req_ids = {r["id"] for r in json.loads(
        (ROOT / "checklist" / "poc-checklist.json").read_text(encoding="utf-8"))}
    errors = []
    seen = defaultdict(set)
    for row in rows:
        rid, fw, mt = row["poc_requirement_id"], row["source_framework"], row["match_type"]
        if rid not in req_ids:
            errors.append(f"unknown requirement id {rid} ({fw})")
        if mt not in {"EM", "PM", "NM"}:
            errors.append(f"invalid match_type {mt!r} for {rid} x {fw}")
        if rid in seen[fw]:
            errors.append(f"duplicate coding for {rid} x {fw}")
        seen[fw].add(rid)
    for fw, ids in seen.items():
        missing = req_ids - ids
        if missing:
            errors.append(f"{fw}: {len(missing)} requirements uncoded "
                          f"(e.g., {sorted(missing)[:3]})")
    if errors:
        print("Coding-sheet validation FAILED:", file=sys.stderr)
        for e in errors[:20]:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    return rows, len(req_ids)


def coverage(rows, total):
    counts = defaultdict(lambda: defaultdict(int))
    for row in rows:
        counts[row["source_framework"]][row["match_type"]] += 1
    result = {}
    for fw, c in counts.items():
        result[fw] = {
            "EM": c["EM"], "PM": c["PM"], "NM": c["NM"],
            "coverage": round(100 * (c["EM"] + c["PM"]) / total),
        }
    return dict(sorted(result.items(), key=lambda kv: -kv[1]["coverage"]))


def print_table(cov, total):
    print(f"Coverage of {total} Proof-of-Control requirements "
          f"(EM+PM)/total; see mappings/rubric.md\n")
    print(f"{'Framework':<30} {'EM':>4} {'PM':>4} {'NM':>4} {'Coverage':>9}")
    for fw, c in cov.items():
        print(f"{DISPLAY_NAMES.get(fw, fw):<30} {c['EM']:>4} {c['PM']:>4} "
              f"{c['NM']:>4} {c['coverage']:>8}%")


BEGIN = "<!-- BEGIN GENERATED COVERAGE -->"
END = "<!-- END GENERATED COVERAGE -->"


def markdown_table(cov, total, prefix=""):
    """The coverage table, generated. Hand-maintained copies of this drift:
    the previous one had stale counts, a divisor of 111, and every crosswalk
    link shifted one row down."""
    lines = [
        f"**Coverage = (EM + PM) / {total} requirements.** Only exact and partial "
        f"matches count; the NM column is the gap only Proof-of-Control fills.",
        "",
        "| Framework | Exact (EM) | Partial (PM) | None (NM) | Coverage |",
        "| --- | :---: | :---: | :---: | :---: |",
    ]
    for fw, c in cov.items():
        name = DISPLAY_NAMES.get(fw, fw)
        xw = CROSSWALKS.get(fw)
        cell = f"[{name}]({prefix}{xw})" if xw else name
        lines.append(f"| {cell} | {c['EM']} | {c['PM']} | {c['NM']} | "
                     f"**{c['coverage']}%** |")
    return "\n".join(lines)


def inject(cov, total):
    """Write the table into the README files between markers."""
    import re
    targets = [(ROOT / "mappings" / "README.md", ""),
               (ROOT / "README.md", "mappings/")]
    for path, prefix in targets:
        text = path.read_text(encoding="utf-8")
        if BEGIN not in text:
            print(f"  {path.name}: no marker, skipped")
            continue
        block = BEGIN + "\n\n" + markdown_table(cov, total, prefix) + "\n\n" + END
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block,
                      text, flags=re.DOTALL)
        path.write_text(text, encoding="utf-8")
        print(f"  {path.name}: coverage table injected")


def write_svg(cov, total):
    SVG, THEMES = _diagram_kit()
    for variant, theme in THEMES.items():
        n = len(cov)
        bar_h, gap, top, label_w = 34, 16, 148, 320
        h = top + n * (bar_h + gap) + 64
        track_w = 560
        em_fill = "#7a9900" if variant == "light" else "#8fae00"
        pm_fill = "#cfff04"
        s = SVG("mapping-coverage", 1040, h, theme, variant,
                eyebrow="REGULATORY COVERAGE",
                title="How much of Proof-of-Control each framework already addresses")
        # swatch legend
        lx = 34
        for fill, lab in ((em_fill, "exact match"), (pm_fill, "partial match"),
                          (theme["warm_bot"], "gap — only PoC covers it")):
            s.parts.append(
                f'<rect x="{lx}" y="92" width="14" height="14" rx="4" '
                f'fill="{fill}" stroke="{theme["card_stroke"]}"/>')
            s.text(lx + 22, 104, lab, 11.5, theme["muted"], anchor="start")
            lx += 22 + len(lab) * 6.4 + 26
        s.text(34 + 0, 124, f"coverage = (exact + partial) / {total} requirements",
               11, theme["faint"], anchor="start")
        for i, (fw, c) in enumerate(cov.items()):
            y = top + i * (bar_h + gap)
            s.text(label_w - 16, y + bar_h / 2 + 4.5, DISPLAY_NAMES.get(fw, fw),
                   12.5, theme["text"], anchor="end")
            # track with rounded ends; segments flat-joined via clip
            cid = f"clip{i}"
            s.parts.append(
                f'<clipPath id="{cid}"><rect x="{label_w}" y="{y}" '
                f'width="{track_w}" height="{bar_h}" rx="9"/></clipPath>')
            s.parts.append(
                f'<rect x="{label_w}" y="{y}" width="{track_w}" height="{bar_h}" '
                f'rx="9" fill="url(#gWarm)" stroke="{theme["warm_stroke"]}"/>')
            em_w = track_w * c["EM"] / total
            pm_w = track_w * c["PM"] / total
            if em_w:
                s.parts.append(
                    f'<rect x="{label_w}" y="{y}" width="{em_w:.1f}" '
                    f'height="{bar_h}" fill="{em_fill}" clip-path="url(#{cid})"/>')
            if pm_w:
                s.parts.append(
                    f'<rect x="{label_w + em_w:.1f}" y="{y}" width="{pm_w:.1f}" '
                    f'height="{bar_h}" fill="{pm_fill}" clip-path="url(#{cid})"/>')
            s.text(label_w + track_w + 18, y + bar_h / 2 + 5,
                   f'{c["coverage"]}%', 14, theme["text"], bold=True,
                   anchor="start")
        s.caption("the uncovered remainder — evidence gradability, the binary "
                  "threshold, trust-assumption disclosure — is the gap "
                  "Proof-of-Control exists to close", y=h - 24)
        s.save()
    print("wrote mapping-coverage-{light,dark}.svg")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", default=str(ROOT / "mappings" / "coding_sheet.csv"))
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--inject", action="store_true",
                    help="write the table into README.md and mappings/README.md")
    ap.add_argument("--svg", action="store_true")
    args = ap.parse_args()
    rows, total = load(Path(args.sheet))
    cov = coverage(rows, total)
    if args.markdown:
        print(markdown_table(cov, total))
    else:
        print_table(cov, total)
    if args.inject:
        inject(cov, total)
    if args.svg:
        write_svg(cov, total)


if __name__ == "__main__":
    main()
