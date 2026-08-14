# Body Measurement Progression v1

Status: BC-3 implementation contract

## Purpose

BC-3 turns authored body circumferences into deterministic simulated profile state without pretending that circumference can be inferred from body weight alone.

Invariant:

`BC-2 bounded body-composition settlement + regional resistance evidence + authored anatomy/genetic envelope -> bounded regional measurement settlement -> atomic profile history + event`

BC-3 is downstream of BC-2. It does not create a second nutrition, calorie, body-composition or hypertrophy authority.

## Scope

Target family:
- neck;
- shoulders;
- chest;
- waist;
- hips when an authored baseline/envelope exists;
- biceps relaxed/flexed;
- triceps;
- forearms;
- thighs;
- calves.

Darian is the first rich fixture, not the reusable engine identity.

## Evidence model

BC-3 consumes completed `body_composition_progression_settled` events. Those events provide the coupled FM/FFM body-composition signal for a bounded BC-2 window.

Regional hypertrophy is not treated as uniform. Completed resistance-training events inside the same BC-2 window are mapped from data-driven training method semantics to regional exposure weights. Non-resistance work does not create a regional hypertrophy signal.

Research direction supporting this approximation includes evidence that resistance-training hypertrophy can be regionally non-uniform and associated with regional muscle activation, while changes in adiposity are associated with regional circumference changes. The implementation therefore separates whole-body composition effects from regional resistance exposure instead of mapping body-weight delta uniformly across every circumference.

This remains a bounded deterministic approximation, not an exact anthropometric predictor.

## Activation boundary

First BC-3 activation:
- preserves every available authored circumference numerically;
- switches eligible fields to `simulated` / `body_progression_engine`;
- records an activation event and cursor;
- never invents a missing measurement or genetic envelope.

A BC-2 settlement window that began before the BC-3 activation boundary is advanced as `deferred_partial_pre_activation_window` with no measurement mutation. This prevents retroactive progression.

## Projection semantics

Each measurement policy contains:
- anatomical region;
- optional authored genetic muscular maximum or waist target;
- adiposity elasticity;
- lean-loss elasticity;
- per-window absolute change guard.

Positive general FFM change can use remaining authored muscular headroom. Resistance-specific FFM gain is additionally weighted by the region's training exposure. Negative FFM can reduce muscular circumference according to the field's lean-loss elasticity. Fat-mass change contributes separately using regional adiposity elasticity; waist is intentionally more adiposity-sensitive than limb circumferences.

Genetic circumference maxima represent muscular/lean-condition potential rather than a claim that fat-associated circumference can never exceed the number. Final values are still bounded by activation-relative safety guards and per-window clamps.

For waist, `genetics.waist_target_in` acts as the lower lean-condition target when fat mass is falling. Fat gain may increase waist above that target.

## Missing hips evidence

The universal profile schema supports `body.hips_in`, but Darian currently has neither an authored hip baseline nor `genetics.hips_max_in`. BC-3 therefore reports hips as deferred and does not fabricate a value. A future character or future canonical Darian update may activate hips once both required facts exist.

## Persistence

All changed measurement fields in one settlement are written inside one SQLite savepoint:
- current profile value;
- `character_profile_history` row;
- one `body_measurement_progression_settled` event linked to the causal BC-2 event.

No schema migration is required. No LLM call is used. Telegram Profile Body automatically observes the existing body-domain profile values after activation.

## Validation

Focused tests cover:
- activation preserves authored measurements;
- absent hips are not invented;
- partial pre-activation BC-2 windows cannot mutate measurements;
- a full post-activation window combines body composition with regional resistance exposure;
- upper-body bench evidence affects chest/triceps more than unexposed calves;
- waist responds independently to fat-mass change;
- batched history/event persistence is atomic and bounded.

The stateful acceptance lane runs the candidate code against a disposable production database copy only. It bootstraps BC-3 without numerical change, proves the non-retroactive boundary, injects synthetic future evidence on the copy, verifies one regional settlement, and never mutates production.

## Deferred

BC-3 does not add:
- detailed muscle-by-muscle anatomy;
- bone-remodeling simulation;
- fluid/glycogen circumference noise;
- endocrine simulation;
- image/appearance grading;
- a Mind or Behavior Engine;
- an extra model call.
