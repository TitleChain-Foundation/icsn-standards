"""Validate the documented Markdown shape of use-case stories.

This is a structural check, not a judgment about tier reasoning, claim truth, or
conformance. Frontmatter supports the template's scalars and indented block
lists for threats and incident sources; this is not a general YAML parser.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
USE_CASES_DIR = REPO_ROOT / "docs" / "use-cases"
EXCLUDED_FILES = {"README.md", "_TEMPLATE.md", "THREATS.md", "COVERAGE.md"}
REQUIRED_FIELDS = ("industry", "use_case", "submission_type", "claimed_tier", "threats")
REQUIRED_HEADINGS = (
    "Scenario",
    "Why not one tier down?",
    "Tier by domain",
    "Threats exercised",
    "What Proof-of-Control does not verify here",
    "Residual trust assumptions to disclose",
    "Notes / open questions",
)
DOMAINS = (
    "Provenance",
    "Privacy",
    "Portability",
    "Authorization",
    "Identity",
    "Security",
)
DISCLAIMER = (
    "Illustrative, hypothetical scenario for calibration. Not necessarily "
    "indicative of any specific organization's current state."
)
INCIDENT_DISCLAIMER = (
    "Documented incident. Facts are drawn from the sources listed in the frontmatter."
)
THREAT_SLUGS = set(
    re.findall(
        r"^\|\s*`([a-z0-9-]+)`\s*\|",
        (USE_CASES_DIR / "THREATS.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
)
# Only one unchanged v1 story is exempt, pending its retrofit to the v2 template:
# sovereign-agents.md, ported as submitted from AAI-Society/openverification#2.
# Any edit to it requires completing the v2 migration.
LEGACY_V1_STORY = "sovereign-agents.md"
LEGACY_V1_SHA256 = (
    "f1b7734c69c65f29ca20272eb4fbeb38df792649867ca3e76a4d8df8f84200e2"
)

FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$")
LIST_ITEM_RE = re.compile(r"^ +-[ \t]+(.+?)\s*$")
CLAIMED_RE = re.compile(r"^##\s+Claimed tier:\s+Tier\s+([1-4])\s*$")
H1_RE = re.compile(r"^#\s+(?!#)(.+?)\s*$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
TABLE_DELIMITER_RE = re.compile(r"^:?-+:?$")
COMMENT_RE = re.compile(r"<!--.*?(?:-->|$)", re.DOTALL)
PLACEHOLDER_RE = re.compile(
    r"<(?:sector(?:,[^>]*)?|one line(?::[^>]*)?|1-4|short title[^>]*|N(?:-1)?|title|url)>"
    r"|\bTier N(?:-1)?\b|^# The title of your use case$",
    re.IGNORECASE,
)
TEMPLATE_PROMPTS = tuple(
    " ".join(prompt.split())
    for prompt in re.findall(
        r"(?m)^\*([^*]+)\*$",
        (USE_CASES_DIR / "_TEMPLATE.md").read_text(encoding="utf-8"),
    )
)

Error = tuple[int, str]
FieldValue = str | list[str]


def is_indented_code(line: str) -> bool:
    """Return whether leading whitespace reaches Markdown's four-column indent."""

    column = 0
    for character in line:
        if character == " ":
            column += 1
        elif character == "\t":
            column += 4 - (column % 4)
        else:
            break
        if column >= 4:
            return True
    return False


def visible_lines(lines: Sequence[str]) -> list[tuple[int, str]]:
    """Return lines that Markdown renders as ordinary content."""

    text = "\n".join(lines)
    text = COMMENT_RE.sub(lambda match: "\n" * match.group().count("\n"), text)
    fence: tuple[str, int] | None = None
    visible: list[tuple[int, str]] = []

    for number, line in enumerate(text.split("\n"), start=1):
        if match := FENCE_RE.match(line):
            marker, trailing = match.groups()
            if fence is None:
                if marker[0] != "`" or "`" not in trailing:
                    fence = marker[0], len(marker)
                    continue
            elif (
                marker[0] == fence[0]
                and len(marker) >= fence[1]
                and not trailing.strip()
            ):
                fence = None
                continue
        if fence is None and not is_indented_code(line):
            visible.append((number, line))
    return visible


def normalize(text: str) -> str:
    return " ".join(text.replace("*", "").replace("_", "").replace("`", "").split())


def blockquote_content(line: str) -> str:
    """Remove one Markdown blockquote marker and its optional following space."""

    stripped = line.lstrip()
    if not stripped.startswith(">"):
        return ""
    content = stripped[1:]
    return content.removeprefix(" ")


def table_cells(line: str, columns: int = 3) -> tuple[str, ...] | None:
    if not line.lstrip().startswith("|"):
        return None
    cells = re.split(r"(?<!\\)\|", line.strip().removeprefix("|").removesuffix("|"))
    if len(cells) != columns:
        return None
    return tuple(normalize(cell) for cell in cells)


def section(
    visible: Sequence[tuple[int, str]],
    start_line: int,
    *,
    keep_blank: bool = False,
) -> list[tuple[int, str]]:
    body: list[tuple[int, str]] = []
    for number, line in visible:
        if number <= start_line:
            continue
        if line.strip().startswith("## "):
            break
        if keep_blank or line.strip():
            body.append((number, line))
    return body


def unquote(value: str, number: int, errors: list[Error]) -> str:
    value = value.strip()
    if value.startswith(("'", '"')):
        if len(value) < 2 or value[-1] != value[0]:
            errors.append((number, "unclosed quoted frontmatter value"))
        else:
            return value[1:-1]
    return value


def parse_frontmatter(
    lines: Sequence[str],
) -> tuple[list[Error], int | None, dict[str, tuple[FieldValue, int]]]:
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return [(1, "missing opening frontmatter delimiter '---'")], None, {}
    end = next(
        (i for i, line in enumerate(lines[1:], start=2) if line.strip() == "---"),
        None,
    )
    if end is None:
        return [(1, "frontmatter is missing its closing '---'")], None, {}

    errors: list[Error] = []
    fields: dict[str, tuple[FieldValue, int]] = {}
    # ponytail: template scalars and block lists; use YAML if nested values become needed.
    list_key: str | None = None
    for number, line in enumerate(lines[1 : end - 1], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if item := LIST_ITEM_RE.fullmatch(line):
            if list_key is None:
                errors.append((number, "list item must belong to threats or sources"))
            else:
                values = fields[list_key][0]
                assert isinstance(values, list)
                values.append(unquote(item.group(1), number, errors))
            continue
        match = FIELD_RE.match(line)
        if not match:
            errors.append(
                (
                    number,
                    "unsupported frontmatter syntax; use scalars or indented block lists",
                )
            )
            list_key = None
            continue
        key, value = match.group(1), unquote(match.group(2), number, errors)
        list_key = None
        if key in fields:
            errors.append((number, f"duplicate frontmatter field '{key}'"))
        else:
            if key in {"threats", "sources"}:
                fields[key] = [], number
                if match.group(2).strip():
                    errors.append((number, f"{key} must use an indented block list"))
                else:
                    list_key = key
            else:
                fields[key] = value, number

    submission_type = fields.get("submission_type", ("scenario", 1))[0]
    required: tuple[str, ...] = ("industry", "use_case", "submission_type", "threats")
    required += (
        ("observed_tier", "required_tier", "sources")
        if submission_type == "incident"
        else ("claimed_tier",)
    )
    for key in required:
        if key not in fields:
            errors.append((1, f"missing required frontmatter field '{key}'"))
        else:
            required_value, number = fields[key]
            if not required_value or (
                isinstance(required_value, str) and not required_value.strip()
            ):
                errors.append((number, f"frontmatter field '{key}' must not be blank"))
    if submission_type not in {"scenario", "incident"}:
        errors.append(
            (
                fields.get("submission_type", ("", 1))[1],
                "submission_type must be scenario or incident",
            )
        )
    incompatible = (
        ("claimed_tier",)
        if submission_type == "incident"
        else ("observed_tier", "required_tier")
    )
    for key in incompatible:
        if key in fields:
            errors.append(
                (fields[key][1], f"{key} is not used for {submission_type} submissions")
            )
    for key in ("claimed_tier", "observed_tier", "required_tier"):
        if key in fields:
            tier_value, number = fields[key]
            if not isinstance(tier_value, str) or not re.fullmatch(
                r"[1-4]", tier_value
            ):
                errors.append((number, f"{key} must be an integer from 1 to 4"))
    for key, (field_value, number) in fields.items():
        if isinstance(field_value, str) and (
            PLACEHOLDER_RE.search(field_value)
            or field_value == "One line on what the AI system does"
        ):
            errors.append(
                (number, f"frontmatter field '{key}' contains a template placeholder")
            )
    if "sources" in fields:
        values, number = fields["sources"]
        assert isinstance(values, list)
        for value in values:
            if not re.search(r"https?://[^\s<>]+", value) or PLACEHOLDER_RE.search(
                value
            ):
                errors.append(
                    (
                        number,
                        "each source must contain an HTTP(S) URL and no placeholders",
                    )
                )
    return errors, end, fields


def table_rows(
    visible: Sequence[tuple[int, str]], heading_line: int, headers: tuple[str, ...]
) -> tuple[list[Error], list[tuple[int, tuple[str, ...]]]]:
    body = section(visible, heading_line, keep_blank=True)
    header = next(
        (
            i
            for i, (_, line) in enumerate(body)
            if table_cells(line, len(headers)) == headers
        ),
        None,
    )
    if header is None:
        label = "tier-by-domain" if headers[0] == "Domain" else "threats-exercised"
        return [(heading_line, f"{label} Markdown table is missing")], []
    label = "domain" if headers[0] == "Domain" else "threat"
    header_line = body[header][0]
    if header + 1 >= len(body) or body[header + 1][0] != header_line + 1:
        return [(body[header][0], f"{label} table separator is missing")], []

    separator_line, separator_text = body[header + 1]
    separator = table_cells(separator_text, len(headers))
    valid_separator = separator is not None and all(
        TABLE_DELIMITER_RE.fullmatch(value.strip()) for value in separator
    )
    if not valid_separator:
        return [(separator_line, f"{label} table separator is invalid")], []

    rows: list[tuple[int, tuple[str, ...]]] = []
    next_line = separator_line + 1
    for number, line in body[header + 2 :]:
        if number != next_line or not line.strip():
            break
        cells = table_cells(line, len(headers))
        if cells is None:
            if line.lstrip().startswith("|"):
                return [
                    (number, f"{label} table row must have {len(headers)} cells")
                ], rows
            break
        next_line += 1
        rows.append((number, cells))
    return [], rows


def validate_table(
    visible: Sequence[tuple[int, str]], heading_line: int, *, incident: bool = False
) -> list[Error]:
    errors, rows = table_rows(visible, heading_line, ("Domain", "Tier", "Why"))
    if errors:
        return errors

    expected = {domain.casefold(): domain for domain in DOMAINS}
    seen: set[str] = set()
    order: list[str] = []
    for number, cells in rows:
        domain, tier, reason = cells
        key = domain.casefold()
        if key not in expected:
            errors.append((number, f"unexpected domain row '{domain}'"))
            continue
        name = expected[key]
        if key in seen:
            errors.append((number, f"duplicate domain row '{name}'"))
            continue
        seen.add(key)
        order.append(name)
        tier_pattern = r"[1-4](?:\s*→\s*[1-4])?" if incident else r"[1-4]"
        if not re.fullmatch(tier_pattern, tier) and tier != "not claimed":
            pair = ", an observed → required pair," if incident else ""
            errors.append(
                (
                    number,
                    f"{name} tier must be an integer from 1 to 4{pair} or 'not claimed'",
                )
            )
        if not reason:
            errors.append((number, f"{name} rationale must not be blank"))

    errors.extend(
        (heading_line, f"missing domain row '{domain}'")
        for key, domain in expected.items()
        if key not in seen
    )
    if len(order) == len(DOMAINS) and tuple(order) != DOMAINS:
        errors.append(
            (
                heading_line,
                "domain rows must follow canonical order: " + ", ".join(DOMAINS),
            )
        )
    return errors


def validate_threats(
    visible: Sequence[tuple[int, str]], heading_line: int, tags: Sequence[str]
) -> list[Error]:
    errors, rows = table_rows(
        visible, heading_line, ("Threat", "What it looks like here")
    )
    seen: set[str] = set()
    for number, cells in rows:
        slug, reason = cells
        if slug in seen:
            errors.append((number, f"duplicate threat row '{slug}'"))
        seen.add(slug)
        if slug not in THREAT_SLUGS:
            errors.append((number, f"unknown threat slug '{slug}'"))
        if not reason:
            errors.append((number, f"{slug} threat description must not be blank"))
    if seen != set(tags):
        errors.append(
            (heading_line, "Threats exercised rows must match frontmatter threats")
        )
    return errors


def validate_file(path: Path) -> list[Error]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return [(1, f"cannot read UTF-8 Markdown: {error}")]

    errors, frontmatter_end, fields = parse_frontmatter(lines)
    incident = fields.get("submission_type", ("scenario", 1))[0] == "incident"
    tags_value, tags_line = fields.get("threats", ([], 1))
    tags = tags_value if isinstance(tags_value, list) else []
    if len(tags) != len(set(tags)):
        errors.append((tags_line, "duplicate frontmatter threat slugs"))
    for tag in tags:
        if tag not in THREAT_SLUGS:
            errors.append((tags_line, f"unknown threat slug '{tag}'"))
    visible = [
        (number, line)
        for number, line in visible_lines(lines)
        if frontmatter_end is None or number > frontmatter_end
    ]
    headings: dict[str, list[int]] = {}
    claimed: list[tuple[int, int | None]] = []
    titles: list[tuple[int, str]] = []

    for number, line in visible:
        stripped = line.strip()
        if match := H1_RE.fullmatch(stripped):
            titles.append((number, normalize(match.group(1))))
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            headings.setdefault(heading, []).append(number)
            if heading.startswith("Claimed tier:"):
                match = CLAIMED_RE.fullmatch(stripped)
                claimed.append((number, int(match.group(1)) if match else None))

    if len(titles) != 1:
        errors.append((1, "expected exactly one non-placeholder H1 title"))
    elif not titles[0][1] or PLACEHOLDER_RE.search(titles[0][1]):
        errors.append((titles[0][0], "H1 title still contains a placeholder"))

    first_section = min(
        (number for occurrences in headings.values() for number in occurrences),
        default=len(lines) + 1,
    )
    quote_source = [
        blockquote_content(line) if number < first_section else ""
        for number, line in visible
    ]
    quote = " ".join(
        line.strip() for _, line in visible_lines(quote_source) if line.strip()
    )
    disclaimer = INCIDENT_DISCLAIMER if incident else DISCLAIMER
    if disclaimer not in normalize(quote):
        errors.append(
            (
                (frontmatter_end or 0) + 1,
                f"missing the {'documented-incident' if incident else 'hypothetical-scenario'} disclaimer before sections",
            )
        )

    heading_lines: dict[str, int] = {}
    for heading in REQUIRED_HEADINGS:
        occurrences = headings.get(heading, [])
        if not occurrences:
            errors.append((1, f"missing required heading '## {heading}'"))
            continue
        heading_lines[heading] = occurrences[0]
        errors.extend(
            (number, f"duplicate required heading '## {heading}'")
            for number in occurrences[1:]
        )

    if incident:
        if claimed:
            errors.append(
                (
                    claimed[0][0],
                    "incidents use Tier observed and Tier the risky domains demanded headings",
                )
            )
        for heading, key in (
            ("Tier observed", "observed_tier"),
            ("Tier the risky domains demanded", "required_tier"),
        ):
            matches = [
                (number, title)
                for title, numbers in headings.items()
                if title == heading or title.startswith(heading + ":")
                for number in numbers
            ]
            if len(matches) != 1:
                errors.append((1, f"expected one '## {heading}' heading"))
                continue
            number, title = matches[0]
            heading_lines[heading] = number
            if title != heading:
                value = title.removeprefix(heading + ":").strip()
                tier = fields.get(key, ("", 1))[0]
                if value != f"Tier {tier}" or not re.fullmatch(r"Tier [1-4]", value):
                    errors.append(
                        (number, f"{heading} heading must match frontmatter {key}")
                    )
    elif len(claimed) != 1 or claimed[0][1] is None:
        errors.append(
            (
                claimed[0][0] if claimed else 1,
                "expected one '## Claimed tier: Tier N' heading with N from 1 to 4",
            )
        )
    else:
        number, claimed_tier = claimed[0]
        heading_lines["Claimed tier"] = number
        frontmatter_tier = fields.get("claimed_tier", ("", 1))[0]
        if frontmatter_tier and str(claimed_tier) != frontmatter_tier:
            message = (
                f"heading Tier {claimed_tier} does not match frontmatter "
                f"claimed_tier {frontmatter_tier}"
            )
            errors.append((number, message))

    for heading, number in heading_lines.items():
        content = section(visible, number)
        if not content:
            errors.append((number, f"section '## {heading}' must not be blank"))
        prose = " ".join(line.strip() for _, line in content)
        if any(prompt in prose.replace("*", "") for prompt in TEMPLATE_PROMPTS):
            errors.append(
                (number, f"section '## {heading}' still contains a template prompt")
            )

    if "Tier by domain" in heading_lines:
        errors.extend(
            validate_table(visible, heading_lines["Tier by domain"], incident=incident)
        )
    if "Threats exercised" in heading_lines:
        errors.extend(
            validate_threats(visible, heading_lines["Threats exercised"], tags)
        )
    for number, line in visible:
        if match := PLACEHOLDER_RE.search(line):
            errors.append(
                (number, f"unresolved template placeholder '{match.group(0)}'")
            )
    return sorted(set(errors))


def collect_story_files(paths: Sequence[Path]) -> list[Path]:
    candidates: list[Path] = []
    for path in paths or (USE_CASES_DIR,):
        candidates.extend(path.rglob("*.md") if path.is_dir() else [path])
    return sorted(
        {
            path.resolve()
            for path in candidates
            if path.suffix.lower() == ".md" and path.name not in EXCLUDED_FILES
        }
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "paths", nargs="*", type=Path, help="story files or directories"
    )
    stories = collect_story_files(parser.parse_args(argv).paths)
    if not stories:
        print("No use-case story Markdown files found.", file=sys.stderr)
        return 2

    findings: list[tuple[Path, int, str]] = []
    legacy = 0
    for story in stories:
        if story == USE_CASES_DIR / LEGACY_V1_STORY:
            try:
                unchanged = (
                    hashlib.sha256(story.read_bytes()).hexdigest()
                    == LEGACY_V1_SHA256
                )
            except OSError:
                unchanged = False
            if unchanged:
                legacy += 1
                print(
                    f"warning: unchanged v1 {LEGACY_V1_STORY} exempt pending its v2 retrofit; not v2-validated",
                    file=sys.stderr,
                )
                continue
        findings.extend(
            (story, line, message) for line, message in validate_file(story)
        )
    if findings:
        for path, line, message in findings:
            try:
                path = path.relative_to(REPO_ROOT)
            except ValueError:
                pass
            print(f"{path}:{line}: {message}", file=sys.stderr)
        print(
            f"Found {len(findings)} structural error(s) in {len(stories)} file(s).",
            file=sys.stderr,
        )
        return 1

    count = len(stories) - legacy
    noun = "story" if count == 1 else "stories"
    print(
        f"Validated the documented v2 shape of {count} use-case {noun}; {legacy} unchanged legacy exemption(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
