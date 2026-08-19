# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-19

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve world truth, exposure, perception, memory, Mind and action-authority separation.
- Use minimum-runnable reversible slices; prefer exemplar-first, then batch-by-pattern.
- Character-specific behavioral hard-coding is forbidden.
- Persistent branches are only `main` and `test`; normal development occurs on `test` and is promoted after validation.
- Prefer vertical completeness and operational usefulness over subsystem sprawl.
- Reconcile roadmap/bootstrap at material checkpoints and do not claim production without deploy/runtime evidence.
- Do not seed another real production character merely to test unfinished foundations.

## Current canonical repository checkpoint

**Body Aesthetic Proportion & Grade Targeting v2 is IMPLEMENTED / CI-GREEN / MERGED. Exact newer production deploy verification is still pending independent evidence.**

Verified repository evidence:
- PR #275 — `Add Body aesthetic grade targeting v2`
- final head `9cd286b95f81f1f5849e5c089be0abdeeb472ccd`
- CI #1064 / run `32221713304`: **SUCCESS**
- Read-Only Grading Proof Acceptance #56: **SUCCESS**
- Attribute Grading Batch 1 Acceptance #55: **SUCCESS**
- merge `cb68d51125610fc52cc146c0d69910257ebd7258`
- no schema migration; schema remains v15.

Initial CI #1062 reached `782 passed / 1 failed`. The single failure was the existing display expectation `Chest / Waist: 1.364`. V2 deliberately makes `Waist / Chest` the grade-driving male metric, but the approved design also allows the intuitive inverse display. The final fix preserves `Chest / Waist` as derived display context only; it does not participate in Body scoring. Final CI #1064 is green.

Latest independently verified production remains Perception Foundation v1 / Deploy #289 until newer push-deploy/runtime evidence is available. Do not invent a deploy number or success state.

## Creator Character Profile Editing & Grade Targeting

Canonical docs:
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_ACCEPTANCE_V1.md`
- `docs/TELEGRAM_CREATOR_PROFILE_EDIT_UX_V1.md`
- `docs/BODY_AESTHETIC_PROPORTION_GRADE_TARGETING_V2.md`
- `docs/BODY_AESTHETIC_PROPORTION_GRADE_TARGETING_IMPLEMENTATION_PLAN_V2.md`

Runtime:
- `src/observer_sandbox/creator_profile_edit.py`
- `src/observer_sandbox/telegram_profile_edit.py`
- `src/observer_sandbox/telegram_profile_edit_ui.py`
- `src/observer_sandbox/body_aesthetic.py`
- `src/observer_sandbox/body_grade_target.py`
- `src/observer_sandbox/profile_observer.py`

Acceptance includes:
- `tests/test_creator_profile_editing_grade_targeting_v1.py`
- `tests/test_telegram_profile_edit_paused_ux_v1.py`
- `tests/test_body_aesthetic_grade_targeting_v2.py`

### Profile edit authority

Creator controls may correct represented profile facts and explicitly override represented engine-owned/progression values through one generic control contract.

Mutation classes:
- `canonical_correction` — replace represented canon without fabricating an in-world change experience;
- `creator_override` — replace represented current/progression state and re-anchor future progression from the corrected value.

Canonical flow:
`Creator preview -> validated raw-value proposal -> explicit Apply -> atomic mutation -> derived grade/progression/self-knowledge reconciliation -> future cognition`.

Raw values remain authoritative. Grades remain read-time derived. No persisted grade column or label becomes a second source of truth.

### Native paused Telegram Profile edit UX

Preferred Creator path:
`Characters -> Character -> Profile -> ✏️ Edit Profile`.

Entering Edit Profile:
- owner-only;
- records prior pause state;
- pauses a running universe;
- persistently shows `UNIVERSE PAUSED — CREATOR EDIT MODE`;
- Apply keeps the universe paused;
- Done Editing restores the pre-edit pause state;
- an already-paused universe remains paused afterward.

Individual fields are still editable through section -> field -> typed value -> preview -> Apply/Cancel.

General Grade Target still supports monotonic RAPS/Skills groups with E-S Preserve/Normalize.

## Body Aesthetic Proportion & Grade Targeting v2 — MERGED

### Forward grading contract

Body does **not** grade ordinary circumferences as `larger = better`.

Canonical forward flow:
`raw body measurements -> sex-aware ratio registry -> per-ratio target-range grade -> weighted Body aesthetic composite`.

Reference profiles:
- `body-aesthetic-male-v2`
- `body-aesthetic-female-v2`

Profile selection is based on represented canonical sex/body facts, not character identity.

### Male minimum

Grade-driving metrics and initial weights:
- Waist / Chest: 0.45 — empirical anchor near 0.70, project-calibrated S band 0.68..0.74;
- Waist / Shoulders: 0.35 — project-calibrated S band 0.55..0.65;
- Waist / Hips: 0.20 — empirical anchor near 0.80, project-calibrated S band 0.78..0.84.

For readability:
- `Waist / Chest` is authoritative for grading;
- `Chest / Waist` remains a derived inverse display context;
- the inverse display contributes zero scoring weight.

### Female minimum

Current minimum grade-driving metric:
- Waist / Hips — empirical anchor near 0.70 with project-calibrated S band 0.67..0.73.

Richer female metrics activate only when authoritative raw inputs exist. Do not fabricate bust/underbust/body-volume fields to satisfy grading.

Composite output remains coverage-aware so a one-metric evaluation is distinguishable from a richer multi-metric evaluation.

### Health context separation

Waist / Height remains health/central-adiposity context. It is displayed separately and is **not** silently averaged into Body aesthetic score.

### Body inverse targeting

Creator UX:
`Edit Profile -> Body -> 🎯 Body Grade Target`.

The general Grade Target menu also includes Body.

Supported targets: E/D/C/B/A/S.

Modes:
- `Preserve Shape` — default; deterministic nearest valid measurement vector, minimizing normalized raw changes and unnecessary proportional drift;
- `Normalize` — explicit stronger movement toward deterministic target ratios.

Height is a hard anchor in the initial solver. Shoulder/hip movement is more heavily penalized than ordinary soft-tissue circumference movement.

The solver is deterministic and bounded. It uses no LLM and never writes a grade. Every proposal must pass the ordinary forward Body evaluator and produce the requested composite grade before preview is created.

Preview exposes:
- sex-aware reference profile;
- old/new Body composite;
- metric coverage;
- projected ratio grades;
- separate Waist/Height health context;
- every raw measurement change;
- unchanged hard anchors.

Apply reuses the existing generic Creator mutation/reconciliation authority.

### Reconciliation

Body grade targeting remains a Creator control, not a character action or autobiographical event.

Apply:
- preserves audit/profile history;
- emits `creator_profile_corrected` provenance;
- re-anchors profile/stat-notification baselines;
- does not emit false earned-progression notifications;
- does not wipe Character Memory;
- retires only explicitly profile-derived stale semantic self-knowledge when present;
- preserves unrelated semantic/episodic Memory;
- never rewrites historical Cognition Context;
- creates no Mental Cycle/Episode/Artifact merely because a profile edit occurred.

Production Darian is not mutated merely for acceptance; disposable initialized databases prove mutation behavior.

## Perception Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Verified production:
- PR #269
- CI #1054 / run `32045634180`: SUCCESS
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- Deploy #289 / run `32045825836`: SUCCESS
- canonical service active;
- runtime log ready;
- SQLite quick-check green;
- schema v15;
- cognition recovery validated;
- Telegram healthy.

Perception closes:
`W0 actor exposure -> bounded actor-relative perception input`
without implying understanding, belief, Memory, Mind artifact, intention, plan or action authority.

## Completed minimum external-input stack

- W0 World Stimulus / Exposure — DEPLOYED
- W1 / W1.1 Weather — DEPLOYED
- W2 Commitments / Obligations — DEPLOYED
- W3 / W3.1 Economy / Valuation — DEPLOYED
- W4 / W4.1 Information / Media — DEPLOYED
- W5 Communication Exposure — DEPLOYED
- Perception Foundation v1 — DEPLOYED

## Intelligent Mind Engine route

Canonical: `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

After Body v2 production deploy/health verification, exact next development returns to:

### MIND-F2 — Mental Episode Runtime

Approved boundaries:
- keep Cognition Context as model-input observability;
- no extra LLM call merely to populate Cognition Context;
- generic context assembly provides structured sockets universally;
- one bounded cognition call is the normal path;
- the same call may emit a small represented Mental Episode bundle plus action proposal;
- use existing Mental Cycle/Episode substrate;
- episodes are bounded represented summaries, not hidden chain-of-thought transcripts;
- Mental Episodes do not automatically become Character Memory;
- prospective thought does not automatically become intention/plan;
- deterministic runtime remains executable action authority;
- no continuous/per-minute LLM thought polling;
- no character-specific prompt scripts;
- do not prebuild F3-F7 inside F2.

Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real production character seed`.

## Second-character seed gate

Required before another real production character:
1. W0-W5 minimum producers — satisfied;
2. Perception handoff — satisfied;
3. Creator profile editing + Body v2 production verification;
4. MIND-F2..F7 minimum foundations;
5. A3.3 interim planning scaffolding reconciliation;
6. Foundation Completion Review v2;
7. only then propose/authorize the next real character seed.

The next character is live multi-character architecture acceptance, not a test dummy.

## A3.3 — Bounded Multi-Step Destination Intent v1

A3.3 remains deployed. Continue read-only natural observation of inside-to-outside multi-hop initiation; do not force an outing. When F4/F5 activate, migrate/retire duplicate interim route-purpose scaffolding into canonical Mind intention/plan flow.

## Operational diagnostics

Creator-only Telegram diagnostics remain:
`/logs`, `/logs errors [lines]`, `/logs system [lines]`, `/logs runtime`, `/logs file [lines]`.

## World / spatial lock

Estate-first scope remains active. Broader public South Lake Tahoe traversal stays closed until explicitly authorized.

## Exact resume point

**PR #275 is merged at `cb68d51125610fc52cc146c0d69910257ebd7258` after final CI #1064 SUCCESS. Body v2 now provides sex-aware weighted forward grading, male Waist/Chest grading with Chest/Wasit display compatibility, deterministic E-S Preserve/Normalize inverse measurement targeting, and native paused Telegram Body Grade Target UX. No schema migration and no production Darian mutation were required for acceptance. Exact newer push-deploy evidence is not yet independently recorded; after runtime health verification, MIND-F2 is the next development slice.**