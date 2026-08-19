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
`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> sync test to final main checkpoint`.

Do not claim production deployment without deploy/runtime evidence.

## Current canonical repository checkpoint

**Creator Character Profile Editing & Grade Targeting v1 plus its native paused Telegram Profile UX are implemented, CI-green and merged. Exact production deploy verification remains pending independent evidence.**

Latest repository evidence:
- PR #273 — `Add paused Telegram profile edit UX`
- final head `232c4db3098940e09696cb6af90296db8f466091`
- CI #1061 / run `32214382666`: **SUCCESS**
- merge `a324a9a8b0ff0dc9538b850ccd7ab0d59ed1eef0`
- no schema migration; schema contract remains v15.

Underlying profile-control evidence:
- PR #271 — `Add Creator profile editing and grade targeting v1`
- final CI #1060 / run `32210592168`: **SUCCESS**
- merge `da64a8278d44c94c2db4b7fcac2e086d9e034269`
- first CI #1055 was `770 passed / 1 failed`; the only failure was an incorrect assumption that `character_skills` had `updated_at`. The final implementation preserves the existing table and records Creator skill re-anchor time in metadata.

The deploy workflow triggers on `main` source changes. PR #273 contains runtime/Telegram changes and therefore is deploy-triggering, but the available connector does not list push-triggered workflow runs. Public search did not expose an independently usable run either. **Do not invent a deployment number/status.** The latest independently verified production checkpoint remains Perception Foundation v1 / Deploy #289 until newer deploy/runtime evidence is available.

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

Tests:
- `tests/test_creator_profile_editing_grade_targeting_v1.py`
- `tests/test_telegram_creator_profile_edit_v1.py`
- `tests/test_telegram_profile_edit_paused_ux_v1.py`

### Authority / grading

Creator edits are explicit control authority, not character actions.

Mutation classes:
- `canonical_correction` — replace a represented fact without fabricating an in-world experience;
- `creator_override` — explicitly replace a represented current/progression value and re-anchor future progression from the new value.

Raw profile/runtime/skill values remain authoritative. Grades remain read-time derived; no grade state is persisted.

Monotonic RAPS/Skill grade intervals:
- E 0..<20
- D 20..<40
- C 40..<60
- B 60..<75
- A 75..<90
- S 90..100

Section inverse targeting supports compatible monotonic RAPS/Attributes and Skills groups. `preserve_shape` is the default; `normalize` is explicit. V1 representative points are E=10, D=30, C=50, B=67.5, A=82.5, S=95.

Body uses ratio/reference/composite grading. Individual writable Body inputs may be corrected and auto-regraded, but v1 does not fabricate a bulk inverse Body vector.

### Preferred Telegram Creator UX

Primary path:
`Characters -> Character -> Profile -> ✏️ Edit Profile`.

The `/profileedit`, `/profilegrade`, `/profileapply` commands remain advanced fallback/manual controls; they are no longer the preferred UX.

Owner-only Profile editing behavior:
1. owner Profile menu shows `✏️ Edit Profile`;
2. authorized non-owner observers remain read-only and do not receive the button;
3. entering Edit Profile records the pre-edit pause state and pauses a running universe through canonical autonomy pause control;
4. every edit-mode screen prominently shows `UNIVERSE PAUSED — CREATOR EDIT MODE`;
5. Creator chooses a profile section and a represented writable field;
6. bot asks for the new value as the Creator's next private Telegram message;
7. value is validated through `preview_profile_edit(...)` and shown as before/after preview;
8. Creator presses `Apply Change` or `Cancel Preview`;
9. Apply keeps the universe paused so multiple corrections can be made safely;
10. `Done Editing` closes the session and restores the pause state that existed before entry.

If the universe was already paused before editing, Done Editing leaves it paused. Applying one correction never auto-resumes the universe.

Native Grade Target UX exposes Physical, Mental, Intellectual, Verbal Charisma, All Attributes and All Skills groups with E-S plus Preserve/Normalize buttons. Physical -> Grade B Preserve is acceptance-covered.

Derived-only fields and collections not owned by this editor contract remain read-only.

### Reconciliation

Apply remains preview-first and atomic. Stale proposals reject if affected raw state changed after preview.

Targeted reconciliation:
- profile history where applicable;
- Creator audit event `creator_profile_corrected`;
- skill re-anchor provenance in existing metadata;
- display/stat-notification baselines re-anchored so correction is not reported as earned progression;
- no broad Character Memory wipe;
- only semantic self-knowledge explicitly tagged as derived from corrected profile fields may be retired;
- unrelated semantic/episodic memories stay intact;
- historical Cognition Context is never rewritten;
- no Mental Cycle/Episode/Artifact is created by profile editing.

Do not mutate Darian's production profile merely for deployment acceptance.

## Latest independently verified production checkpoint — Perception Foundation v1

Verified production evidence:
- PR #269
- CI #1054 / run `32045634180`: SUCCESS
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- Deploy #289 / run `32045825836`: SUCCESS
- canonical service active;
- runtime log ready;
- SQLite readable and `PRAGMA quick_check=ok`;
- schema v15;
- cognition recovery non-mutating/validated;
- Telegram healthy.

Perception v1 closes:
`W0 character exposure -> bounded actor-relative perception input`.

It does not imply understanding, belief, Memory, thought, intention, plan or action authority.

## Completed minimum external-input foundation

- W0 World Stimulus / Exposure
- W1 / W1.1 Weather
- W2 Commitments / Obligations
- W3 / W3.1 Economy / Valuation
- W4 / W4.1 Information / Media
- W5 Communication Exposure
- Perception Foundation v1

The W0-W5 minimum producer sequence and exposure-to-perception bridge are complete.

## Mind Engine continuation

Canonical: `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

MIND-F2 design is approved. Repository development should resume there after the current merged profile-control/Telegram UX deployment is independently verified or when the Creator explicitly directs continuation despite the observability limitation.

MIND-F2 boundaries:
- Cognition Context stays as raw model-input observability and causes no extra LLM call;
- generic context assembly owns structured sockets universally;
- one bounded cognition call is the normal path;
- that call may return a small represented Mental Episode bundle plus action proposal;
- use existing Mental Cycle/Episode substrate;
- episodes are bounded represented summaries, not hidden chain-of-thought transcripts;
- Mental Episodes do not automatically become Character Memory;
- prospective thought does not automatically become intention/plan;
- deterministic runtime remains action authority;
- no continuous/per-minute LLM thought polling;
- no F3-F7 behavior prebuilt inside F2.

Continuation:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character seed`.

## Second-character seed gate

Do not seed another real production character before:
1. W0-W5 minimum external inputs — satisfied;
2. Perception handoff — satisfied;
3. Creator profile correction + Telegram control production verification;
4. MIND-F2..F7 minimum foundations;
5. A3.3 interim planning scaffolding reconciliation;
6. Foundation Completion Review v2.

The next real character is live multi-character acceptance, not a development test dummy.

## A3.3 observation

A3.3 remains independently deployed. Continue read-only natural observation of inside-to-outside multi-hop behavior; do not force an outing. Reconcile temporary route-purpose scaffolding into F4/F5 when canonical intention/planning activates.

## Exact resume point

**PR #273 is merged at `a324a9a8b0ff0dc9538b850ccd7ab0d59ed1eef0` after CI #1061 SUCCESS. The Creator can now reach profile editing from Character -> Profile -> Edit Profile in canonical repository source; entering edit mode pauses the universe, all edits are preview-first, Apply keeps the session paused, and Done Editing restores the pre-edit pause state. Exact newer push-deploy evidence is still unavailable, so production deployment is not claimed. Latest independently verified production remains Deploy #289. After verification, resume MIND-F2. Do not mutate Darian merely for acceptance and do not seed a second production character before the foundation gate.**