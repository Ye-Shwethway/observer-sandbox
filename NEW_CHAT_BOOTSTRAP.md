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
`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`

Do not reopen local psychology merely for depth.

The active phase is the **Overall Workflow/Foundation Review**. Three selected structural gaps are now COMPLETE:
1. **Autonomy Intent Continuity v1** — PR #178 / Deploy #236.
2. **Active Modifier Runtime Foundation v1** — PR #180 / Deploy #237.
3. **Action Condition Runtime Foundation v1** — PR #182 / Deploy #238.

Continue the read-only review before selecting another runtime slice.

Relevant docs:
- `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`
- `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`
- `docs/ACTIVE_MODIFIER_RUNTIME_V1.md`
- `docs/ACTION_CONDITION_RUNTIME_V1.md`
- `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`

## Overall Workflow/Foundation Review status

Minimum foundations already classified present:
- generic action/task lifecycle;
- resources/inventory/state consequences;
- environment/world topology/context;
- object knowledge/familiarity;
- generic inter-character participation socket;
- event/lifecycle evidence;
- long-horizon progression/decay exemplars;
- profile -> cognition/runtime integration;
- autonomy purpose continuity;
- persistent temporary modifier lifecycle;
- action-definition prerequisite runtime.

### Autonomy Intent Continuity v1 — COMPLETE

PR #178 adds a thin deterministic purpose bridge around the unchanged core autonomy scheduler:
- at most one active actor-scoped intent;
- purposeful represented `move` may start it from the committed action reason;
- next cognition receives compact intent guidance, never authority;
- legal action options, physiological needs and safety override it;
- up to four movement steps may continue it;
- `sleep`/`eat`/`drink`/`shower`/`rest` may interrupt without forced abandonment;
- first ordinary local follow-up clears only after represented completion;
- intent older than 12 simulated hours expires at the next free decision boundary;
- transition metadata is traceable under `conditions.autonomy_intent_transition`;
- runtime persistence uses existing `runtime_state`; schema stays v5;
- no new action vocabulary, planner, task graph or deterministic story chooser.

No live production intent is claimed unless ordinary runtime naturally plans a qualifying purposeful move.

### Active Modifier Runtime Foundation v1 — COMPLETE

PR #180 makes the existing `active_modifiers` schema socket executable without creating a universal hidden bonus engine:
- generic numeric effective-value resolver;
- half-open simulated-time activation/expiry;
- deterministic `stack`, `replace`, `max`, and `min` semantics;
- exact caller-supplied context conditions;
- first runtime consumer bounded to energy, hunger, thirst, sleepiness, cleanliness and fatigue;
- effective living-state reads flow through existing cognition/need/training/action-legality consumers;
- temporary modifiers do not overwrite raw authoritative physiology;
- no LLM modifier-write authority, modifier producer, authoring UI or schema change.

Existing Training Readiness and Cognitive Performance remain separate domain-specific modifier systems.

### Action Condition Runtime Foundation v1 — COMPLETE

PR #182 makes `action_definitions.conditions_json` executable through one bounded fail-closed prerequisite seam:
- v1 supports one conjunctive `all` list only;
- primitive comparators are `lt`, `lte`, `gt`, `gte`, `eq`, and `ne`;
- malformed shapes, unknown fields and unsupported operators fail closed;
- first available values are current location plus the six established effective living-state fields;
- the existing systemic-fatigue training legality boundary now lives in the canonical `train` definition as `physiology.fatigue < 70`;
- `action_options()` and `validate_action()` consume the same prerequisite;
- proposal `Action.conditions` remains per-instance represented metadata and cannot grant permission;
- Active Modifier Runtime composes through effective living-state reads without overwriting raw physiology;
- canonical definition conditions resynchronize during initialize; schema remains v5;
- no nested expression language, scripts, cross-entity predicates, authoring UI or new action vocabulary.

Routine/schedule reinspection found authored time windows + current simulation time + physiological priorities already produce meaningful cognition influence. Absence of a full sequence ledger is later depth, not currently a missing minimum foundation.

## Adaptive disposition checkpoint

- PR #167 — Habit Formation/Extinction v1 COMPLETE.
- PR #172 — Hobby/Interest Lifecycle v1 COMPLETE.
- PR #174 — Preference Adaptation v1 COMPLETE.
- PR #176 — Slow Personality Plasticity v1 COMPLETE.

Authored personality remains baseline authority. Learned disposition state changes only through deterministic bounded evidence contracts; LLM cognition remains proposal-only.

## Autonomy Livelock Watchdog v1 — COMPLETE

PR #170's bounded watchdog remains installed for repeated authoritative action/target pair-validation livelock. It does not recover provider/API/quota/rate-limit or unrelated failures and must not grow into a general action chooser.

## Current verified deployment

Latest runtime deployment: **Deploy #238 / run `31922007671` SUCCESS**.

Runtime PR: **#182 — Action Condition Runtime Foundation v1**
- final tested head: `fd86ef8a7a1d40fd58e42922e6fe7678a9bee1cf`;
- merge: `a79d5930b0fb206139d9c8359f3e35aa9499b68e`;
- **CI #943 / run `31921888887`: SUCCESS**;
- **596 passed in 46.28s**;
- fresh DB init/status healthy; schema v5;
- Research Action Semantics Acceptance #43: SUCCESS;
- Strength Live Cycle Validation v1 #85: SUCCESS;
- Solo Regulation Naturalism v2 Acceptance #32: SUCCESS;
- Inventory Foundation v1 Acceptance #49: SUCCESS;
- Minimum Training Stimulus Acceptance #29: SUCCESS.

The preceding CI attempt found one stale test assertion expecting the old bespoke `"systemic fatigue"` error text. Runtime behavior was correct; the assertion was aligned to the generic action-condition semantics and the final CI passed 596/596.

Production readback after Deploy #238:
- service active/healthy;
- schema v5;
- autonomy enabled, normal mode, retry null, pending action preserved;
- speed **1x**;
- Darian remained naturally **sleeping in Darian's Master Suite**;
- living state: cleanliness 98.491, energy 88.791, fatigue 6.305, hunger 7.578, sleepiness 58.55, thirst 23.15;
- deploy output exposed sim time only as `2025-05-07T***:27:00+00:00`; do not guess the masked hour;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

No production state was manipulated to manufacture action-condition evidence.

## Character Profile / Skills baseline

Profile sections minimum-unlocked:
- Identity
- Appearance
- Body
- Attributes
- Recovery
- Sexual
- Personality
- Skills
- Preferences
- Background

Skills CLOSED v1 learned leaves:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is derived/non-executable; hidden legacy `weapons` is compatibility only.

## Development boundaries

- LLM proposes; deterministic runtime validates/mutates.
- Do not repeatedly run the full suite.
- Do not automatically deepen autonomy planning, modifiers, action-condition syntax, or routine scheduling after their minimum closure.
- Do not infer a missing foundation merely because an existing one lacks exhaustive depth.
- No relationship-system expansion by default.
- No giant planner/task graph, universal episodic-memory engine, weather/economy/vehicles merely for completeness, hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, modifier authoring UI/status-effect taxonomy, universal condition language, or real-world weapon instructions.
- Do not fabricate production actions/actors/casualties/modifiers solely for proof.

## Exact resume point

**Overall Workflow/Foundation Review v1 is active. Three selected structural gaps are COMPLETE: Autonomy Intent Continuity v1 through PR #178 / Deploy #236, Active Modifier Runtime Foundation v1 through PR #180 / Deploy #237, and Action Condition Runtime Foundation v1 through PR #182 final head `fd86ef8a7a1d40fd58e42922e6fe7678a9bee1cf`, final CI #943 with 596 passed, merge `a79d5930b0fb206139d9c8359f3e35aa9499b68e`, and Deploy #238 / run `31922007671` SUCCESS. Production is healthy at schema v5, autonomy normal, retry null, pending action preserved, speed 1x; Darian remained naturally sleeping in the Master Suite. The sim-time hour was masked in deploy output (`2025-05-07T***:27:00+00:00`). Resume by continuing the read-only Overall Workflow/Foundation Review and selecting the next actual cross-system gap from current canonical/live evidence rather than deepening planning, modifiers, condition syntax, or routine scheduling.**
