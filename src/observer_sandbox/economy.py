from __future__ import annotations

"""Authoritative economy state for the fictional Observer Sandbox simulation.

No function in this module connects to real banks, payment providers, markets, or
external financial services. Amounts are deterministic in-universe state only.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable

from .world_stimulus import add_stimulus_scope, create_world_stimulus

REPO_ROOT = Path(__file__).resolve().parents[2]
DARIAN_ECONOMY_SEED_PATH = REPO_ROOT / "config" / "economy" / "darian.v1.json"
ECONOMIC_ENTITY_TYPES = {"character", "household", "company", "organization", "government", "trust", "other"}


def _json(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, sort_keys=True, separators=(",", ":"))


def _required(value: str, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name} is required")
    return result


def _currency(value: str) -> str:
    result = _required(value, "currency_code").upper()
    if len(result) != 3 or not result.isalpha():
        raise ValueError("currency_code must be a three-letter code")
    return result


def _minor(value: int, name: str, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer minor-unit amount")
    if value < 0 or (positive and value == 0):
        raise ValueError(f"{name} must be {'positive' if positive else 'non-negative'}")
    return value


def economic_entity(conn: sqlite3.Connection, economic_entity_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM economic_entities WHERE economic_entity_id=?", (economic_entity_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown economic entity: {economic_entity_id}")
    result = dict(row)
    result["provenance"] = json.loads(result.pop("provenance_json"))
    result["metadata"] = json.loads(result.pop("metadata_json"))
    return result


def ensure_economic_entity(conn: sqlite3.Connection, *, economic_entity_id: str, entity_type: str,
                           display_name: str, represented_entity_id: str | None = None,
                           provenance: dict[str, Any] | None = None,
                           metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    if entity_type not in ECONOMIC_ENTITY_TYPES:
        raise ValueError(f"unsupported economic entity_type: {entity_type}")
    if represented_entity_id is not None and conn.execute(
        "SELECT 1 FROM entities WHERE id=?", (represented_entity_id,)
    ).fetchone() is None:
        raise ValueError(f"unknown represented entity: {represented_entity_id}")
    conn.execute(
        """INSERT INTO economic_entities(
               economic_entity_id,represented_entity_id,entity_type,display_name,provenance_json,metadata_json
           ) VALUES(?,?,?,?,?,?)
           ON CONFLICT(economic_entity_id) DO UPDATE SET
             represented_entity_id=excluded.represented_entity_id,
             entity_type=excluded.entity_type,display_name=excluded.display_name,
             provenance_json=excluded.provenance_json,metadata_json=excluded.metadata_json,
             updated_at=CURRENT_TIMESTAMP""",
        (_required(economic_entity_id, "economic_entity_id"), represented_entity_id, entity_type,
         _required(display_name, "display_name"), _json(provenance), _json(metadata)),
    )
    conn.commit()
    return economic_entity(conn, economic_entity_id)


def financial_account(conn: sqlite3.Connection, account_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM financial_accounts WHERE account_id=?", (account_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown financial account: {account_id}")
    result = dict(row)
    result["provenance"] = json.loads(result.pop("provenance_json"))
    result["metadata"] = json.loads(result.pop("metadata_json"))
    result["allow_negative"] = bool(result["allow_negative"])
    return result


def create_financial_account(conn: sqlite3.Connection, *, account_id: str, owner_economic_entity_id: str,
                             account_type: str, currency_code: str, opening_balance_minor: int = 0,
                             allow_negative: bool = False, provenance: dict[str, Any] | None = None,
                             metadata: dict[str, Any] | None = None,
                             opening_sim_time: str = "1970-01-01T00:00:00+00:00") -> dict[str, Any]:
    economic_entity(conn, owner_economic_entity_id)
    opening_balance_minor = _minor(opening_balance_minor, "opening_balance_minor")
    conn.execute(
        """INSERT INTO financial_accounts(
               account_id,owner_economic_entity_id,account_type,currency_code,balance_minor,
               allow_negative,provenance_json,metadata_json
           ) VALUES(?,?,?,?,0,?,?,?)""",
        (_required(account_id, "account_id"), owner_economic_entity_id, _required(account_type, "account_type"),
         _currency(currency_code), 1 if allow_negative else 0, _json(provenance), _json(metadata)),
    )
    conn.commit()
    if opening_balance_minor:
        post_transaction(
            conn, transaction_id=f"opening:{account_id}", transaction_type="opening_balance",
            sim_time=opening_sim_time,
            entries=[{"account_id": account_id, "delta_minor": opening_balance_minor, "memo": "opening balance"}],
            reason="Canonical in-universe opening balance", source_type="economic_seed", source_id=account_id,
            metadata={"boundary_flow": True},
        )
    return financial_account(conn, account_id)


def can_afford(conn: sqlite3.Connection, account_id: str, amount_minor: int) -> bool:
    amount_minor = _minor(amount_minor, "amount_minor")
    account = financial_account(conn, account_id)
    return account["status"] == "active" and int(account["balance_minor"]) >= amount_minor


def post_transaction(conn: sqlite3.Connection, *, transaction_id: str, transaction_type: str, sim_time: str,
                     entries: Iterable[dict[str, Any]], reason: str | None = None,
                     source_type: str | None = None, source_id: str | None = None,
                     source_event_id: int | None = None, provenance: dict[str, Any] | None = None,
                     metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    normalized: list[dict[str, Any]] = []
    for raw in entries:
        account = financial_account(conn, _required(str(raw.get("account_id", "")), "account_id"))
        delta = raw.get("delta_minor")
        if isinstance(delta, bool) or not isinstance(delta, int) or delta == 0:
            raise ValueError("delta_minor must be a non-zero integer minor-unit amount")
        if account["status"] != "active":
            raise ValueError(f"financial account is not active: {account['account_id']}")
        if int(account["balance_minor"]) + delta < 0 and not account["allow_negative"]:
            raise ValueError(f"insufficient funds in {account['account_id']}")
        normalized.append({"account": account, "delta": delta, "memo": raw.get("memo"), "metadata": raw.get("metadata")})
    if not normalized:
        raise ValueError("transaction requires at least one entry")
    if len({item["account"]["account_id"] for item in normalized}) != len(normalized):
        raise ValueError("transaction may contain only one entry per account")
    if len({item["account"]["currency_code"] for item in normalized}) > 1:
        raise ValueError("cross-currency settlement requires a represented FX contract")

    conn.execute("SAVEPOINT simulated_economy_transaction")
    try:
        conn.execute(
            """INSERT INTO economic_transactions(
                   transaction_id,transaction_type,sim_time,reason,source_type,source_id,source_event_id,
                   provenance_json,metadata_json
               ) VALUES(?,?,?,?,?,?,?,?,?)""",
            (_required(transaction_id, "transaction_id"), _required(transaction_type, "transaction_type"),
             _required(sim_time, "sim_time"), reason, source_type, source_id, source_event_id,
             _json(provenance), _json(metadata)),
        )
        for item in normalized:
            conn.execute(
                """INSERT INTO economic_transaction_entries(transaction_id,account_id,delta_minor,memo,metadata_json)
                   VALUES(?,?,?,?,?)""",
                (transaction_id, item["account"]["account_id"], item["delta"], item["memo"], _json(item["metadata"])),
            )
            conn.execute(
                "UPDATE financial_accounts SET balance_minor=balance_minor+?,updated_at=CURRENT_TIMESTAMP WHERE account_id=?",
                (item["delta"], item["account"]["account_id"]),
            )
        conn.execute("RELEASE SAVEPOINT simulated_economy_transaction")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT simulated_economy_transaction")
        conn.execute("RELEASE SAVEPOINT simulated_economy_transaction")
        raise
    return economic_transaction(conn, transaction_id)


def transfer_funds(conn: sqlite3.Connection, *, transaction_id: str, from_account_id: str,
                   to_account_id: str, amount_minor: int, sim_time: str,
                   reason: str | None = None, source_type: str | None = None,
                   source_id: str | None = None) -> dict[str, Any]:
    amount_minor = _minor(amount_minor, "amount_minor", positive=True)
    source, target = financial_account(conn, from_account_id), financial_account(conn, to_account_id)
    if source["currency_code"] != target["currency_code"]:
        raise ValueError("cross-currency transfer requires a represented FX contract")
    return post_transaction(
        conn, transaction_id=transaction_id, transaction_type="transfer", sim_time=sim_time,
        entries=[{"account_id": from_account_id, "delta_minor": -amount_minor, "memo": reason},
                 {"account_id": to_account_id, "delta_minor": amount_minor, "memo": reason}],
        reason=reason, source_type=source_type, source_id=source_id,
    )


def economic_transaction(conn: sqlite3.Connection, transaction_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM economic_transactions WHERE transaction_id=?", (transaction_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown economic transaction: {transaction_id}")
    result = dict(row)
    result["provenance"] = json.loads(result.pop("provenance_json"))
    result["metadata"] = json.loads(result.pop("metadata_json"))
    rows = conn.execute(
        "SELECT entry_id,account_id,delta_minor,memo,metadata_json FROM economic_transaction_entries WHERE transaction_id=? ORDER BY entry_id",
        (transaction_id,),
    ).fetchall()
    result["entries"] = [{"entry_id": row["entry_id"], "account_id": row["account_id"],
                           "delta_minor": row["delta_minor"], "memo": row["memo"],
                           "metadata": json.loads(row["metadata_json"])} for row in rows]
    return result


def record_asset(conn: sqlite3.Connection, *, asset_id: str, owner_economic_entity_id: str, asset_type: str,
                 represented_entity_id: str | None = None, quantity: float = 1.0,
                 provenance: dict[str, Any] | None = None, metadata: dict[str, Any] | None = None) -> None:
    economic_entity(conn, owner_economic_entity_id)
    if represented_entity_id is not None and conn.execute("SELECT 1 FROM entities WHERE id=?", (represented_entity_id,)).fetchone() is None:
        raise ValueError(f"unknown represented entity: {represented_entity_id}")
    conn.execute(
        "INSERT INTO economic_assets(asset_id,owner_economic_entity_id,asset_type,represented_entity_id,quantity,provenance_json,metadata_json) VALUES(?,?,?,?,?,?,?)",
        (_required(asset_id, "asset_id"), owner_economic_entity_id, _required(asset_type, "asset_type"),
         represented_entity_id, float(quantity), _json(provenance), _json(metadata)),
    )
    conn.commit()


def record_liability(conn: sqlite3.Connection, *, liability_id: str, debtor_economic_entity_id: str,
                     liability_type: str, principal_minor: int, outstanding_minor: int, currency_code: str,
                     creditor_economic_entity_id: str | None = None,
                     provenance: dict[str, Any] | None = None, metadata: dict[str, Any] | None = None) -> None:
    economic_entity(conn, debtor_economic_entity_id)
    if creditor_economic_entity_id is not None:
        economic_entity(conn, creditor_economic_entity_id)
    principal_minor, outstanding_minor = _minor(principal_minor, "principal_minor"), _minor(outstanding_minor, "outstanding_minor")
    if outstanding_minor > principal_minor:
        raise ValueError("outstanding_minor cannot exceed principal_minor")
    conn.execute(
        """INSERT INTO economic_liabilities(
               liability_id,debtor_economic_entity_id,creditor_economic_entity_id,liability_type,
               principal_minor,outstanding_minor,currency_code,provenance_json,metadata_json
           ) VALUES(?,?,?,?,?,?,?,?,?)""",
        (_required(liability_id, "liability_id"), debtor_economic_entity_id, creditor_economic_entity_id,
         _required(liability_type, "liability_type"), principal_minor, outstanding_minor, _currency(currency_code),
         _json(provenance), _json(metadata)),
    )
    conn.commit()


def record_valuation(conn: sqlite3.Connection, *, valuation_id: str, subject_type: str, subject_id: str,
                     amount_minor: int, currency_code: str, method: str, valuation_sim_time: str | None = None,
                     source_type: str | None = None, source_id: str | None = None,
                     provenance: dict[str, Any] | None = None) -> None:
    if subject_type not in {"asset", "economic_entity", "liability", "aggregate"}:
        raise ValueError(f"unsupported valuation subject_type: {subject_type}")
    conn.execute(
        """INSERT INTO economic_valuations(
               valuation_id,subject_type,subject_id,amount_minor,currency_code,valuation_sim_time,method,
               source_type,source_id,provenance_json
           ) VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (_required(valuation_id, "valuation_id"), subject_type, _required(subject_id, "subject_id"),
         _minor(amount_minor, "amount_minor"), _currency(currency_code), valuation_sim_time,
         _required(method, "method"), source_type, source_id, _json(provenance)),
    )
    conn.commit()


def economic_net_worth(conn: sqlite3.Connection, economic_entity_id: str, *, currency_code: str = "USD") -> int:
    economic_entity(conn, economic_entity_id)
    currency_code = _currency(currency_code)
    accounts = conn.execute(
        "SELECT COALESCE(SUM(balance_minor),0) FROM financial_accounts WHERE owner_economic_entity_id=? AND currency_code=? AND status!='closed'",
        (economic_entity_id, currency_code),
    ).fetchone()[0]
    assets = conn.execute(
        """SELECT COALESCE(SUM(v.amount_minor),0) FROM economic_assets a
           JOIN economic_valuations v ON v.valuation_id=(
             SELECT v2.valuation_id FROM economic_valuations v2
             WHERE v2.subject_type='asset' AND v2.subject_id=a.asset_id AND v2.currency_code=?
             ORDER BY CASE WHEN v2.valuation_sim_time IS NULL THEN 1 ELSE 0 END,
                      v2.valuation_sim_time DESC,v2.created_at DESC,v2.valuation_id DESC LIMIT 1)
           WHERE a.owner_economic_entity_id=? AND a.status='active'""",
        (currency_code, economic_entity_id),
    ).fetchone()[0]
    liabilities = conn.execute(
        "SELECT COALESCE(SUM(outstanding_minor),0) FROM economic_liabilities WHERE debtor_economic_entity_id=? AND currency_code=? AND status IN ('active','defaulted')",
        (economic_entity_id, currency_code),
    ).fetchone()[0]
    return int(accounts or 0) + int(assets or 0) - int(liabilities or 0)


def publish_financial_notice(conn: sqlite3.Connection, *, stimulus_id: str, character_id: str, subject: str,
                             notice_sim_time: str, source_type: str, source_id: str,
                             payload: dict[str, Any] | None = None, salience: float = 0.5) -> dict[str, Any]:
    if conn.execute("SELECT 1 FROM entities WHERE id=? AND entity_type='character'", (character_id,)).fetchone() is None:
        raise ValueError(f"unknown character: {character_id}")
    sources = {"economic_transaction": ("economic_transactions", "transaction_id"),
               "financial_account": ("financial_accounts", "account_id"),
               "economic_asset": ("economic_assets", "asset_id"),
               "economic_liability": ("economic_liabilities", "liability_id"),
               "economic_valuation": ("economic_valuations", "valuation_id")}
    if source_type not in sources:
        raise ValueError(f"unsupported financial notice source_type: {source_type}")
    table, key = sources[source_type]
    if conn.execute(f"SELECT 1 FROM {table} WHERE {key}=?", (source_id,)).fetchone() is None:
        raise ValueError(f"unknown {source_type}: {source_id}")
    notice = create_world_stimulus(
        conn, stimulus_id=stimulus_id, stimulus_type="financial", channel="other", subject=subject,
        start_sim_time=notice_sim_time, payload=payload, source_type=source_type, source_id=source_id,
        salience=salience, metadata={"economy_schema_version": 1},
    )
    add_stimulus_scope(conn, stimulus_id=stimulus_id, scope_type="character", scope_id=character_id)
    return notice


def load_economy_seed(path: str | Path = DARIAN_ECONOMY_SEED_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def seed_initial_economy(conn: sqlite3.Connection, path: str | Path = DARIAN_ECONOMY_SEED_PATH) -> None:
    seed = load_economy_seed(path)
    if conn.execute("SELECT 1 FROM entities WHERE id=?", (seed["represented_entity_id"],)).fetchone() is None:
        return
    item = seed["economic_entity"]
    ensure_economic_entity(conn, economic_entity_id=item["economic_entity_id"], entity_type=item["entity_type"],
                           display_name=item["display_name"], represented_entity_id=seed["represented_entity_id"],
                           provenance=seed.get("provenance"), metadata=item.get("metadata"))
    for account in seed.get("accounts", []):
        if conn.execute("SELECT 1 FROM financial_accounts WHERE account_id=?", (account["account_id"],)).fetchone() is None:
            create_financial_account(conn, account_id=account["account_id"], owner_economic_entity_id=item["economic_entity_id"],
                                     account_type=account["account_type"], currency_code=account["currency_code"],
                                     opening_balance_minor=int(account["opening_balance_minor"]),
                                     provenance=seed.get("provenance"), metadata=account.get("metadata"),
                                     opening_sim_time=seed["valuation_sim_time"])
    for asset in seed.get("assets", []):
        if conn.execute("SELECT 1 FROM economic_assets WHERE asset_id=?", (asset["asset_id"],)).fetchone() is None:
            record_asset(conn, asset_id=asset["asset_id"], owner_economic_entity_id=item["economic_entity_id"],
                         asset_type=asset["asset_type"], represented_entity_id=asset.get("represented_entity_id"),
                         provenance=seed.get("provenance"), metadata=asset.get("metadata"))
        valuation = asset["valuation"]
        if conn.execute("SELECT 1 FROM economic_valuations WHERE valuation_id=?", (valuation["valuation_id"],)).fetchone() is None:
            record_valuation(conn, valuation_id=valuation["valuation_id"], subject_type="asset", subject_id=asset["asset_id"],
                             amount_minor=int(valuation["amount_minor"]), currency_code=valuation["currency_code"],
                             method=valuation["method"], valuation_sim_time=seed["valuation_sim_time"],
                             source_type="canonical_seed", source_id=seed["revision"], provenance=seed.get("provenance"))
    for liability in seed.get("liabilities", []):
        if conn.execute("SELECT 1 FROM economic_liabilities WHERE liability_id=?", (liability["liability_id"],)).fetchone() is None:
            record_liability(conn, liability_id=liability["liability_id"], debtor_economic_entity_id=item["economic_entity_id"],
                             liability_type=liability["liability_type"], principal_minor=int(liability["principal_minor"]),
                             outstanding_minor=int(liability["outstanding_minor"]), currency_code=liability["currency_code"],
                             provenance=seed.get("provenance"), metadata=liability.get("metadata"))
