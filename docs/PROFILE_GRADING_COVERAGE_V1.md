# Profile Grading Coverage v1

Status: IMPLEMENTED CANDIDATE / VALIDATION PENDING

## Purpose

Classify current profile surfaces so grading is applied only where its semantics are meaningful.

## Current coverage

- Attributes — `graded`: explicit compatible 0..100 fields use `raps-100-proof-v1`; IQ remains excluded.
- Skills — `graded`: represented `character_skills.score` values use `skill-proficiency-100-v1`; persisted `tier` is not grading authority.
- Body — `derived-grade candidate / partially graded`: raw size remains descriptive; v1 derives explicit reference metrics for waist/shoulders, waist/hips and waist/height plus context-only chest/waist.
- Appearance — `contextual-only`: PARS and appearance anchors remain represented but do not silently inherit RAPS grading.
- Recovery — `contextual-only`: fatigue/readiness are current condition/status surfaces, not quality grades by default.
- Personality — `not gradeable` by default.
- Preferences/Habits — `not gradeable` by default.
- Sexual Anatomy & Physiology — `contextual-only / not gradeable` by default; anatomy, drive, arousal and rolling activity counts do not receive quality grades merely because some values are numeric.
- Background — `not gradeable`.

## Body reference semantics

v1 deliberately separates aesthetics-oriented and health-oriented references:

- `body.waist_to_shoulders_ratio`: reference 0.55..0.65, centered around the ~0.6 adult-male preference reported in published attractiveness research.
- `body.waist_to_hips_ratio`: reference 0.80..0.90 from published adult-male attractiveness research.
- `body.waist_to_height_ratio`: reference 0.40..0.49 from NICE adult central-adiposity guidance.
- `body.chest_to_waist_ratio`: derived context only in v1 because the literature supports its relevance but this slice does not encode an unsupported single universal optimum.

These are reference interpretations, not biological laws. Future general-aesthetic, health, bodybuilding/classic-physique and modelling schemes may interpret the same authoritative body state differently.

## Authority boundary

Grades are read-time metadata only. No profile/skill grade column is introduced and no raw value is mutated by grading. Future career/quest/job/salary systems may consume grading results from the grading/query layer but must not make Telegram presentation authoritative.
