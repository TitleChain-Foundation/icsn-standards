#!/usr/bin/env python3
"""Regression check for the UTF-8 mojibake bug: on a system whose locale
encoding isn't UTF-8 (e.g. Windows/cp1252), reading source chapters or
writing generated output without an explicit encoding mis-decodes
non-ASCII characters (em dashes, middots) into mojibake. See the issue
this fixes: generator scripts must pass encoding="utf-8" everywhere.

Usage:  python3 tools/test_generate_checklist_encoding.py
"""

from generate_checklist import parse

MOJIBAKE_MARKERS = ("â€", "Â·")  # UTF-8 bytes of em dash / middot mis-decoded as Latin-1


def demo() -> None:
    chapters = parse()
    assert chapters, "parse() returned no chapters — is 0.1/en/ present?"

    text = "\n".join(
        req["text_md"]
        for *_, reqs in chapters
        for req in reqs
    )
    assert "—" in text, "expected at least one em dash (—) in parsed requirement text"
    for marker in MOJIBAKE_MARKERS:
        assert marker not in text, f"mojibake marker {marker!r} found — a read/write is missing encoding=\"utf-8\""

    total = sum(len(reqs) for *_, reqs in chapters)
    print(f"ok: {total} requirements parsed, no mojibake")


if __name__ == "__main__":
    demo()
