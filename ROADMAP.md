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

**Creator Character Profile Editing & Grade Targeting v1 and its native paused Telegram Profile UX are IMPLEMENTED / CI-GREEN / MERGED. Exact production deploy verification is pending independent evidence.**

Latest repository evidence:
- PR #273 — `Add paused Telegram profile edit UX`
- final head `232c4db3098940e09696cb6af90296db8f466091`
- CI #1061 / run `32214382666`: **SUCCESS**
- merge `a324a9a8b0ff0dc9538b850ccd7ab0d59ed1eef0`
- no schema migration; schema contract remains v15.

Underlying editor foundation:
- PR #271
- CI #1060 / run `32210592168`: SUCCESS
- merge `da64a8278d44c94c2db4b7fcac2e086d9e034269`
- first CI #1055 was `770 passed / 1 failed`; the sole issue was a false `character_skills.updated_at` assumption and was fixed without schema expansion.

PR #273 contains deploy-triggering source changes. The current connector cannot list push-triggered workflow runs, and public search did not provide independently usable deploy evidence. Do not fabricate a deployment number or success state. Latest independently verified production remains Perception Foundation v1 / Deploy #289.

## Creator Character Profile Editing & Grade Targeting v1

Canonical docs:
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_ACCEPTANCE_V1.md`
- `docs/TELEGRAM_CREATOR_PROFILE_EDIT_UX_V1.md`

Runtime:
- `src/observer_sandbox/creator_profile_edit.py`
- `src/observer_sandbox/telegram_profile_edit.py`
- `src/observer_sandbox/telegram_profile_edit_ui.py`
- `src/observer_sandbox/telegram_runtime_bot.py`

Acceptance:
- `tests/test_creator_profile_editing_grade_targeting_v1.py`
- `tests/test_telegram_creator_profile_edit_v1.py`
- `tests/test_telegram_profile_edit_paused_ux_v1.py`

### Authority and edit semantics

Creator controls may correct represented profile facts and explicitly override represented engine-owned/progression values through one generic control contract.

Mutation classes:
- `canonical_correction` — replace represented canon without fabricating an in-world change experience;
- `creator_override` — replace represented current/progression state and re-anchor future progression from the corrected value.

Canonical flow:
`Creator preview -> validated raw-value proposal -> explicit Apply -> atomic mutation -> derived grade/progression/self-knowledge reconciliation -> future cognition`.

Guards preserve data/schema/cross-field validity; they are not arbitrary realism restrictions on Creator authority.

### Raw values / grades

Grades remain read-time derived. No grade label or grade column becomes authoritative state.

Monotonic RAPS/Skill intervals:
- E: 0..<20
- D: 20..<40
- C: 40..<60
- B: 60..<75
- A: 75..<90
- S: 90..100

Section inverse targeting supports compatible monotonic RAPS/Attributes and Skills families. `preserve_shape` is default; `normalize` is explicit. Representative v1 targets: E=10, D=30, C=50, B=67.5, A=82.5, S=95.

Body grading remains ratio/reference/composite. Individual authoritative Body inputs may be edited and auto-regraded, but no arbitrary bulk inverse Body vector is created in v1.

## Native Telegram Profile Edit UX — MERGED

Preferred Creator path:
`Characters -> Character -> Profile -> ✏️ Edit Profile`.

Owner-only behavior:
- owner Profile menu receives `Edit Profile`;
- allowed non-owner Profile remains read-only;
- entering edit mode records the pre-edit pause state and pauses a running universe through canonical autonomy pause control;
- every edit screen shows `UNIVERSE PAUSED — CREATOR EDIT MODE`;
- section -> represented writable field -> next typed Telegram message -> validated preview -> Apply/Cancel;
- raw state remains unchanged before Apply;
- Apply keeps the universe paused so Creator may continue editing;
- Done Editing restores the pause state that existed before entry;
- a universe already paused before editing remains paused afterward.

The visible pause warning is persistent in the edit message, not a short-lived toast. It explicitly tells the Creator that simulation is frozen and Done Editing restores the prior state.

Native Grade Target buttons support Physical, Mental, Intellectual, Verbal Charisma, All Attributes and All Skills with E-S plus Preserve/Normalize choices. `Physical Attributes -> Grade B -> Preserve` is acceptance-covered and resolves against the existing grading engine.

The advanced `/profileedit`, `/profilegrade`, `/profileapply` commands remain available but are fallback/manual controls rather than the primary UX.

Derived-only fields and collections not owned by the current editor remain read-only.

### Reconciliation semantics

Applied Creator edits:
- reuse profile history where applicable;
- emit `creator_profile_corrected` audit provenance;
- preserve existing skill storage and write re-anchor provenance to skill metadata;
- re-anchor profile display/stat-notification baselines so corrections are not announced as organically earned progression;
- do not wipe Character Memory;
- retire only semantic self-knowledge explicitly tagged as derived from corrected profile field keys;
- preserve unrelated semantic/episodic memory;
- never rewrite historical Cognition Context snapshots;
- create no Mental Cycle, Mental Episode or Mental Artifact.

Production Darian must not be changed merely to prove deployment. Acceptance uses disposable initialized databases.

## Perception Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Verified production:
- PR #269
- CI #1054 / run `32045634180`: SUCCESS
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- Deploy #289 / run `32045825836`: SUCCESS
- canonical service active, runtime log ready, SQLite quick-check green, schema v15, cognition recovery validated, Telegram healthy.

Perception v1 closes:
`W0 actor exposure -> bounded actor-relative perception input`.

It preserves provenance and creates no understanding, belief, Memory, Mind artifact, intention, plan or action authority.

## Completed minimum external-input stack

- W0 World Stimulus / Exposure — DEPLOYED
- W1 / W1.1 Weather — DEPLOYED
- W2 Commitments / Obligations — DEPLOYED
- W3 / W3.1 Economy / Valuation — DEPLOYED
- W4 / W4.1 Information / Media — DEPLOYED
- W5 Communication Exposure — DEPLOYED
- Perception Foundation v1 — DEPLOYED

The W0-W5 producer sequence and minimum exposure-to-perception handoff are complete.

## Intelligent Mind Engine route

Canonical: `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

MIND-F2 design is approved. Resume it after independent verification of the merged profile-control/Telegram UX deployment, or earlier only if the Creator explicitly directs continuation despite the deploy-observability limitation.

### MIND-F2 — Mental Episode Runtime

Approved boundaries:
- keep Cognition Context as model-input observability;
- no extra LLM call merely to populate Cognition Context;
- generic context assembly provides structured sockets universally;
- one bounded cognition call is the normal path;
- the same call may emit a small represented Mental Episode bundle plus action proposal;
- use the existing Mental Cycle/Episode substrate;
- episodes are bounded represented summaries, not hidden chain-of-thought transcripts;
- Mental Episodes do not automatically become Character Memory;
- prospective thought does not automatically become intention/plan;
- deterministic runtime remains executable action authority;
- no continuous/per-minute LLM thought polling;
- no character-specific prompt scripts;
- do not prebuild F3-F7 behavior inside F2.

Then:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real production character seed`.

## Second-character seed gate

Required before another real production character:
1. W0-W5 minimum producers — satisfied;
2. Perception handoff — satisfied;
3. Creator profile correction + native Telegram edit control production verification;
4. MIND-F2..F7 minimum foundations;
5. A3.3 interim planning scaffolding reconciliation;
6. Foundation Completion Review v2;
7. only then propose/authorize the next real character seed.

The next character is live multi-character acceptance, not a test dummy.

## A3.3 — Bounded Multi-Step Destination Intent v1

A3.3 remains deployed. Continue read-only natural observation of the missing inside-to-outside multi-hop initiation; do not force an outing. When F4/F5 activate, migrate/retire duplicate interim planning scaffolding into canonical Mind intention/plan flow.

## Operational diagnostics

Creator-only Telegram diagnostics remain:
`/logs`, `/logs errors [lines]`, `/logs system [lines]`, `/logs runtime`, `/logs file [lines]`.

## World / spatial lock

Estate-first scope remains active. Broader public South Lake Tahoe traversal stays closed until explicitly authorized.

## Exact resume point

**PR #273 is merged at `a324a9a8b0ff0dc9538b850ccd7ab0d59ed1eef0` after CI #1061 SUCCESS. Native Character -> Profile -> Edit Profile editing now exists in canonical source with automatic universe pause, persistent warning, direct field selection + typed input, preview/apply, native grade targeting, and prior-pause restoration on Done Editing. Exact newer push-deploy evidence remains unavailable, so production deployment is intentionally not claimed; Deploy #289 remains the latest independently verified production checkpoint. After verification, MIND-F2 is next. Do not mutate Darian merely for acceptance and do not seed a second real character before the foundation gate.**