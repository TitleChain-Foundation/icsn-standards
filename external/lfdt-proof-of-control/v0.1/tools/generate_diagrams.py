#!/usr/bin/env python3
"""Generate the standard's branded SVG diagrams in light and dark variants.

Design system v2 — Advanced AI Society brand (advancedaisociety.org):
near-black #0a0a0a, electric lime #cfff04, warm off-white #f0edea,
reds #ff6568/#bf000f, Montserrat / Source Sans 3.

Every figure is a self-contained rounded panel (opaque background, subtle
gradient, dot-grid texture, soft card shadows), so it renders correctly on
any page background. Semantic colors: lime = proof/evidence (the brand
moment), red = blocked/never-crosses, warm neutral = ordinary machinery,
black-on-lime inversion = the accent (mirrors the site's CTA buttons).

Usage:  python3 tools/generate_diagrams.py
Outputs images/diagrams/<name>-{light,dark}.svg. Embed via <picture>.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "diagrams"

FONT = "Montserrat,'Source Sans 3',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "light": {
        "panel_top": "#ffffff", "panel_bot": "#f5f3ef", "panel_stroke": "#e3ded7",
        "grid": "#0a0a0a", "grid_op": "0.05",
        "text": "#141414", "muted": "#6b665f", "faint": "#a09a91", "line": "#8a857c",
        "card_top": "#ffffff", "card_bot": "#f8f6f3", "card_stroke": "#dcd6cd",
        "warm_top": "#efece6", "warm_bot": "#e6e2da", "warm_stroke": "#c6bfb4", "warm_text": "#4a463f",
        "lime_top": "#e4ff5c", "lime_bot": "#cfff04", "lime_stroke": "#8fae00", "lime_text": "#1a2000",
        "tint_top": "#f8ffd8", "tint_bot": "#eeffa8", "tint_stroke": "#a9c920", "tint_text": "#3a4900",
        "red_top": "#ffeced", "red_bot": "#ffdcde", "red_stroke": "#d94a52", "red_text": "#8c1119",
        "ink_top": "#242424", "ink_bot": "#0a0a0a", "ink_stroke": "#0a0a0a", "ink_text": "#f0edea",
        "gate_top": "#242424", "gate_bot": "#0a0a0a", "gate_stroke": "#0a0a0a", "gate_text": "#f0edea",
        "accent": "#7a9900", "shadow_op": "0.16",
    },
    "dark": {
        "panel_top": "#171717", "panel_bot": "#0e0e0e", "panel_stroke": "#2c2c2c",
        "grid": "#ffffff", "grid_op": "0.05",
        "text": "#f0edea", "muted": "#9d978e", "faint": "#6a665f", "line": "#8d877e",
        "card_top": "#242424", "card_bot": "#1b1b1b", "card_stroke": "#454545",
        "warm_top": "#2b2a26", "warm_bot": "#22211e", "warm_stroke": "#5c5850", "warm_text": "#d4cfc7",
        "lime_top": "#e3ff66", "lime_bot": "#c6f500", "lime_stroke": "#e3ff66", "lime_text": "#131800",
        "tint_top": "#2a3608", "tint_bot": "#1e2704", "tint_stroke": "#a5c614", "tint_text": "#dfff5e",
        "red_top": "#361417", "red_bot": "#280f12", "red_stroke": "#ff6568", "red_text": "#ffb3b5",
        "ink_top": "#e3ff66", "ink_bot": "#cfff04", "ink_stroke": "#cfff04", "ink_text": "#0a0a0a",
        "gate_top": "#222222", "gate_bot": "#151515", "gate_stroke": "#cfff04", "gate_text": "#e3ff66",
        "accent": "#cfff04", "shadow_op": "0.55",
    },
}

# Icon paths drawn on a 24x24 grid, stroke-based (round caps/joins).
ICONS = {
    "shield": "M12 3 L20 6 V12 C20 17 16.5 20 12 21.5 C7.5 20 4 17 4 12 V6 Z",
    "shieldcheck": "M9 12 L11.4 14.4 L15.6 9.6",
    "link_a": "M9.5 14.5 L14.5 9.5",
    "link_b": "M12.5 7 L14.5 5 A3.5 3.5 0 0 1 19.5 10 L17.5 12",
    "link_c": "M11.5 17 L9.5 19 A3.5 3.5 0 0 1 4.5 14 L6.5 12",
    "key_ring": "M9 15 m-4 0 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0",
    "key_stem": "M12.5 11.5 L20 4 M17 7 L19.5 9.5 M14.5 9.5 L16.5 11.5",
    "lock_body": "M6 11 H18 V20 H6 Z",
    "lock_arc": "M8.5 11 V8 A3.5 3.5 0 0 1 15.5 8 V11",
    "person_head": "M12 8 m-3 0 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0",
    "person_body": "M5.5 20 C5.5 15.8 8.4 13.8 12 13.8 C15.6 13.8 18.5 15.8 18.5 20",
    "doc": "M7 3.5 H14 L18 7.5 V20.5 H7 Z",
    "doc_fold": "M14 3.5 V7.5 H18",
    "doc_lines": "M9.5 12 H15.5 M9.5 15 H15.5 M9.5 18 H13",
    "eye_outer": "M3 12 C6 7 18 7 21 12 C18 17 6 17 3 12 Z",
    "eye_pupil": "M12 12 m-2.4 0 a2.4 2.4 0 1 0 4.8 0 a2.4 2.4 0 1 0 -4.8 0",
    "db_top": "M12 4.5 m-7 0 a7 2.6 0 1 0 14 0 a7 2.6 0 1 0 -14 0",
    "db_side": "M5 4.5 V18 A7 2.6 0 0 0 19 18 V4.5",
    "db_mid": "M5 11.2 A7 2.6 0 0 0 19 11.2",
    "globe_o": "M12 12 m-8.5 0 a8.5 8.5 0 1 0 17 0 a8.5 8.5 0 1 0 -17 0",
    "globe_v": "M12 3.5 C8.6 8 8.6 16 12 20.5 C15.4 16 15.4 8 12 3.5 M3.5 12 H20.5",
    "bolt": "M13 3 L6 13.5 H11 L10 21 L18 10 H13 Z",
    "gauge_o": "M4 17 A8.6 8.6 0 1 1 20 17",
    "gauge_n": "M12 15.5 L16.2 9",
}


class SVG:
    def __init__(self, name, w, h, theme, variant, title=None, eyebrow=None):
        self.name, self.w, self.h = name, w, h
        self.t, self.v = theme, variant
        t = theme
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}">',
            "<defs>",
            f'<linearGradient id="gPanel" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["panel_top"]}"/>'
            f'<stop offset="1" stop-color="{t["panel_bot"]}"/></linearGradient>',
            f'<linearGradient id="gCard" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["card_top"]}"/>'
            f'<stop offset="1" stop-color="{t["card_bot"]}"/></linearGradient>',
            f'<linearGradient id="gWarm" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["warm_top"]}"/>'
            f'<stop offset="1" stop-color="{t["warm_bot"]}"/></linearGradient>',
            f'<linearGradient id="gLime" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["lime_top"]}"/>'
            f'<stop offset="1" stop-color="{t["lime_bot"]}"/></linearGradient>',
            f'<linearGradient id="gTint" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["tint_top"]}"/>'
            f'<stop offset="1" stop-color="{t["tint_bot"]}"/></linearGradient>',
            f'<linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["red_top"]}"/>'
            f'<stop offset="1" stop-color="{t["red_bot"]}"/></linearGradient>',
            f'<linearGradient id="gInk" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["ink_top"]}"/>'
            f'<stop offset="1" stop-color="{t["ink_bot"]}"/></linearGradient>',
            f'<linearGradient id="gGate" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["gate_top"]}"/>'
            f'<stop offset="1" stop-color="{t["gate_bot"]}"/></linearGradient>',
            f'<filter id="fShadow" x="-30%" y="-30%" width="160%" height="170%">'
            f'<feDropShadow dx="0" dy="2.5" stdDeviation="4" '
            f'flood-color="#000000" flood-opacity="{t["shadow_op"]}"/></filter>',
            (f'<filter id="fGlow" x="-60%" y="-60%" width="220%" height="220%">'
             f'<feDropShadow dx="0" dy="3" stdDeviation="5" '
             f'flood-color="#000000" flood-opacity="0.22"/></filter>'
             if variant == "light" else
             f'<filter id="fGlow" x="-60%" y="-60%" width="220%" height="220%">'
             f'<feDropShadow dx="0" dy="0" stdDeviation="3.5" '
             f'flood-color="{t["accent"]}" flood-opacity="0.55"/></filter>'),
            f'<pattern id="pGrid" width="22" height="22" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1" fill="{t["grid"]}" '
            f'opacity="{t["grid_op"]}"/></pattern>',
            "</defs>",
            # panel
            f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="20" '
            f'fill="url(#gPanel)" stroke="{t["panel_stroke"]}" stroke-width="1.5"/>',
            f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="20" '
            f'fill="url(#pGrid)"/>',
        ]
        if eyebrow:
            self.parts.append(
                f'<text x="34" y="42" font-size="11.5" font-weight="700" '
                f'letter-spacing="2.2" fill="{t["accent"]}">{eyebrow}</text>')
        if title:
            self.parts.append(
                f'<text x="34" y="70" font-size="19" font-weight="700" '
                f'letter-spacing="-0.2" fill="{t["text"]}">{title}</text>')

    # ---------------------------------------------------------- primitives
    def text(self, x, y, s, size=13, fill=None, bold=False, anchor="middle",
             mono=False, spacing=None):
        t = self.t
        attrs = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"',
                 f'fill="{fill or t["text"]}"', f'text-anchor="{anchor}"']
        if bold:
            attrs.append('font-weight="700"')
        if mono:
            attrs.append(f'font-family="{MONO}"')
        if spacing:
            attrs.append(f'letter-spacing="{spacing}"')
        self.parts.append(f'<text {" ".join(attrs)}>{s}</text>')

    def card(self, x, y, w, h, kind="card", rx=14, shadow=True, glow=False):
        t = self.t
        stroke = {"card": t["card_stroke"], "warm": t["warm_stroke"],
                  "lime": t["lime_stroke"], "tint": t["tint_stroke"],
                  "red": t["red_stroke"], "ink": t["ink_stroke"],
                  "gate": t["gate_stroke"]}[kind]
        grad = {"card": "gCard", "warm": "gWarm", "lime": "gLime",
                "tint": "gTint", "red": "gRed", "ink": "gInk",
                "gate": "gGate"}[kind]
        f = ' filter="url(#fGlow)"' if glow else (' filter="url(#fShadow)"' if shadow else "")
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="url(#{grad})" stroke="{stroke}" stroke-width="1.5"{f}/>')

    def card_text(self, kind):
        t = self.t
        return {"card": t["text"], "warm": t["warm_text"], "lime": t["lime_text"],
                "tint": t["tint_text"], "red": t["red_text"], "ink": t["ink_text"],
                "gate": t["gate_text"]}[kind]

    def icon(self, name_list, x, y, color, scale=1.0, width=1.9):
        g = (f'<g transform="translate({x},{y}) scale({scale})" fill="none" '
             f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
             f'stroke-linejoin="round">')
        for n in name_list:
            g += f'<path d="{ICONS[n]}"/>'
        g += "</g>"
        self.parts.append(g)

    def arrow(self, x1, y1, x2, y2, dashed=False, color=None, width=2):
        c = color or self.t["line"]
        d = ' stroke-dasharray="7 5"' if dashed else ""
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" '
            f'stroke-width="{width}" stroke-linecap="round"{d}/>')
        if x1 == x2:
            s = 1 if y2 > y1 else -1
            pts = f"{x2},{y2 + s*1} {x2-5.5},{y2 - s*9} {x2+5.5},{y2 - s*9}"
        else:
            s = 1 if x2 > x1 else -1
            pts = f"{x2 + s*1},{y2} {x2 - s*9},{y2-5.5} {x2 - s*9},{y2+5.5}"
        self.parts.append(f'<polygon points="{pts}" fill="{c}"/>')

    def curve(self, x1, y1, x2, y2, bend, dashed=False, color=None, width=2,
              head=True):
        c = color or self.t["line"]
        d = ' stroke-dasharray="7 5"' if dashed else ""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + bend
        self.parts.append(
            f'<path d="M{x1} {y1} Q {mx} {my} {x2} {y2}" fill="none" '
            f'stroke="{c}" stroke-width="{width}" stroke-linecap="round"{d}/>')
        if head:
            s = 1 if x2 > mx else -1
            self.parts.append(
                f'<polygon points="{x2 + s*3},{y2} {x2 - s*8},{y2-5.5} '
                f'{x2 - s*8},{y2+5.5}" fill="{c}"/>')

    def pill(self, cx, cy, s, kind="warm", size=11, w=None, mono=False):
        t = self.t
        w = w or (len(s) * size * 0.62 + 26)
        self.card(cx - w / 2, cy - 13, w, 26, kind=kind, rx=13, shadow=False)
        self.text(cx, cy + 4, s, size=size, fill=self.card_text(kind),
                  bold=True, mono=mono)

    def label(self, x, y, s, size=11, anchor="middle"):
        self.text(x, y, s, size=size, fill=self.t["muted"], anchor=anchor)

    def caption(self, s, y=None, size=12.5):
        self.text(self.w / 2, y or self.h - 26, s, size=size,
                  fill=self.t["muted"])

    def save(self):
        self.parts.append("</svg>")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{self.name}-{self.v}.svg").write_text("\n".join(self.parts) + "\n", encoding="utf-8")


def multiline(s, x, y, lines, lh=17, size=12, fill=None, bold_first=False,
              anchor="middle", first_size=None):
    for i, line in enumerate(lines):
        s.text(x, y + i * lh, line,
               size=(first_size or size) if i == 0 else size,
               fill=fill, bold=(bold_first and i == 0), anchor=anchor)


# ================================================================ diagrams\n

def standard_at_a_glance(t, v):
    s = SVG("standard-at-a-glance", 1120, 430, t, v,
            eyebrow="THE STANDARD AT A GLANCE",
            title="From six domains to a checkable claim")
    s.card(34, 96, 250, 262, kind="card")
    s.text(159, 124, "WHAT — C1–C6", 11, t["muted"], bold=True, spacing=1.5)
    doms = [("Provenance", ["link_a", "link_b", "link_c"]),
            ("Privacy", ["eye_outer", "eye_pupil"]),
            ("Portability", ["globe_o", "globe_v"]),
            ("Authorization", ["lock_body", "lock_arc"]),
            ("Identity", ["person_head", "person_body"]),
            ("Security", ["shield", "shieldcheck"])]
    for i, (name, ic) in enumerate(doms):
        y = 138 + i * 36
        s.icon(ic, 52, y, t["accent"], scale=0.78)
        s.text(78, y + 14, name, 13, t["text"], bold=True, anchor="start")
    s.card(330, 128, 230, 176, kind="gate", glow=True)
    s.icon(["bolt"], 430, 142, t["gate_text"], scale=1.0)
    s.text(445, 188, "HOW — C7", 10.5, t["gate_text"], bold=True, spacing=1.5)
    s.text(445, 210, "Action Interception", 15.5, t["gate_text"], bold=True)
    s.text(445, 229, "Gateway", 15.5, t["gate_text"], bold=True)
    s.text(445, 255, "binary · contemporaneous", 11, t["gate_text"])
    s.text(445, 271, "tamper-evident · transparent", 11, t["gate_text"])
    s.card(606, 128, 210, 176, kind="tint")
    s.icon(["gauge_o", "gauge_n"], 700, 142, t["tint_text"], scale=1.0)
    s.text(711, 188, "HOW MUCH — C8", 10.5, t["tint_text"], bold=True, spacing=1.5)
    s.text(711, 210, "Verifiability", 15.5, t["tint_text"], bold=True)
    s.text(711, 229, "Tiers 1–4", 15.5, t["tint_text"], bold=True)
    s.text(711, 255, "binary threshold", 11, t["tint_text"])
    s.text(711, 271, "at Tier 3", 11, t["tint_text"])
    s.card(862, 128, 224, 176, kind="lime")
    s.icon(["doc", "doc_fold", "doc_lines"], 962, 142, t["lime_text"], scale=1.0)
    s.text(974, 188, "CHECKED — C10", 10.5, t["lime_text"], bold=True, spacing=1.5)
    s.text(974, 211, "Self-Declared", 13, t["lime_text"], bold=True)
    s.text(974, 233, "Third-Party Assessed", 13, t["lime_text"], bold=True)
    s.text(974, 255, "Continuously", 13, t["lime_text"], bold=True)
    s.text(974, 273, "Monitored", 13, t["lime_text"], bold=True)
    s.arrow(290, 216, 324, 216)
    s.arrow(566, 216, 600, 216)
    s.arrow(822, 216, 856, 216)
    s.card(330, 334, 756, 40, kind="warm", shadow=False)
    s.text(708, 359, "WHERE — C9 · every claim locates its evidence on MAESTRO Layers 1–7",
           12, t["warm_text"], bold=True)
    for cx in (445, 711, 974):
        s.arrow(cx, 310, cx, 328, dashed=True)
    s.caption("a claim = domains × evidence × tier × stage — checkable by anyone",
              y=s.h - 24)
    s.save()


def tier_ladder(t, v):
    s = SVG("tier-ladder", 860, 620, t, v,
            eyebrow="THE VERIFIABILITY TIERS",
            title="Graded by who you must trust — not by whether cryptography is used")
    rungs = [
        ("lime", 104, "TIER 4", "Self-Enforcing",
         "trust: the protocol itself — cannot run otherwise", "PROOF-OF-CONTROL", True),
        ("tint", 206, "TIER 3", "Trust-minimized",
         "trust: the mechanism and the parties it rests on", "PROOF-OF-CONTROL", True),
        ("warm", 366, "TIER 2", "Attestation",
         "trust: a third party or qualified auditor", "NOT PROOF-OF-CONTROL", False),
        ("red", 468, "TIER 1", "Assertion",
         "trust: the operator's word", "NOT PROOF-OF-CONTROL", False),
    ]
    for kind, y, tier, name, trust, verdict, is_poc in rungs:
        s.card(150, y, 600, 84, kind=kind, glow=(kind == "lime"))
        fill = s.card_text(kind)
        s.text(184, y + 38, tier, 12.5, fill, bold=True, spacing=1.5, anchor="start")
        s.text(184, y + 60, verdict, 9, fill, spacing=1.0, anchor="start")
        s.text(420, y + 38, name, 17, fill, bold=True, anchor="start")
        s.text(420, y + 60, trust, 11.5, fill, anchor="start")
        s.icon(["shield", "shieldcheck"] if is_poc else ["shield"],
               702, y + 30, fill, scale=0.95)
    s.arrow(104, 556, 104, 162, color=t["faint"])
    s.parts.append(
        f'<text x="88" y="360" font-size="11.5" fill="{t["muted"]}" '
        f'text-anchor="middle" transform="rotate(-90 88 360)">less trust required</text>')
    s.parts.append(
        f'<line x1="150" y1="322" x2="750" y2="322" stroke="{t["accent"]}" '
        f'stroke-width="3" stroke-dasharray="10 7" stroke-linecap="round"/>')
    s.card(288, 300, 324, 44, kind="ink", rx=22)
    s.text(450, 327, "THE BINARY THRESHOLD", 13.5, t["ink_text"], bold=True,
           spacing=1.2)
    s.caption("below: authenticated documentation — above: mechanism-generated evidence",
              y=586)
    s.save()


def conformance_stages(t, v):
    s = SVG("conformance-stages", 1040, 370, t, v,
            eyebrow="CONFORMANCE — C10",
            title="Three stages, one disclosure")
    stages = [
        (34, "warm", "01", "Self-Declared",
         ["operator publishes a", "standardized statement"], ["doc", "doc_fold", "doc_lines"]),
        (376, "tint", "02", "Third-Party Assessed",
         ["accredited assessor examines", "and confirms conformance"], ["eye_outer", "eye_pupil"]),
        (718, "lime", "03", "Continuously Monitored",
         ["every in-scope action", "validated as it occurs"], ["gauge_o", "gauge_n"]),
    ]
    for x, kind, num, name, desc, ic in stages:
        s.card(x, 100, 288, 134, kind=kind, glow=(kind == "lime"))
        fill = s.card_text(kind)
        s.text(x + 30, 138, num, 22, fill, bold=True, anchor="start", mono=True)
        s.icon(ic, x + 240, 115, fill, scale=0.95)
        s.text(x + 30, 172, name, 16.5, fill, bold=True, anchor="start")
        s.text(x + 30, 196, desc[0], 12, fill, anchor="start")
        s.text(x + 30, 213, desc[1], 12, fill, anchor="start")
    s.arrow(328, 167, 370, 167)
    s.arrow(670, 167, 712, 167)
    for cx in (178, 520, 862):
        s.arrow(cx, 240, cx, 262, dashed=True)
    s.card(140, 270, 760, 44, kind="ink", rx=22)
    s.text(520, 297, "TRUST-ASSUMPTION DISCLOSURE — REQUIRED AT EVERY STAGE",
           12.5, t["ink_text"], bold=True, spacing=1)
    s.caption("the disclosure is what lets two conformant systems be priced differently",
              y=s.h - 24)
    s.save()


def document_map(t, v):
    s = SVG("document-map", 1040, 500, t, v,
            eyebrow="HOW THE STANDARD IS ORGANIZED",
            title="The specification, the case, and the crosswalks")
    s.card(34, 96, 564, 340, kind="card")
    s.text(64, 128, "THE STANDARD — NORMATIVE · 0.1/en/", 11, t["muted"],
           bold=True, spacing=1.5, anchor="start")
    bands = [
        (146, "tint", "C1–C6 · The six domains",
         "Provenance · Privacy · Portability · Authorization · Identity · Security"),
        (240, "tint", "C7–C10 · Cross-cutting requirements",
         "Evidence generation · Verifiability Tiers · System surface · Conformance"),
        (334, "warm", "Appendices A–E",
         "Glossary · Mechanisms · Threat model · Open issues · Audit checklist"),
    ]
    for y, kind, tt, sub in bands:
        s.card(58, y, 512, 78, kind=kind, shadow=False)
        fill = s.card_text(kind)
        s.text(82, y + 32, tt, 14.5, fill, bold=True, anchor="start")
        s.text(82, y + 54, sub, 11, fill, anchor="start")
    # bracket connecting the three bands to the two companions
    bx = 622
    s.parts.append(
        f'<path d="M604 185 H{bx} M604 279 H{bx} M604 373 H{bx} '
        f'M{bx} 171 V373" fill="none" stroke="{t["line"]}" stroke-width="2" '
        f'stroke-linecap="round" stroke-dasharray="7 5"/>')
    s.arrow(bx, 171, 668, 171, dashed=True)
    s.arrow(bx, 361, 668, 361, dashed=True)
    s.card(676, 96, 330, 150, kind="card")
    s.icon(["doc", "doc_fold", "doc_lines"], 952, 112, t["accent"], scale=0.9)
    s.text(702, 130, "THE CASE — docs/", 11, t["muted"], bold=True,
           spacing=1.5, anchor="start")
    s.text(702, 158, "Companion documents", 14.5, t["text"], bold=True, anchor="start")
    s.text(702, 182, "Introduction · Why verification matters", 11.5, t["muted"], anchor="start")
    s.text(702, 199, "Use cases · Roadmap · Governance", 11.5, t["muted"], anchor="start")
    s.text(702, 216, "Research basis · The Smart Leash", 11.5, t["muted"], anchor="start")
    s.card(676, 286, 330, 150, kind="card")
    s.icon(["globe_o", "globe_v"], 952, 302, t["accent"], scale=0.9)
    s.text(702, 320, "CROSSWALKS — mappings/", 11, t["muted"], bold=True,
           spacing=1.5, anchor="start")
    s.text(702, 348, "Coverage mapping", 14.5, t["text"], bold=True, anchor="start")
    s.text(702, 372, "NIST · ISO 42001 · OWASP · EU AI Act", 11.5, t["muted"], anchor="start")
    s.text(702, 389, "SOC 2 · AARM · ATLAS · Zero Trust", 11.5, t["muted"], anchor="start")
    s.text(702, 406, "Rubric · coding sheet · reproducible", 11.5, t["muted"], anchor="start")
    s.caption("the normative core is under change control; the case and the "
              "crosswalks travel with it", y=s.h - 24)
    s.save()


def first_claim_journey(t, v):
    s = SVG("first-claim-journey", 1180, 290, t, v,
            eyebrow="MAKING YOUR FIRST CLAIM",
            title="Seven steps from domains to a published statement")
    steps = [
        ("1", "Choose", "domains", "C1–C6"),
        ("2", "Locate on", "the stack", "C9"),
        ("3", "Choose", "mechanisms", "App. B"),
        ("4", "Meet the four", "properties", "C7"),
        ("5", "Grade on", "the Tiers", "C8"),
        ("6", "Disclose trust", "assumptions", "C10.2"),
        ("7", "Publish the", "statement", "C10.1"),
    ]
    for i, (n, l1, l2, ref) in enumerate(steps):
        x = 34 + i * 163
        last = i == len(steps) - 1
        kind = "lime" if last else "card"
        s.card(x, 104, 138, 112, kind=kind, glow=last)
        fill = s.card_text(kind)
        ring = fill if last else t["accent"]
        s.parts.append(
            f'<circle cx="{x+28}" cy="{104+26}" r="13" fill="none" '
            f'stroke="{ring}" stroke-width="2"/>')
        s.text(x + 28, 135, n, 12.5, ring, bold=True)
        s.text(x + 20, 166, l1, 12.5, fill, bold=True, anchor="start")
        s.text(x + 20, 184, l2, 12.5, fill, bold=True, anchor="start")
        s.text(x + 20, 204, ref, 10.5, fill if last else t["muted"],
               anchor="start", mono=True)
        if not last:
            cxa = x + 146
            s.parts.append(
                f'<path d="M{cxa} 152 l8 8 l-8 8" fill="none" '
                f'stroke="{t["line"]}" stroke-width="2.5" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    s.caption("your entry point is the Self-Declared conformance statement (C10.1)",
              y=s.h - 26)
    s.save()


def evidence_flow(t, v):
    s = SVG("evidence-flow", 1040, 430, t, v,
            eyebrow="EVIDENCE GENERATION — C7",
            title="No side effect without evidence")
    s.card(34, 120, 200, 100, kind="warm")
    s.icon(["bolt"], 54, 134, t["warm_text"], scale=0.8)
    s.text(84, 152, "Agent", 15.5, t["warm_text"], bold=True, anchor="start")
    s.text(54, 182, "plans an action", 12, t["warm_text"], anchor="start")
    s.card(330, 100, 250, 140, kind="gate", glow=True)
    s.icon(["shield", "shieldcheck"], 344, 114, t["gate_text"], scale=0.85)
    s.text(374, 132, "Action Interception", 15.5, t["gate_text"], bold=True,
           anchor="start")
    s.text(374, 151, "Gateway", 15.5, t["gate_text"], bold=True, anchor="start")
    s.text(344, 182, "out-of-band · C7.1", 11.5, t["gate_text"], anchor="start",
           mono=True)
    s.text(344, 205, "evidence written before the", 11.5, t["gate_text"], anchor="start")
    s.text(344, 221, "action is released", 11.5, t["gate_text"], anchor="start")
    s.card(790, 120, 160, 100, kind="warm")
    s.text(810, 152, "Tool / effect", 15, t["warm_text"], bold=True, anchor="start")
    s.text(810, 176, "executes", 12, t["warm_text"], anchor="start")
    s.card(330, 290, 250, 106, kind="lime", glow=True)
    s.icon(["doc", "doc_fold", "doc_lines"], 344, 302, t["lime_text"], scale=0.8)
    s.text(374, 320, "Evidence", 15.5, t["lime_text"], bold=True, anchor="start")
    s.text(344, 348, "binary · contemporaneous", 11.5, t["lime_text"], anchor="start")
    s.text(344, 364, "tamper-evident · transparent", 11.5, t["lime_text"], anchor="start")
    s.card(700, 290, 300, 106, kind="card")
    s.icon(["eye_outer", "eye_pupil"], 716, 302, t["accent"], scale=0.8)
    s.text(746, 320, "Any verifier", 15, t["text"], bold=True, anchor="start")
    s.text(716, 348, "auditor · insurer · regulator", 11.5, t["muted"], anchor="start")
    s.text(716, 364, "no privileged access", 11.5, t["muted"], anchor="start")
    s.arrow(240, 170, 322, 170)
    s.label(281, 158, "action")
    s.arrow(586, 152, 782, 152)
    s.label(684, 140, "authorized")
    s.curve(784, 194, 590, 194, 26, dashed=True)
    s.label(688, 236, "result")
    s.arrow(455, 246, 455, 282)
    s.text(475, 258, "before · during · after", 11, t["muted"], anchor="start")
    s.text(475, 274, "out of scope: rejected + evidenced", 11, t["red_stroke"],
           anchor="start")
    s.arrow(586, 343, 694, 343)
    s.save()


def maestro_stack(t, v):
    s = SVG("maestro-stack", 760, 620, t, v,
            eyebrow="THE SYSTEM SURFACE — C9",
            title="Seven MAESTRO layers; every claim states where it applies")
    layers = [
        ("L7", "Agent Ecosystem", "marketplaces · registries · other agents"),
        ("L6", "Security, Governance &amp; Compliance", "policy · change management · audit"),
        ("L5", "Evaluation &amp; Observability", "tamper-evident logging · forensics"),
        ("L4", "Deployment &amp; Infrastructure", "containers · networks · secrets · TEEs"),
        ("L3", "Agent Framework", "planning · tools · workflows · memory"),
        ("L2", "Data Operations", "ingestion · embeddings · RAG"),
        ("L1", "Foundation Model", "weights · serving · behavioral policy"),
    ]
    for i, (lid, name, sub) in enumerate(layers):
        y = 100 + i * 66
        hl = lid == "L5"
        kind = "lime" if hl else "card"
        s.card(60, y, 640, 54, kind=kind, glow=hl)
        fill = s.card_text(kind)
        s.text(92, y + 33, lid, 15, fill, bold=True, mono=True)
        s.text(126, y + 26, name, 14.5, fill, bold=True, anchor="start")
        s.text(126, y + 44, sub, 11, fill if hl else t["muted"], anchor="start")
        if hl:
            s.icon(["doc", "doc_fold", "doc_lines"], 654, y + 15, fill, scale=0.8)
    s.caption("L5 highlighted: without tamper-evident records, no post-hoc proof is possible",
              y=s.h - 24)
    s.save()


def risk_value_quadrant(t, v):
    s = SVG("risk-value-quadrant", 780, 500, t, v,
            eyebrow="WHY VERIFICATION MATTERS",
            title="The agent risk-to-value bind")
    x0, y0, cw, ch = 150, 104, 280, 150
    cells = [
        (x0, y0, "red", "Failed deployment", "risk realized, value lost"),
        (x0 + cw + 10, y0, "warm", "Unleash", "value, but unquantifiable risk"),
        (x0, y0 + ch + 10, "card", "Constrain", "safe, but can't do the job"),
        (x0 + cw + 10, y0 + ch + 10, "lime", "Proof-of-Control", "value up, risk down"),
    ]
    for x, y, kind, tt, sub in cells:
        s.card(x, y, cw, ch, kind=kind, glow=(kind == "lime"))
        fill = s.card_text(kind)
        s.text(x + cw / 2, y + ch / 2 - 4, tt, 17, fill, bold=True)
        s.text(x + cw / 2, y + ch / 2 + 20, sub, 12, fill)
    ox, oy = 118, y0 + 2 * ch + 42
    s.arrow(ox, oy, ox, y0 - 16, color=t["faint"])
    s.parts.append(
        f'<text x="102" y="{y0+ch}" font-size="11.5" fill="{t["muted"]}" '
        f'text-anchor="middle" transform="rotate(-90 102 {y0+ch})">risk</text>')
    s.arrow(ox, oy, x0 + 2 * cw + 26, oy, color=t["faint"])
    s.label(x0 + cw + 5, oy + 22, "value")
    s.caption("Proof-of-Control breaks the bind — value up and risk down at once",
              y=s.h - 22)
    s.save()


def smart_leash(t, v):
    s = SVG("smart-leash", 1180, 330, t, v,
            eyebrow="THE SMART LEASH",
            title="trust me → trust my auditor → trust the math → the leash locks itself")
    grad_end = "#7a9900" if v == "light" else "#cfff04"
    s.parts.append(
        f'<defs><linearGradient id="gLeash" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{t["faint"]}"/>'
        f'<stop offset="0.35" stop-color="{t["red_stroke"]}"/>'
        f'<stop offset="0.65" stop-color="{t["warm_stroke"]}"/>'
        f'<stop offset="1" stop-color="{grad_end}"/></linearGradient></defs>'
        f'<rect x="76" y="122" width="990" height="5" rx="2.5" '
        f'fill="url(#gLeash)"/>')
    s.parts.append(
        f'<polygon points="1082,124.5 1064,117 1064,132" fill="{grad_end}"/>')
    nodes = [
        (34, "warm", "I", "PREREQUISITE", "Whose dog is this?",
         ["Collar tag and owner registration:", "identity, provenance, liability."],
         ["person_head", "person_body"]),
        (322, "red", "T1", "TIER 1 · ASSERTION", "The owner's word",
         ["“My dog is friendly and stays in the", "yard.” They also write the incident report."],
         ["doc", "doc_fold"]),
        (610, "warm", "T2", "TIER 2 · ATTESTATION", "The inspector's badge",
         ["A yearly paper stamp. It can't stop", "the dog jumping the fence today."],
         ["eye_outer", "eye_pupil"]),
        (898, "lime", "✓", "TIER 3–4 · PROOF-OF-CONTROL",
         "The smart, tamper-evident leash",
         ["Anyone can verify the proof — and the", "leash locks before the boundary is crossed."],
         ["shield", "shieldcheck"]),
    ]
    for x, kind, dot, tier, q, an, ic in nodes:
        cx = x + 110
        stroke = {"warm": t["warm_stroke"], "red": t["red_stroke"],
                  "lime": t["lime_stroke"]}[kind]
        fillbg = {"warm": t["warm_top"], "red": t["red_top"],
                  "lime": t["lime_bot"]}[kind]
        glow = ' filter="url(#fGlow)"' if kind == "lime" else ""
        s.parts.append(
            f'<circle cx="{cx}" cy="124" r="20" fill="{fillbg}" '
            f'stroke="{stroke}" stroke-width="2.5"{glow}/>')
        s.text(cx, 130, dot, 13.5, s.card_text(kind), bold=True, mono=True)
        acc = grad_end if kind == "lime" else stroke
        s.icon(ic, x, 162, acc, scale=0.72)
        s.text(x + 26, 176, tier, 10.5, acc, bold=True, spacing=1.2, anchor="start")
        s.text(x, 202, q, 15.5, t["text"], bold=True, anchor="start")
        s.text(x, 226, an[0], 11.5, t["muted"], anchor="start")
        s.text(x, 243, an[1], 11.5, t["muted"], anchor="start")
    s.caption("as you move right — verifiability rises, trust required falls",
              y=s.h - 26)
    s.save()


def roadmap(t, v):
    s = SVG("roadmap", 1180, 440, t, v,
            eyebrow="IMPLEMENTATION ROADMAP",
            title="Three phases, twenty-four months, three conformance stages")
    grad_end = "#7a9900" if v == "light" else "#cfff04"
    s.parts.append(
        f'<defs><linearGradient id="gTime" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{t["faint"]}"/>'
        f'<stop offset="1" stop-color="{grad_end}"/></linearGradient></defs>'
        f'<rect x="48" y="118" width="1084" height="5" rx="2.5" fill="url(#gTime)"/>')
    for m, x in (("M1", 48), ("M6", 406), ("M12", 778), ("M24", 1132)):
        s.parts.append(f'<circle cx="{x}" cy="120" r="5" fill="{t["muted"]}"/>')
        s.label(x, 102, m, size=10.5)
    phases = [
        (48, 340, "card", "PHASE 1 · MONTHS 1–6", "Foundational infrastructure",
         ["HSM key management and signing", "provenance signing · tamper-evident logs",
          "TEE runtime attestation"],
         "SELF-DECLARED READINESS"),
        (420, 340, "tint", "PHASE 2 · MONTHS 7–12", "Expanded proof coverage",
         ["provenance chains on pipelines and RAG", "tool-schema and workflow verification",
          "ZKP privacy compliance · PKI agent identity"],
         "THIRD-PARTY ASSESSED READINESS"),
        (792, 340, "lime", "PHASE 3 · MONTHS 13–24", "Ecosystem integration",
         ["cross-layer evidence aggregation", "delegation-chain verification",
          "cross-org proof interoperability · MPC gates"],
         "CONTINUOUSLY MONITORED READINESS"),
    ]
    for x, w, kind, tag, name, items, ready in phases:
        s.card(x, 148, w, 196, kind=kind, glow=(kind == "lime"))
        fill = s.card_text(kind)
        s.text(x + 26, 180, tag, 10.5, fill, bold=True, spacing=1.4, anchor="start")
        s.text(x + 26, 206, name, 16, fill, bold=True, anchor="start")
        for i, it in enumerate(items):
            s.text(x + 26, 232 + i * 19, it, 11.5, fill, anchor="start")
        s.card(x + 24, 296, w - 48, 30, kind="ink", rx=15, shadow=False)
        s.text(x + w / 2, 315, ready, 10, t["ink_text"], bold=True, spacing=1)
    s.arrow(394, 246, 414, 246)
    s.arrow(766, 246, 786, 246)
    s.caption("each phase brings the organization to readiness for one conformance "
              "stage (C10) — Version 1.0 of the standard targets February 1, 2027",
              y=s.h - 26)
    s.save()




def reference_architecture(t, v):
    s = SVG("reference-architecture", 1040, 760, t, v,
            eyebrow="REFERENCE ARCHITECTURE",
            title="From intercepted action to checkable proof")

    def rats(x, y, label):
        w = len(label) * 7.4 + 24
        s.card(x - w, y, w, 24, kind="warm", rx=12, shadow=False)
        s.text(x - w / 2, y + 16, label, 9.5, t["warm_text"], bold=True,
               spacing=1.1)

    # 1 · agent host
    s.card(120, 96, 560, 74, kind="warm")
    s.icon(["bolt"], 142, 110, t["warm_text"], scale=0.75)
    s.text(172, 128, "Agent host / runtime", 15, t["warm_text"], bold=True,
           anchor="start")
    s.text(172, 150, "plans · calls tools · delegates sub-tasks", 11.5,
           t["warm_text"], anchor="start")
    rats(1006, 108, "RATS · ATTESTER")
    s.arrow(400, 170, 400, 196)
    # 2 · interception
    s.card(120, 200, 560, 74, kind="card")
    s.icon(["gauge_o", "gauge_n"], 142, 214, t["accent"], scale=0.75)
    s.text(172, 232, "ACS lifecycle interception point", 15, t["text"],
           bold=True, anchor="start")
    s.text(172, 254, "task init · context · plan · pre/post-tool · memory · delegation · completion",
           11, t["muted"], anchor="start")
    rats(1006, 212, "TARGET ENVIRONMENT")
    s.arrow(400, 274, 400, 300)
    s.text(416, 292, "canonical state snapshot — path · identity · proposed action",
           11, t["muted"], anchor="start")
    # 3 · enclave
    s.card(120, 304, 560, 224, kind="gate", glow=True)
    s.icon(["shield", "shieldcheck"], 142, 318, t["gate_text"], scale=0.8)
    s.text(174, 336, "Hardware TEE enclave", 15, t["gate_text"], bold=True,
           anchor="start")
    steps = ["1  verify signed Rego policy bundle",
             "2  evaluate snapshot → ALLOW · DENY · MODIFY · ESCALATE",
             "3  append signed Merkle leaf  L_t = H(L_t-1 || H(snap) || verdict)",
             "4  sign Entity Attestation Token (EAT / CWT)"]
    for i, st in enumerate(steps):
        s.card(146, 356 + i * 42, 508, 34, kind="card", rx=8, shadow=False)
        s.text(164, 378 + i * 42, st, 11.5, t["text"], anchor="start",
               mono=True)
    rats(1006, 316, "ATTESTING ENVIRONMENT")
    s.arrow(400, 528, 400, 556)
    s.text(416, 548, "Evidence — signed EAT over the Merkle chain", 11,
           t["muted"], anchor="start")
    rats(1006, 536, "EVIDENCE")
    # 4 · verifier + relying party
    s.card(120, 560, 320, 108, kind="lime", glow=True)
    s.icon(["eye_outer", "eye_pupil"], 140, 574, t["lime_text"], scale=0.75)
    s.text(170, 592, "Verifier", 15, t["lime_text"], bold=True, anchor="start")
    s.text(140, 620, "compares evidence to published", 11.5, t["lime_text"],
           anchor="start")
    s.text(140, 637, "reference values → attestation result", 11.5,
           t["lime_text"], anchor="start")
    s.card(500, 560, 340, 108, kind="card")
    s.icon(["lock_body", "lock_arc"], 520, 574, t["accent"], scale=0.75)
    s.text(550, 592, "Relying party", 15, t["text"], bold=True, anchor="start")
    s.text(520, 620, "API gateway or service — requires a valid", 11.5,
           t["muted"], anchor="start")
    s.text(520, 637, "result before executing the tool request", 11.5,
           t["muted"], anchor="start")
    s.arrow(444, 614, 496, 614)
    rats(1006, 572, "VERIFIER")
    rats(1006, 604, "RELYING PARTY")
    s.caption("policy evaluation, evidence signing, and history live inside the "
              "enclave — the operator can run the agent, but cannot forge its record",
              y=s.h - 26)
    s.save()


# ------------------------------------------------- domain chapter figures

def c1_provenance(t, v):
    s = SVG("c1-provenance", 1040, 300, t, v,
            eyebrow="C1 · PROVENANCE", title="The chain of custody")
    s.card(34, 110, 250, 120, kind="warm")
    s.icon(["db_top", "db_side", "db_mid"], 54, 124, t["warm_text"], scale=0.8)
    s.text(86, 142, "Origin", 15.5, t["warm_text"], bold=True, anchor="start")
    s.text(54, 174, "training data · inputs", 12, t["warm_text"], anchor="start")
    s.text(54, 192, "signed at source", 12, t["warm_text"], anchor="start")
    s.card(384, 110, 280, 120, kind="card")
    s.icon(["doc", "doc_fold", "doc_lines"], 404, 124, t["accent"], scale=0.8)
    s.text(436, 142, "Model state", 15.5, t["text"], bold=True, anchor="start")
    s.text(404, 174, "sha256: 9f2c…e1", 12, t["muted"], anchor="start",
           mono=True)
    s.text(404, 192, "matches signed manifest ✓", 12, t["muted"], anchor="start")
    s.card(764, 110, 242, 120, kind="lime", glow=True)
    s.icon(["shield", "shieldcheck"], 784, 124, t["lime_text"], scale=0.8)
    s.text(816, 142, "Action record", 15.5, t["lime_text"], bold=True, anchor="start")
    s.text(784, 174, "what ran, on what, when", 12, t["lime_text"], anchor="start")
    s.text(784, 192, "custody chain complete ✓", 12, t["lime_text"], anchor="start")
    for x1, x2 in ((290, 376), (670, 756)):
        s.arrow(x1, 170, x2, 170)
        mid = (x1 + x2) / 2
        s.icon(["link_a", "link_b", "link_c"], mid - 30, 136, t["accent"], scale=0.62)
        s.text(mid + 6, 152, "hash link", 10.5, t["muted"], anchor="start")
    s.caption("an immutable chain from origin to action — a reviewer can walk it "
              "end-to-end without trusting the operator (C1.1–C1.2)", y=s.h - 26)
    s.save()


def c2_privacy(t, v):
    s = SVG("c2-privacy", 1040, 360, t, v,
            eyebrow="C2 · PRIVACY", title="Evidence without exposure")
    s.card(34, 110, 380, 120, kind="warm")
    s.icon(["db_top", "db_side", "db_mid"], 54, 124, t["warm_text"], scale=0.8)
    s.text(86, 142, "What the agent touched", 15, t["warm_text"], bold=True,
           anchor="start")
    s.text(54, 174, "customer record · full payload", 12, t["warm_text"],
           anchor="start")
    s.text(54, 192, "protected data — stays inside", 12, t["warm_text"],
           anchor="start")
    s.parts.append(
        f'<line x1="520" y1="96" x2="520" y2="252" stroke="{t["line"]}" '
        f'stroke-width="2" stroke-dasharray="8 6" stroke-linecap="round"/>')
    s.label(520, 88, "the disclosure boundary")
    s.card(626, 110, 380, 120, kind="lime", glow=True)
    s.icon(["doc", "doc_fold", "doc_lines"], 646, 124, t["lime_text"], scale=0.8)
    s.text(678, 142, "What the evidence shows", 15, t["lime_text"], bold=True,
           anchor="start")
    s.text(646, 174, "digest a41f…9c · 3 fields read", 12, t["lime_text"],
           anchor="start", mono=True)
    s.text(646, 192, "policy held ✓ — no payload", 12, t["lime_text"],
           anchor="start")
    s.arrow(420, 150, 620, 150)
    s.text(440, 138, "derived evidence only", 11, t["muted"], anchor="start")
    s.card(360, 266, 320, 44, kind="red", rx=22)
    s.text(520, 293, "raw payload ✕ never crosses", 13, t["red_text"],
           bold=True)
    s.caption("privacy evidence proves the rules held without re-leaking the "
              "data they protect (C2.1–C2.3)", y=s.h - 22)
    s.save()


def c3_portability(t, v):
    s = SVG("c3-portability", 1040, 340, t, v,
            eyebrow="C3 · PORTABILITY", title="The chain survives the crossing")
    for x0, title, ids in ((34, "Cloud A · attestation domain A", ("41", "42", "43")),
                           (634, "Cloud B · attestation domain B", ("44", "45", "46"))):
        s.card(x0, 100, 372, 168, kind="card")
        s.icon(["globe_o", "globe_v"], x0 + 22, 112, t["accent"], scale=0.7)
        s.text(x0 + 50, 129, title, 12.5, t["muted"], bold=True, anchor="start")
        for i, rid in enumerate(ids):
            bx = x0 + 24 + i * 112
            s.card(bx, 152, 96, 88, kind="warm", shadow=False)
            s.text(bx + 48, 186, "record", 11, t["warm_text"])
            s.text(bx + 48, 210, rid, 15, t["warm_text"], bold=True, mono=True)
            if i < 2:
                s.arrow(bx + 100, 196, bx + 108, 196)
    s.card(456, 152, 128, 88, kind="lime", glow=True)
    s.text(520, 188, "signed", 12.5, t["lime_text"], bold=True)
    s.text(520, 208, "linking record", 12.5, t["lime_text"], bold=True)
    s.arrow(412, 196, 450, 196)
    s.arrow(590, 196, 628, 196)
    s.caption("when evidence crosses vendors or jurisdictions, a signed link binds "
              "the two chains — no unverifiable gap at the boundary (C3.2)",
              y=s.h - 26)
    s.save()


def c4_authorization(t, v):
    s = SVG("c4-authorization", 1040, 400, t, v,
            eyebrow="C4 · AUTHORIZATION", title="The envelope and the gateway")
    s.card(34, 100, 640, 220, kind="card")
    s.icon(["lock_body", "lock_arc"], 54, 114, t["accent"], scale=0.7)
    s.text(82, 131, "GRANTED AUTHORITY — SCOPE · LIMITS · EXPIRY", 11,
           t["muted"], bold=True, spacing=1.2, anchor="start")
    chips = [("read customer record", 60, 156), ("issue refund within limit", 366, 156),
             ("call registered tools", 60, 222)]
    for label, x, y in chips:
        s.card(x, y, 286, 50, kind="tint", shadow=False)
        s.text(x + 20, y + 30, f"{label} ✓", 12.5, t["tint_text"],
               bold=True, anchor="start")
    s.text(366, 252, "every decision recorded", 11, t["muted"], anchor="start")
    s.parts.append(
        f'<rect x="716" y="120" width="12" height="200" rx="6" '
        f'fill="url(#gGate)" stroke="{t["gate_stroke"]}" filter="url(#fGlow)"/>')
    s.label(722, 342, "interception gateway")
    s.arrow(680, 220, 710, 220)
    # two outcomes
    s.arrow(734, 170, 762, 170)
    s.card(768, 138, 238, 62, kind="tint")
    s.text(788, 164, "in-scope action", 13, t["tint_text"], bold=True,
           anchor="start")
    s.text(788, 184, "executes · recorded ✓", 12, t["tint_text"], anchor="start")
    s.arrow(734, 268, 762, 268)
    s.card(768, 238, 238, 62, kind="red")
    s.text(788, 264, "export database", 13, t["red_text"], bold=True,
           anchor="start")
    s.text(788, 284, "✕ blocked + evidenced", 12, t["red_text"], anchor="start")
    s.caption("in-scope actions execute and are recorded; out-of-scope actions "
              "stop at the gateway — both leave evidence (C4.1)", y=s.h - 26)
    s.save()


def c5_identity(t, v):
    s = SVG("c5-identity", 1040, 320, t, v,
            eyebrow="C5 · IDENTITY", title="Every action has a principal")
    s.card(34, 110, 210, 108, kind="warm")
    s.icon(["person_head", "person_body"], 54, 124, t["warm_text"], scale=0.8)
    s.text(86, 142, "Principal", 15, t["warm_text"], bold=True, anchor="start")
    s.text(54, 176, "person or", 12, t["warm_text"], anchor="start")
    s.text(54, 193, "organization", 12, t["warm_text"], anchor="start")
    s.card(314, 110, 260, 108, kind="lime", glow=True)
    s.icon(["key_ring", "key_stem"], 334, 124, t["lime_text"], scale=0.8)
    s.text(366, 142, "Delegation token", 15, t["lime_text"], bold=True,
           anchor="start")
    s.text(334, 176, "signed · short-lived · scoped", 12, t["lime_text"],
           anchor="start")
    s.card(644, 110, 180, 108, kind="warm")
    s.icon(["bolt"], 664, 124, t["warm_text"], scale=0.8)
    s.text(692, 142, "Agent", 15, t["warm_text"], bold=True, anchor="start")
    s.text(664, 176, "cryptographic", 12, t["warm_text"], anchor="start")
    s.text(664, 193, "identity", 12, t["warm_text"], anchor="start")
    s.card(894, 110, 112, 108, kind="card")
    s.icon(["shield", "shieldcheck"], 916, 122, t["accent"], scale=0.7)
    s.text(950, 174, "Action", 14.5, t["text"], bold=True)
    s.text(950, 196, "recorded ✓", 11, t["muted"])
    s.arrow(250, 164, 308, 164)
    s.arrow(580, 164, 638, 164)
    s.arrow(830, 164, 888, 164)
    s.curve(950, 226, 139, 244, 46, dashed=True, head=False)
    s.arrow(139, 254, 139, 228, dashed=True)
    s.label(545, 284, "traces back — accountability")
    s.caption("every action traces back to a legitimate principal — no anonymous "
              "authority (C5.1)", y=s.h - 20)
    s.save()


def c6_security(t, v):
    s = SVG("c6-security", 1040, 380, t, v,
            eyebrow="C6 · SECURITY", title="The environment proves itself")
    s.card(34, 100, 450, 216, kind="card")
    s.icon(["shield", "shieldcheck"], 54, 114, t["accent"], scale=0.7)
    s.text(82, 131, "EXECUTION ENVIRONMENT", 11, t["muted"], bold=True,
           spacing=1.5, anchor="start")
    s.card(60, 152, 268, 52, kind="ink", rx=10, shadow=False)
    s.text(80, 184, "measurement 9e11…4b", 12.5, t["ink_text"], bold=True,
           anchor="start", mono=True)
    s.card(60, 222, 330, 52, kind="warm", shadow=False)
    s.text(80, 254, "generated code runs in a sandbox", 12.5, t["warm_text"],
           anchor="start")
    s.arrow(490, 158, 586, 158)
    s.label(538, 146, "attestation report")
    s.card(592, 100, 414, 116, kind="lime", glow=True)
    s.icon(["eye_outer", "eye_pupil"], 612, 114, t["lime_text"], scale=0.8)
    s.text(644, 132, "Independent verification", 15, t["lime_text"], bold=True,
           anchor="start")
    s.text(612, 164, "report compared to published", 12, t["lime_text"],
           anchor="start")
    s.text(612, 182, "reference values — pass ✓", 12, t["lime_text"],
           anchor="start")
    s.arrow(490, 276, 586, 276)
    s.label(538, 264, "signs evidence with")
    s.card(592, 248, 388, 56, kind="card")
    s.icon(["key_ring", "key_stem"], 610, 262, t["accent"], scale=0.75)
    s.text(642, 282, "evidence-signing keys in HSM — non-exportable", 12.5,
           t["text"], bold=True, anchor="start")
    s.caption("the environment is attested against reference values anyone can "
              "verify; the keys that sign evidence live in hardware (C6.1, C6.3)",
              y=s.h - 26)
    s.save()


DIAGRAMS = [standard_at_a_glance, tier_ladder, conformance_stages, document_map,
            first_claim_journey, evidence_flow, maestro_stack,
            risk_value_quadrant, smart_leash, roadmap, reference_architecture, c1_provenance, c2_privacy,
            c3_portability, c4_authorization, c5_identity, c6_security]


def main():
    for variant, theme in THEMES.items():
        for fn in DIAGRAMS:
            fn(theme, variant)
    print(f"Generated {len(DIAGRAMS)} diagrams x {len(THEMES)} variants into {OUT}")


if __name__ == "__main__":
    main()
