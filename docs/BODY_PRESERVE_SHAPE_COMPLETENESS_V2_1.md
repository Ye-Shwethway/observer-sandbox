# Body Preserve Shape Completeness v2.1

Status: IMPLEMENTATION CONTRACT
Date: 2026-08-19

## Purpose

Close the gap between Body Aesthetic Proportion & Grade Targeting v2 design and the current minimum inverse solver.

The v2 solver can reach a requested Body grade by moving the active grade-driving torso measurements, but Preserve Shape must preserve the whole represented muscular silhouette rather than leaving neck, arms, forearms, thighs and calves behind at unrelated scales.

Canonical goal:

`requested Body grade -> primary ratio candidate -> registry-driven whole-body projection -> secondary-ratio drift scoring -> forward Body grade verification -> preview -> Apply`

Raw represented measurements remain authoritative. Grades remain read-time derived. No LLM is used.

## Scope

This slice upgrades Body Grade Targeting only. It does not redesign the Body aesthetic grading bands, progression rates, physiology, genetics or Mind Engine.

### Hard anchors

Remain unchanged:
- `body.height_in`;
- represented sex/reference-profile selector;
- skeletal/genetic facts outside the ordinary Body measurement vector.

### Primary grade drivers

The existing sex-aware Body aesthetic registry remains authoritative for grade-driving ratios.

For the current male v2 profile these are driven by:
- waist;
- chest;
- shoulders;
- hips.

For female profiles, only represented metrics already activated by the sex-aware Body registry may drive grade targeting.

### Proportional dependent fields

When represented and writable, Preserve Shape projects dependent soft-tissue measurements from the solved primary vector:
- neck;
- relaxed biceps;
- flexed biceps;
- triceps;
- forearms;
- thighs;
- calves.

Relationships are data-driven through `config/body_shape_preservation.v2.json`, not character-name branches or scattered field-name rules.

Missing dependent fields are skipped; values are never invented.

## Cleaner solver architecture

Do not brute-force every Body field independently.

That would create a large search space and make the result harder to reason about. Instead use a bounded two-layer deterministic optimizer:

1. **Primary search** — solve only the active grade-driving ratio family using the existing bounded candidate search.
2. **Whole-body projection** — for every primary candidate, project represented dependent measurements using weighted regional scale anchors from the preservation registry.
3. **Objective scoring** — score raw movement plus drift in configured secondary ratios.
4. **Forward verification** — run the ordinary sex-aware Body evaluator on the completed candidate and accept only candidates that actually produce the requested grade.

This keeps search bounded while making the candidate section-wide and proportionally coherent.

## Projection rule

For a dependent measurement, compute each available anchor's scale:

`anchor_scale = proposed_anchor / current_anchor`

Combine available anchor scales with a weighted geometric mean, then apply that scale to the dependent field:

`new_dependent = old_dependent * exp(sum(weight_i * ln(anchor_scale_i)) / sum(weight_i))`

A geometric blend is used because Body dimensions are multiplicative scale relationships. It avoids directional bias from arithmetic averaging of percentage changes.

Dependent rules are ordered so one projected field may serve as an anchor for a later field, for example:

`torso -> biceps -> forearms`

and

`hips/waist -> thighs -> calves`.

## Objective

For each candidate:

`objective = raw_change_cost + secondary_ratio_drift_cost + primary_ratio_direction_cost`

Raw change cost uses normalized squared movement with registry-defined penalties. Frame-sensitive shoulder and hip measurements retain stronger movement penalties.

Secondary ratio drift compares current and candidate ratios such as:
- neck/chest;
- biceps/chest;
- forearm/biceps;
- thigh/hip;
- calf/thigh.

These are preservation constraints, not aesthetic grade authority. They do not become scientifically universal attractiveness bands and do not contribute to the Body composite.

Preserve Shape uses the full configured drift penalty. Normalize keeps the same anatomical projection but uses a weaker preservation penalty so the grade-driving target may move more assertively toward its deterministic target region.

## Body-section completeness boundary

Section-wide does not mean mutate every Body-domain field indiscriminately.

The solver must distinguish:
- hard anchors;
- grade-driving measurements;
- proportional soft-tissue dependents;
- independent physiology/context values such as body-fat percentage;
- deterministic derived values such as BMI, lean mass and fat mass.

Independent physiology/context and deterministic derived fields are not changed merely to make a visual proportion solver look complete. They remain owned by their normal authority unless a future explicit contract couples them to Body inverse targeting.

The completeness requirement for v2.1 is therefore:

> every represented writable circumference measurement participating in the character's visible muscular silhouette is either a primary solved field, a projected proportional dependent, or explicitly excluded by registry policy.

## Preview

Preview must continue to show every raw mutation that Apply will perform.

It also exposes preservation metadata including:
- preservation registry revision;
- represented projected dependent fields;
- hard anchors;
- requested mode.

A normal male Body target should no longer show only chest/waist/shoulders/hips when other represented circumference fields exist and require proportional follow-through.

## Acceptance

Disposable acceptance must prove:

1. A male Preserve target reaches the requested Body grade through ordinary forward evaluation.
2. Height remains unchanged.
3. Represented neck, relaxed/flexed biceps, triceps, forearms, thighs and calves are projected when their regional anchors move.
4. The proposal contains those actual raw changes and Apply remains atomic.
5. Configured secondary-ratio drift remains materially smaller than leaving dependent measurements frozen against the same primary candidate.
6. Female targeting uses the same generic preservation machinery without reusing male grade-driving semantics.
7. Missing dependent measurements are skipped rather than fabricated.
8. Normalize remains deterministic and forward-verifiable.
9. No schema migration is required.
10. No production Darian mutation is required for acceptance.

## Non-goals

- no new attractiveness research bands;
- no persisted Body grade;
- no automatic weight/body-fat mutation;
- no progression-rate calibration in this slice;
- no character-specific Darian body solver;
- no schema migration;
- no Mind or cognition behavior.
