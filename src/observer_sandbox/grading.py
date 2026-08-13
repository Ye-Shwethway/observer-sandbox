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


# Exemplar-only scheme for current 0..100 RAPS attribute values.
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
