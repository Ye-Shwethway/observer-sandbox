# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-16

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Default workflow:
`branch -> focused tests + final PR CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Do not repeatedly run the full suite. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes skip the Python suite. Use **exemplar-first, then batch-by-pattern** and prefer vertical completeness before local depth.

## Strategic checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1.

Adaptive Character Disposition Foundation is COMPLETE v1:
`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`.

The **Overall Workflow/Foundation Review v1 is COMPLETE / CLOSED**. The bounded final closure pass found no additional blocking cross-system foundation gap. Do not continue open-ended gap hunting by default.

Four evidence-selected structural gaps were closed during that review:
1. **Autonomy Intent Continuity v1** — PR #178 / Deploy #236.
2. **Active Modifier Runtime Foundation v1** — PR #180 / Deploy #237.
3. **Action Condition Runtime Foundation v1** — PR #182 / Deploy #238.
4. **Participant-Aware Recent Event Context v1** — PR #184 / Deploy #239.

Relevant docs:
- `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`
- `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`
- `docs/ACTIVE_MODIFIER_RUNTIME_V1.md`
- `docs/ACTION_CONDITION_RUNTIME_V1.md`
- `docs/PARTICIPANT_RECENT_EVENT_CONTEXT_V1.md`
- `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`
- `docs/TELEGRAM_COGNITION_CONTEXT_INSPECTOR_V1.md`
- `docs/COGNITION_CONTEXT_EFFICIENCY_V1.md`

## Foundation closure state

Minimum foundations classified present:
- generic action/task lifecycle;
- resources/inventory/state consequences;
- environment/world topology/context;
- object knowledge/familiarity;
- generic inter-character participation socket;
- event/lifecycle evidence;
- participant-aware bounded recent-event cognition;
- long-horizon progression/decay exemplars;
- profile -> cognition/runtime integration;
- autonomy purpose continuity;
- persistent temporary modifier lifecycle;
- action-definition prerequisite runtime.

Absence of exhaustive depth is not a foundation defect. Rich relationships, generalized group coordination, broad episodic memory, witness inference, weather, economy, vehicles and similar domains are explicit feature/depth candidates only.

## Current phase — Creator Feature Planning

The project is implementing explicitly requested product features as minimum-runnable slices.

For each proposed feature:
- define the user-visible capability;
- identify current-contract dependencies;
- separate minimum-runnable scope from later depth;
- compare value, implementation cost and runtime risk;
- use one exemplar only for a genuinely new invariant, then batch equivalent follow-ons.

Reopen the Overall Workflow/Foundation Review only when concrete feature work exposes a cross-system invariant the current runtime cannot represent or execute safely.

### Telegram Cognition Context Inspector v1

Status: **COMPLETE / DEPLOYED**.

The owner-only selected-character Telegram page exposes the actual compact runtime context captured immediately before production cognition injection, retains the latest three actor-scoped injections, distinguishes primary versus corrective retry, generically renders future context keys, and pages long snapshots without Telegram message splitting.

Runtime PR #187:
- final tested head `b4e0248b5fbf1d4fbc65c62181b8d1bfb74dc8ff`;
- CI #950 / run `31929295850`: SUCCESS, **605 passed in 45.27s**;
- merge `c1ee61ad335ea3fd37509e868c8b406e20d714b7`;
- Deploy #240 / run `31929343421`: SUCCESS.

No production cognition call was fabricated solely to populate the viewer.

### Latest completed feature — Cognition Context Efficiency v1

Status: **COMPLETE / DEPLOYED / CLOSED**.

The inspector exposed a real production prompt-bloat issue. A read-only pre-compaction audit on Deploy #242 measured **66,952 full-prompt characters** and **64,575 runtime-context characters**. `capability_awareness` contributed 24,404 characters (37.8%) and `action_options` 17,866 (27.7%); `training_method` metadata alone contributed 8,411 characters.

PR #191 compacted only the model-facing projection. It removes repeated capability-definition/application prose and repeated training catalog/planning metadata while preserving executable action/target/duration/resource, movement-ID, proficiency, requirement, risk and supporting-knowledge semantics. Deterministic state/validation/mutation contracts are unchanged, and the Telegram inspector still observes the same `_compact_prompt_state()` projection sent to the model.

Runtime PR #191:
- final tested head `b4febc29ad7ba37d67547346abd5bb9fff73b772`;
- CI #954: SUCCESS, **613 passed in 53.34s**;
- task-relevant acceptance workflows green;
- merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`;
- Deploy #243 / run `31931381264`: **SUCCESS**, including production cognition-context audit execution.

The GitHub connector confirmed the successful deploy/audit job but did not expose the raw redirected job-log body, so no post-deploy reduction percentage is invented. The v1 closure is based on measured baseline targeting, deterministic serialized-size reduction coverage, semantic-preservation regressions, full CI, and successful production deploy/audit execution. See `docs/COGNITION_CONTEXT_EFFICIENCY_V1.md`.

## Current verified deployment

Latest runtime deployment: **Deploy #243 / run `31931381264` SUCCESS**, Cognition Context Efficiency v1.

Verified deployment evidence:
- runtime merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6` deployed;
- install/configure/restart/verify step succeeded;
- production cognition-context audit step completed successfully;
- schema remains v5;
- no schema migration and no synthetic production cognition call were required for this slice.

## Development boundaries

- LLM proposes; deterministic runtime validates/mutates.
- Do not repeatedly run the full suite.
- Do not reopen planning, modifiers, action-condition syntax, routines, participant history, relationships, memory or environment merely for depth.
- Do not infer a missing foundation merely because an existing one lacks exhaustive mechanics.
- Do not continue speculative cognition-context trimming after v1; reopen only with measured prompt-size/cognition-quality evidence.
- No giant planner/task graph, universal episodic-memory engine, witness model, weather/economy/vehicles merely for completeness, hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, modifier authoring UI/status-effect taxonomy, universal condition language, or real-world weapon instructions unless separately planned within policy and project scope.
- Do not fabricate production actions/actors/casualties/modifiers/shared events/cognition calls solely for proof.

## Exact resume point

**Overall Workflow/Foundation Review v1 remains COMPLETE / CLOSED. Telegram Cognition Context Inspector v1 and Cognition Context Efficiency v1 are COMPLETE / DEPLOYED. The latest runtime checkpoint is PR #191, final tested head `b4febc29ad7ba37d67547346abd5bb9fff73b772`, CI #954 with 613 passing tests, merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`, and Deploy #243 SUCCESS. Cognition prompt compaction is CLOSED v1: it targets the two measured dominant metadata sources while preserving deterministic/runtime semantics and exact decision-relevant identifiers. Resume with the next Creator-prioritized product feature, not further speculative context trimming or generic gap hunting.**