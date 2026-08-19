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

Do not turn an expected automatic deploy into claimed production truth without run/runtime evidence.

## Current canonical repository checkpoint

**Creator Character Profile Editing & Grade Targeting v1 is implemented, CI-green and merged. Exact production deploy verification is pending.**

Repository evidence:
- PR #271 — `Add Creator profile editing and grade targeting v1`
- final head `36de367cfe89b5602088273342e2665617bb928d`
- CI #1060 / run `32210592168`: **SUCCESS**
- merge `da64a8278d44c94c2db4b7fcac2e086d9e034269`
- no schema migration introduced; expected schema remains v15.

Initial CI #1055 produced `770 passed / 1 failed`. The only failure was `sqlite3.OperationalError: no such column: updated_at` on the new skill-edit path. `character_skills` intentionally has no `updated_at`; the implementation was narrowed to the existing store and now records Creator re-anchor simulation time in `metadata_json`. Final CI #1060 is green.

The deploy workflow is configured for `main` changes under `src/**`, so PR #271 contains deploy-triggering changes. However, the available GitHub connector exposes PR-triggered workflow runs but no push-triggered run listing. **Do not invent a Deploy #290 number/status.** Until independent deploy/runtime evidence is available, the last verified production checkpoint remains Perception Foundation v1 / Deploy #289.

## Creator Character Profile Editing & Grade Targeting v1 — MERGED / DEPLOY VERIFICATION PENDING

Canonical docs:
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`
- `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_ACCEPTANCE_V1.md`

Runtime:
- `src/observer_sandbox/creator_profile_edit.py`
- `src/observer_sandbox/telegram_profile_edit.py`
- `src/observer_sandbox/telegram_runtime_bot.py`

Tests:
- `tests/test_creator_profile_editing_grade_targeting_v1.py`
- `tests/test_telegram_creator_profile_edit_v1.py`

### Control semantics

Creator edits are explicit control authority, not ordinary character actions.

Modes:
- `canonical_correction` — replace a represented fact as canon without fabricating an in-world change experience;
- `creator_override` — explicitly replace a represented current/progression value and re-anchor later engine progression from the new value.

Creator guards preserve data type, canonical numeric domains and existing cross-field invariants. They must not become arbitrary realism restrictions that prevent legitimate Creator editing.

### Raw values and grading

Raw represented profile/skill values remain authoritative. Grades remain read-time derived through the existing grading framework.

Monotonic 0..100 grades:
- E 0..<20
- D 20..<40
- C 40..<60
- B 60..<75
- A 75..<90
- S 90..100

Changing a raw gradeable value automatically changes its read-time grade and compatible aggregate. No grade state is persisted.

### Section grade targeting

Supported v1 inverse families:
- RAPS/Attributes monotonic sections/groups;
- Skills monotonic 0..100 groups.

Example:
`Physical Attributes -> Grade B -> preserve_shape`.

The grade request is translated to proposed raw values, verified by the existing grading evaluator, previewed, and only then atomically applied.

Modes:
- `preserve_shape` default — preserve relative strengths/weaknesses as far as bounded constraints permit;
- `normalize` — explicitly move compatible fields toward one representative target value.

V1 representative target points are E=10, D=30, C=50, B=67.5, A=82.5, S=95.

Body uses ratio/reference/composite grading, so v1 supports individual body-input edit + automatic regrading but deliberately does not invent an arbitrary bulk inverse Body vector.

### Creator Telegram surface

Owner-only:
- `/profileedit <character_id> <field_key> <value>`
- `/profilegrade <character_id> <group> <grade> [preserve|normalize]`
- `/profileapply <preview_token>`

The command flow is preview-first. Unapplied previews do not change character state. Apply tokens belong to their requester and stale proposals are rejected if the underlying value changed after preview.

Do not mutate Darian's production profile just to prove deployment.

### Reconciliation

Apply performs targeted reconciliation:
- scalar profile history through existing `character_profile_history` where appropriate;
- Creator audit event `creator_profile_corrected`;
- skill re-anchor provenance in existing skill metadata;
- profile display/stat-notification baselines re-anchored so Creator edits are not later shown as earned progression;
- no broad Character Memory wipe;
- only active semantic self-knowledge explicitly tagged as deriving from corrected profile field(s) is retired;
- unrelated semantic and episodic memories stay intact;
- historical Cognition Context snapshots are never rewritten;
- no Mental Cycle/Episode/Artifact is created in this slice.

When F2-F7 later exist, profile correction reconciliation must remain targeted: past episode records remain historical represented activity; only invalidated active artifacts are reevaluated/retired by their owning Mind modules.

## Latest verified production checkpoint — Perception Foundation v1

Verified production evidence remains:
- PR #269
- CI #1054 / `32045634180`: SUCCESS
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`
- Deploy #289 / `32045825836`: SUCCESS
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

The Creator has approved the F2 design, but implementation waits only for the current merged profile-control slice's production deploy/health verification.

### MIND-F2 Mental Episode Runtime — next development slice after verification

Approved boundaries:
- Cognition Context stays; it is raw model-input observability, not represented Mind state;
- Cognition Context does not cause an extra LLM call;
- generic context assembly manages structured input sockets universally for every character;
- subsystems provide represented facts/state, not character-specific behavior instructions;
- one bounded cognition call is the normal path;
- the same call may return a small structured Mental Episode bundle plus the action proposal;
- use the existing Mental Cycle/Episode substrate;
- episodes are bounded represented summaries, not stored hidden chain-of-thought transcripts;
- Mental Episodes do not automatically become Character Memory;
- prospective thought does not automatically become intention/plan;
- action proposal remains subject to deterministic action authority;
- no continuous per-minute LLM thought polling;
- no F3-F7 behavior is prebuilt inside F2.

Continuation:
`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character seed`.

## Second-character seed gate

No second real production character until:
1. W0-W5 minimum external inputs complete — satisfied;
2. Perception handoff complete — satisfied;
3. Creator profile correction/reconciliation control production verification complete;
4. MIND-F2..F7 minimum foundations complete;
5. A3.3 interim planning scaffolding reconciled where appropriate;
6. Foundation Completion Review v2 authorizes the seed.

The next real character is live multi-character acceptance, not a development test dummy.

## A3.3 observation

A3.3 remains independently deployed. Continue read-only natural observation of the inside-to-outside multi-hop behavior; do not force an outing. Reconcile temporary route-purpose scaffolding into F4/F5 when canonical intention/planning activates.

## Exact resume point

**PR #271 is merged at `da64a8278d44c94c2db4b7fcac2e086d9e034269` after final CI #1060 SUCCESS. Creator Character Profile Editing & Grade Targeting v1 now exists in canonical repository source with preview-first owner controls, derived grading, section-grade inverse targeting, targeted Memory/progression reconciliation and no schema migration. Exact push-deploy evidence is not accessible through the current connector, so production deployment is not yet claimed. Verify deployment/runtime health read-only when evidence becomes available; then begin MIND-F2. Do not change Darian merely for acceptance and do not seed a second production character before the foundation gate.**
