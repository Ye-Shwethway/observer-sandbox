from __future__ import annotations

import pytest

from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.economy import (
    can_afford,
    create_financial_account,
    economic_net_worth,
    ensure_economic_entity,
    financial_account,
    publish_financial_notice,
    transfer_funds,
)
from observer_sandbox.economy_schema import ECONOMY_SCHEMA_VERSION, migrate_economy_schema
from observer_sandbox.runtime import initialize
from observer_sandbox.world_stimulus import eligible_world_stimuli

DARIAN = "char_darian"
DARIAN_ECON = "econ_char_darian"
DARIAN_LIQUID = "acct_darian_primary_liquid"


def test_w3_schema_and_darian_seed(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        migrate_economy_schema(conn)
        migrate_economy_schema(conn)
        schema = int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0])
        economy_schema = int(conn.execute("SELECT value FROM schema_meta WHERE key='economy_schema_version'").fetchone()[0])
        assert schema == SCHEMA_VERSION
        assert economy_schema == ECONOMY_SCHEMA_VERSION

        account = financial_account(conn, DARIAN_LIQUID)
        assert account["currency_code"] == "USD"
        assert account["balance_minor"] == 180_000_000
        assert account["owner_economic_entity_id"] == DARIAN_ECON

        estate = conn.execute("SELECT represented_entity_id FROM economic_assets WHERE asset_id='asset_thorne_estate'").fetchone()
        assert estate["represented_entity_id"] == "loc_thorne_estate"
        assert economic_net_worth(conn, DARIAN_ECON) == 2_500_000_000


def test_runtime_reinitialization_does_not_reset_live_money(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        ensure_economic_entity(
            conn,
            economic_entity_id="econ_fixture_vendor",
            entity_type="company",
            display_name="Fixture Vendor",
        )
        create_financial_account(
            conn,
            account_id="acct_fixture_vendor",
            owner_economic_entity_id="econ_fixture_vendor",
            account_type="operating",
            currency_code="USD",
        )
        transfer_funds(
            conn,
            transaction_id="txn_fixture_purchase",
            from_account_id=DARIAN_LIQUID,
            to_account_id="acct_fixture_vendor",
            amount_minor=25_00,
            sim_time="2025-05-04T12:00:00+00:00",
            reason="fixture purchase",
        )
        assert financial_account(conn, DARIAN_LIQUID)["balance_minor"] == 179_997_500

    initialize(db)
    with connect(db) as conn:
        assert financial_account(conn, DARIAN_LIQUID)["balance_minor"] == 179_997_500
        assert conn.execute(
            "SELECT COUNT(*) FROM economic_transactions WHERE transaction_id='opening:acct_darian_primary_liquid'"
        ).fetchone()[0] == 1


def test_affordability_and_transaction_settlement_are_deterministic(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        ensure_economic_entity(
            conn,
            economic_entity_id="econ_fixture_shop",
            entity_type="company",
            display_name="Fixture Shop",
        )
        create_financial_account(
            conn,
            account_id="acct_fixture_shop",
            owner_economic_entity_id="econ_fixture_shop",
            account_type="operating",
            currency_code="USD",
        )
        before = financial_account(conn, DARIAN_LIQUID)["balance_minor"]
        assert can_afford(conn, DARIAN_LIQUID, 50_00)
        transfer = transfer_funds(
            conn,
            transaction_id="txn_fixture_50",
            from_account_id=DARIAN_LIQUID,
            to_account_id="acct_fixture_shop",
            amount_minor=50_00,
            sim_time="2025-05-04T13:00:00+00:00",
        )
        assert [entry["delta_minor"] for entry in transfer["entries"]] == [-50_00, 50_00]
        assert financial_account(conn, DARIAN_LIQUID)["balance_minor"] == before - 50_00
        assert financial_account(conn, "acct_fixture_shop")["balance_minor"] == 50_00

        darian_before_failed = financial_account(conn, DARIAN_LIQUID)["balance_minor"]
        shop_before_failed = financial_account(conn, "acct_fixture_shop")["balance_minor"]
        with pytest.raises(ValueError, match="insufficient funds"):
            transfer_funds(
                conn,
                transaction_id="txn_fixture_impossible",
                from_account_id="acct_fixture_shop",
                to_account_id=DARIAN_LIQUID,
                amount_minor=99_00,
                sim_time="2025-05-04T13:05:00+00:00",
            )
        assert financial_account(conn, DARIAN_LIQUID)["balance_minor"] == darian_before_failed
        assert financial_account(conn, "acct_fixture_shop")["balance_minor"] == shop_before_failed
        assert conn.execute(
            "SELECT 1 FROM economic_transactions WHERE transaction_id='txn_fixture_impossible'"
        ).fetchone() is None


def test_financial_notice_uses_w0_without_automatic_exposure_memory_or_mind(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = {
            "exposure": conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0],
            "memory": conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0],
            "cycles": conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0],
            "artifacts": conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0],
        }
        notice = publish_financial_notice(
            conn,
            stimulus_id="stim_financial_fixture",
            character_id=DARIAN,
            subject="Primary liquid balance statement available",
            notice_sim_time="2025-05-04T14:00:00+00:00",
            source_type="financial_account",
            source_id=DARIAN_LIQUID,
            payload={"currency_code": "USD", "balance_minor": financial_account(conn, DARIAN_LIQUID)["balance_minor"]},
        )
        assert notice["stimulus_type"] == "financial"
        assert notice["source_type"] == "financial_account"
        eligible = eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time="2025-05-04T14:01:00+00:00",
        )
        assert "stim_financial_fixture" in [item["stimulus_id"] for item in eligible]
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == before["exposure"]
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == before["memory"]
        assert conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0] == before["cycles"]
        assert conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0] == before["artifacts"]