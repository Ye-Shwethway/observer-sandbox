# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-19

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches are only `main` and `test`.

Default workflow:
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> continuity sync -> test/main synchronization`.

Do not claim production deployment without deploy/runtime evidence.

## Current canonical repository checkpoint

**Body Aesthetic Proportion & Grade Targeting v2 is docs-complete, implemented, CI-green and merged. Exact newer push-deploy verification remains pending independent evidence.**

Latest repository evidence:
- PR #275 — `Add Body aesthetic grade targeting v2`
- final head `9cd286b95f81f1f5849e5c089be0abdeeb472ccd`
- CI #1064 / run `32221713304`: **SUCCESS**
- specialized Read-Only Grading Proof Acceptance #56: **SUCCESS**
- specialized Attribute Grading Batch 1 Acceptance #55: **SUCCESS**
- merge `cb68d51125610fc52cc146c0d69910257ebd7258`
- no schema migration introduced; schema contract remains v15.

Initial CI #1062 reached **782 passed / 1 failed**. The single failure was the existing Telegram/profile expectation `Chest / Waist: 1.364`. V2 intentionally changed grading authority to `Waist / Chest`, but the approved contract also preserves the inverse Chest/Wasit display for readability. The fix therefore restored `Chest / Waist` as derived display context while keeping `Waist / Chest` as the grade-driving metric. Final CI #1064 is green.

Do not invent a deployment number/status if the push-triggered run is not independently visible. Latest independently verified production remains Perception Foundation v1 / Deploy #289 until newer runtime evidence is obtained.

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

Tests include:
- `tests/test_creator_profile_editing_grade_targeting_v1.py`
- `tests/test_telegram_profile_edit_paused_ux_v1.py`
- `tests/test_body_aesthetic_grade_targeting_v2.py`

### Creator profile edit UX

Preferred path:
`Characters -> Character -> Profile -> ✏️ Edit Profile`.

Entering edit mode:
- owner-only;
- records prior pause state;
- pauses a running universe;
- shows persistent `UNIVERSE PAUSED — CREATOR EDIT MODE` warning;
- Apply keeps the edit session paused;
- `Done Editing` restores the prior pause state;
- an already-paused universe remains paused after exit.

Profile mutation remains preview-first and atomic. Raw represented values remain authoritative. Grades remain read-time derived and are never persisted as a second truth.

### Body Aesthetic Proportion & Grade Targeting v2

Canonical body rule:
`raw measurements -> sex-aware derived ratios -> reference profile -> per-ratio grades -> weighted Body composite`.

Inverse targeting:
`requested Body grade -> deterministic preserve/normalize solver -> proposed raw measurements -> ordinary forward grading verification -> preview -> Apply`.

No LLM is used for body grading or measurement solving.

Sex-aware profiles:
- `body-aesthetic-male-v2`
- `body-aesthetic-female-v2`

The profile selector uses represented sex/body facts, never character identity.

Male minimum grade-driving ratios:
- Waist / Chest — weight 0.45; empirical anchor near 0.70 plus project-calibrated S band 0.68..0.74;
- Waist / Shoulders — weight 0.35; project-calibrated S band 0.55..0.65;
- Waist / Hips — weight 0.20; empirical anchor near 0.80 plus project-calibrated S band 0.78..0.84.

Female minimum currently grades represented Waist / Hips with empirical anchor near 0.70 plus project-calibrated S band 0.67..0.73. Richer female metrics activate only when their authoritative raw inputs exist; missing bust/underbust/body-volume values are never fabricated.

Waist / Height remains separate health/central-adiposity context and is **not** silently averaged into the aesthetic composite.

For male UI readability:
- `Waist / Chest` is the grade-driving metric;
- `Chest / Waist` remains visible as the familiar inverse derived context;
- the inverse display does not affect the composite.

Body Grade Target is available both from the general Grade Target menu and directly inside Body edit:
`Edit Profile -> Body -> 🎯 Body Grade Target`.

Grades E/D/C/B/A/S support:
- `Preserve Shape` — default; deterministic nearest valid measurement vector while height remains a hard anchor and unnecessary proportional drift is penalized;
- `Normalize` — explicit stronger movement toward deterministic target ratios.

The Body solver uses bounded deterministic search and the ordinary forward evaluator as final authority. If the requested grade is not achieved, the proposal fails before mutation.

Body preview shows:
- selected sex-aware reference profile;
- current/projected Body composite;
- metric coverage;
- projected ratio grades;
- Waist/Height health context separately;
- every raw measurement change;
- hard anchors left unchanged.

Acceptance uses disposable initialized databases; production Darian must not be distorted merely to prove the control.

### Reconciliation semantics

Applied Creator edits:
- reuse profile history/audit provenance;
- emit `creator_profile_corrected`;
- re-anchor progression/display/stat-notification baselines so direct control is not reported as organically earned progression;
- do not wipe Character Memory;
- retire only explicitly profile-derived stale semantic self-knowledge when present;
- preserve unrelated semantic/episodic Memory;
- never rewrite historical Cognition Context;
- create no Mental Cycle/Episode/Artifact merely because profile editing occurred.

Future Mind reconciliation remains targeted: historical episodes remain historical; only active artifacts invalidated by corrected premises are reevaluated by their owning Mind modules.

## Latest independently verified production checkpoint — Perception Foundation v1

Verified:
- PR #269
- CI #1054 / `32045634180`: SUCCESS
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- Deploy #289 / `32045825836`: SUCCESS
- service/runtime log/SQLite/Telegram/cognition recovery healthy;
- schema v15.

Perception closes:
`W0 exposure -> bounded actor-relative perception input`
without implying understanding, belief, Memory, thought, intention, plan or action authority.

## Completed minimum external-input stack

- W0 World Stimulus / Exposure
- W1 / W1.1 Weather
- W2 Commitments / Obligations
- W3 / W3.1 Economy / Valuation
- W4 / W4.1 Information / Media
- W5 Communication Exposure
- Perception Foundation v1

## Mind Engine continuation

Canonical: `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

After Body v2 deployment/health verification, exact next implementation returns to:
**MIND-F2 — Mental Episode Runtime**.

Approved boundaries:
- Cognition Context remains raw model-input observability and is not another LLM call;
- generic structured context assembly is universal across characters;
- one bounded cognition call is the normal path;
- the same call may return a small Mental Episode bundle plus action proposal;
- episodes are bounded represented summaries, not hidden chain-of-thought transcripts;
- Mental Episodes do not automatically become Character Memory;
- prospective thought does not automatically become intention/plan;
- deterministic runtime remains action authority;
- no continuous/per-minute thought polling;
- no character-specific prompt scripts;
- do not prebuild F3-F7 inside F2.

Continuation:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character seed`.

## Second-character seed gate

Do not seed another real production character before:
1. W0-W5 minimum external inputs — satisfied;
2. Perception handoff — satisfied;
3. Creator profile editing + Body v2 production verification;
4. MIND-F2..F7 minimum foundations;
5. A3.3 interim planning scaffolding reconciliation;
6. Foundation Completion Review v2.

## A3.3 observation

A3.3 remains independently deployed. Continue read-only natural observation of inside-to-outside multi-hop behavior; never force Darian outside. Migrate/retire duplicate route-purpose scaffolding when F4/F5 activate.

## Exact resume point

**PR #275 is merged at `cb68d51125610fc52cc146c0d69910257ebd7258` after final CI #1064 SUCCESS. Body grading is now sex-aware, weighted and coverage-aware in canonical source; male Waist/Chest is grade-driving while Chest/Wasit remains display context; deterministic Body E-S Preserve/Normalize targeting is wired into the paused Creator Profile UX and verified on disposable state. No schema migration and no production Darian mutation were used. Exact newer push-deploy evidence is not yet independently recorded; once runtime health is verified, resume MIND-F2.**