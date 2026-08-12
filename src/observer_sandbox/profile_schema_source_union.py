from __future__ import annotations

import json
import sqlite3

# Fields present in the supplied Darian source formats or previously agreed profile display
# surfaces that are intentionally preserved even where they overlap another domain.
SOURCE_UNION_FIELDS = (
    ("raps_pa.focus_precision", "raps_pa", "Focus and precision", "number", None, "static", "profile_core", "normal"),
    ("raps_pa.practical_skill", "raps_pa", "Practical skill", "number", None, "static", "profile_core", "normal"),
    ("raps_ma.tactical_leadership", "raps_ma", "Tactical leadership", "number", None, "static", "profile_core", "normal"),
    ("raps_ia.capability_notes", "raps_ia", "Intellectual capability notes", "text", None, "canonical", "profile_core", "normal"),
    ("raps_sa.charisma", "raps_sa", "Sexual charisma", "number", None, "static", "profile_core", "private"),
    ("appearance.marks_scars_tattoos", "appearance", "Marks, scars and tattoos", "json", None, "canonical", "profile_core", "normal"),
    ("background.connection_notes", "background", "Important connection notes", "json", None, "canonical", "profile_core", "normal"),
)

# Architecture-agreed dynamic fields needed by future life-like simulation. They start static
# until their owning engine is enabled.
LIFE_SIM_FIELDS = (
    ("sleep.last_sleep_start", "sleep", "Last sleep start", "datetime", None, "static", "sleep_engine", "normal"),
    ("sleep.last_wake_time", "sleep", "Last wake time", "datetime", None, "static", "sleep_engine", "normal"),
    ("sleep.duration_hours", "sleep", "Recent sleep duration", "number", "hours", "static", "sleep_engine", "normal"),
    ("sleep.quality", "sleep", "Sleep quality", "number", None, "static", "sleep_engine", "normal"),
    ("sleep.debt_hours", "sleep", "Sleep debt", "number", "hours", "static", "sleep_engine", "normal"),
    ("physiology.resting_heart_rate_bpm", "physiology", "Resting heart rate", "number", "bpm", "static", "health_engine", "private"),
    ("physiology.current_heart_rate_bpm", "physiology", "Current heart rate", "number", "bpm", "static", "health_engine", "private"),
    ("physiology.body_temperature_c", "physiology", "Body temperature", "number", "C", "static", "health_engine", "private"),
    ("physiology.blood_pressure", "physiology", "Blood pressure", "json", "mmHg", "static", "health_engine", "private"),
    ("nutrition.calorie_balance_kcal", "nutrition", "Calorie balance", "number", "kcal", "static", "nutrition_engine", "normal"),
    ("nutrition.protein_g", "nutrition", "Protein intake", "number", "g", "static", "nutrition_engine", "normal"),
    ("nutrition.glycogen_state", "nutrition", "Glycogen state", "number", None, "static", "nutrition_engine", "normal"),
    ("training.training_age_years", "training", "Training age", "number", "years", "canonical", "profile_core", "normal"),
    ("training.accumulated_stimulus", "training", "Accumulated training stimulus", "json", None, "static", "training_adaptation_engine", "normal"),
    ("training.adaptation_state", "training", "Adaptation state", "json", None, "static", "training_adaptation_engine", "normal"),
    ("emotion.current_mood", "emotion", "Current mood", "text", None, "static", "emotion_engine", "normal"),
    ("emotion.valence", "emotion", "Emotional valence", "number", None, "static", "emotion_engine", "normal"),
    ("emotion.arousal", "emotion", "Emotional arousal", "number", None, "static", "emotion_engine", "normal"),
    ("goal.current_short_term_goals", "goal", "Current short-term goals", "json", None, "static", "goal_engine", "normal"),
)


def seed_source_union_extensions(conn: sqlite3.Connection) -> None:
    for field in SOURCE_UNION_FIELDS + LIFE_SIM_FIELDS:
        key, domain, label, data_type, unit, mode, authority, sensitivity = field
        metadata = {"scale": "0-100"} if data_type == "number" and domain.startswith("raps_") else {}
        conn.execute(
            """
            INSERT INTO profile_field_definitions(
                field_key, domain, label, data_type, unit, default_mode,
                default_authority, sensitivity, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(field_key) DO UPDATE SET
                domain=excluded.domain,
                label=excluded.label,
                data_type=excluded.data_type,
                unit=excluded.unit,
                default_mode=excluded.default_mode,
                default_authority=excluded.default_authority,
                sensitivity=excluded.sensitivity,
                metadata_json=excluded.metadata_json,
                updated_at=CURRENT_TIMESTAMP
            """,
            (key, domain, label, data_type, unit, mode, authority, sensitivity, json.dumps(metadata)),
        )
    conn.commit()
