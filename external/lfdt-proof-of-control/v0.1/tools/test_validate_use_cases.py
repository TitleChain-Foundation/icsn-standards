from __future__ import annotations

import hashlib
import io
import re
import runpy
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.validate_use_cases import (
    DISCLAIMER,
    DOMAINS,
    INCIDENT_DISCLAIMER,
    LEGACY_V1_SHA256,
    LEGACY_V1_STORY,
    REPO_ROOT,
    REQUIRED_FIELDS,
    USE_CASES_DIR,
    collect_story_files,
    main,
    normalize,
    table_cells,
    validate_file,
    visible_lines,
)

DISCLAIMER_BLOCK = (
    "> *Illustrative, hypothetical scenario for calibration. Not necessarily\n"
    "> indicative of any specific organization's current state.*"
)


def valid_story() -> str:
    return f"""---
industry: testing
use_case: AI agent exercising a documented action
submission_type: scenario
claimed_tier: 3
threats:
  - context-blind-authorization
review_note: extra scalar fields are allowed
---

# Structural validation fixture

{DISCLAIMER_BLOCK}

## Scenario

One actor takes one action with a concrete consequence.

## Claimed tier: Tier 3

The fixture explains its target tier.

## Why not one tier down?

The fixture names the remaining Tier 2 failure.

## Extra context

Additional sections are allowed.

## Tier by domain

| Domain | Tier | Why |
| :--- | :---: | ---: |
| Provenance | 3 | A nonblank rationale. |
| Privacy | not claimed | No privacy claim. |
| Portability | 2 | A nonblank rationale. |
| Authorization | 3 | A nonblank rationale. |
| Identity | 2 | A nonblank rationale. |
| Security | 3 | A nonblank rationale. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `context-blind-authorization` | A grant is reused for a different target. |

## What Proof-of-Control does not verify here

Whether the policy was adequate.

## Residual trust assumptions to disclose

Credential issuers and verification-toolchain soundness.

## Notes / open questions

None.
"""


def valid_incident() -> str:
    return (
        valid_story()
        .replace(
            "submission_type: scenario\nclaimed_tier: 3",
            "submission_type: incident\nobserved_tier: 1\nrequired_tier: 4\nsources:\n  - Investigator report — https://example.com/report",
        )
        .replace(DISCLAIMER_BLOCK, f"> *{INCIDENT_DISCLAIMER}*")
        .replace(
            "## Claimed tier: Tier 3\n\nThe fixture explains its target tier.",
            "## Tier observed\n\nThe sources support Tier 1.\n\n## Tier the risky domains demanded\n\nThe deployment needed Tier 4.",
        )
    )


class ValidateUseCasesTests(unittest.TestCase):
    def findings_for(self, text: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "story.md"
            path.write_text(text, encoding="utf-8")
            return [message for _, message in validate_file(path)]

    def test_repository_stories_pass(self) -> None:
        stories = collect_story_files(())
        self.assertTrue(stories)
        for story in stories:
            with self.subTest(story=story):
                if (
                    story.name == LEGACY_V1_STORY
                    and hashlib.sha256(story.read_bytes()).hexdigest()
                    == LEGACY_V1_SHA256
                ):
                    self.assertTrue(
                        validate_file(story),
                        "the strict validator must still reject the legacy story",
                    )
                else:
                    self.assertEqual(validate_file(story), [])
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            self.assertEqual(main(()), 0)

    def test_contract_matches_template(self) -> None:
        template = (USE_CASES_DIR / "_TEMPLATE.md").read_text(encoding="utf-8")
        lines = template.splitlines()
        end = lines[1:].index("---") + 2
        fields = tuple(
            match.group(1)
            for line in lines[1 : end - 1]
            if (match := re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):", line))
        )
        self.assertEqual(fields, REQUIRED_FIELDS)

        headings = tuple(
            line.strip()[3:].strip()
            for _, line in visible_lines(lines)
            if line.strip().startswith("## ")
        )
        expected = (
            "Scenario",
            "Claimed tier: Tier N",
            "Why not one tier down?",
            "Tier by domain",
            "Threats exercised",
            "What Proof-of-Control does not verify here",
            "Residual trust assumptions to disclose",
            "Notes / open questions",
        )
        self.assertEqual(headings, expected)

        rows = [
            cells[0]
            for line in lines
            if (cells := table_cells(line)) and cells[0] in DOMAINS
        ]
        self.assertEqual(tuple(rows), DOMAINS)
        quote = " ".join(line.lstrip()[1:] for line in lines if line.startswith(">"))
        self.assertIn(DISCLAIMER, normalize(quote))

    def test_allows_documented_extensions_and_formatting(self) -> None:
        self.assertEqual(self.findings_for(valid_story()), [])

    def test_ignores_markdown_syntax_in_frontmatter_comments(self) -> None:
        story = valid_story().replace(
            "industry: testing",
            "industry: testing\n# metadata note\n## Scenario",
        )
        self.assertEqual(self.findings_for(story), [])

    def test_reports_frontmatter_errors_and_tier_mismatch(self) -> None:
        cases = {
            "blank scalar": (
                valid_story().replace("industry: testing", 'industry: "   "'),
                "frontmatter field 'industry' must not be blank",
            ),
            "unclosed": (
                valid_story().replace("---\n\n# Structural", "\n# Structural", 1),
                "frontmatter is missing its closing '---'",
            ),
            "syntax": (
                valid_story().replace(
                    "review_note: extra scalar fields are allowed",
                    "review_note: [unsupported inline collection]\n  nested: value",
                ),
                "unsupported frontmatter syntax",
            ),
            "missing": (
                valid_story().replace(
                    "use_case: AI agent exercising a documented action\n", ""
                ),
                "missing required frontmatter field 'use_case'",
            ),
            "duplicate": (
                valid_story().replace(
                    "industry: testing", "industry: testing\nindustry: duplicate"
                ),
                "duplicate frontmatter field 'industry'",
            ),
            "invalid": (
                valid_story().replace("claimed_tier: 3", "claimed_tier: 5"),
                "claimed_tier must be an integer from 1 to 4",
            ),
            "mismatch": (
                valid_story().replace("claimed_tier: 3", "claimed_tier: 2"),
                "heading Tier 3 does not match frontmatter claimed_tier 2",
            ),
        }
        for name, (story, expected) in cases.items():
            with self.subTest(name=name):
                self.assertTrue(
                    any(expected in message for message in self.findings_for(story))
                )

    def test_requires_visible_disclaimer(self) -> None:
        hidden_versions = (
            f"<!--\n{DISCLAIMER_BLOCK}\n-->",
            f"```\n{DISCLAIMER_BLOCK}\n```",
            f"> ```\n{DISCLAIMER_BLOCK}\n> ````",
            DISCLAIMER_BLOCK.replace("> ", ">     "),
        )
        for replacement in hidden_versions:
            with self.subTest(replacement=replacement):
                story = valid_story().replace(
                    DISCLAIMER_BLOCK,
                    replacement,
                )
                self.assertTrue(
                    any(
                        "missing the hypothetical-scenario disclaimer" in message
                        for message in self.findings_for(story)
                    )
                )

    def test_requires_one_filled_title(self) -> None:
        missing = valid_story().replace("# Structural validation fixture\n", "")
        placeholder = valid_story().replace(
            "# Structural validation fixture", "# <Short title for the use case>"
        )
        self.assertIn(
            "expected exactly one non-placeholder H1 title",
            self.findings_for(missing),
        )
        self.assertTrue(
            any("placeholder" in message for message in self.findings_for(placeholder))
        )

    def test_hidden_headings_do_not_count(self) -> None:
        replacements = (
            "<!-- ## Scenario -->",
            "```\n## Scenario\n```",
            "    ## Scenario",
            " \t## Scenario",
        )
        for replacement in replacements:
            with self.subTest(replacement=replacement):
                story = valid_story().replace("## Scenario", replacement)
                self.assertIn(
                    "missing required heading '## Scenario'",
                    self.findings_for(story),
                )

    def test_fence_with_trailing_text_does_not_close_code(self) -> None:
        replacement = (
            "```\n"
            "```not-a-close\n"
            "## Scenario\n\n"
            "One actor takes one action with a concrete consequence.\n"
            "````"
        )
        story = valid_story().replace(
            "## Scenario\n\nOne actor takes one action with a concrete consequence.",
            replacement,
        )
        self.assertIn(
            "missing required heading '## Scenario'",
            self.findings_for(story),
        )

    def test_requires_content_in_core_sections(self) -> None:
        cases = (
            (
                "One actor takes one action with a concrete consequence.\n",
                "section '## Scenario' must not be blank",
            ),
            (
                "The fixture explains its target tier.\n",
                "section '## Claimed tier' must not be blank",
            ),
            (
                "The fixture names the remaining Tier 2 failure.\n",
                "section '## Why not one tier down?' must not be blank",
            ),
            (
                "Whether the policy was adequate.\n",
                "section '## What Proof-of-Control does not verify here' must not be blank",
            ),
            (
                "Credential issuers and verification-toolchain soundness.\n",
                "section '## Residual trust assumptions to disclose' must not be blank",
            ),
        )
        for content, expected in cases:
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.findings_for(valid_story().replace(content, "")),
                )

    def test_reports_heading_errors(self) -> None:
        missing = valid_story().replace("## Scenario", "## Context")
        duplicate = valid_story().replace(
            "## Scenario\n", "## Scenario\n\nFirst.\n\n## Scenario\n", 1
        )
        malformed = valid_story().replace(
            "## Claimed tier: Tier 3", "## Claimed tier: Level 3"
        )
        self.assertIn(
            "missing required heading '## Scenario'", self.findings_for(missing)
        )
        self.assertIn(
            "duplicate required heading '## Scenario'", self.findings_for(duplicate)
        )
        self.assertTrue(
            any(
                "'## Claimed tier: Tier N' heading" in message
                for message in self.findings_for(malformed)
            )
        )

    def test_requires_a_real_domain_table(self) -> None:
        no_header = valid_story().replace(
            "| Domain | Tier | Why |", "Domain | Tier | Why"
        )
        hidden_row = valid_story().replace(
            "| Privacy | not claimed | No privacy claim. |",
            "<!-- | Privacy | not claimed | No privacy claim. | -->",
        )
        self.assertIn(
            "tier-by-domain Markdown table is missing",
            self.findings_for(no_header),
        )
        self.assertIn("missing domain row 'Privacy'", self.findings_for(hidden_row))

    def test_enforces_gfm_domain_table_boundaries(self) -> None:
        separator = "| :--- | :---: | ---: |"
        short_separator = valid_story().replace(separator, "| : | - | :: |")
        interior_colon = valid_story().replace(separator, "| -:- | --- | --- |")
        gap_after_header = valid_story().replace(
            "| Domain | Tier | Why |\n" + separator,
            "| Domain | Tier | Why |\n\n" + separator,
        )
        gap_after_separator = valid_story().replace(
            separator + "\n| Provenance",
            separator + "\n\n| Provenance",
        )

        one_hyphen = valid_story().replace(separator, "| :- | -: | :- |")
        self.assertEqual(self.findings_for(one_hyphen), [])
        self.assertIn(
            "domain table separator is invalid",
            self.findings_for(short_separator),
        )
        self.assertIn(
            "domain table separator is invalid",
            self.findings_for(interior_colon),
        )
        self.assertIn(
            "domain table separator is invalid",
            self.findings_for(gap_after_header),
        )
        self.assertIn(
            "missing domain row 'Privacy'",
            self.findings_for(gap_after_separator),
        )

    def test_reports_domain_row_errors(self) -> None:
        story = (
            valid_story()
            .replace("| Privacy | not claimed |", "| Privacy | 5 |")
            .replace(
                "| Provenance | 3 | A nonblank rationale. |",
                "| Provenance | 3 | |",
            )
            .replace(
                "| Identity | 2 | A nonblank rationale. |",
                "| Identity | 2 | A nonblank rationale. |\n"
                "| Reliability | 2 | Unexpected. |\n"
                "| Identity | 2 | Duplicate. |",
            )
        )
        messages = self.findings_for(story)
        expected = (
            "Privacy tier must be an integer from 1 to 4 or 'not claimed'",
            "Provenance rationale must not be blank",
            "unexpected domain row 'Reliability'",
            "duplicate domain row 'Identity'",
        )
        for message in expected:
            self.assertIn(message, messages)

    def test_collects_nested_stories_and_excludes_support_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            story = nested / "story.md"
            story.write_text(valid_story(), encoding="utf-8")
            (root / "README.md").write_text("support", encoding="utf-8")
            (root / "_TEMPLATE.md").write_text("support", encoding="utf-8")
            (root / "THREATS.md").write_text("support", encoding="utf-8")
            (root / "COVERAGE.md").write_text("support", encoding="utf-8")
            self.assertEqual(collect_story_files((root,)), [story.resolve()])

    def test_cli_reports_file_line_and_nonzero_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.md"
            path.write_text("# Missing everything else\n", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main((str(path),))
            self.assertEqual(code, 1)
            self.assertRegex(stderr.getvalue(), r"bad\.md:\d+: ")

    def test_incident_keeps_observed_and_required_tiers_distinct(self) -> None:
        self.assertEqual(self.findings_for(valid_incident()), [])
        numbered = (
            valid_incident()
            .replace("## Tier observed\n", "## Tier observed: Tier 1\n")
            .replace(
                "## Tier the risky domains demanded\n",
                "## Tier the risky domains demanded: Tier 4\n",
            )
        )
        self.assertEqual(self.findings_for(numbered), [])
        self.assertTrue(
            any(
                "must match frontmatter observed_tier" in message
                for message in self.findings_for(
                    numbered.replace("Tier observed: Tier 1", "Tier observed: Tier 4")
                )
            )
        )
        # Ordinal tiers are not averaged, nor forced to equal a domain maximum.
        self.assertEqual(
            self.findings_for(
                valid_incident()
                .replace("observed_tier: 1", "observed_tier: 4")
                .replace("required_tier: 4", "required_tier: 1")
            ),
            [],
        )

    def test_incident_requires_sources_disclaimer_and_two_headings(self) -> None:
        cases = (
            (
                "sources:\n  - Investigator report — https://example.com/report\n",
                "",
                "missing required frontmatter field 'sources'",
            ),
            (
                "https://example.com/report",
                "no URL",
                "each source must contain an HTTP(S) URL",
            ),
            (
                "required_tier: 4",
                "required_tier: 5",
                "required_tier must be an integer",
            ),
            (
                INCIDENT_DISCLAIMER,
                "Illustrative scenario.",
                "documented-incident disclaimer",
            ),
            (
                "## Tier observed",
                "## Claimed tier: Tier 1",
                "incidents use Tier observed",
            ),
            (
                "## Tier the risky domains demanded",
                "## Requested tier",
                "expected one '## Tier the risky domains demanded'",
            ),
            (
                "observed_tier: 1",
                "observed_tier: 1\nclaimed_tier: 1",
                "claimed_tier is not used for incident",
            ),
        )
        for old, new, expected in cases:
            with self.subTest(expected=expected):
                self.assertTrue(
                    any(
                        expected in message
                        for message in self.findings_for(
                            valid_incident().replace(old, new)
                        )
                    )
                )

    def test_threats_are_known_unique_and_match_the_visible_table(self) -> None:
        cases = (
            (
                "| `context-blind-authorization` | A grant is reused for a different target. |",
                "| `context-blind-authorization` | A grant is reused for a different target. |\n| `context-blind-authorization` | Another description. |",
                "duplicate threat row 'context-blind-authorization'",
            ),
            (
                "  - context-blind-authorization",
                "  - invented-threat",
                "unknown threat slug 'invented-threat'",
            ),
            (
                "  - context-blind-authorization",
                "  - context-blind-authorization\n  - context-blind-authorization",
                "duplicate frontmatter threat slugs",
            ),
            (
                "`context-blind-authorization`",
                "`excessive-agency`",
                "rows must match frontmatter threats",
            ),
            (
                "A grant is reused for a different target.",
                "",
                "threat description must not be blank",
            ),
            (
                "| `context-blind-authorization` | A grant is reused for a different target. |",
                "<!-- | `context-blind-authorization` | A grant is reused for a different target. | -->",
                "rows must match frontmatter threats",
            ),
            (
                "threats:\n  - context-blind-authorization",
                "threats: [context-blind-authorization]",
                "must use an indented block list",
            ),
        )
        for old, new, expected in cases:
            with self.subTest(expected=expected):
                self.assertTrue(
                    any(
                        expected in message
                        for message in self.findings_for(
                            valid_story().replace(old, new)
                        )
                    )
                )

    def test_domain_order_and_explicit_unclaimed_domains(self) -> None:
        out_of_order = valid_story().replace(
            "| Provenance | 3 | A nonblank rationale. |\n| Privacy | not claimed | No privacy claim. |",
            "| Privacy | not claimed | No privacy claim. |\n| Provenance | 3 | A nonblank rationale. |",
        )
        self.assertTrue(
            any(
                "canonical order" in message
                for message in self.findings_for(out_of_order)
            )
        )
        self.assertIn(
            "Privacy tier must be an integer from 1 to 4 or 'not claimed'",
            self.findings_for(
                valid_story().replace("| Privacy | not claimed |", "| Privacy | |")
            ),
        )

    def test_rejects_copied_prompts_and_unclosed_quotes(self) -> None:
        prompt = "*Anything unresolved, or where reasonable people might place this differently.\nIf this use case turns on a control that was asserted but never wired into the\nexecution path, note it here: no tier closes that gap.*"
        self.assertTrue(
            any(
                "still contains a template prompt" in message
                for message in self.findings_for(valid_story().replace("None.", prompt))
            )
        )
        for old, new in (
            ("claimed_tier: 3", 'claimed_tier: "3'),
            ("  - context-blind-authorization", "  - 'context-blind-authorization"),
        ):
            with self.subTest(new=new):
                self.assertIn(
                    "unclosed quoted frontmatter value",
                    self.findings_for(valid_story().replace(old, new)),
                )
        quoted = (
            valid_story()
            .replace("claimed_tier: 3", 'claimed_tier: "3"')
            .replace(
                "  - context-blind-authorization", "  - 'context-blind-authorization'"
            )
        )
        self.assertEqual(self.findings_for(quoted), [])

    def test_checks_visible_tables_and_preserves_escaped_pipes(self) -> None:
        self.assertEqual(
            self.findings_for(
                valid_story().replace(
                    "A nonblank rationale.", r"One option \| another."
                )
            ),
            [],
        )
        self.assertTrue(
            any(
                "must have 3 cells" in message
                for message in self.findings_for(
                    valid_story().replace(
                        "| Security | 3 | A nonblank rationale. |",
                        "| Security | 3 | Split | rationale. |",
                    )
                )
            )
        )

    def test_incident_domain_pairs_are_not_scenario_claims(self) -> None:
        paired = (
            valid_incident()
            .replace("| Provenance | 3 |", "| Provenance | 1 → 3 |")
            .replace("| Authorization | 3 |", "| Authorization | 1 → 4 |")
        )
        self.assertEqual(self.findings_for(paired), [])
        self.assertTrue(
            any(
                "Authorization tier must" in message
                for message in self.findings_for(
                    valid_story().replace(
                        "| Authorization | 3 |", "| Authorization | 1 → 4 |"
                    )
                )
            )
        )
        self.assertTrue(
            any(
                "Authorization tier must" in message
                for message in self.findings_for(
                    paired.replace(
                        "| Authorization | 1 → 4 |", "| Authorization | 1 → 5 |"
                    )
                )
            )
        )

    def test_coverage_reads_the_same_threat_list_as_the_validator(self) -> None:
        namespace = runpy.run_path(
            str(REPO_ROOT / "tools" / "generate_use_case_coverage.py")
        )
        submissions = namespace["submissions"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            story = (
                valid_story()
                .replace(
                    "use_case: AI agent exercising a documented action",
                    "use_case: A task --- with a delimiter inside a scalar",
                )
                .replace(
                    "  - context-blind-authorization",
                    "  - 'context-blind-authorization'\n  # A note between tags.\n\n  - excessive-agency",
                )
                .replace(
                    "| `context-blind-authorization` | A grant is reused for a different target. |",
                    "| `context-blind-authorization` | A grant is reused for a different target. |\n| `excessive-agency` | A grant is too broad. |",
                )
            )
            (root / "story.md").write_text(story, encoding="utf-8")
            self.assertEqual(self.findings_for(story), [])
            with patch.dict(submissions.__globals__, {"HERE": root}):
                _, by_case = submissions()
            self.assertEqual(
                by_case, {"story": ["context-blind-authorization", "excessive-agency"]}
            )
        hidden = valid_story().replace("|---|---|", "|---|---|\n\n")
        self.assertTrue(
            any(
                "rows must match frontmatter threats" in message
                for message in self.findings_for(hidden)
            )
        )

    def test_legacy_exemption_is_exact_and_does_not_hide_edits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            credit = root / LEGACY_V1_STORY
            credit.write_text("# Legacy bytes\n", encoding="utf-8")
            with (
                patch("tools.validate_use_cases.USE_CASES_DIR", root),
                patch(
                    "tools.validate_use_cases.LEGACY_V1_SHA256",
                    hashlib.sha256(credit.read_bytes()).hexdigest(),
                ),
            ):
                stderr = io.StringIO()
                with redirect_stderr(stderr), redirect_stdout(io.StringIO()):
                    self.assertEqual(main((str(credit),)), 0)
                self.assertIn("not v2-validated", stderr.getvalue())
                credit.write_text("# Edited legacy bytes\n", encoding="utf-8")
                with redirect_stderr(io.StringIO()):
                    self.assertEqual(main((str(credit),)), 1)
                other = root / "other.md"
                other.write_text("# Legacy bytes\n", encoding="utf-8")
                with redirect_stderr(io.StringIO()):
                    self.assertEqual(main((str(other),)), 1)


if __name__ == "__main__":
    unittest.main()
