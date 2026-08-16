from __future__ import annotations

import sqlite3
from typing import Any

from .economy_observer import character_economy_summary, entity_economic_value, represented_asset_summary


def format_money_minor(amount_minor: int, currency_code: str | None = "USD") -> str:
    code = (currency_code or "").upper()
    amount = int(amount_minor)
    sign = "-" if amount < 0 else ""
    absolute = abs(amount)
    whole, cents = divmod(absolute, 100)
    number = f"{whole:,}.{cents:02d}"
    return f"{sign}${number}" if code == "USD" else f"{sign}{code} {number}".strip()


def _friendly(value: str) -> str:
    return str(value).replace("_", " ").title()


def character_finances_view(
    conn: sqlite3.Connection,
    character_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    data = character_economy_summary(conn, character_id)
    currency = str(data["currency_code"])
    lines = [
        f"💰 {data['character']['name']} · FINANCES",
        "━━━━━━━━━━━━━━━━━━",
        f"💎 Net worth   {format_money_minor(data['net_worth_minor'], currency)}",
    ]

    accounts = data.get("accounts") or []
    if accounts:
        lines.extend(["", "🏦 Accounts"])
        for account in accounts:
            lines.append(
                f"• {_friendly(account['account_type'])}: "
                f"{format_money_minor(account['balance_minor'], account['currency_code'])}"
            )

    assets = data.get("assets") or []
    if assets:
        lines.extend(["", "🏛 Assets"])
        for asset in assets:
            valuation = asset.get("valuation")
            value = "Unvalued" if valuation is None else format_money_minor(
                valuation["amount_minor"], valuation["currency_code"]
            )
            label = asset.get("represented_name") or _friendly(asset["asset_type"])
            lines.append(f"• {label}: {value}")

    liabilities = data.get("liabilities") or []
    if liabilities:
        lines.extend(["", "📉 Liabilities"])
        for liability in liabilities:
            lines.append(
                f"• {_friendly(liability['liability_type'])}: "
                f"{format_money_minor(liability['outstanding_minor'], liability['currency_code'])}"
            )

    lines.extend([
        "",
        "ℹ️ Net worth and spendable balance are separate economic facts.",
    ])
    keyboard = [
        [{"text": f"← {data['character']['name']}", "callback_data": f"char:{character_id}"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]
    return "\n".join(lines), keyboard


def location_asset_lines(conn: sqlite3.Connection, location_id: str) -> list[str]:
    asset = represented_asset_summary(conn, location_id)
    if asset is None:
        return []
    valuation = asset.get("valuation")
    lines = ["", "💰 Economic asset"]
    if valuation is not None:
        lines.append(f"• Value: {format_money_minor(valuation['amount_minor'], valuation['currency_code'])}")
    lines.append(f"• Owner: {asset['owner_name']}")
    lines.append(f"• Type: {_friendly(asset['asset_type'])}")
    return lines


def object_value_lines(conn: sqlite3.Connection, object_id: str) -> list[str]:
    value = entity_economic_value(conn, object_id)
    if value is None:
        return []
    lines = ["", "💰 Economic value"]
    currency = value.get("currency_code")
    if value.get("market_value_minor") is not None:
        lines.append(f"• Market value: {format_money_minor(value['market_value_minor'], currency)}")
    if value.get("replacement_value_minor") is not None:
        lines.append(f"• Replacement value: {format_money_minor(value['replacement_value_minor'], currency)}")
    treatment = str(value.get("net_worth_treatment") or "")
    if treatment == "included_in_parent":
        parent = value.get("parent_asset") or {}
        label = parent.get("represented_name") or parent.get("asset_id") or "parent asset"
        lines.append(f"• Net worth: Included in {label}")
    elif treatment == "excluded":
        lines.append("• Net worth: Excluded to prevent duplicate economic counting")
    elif treatment:
        lines.append(f"• Net worth: {_friendly(treatment)}")
    return lines
