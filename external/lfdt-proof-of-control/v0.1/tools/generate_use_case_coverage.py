#!/usr/bin/env python3
"""Regenerate docs/use-cases/COVERAGE.md, and the summary block in
docs/use-cases/README.md, from the `threats:` frontmatter of every use-case
submission in docs/use-cases/.

    python3 tools/generate_use_case_coverage.py            rewrite both files
    python3 tools/generate_use_case_coverage.py --check    exit 1 if either is stale

Run --check in CI so the index can never drift from the submissions.
COVERAGE.md and the block between the coverage markers in README.md are
generated artifacts: change a submission or THREATS.md and re-run this, never
edit them by hand.
"""
import re, sys, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent.parent / "docs" / "use-cases"
SKIP = {"THREATS.md", "README.md", "COVERAGE.md", "_TEMPLATE.md"}
START, END = "<!-- coverage:start -->", "<!-- coverage:end -->"


def vocabulary():
    vocab, meta, family = [], {}, None
    for line in (HERE / "THREATS.md").read_text().splitlines():
        if line.startswith("## "):
            family = line[3:].strip()
        m = re.match(r"\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            vocab.append(m.group(1))
            meta[m.group(1)] = (family, m.group(2))
    return vocab, meta


def submissions():
    used, by_case = collections.defaultdict(list), {}
    for f in sorted(HERE.glob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text()
        match = re.match(r"\A\ufeff?---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
        fm = match.group(1) if match else ""
        tags, in_threats = [], False
        for line in fm.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("threats:"):
                in_threats = True
            elif line[0].isspace() and in_threats:
                item = re.match(r"^ +-[ \t]+(.+?)\s*$", line)
                if item:
                    tags.append(item.group(1).strip().strip("'\""))
            else:
                in_threats = False
        by_case[f.stem] = tags
        for slug in tags:
            used[slug].append(f.stem)
    return used, by_case


def bar(covered, total, width=20):
    filled = round(width * covered / total) if total else 0
    return "█" * filled + "░" * (width - filled)


def render(vocab, meta, used, by_case):
    families = collections.OrderedDict()
    for slug in vocab:
        families.setdefault(meta[slug][0], []).append(slug)

    covered = [s for s in vocab if used.get(s)]
    gaps = [s for s in vocab if not used.get(s)]

    out = ["# Coverage index", "",
           f"**{len(covered)} of {len(vocab)} threats have a worked use case.** "
           f"{len(by_case)} submissions.", "",
           "Generated from the `threats:` frontmatter across this folder. Do not",
           "edit by hand: run `python3 tools/generate_use_case_coverage.py`.", "",
           "## By family", "",
           "| Family | Covered | |", "|---|---|---|"]
    for fam, slugs in families.items():
        n = sum(1 for s in slugs if used.get(s))
        out.append(f"| {fam} | {n}/{len(slugs)} | `{bar(n, len(slugs))}` |")

    if gaps:
        out += ["", "## Threats with no use case yet", "",
                "A submission covering one of these helps most.", "",
                "| Family | Threat | |", "|---|---|---|"]
        out += [f"| {meta[s][0]} | `{s}` | {meta[s][1]} |" for s in gaps]

    out += ["", "## Every threat", "", "| Family | Threat | Use cases |", "|---|---|---|"]
    for slug in vocab:
        cases = used.get(slug, [])
        out.append(f"| {meta[slug][0]} | `{slug}` | "
                   f"{', '.join(f'`{c}`' for c in cases) if cases else '—'} |")

    out += ["", "## Every use case", "", "| Use case | Threats tagged |", "|---|---|"]
    for case, tags in sorted(by_case.items()):
        out.append(f"| `{case}` | {', '.join(f'`{t}`' for t in tags) if tags else '**none tagged**'} |")

    summary = (f"{START}\n"
               f"**Coverage: {len(covered)} of {len(vocab)} threats** across "
               f"{len(by_case)} use cases. `{bar(len(covered), len(vocab), 28)}`  \n"
               f"Full index in [COVERAGE.md](COVERAGE.md).\n"
               f"{END}")
    return "\n".join(out) + "\n", summary


def readme_with(summary):
    text = (HERE / "README.md").read_text()
    if START in text and END in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), summary, text, flags=re.S)
    return text.rstrip() + "\n\n" + summary + "\n"


def main():
    vocab, meta = vocabulary()
    used, by_case = submissions()

    unknown = {t for tags in by_case.values() for t in tags} - set(vocab)
    if unknown:
        print(f"error: tags not in THREATS.md: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1

    coverage, summary = render(vocab, meta, used, by_case)
    readme = readme_with(summary)
    check = "--check" in sys.argv

    stale = []
    if (HERE / "COVERAGE.md").read_text() != coverage if (HERE / "COVERAGE.md").exists() else True:
        stale.append("COVERAGE.md")
    if (HERE / "README.md").read_text() != readme:
        stale.append("README.md")

    if check:
        if stale:
            print(f"error: {' and '.join(stale)} out of date. "
                  f"Run: python3 tools/generate_use_case_coverage.py", file=sys.stderr)
            return 1
        print(f"up to date: {len([s for s in vocab if used.get(s)])}/{len(vocab)} threats covered")
        return 0

    (HERE / "COVERAGE.md").write_text(coverage)
    (HERE / "README.md").write_text(readme)
    print(f"wrote COVERAGE.md and README.md: "
          f"{len([s for s in vocab if used.get(s)])}/{len(vocab)} threats covered, "
          f"{len(by_case)} use cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
