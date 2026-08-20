from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Iterable, Mapping


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


@dataclass(frozen=True)
class GradeScheme:
    scheme_id: str
    family: str
    description: str


@dataclass(frozen=True)
class TargetRange:
    metric_key: str
    label: str
    low: float
    high: float
    evidence_note: str


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

RAPS_100_PROOF_SCHEME_ID = "raps-100-proof-v1"
SKILL_PROFICIENCY_100_SCHEME_ID = "skill-proficiency-100-v1"
BODY_AESTHETIC_PROPORTION_SCHEME_ID = "body-aesthetic-proportion-v1"
BODY_CENTRAL_ADIPOSITY_SCHEME_ID = "body-central-adiposity-v1"
BODY_PHYSIQUE_COMPOSITE_SCHEME_ID = "body-physique-composite-v1"

SCHEME_REGISTRY: Mapping[str, GradeScheme] = {
    RAPS_100_PROOF_SCHEME_ID: GradeScheme(
        RAPS_100_PROOF_SCHEME_ID,
        "monotonic",
        "Explicit 0..100 RAPS attribute proficiency/capability interpretation.",
    ),
    SKILL_PROFICIENCY_100_SCHEME_ID: GradeScheme(
        SKILL_PROFICIENCY_100_SCHEME_ID,
        "monotonic",
        "Explicit 0..100 learned-skill proficiency interpretation.",
    ),
    BODY_AESTHETIC_PROPORTION_SCHEME_ID: GradeScheme(
        BODY_AESTHETIC_PROPORTION_SCHEME_ID,
        "target_range",
        "Reference-band interpretation of represented adult male torso proportions; not a universal beauty law.",
    ),
    BODY_CENTRAL_ADIPOSITY_SCHEME_ID: GradeScheme(
        BODY_CENTRAL_ADIPOSITY_SCHEME_ID,
        "target_range",
        "Health-oriented waist-to-height central-adiposity reference interpretation.",
    ),
    BODY_PHYSIQUE_COMPOSITE_SCHEME_ID: GradeScheme(
        BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
        "composite",
        "Read-time composite across compatible body proportion/reference metrics.",
    ),
}

RAPS_100_PROOF_BANDS: tuple[GradeBand, ...] = (
    GradeBand(90.0, "S", GRADE_LABELS["S"]),
    GradeBand(75.0, "A", GRADE_LABELS["A"]),
    GradeBand(60.0, "B", GRADE_LABELS["B"]),
    GradeBand(40.0, "C", GRADE_LABELS["C"]),
    GradeBand(20.0, "D", GRADE_LABELS["D"]),
    GradeBand(0.0, "E", GRADE_LABELS["E"]),
)

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

# These reference bands are intentionally modest and explicit. They are not a
# claim that one immutable ratio defines human attractiveness. WSR/WHR are
# grounded in adult-male attractiveness literature; WHtR is a separate health
# reference and is not merged into an aesthetics-only claim.
BODY_REFERENCE_RANGES: Mapping[str, TargetRange] = {
    "body.waist_to_shoulders_ratio": TargetRange(
        "body.waist_to_shoulders_ratio",
        "Waist / Shoulders",
        0.55,
        0.65,
        "Adult male attractiveness literature reports a preferred waist-to-shoulder ratio around 0.6.",
    ),
    "body.waist_to_hips_ratio": TargetRange(
        "body.waist_to_hips_ratio",
        "Waist / Hips",
        0.80,
        0.90,
        "Adult male attractiveness literature reports a preferred waist-to-hip range around 0.8-0.9.",
    ),
    "body.waist_to_height_ratio": TargetRange(
        "body.waist_to_height_ratio",
        "Waist / Height",
        0.40,
        0.49,
        "NICE adult central-adiposity guidance classifies 0.4-0.49 as healthy.",
    ),
}


def grading_scheme(scheme_id: str) -> GradeScheme:
    try:
        return SCHEME_REGISTRY[scheme_id]
    except KeyError as exc:
        raise KeyError(f"Unknown grading scheme: {scheme_id}") from exc


def _evaluate_bands(value: float, *, scheme_id: str, bands: tuple[GradeBand, ...]) -> GradeResult:
    for band in bands:
        if value >= band.minimum:
            return GradeResult(scheme_id=scheme_id, grade=band.grade, label=band.label, value=value)
    raise AssertionError("grading bands do not cover the configured range")


def evaluate_raps_100(value: float | int) -> GradeResult:
    numeric = float(value)
    if numeric < 0.0 or numeric > 100.0:
        raise ValueError("raps-100-proof-v1 expects a value in the inclusive range 0..100")
    return _evaluate_bands(numeric, scheme_id=RAPS_100_PROOF_SCHEME_ID, bands=RAPS_100_PROOF_BANDS)


def evaluate_skill_score(value: float | int) -> GradeResult:
    numeric = float(value)
    if numeric < 0.0 or numeric > 100.0:
        raise ValueError("skill-proficiency-100-v1 expects a value in the inclusive range 0..100")
    return _evaluate_bands(numeric, scheme_id=SKILL_PROFICIENCY_100_SCHEME_ID, bands=RAPS_100_PROOF_BANDS)


def evaluate_attribute_field(field_key: str, value: object) -> GradeResult | None:
    if field_key not in ATTRIBUTE_RAPS_100_FIELDS or not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    return evaluate_raps_100(value)


def evaluate_profile_field(field_key: str, value: object) -> GradeResult | None:
    """Route only explicitly opted-in ordinary profile fields to a scheme."""
    return evaluate_attribute_field(field_key, value)


def aggregate_raps_100(results: Iterable[GradeResult]) -> GradeResult | None:
    values = [float(result.value) for result in results if result.scheme_id == RAPS_100_PROOF_SCHEME_ID]
    if not values:
        return None
    return evaluate_raps_100(fmean(values))


def aggregate_skill_100(results: Iterable[GradeResult]) -> GradeResult | None:
    values = [float(result.value) for result in results if result.scheme_id == SKILL_PROFICIENCY_100_SCHEME_ID]
    if not values:
        return None
    return evaluate_skill_score(fmean(values))


def _target_distance_fraction(value: float, target: TargetRange) -> float:
    if target.low <= value <= target.high:
        return 0.0
    edge = target.low if value < target.low else target.high
    center = (target.low + target.high) / 2.0
    return abs(value - edge) / max(center, 1e-9)


def evaluate_target_range(value: float | int, target: TargetRange, *, scheme_id: str) -> GradeResult:
    numeric = float(value)
    distance = _target_distance_fraction(numeric, target)
    if distance == 0.0:
        grade = "S"
    elif distance <= 0.05:
        grade = "A"
    elif distance <= 0.10:
        grade = "B"
    elif distance <= 0.20:
        grade = "C"
    elif distance <= 0.35:
        grade = "D"
    else:
        grade = "E"
    return GradeResult(scheme_id=scheme_id, grade=grade, label=GRADE_LABELS[grade], value=numeric)


def _number(values: Mapping[str, object], key: str) -> float | None:
    value = values.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    return float(value)


def derive_body_grade_items(values: Mapping[str, object]) -> list[dict[str, object]]:
    """Derive gradeable body relationships without grading raw size itself."""
    height = _number(values, "body.height_in")
    shoulders = _number(values, "body.shoulders_in")
    waist = _number(values, "body.waist_in")
    hips = _number(values, "body.hips_in")
    if waist is None or waist <= 0:
        return []

    derived: list[dict[str, object]] = []

    def add_ratio(metric_key: str, numerator: float | None, denominator: float | None, scheme_id: str) -> None:
        if numerator is None or denominator is None or denominator <= 0:
            return
        ratio = numerator / denominator
        target = BODY_REFERENCE_RANGES[metric_key]
        derived.append(
            {
                "kind": "derived_grade",
                "field_key": metric_key,
                "domain": "body",
                "label": target.label,
                "value": round(ratio, 3),
                "data_type": "number",
                "unit": "ratio",
                "mode": "derived",
                "grade_result": evaluate_target_range(ratio, target, scheme_id=scheme_id),
                "reference_range": [target.low, target.high],
                "reference_note": target.evidence_note,
            }
        )

    add_ratio(
        "body.waist_to_shoulders_ratio",
        waist,
        shoulders,
        BODY_AESTHETIC_PROPORTION_SCHEME_ID,
    )
    add_ratio(
        "body.waist_to_hips_ratio",
        waist,
        hips,
        BODY_AESTHETIC_PROPORTION_SCHEME_ID,
    )
    add_ratio(
        "body.waist_to_height_ratio",
        waist,
        height,
        BODY_CENTRAL_ADIPOSITY_SCHEME_ID,
    )
    return derived


def aggregate_body_grades(items: Iterable[dict[str, object]]) -> GradeResult | None:
    """Composite compatible grade letters without pretending raw ratios share one numeric scale."""
    grade_scores = {"E": 10.0, "D": 30.0, "C": 50.0, "B": 67.5, "A": 82.5, "S": 95.0}
    scores: list[float] = []
    for item in items:
        result = item.get("grade_result")
        if isinstance(result, GradeResult) and result.grade in grade_scores:
            scores.append(grade_scores[result.grade])
    if not scores:
        return None
    numeric = fmean(scores)
    base = _evaluate_bands(numeric, scheme_id=BODY_PHYSIQUE_COMPOSITE_SCHEME_ID, bands=RAPS_100_PROOF_BANDS)
    return GradeResult(
        scheme_id=BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
        grade=base.grade,
        label=base.label,
        value=numeric,
    )
