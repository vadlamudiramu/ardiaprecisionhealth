"""PHI-free audit trail — HIPAA §164.312(b) technical safeguard (scaffold).

Records WHO / WHAT / WHEN metadata for every guarded AI action — the model, the
action, the COUNTS of identifiers de-identified, pass/fail, and a hash of the
already-de-identified text for correlation — and NEVER the content itself.

Honest scope: a production audit control must write to a durable, access-controlled,
tamper-evident store with retention and review procedures. This module emits
structured events (an in-memory ring + optional sinks) so the accountability control
is demonstrable and testable rather than merely described. Point ``add_sink`` at a
real append-only store for production.

Defense-in-depth: even though callers are expected to pass only metadata, every
string value is length-capped so a raw content string can never be logged by mistake.
"""
from __future__ import annotations

import itertools
import time
from collections import deque

_seq = itertools.count(1)
_RING: deque = deque(maxlen=2000)     # recent events (metadata only)
_SINKS: list = []                     # optional callables(event: dict) -> None

_MAX_STR = 64                         # any string metadata longer than this is dropped (content guard)
_MAX_LIST = 32


def add_sink(fn) -> None:
    """Register a durable sink, e.g. append-to-file or a WORM store."""
    _SINKS.append(fn)


def _safe(v):
    """Allow only short, PHI-free primitives; drop anything that could carry content."""
    if isinstance(v, bool) or isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        return None if len(v) > _MAX_STR else v
    if isinstance(v, list):
        out = [_safe(x) for x in v[:_MAX_LIST]]
        return [x for x in out if x is not None]
    return None


def record(action: str, *, model: str = "", deid: dict | None = None, extra: dict | None = None) -> str:
    """Append a PHI-free audit event. Returns the event id."""
    eid = "evt_%d_%d" % (int(time.time()), next(_seq))
    ev = {"id": eid, "ts": round(time.time(), 3), "action": str(action)[:_MAX_STR], "model": (model or "")[:_MAX_STR]}
    if deid:
        ev["deid"] = {"removed": int(deid.get("removed", 0) or 0),
                      "categories": [str(c)[:_MAX_STR] for c in (deid.get("categories") or [])][:_MAX_LIST]}
    if extra:
        meta = {}
        for k, v in extra.items():
            sv = _safe(v)
            if sv is not None:
                meta[str(k)[:_MAX_STR]] = sv
        if meta:
            ev["meta"] = meta
    _RING.append(ev)
    for s in _SINKS:
        try:
            s(ev)
        except Exception:
            pass   # a failing sink must never break the guarded call (and never leak why)
    return eid


def recent(n: int = 50) -> list:
    """Return the most recent audit events (metadata only)."""
    return list(_RING)[-n:]


def clear() -> None:
    """Test helper — reset the in-memory ring."""
    _RING.clear()
