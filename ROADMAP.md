# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-19

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve the separation of world truth, exposure, perception, memory, Mind and action authority.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Character-specific behavioral hard-coding is forbidden.
- Persistent branches are only `main` and `test`; normal development occurs on `test` and is promoted to `main` after validation.
- Prefer vertical completeness and operational usefulness over subsystem sprawl.
- At material checkpoints, reconcile roadmap/bootstrap state with implementation and verified runtime truth. Do not claim production deployment without deploy/runtime evidence.
- Do not seed another real production character merely to test unfinished foundations; use generic fixtures until the foundation-completion gate is reached.

## Current canonical repository checkpoint

**Creator Character Profile Editing & Grade Targeting v1 is IMPLEMENTED / CI-GREEN / MERGED. Production deploy verification is still pending exact evidence.**

Verified repository evidence:
- PR #271 — `Add Creator profile editing and grade targeting v1`
- final head `36de367cfe89b5602088273342e2665617bb928d`
- **CI #1060 / run `32210592168`: SUCCESS**
- initial CI #1055: `770 passed / 1 failed`; the sole failure was a stale implementation assumption that `character_skills` had an `updated_at` column. The fix preserved the existing schema and moved Creator re-anchor time into skill metadata.
- merge `da64a8278d44c94c2db4b7fcac2e086d9e034269`
- no schema migration introduced; repository contract remains compatible with production schema **v15**.

The automatic deploy workflow is configured to run on `main` changes under `src/**`, but the currently available GitHub connector can list only PR-triggered runs for a commit and exposes no push-run listing action. Therefore the deploy number/run/status is **not recorded here until independently verified**. Do not infer or fabricate a Deploy #290 result.

Latest independently verified production checkpoint remains **Perception Foundation v1 / Deploy #289 / run `32045825836`: SUCCESS**.

## Creator Character Profile Editing & Grade Targeting v1 — MERGED / DEPLOY VERIFICATION PENDING

Canonical docs:
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_ACCEPTANCE_V1.md`

Runtime:
- `src/observer_sandbox/creator_profile_edit.py`
- `src/observer_sandbox/telegram_profile_edit.py`
- `src/observer_sandbox/telegram_runtime_bot.py`

Acceptance:
- `tests/test_creator_profile_editing_grade_targeting_v1.py`
- `tests/test_telegram_creator_profile_edit_v1.py`

### Authority and edit semantics

Creator control may edit represented profile/seed facts and explicitly override represented engine-owned/progression values through the generic control contract.

Mutation classes:
- `canonical_correction` — replace a represented canonical fact without inventing an in-world change event;
- `creator_override` — explicitly replace a currently represented value and re-anchor its owning progression/runtime context.

Guards preserve data/schema/cross-field validity; they are not arbitrary realism restrictions on Creator authority.

Canonical flow:
`Creator preview -> validated authoritative raw-value proposal -> explicit apply -> atomic mutation -> derived grade/progression/self-knowledge reconciliation -> future cognition`.

### Raw values remain grading authority

Grades remain read-time derived. No grade column or grade label becomes authoritative state.

Existing monotonic 0..100 grading intervals remain:
- E: 0..<20
- D: 20..<40
- C: 40..<60
- B: 60..<75
- A: 75..<90
- S: 90..100

Editing an authoritative RAPS or Skill value therefore automatically changes its individual and compatible aggregate grade on the next ordinary profile read.

### Section-level inverse grade targeting

V1 supports deterministic inverse targeting for monotonic 0..100 RAPS/Attributes and Skills families.

Example:
`Physical Attributes -> Grade B -> preserve_shape`

The system converts the requested grade into the existing scheme's numeric interval, proposes raw values, verifies the existing grading evaluator returns the requested aggregate, previews every change, and mutates only after explicit Creator apply.

Modes:
- `preserve_shape` — default; preserve relative strengths/weaknesses as far as bounded 0..100 constraints permit;
- `normalize` — intentionally move compatible fields to a common representative target value.

Representative midpoint targets in v1 are E=10, D=30, C=50, B=67.5, A=82.5, S=95.

Body grading remains read-time ratio/reference/composite grading. Individual authoritative body inputs may be edited and will auto-regrade, but Body composite grades are **not bulk-inverted in v1** because there is no single canonical inverse measurement vector.

### Preview-first Creator Telegram surface

Owner-only commands:
- `/profileedit <character_id> <field_key> <value>`
- `/profilegrade <character_id> <group> <grade> [preserve|normalize]`
- `/profileapply <preview_token>`

Unapplied previews do not mutate character state. Apply tokens are requester-bound and stale proposals fail closed if any affected raw value changed since preview.

Production Darian must not be modified merely to prove deployment. Automated acceptance uses disposable initialized databases.

### Reconciliation semantics

Applied Creator edits:
- reuse `character_profile_history` for scalar profile audit where applicable;
- emit Creator control provenance through `creator_profile_corrected`;
- preserve existing skill storage and store Creator re-anchor provenance in skill metadata;
- re-anchor profile display/stat-notification baselines so the edit is not later announced as organically earned progression;
- do **not** wipe Character Memory;
- retire only active semantic self-knowledge explicitly tagged as derived from affected profile field keys;
- preserve unrelated semantic/episodic memory;
- do not rewrite historical Cognition Context snapshots;
- create no Mental Cycle, Mental Episode or Mental Artifact in this slice.

Future Mind reconciliation remains targeted: historical episodes remain historical represented activity; only active artifacts whose premises are invalidated by a later correction should be reevaluated/retired by their owning F3-F7 modules.

## Perception Foundation v1 — DEPLOYED / MINIMUM COMPLETE

Verified:
- PR #269
- CI #1054 / `32045634180`: SUCCESS
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- Deploy #289 / `32045825836`: SUCCESS
- production service/runtime log/SQLite/Telegram/cognition-recovery health green; schema v15 unchanged.

Perception v1 is a deterministic bounded read projection:
`W0 actor exposure -> actor-relative perception input`.

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

Canonical contract: `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

Once the merged Creator Profile Editing slice has verified production deployment/health, resume the previously approved Mind sequence.

### MIND-F2 — Mental Episode Runtime — NEXT DEVELOPMENT SLICE AFTER DEPLOY VERIFICATION

Approved design:
- Cognition Context remains an observability snapshot and is **not** deleted;
- Cognition Context is not a second LLM call;
- one bounded cognition call is the default;
- generic context assembly supplies purpose-specific sockets such as present state, physiology, perception, recallable Memory and later active Mind artifacts;
- the same cognition call may emit a small structured Mental Episode bundle plus an action proposal;
- episodes are represented actor-owned mental state, not raw hidden chain-of-thought transcripts;
- Mental Episodes remain separate from durable Character Memory;
- prospective thought is not automatically an intention or plan;
- action proposal remains separate from deterministic action authority;
- no continuous/per-minute thought polling;
- no character-specific prompt scripts or algorithms.

Then continue:
`MIND-F2 -> MIND-F3 Attention/Appraisal/Active Concerns -> MIND-F4 Intention -> MIND-F5 Planning -> MIND-F6 Social Cognition/Communication -> MIND-F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real production character seed`.

## Second-character seed gate

Required before another real production character:
1. W0-W5 minimum producer foundations — satisfied;
2. Perception handoff — satisfied;
3. Creator profile correction/reconciliation control — repository implementation merged; production deploy verification pending;
4. MIND-F2..F7 minimum foundations;
5. A3.3 interim planning scaffolding reconciled into canonical Mind planning where appropriate;
6. Foundation Completion Review v2;
7. only then propose/authorize the next real character seed.

The next character is live multi-character architecture acceptance, not a test dummy.

## A3.3 — Bounded Multi-Step Destination Intent v1 — DEPLOYED / OBSERVATION CONTINUES

A3.3 remains deployed and provides actor-known bounded route-purpose hints while one-hop `action_options` remain deterministic movement authority.

Natural proof of the previously missing inside-to-outside initiation remains read-only observation. Do not force an outing. When F4/F5 activate, reconcile/retire duplicate interim planning scaffolding into canonical Mind intention/plan flow.

## Operational diagnostics — DEPLOYED

Creator-only Telegram diagnostics remain:
`/logs`, `/logs errors [lines]`, `/logs system [lines]`, `/logs runtime`, `/logs file [lines]`.

## World / spatial lock

Estate-first scope remains active. Broader public South Lake Tahoe traversal stays closed until explicitly authorized.

## Exact resume point

**Creator Character Profile Editing & Grade Targeting v1 is merged at `da64a8278d44c94c2db4b7fcac2e086d9e034269` after final CI #1060 SUCCESS. Its deploy-triggering source changes are on main, but exact push-triggered deploy/run evidence is not visible through the current GitHub connector, so production deployment is intentionally not claimed yet. The next operational step is read-only deploy/production verification; once verified, MIND-F2 Mental Episode Runtime is the next development slice. Do not mutate Darian merely for profile-editor acceptance, and do not seed a second real character before the F2-F7 + Foundation Completion Review v2 gate.**
