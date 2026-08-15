# Universal Profile Grading Framework v1

Status: IMPLEMENTED / PRE-MERGE VALIDATED

## Purpose

Complete grading as a reusable profile-wide interpretation layer before Skill Progression begins.

The authoritative state remains the underlying profile/skill/body value. Grades are derived at read time and are never independently persisted truth.

Core invariant:

`authoritative current value(s) + explicit named grading scheme + scheme-specific context -> derived grade metadata -> profile/query consumers -> Telegram / future unlock systems`

Future career, quest, job, salary and progression systems may consume grade results, but must not make Telegram presentation the authority.

## Shared vocabulary

Canonical cross-domain vocabulary remains:

- E — Beginner
- D — Novice
- C — Capable
- B — Skilled
- A — Advanced
- S — Expert
- SS — Elite
- SSS — Master
- X — Mythic
- XX — Transcendent

A grading scheme may expose only a legitimate subset. Current 0..100 RAPS and skill schemes use E..S; SS..XX are not compressed into that range.

## Explicit scheme registry

`src/observer_sandbox/grading.py` now owns an explicit named registry. Numeric fields do not silently inherit grading.

Implemented scheme families/IDs:
- `raps-100-proof-v1` — monotonic 0..100 Attributes;
- `skill-proficiency-100-v1` — monotonic 0..100 learned-skill proficiency;
- `body-aesthetic-proportion-v1` — target-range interpretation for selected body ratios;
- `body-central-adiposity-v1` — target-range health interpretation for waist/height;
- `body-physique-composite-v1` — read-time composite across compatible body reference grades.

The architecture remains extensible to later target-proximity/reference-distribution/context-specific schemes without changing authoritative raw state.

## Attributes

The proven 36-field `raps-100-proof-v1` behavior is preserved unchanged:
- S >= 90;
- A >= 75;
- B >= 60;
- C >= 40;
- D >= 20;
- E >= 0.

IQ remains excluded because its scale semantics differ. Compatible Attribute group/overall grades remain read-time derived values.

## Skills

Represented `character_skills.score` values now receive read-time `skill-proficiency-100-v1` grades and a current Skills overall presentation grade.

Example:
`Hand To Hand Combat   90 (S) · Expert`

Persisted `tier`, `score`, and `experience` are not mutated by grading. Skill Progression will separately reconcile their progression authority; this slice does not implement learning/progression.

## Body and physique grading

Raw body dimensions remain descriptive and ungraded. v1 grades selected derived relationships instead of applying `larger = better`.

Implemented references:
- `body.waist_to_shoulders_ratio` — 0.55..0.65 reference band, centered around the ~0.6 adult-male preference reported in published attractiveness research;
- `body.waist_to_hips_ratio` — 0.80..0.90 reference band from adult-male attractiveness research;
- `body.waist_to_height_ratio` — 0.40..0.49 health-oriented reference from NICE adult central-adiposity guidance;
- `body.chest_to_waist_ratio` — derived context only in v1; no unsupported exact universal optimum is encoded.

These are bounded reference interpretations, not universal biological beauty laws. No popularized golden-ratio constant is encoded.

Target-range grading is non-linear: values inside the reference band receive the top grade for that scheme, while deviation in either direction reduces the grade. Raw height, weight, chest, waist, shoulders, hips, limbs and other circumferences are not independently quality-graded.

Body overall grade is a read-time composite of compatible derived reference grades. Future general-aesthetic, health, classic-bodybuilding and modelling schemes may interpret the same authoritative body state differently.

## Profile coverage

Canonical coverage classification: `docs/PROFILE_GRADING_COVERAGE_V1.md`.

Current surfaces are explicitly classified as graded, derived/contextual, or not gradeable so personality, preferences, recovery status, intimate anatomy/activity counts and other numeric fields do not receive meaningless grades by accident.

## Telegram/query architecture

- grading logic lives outside Telegram;
- profile query attaches derived grade metadata;
- Telegram renders that metadata generically for Attributes, Skills and applicable Body derived rows;
- ratios use dedicated display precision without changing ordinary profile numeric formatting;
- no grade column or grade mutation is introduced.

## Validation

Final runtime candidate before documentation-only synchronization: `5d893ff58429d9ccc53c57c04c73788319791250`.

Green evidence on that candidate:
- CI #765 / run `31865573821`: SUCCESS;
- Read-Only Grading Proof Acceptance #28 / run `31865573852`: SUCCESS;
- Attribute Grading Batch 1 Acceptance #27 / run `31865573805`: SUCCESS on a disposable production copy;
- Public Readiness Security Audit #52 / run `31865573804`: SUCCESS.

The production-copy acceptance proves existing Attribute grading, raw Body non-grading, derived Body grading, separate Skill grading, Telegram rendering, zero model calls, and unchanged profile/skill persisted state. The VPS-backed PR acceptance is restricted to same-repository pull requests.

## Boundaries

v1 does not:
- persist grades as competing authoritative state;
- grade every numeric field;
- treat raw body size as linear quality;
- conflate health, aesthetics, bodybuilding and modelling criteria;
- encode an unsupported universal body-proportion constant;
- mutate Skill scores/tier/experience;
- introduce careers, quests, jobs, salary, economy, endocrine or relationship systems.

After deployment/closure, the next development family is Skill Progression Foundation v1.
