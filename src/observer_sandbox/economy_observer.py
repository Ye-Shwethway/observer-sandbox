from __future__ import annotations

import json
import sqlite3
from typing import Any

from .economic_value import value_profile
from .economy import economic_net_worth


def _latest_valuation(
    conn: sqlite3.Connection,
    *,
    subject_type: str,
    subject_id: str,
    currency_code: str,
) -> dict[str, Any] | None:
    row = conn.execute(
        """SELECT amount_minor,currency_code,valuation_sim_time,method,source_type,source_id
           FROM economic_valuations
           WHERE subject_type=? AND subject_id=? AND currency_code=?
           ORDER BY CASE WHEN valuation_sim_time IS NULL THEN 1 ELSE 0 END,
                    valuation_sim_time DESC, created_at DESC, valuation_id DESC
           LIMIT 1""",
        (subject_type, subject_id, currency_code),
    ).fetchone()
    return None if row is None else dict(row)


def character_economy_summary(
    conn: sqlite3.Connection,
    character_id: str,
    *,
    currency_code: str = "USD",
) -> dict[str, Any]:
    character = conn.execute(
        "SELECT id,name FROM entities WHERE id=? AND entity_type='character'",
        (character_id,),
    ).fetchone()
    if character is None:
        raise KeyError(f"Unknown character: {character_id}")
    economic = conn.execute(
        "SELECT * FROM economic_entities WHERE represented_entity_id=? AND status='active'",
        (character_id,),
    ).fetchone()
    if economic is None:
        raise KeyError(f"Character has no represented economy: {character_id}")
    economic_entity_id = str(economic["economic_entity_id"])

    account_rows = conn.execute(
        """SELECT account_id,account_type,currency_code,balance_minor,status,metadata_json
           FROM financial_accounts
           WHERE owner_economic_entity_id=? AND status<>'closed'
           ORDER BY account_type,account_id""",
        (economic_entity_id,),
    ).fetchall()
    accounts: list[dict[str, Any]] = []
    for row in account_rows:
        item = dict(row)
        item["metadata"] = json.loads(item.pop("metadata_json"))
        accounts.append(item)

    asset_rows = conn.execute(
        """SELECT asset_id,asset_type,represented_entity_id,quantity,status,metadata_json
           FROM economic_assets
           WHERE owner_economic_entity_id=? AND status='active'
           ORDER BY asset_type,asset_id""",
        (economic_entity_id,),
    ).fetchall()
    assets: list[dict[str, Any]] = []
    for row in asset_rows:
        item = dict(row)
        item["metadata"] = json.loads(item.pop("metadata_json"))
        item["valuation"] = _latest_valuation(
            conn,
            subject_type="asset",
            subject_id=str(item["asset_id"]),
            currency_code=currency_code,
        )
        represented_id = item.get("represented_entity_id")
        if represented_id:
            represented = conn.execute("SELECT name FROM entities WHERE id=?", (represented_id,)).fetchone()
            item["represented_name"] = None if represented is None else str(represented["name"])
        assets.append(item)

    liability_rows = conn.execute(
        """SELECT liability_id,liability_type,outstanding_minor,currency_code,due_sim_time,status,metadata_json
           FROM economic_liabilities
           WHERE debtor_economic_entity_id=? AND status='active'
           ORDER BY liability_type,liability_id""",
        (economic_entity_id,),
    ).fetchall()
    liabilities: list[dict[str, Any]] = []
    for row in liability_rows:
        item = dict(row)
        item["metadata"] = json.loads(item.pop("metadata_json"))
        liabilities.append(item)

    return {
        "character": {"id": str(character["id"]), "name": str(character["name"])},
        "economic_entity": {
            "id": economic_entity_id,
            "display_name": str(economic["display_name"]),
            "entity_type": str(economic["entity_type"]),
        },
        "currency_code": currency_code,
        "net_worth_minor": economic_net_worth(conn, economic_entity_id, currency_code=currency_code),
        "accounts": accounts,
        "assets": assets,
        "liabilities": liabilities,
    }


def represented_asset_summary(
    conn: sqlite3.Connection,
    represented_entity_id: str,
    *,
    currency_code: str = "USD",
) -> dict[str, Any] | None:
    row = conn.execute(
        """SELECT a.asset_id,a.asset_type,a.owner_economic_entity_id,e.display_name AS owner_name
           FROM economic_assets a
           JOIN economic_entities e ON e.economic_entity_id=a.owner_economic_entity_id
           WHERE a.represented_entity_id=? AND a.status='active'
           ORDER BY a.asset_id LIMIT 1""",
        (represented_entity_id,),
    ).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["valuation"] = _latest_valuation(
        conn,
        subject_type="asset",
        subject_id=str(row["asset_id"]),
        currency_code=currency_code,
    )
    return result


def entity_economic_value(conn: sqlite3.Connection, entity_id: str) -> dict[str, Any] | None:
    try:
        profile = value_profile(conn, "entity", entity_id)
    except ValueError:
        return None
    parent_asset = None
    parent_asset_id = profile.get("included_in_asset_id")
    if parent_asset_id:
        row = conn.execute(
            "SELECT asset_id,asset_type,represented_entity_id FROM economic_assets WHERE asset_id=?",
            (str(parent_asset_id),),
        ).fetchone()
        if row is not None:
            parent_asset = dict(row)
            represented_id = parent_asset.get("represented_entity_id")
            if represented_id:
                entity = conn.execute("SELECT name FROM entities WHERE id=?", (represented_id,)).fetchone()
                parent_asset["represented_name"] = None if entity is None else str(entity["name"])
    return {**profile, "parent_asset": parent_asset}
