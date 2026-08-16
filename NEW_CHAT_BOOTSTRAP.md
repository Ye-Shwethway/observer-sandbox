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

The **Overall Workflow/Foundation Review v1 is COMPLETE / CLOSED**.

The bounded final closure pass found no additional blocking cross-system foundation gap. Do not continue open-ended gap hunting by default.

Four evidence-selected structural gaps were closed during the review:
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

Final bounded reinspection also confirmed:
- actor scheduler/runtime state is actor-scoped and authoritative;
- cognition receives authoritative action options and deterministic validation remains downstream authority;
- model dry-run enforces proposal-only/no-mutation behavior;
- authored time windows + simulation time + physiological priorities already influence cognition;
- world topology/location and reachable-resource context already participate in planning/execution.

Absence of exhaustive depth is not a foundation defect. Rich relationships, generalized group coordination, broad episodic memory, witness inference, weather, economy, vehicles and similar domains are explicit feature/depth candidates only.

## Current phase — Creator Feature Planning

The project is now implementing explicitly requested product features as minimum-runnable slices.

For each proposed feature:
- define the user-visible capability;
- identify current-contract dependencies;
- separate minimum-runnable scope from later depth;
- compare value, implementation cost and runtime risk;
- use one exemplar only for a genuinely new invariant, then batch equivalent follow-ons.

Reopen the Overall Workflow/Foundation Review only when concrete feature work exposes a cross-system invariant the current runtime cannot represent or execute safely.

### Latest completed feature — Telegram Cognition Context Inspector v1

Status: **COMPLETE / DEPLOYED**.

The selected Character Telegram page now gives the configured owner a `Cognition Context` viewer directly below `Profile`. It shows the actual compact runtime context captured immediately before production cognition injection, keeps only the latest three actor-scoped injections, labels primary versus corrective retry, renders future context keys generically, and uses a single-message Prev/Next pager for long snapshots rather than message splitting.

Runtime PR: **#187 — Telegram Cognition Context Inspector v1**
- final tested head: `b4e0248b5fbf1d4fbc65c62181b8d1bfb74dc8ff`;
- merge: `c1ee61ad335ea3fd37509e868c8b406e20d714b7`;
- CI #950 / run `31929295850`: **SUCCESS**;
- **605 passed in 45.27s**;
- fresh DB init/status healthy; schema v5;
- final-head task-relevant acceptance workflows green;
- Deploy #240 / run `31929343421`: **SUCCESS**.

No production cognition call was fabricated solely to populate the new viewer. Snapshot history begins naturally on the next real production cognition injection.

## Current verified deployment

Latest runtime deployment: **Deploy #240 / run `31929343421` SUCCESS**.

Production readback after Deploy #240:
- service active/healthy;
- schema v5;
- autonomy enabled, normal mode, retry null, pending action `09c5b034-d175-48db-87c5-32557993561e` preserved;
- speed **1x**;
- Darian remained naturally **sleeping in Darian's Master Suite**;
- living state: cleanliness 98.491, energy 88.791, fatigue 6.305, hunger 7.578, sleepiness 58.55, thirst 23.15;
- deploy output exposed sim time only as `2025-05-07T***:27:00+00:00`; do not guess the masked hour;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

## Development boundaries

- LLM proposes; deterministic runtime validates/mutates.
- Do not repeatedly run the full suite.
- Do not reopen planning, modifiers, action-condition syntax, routines, participant history, relationships, memory or environment merely for depth.
- Do not infer a missing foundation merely because an existing one lacks exhaustive mechanics.
- No giant planner/task graph, universal episodic-memory engine, witness model, weather/economy/vehicles merely for completeness, hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, modifier authoring UI/status-effect taxonomy, universal condition language, or real-world weapon instructions unless separately planned within policy and project scope.
- Do not fabricate production actions/actors/casualties/modifiers/shared events/cognition calls solely for proof.

## Exact resume point

**Overall Workflow/Foundation Review v1 remains COMPLETE / CLOSED. Telegram Cognition Context Inspector v1 is COMPLETE / DEPLOYED through PR #187, final tested head `b4e0248b5fbf1d4fbc65c62181b8d1bfb74dc8ff`, CI #950 with 605 passing tests, merge `c1ee61ad335ea3fd37509e868c8b406e20d714b7`, and Deploy #240 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action preserved and speed 1x. The owner-only Cognition Context viewer will naturally accumulate its latest-three snapshot history starting with the next real production cognition injection; no synthetic call was made for proof. Resume with the next Creator-prioritized product feature rather than generic gap hunting.**
