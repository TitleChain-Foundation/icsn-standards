"""Nash M5Score: deterministic, integer-only reference implementation.

M5-MATH-001 entries MATH-NASH-DECAY, MATH-NASH-COMPONENT and
MATH-NASH-COMPOSITE. Weights and constants live in
packages/m5-math/nash-weights.json; the JavaScript twin is
packages/m5-math/nash-score.js and both are held to
packages/m5-math/vectors/nash-score.vectors.json.

    weight(d)  = Q32 power of the published daily factor for the signal's
                 half-life (30 days good, 180 days bad), flooring after
                 every multiplication
    component  = floor(scale * (G + alpha*Q) / (G + B + (alpha+beta)*Q))
                 where G, B are the summed decay weights of good and bad
                 signals (a component with no signals scores 500)
    m5score    = floor(sum(weight_bps[c] * component[c]) / 10000)

Roles: NASH is the scoring agent, GREEN computes and records the score,
PAINE checks holder notes before they become signals.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from core.m5_canonical import canonical_sha256, file_sha256, parse_utc, require_utc, utc_iso

WEIGHTS_PATH = (
    Path(__file__).resolve().parents[1] / "packages" / "m5-math" / "nash-weights.json"
)
COMPONENTS = (
    "settlement_reliability",
    "attestation_integrity",
    "information_symmetry",
    "reciprocity",
    "externality",
    "governance_participation",
)
POLARITIES = ("GOOD", "BAD")
Q_BITS = 32
Q = 1 << Q_BITS
SECONDS_PER_DAY = 86_400


class NashScoreError(ValueError):
    """Raised when a Nash input or rule is invalid."""


@dataclass(frozen=True)
class NashSignal:
    subject: str
    component: str
    polarity: str
    at: datetime
    source_ref: str

    def as_record(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "component": self.component,
            "polarity": self.polarity,
            "at": utc_iso(self.at),
            "source_ref": self.source_ref,
        }


def load_weights(path: Path = WEIGHTS_PATH) -> dict[str, Any]:
    weights = json.loads(path.read_text(encoding="utf-8"))
    validate_weights(weights)
    return weights


def validate_weights(weights: Mapping[str, Any]) -> None:
    bps = weights["weights_bps"]
    if set(bps) != set(COMPONENTS):
        raise NashScoreError("weights must cover exactly the six Nash components")
    if any(not isinstance(value, int) or value < 0 for value in bps.values()):
        raise NashScoreError("weights must be non-negative integers")
    if sum(bps.values()) != 10_000:
        raise NashScoreError("weights must sum to 10000 bps")
    prior = weights["prior"]
    if prior["alpha"] < 1 or prior["beta"] < 1:
        raise NashScoreError("prior alpha and beta must be at least 1")
    decay = weights["decay"]
    if decay["fixed_point_bits"] != Q_BITS:
        raise NashScoreError("decay must use 32-bit fixed point")
    for key in ("positive_half_life_days", "negative_half_life_days"):
        if str(decay[key]) not in decay["daily_factor_q32"]:
            raise NashScoreError(f"missing daily factor for {key}")


def decay_weight(age_days: int, daily_factor_q32: int) -> int:
    """Q32 weight of a signal ``age_days`` old (square-and-multiply, floor)."""
    if age_days < 0:
        raise NashScoreError("signals cannot be in the future")
    result = Q
    base = daily_factor_q32
    exponent = age_days
    while exponent:
        if exponent & 1:
            result = (result * base) >> Q_BITS
        base = (base * base) >> Q_BITS
        exponent >>= 1
    return result


def age_in_days(signal_at: datetime, as_of: datetime) -> int:
    seconds = int(
        (require_utc(as_of, "as_of") - require_utc(signal_at, "signal time")).total_seconds()
    )
    if seconds < 0:
        raise NashScoreError("signals cannot be in the future")
    return seconds // SECONDS_PER_DAY


def component_score(good_q: int, bad_q: int, weights: Mapping[str, Any]) -> int:
    alpha = weights["prior"]["alpha"]
    beta = weights["prior"]["beta"]
    scale = weights["scale"]
    return (scale * (good_q + alpha * Q)) // (good_q + bad_q + (alpha + beta) * Q)


def _validate_signals(signals: Sequence[NashSignal], subject: str) -> None:
    seen = set()
    for signal in signals:
        if signal.subject != subject:
            raise NashScoreError("all signals must belong to the scored subject")
        if signal.component not in COMPONENTS:
            raise NashScoreError(f"unknown component {signal.component}")
        if signal.polarity not in POLARITIES:
            raise NashScoreError(f"unknown polarity {signal.polarity}")
        if not signal.source_ref:
            raise NashScoreError("every signal needs a source_ref")
        key = (signal.source_ref, signal.component)
        if key in seen:
            # One signal per source per component: a single sale cannot be
            # counted twice toward the same component.
            raise NashScoreError(
                f"duplicate signal for {signal.source_ref} / {signal.component}"
            )
        seen.add(key)


def compute_m5score(
    *,
    subject: str,
    signals: Sequence[NashSignal],
    as_of: datetime,
    weights: Mapping[str, Any] | None = None,
    previous_record_hash: str | None = None,
) -> dict[str, Any]:
    """Compute a subject's M5Score and its auditable score record."""
    weights = weights if weights is not None else load_weights()
    validate_weights(weights)
    _validate_signals(signals, subject)
    decay = weights["decay"]
    factors = {
        "GOOD": decay["daily_factor_q32"][str(decay["positive_half_life_days"])],
        "BAD": decay["daily_factor_q32"][str(decay["negative_half_life_days"])],
    }
    sums = {component: {"GOOD": 0, "BAD": 0} for component in COMPONENTS}
    counts = {component: {"GOOD": 0, "BAD": 0} for component in COMPONENTS}
    for signal in signals:
        weight = decay_weight(age_in_days(signal.at, as_of), factors[signal.polarity])
        sums[signal.component][signal.polarity] += weight
        counts[signal.component][signal.polarity] += 1
    components = {}
    weighted = 0
    for component in COMPONENTS:
        score = component_score(sums[component]["GOOD"], sums[component]["BAD"], weights)
        components[component] = {
            "score": score,
            "weight_bps": weights["weights_bps"][component],
            "good_weight_q32": sums[component]["GOOD"],
            "bad_weight_q32": sums[component]["BAD"],
            "good_signals": counts[component]["GOOD"],
            "bad_signals": counts[component]["BAD"],
        }
        weighted += weights["weights_bps"][component] * score
    m5score = weighted // 10_000
    ordered = sorted(
        (signal.as_record() for signal in signals),
        key=lambda record: (record["at"], record["source_ref"], record["component"]),
    )
    record = {
        "subject": subject,
        "as_of": utc_iso(as_of),
        "m5score": m5score,
        "nash_score_db": f"{m5score // 10}.{m5score % 10}",
        "components": components,
        "weights_version": weights["version"],
        "weights_status": weights["status"],
        "weights_sha256": canonical_sha256(weights),
        "economic_consequences_enabled": weights["economic_consequences_enabled"],
        "trust_tier": None,
        "event_type": "TRIGGERED_REVIEW" if previous_record_hash else "GENESIS",
        "event_authority": "NASH_AGENT",
        "computed_by": weights["roles"]["score_computed_by"],
        "signals": ordered,
        "signals_sha256": canonical_sha256(ordered),
        "previous_record_hash": previous_record_hash,
    }
    record["record_hash"] = canonical_sha256(record)
    return record


# Signals derived from a settlement and the buyer's inputs.


def signals_from_settlement(
    settlement: Mapping[str, Any],
    *,
    seller_subject: str,
    buyer_rating: int | None = None,
    holder_note: Mapping[str, Any] | None = None,
) -> list[NashSignal]:
    """Translate a closed settlement into seller Nash signals.

    - Released with no adjudicated refund, or an adjudicator RELEASE:
      settlement_reliability GOOD.
    - Refund after the non-delivery deadline: settlement_reliability BAD.
    - Adjudicator FULL_REFUND or PARTIAL_REFUND (claim upheld):
      information_symmetry BAD.
    - Seller-approved refunds, cancellations before delivery and claims
      denied by the sale terms: no signal (neutral).
    - Buyer rating 1-5 on a released sale: 4-5 reciprocity GOOD, 1-2 BAD,
      3 neutral.
    - Accepted holder note on a released sale: matches_listing true
      information_symmetry GOOD, false BAD (unless already BAD from an
      upheld claim on the same sale).
    """
    ref = settlement["receipt_id"]
    events = settlement["events"]
    signals: list[NashSignal] = []

    def at(event: Mapping[str, Any]) -> datetime:
        return parse_utc(event["at"])

    closing = events[-1] if events else None
    upheld = next(
        (
            event
            for event in events
            if event["kind"] == "ADJUDICATOR_DECISION"
            and event["decision"] in {"FULL_REFUND", "PARTIAL_REFUND"}
        ),
        None,
    )
    if upheld is not None:
        signals.append(NashSignal(seller_subject, "information_symmetry", "BAD", at(upheld), ref))
    if settlement["state"] == "RELEASED" and upheld is None:
        signals.append(NashSignal(seller_subject, "settlement_reliability", "GOOD", at(closing), ref))
    if closing is not None and closing["kind"] == "NON_DELIVERY_DEADLINE":
        signals.append(NashSignal(seller_subject, "settlement_reliability", "BAD", at(closing), ref))

    if buyer_rating is not None:
        if settlement["state"] != "RELEASED":
            raise NashScoreError("ratings count only on released sales")
        if buyer_rating not in range(1, 6):
            raise NashScoreError("rating must be 1 to 5")
        if buyer_rating >= 4:
            signals.append(NashSignal(seller_subject, "reciprocity", "GOOD", at(closing), ref))
        elif buyer_rating <= 2:
            signals.append(NashSignal(seller_subject, "reciprocity", "BAD", at(closing), ref))

    if holder_note is not None:
        if holder_note["titlechain_record"] != ref:
            raise NashScoreError("holder note is for a different record")
        if holder_note["holder"] != settlement["buyer_account"]:
            raise NashScoreError("holder note must come from the buyer")
        if upheld is None and holder_note["matches_listing"] is not None:
            note_at = parse_utc(holder_note["at"])
            polarity = "GOOD" if holder_note["matches_listing"] else "BAD"
            signals.append(NashSignal(seller_subject, "information_symmetry", polarity, note_at, ref))
    return signals


def attestation_signal(
    *, subject: str, active_business_verified: bool, verified_at: datetime, source_ref: str
) -> NashSignal:
    """Registry verification of an active business: GOOD if active, else BAD."""
    return NashSignal(
        subject,
        "attestation_integrity",
        "GOOD" if active_business_verified else "BAD",
        verified_at,
        source_ref,
    )


def weights_file_sha256() -> str:
    return file_sha256(WEIGHTS_PATH)
