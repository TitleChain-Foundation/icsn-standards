"""Canonical JSON and hashing for M5 evidence (M5-MATH-001, MATH-CANONICAL-HASH).

Every hash an M5 engine publishes is SHA-256 over the canonical JSON of a
value, so any implementation in any language can recompute it:

- object keys sorted by Unicode code point; no insignificant whitespace;
- non-ASCII characters emitted as UTF-8, not escaped;
- integral numbers emitted as JSON integers (5.0 and 5 are both ``5``) and
  limited to +/-(2**53 - 1) so every language represents them exactly;
- non-integral numbers emitted as plain decimal strings with no exponent,
  using the shortest round-trip digits (0.1 -> "0.1", 1e-7 -> "0.0000001");
- booleans, null, strings and arrays unchanged.

The JavaScript twin is packages/m5-math/canonical.js; both are held to
packages/m5-math/vectors/canonical-hash.vectors.json.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

MAX_SAFE_INTEGER = 2**53 - 1


def _number(value: int | float | Decimal) -> int | str:
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite numbers cannot be canonicalized")
        decimal = Decimal(repr(value))
    elif isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("non-finite numbers cannot be canonicalized")
        decimal = value
    else:
        decimal = Decimal(value)
    if decimal == decimal.to_integral_value():
        integer = int(decimal)
        if abs(integer) > MAX_SAFE_INTEGER:
            raise ValueError("integers must be within +/-(2**53 - 1)")
        return integer
    text = format(decimal.normalize(), "f")
    return text


def canonical_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, (int, float, Decimal)):  # bool handled above
        return _number(value)
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("object keys must be strings")
        return {key: canonical_value(value[key]) for key in value}
    if isinstance(value, (list, tuple)):
        return [canonical_value(item) for item in value]
    raise ValueError(f"cannot canonicalize {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        canonical_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def canonical_sha256(value: Any) -> str:
    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def file_sha256(path: Path) -> str:
    """SHA-256 of a file's exact bytes (reproducible with ``shasum -a 256``)."""
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_utc(value: datetime, label: str) -> datetime:
    """Reject naive datetimes; return the value converted to UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware")
    return value.astimezone(timezone.utc)


def utc_iso(value: datetime) -> str:
    """Canonical evidence time: UTC, whole seconds, ``Z`` suffix."""
    return require_utc(value, "time").strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc(text: str) -> datetime:
    return require_utc(datetime.fromisoformat(text.replace("Z", "+00:00")), "time")
