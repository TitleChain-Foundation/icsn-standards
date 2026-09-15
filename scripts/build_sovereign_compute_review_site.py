from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DISCUSSION_URL = "https://github.com/orgs/TitleChain-Foundation/discussions/38"
GRAPHQL_URL = "https://api.github.com/graphql"
SEED_AUTHOR = "satonakaoshimoto"
QUERY = """
query {
  repository(owner: "TitleChain-Foundation", name: ".github") {
    discussion(number: 38) {
      title url updatedAt
      comments(first: 100) {
        totalCount
        nodes {
          id url createdAt updatedAt body author { login }
          replies(first: 100) {
            nodes { id url createdAt updatedAt body author { login } }
          }
        }
      }
    }
  }
}
"""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_discussion(token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps({"query": QUERY}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "TitleChain-Sovereign-Compute-Review/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload["data"]["repository"]["discussion"]


def normalize_input(payload: dict[str, Any]) -> dict[str, Any]:
    if "data" in payload:
        return payload["data"]["repository"]["discussion"]
    return payload


def flatten(discussion: dict[str, Any]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for comment in discussion["comments"]["nodes"]:
        entries.append(
            {
                "url": comment["url"],
                "created_at": comment["createdAt"],
                "author": (comment.get("author") or {}).get("login", "ghost"),
                "body": comment["body"],
            }
        )
        for reply in comment["replies"]["nodes"]:
            entries.append(
                {
                    "url": reply["url"],
                    "created_at": reply["createdAt"],
                    "author": (reply.get("author") or {}).get("login", "ghost"),
                    "body": reply["body"],
                }
            )
    return sorted(entries, key=lambda item: item["created_at"], reverse=True)


def title(body: str) -> str:
    for line in body.splitlines():
        value = line.strip().lstrip("#").strip()
        if value:
            return value
    return "Public comment"


def body_html(body: str) -> str:
    blocks = []
    for index, block in enumerate(body.split("\n\n")):
        value = " ".join(line.strip() for line in block.splitlines() if line.strip())
        if not value or (index == 0 and value.startswith("##")):
            continue
        value = html.escape(value.lstrip("#").strip())
        value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
        value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
        blocks.append(f"<p>{value}</p>")
    return "".join(blocks)


def render(feed: dict[str, Any], reviewed: dict[str, Any]) -> str:
    entries = feed["entries"]
    themes = "".join(
        f"<article><h3>{html.escape(item['title'])}</h3>"
        f"<p>{html.escape(item['summary'])}</p>"
        f"<a href=\"{html.escape(item['source_comment'])}\">Source question</a></article>"
        for item in reviewed["themes"]
    )
    questions = "".join(
        f"<li>{html.escape(item)}</li>" for item in reviewed["open_questions"]
    )
    comments = "".join(
        "<article class=\"comment\">"
        f"<div class=\"meta\">{'Foundation seed question' if item['author'] == SEED_AUTHOR else 'Public response'} · "
        f"@{html.escape(item['author'])} · {html.escape(item['created_at'][:10])}</div>"
        f"<h3>{html.escape(title(item['body']))}</h3>"
        f"{body_html(item['body'])}"
        f"<a href=\"{html.escape(item['url'])}\">Read and respond on GitHub</a>"
        "</article>"
        for item in entries
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sovereign Compute Review Observatory</title>
<style>
:root{{--ink:#201726;--paper:#fbfaf7;--line:#d8d0c4;--gold:#936915;--rose:#9b2b65;--green:#176b58}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Avenir Next","Trebuchet MS",sans-serif;letter-spacing:0}}a{{color:#723057;text-underline-offset:3px}}header{{background:#fff;border-bottom:1px solid var(--line)}}.wrap{{width:min(1160px,calc(100% - 32px));margin:auto}}header .wrap{{padding:38px 0 32px}}.eyebrow,.meta{{color:var(--gold);font-size:.78rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}}h1,h2{{font-family:Georgia,serif;font-weight:500}}h1{{font-size:clamp(2.5rem,7vw,5.6rem);line-height:.96;max-width:900px;margin:12px 0}}.lede{{max-width:760px;font-size:1.1rem;line-height:1.6}}nav{{display:flex;flex-wrap:wrap;gap:12px 24px;margin-top:22px}}main{{padding:30px 0 70px}}.notice{{background:#fff;border-left:5px solid var(--rose);padding:16px 20px}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);border-block:1px solid var(--line);margin:30px 0}}.metric{{padding:24px;border-right:1px solid var(--line)}}.metric:last-child{{border:0}}.metric strong{{display:block;font:500 2.8rem Georgia,serif}}section{{margin-top:50px}}h2{{font-size:clamp(1.8rem,4vw,3rem)}}.summary{{font-size:1.15rem;line-height:1.65;max-width:900px}}.themes{{display:grid;grid-template-columns:repeat(2,1fr);border-top:1px solid var(--line)}}.themes article,.comment{{padding:25px 24px 28px 0;border-bottom:1px solid var(--line)}}.themes article:nth-child(odd){{border-right:1px solid var(--line)}}.themes article:nth-child(even){{padding-left:24px}}.visual{{display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center;background:#18302b;color:#fff;padding:30px}}.visual img{{width:100%;background:#fff}}.visual a{{color:#f0cb7d}}.questions,.comment{{max-width:940px;line-height:1.65}}.comment .meta{{color:var(--green)}}footer{{border-top:1px solid var(--line);padding:28px 0 50px;color:#655c6d}}@media(max-width:720px){{.metrics,.themes,.visual{{grid-template-columns:1fr}}.metric,.themes article:nth-child(odd){{border-right:0}}.themes article:nth-child(even){{padding-left:0}}}}
</style></head><body>
<header><div class="wrap"><div class="eyebrow">TitleChain Foundation · Draft v1 public review</div><h1>Sovereign Compute Review Observatory</h1><p class="lede">A live source index and human-reviewed synthesis of comments on the Sovereign Compute Access Act. Discussion 38 remains the authoritative public record.</p><nav><a href="{DISCUSSION_URL}">Submit a comment</a><a href="https://github.com/TitleChain-Foundation/icsn-standards/blob/main/legislation/sovereign-compute-access-act/OFFICIAL-TEXT.md">Official Draft v1</a><a href="visuals/open-weight-compute-reference.html">Open-Weight Compute Reference</a><a href="visuals/sovereign-intelligence-stack.html">Sovereign Intelligence Stack</a><a href="media/open-weight-m5/index.html">Open Weights + M5 carousel</a><a href="media/carousel/index.html">Act carousel</a></nav></div></header>
<main class="wrap"><div class="notice"><strong>Public-review intelligence, not a vote.</strong> Seed questions frame the initial agenda. Counts do not establish consensus, and summaries do not replace source comments.</div>
<div class="metrics"><div class="metric"><strong>{feed['entry_count']}</strong>total entries</div><div class="metric"><strong>{feed['seed_count']}</strong>Foundation seed questions</div><div class="metric"><strong>{feed['independent_count']}</strong>independent responses</div></div>
<section><div class="eyebrow">Human-reviewed synthesis</div><h2>Initial takeaways</h2><p class="summary">{html.escape(reviewed['takeaway'])}</p><div class="themes">{themes}</div><p><strong>Approved:</strong> {html.escape(reviewed['approved_at'])} · {html.escape(reviewed['reviewer'])}</p></section>
<section><div class="eyebrow">Evidence agenda</div><h2>Questions the record must answer</h2><ol class="questions">{questions}</ol></section>
<section class="visual"><div><div class="eyebrow">Featured architecture</div><h2>Sovereign Intelligence Stack</h2><p>Open the browser-rendered visual, not GitHub's source-code view.</p><a href="visuals/sovereign-intelligence-stack.html">View full visual</a></div><a href="visuals/sovereign-intelligence-stack.html"><img src="visuals/sovereign-intelligence-stack.png" alt="Sovereign Intelligence Stack architecture"></a></section>
<section><div class="eyebrow">Live source feed</div><h2>Discussion 38 comments</h2><p>Source updated <code>{html.escape(feed['discussion_updated_at'])}</code>. Feed generated <code>{html.escape(feed['generated_at'])}</code>.</p>{comments}</section></main>
<footer><div class="wrap">Source: <a href="{DISCUSSION_URL}">GitHub Discussion 38</a>. Verify every summary against its linked source.</div></footer></body></html>"""


def copy_assets(root: Path, output: Path) -> None:
    act = root / "legislation" / "sovereign-compute-access-act"
    visuals = output / "visuals"
    carousel = output / "media" / "carousel"
    open_weight_carousel = output / "media" / "open-weight-m5"
    visuals.mkdir(parents=True, exist_ok=True)
    carousel.mkdir(parents=True, exist_ok=True)
    pairs = {
        "OPEN-WEIGHT-COMPUTE-REFERENCE.html": "open-weight-compute-reference.html",
        "OPEN-WEIGHT-COMPUTE-REFERENCE.png": "open-weight-compute-reference.png",
        "SOVEREIGN-INTELLIGENCE-STACK.html": "sovereign-intelligence-stack.html",
        "SOVEREIGN-INTELLIGENCE-STACK.png": "sovereign-intelligence-stack.png",
    }
    for source, target in pairs.items():
        shutil.copy2(act / "appendices" / source, visuals / target)
    for name in ("index.html", "Sovereign-Compute-Access-Act-Carousel.pdf"):
        shutil.copy2(act / "media" / "sovereign-compute-act-carousel" / name, carousel / name)
    shutil.copytree(
        act / "media" / "open-weight-m5-carousel",
        open_weight_carousel,
        dirs_exist_ok=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    if args.input:
        discussion = normalize_input(load_json(args.input))
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise RuntimeError("GITHUB_TOKEN is required unless --input is used")
        discussion = fetch_discussion(token)
    reviewed = load_json(root / "legislation/sovereign-compute-access-act/observatory/reviewed-summary.json")
    if reviewed.get("review_status") != "APPROVED":
        raise ValueError("Reviewed summary is not approved")
    entries = flatten(discussion)
    seed_count = sum(item["author"] == SEED_AUTHOR for item in entries)
    feed = {
        "discussion_url": discussion["url"],
        "discussion_updated_at": discussion["updatedAt"],
        "generated_at": datetime.now(UTC).isoformat(),
        "entry_count": len(entries),
        "seed_count": seed_count,
        "independent_count": len(entries) - seed_count,
        "reviewed_summary": reviewed,
        "entries": entries,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "feed.json").write_text(json.dumps(feed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.output / "index.html").write_text(render(feed, reviewed), encoding="utf-8")
    copy_assets(root, args.output)
    print(f"Built {len(entries)} entries with {feed['independent_count']} independent responses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
