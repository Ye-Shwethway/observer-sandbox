from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileField:
    key: str
    domain: str
    label: str
    data_type: str = "number"
    unit: str | None = None
    default_mode: str = "static"
    authority: str = "profile_core"
    sensitivity: str = "normal"
    description: str | None = None


FIELDS = (
    # Identity / chronology
    ProfileField("identity.full_name", "identity", "Full name", "text", default_mode="canonical"),
    ProfileField("identity.date_of_birth", "identity", "Date of birth", "date", default_mode="canonical"),
    ProfileField("identity.age_years", "identity", "Age", "number", "years", "derived", "time_engine"),
    ProfileField("identity.sex", "identity", "Sex", "text", default_mode="canonical"),
    ProfileField("identity.gender", "identity", "Gender", "text", default_mode="canonical"),
    ProfileField("identity.sexual_orientation", "identity", "Sexual orientation", "text", default_mode="canonical", sensitivity="private"),
    ProfileField("identity.zodiac_sign", "identity", "Zodiac sign", "text", default_mode="derived", authority="time_engine"),
    ProfileField("identity.current_status", "identity", "Current status", "text"),

    # Core visual/body metrics
    ProfileField("body.height_in", "body", "Height", unit="in", default_mode="canonical"),
    ProfileField("body.weight_lb", "body", "Weight", unit="lb", default_mode="static", authority="physiology_engine"),
    ProfileField("body.body_fat_pct", "body", "Body fat", unit="percent", authority="physiology_engine"),
    ProfileField("body.lean_mass_lb", "body", "Lean mass", unit="lb", default_mode="derived", authority="physiology_engine"),
    ProfileField("body.fat_mass_lb", "body", "Fat mass", unit="lb", default_mode="derived", authority="physiology_engine"),
    ProfileField("body.bmi", "body", "BMI", default_mode="derived", authority="physiology_engine"),
    ProfileField("body.neck_in", "body", "Neck circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.shoulders_in", "body", "Shoulder circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.chest_in", "body", "Chest circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.waist_in", "body", "Waist circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.hips_in", "body", "Hip circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.biceps_relaxed_in", "body", "Biceps relaxed", unit="in", authority="body_progression_engine"),
    ProfileField("body.biceps_flexed_in", "body", "Biceps flexed", unit="in", authority="body_progression_engine"),
    ProfileField("body.triceps_in", "body", "Triceps circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.forearms_in", "body", "Forearm circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.thighs_in", "body", "Thigh circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.calves_in", "body", "Calf circumference", unit="in", authority="body_progression_engine"),
    ProfileField("body.abdominal_definition", "appearance", "Abdominal definition", "text"),
    ProfileField("body.chest_hair", "appearance", "Chest hair", "text", default_mode="canonical"),

    # Sexual anatomy / physiology; intimate but first-class, not hidden in prose.
    ProfileField("sexual_anatomy.penis_length_in", "sexual_anatomy", "Penis length", unit="in", default_mode="canonical", sensitivity="intimate"),
    ProfileField("sexual_anatomy.penis_girth_in", "sexual_anatomy", "Penis girth", unit="in", default_mode="canonical", sensitivity="intimate"),
    ProfileField("sexual_anatomy.erection_firmness", "sexual_anatomy", "Erection firmness", "number", default_mode="static", authority="sexual_physiology_engine", sensitivity="intimate"),
    ProfileField("sexual_anatomy.sensitivity", "sexual_anatomy", "Genital sensitivity", "number", default_mode="static", authority="sexual_physiology_engine", sensitivity="intimate"),

    # Face / appearance
    ProfileField("appearance.face_shape", "appearance", "Face shape", "text", default_mode="canonical"),
    ProfileField("appearance.jawline", "appearance", "Jawline", "text", default_mode="canonical"),
    ProfileField("appearance.cheekbones", "appearance", "Cheekbones", "text", default_mode="canonical"),
    ProfileField("appearance.facial_symmetry", "appearance", "Facial symmetry", "number", default_mode="canonical"),
    ProfileField("appearance.golden_ratio_alignment", "appearance", "Golden-ratio alignment", "number", default_mode="canonical"),
    ProfileField("appearance.eye_color", "appearance", "Eye color", "text", default_mode="canonical"),
    ProfileField("appearance.eye_appeal", "appearance", "Eye appeal", "number", default_mode="canonical"),
    ProfileField("appearance.hair_color", "appearance", "Hair color", "text", default_mode="canonical"),
    ProfileField("appearance.hair_style", "appearance", "Hair style", "text", default_mode="canonical"),
    ProfileField("appearance.facial_hair", "appearance", "Facial hair", "text", default_mode="canonical"),
    ProfileField("appearance.skin_quality", "appearance", "Skin quality", "number", default_mode="static", authority="physiology_engine"),
    ProfileField("appearance.smile_appeal", "appearance", "Smile appeal", "number", default_mode="canonical"),
    ProfileField("appearance.facial_beauty", "appearance", "Overall facial beauty", "number", default_mode="canonical"),
    ProfileField("appearance.pars", "appearance", "Physical Appeal Rating", "number", default_mode="derived", authority="appearance_engine"),
    ProfileField("appearance.distinctive_features", "appearance", "Distinctive features", "json", default_mode="canonical"),

    # Physical attributes / RAPS-PA
    ProfileField("raps_pa.strength", "raps_pa", "Strength"),
    ProfileField("raps_pa.stamina", "raps_pa", "Stamina"),
    ProfileField("raps_pa.agility", "raps_pa", "Agility"),
    ProfileField("raps_pa.speed", "raps_pa", "Speed"),
    ProfileField("raps_pa.reflexes", "raps_pa", "Reflexes"),
    ProfileField("raps_pa.endurance", "raps_pa", "Endurance"),
    ProfileField("raps_pa.flexibility", "raps_pa", "Flexibility"),
    ProfileField("raps_pa.combat_skill", "raps_pa", "Combat skill"),
    ProfileField("raps_pa.weapons_proficiency", "raps_pa", "Weapons proficiency"),
    ProfileField("raps_pa.survival_skill", "raps_pa", "Survival skill"),
    ProfileField("raps_pa.powerlifting_capacity", "raps_pa", "Powerlifting capacity"),

    # Mental / emotional / intellectual
    ProfileField("raps_ma.confidence", "raps_ma", "Confidence"),
    ProfileField("raps_ma.resilience", "raps_ma", "Resilience"),
    ProfileField("raps_ma.adaptability", "raps_ma", "Adaptability"),
    ProfileField("raps_ma.emotional_stability", "raps_ma", "Emotional stability"),
    ProfileField("raps_ma.focus", "raps_ma", "Focus"),
    ProfileField("raps_ma.leadership", "raps_ma", "Leadership"),
    ProfileField("raps_ma.stress_management", "raps_ma", "Stress management", authority="emotion_engine"),
    ProfileField("raps_ma.curiosity", "raps_ma", "Curiosity"),
    ProfileField("raps_ia.iq", "raps_ia", "IQ", default_mode="canonical"),
    ProfileField("raps_ia.problem_solving", "raps_ia", "Problem solving"),
    ProfileField("raps_ia.tactical_thinking", "raps_ia", "Tactical thinking"),
    ProfileField("raps_ia.creativity", "raps_ia", "Creativity"),
    ProfileField("raps_ia.technological_aptitude", "raps_ia", "Technological aptitude"),
    ProfileField("raps_ia.medical_knowledge", "raps_ia", "Medical knowledge"),
    ProfileField("raps_ia.social_intelligence", "raps_ia", "Social intelligence"),
    ProfileField("raps_ia.strategic_ingenuity", "raps_ia", "Strategic ingenuity"),

    # Social / verbal charisma
    ProfileField("social.charisma", "social", "Charisma"),
    ProfileField("social.emotional_intelligence", "social", "Emotional intelligence"),
    ProfileField("raps_vc.tone_resonance", "raps_vc", "Tone resonance"),
    ProfileField("raps_vc.wit_humor", "raps_vc", "Wit and humor"),
    ProfileField("raps_vc.persuasion", "raps_vc", "Persuasion"),
    ProfileField("raps_vc.empathy_in_speech", "raps_vc", "Empathy in speech"),
    ProfileField("raps_vc.overall", "raps_vc", "Verbal charisma"),

    # Sexual attributes / RAPS-SA
    ProfileField("raps_sa.libido", "raps_sa", "Libido", authority="sexual_physiology_engine", sensitivity="private"),
    ProfileField("raps_sa.sensitivity", "raps_sa", "Sensitivity", authority="sexual_physiology_engine", sensitivity="private"),
    ProfileField("raps_sa.performance", "raps_sa", "Sexual performance", sensitivity="private"),
    ProfileField("raps_sa.experience", "raps_sa", "Sexual experience", sensitivity="private"),
    ProfileField("raps_sa.arousal_control", "raps_sa", "Arousal control", authority="sexual_physiology_engine", sensitivity="private"),
    ProfileField("raps_sa.sexual_endurance", "raps_sa", "Sexual endurance", authority="sexual_physiology_engine", sensitivity="private"),
    ProfileField("raps_sa.dominance_appeal", "raps_sa", "Dominance appeal", sensitivity="private"),
    ProfileField("raps_sa.self_satisfaction_weekly", "raps_sa", "Self-satisfaction weekly count", "integer", default_mode="simulated", authority="sexual_behavior_engine", sensitivity="intimate"),
    ProfileField("raps_sa.partnered_satisfaction_weekly", "raps_sa", "Partnered satisfaction weekly count", "integer", default_mode="simulated", authority="sexual_behavior_engine", sensitivity="intimate"),

    # Dynamic physical/needs state planned for progressive activation
    ProfileField("needs.energy", "needs", "Energy", authority="needs_engine"),
    ProfileField("needs.hunger", "needs", "Hunger", authority="needs_engine"),
    ProfileField("needs.hydration", "needs", "Hydration", authority="needs_engine"),
    ProfileField("needs.sleepiness", "needs", "Sleepiness", authority="sleep_engine"),
    ProfileField("physiology.fatigue", "physiology", "Systemic fatigue", authority="physiology_engine"),
    ProfileField("physiology.muscle_soreness", "physiology", "Muscle soreness", "json", authority="training_adaptation_engine"),
    ProfileField("physiology.injury_state", "physiology", "Injury state", "json", authority="injury_engine"),
    ProfileField("physiology.illness_state", "physiology", "Illness state", "json", authority="health_engine"),
    ProfileField("physiology.recovery", "physiology", "Recovery readiness", authority="recovery_engine"),

    # Genetics / limits
    ProfileField("genetics.height_max_in", "genetics", "Genetic maximum height", unit="in", default_mode="canonical"),
    ProfileField("genetics.weight_lean_min_lb", "genetics", "Genetic lean-weight range minimum", unit="lb", default_mode="canonical"),
    ProfileField("genetics.weight_lean_max_lb", "genetics", "Genetic lean-weight range maximum", unit="lb", default_mode="canonical"),
    ProfileField("genetics.body_fat_floor_pct", "genetics", "Sustainable body-fat floor", unit="percent", default_mode="canonical"),
    ProfileField("genetics.neck_max_in", "genetics", "Genetic maximum neck", unit="in", default_mode="canonical"),
    ProfileField("genetics.shoulders_max_in", "genetics", "Genetic maximum shoulders", unit="in", default_mode="canonical"),
    ProfileField("genetics.chest_max_in", "genetics", "Genetic maximum chest", unit="in", default_mode="canonical"),
    ProfileField("genetics.waist_target_in", "genetics", "Genetic-maximum-condition waist", unit="in", default_mode="canonical"),
    ProfileField("genetics.biceps_relaxed_max_in", "genetics", "Genetic maximum relaxed biceps", unit="in", default_mode="canonical"),
    ProfileField("genetics.biceps_flexed_max_in", "genetics", "Genetic maximum flexed biceps", unit="in", default_mode="canonical"),
    ProfileField("genetics.triceps_max_in", "genetics", "Genetic maximum triceps", unit="in", default_mode="canonical"),
    ProfileField("genetics.forearms_max_in", "genetics", "Genetic maximum forearms", unit="in", default_mode="canonical"),
    ProfileField("genetics.thighs_max_in", "genetics", "Genetic maximum thighs", unit="in", default_mode="canonical"),
    ProfileField("genetics.calves_max_in", "genetics", "Genetic maximum calves", unit="in", default_mode="canonical"),
    ProfileField("genetics.penis_length_in", "genetics", "Genetically fixed penis length", unit="in", default_mode="canonical", sensitivity="intimate"),
    ProfileField("genetics.penis_girth_in", "genetics", "Genetically fixed penis girth", unit="in", default_mode="canonical", sensitivity="intimate"),

    # Personality / narrative / background
    ProfileField("personality.primary_motivation", "personality", "Primary motivation", "text", default_mode="canonical"),
    ProfileField("personality.primary_traits", "personality", "Primary traits", "json", default_mode="canonical"),
    ProfileField("personality.complexity_notes", "personality", "Personality complexity", "text", default_mode="canonical"),
    ProfileField("background.origins", "background", "Origins", "text", default_mode="canonical"),
    ProfileField("background.story_elements", "background", "Story elements", "json", default_mode="canonical"),
    ProfileField("narrative.current_arc", "narrative", "Current narrative arc", "text", authority="narrative_engine"),
    ProfileField("narrative.current_goal", "narrative", "Current goal", "text", authority="goal_engine"),
)


def seed_profile_field_definitions(conn: sqlite3.Connection) -> None:
    for f in FIELDS:
        conn.execute(
            """
            INSERT INTO profile_field_definitions(
                field_key, domain, label, data_type, unit, description,
                default_mode, default_authority, sensitivity, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '{}')
            ON CONFLICT(field_key) DO UPDATE SET
                domain=excluded.domain,
                label=excluded.label,
                data_type=excluded.data_type,
                unit=excluded.unit,
                description=excluded.description,
                default_mode=excluded.default_mode,
                default_authority=excluded.default_authority,
                sensitivity=excluded.sensitivity,
                updated_at=CURRENT_TIMESTAMP
            """,
            (
                f.key, f.domain, f.label, f.data_type, f.unit, f.description,
                f.default_mode, f.authority, f.sensitivity,
            ),
        )
    conn.commit()


def profile_schema_summary(conn: sqlite3.Connection) -> dict[str, object]:
    rows = conn.execute(
        "SELECT domain, COUNT(*) AS count FROM profile_field_definitions GROUP BY domain ORDER BY domain"
    ).fetchall()
    return {
        "field_count": sum(row["count"] for row in rows),
        "domains": {row["domain"]: row["count"] for row in rows},
    }
