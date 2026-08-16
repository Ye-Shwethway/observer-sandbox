from __future__ import annotations

import sqlite3


ECONOMY_SCHEMA_VERSION = 1

ECONOMY_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS economic_entities (
    economic_entity_id TEXT PRIMARY KEY,
    represented_entity_id TEXT UNIQUE REFERENCES entities(id) ON DELETE SET NULL,
    entity_type TEXT NOT NULL CHECK(entity_type IN (
        'character','household','company','organization','government','trust','other'
    )),
    display_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','inactive','closed')),
    provenance_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS financial_accounts (
    account_id TEXT PRIMARY KEY,
    owner_economic_entity_id TEXT NOT NULL REFERENCES economic_entities(economic_entity_id) ON DELETE CASCADE,
    account_type TEXT NOT NULL,
    currency_code TEXT NOT NULL,
    balance_minor INTEGER NOT NULL DEFAULT 0,
    institution_economic_entity_id TEXT REFERENCES economic_entities(economic_entity_id) ON DELETE SET NULL,
    allow_negative INTEGER NOT NULL DEFAULT 0 CHECK(allow_negative IN (0,1)),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','frozen','closed')),
    provenance_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_financial_accounts_owner
    ON financial_accounts(owner_economic_entity_id, status);

CREATE TABLE IF NOT EXISTS economic_assets (
    asset_id TEXT PRIMARY KEY,
    owner_economic_entity_id TEXT NOT NULL REFERENCES economic_entities(economic_entity_id) ON DELETE CASCADE,
    asset_type TEXT NOT NULL,
    represented_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    quantity REAL NOT NULL DEFAULT 1.0 CHECK(quantity > 0),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','disposed','destroyed')),
    provenance_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_economic_assets_owner
    ON economic_assets(owner_economic_entity_id, status);
CREATE INDEX IF NOT EXISTS idx_economic_assets_represented_entity
    ON economic_assets(represented_entity_id);

CREATE TABLE IF NOT EXISTS economic_liabilities (
    liability_id TEXT PRIMARY KEY,
    debtor_economic_entity_id TEXT NOT NULL REFERENCES economic_entities(economic_entity_id) ON DELETE CASCADE,
    creditor_economic_entity_id TEXT REFERENCES economic_entities(economic_entity_id) ON DELETE SET NULL,
    liability_type TEXT NOT NULL,
    principal_minor INTEGER NOT NULL CHECK(principal_minor >= 0),
    outstanding_minor INTEGER NOT NULL CHECK(outstanding_minor >= 0),
    currency_code TEXT NOT NULL,
    due_sim_time TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','settled','cancelled','defaulted')),
    provenance_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_economic_liabilities_debtor
    ON economic_liabilities(debtor_economic_entity_id, status);

CREATE TABLE IF NOT EXISTS economic_valuations (
    valuation_id TEXT PRIMARY KEY,
    subject_type TEXT NOT NULL CHECK(subject_type IN ('asset','economic_entity','liability','aggregate')),
    subject_id TEXT NOT NULL,
    amount_minor INTEGER NOT NULL CHECK(amount_minor >= 0),
    currency_code TEXT NOT NULL,
    valuation_sim_time TEXT,
    method TEXT NOT NULL,
    source_type TEXT,
    source_id TEXT,
    provenance_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_economic_valuations_subject
    ON economic_valuations(subject_type, subject_id, currency_code, valuation_sim_time);

CREATE TABLE IF NOT EXISTS economic_transactions (
    transaction_id TEXT PRIMARY KEY,
    transaction_type TEXT NOT NULL,
    sim_time TEXT NOT NULL,
    reason TEXT,
    source_type TEXT,
    source_id TEXT,
    source_event_id INTEGER REFERENCES events(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'committed' CHECK(status IN ('committed','reversed')),
    provenance_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS economic_transaction_entries (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT NOT NULL REFERENCES economic_transactions(transaction_id) ON DELETE RESTRICT,
    account_id TEXT NOT NULL REFERENCES financial_accounts(account_id) ON DELETE RESTRICT,
    delta_minor INTEGER NOT NULL CHECK(delta_minor != 0),
    memo TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(transaction_id, account_id, delta_minor, memo)
);

CREATE INDEX IF NOT EXISTS idx_economic_transaction_entries_account
    ON economic_transaction_entries(account_id, entry_id);
"""


def migrate_economy_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(ECONOMY_SCHEMA_SQL)
    conn.execute(
        "INSERT INTO schema_meta(key, value) VALUES('economy_schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(ECONOMY_SCHEMA_VERSION),),
    )
    conn.commit()
