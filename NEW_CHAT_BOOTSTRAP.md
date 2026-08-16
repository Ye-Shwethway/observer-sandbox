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

Do not reopen local psychology merely for depth.

The active phase is the **Overall Workflow/Foundation Review**. Four selected structural gaps are now COMPLETE:
1. **Autonomy Intent Continuity v1** — PR #178 / Deploy #236.
2. **Active Modifier Runtime Foundation v1** — PR #180 / Deploy #237.
3. **Action Condition Runtime Foundation v1** — PR #182 / Deploy #238.
4. **Participant-Aware Recent Event Context v1** — PR #184 / Deploy #239.

Continue the read-only review before selecting another runtime slice.

Relevant docs:
- `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`
- `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`
- `docs/ACTIVE_MODIFIER_RUNTIME_V1.md`
- `docs/ACTION_CONDITION_RUNTIME_V1.md`
- `docs/PARTICIPANT_RECENT_EVENT_CONTEXT_V1.md`
- `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`

## Overall Workflow/Foundation Review status

Minimum foundations already classified present:
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

### Autonomy Intent Continuity v1 — COMPLETE

PR #178 provides one bounded actor-scoped purpose bridge across action boundaries without overriding legal options, physiological priorities, or safety. Persistence uses existing `runtime_state`; schema remains v5. No planner/task graph or deterministic story chooser was introduced.

### Active Modifier Runtime Foundation v1 — COMPLETE

PR #180 makes the existing `active_modifiers` persistence socket executable through a bounded deterministic numeric resolver. Temporary effective values remain separate from raw authoritative physiology. No modifier producer, authoring UI, universal bonus system, or schema change was introduced.

### Action Condition Runtime Foundation v1 — COMPLETE

PR #182 makes `action_definitions.conditions_json` executable through one bounded fail-closed prerequisite seam. V1 supports a conjunctive `all` list with primitive comparisons only. The canonical `train` definition now owns `physiology.fatigue < 70`; option shaping and direct validation share that prerequisite. Proposal `Action.conditions` remains non-authoritative instance metadata.

### Participant-Aware Recent Event Context v1 — COMPLETE

PR #184 closes the read-side mismatch between authoritative `event_participants` and cognition history:
- an event is relevant when the character is primary actor or an authoritative participant;
- the existing bounded recent-event window and chronological ordering remain unchanged;
- cognition receives primary `actor_id` plus its own persisted `participation_role`;
- actor-owned events remain visible once, with legacy actor fallback;
- unrelated characters receive nothing merely from event existence or co-location;
- no relationship state, witness model, social interpretation, generalized group coordination, long-term episodic-memory engine, or schema change was introduced.

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

Latest runtime deployment: **Deploy #239 / run `31924581764` SUCCESS**.

Runtime PR: **#184 — Participant-Aware Recent Event Context v1**
- final tested head: `09f629b197b55f0abc8271e22e86a9a11f2cab0c`;
- merge: `13d4a9270f3c372a5180438f92f13441d98e804a`;
- **CI #944 / run `31924499307`: SUCCESS**;
- **600 passed in 44.52s**;
- fresh DB init/status healthy; schema v5;
- Cognition Capability Awareness v1 Acceptance #24: SUCCESS;
- Solo Regulation Naturalism v2 Acceptance #33: SUCCESS;
- Eating Behavior v1 Acceptance #46: SUCCESS;
- Training Movement Contract Normalization v1 Acceptance #14: SUCCESS;
- Research Action Semantics Acceptance #45: SUCCESS.

Production readback after Deploy #239:
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

No production shared event was fabricated to manufacture participant-aware cognition evidence.

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
- Do not automatically deepen autonomy planning, modifiers, action-condition syntax, routine scheduling, participant history, relationships, or memory after their minimum closure.
- Do not infer a missing foundation merely because an existing one lacks exhaustive depth.
- No relationship-system expansion by default.
- No giant planner/task graph, universal episodic-memory engine, witness model, weather/economy/vehicles merely for completeness, hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, modifier authoring UI/status-effect taxonomy, universal condition language, or real-world weapon instructions.
- Do not fabricate production actions/actors/casualties/modifiers/shared events solely for proof.

## Exact resume point

**Overall Workflow/Foundation Review v1 is active. Four selected structural gaps are COMPLETE: Autonomy Intent Continuity v1 through PR #178 / Deploy #236; Active Modifier Runtime Foundation v1 through PR #180 / Deploy #237; Action Condition Runtime Foundation v1 through PR #182 / Deploy #238; and Participant-Aware Recent Event Context v1 through PR #184 final head `09f629b197b55f0abc8271e22e86a9a11f2cab0c`, final CI #944 with 600 passed, merge `13d4a9270f3c372a5180438f92f13441d98e804a`, and Deploy #239 / run `31924581764` SUCCESS. Production is healthy at schema v5, autonomy normal, retry null, pending action preserved, speed 1x; Darian remained naturally sleeping in the Master Suite. The sim-time hour was masked in deploy output (`2025-05-07T***:27:00+00:00`). Resume by continuing the read-only Overall Workflow/Foundation Review and selecting the next actual cross-system gap from current canonical/live evidence rather than deepening planning, modifiers, condition syntax, routines, participant history, relationships, or memory.**
