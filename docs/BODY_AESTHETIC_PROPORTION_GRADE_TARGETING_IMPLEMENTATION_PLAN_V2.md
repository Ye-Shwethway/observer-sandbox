# Body Aesthetic Proportion & Grade Targeting v2 — Implementation Plan

Status: **APPROVED IMPLEMENTATION PLAN — DOCS FIRST**

Canonical design:
`docs/BODY_AESTHETIC_PROPORTION_GRADE_TARGETING_V2.md`

Parent control contract:
`docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`

Telegram edit-session contract:
`docs/TELEGRAM_CREATOR_PROFILE_EDIT_UX_V1.md`

## Goal

Add deterministic Body Measurements grade targeting to the existing Creator Profile Edit flow while preserving:
- raw measurements as authority;
- sex-aware proportion grading;
- project/evidence calibration transparency;
- preserve-shape default behavior;
- preview-first atomic Creator control;
- automatic pause lifecycle already implemented by the Telegram editor;
- no LLM dependence;
- no character-specific code.

## Phase 1 — Forward Body grading v2

Refine the current Body grading model before any inverse solver exists.

Required changes:
1. introduce an explicit sex-aware body reference-profile registry;
2. promote male `waist/chest` from context-only to a grade-driving target-range metric;
3. retain male waist/shoulders and waist/hips with corrected evidence/calibration metadata;
4. separate waist/height into health/context evaluation rather than aesthetic-composite weighting;
5. support female metric selection through the same registry;
6. use only represented female inputs; never synthesize missing bust/underbust/body-volume fields;
7. replace the current equal grade-letter average with a weighted, coverage-aware Body aesthetic composite;
8. expose active metric coverage and calibration metadata to the Profile renderer/diagnostics where useful.

No persisted grade state.

## Phase 2 — Deterministic inverse solver

Add a bounded module responsible only for proposing raw measurements.

Conceptual API:

```text
preview_body_grade_target(
    conn,
    character_id,
    target_grade,
    mode="preserve_shape",
) -> proposal
```

The solver must:
- load authoritative represented body measurements;
- select the reference profile generically;
- determine active grade-driving ratios;
- preserve hard anchors;
- minimize normalized measurement movement in Preserve mode;
- use a deterministic bounded search/optimization strategy;
- recompute all ratios using the ordinary forward evaluator;
- reject if requested grade is not achieved;
- return a proposal only; never mutate directly.

### Solver determinism

Identical authoritative input + same target grade + same mode must produce identical proposed measurements.

Do not depend on random seeds or LLM output.

### Preserve objective

Prefer the nearest valid measurement vector.

The implementation does not need a heavyweight optimization dependency if a bounded deterministic coordinate/search method can satisfy the contract cleanly.

Avoid over-engineering.

## Phase 3 — Creator proposal/apply integration

Extend the existing generic Creator profile proposal system rather than creating a Body-specific mutation authority.

Proposal must include:
- `kind = body_grade_target`;
- character id;
- selected reference profile;
- target grade;
- target mode;
- current/projected composite;
- current/projected active ratios;
- raw measurement changes;
- unchanged anchors;
- coverage metadata;
- calibration/evidence notes sufficient for diagnostics;
- stale-state fingerprints for every affected raw input.

Apply must reuse the existing atomic mutation/reconciliation path.

No Body grade value is persisted.

## Phase 4 — Telegram UX

Extend the existing native paused editor:

`Characters -> Character -> Profile -> Edit Profile -> Body Measurements -> Grade Target`

Owner-only.

Expected flow:
1. Body Measurements screen shows `🎯 Grade Target`;
2. choose target E/D/C/B/A/S;
3. choose `Preserve Shape` (default) or `Normalize`;
4. preview lists ratio/composite and raw measurement changes;
5. Apply / Cancel;
6. Apply keeps universe paused;
7. Done Editing restores pre-edit pause state.

No new command is required for the preferred UX. A command fallback may be added only if it reuses the same service and materially improves diagnostics/manual control.

## Initial male minimum

Targetable raw set:
- height — hard anchor;
- shoulders — soft anchor;
- chest — adjustable;
- waist — adjustable;
- hips — soft/adjustable subject to registry.

Primary aesthetic ratios:
- waist/chest;
- waist/shoulders;
- waist/hips.

Initial composite weights:
- waist/chest 0.45;
- waist/shoulders 0.35;
- waist/hips 0.20.

Waist/height is separate health/context output.

Secondary limb ratios may initially be used only as preservation penalties rather than grade-driving metrics.

## Initial female minimum

Targetable minimum represented set:
- height — hard anchor;
- waist — adjustable;
- hips — soft/adjustable.

Primary initial aesthetic ratio:
- waist/hips.

Richer metrics are automatically eligible only when their canonical raw inputs exist and their calibration is registered.

The female composite must expose metric coverage; it must not pretend a one-metric evaluation has the same evidentiary richness as a multi-metric evaluation.

## Calibration checkpoint

Before runtime merge, focused fixtures must cover representative:
- male lean/aesthetic;
- male average;
- male disproportionate;
- female proportion examples using represented inputs;
- boundary values around every enabled target band.

The purpose is to catch discontinuities and solver distortion, not to build a giant aesthetic benchmark suite.

If the recommended initial project bands create obviously unstable or counterintuitive grade jumps in fixtures, adjust the project calibration in the same PR and document the reason. Do not silently present the adjustment as new scientific evidence.

## Tests

Focused acceptance should cover:

### Forward grading
- male WCR grade-driving;
- male weighted composite;
- female registry selection;
- missing metric coverage;
- health-context separation;
- target-band boundaries.

### Inverse solver
- target B Preserve from a high-grade male fixture;
- target A Preserve from a lower-grade fixture;
- Normalize target correctness;
- hard-anchor preservation;
- deterministic repeatability;
- bounded/raw validity;
- insufficient-data rejection;
- target forward verification.

### Creator integration
- no mutation before Apply;
- stale proposal rejection;
- atomic multi-field mutation;
- grading recomputes from new raw values;
- notification baseline reconciliation remains correct;
- unrelated Memory unchanged.

### Telegram
- owner-only Body Grade Target button;
- edit session remains paused through preview/apply;
- Apply does not resume;
- Done Editing restores previous pause state;
- allowed user remains read-only.

Final repository CI is required once the bounded implementation is complete.

## Schema expectation

Prefer **no schema migration**.

Reference profiles/calibration should be code/config registry data unless inspection proves durable schema state is genuinely required.

Do not add a persisted Body-grade table merely for inverse targeting.

## Deployment/production proof

Production deploy is runtime-affecting and follows the normal main-branch deploy workflow.

Do not change Darian's real production measurements solely for acceptance.

Production verification should prove:
- service healthy;
- schema remains valid;
- Telegram Body Grade Target UX is reachable for Creator;
- read-only current Body grading renders correctly.

A real production measurement correction is only performed if the Creator deliberately chooses one.

## Completion condition

This refinement is complete when:
- forward Body grading v2 is sex-aware and weighted;
- male chest/waist participates canonically;
- Body grade targeting can deterministically produce valid raw measurement proposals;
- Preserve is the default and demonstrably preserves shape better than arbitrary single-field distortion;
- Telegram native Body target UX is wired into the paused Profile editor;
- CI is green;
- runtime merge/deploy evidence is reconciled;
- continuity docs return exact next implementation to MIND-F2.
