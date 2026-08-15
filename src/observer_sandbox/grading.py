from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Iterable


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


# Canonical shared vocabulary. Individual grading schemes may expose only a
# bounded subset when their underlying scale cannot legitimately reach the
# higher tiers.
GRADE_VOCABULARY: tuple[tuple[str, str], ...] = (
    ("E", "Beginner"),
    ("D", "Novice"),
    ("C", "Capable"),
    ("B", "Skilled"),
    ("A", "Advanced"),
    ("S", "Expert"),
    ("SS", "Elite"),
    ("SSS", "Master"),
    ("X", "Mythic"),
    ("XX", "Transcendent"),
)

GRADE_LABELS = dict(GRADE_VOCABULARY)


# Current 0..100 RAPS scheme. Preserve its proven thresholds; only the labels
# are aligned with the canonical cross-domain vocabulary. Higher tiers remain
# available to future schemes with wider/higher-cap scales.
RAPS_100_PROOF_SCHEME_ID = "raps-100-proof-v1"
RAPS_100_PROOF_BANDS: tuple[GradeBand, ...] = (
    GradeBand(90.0, "S", GRADE_LABELS["S"]),
    GradeBand(75.0, "A", GRADE_LABELS["A"]),
    GradeBand(60.0, "B", GRADE_LABELS["B"]),
    GradeBand(40.0, "C", GRADE_LABELS["C"]),
    GradeBand(20.0, "D", GRADE_LABELS["D"]),
    GradeBand(0.0, "E", GRADE_LABELS["E"]),
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


def aggregate_raps_100(results: Iterable[GradeResult]) -> GradeResult | None:
    """Grade the arithmetic mean of compatible current attribute evaluations."""
    values = [float(result.value) for result in results if result.scheme_id == RAPS_100_PROOF_SCHEME_ID]
    if not values:
        return None
    return evaluate_raps_100(fmean(values))
