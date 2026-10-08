#!/usr/bin/env python3
"""Generate data-driven charts from impl/results/*.json, in the house style.

Usage:  python3 tools/generate_charts.py
Outputs images/diagrams/chart-*-{light,dark}.svg
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from generate_diagrams import SVG, THEMES, OUT  # noqa: E402

RESULTS = ROOT / "impl" / "results"


class Plot:
    """Minimal cartesian plotting on top of the SVG kit."""

    def __init__(self, s: SVG, x0, y0, w, h, xlim, ylim,
                 xlog=False, ylog=False):
        self.s, self.x0, self.y0, self.w, self.h = s, x0, y0, w, h
        self.xlim, self.ylim, self.xlog, self.ylog = xlim, ylim, xlog, ylog
        t = s.t
        s.parts.append(
            f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" '
            f'fill="url(#gCard)" stroke="{t["card_stroke"]}" stroke-width="1.2"/>')

    def _tx(self, x):
        a, b = self.xlim
        if self.xlog:
            x, a, b = math.log10(max(x, 1e-12)), math.log10(a), math.log10(b)
        return self.x0 + (x - a) / (b - a) * self.w

    def _ty(self, y):
        a, b = self.ylim
        if self.ylog:
            y, a, b = math.log10(max(y, 1e-12)), math.log10(a), math.log10(b)
        return self.y0 + self.h - (y - a) / (b - a) * self.h

    def grid(self, xticks, yticks, xfmt=str, yfmt=str, xlabel="", ylabel=""):
        t = self.s.t
        for x in xticks:
            px = self._tx(x)
            self.s.parts.append(
                f'<line x1="{px:.1f}" y1="{self.y0}" x2="{px:.1f}" '
                f'y2="{self.y0+self.h}" stroke="{t["card_stroke"]}" '
                f'stroke-width="0.8" stroke-dasharray="3 4"/>')
            self.s.text(px, self.y0 + self.h + 18, xfmt(x), 10.5, t["muted"])
        for y in yticks:
            py = self._ty(y)
            self.s.parts.append(
                f'<line x1="{self.x0}" y1="{py:.1f}" x2="{self.x0+self.w}" '
                f'y2="{py:.1f}" stroke="{t["card_stroke"]}" stroke-width="0.8" '
                f'stroke-dasharray="3 4"/>')
            self.s.text(self.x0 - 10, py + 4, yfmt(y), 10.5, t["muted"],
                        anchor="end")
        if xlabel:
            self.s.text(self.x0 + self.w / 2, self.y0 + self.h + 40, xlabel,
                        11.5, t["muted"])
        if ylabel:
            self.s.parts.append(
                f'<text x="{self.x0-46}" y="{self.y0+self.h/2}" font-size="11.5" '
                f'fill="{t["muted"]}" text-anchor="middle" '
                f'transform="rotate(-90 {self.x0-46} {self.y0+self.h/2})">'
                f'{ylabel}</text>')

    def line(self, pts, color, width=2.6, dots=True, dash=False):
        d = " ".join(("M" if i == 0 else "L") +
                     f"{self._tx(x):.1f} {self._ty(y):.1f}"
                     for i, (x, y) in enumerate(pts))
        da = ' stroke-dasharray="7 5"' if dash else ""
        self.s.parts.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{da}/>')
        if dots:
            for x, y in pts:
                self.s.parts.append(
                    f'<circle cx="{self._tx(x):.1f}" cy="{self._ty(y):.1f}" '
                    f'r="3.4" fill="{color}"/>')

    def legend(self, items, x, y):
        for i, (color, label, dash) in enumerate(items):
            yy = y + i * 20
            da = ' stroke-dasharray="7 5"' if dash else ""
            self.s.parts.append(
                f'<line x1="{x}" y1="{yy}" x2="{x+26}" y2="{yy}" '
                f'stroke="{color}" stroke-width="2.8" stroke-linecap="round"{da}/>')
            self.s.text(x + 34, yy + 4, label, 11.5, self.s.t["text"],
                        anchor="start")


def lime(t, v):
    return "#7a9900" if v == "light" else "#cfff04"


def red(t):
    return t["red_stroke"]


# ---------------------------------------------------------------- charts

def chart_frontier(data, t, v):
    s = SVG("chart-frontier", 900, 460, t, v,
            eyebrow="THE DECLASSIFICATION FRONTIER",
            title="What path-awareness costs, and what verification buys back")
    p = Plot(s, 96, 104, 660, 264, (0, 46), (0, 105))
    p.grid([0, 10, 20, 30, 40], [0, 25, 50, 75, 100],
           xfmt=lambda x: f"{x}%", yfmt=lambda y: f"{y}%",
           xlabel="legitimate work refused (false-rejection rate)",
           ylabel="attacks blocked")
    unver = [(r["false_rejection_rate"] * 100, r["detection_rate"] * 100)
             for r in data["frontier"]]
    ver = [(r["false_rejection_rate"] * 100, r["detection_rate"] * 100)
           for r in data["frontier_verified"]]
    p.line(unver, red(t), dash=True)
    p.line(ver, lime(t, v))
    p.legend([(lime(t, v), "verified declassification", False),
              (red(t), "unverified (monitor cannot tell)", True)], 470, 130)
    s.text(450, 424, "unverified trades 1.6 points of detection for every point of "
           "relief; verified moves the whole frontier", 12, t["muted"])
    s.save()


def chart_scaling(data, t, v):
    s = SVG("chart-scaling", 900, 440, t, v,
            eyebrow="PATH-LENGTH SCALING",
            title="Bounded summary stays flat; re-reading history does not")
    p = Plot(s, 96, 104, 660, 250, (10, 50000), (0.1, 50000),
             xlog=True, ylog=True)
    p.grid([10, 100, 1000, 10000, 50000], [0.1, 1, 10, 100, 1000, 10000],
           xfmt=lambda x: f"{x:,}",
           yfmt=lambda y: (f"{y:g}" if y >= 1 else "0.1"),
           xlabel="steps taken so far", ylabel="microseconds per decision")
    rows = data["e2_scaling_deep"]
    p.line([(r["path_length"], r["bounded_us"]) for r in rows], lime(t, v))
    p.line([(r["path_length"], r["naive_us"]) for r in rows], red(t), dash=True)
    p.legend([(lime(t, v), "bounded summary", False),
              (red(t), "re-read the whole path", True)], 430, 280)
    # budget line
    py = p._ty(15000)
    s.parts.append(
        f'<line x1="{p.x0}" y1="{py:.1f}" x2="{p.x0+p.w}" y2="{py:.1f}" '
        f'stroke="{t["muted"]}" stroke-width="1.5" stroke-dasharray="9 6"/>')
    s.text(p.x0 + p.w - 6, py - 8, "15 ms budget", 10.5, t["muted"], anchor="end")
    s.text(450, 408, "at 50,000 steps the naive monitor needs 34 ms per decision; "
           "the bounded one needs 0.21 microseconds", 12, t["muted"])
    s.save()


def chart_anchor(data, t, v):
    s = SVG("chart-anchor", 900, 440, t, v,
            eyebrow="THE ANCHORING INTERVAL",
            title="How much history you can hide, versus what publishing costs")
    rows = data["e3_anchoring"]["rows"]
    p = Plot(s, 110, 104, 640, 250, (0.001, 3600), (1, 2e7),
             xlog=True, ylog=True)
    p.grid([0.001, 0.1, 1, 60, 3600], [1, 100, 10000, 1000000],
           xfmt=lambda x: ("1ms" if x == 0.001 else "100ms" if x == 0.1 else
                           "1s" if x == 1 else "1min" if x == 60 else "1h"),
           yfmt=lambda y: (f"{int(y):,}" if y < 10000 else
                           f"{int(y/1000):,}k" if y < 1e6 else "1M+"),
           xlabel="anchoring interval Δ", ylabel="actions inside the blind window")
    p.line([(r["delta_s"], max(r["exposure_actions"], 1)) for r in rows],
           lime(t, v))
    # overhead annotation
    for r, lab, dx, dy, anc in ((rows[0], "8.6% overhead", 12, 20, "start"),
                                (rows[3], "0.009%", 12, 20, "start"),
                                (rows[6], "0.0000024%", -12, 22, "end")):
        px, py = p._tx(r["delta_s"]), p._ty(max(r["exposure_actions"], 1))
        s.text(px + dx, py + dy, lab, 10, t["muted"], anchor=anc)
    s.text(p.x0 + 8, p.y0 + 18, "publishing overhead shown at three points",
           10, t["faint"], anchor="start")
    s.text(450, 408, "exposure and cost are exactly inverse: pick the window you "
           "can afford to lose", 12, t["muted"])
    s.save()


def chart_batch(data, t, v):
    s = SVG("chart-batch", 900, 440, t, v,
            eyebrow="BATCH SIGNING",
            title="Signing one root per N actions removes the dominant cost")
    rows = data["e4_batch_signing"]["rows"]
    p = Plot(s, 110, 104, 640, 250, (1, 128), (1, 1e6), xlog=True, ylog=True)
    p.grid([1, 2, 8, 32, 128], [10, 1000, 100000, 1000000],
           xfmt=lambda x: str(int(x)),
           yfmt=lambda y: (f"{int(y):,}" if y < 1e6 else "1M"),
           xlabel="actions per signature", ylabel="actions per second")
    p.line([(r["batch"], r["steps_per_s"]) for r in rows], lime(t, v))
    p.line([(r["batch"], max(r["worst_case_unsigned_delay_us"], 1)) for r in rows],
           red(t), dash=True)
    p.legend([(lime(t, v), "throughput (actions/s)", False),
              (red(t), "worst-case delay before signing (us)", True)], 330, 306)
    s.text(450, 408, "batching 128 actions is 61x cheaper per action and leaves "
           "them unsigned for at most 180 microseconds", 12, t["muted"])
    s.save()


def chart_retention(data, t, v):
    s = SVG("chart-retention", 900, 430, t, v,
            eyebrow="WHAT KEEPING THE EVIDENCE COSTS",
            title="A 1,000-agent fleet, 100 actions each per day")
    rows = data["e5_retention"]["rows"]
    p = Plot(s, 110, 104, 640, 244, (1, 10), (0, 4))
    p.grid([1, 3, 5, 7, 10], [0, 1, 2, 3, 4],
           xfmt=lambda x: f"{int(x)}y", yfmt=lambda y: f"{int(y)} TB",
           xlabel="retention period", ylabel="stored evidence")
    p.line([(r["years"], r["Ed25519"]) for r in rows], t["muted"])
    p.line([(r["years"], r["ML-DSA-44"]) for r in rows], lime(t, v))
    p.line([(r["years"], r["Hybrid"]) for r in rows], red(t), dash=True)
    p.legend([(t["muted"], "Ed25519 (classical)", False),
              (lime(t, v), "ML-DSA-44 (post-quantum)", False),
              (red(t), "hybrid", True)], 150, 130)
    s.text(450, 400, "seven years of post-quantum evidence for the whole fleet is "
           "2.65 TB — the 38x multiplier is affordable", 12, t["muted"])
    s.save()


def chart_merkle(data, t, v):
    s = SVG("chart-merkle", 900, 476, t, v,
            eyebrow="CHECKING ONE RECORD",
            title="What an auditor must download to verify a single action")
    rows = data["m1_inclusion"]
    p = Plot(s, 110, 104, 640, 258, (10, 100000), (100, 2e8),
             xlog=True, ylog=True)
    p.grid([10, 100, 1000, 10000, 100000],
           [100, 10000, 1000000, 100000000],
           xfmt=lambda x: f"{int(x):,}",
           yfmt=lambda y: ("100 B" if y == 100 else "10 kB" if y == 1e4 else
                           "1 MB" if y == 1e6 else "100 MB"),
           xlabel="records in the log",
           ylabel="bytes fetched to check one record")
    p.line([(r["n"], r["bytes_fetched_chain"]) for r in rows], red(t), dash=True)
    p.line([(r["n"], r["bytes_fetched_tree"]) for r in rows], lime(t, v))
    p.legend([(lime(t, v), "inclusion proof (Merkle tree)", False),
              (red(t), "replay the whole chain", True)], 150, 132)
    last = rows[-1]
    px, py = p._tx(last["n"]), p._ty(last["bytes_fetched_chain"])
    s.text(px - 10, py - 10, f"{last['bytes_fetched_chain']/1e6:.0f} MB",
           10.5, t["muted"], anchor="end")
    px, py = p._tx(last["n"]), p._ty(last["bytes_fetched_tree"])
    s.text(px - 10, py + 20, f"{last['bytes_fetched_tree']:,} B",
           10.5, t["muted"], anchor="end")
    s.text(450, 430, "at 100,000 records the chain costs 123 MB and the proof "
           "costs 1.8 kB - a 69,000-fold difference", 12, t["muted"])
    s.text(450, 450, "the gap widens with every record added, because one line "
           "is linear and the other is logarithmic", 11, t["faint"])
    s.save()


def main():
    frontier = json.loads((RESULTS / "frontier.json").read_text())
    ops = json.loads((RESULTS / "ops.json").read_text())
    merkle = json.loads((RESULTS / "merkle.json").read_text())
    n = 0
    for variant, theme in THEMES.items():
        chart_frontier(frontier, theme, variant)
        chart_scaling(ops, theme, variant)
        chart_anchor(ops, theme, variant)
        chart_batch(ops, theme, variant)
        chart_retention(ops, theme, variant)
        chart_merkle(merkle, theme, variant)
        n += 6
    print(f"generated {n} chart files into {OUT}")


if __name__ == "__main__":
    main()
