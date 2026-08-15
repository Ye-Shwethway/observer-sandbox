from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any


SOURCE = "slow_personality_plasticity_v1"
LEDGER_PREFIX = "personality_plasticity_v1:"

# V1 deliberately proves one reusable trait channel rather than inventing a broad
# psychology taxonomy. More traits may register semantically explicit channels
# later without changing the authority or long-horizon contract.
TRAIT_EVIDENCE_CHANNELS: dict[str, set[str]] = {
    "disciplined": {
        "completed_deliberate_training",
        "represented_self_regulation_outcome",
        "represented_counter_discipline_outcome",
    },
}
AUTOMATIC_ACTION_EVIDENCE: dict[str, tuple[str, int, str]] = {
    "train": ("disciplined", 1, "completed_deliberate_training"),
}

EVIDENCE_DELTA = 1.0
MIN_EFFECTIVE_EVIDENCE = 14.0
MIN_DISTINCT_DAYS = 14
MIN_HORIZON_DAYS = 21
MAX_OVERLAY = 0.15
OVERLAY_STEP = 0.01
OVERLAY_START_SCORE = 12.0


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _ledger_key(actor_id: str, trait: str) -> str:
    return f"{LEDGER_PREFIX}{actor_id}:{trait}"


def _read_ledger(conn: sqlite3.Connection, actor_id: str, trait: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT value_json FROM runtime_state WHERE key=?",
        (_ledger_key(actor_id, trait),),
    ).fetchone()
    if row is None:
        return None
    value = json.loads(row[0])
    return value if isinstance(value, dict) else None


def _write_ledger(conn: sqlite3.Connection, actor_id: str, trait: str, value: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO runtime_state(key,value_json,updated_at)
        VALUES(?,?,CURRENT_TIMESTAMP)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP
        """,
        (_ledger_key(actor_id, trait), json.dumps(value, ensure_ascii=False, sort_keys=True)),
    )


def _horizon_days(first_sim_time: str | None, ended_sim_time: str) -> int:
    if not first_sim_time:
        return 0
    elapsed = _parse_time(ended_sim_time) - _parse_time(first_sim_time)
    return max(0, int(elapsed.total_seconds() // 86400))


def _same_day_weight(last_day: str | None, day: str) -> float:
    # Personality evidence is intentionally much slower than preference evidence:
    # repeated same-day behavior may be situational, so only the first observation
    # on a day contributes to the long-horizon effective-evidence gate.
    return 0.0 if last_day == day else 1.0


def _overlay_for(
    *,
    score: float,
    effective_evidence: float,
    distinct_days: int,
    horizon_days: int,
) -> float:
    eligible = (
        abs(score) >= MIN_EFFECTIVE_EVIDENCE
        and effective_evidence >= MIN_EFFECTIVE_EVIDENCE
        and distinct_days >= MIN_DISTINCT_DAYS
        and horizon_days >= MIN_HORIZON_DAYS
    )
    if not eligible:
        return 0.0
    magnitude = min(MAX_OVERLAY, max(0.0, (abs(score) - OVERLAY_START_SCORE) * OVERLAY_STEP))
    return round(magnitude if score > 0 else -magnitude, 3)


def record_personality_evidence(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    trait: str,
    valence: int,
    ended_sim_time: str,
    evidence_kind: str,
) -> dict[str, Any]:
    """Record one semantically registered signed personality evidence item.

    Personality is the slowest-plastic disposition layer. This API cannot create
    arbitrary traits or evidence channels, and a single observation can never
    change cognition-visible personality. Negative evidence must be produced by
    an explicit represented outcome contract rather than inferred from omission.
    """
    trait = trait.strip().lower()
    evidence_kind = evidence_kind.strip()
    if trait not in TRAIT_EVIDENCE_CHANNELS:
        raise ValueError(f"unregistered personality trait evidence channel: {trait}")
    if evidence_kind not in TRAIT_EVIDENCE_CHANNELS[trait]:
        raise ValueError(f"unregistered evidence kind for {trait}: {evidence_kind}")
    if valence not in (-1, 1):
        raise ValueError("valence must be -1 or 1")

    day = _parse_time(ended_sim_time).date().isoformat()
    ledger = _read_ledger(conn, actor_id, trait) or {
        "source": SOURCE,
        "trait": trait,
        "signed_score": 0.0,
        "evidence_count": 0,
        "effective_evidence": 0.0,
        "distinct_evidence_days": 0,
        "first_evidence_sim_time": ended_sim_time,
        "last_evidence_sim_time": None,
        "last_evidence_day": None,
        "positive_evidence": 0,
        "negative_evidence": 0,
        "overlay": 0.0,
    }

    weight = _same_day_weight(ledger.get("last_evidence_day"), day)
    before_score = float(ledger.get("signed_score", 0.0))
    after_score = max(-100.0, min(100.0, round(before_score + valence * EVIDENCE_DELTA * weight, 3)))
    distinct_days = int(ledger.get("distinct_evidence_days", 0)) + (1 if weight > 0 else 0)
    effective = round(float(ledger.get("effective_evidence", 0.0)) + weight, 3)
    horizon_days = _horizon_days(str(ledger.get("first_evidence_sim_time") or ended_sim_time), ended_sim_time)
    overlay = _overlay_for(
        score=after_score,
        effective_evidence=effective,
        distinct_days=distinct_days,
        horizon_days=horizon_days,
    )

    ledger.update(
        {
            "signed_score": after_score,
            "evidence_count": int(ledger.get("evidence_count", 0)) + 1,
            "effective_evidence": effective,
            "distinct_evidence_days": distinct_days,
            "last_evidence_sim_time": ended_sim_time,
            "last_evidence_day": day,
            "positive_evidence": int(ledger.get("positive_evidence", 0)) + (1 if valence > 0 else 0),
            "negative_evidence": int(ledger.get("negative_evidence", 0)) + (1 if valence < 0 else 0),
            "last_evidence_kind": evidence_kind,
            "horizon_days": horizon_days,
            "overlay": overlay,
        }
    )
    _write_ledger(conn, actor_id, trait, ledger)

    return {
        "source": SOURCE,
        "trait": trait,
        "score_before": before_score,
        "score_after": after_score,
        "daily_weight": weight,
        "effective_evidence": effective,
        "distinct_evidence_days": distinct_days,
        "horizon_days": horizon_days,
        "overlay": overlay,
        "status": "adapted" if overlay != 0.0 else "baseline",
    }


def settle_personality_plasticity(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    action_name: str,
    ended_sim_time: str,
) -> dict[str, Any] | None:
    """Extract only explicitly registered automatic evidence from completion."""
    mapping = AUTOMATIC_ACTION_EVIDENCE.get(action_name)
    if mapping is None:
        return None
    trait, valence, evidence_kind = mapping
    return record_personality_evidence(
        conn,
        actor_id,
        trait=trait,
        valence=valence,
        ended_sim_time=ended_sim_time,
        evidence_kind=evidence_kind,
    )


def personality_plasticity_state(conn: sqlite3.Connection, actor_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT key,value_json FROM runtime_state WHERE key LIKE ? ORDER BY key",
        (f"{LEDGER_PREFIX}{actor_id}:%",),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        item = json.loads(row["value_json"])
        if isinstance(item, dict):
            result.append(item)
    return result


def personality_plasticity_context(conn: sqlite3.Connection, actor_id: str) -> list[dict[str, Any]]:
    """Return compact established overlays only; never expose evidence ledgers."""
    context: list[dict[str, Any]] = []
    for item in personality_plasticity_state(conn, actor_id):
        overlay = float(item.get("overlay", 0.0))
        if overlay == 0.0:
            continue
        context.append(
            {
                "trait": str(item["trait"]),
                "direction": "strengthened" if overlay > 0 else "softened",
                "magnitude": "slight",
                "overlay": abs(round(overlay, 3)),
            }
        )
    return context
