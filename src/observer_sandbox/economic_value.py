from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
VALUE_PROFILE_PATH = REPO_ROOT / "config" / "economy" / "value_profiles.v1.json"
VALID_CLASSIFICATIONS = {
    "standalone_asset",
    "component",
    "consumable_stock",
    "resource_proxy",
    "economically_immaterial",
}
VALID_NET_WORTH_TREATMENTS = {"independent", "included_in_parent", "derived_stock", "excluded"}


def load_value_profiles(path: str | Path = VALUE_PROFILE_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _json(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, sort_keys=True, separators=(",", ":"))


def _upsert_profile(
    conn: sqlite3.Connection,
    *,
    subject_type: str,
    raw: dict[str, Any],
    default_currency: str,
    parent_asset_id: str | None,
    revision: str,
) -> None:
    subject_id = str(raw.get("subject_id") or "").strip()
    if not subject_id:
        raise ValueError("economic value profile requires subject_id")
    classification = str(raw.get("classification") or "").strip()
    if classification not in VALID_CLASSIFICATIONS:
        raise ValueError(f"unsupported economic value classification: {classification}")
    treatment = str(raw.get("net_worth_treatment") or "").strip()
    if treatment not in VALID_NET_WORTH_TREATMENTS:
        raise ValueError(f"unsupported net_worth_treatment: {treatment}")
    if subject_type == "entity":
        if conn.execute("SELECT 1 FROM entities WHERE id=?", (subject_id,)).fetchone() is None:
            raise ValueError(f"economic value profile references unknown entity: {subject_id}")
    elif subject_type == "entity_definition":
        if conn.execute("SELECT 1 FROM entity_definitions WHERE id=?", (subject_id,)).fetchone() is None:
            raise ValueError(f"economic value profile references unknown definition: {subject_id}")
    else:
        raise ValueError(f"unsupported profile subject_type: {subject_type}")

    included_in_asset_id = raw.get("included_in_asset_id")
    if treatment == "included_in_parent":
        included_in_asset_id = included_in_asset_id or parent_asset_id
        if not included_in_asset_id:
            raise ValueError(f"included_in_parent profile requires asset: {subject_id}")
    if included_in_asset_id is not None and conn.execute(
        "SELECT 1 FROM economic_assets WHERE asset_id=?", (str(included_in_asset_id),)
    ).fetchone() is None:
        raise ValueError(f"unknown included parent asset: {included_in_asset_id}")

    currency_code = raw.get("currency_code") or default_currency
    if classification in {"resource_proxy", "economically_immaterial"} and not any(
        raw.get(key) is not None for key in ("market_value_minor", "replacement_value_minor", "unit_value_minor")
    ):
        currency_code = raw.get("currency_code")

    conn.execute(
        """
        INSERT INTO economic_value_profiles(
            subject_type,subject_id,classification,currency_code,market_value_minor,
            replacement_value_minor,unit_value_minor,unit_quantity,unit_label,
            net_worth_treatment,included_in_asset_id,valuation_method,rule_key,
            provenance_json,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(subject_type,subject_id) DO UPDATE SET
            classification=excluded.classification,
            currency_code=excluded.currency_code,
            market_value_minor=excluded.market_value_minor,
            replacement_value_minor=excluded.replacement_value_minor,
            unit_value_minor=excluded.unit_value_minor,
            unit_quantity=excluded.unit_quantity,
            unit_label=excluded.unit_label,
            net_worth_treatment=excluded.net_worth_treatment,
            included_in_asset_id=excluded.included_in_asset_id,
            valuation_method=excluded.valuation_method,
            rule_key=excluded.rule_key,
            provenance_json=excluded.provenance_json,
            metadata_json=excluded.metadata_json,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            subject_type,
            subject_id,
            classification,
            currency_code,
            raw.get("market_value_minor"),
            raw.get("replacement_value_minor"),
            raw.get("unit_value_minor"),
            raw.get("unit_quantity"),
            raw.get("unit_label"),
            treatment,
            included_in_asset_id,
            str(raw.get("valuation_method") or "explicit_policy"),
            str(raw.get("rule_key") or revision),
            _json({"source": revision, "authority": "creator-approved W3.1 value policy"}),
            _json(raw.get("metadata")),
        ),
    )


def seed_economic_value_profiles(
    conn: sqlite3.Connection, path: str | Path = VALUE_PROFILE_PATH
) -> None:
    source = load_value_profiles(path)
    revision = str(source["revision"])
    currency = str(source.get("currency_code") or "USD")
    parent_asset_id = source.get("parent_asset_id")
    for raw in source.get("entity_profiles", []):
        _upsert_profile(
            conn,
            subject_type="entity",
            raw=dict(raw),
            default_currency=currency,
            parent_asset_id=None if parent_asset_id is None else str(parent_asset_id),
            revision=revision,
        )
    for raw in source.get("definition_profiles", []):
        _upsert_profile(
            conn,
            subject_type="entity_definition",
            raw=dict(raw),
            default_currency=currency,
            parent_asset_id=None,
            revision=revision,
        )
    conn.execute(
        """INSERT INTO runtime_state(key,value_json) VALUES('economic_value_profile_revision',?)
           ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP""",
        (json.dumps(revision),),
    )
    conn.commit()


def value_profile(conn: sqlite3.Connection, subject_type: str, subject_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT * FROM economic_value_profiles WHERE subject_type=? AND subject_id=?",
        (subject_type, subject_id),
    ).fetchone()
    if row is None:
        raise ValueError(f"missing economic value policy: {subject_type}:{subject_id}")
    result = dict(row)
    result["provenance"] = json.loads(result.pop("provenance_json"))
    result["metadata"] = json.loads(result.pop("metadata_json"))
    return result


def inventory_stack_value_minor(conn: sqlite3.Connection, stack_id: str) -> int:
    row = conn.execute(
        """SELECT s.quantity,s.unit,e.definition_id
           FROM inventory_stacks s JOIN entities e ON e.id=s.entity_id
           WHERE s.entity_id=?""",
        (stack_id,),
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown inventory stack: {stack_id}")
    profile = value_profile(conn, "entity_definition", str(row["definition_id"]))
    if profile["classification"] != "consumable_stock" or profile["unit_value_minor"] is None:
        raise ValueError(f"inventory definition lacks consumable stock unit value: {row['definition_id']}")
    unit_label = str(profile["unit_label"] or "")
    if unit_label != str(row["unit"]):
        raise ValueError(
            f"economic unit {unit_label} does not match inventory unit {row['unit']} for {stack_id}"
        )
    unit_quantity = float(profile["unit_quantity"] or 1.0)
    return int(round(float(row["quantity"]) / unit_quantity * int(profile["unit_value_minor"])))


def estate_inventory_stock_value_minor(conn: sqlite3.Connection) -> int:
    rows = conn.execute("SELECT entity_id FROM inventory_stacks WHERE quantity > 0 ORDER BY entity_id").fetchall()
    return sum(inventory_stack_value_minor(conn, str(row["entity_id"])) for row in rows)


def validate_current_value_coverage(conn: sqlite3.Connection) -> None:
    """Fail closed when a represented world object or item definition lacks value policy.

    This is the creation-rule socket for current seed paths: adding a new object to
    a world seed or a new item definition requires an explicit economic policy in
    the same development slice. Runtime-created object APIs should call
    require_entity_value_policy before committing newly represented objects.
    """
    object_rows = conn.execute("SELECT id FROM entities WHERE entity_type='object' ORDER BY id").fetchall()
    missing_objects = [
        str(row["id"])
        for row in object_rows
        if conn.execute(
            "SELECT 1 FROM economic_value_profiles WHERE subject_type='entity' AND subject_id=?",
            (str(row["id"]),),
        ).fetchone()
        is None
    ]
    definition_rows = conn.execute(
        "SELECT id FROM entity_definitions WHERE entity_type='item' ORDER BY id"
    ).fetchall()
    missing_definitions = [
        str(row["id"])
        for row in definition_rows
        if conn.execute(
            "SELECT 1 FROM economic_value_profiles WHERE subject_type='entity_definition' AND subject_id=?",
            (str(row["id"]),),
        ).fetchone()
        is None
    ]
    if missing_objects or missing_definitions:
        parts: list[str] = []
        if missing_objects:
            parts.append("objects=" + ",".join(missing_objects))
        if missing_definitions:
            parts.append("item_definitions=" + ",".join(missing_definitions))
        raise ValueError("missing economic value policy coverage: " + "; ".join(parts))


def require_entity_value_policy(conn: sqlite3.Connection, entity_id: str) -> dict[str, Any]:
    return value_profile(conn, "entity", entity_id)
