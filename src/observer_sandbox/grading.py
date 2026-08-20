from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Iterable, Mapping

from .physical_quantity import PhysicalQuantity


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
    domain: str | None = None
    dimension: str | None = None


@dataclass(frozen=True)
class GradeScheme:
    scheme_id: str
    family: str
    description: str
    domain: str | None = None
    dimension: str | None = None
    supported_grades: tuple[str, ...] = ()


@dataclass(frozen=True)
class GradeProfile:
    domain: str
    dimensions: Mapping[str, GradeResult]
    overall: GradeResult | None = None


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
GRADE_ORDER: Mapping[str, int] = {
    grade: index for index, (grade, _label) in enumerate(GRADE_VOCABULARY)
}
STANDARD_E_TO_S_GRADES = ("E", "D", "C", "B", "A", "S")

RAPS_100_PROOF_SCHEME_ID = "raps-100-proof-v1"
SKILL_PROFICIENCY_100_SCHEME_ID = "skill-proficiency-100-v1"
BODY_AESTHETIC_PROPORTION_SCHEME_ID = "body-aesthetic-proportion-v1"
BODY_CENTRAL_ADIPOSITY_SCHEME_ID = "body-central-adiposity-v1"
BODY_PHYSIQUE_COMPOSITE_SCHEME_ID = "body-physique-composite-v1"
ITEM_RESISTANCE_LOAD_SCHEME_ID = "item-resistance-load-v1"
LOCATION_COMPLETENESS_SCHEME_ID = "location-completeness-v1"

SCHEME_REGISTRY: Mapping[str, GradeScheme] = {
    RAPS_100_PROOF_SCHEME_ID: GradeScheme(
        RAPS_100_PROOF_SCHEME_ID,
        "monotonic",
        "Explicit 0..100 RAPS attribute proficiency/capability interpretation.",
        domain="character",
        dimension="attribute_capability",
        supported_grades=STANDARD_E_TO_S_GRADES,
    ),
    SKILL_PROFICIENCY_100_SCHEME_ID: GradeScheme(
        SKILL_PROFICIENCY_100_SCHEME_ID,
        "monotonic",
        "Explicit 0..100 learned-skill proficiency interpretation.",
        domain="character",
        dimension="skill_proficiency",
        supported_grades=STANDARD_E_TO_S_GRADES,
    ),
    BODY_AESTHETIC_PROPORTION_SCHEME_ID: GradeScheme(
        BODY_AESTHETIC_PROPORTION_SCHEME_ID,
        "target_range",
        "Reference-band interpretation of represented adult male torso proportions; not a universal beauty law.",
        domain="body",
        dimension="aesthetic_proportion",
        supported_grades=STANDARD_E_TO_S_GRADES,
    ),
    BODY_CENTRAL_ADIPOSITY_SCHEME_ID: GradeScheme(
        BODY_CENTRAL_ADIPOSITY_SCHEME_ID,
        "target_range",
        "Health-oriented waist-to-height central-adiposity reference interpretation.",
        domain="body",
        dimension="central_adiposity",
        supported_grades=STANDARD_E_TO_S_GRADES,
    ),
    BODY_PHYSIQUE_COMPOSITE_SCHEME_ID: GradeScheme(
        BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
        "composite",
        "Read-time composite across compatible body proportion/reference metrics.",
        domain="body",
        dimension="physique_composite",
        supported_grades=STANDARD_E_TO_S_GRADES,
    ),
    ITEM_RESISTANCE_LOAD_SCHEME_ID: GradeScheme(
        ITEM_RESISTANCE_LOAD_SCHEME_ID,
        "monotonic",
        "Project-defined classification of represented resistance-training item load; this describes the item and is not a Character strength requirement.",
        domain="item",
        dimension="resistance_load",
        supported_grades=STANDARD_E_TO_S_GRADES,
    ),
    LOCATION_COMPLETENESS_SCHEME_ID: GradeScheme(
        LOCATION_COMPLETENESS_SCHEME_ID,
        "ordinal",
        "Derived interpretation of the existing Location L0-L4 completeness contract; it is not access authorization or prestige.",
        domain="location",
        dimension="completeness",
        supported_grades=("E", "D", "C", "B", "A"),
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

# Thresholds are a simulation classification of the resistance load carried by
# one represented training item. They are intentionally not a statement about
# the actor capability required for any exercise or movement involving it.
ITEM_RESISTANCE_LOAD_BANDS_KG: tuple[GradeBand, ...] = (
    GradeBand(50.0 * 0.45359237, "S", GRADE_LABELS["S"]),
    GradeBand(35.0 * 0.45359237, "A", GRADE_LABELS["A"]),
    GradeBand(20.0 * 0.45359237, "B", GRADE_LABELS["B"]),
    GradeBand(10.0 * 0.45359237, "C", GRADE_LABELS["C"]),
    GradeBand(5.0 * 0.45359237, "D", GRADE_LABELS["D"]),
    GradeBand(0.0, "E", GRADE_LABELS["E"]),
)

LOCATION_COMPLETENESS_GRADES: Mapping[int, str] = {
    0: "E",
    1: "D",
    2: "C",
    3: "B",
    4: "A",
}

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


def grade_rank(grade: str) -> int:
    try:
        return GRADE_ORDER[str(grade)]
    except KeyError as exc:
        raise ValueError(f"Unknown grade: {grade!r}") from exc


def compare_grades(left: str, right: str) -> int:
    left_rank = grade_rank(left)
    right_rank = grade_rank(right)
    return (left_rank > right_rank) - (left_rank < right_rank)


def meets_minimum_grade(actual: str, minimum: str) -> bool:
    return grade_rank(actual) >= grade_rank(minimum)


def build_grade_profile(
    domain: str,
    dimensions: Mapping[str, GradeResult],
    *,
    overall: GradeResult | None = None,
) -> GradeProfile:
    normalized_domain = str(domain or "").strip().lower()
    if not normalized_domain:
        raise ValueError("Grade profile domain is required")
    normalized_dimensions = dict(dimensions)
    if not normalized_dimensions:
        raise ValueError("Grade profile requires at least one dimension")
    for key, result in normalized_dimensions.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Grade profile dimension keys must be non-empty strings")
        if not isinstance(result, GradeResult):
            raise TypeError("Grade profile dimensions must contain GradeResult values")
        scheme = grading_scheme(result.scheme_id)
        if scheme.domain is not None and scheme.domain != normalized_domain:
            raise ValueError(
                f"Grade scheme {scheme.scheme_id} belongs to {scheme.domain}, not {normalized_domain}"
            )
    if overall is not None:
        scheme = grading_scheme(overall.scheme_id)
        if scheme.family != "composite":
            raise ValueError("Grade profile overall result requires an explicit composite scheme")
        if scheme.domain is not None and scheme.domain != normalized_domain:
            raise ValueError(
                f"Overall grade scheme {scheme.scheme_id} belongs to {scheme.domain}, not {normalized_domain}"
            )
    return GradeProfile(normalized_domain, normalized_dimensions, overall)


def _evaluate_bands(value: float, *, scheme_id: str, bands: tuple[GradeBand, ...]) -> GradeResult:
    scheme = grading_scheme(scheme_id)
    for band in bands:
        if value >= band.minimum:
            return GradeResult(
                scheme_id=scheme_id,
                grade=band.grade,
                label=band.label,
                value=value,
                domain=scheme.domain,
                dimension=scheme.dimension,
            )
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


def evaluate_item_resistance_load(quantity: PhysicalQuantity) -> GradeResult:
    if not isinstance(quantity, PhysicalQuantity) or quantity.kind != "mass":
        raise ValueError("item-resistance-load-v1 requires a normalized mass quantity")
    return _evaluate_bands(
        quantity.base_value,
        scheme_id=ITEM_RESISTANCE_LOAD_SCHEME_ID,
        bands=ITEM_RESISTANCE_LOAD_BANDS_KG,
    )


def evaluate_location_completeness(level: int | str) -> GradeResult:
    if isinstance(level, bool):
        raise ValueError("location-completeness-v1 expects L0..L4")
    if isinstance(level, str):
        normalized = level.strip().upper()
        if not normalized.startswith("L") or not normalized[1:].isdigit():
            raise ValueError("location-completeness-v1 expects L0..L4")
        numeric = int(normalized[1:])
    elif isinstance(level, int):
        numeric = level
    else:
        raise ValueError("location-completeness-v1 expects L0..L4")
    try:
        grade = LOCATION_COMPLETENESS_GRADES[numeric]
    except KeyError as exc:
        raise ValueError("location-completeness-v1 expects L0..L4") from exc
    scheme = grading_scheme(LOCATION_COMPLETENESS_SCHEME_ID)
    return GradeResult(
        scheme_id=scheme.scheme_id,
        grade=grade,
        label=GRADE_LABELS[grade],
        value=float(numeric),
        domain=scheme.domain,
        dimension=scheme.dimension,
    )


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
    scheme = grading_scheme(scheme_id)
    return GradeResult(
        scheme_id=scheme_id,
        grade=grade,
        label=GRADE_LABELS[grade],
        value=numeric,
        domain=scheme.domain,
        dimension=scheme.dimension,
    )


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
        domain=base.domain,
        dimension=base.dimension,
    )
