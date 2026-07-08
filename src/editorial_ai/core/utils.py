"""Small shared utilities used across modules."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    """Return an ISO timestamp suitable for audit logs and SQLite records."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def stable_id(*parts: str, prefix: str = "id") -> str:
    """Build a deterministic compact id from business keys."""
    raw = "|".join(part.strip().lower() for part in parts if part)
    digest = sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def ensure_parent(path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def to_jsonable(value: Any) -> Any:
    """Convert dataclasses and tuples into JSON-friendly structures."""
    if is_dataclass(value):
        return to_jsonable(asdict(value))
    if isinstance(value, dict):
        return {key: to_jsonable(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(inner) for inner in value]
    return value


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, round(float(value), 2)))

