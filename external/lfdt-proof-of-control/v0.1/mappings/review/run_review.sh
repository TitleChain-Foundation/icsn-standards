#!/usr/bin/env bash
# Cross-model audit of the coverage coding sheet.
#
# The requirements and the coding were produced by the same party, which is the
# weakest possible arrangement: the person deciding whether a framework already
# covers a requirement is the person who wrote the requirement. This script asks
# a DIFFERENT model, from a different vendor, to audit every row.
#
# It does not replace the two-coder study in ../rubric.md and it produces no
# kappa. What it produces is a list of specific, checkable objections, which is
# what a defensive author will not generate alone.
#
#   ./mappings/review/run_review.sh            # all frameworks, in parallel
#   ./mappings/review/run_review.sh SOC_2      # one framework
#
# Requires the `codex` CLI (or substitute any other vendor's agent CLI that
# accepts a prompt and a JSON output schema -- the point is that it is not the
# model that wrote the sheet).
#
# READ THE ACCEPTANCE RULE in ../../docs/reviews/mapping-review-2026-08.md
# BEFORE APPLYING ANYTHING. Wholesale application of the output is exactly the
# mistake this procedure exists to avoid: a fabricated clause citation is worse
# than no citation, because it survives casual review.

set -euo pipefail
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
WORK="${WORK:-$ROOT/.review-work}"
mkdir -p "$WORK"

ALL="SOC_2 EU_AI_Act ISO_42001 NIST_AI_RMF OWASP_AISVS MITRE_ATLAS CSA_AARM NIST_SP_800_207"
FRAMEWORKS="${*:-$ALL}"

command -v codex >/dev/null || { echo "codex CLI not found" >&2; exit 1; }

# one packet per framework: requirement text plus the current coding
python3 - "$WORK" $FRAMEWORKS <<'PY'
import csv, json, pathlib, sys
work = pathlib.Path(sys.argv[1]); frameworks = set(sys.argv[2:])
root = pathlib.Path(__file__).resolve().parents[0]
root = pathlib.Path.cwd().parent.parent
reqs = {r["id"]: r for r in json.loads(
    (root/"checklist"/"poc-checklist.json").read_text())}
rows = list(csv.DictReader((root/"mappings"/"coding_sheet.csv").open()))
by = {}
for r in rows:
    by.setdefault(r["source_framework"], []).append(r)
for fw in frameworks:
    out = []
    for r in by.get(fw, []):
        q = reqs[r["poc_requirement_id"]]
        out.append(
            f'{r["poc_requirement_id"]}\t{r["poc_section"]} {q["section_title"]}\tL{q["level"]}\n'
            f'  REQUIREMENT: {q["requirement"].strip()}\n'
            f'  CURRENT: {r["match_type"]} | clause={r["framework_clause"]} | {r["rationale"]}\n')
    (work/f"{fw}.txt").write_text("\n".join(out))
    print(f"  packet: {fw} ({len(out)} rows)")
PY

for FW in $FRAMEWORKS; do
  { cat review-prompt.md; echo; echo "FRAMEWORK UNDER REVIEW: $FW"; echo;
    cat "$WORK/$FW.txt"; } > "$WORK/in_$FW.txt"
  (
    codex exec --sandbox read-only --skip-git-repo-check \
      --output-schema review-schema.json --color never \
      "$(cat "$WORK/in_$FW.txt")" > "$WORK/out_$FW.json" 2> "$WORK/err_$FW.txt"
    echo "$?" > "$WORK/done_$FW.txt"
  ) &
done
wait

echo
for FW in $FRAMEWORKS; do
  printf '  %-18s exit=%s bytes=%s\n' "$FW" \
    "$(cat "$WORK/done_$FW.txt" 2>/dev/null || echo '?')" \
    "$(wc -c < "$WORK/out_$FW.json" 2>/dev/null || echo 0)"
done
echo
echo "Now consolidate and triage -- do NOT apply wholesale:"
echo "  python3 mappings/review/consolidate.py $WORK"
