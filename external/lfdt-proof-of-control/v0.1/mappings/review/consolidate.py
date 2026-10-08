#!/usr/bin/env python3
"""Consolidate the per-framework cross-model reviews into one triage table.

Usage:  python3 mappings/review/consolidate.py [work-dir]

Reads out_<FRAMEWORK>.json from the work directory written by run_review.sh.
The output is a TRIAGE LIST, not a patch. See the acceptance rule in
docs/reviews/mapping-review-2026-08.md before changing any row."""
import json, pathlib, collections, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".review-work"

FRAMEWORKS = ["SOC_2","EU_AI_Act","ISO_42001","NIST_AI_RMF","OWASP_AISVS",
              "MITRE_ATLAS","CSA_AARM","NIST_SP_800_207"]

reqs = {r["id"]: r for r in json.loads(
    (ROOT / "checklist" / "poc-checklist.json").read_text())}

all_changes, all_errors, systemic = [], [], {}
for fw in FRAMEWORKS:
    p = HERE / f"out_{fw}.json"
    if not p.exists() or not p.stat().st_size:
        print(f"!! {fw}: no output", file=sys.stderr)
        continue
    try:
        d = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        print(f"!! {fw}: unparseable ({e})", file=sys.stderr)
        continue
    for c in d.get("proposed_changes", []):
        c["framework"] = fw
        all_changes.append(c)
    for c in d.get("clause_citation_errors", []):
        c["framework"] = fw
        all_errors.append(c)
    systemic[fw] = {"assessment": d.get("overall_assessment", ""),
                    "issues": d.get("systemic_issues", [])}

# direction of each proposed change
RANK = {"NM": 0, "PM": 1, "EM": 2}
for c in all_changes:
    d = RANK[c["proposed_match"]] - RANK[c["current_match"]]
    c["direction"] = "upgrade" if d > 0 else "downgrade" if d < 0 else "same"

by_conf = collections.Counter(c["confidence"] for c in all_changes)
by_dir = collections.Counter(c["direction"] for c in all_changes)
by_fw = collections.Counter(c["framework"] for c in all_changes)

print(f"PROPOSED CHANGES: {len(all_changes)}")
print(f"  by confidence: {dict(by_conf)}")
print(f"  by direction:  {dict(by_dir)}")
print(f"  by framework:  {dict(by_fw)}")
print(f"CLAUSE CITATION ERRORS: {len(all_errors)}\n")

# requirements flagged by several frameworks at once are the strongest signal:
# if four coders independently think 3.1.1 is miscoded, the requirement text is
# probably the problem, not the coding
multi = collections.Counter(c["requirement_id"] for c in all_changes)
repeat = [(r, n) for r, n in multi.most_common() if n >= 3]
if repeat:
    print("FLAGGED BY 3+ FRAMEWORKS (look at the requirement itself):")
    for r, n in repeat:
        dirs = {c["direction"] for c in all_changes if c["requirement_id"] == r}
        print(f"  {r:8} x{n}  {'/'.join(sorted(dirs))}  "
              f"{reqs[r]['requirement'][:70] if r in reqs else 'UNKNOWN ID'}...")
    print()

print("HIGH-CONFIDENCE CHANGES:")
for c in sorted([c for c in all_changes if c["confidence"] == "high"],
                key=lambda c: (c["framework"], c["requirement_id"])):
    print(f"  [{c['framework']:16}] {c['requirement_id']:8} "
          f"{c['current_match']} -> {c['proposed_match']}  "
          f"clause={c['proposed_clause'][:44]}")
    print(f"      {c['reason'][:150]}")

(HERE / "consolidated.json").write_text(json.dumps(
    {"changes": all_changes, "citation_errors": all_errors,
     "systemic": systemic}, indent=2))
print(f"\nwritten to {HERE/'consolidated.json'}")
