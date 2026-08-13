from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GradeBand:
    minimum: float
    grade: str
    label: str


@dataclass(frozen=True)
class GradeResult:
    scheme_id: str
    grade: str
    label: str
    value: float


# Current proof scheme for explicitly opted-in 0..100 RAPS-style attributes.
# It proves the derived-grading architecture without freezing the future
# universal cross-domain tier vocabulary.
RAPS_100_PROOF_SCHEME_ID = "raps-100-proof-v1"
RAPS_100_PROOF_BANDS: tuple[GradeBand, ...] = (
    GradeBand(90.0, "S", "Exceptional"),
    GradeBand(75.0, "A", "Advanced"),
    GradeBand(60.0, "B", "Strong"),
    GradeBand(40.0, "C", "Capable"),
    GradeBand(20.0, "D", "Developing"),
    GradeBand(0.0, "E", "Foundational"),
)

# Explicit batch membership prevents future fields from silently inheriting a
# grading scheme merely because they happen to be numeric or share a domain.
ATTRIBUTE_RAPS_100_FIELDS: frozenset[str] = frozenset(
    {
        "raps_pa.strength",
        "raps_pa.stamina",
        "raps_pa.agility",
        "raps_pa.speed",
        "raps_pa.reflexes",
        "raps_pa.endurance",
        "raps_pa.flexibility",
        "raps_pa.combat_skill",
        "raps_pa.weapons_proficiency",
        "raps_pa.survival_skill",
        "raps_pa.powerlifting_capacity",
        "raps_pa.focus_precision",
        "raps_pa.practical_skills",
        "raps_ma.confidence",
        "raps_ma.resilience",
        "raps_ma.adaptability",
        "raps_ma.emotional_stability",
        "raps_ma.focus",
        "raps_ma.leadership",
        "raps_ma.stress_management",
        "raps_ma.curiosity",
        "raps_ma.tactical_leadership",
        "raps_ia.problem_solving",
        "raps_ia.tactical_thinking",
        "raps_ia.creativity",
        "raps_ia.technological_aptitude",
        "raps_ia.medical_knowledge",
        "raps_ia.social_intelligence",
        "raps_ia.strategic_ingenuity",
        "social.charisma",
        "social.emotional_intelligence",
        "raps_vc.tone_resonance",
        "raps_vc.wit_humor",
        "raps_vc.persuasion",
        "raps_vc.empathy_in_speech",
        "raps_vc.overall",
    }
)


def evaluate_raps_100(value: float | int) -> GradeResult:
    numeric = float(value)
    if numeric < 0.0 or numeric > 100.0:
        raise ValueError("raps-100-proof-v1 expects a value in the inclusive range 0..100")
    for band in RAPS_100_PROOF_BANDS:
        if numeric >= band.minimum:
            return GradeResult(
                scheme_id=RAPS_100_PROOF_SCHEME_ID,
                grade=band.grade,
                label=band.label,
                value=numeric,
            )
    raise AssertionError("grading bands do not cover the configured range")


def evaluate_attribute_field(field_key: str, value: object) -> GradeResult | None:
    if field_key not in ATTRIBUTE_RAPS_100_FIELDS or not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    return evaluate_raps_100(value)
