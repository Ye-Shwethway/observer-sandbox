from __future__ import annotations

import sqlite3


FIELDS = (
    {
        "field_key": "sexual_anatomy.erectile_state",
        "domain": "sexual_anatomy",
        "label": "Erectile state",
        "data_type": "text",
        "unit": None,
        "description": "Context-dependent physiological state: flaccid, developing, erect, or subsiding.",
        "default_mode": "simulated",
        "default_authority": "sexual_physiology_engine",
        "sensitivity": "intimate",
        "metadata_json": '{"allowed_values":["flaccid","developing","erect","subsiding"],"baseline":"flaccid"}',
    },
    {
        "field_key": "sexual_anatomy.erection_firmness",
        "domain": "sexual_anatomy",
        "label": "Erection firmness",
        "data_type": "number",
        "unit": "0-100",
        "description": "Conditional dynamic rigidity score. Zero while flaccid does not imply dysfunction; it means no erection is present.",
        "default_mode": "simulated",
        "default_authority": "sexual_physiology_engine",
        "sensitivity": "intimate",
        "metadata_json": '{"min":0,"max":100,"meaning":"contextual_response","baseline_when_flaccid":0}',
    },
    {
        "field_key": "sexual_anatomy.erection_firmness_cap",
        "domain": "sexual_anatomy",
        "label": "Erection firmness physiological cap",
        "data_type": "number",
        "unit": "0-100",
        "description": "Individual physiological maximum rigidity ceiling, distinct from the current contextual response.",
        "default_mode": "canonical",
        "default_authority": "profile_core",
        "sensitivity": "intimate",
        "metadata_json": '{"min":0,"max":100}',
    },
    {
        "field_key": "sexual_anatomy.baseline_erectile_function",
        "domain": "sexual_anatomy",
        "label": "Baseline erectile function",
        "data_type": "number",
        "unit": "0-100",
        "description": "Longer-term physiological capacity score used by future sexual physiology simulation; not the momentary erection state.",
        "default_mode": "static",
        "default_authority": "sexual_physiology_engine",
        "sensitivity": "intimate",
        "metadata_json": '{"min":0,"max":100,"timescale":"long_term"}',
    },
    {
        "field_key": "sexual_state.arousal_level",
        "domain": "sexual_state",
        "label": "Arousal level",
        "data_type": "number",
        "unit": "0-100",
        "description": "Contextual arousal state, modeled separately from erectile firmness so psychological arousal and physiological response can diverge.",
        "default_mode": "simulated",
        "default_authority": "sexual_physiology_engine",
        "sensitivity": "intimate",
        "metadata_json": '{"min":0,"max":100,"baseline":0}',
    },
    {
        "field_key": "sexual_state.solo_regulation_drive",
        "domain": "sexual_state",
        "label": "Solo regulation drive",
        "data_type": "number",
        "unit": "0-100",
        "description": "Current non-clinical behavioral drive used by the autonomous solo sexual-regulation loop; derived from authored libido, release recency, and immediate recovery state rather than a testosterone surrogate or weekly quota.",
        "default_mode": "simulated",
        "default_authority": "sexual_behavior_engine",
        "sensitivity": "intimate",
        "metadata_json": '{"min":0,"max":100,"meaning":"behavioral_drive","not_clinical":true}',
    },
)


def seed_sexual_state_fields(conn: sqlite3.Connection) -> None:
    for f in FIELDS:
        conn.execute(
            """
            INSERT INTO profile_field_definitions(
                field_key, domain, label, data_type, unit, description,
                default_mode, default_authority, sensitivity, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(field_key) DO UPDATE SET
                domain=excluded.domain,
                label=excluded.label,
                data_type=excluded.data_type,
                unit=excluded.unit,
                description=excluded.description,
                default_mode=excluded.default_mode,
                default_authority=excluded.default_authority,
                sensitivity=excluded.sensitivity,
                metadata_json=excluded.metadata_json,
                updated_at=CURRENT_TIMESTAMP
            """,
            (
                f["field_key"],
                f["domain"],
                f["label"],
                f["data_type"],
                f["unit"],
                f["description"],
                f["default_mode"],
                f["default_authority"],
                f["sensitivity"],
                f["metadata_json"],
            ),
        )
    conn.commit()
