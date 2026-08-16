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

The active phase is the **Overall Workflow/Foundation Review**. Its first selected structural gap — **Autonomy Intent Continuity v1** — is now COMPLETE. Continue the read-only review before selecting another runtime slice.

Relevant docs:
- `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`
- `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`
- `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`

## Overall Workflow/Foundation Review status

Initial source-level audit found the following minimum foundations already present:
- generic action/task lifecycle;
- resources/inventory/state consequences;
- environment/world topology/context;
- object knowledge/familiarity;
- generic inter-character participation socket;
- event/lifecycle evidence;
- long-horizon progression/decay exemplars;
- profile -> cognition/runtime integration.

The first actual gap was persistent purpose continuity across action boundaries.

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

## Adaptive disposition checkpoint

- PR #167 — Habit Formation/Extinction v1 COMPLETE.
- PR #172 — Hobby/Interest Lifecycle v1 COMPLETE.
- PR #174 — Preference Adaptation v1 COMPLETE.
- PR #176 — Slow Personality Plasticity v1 COMPLETE.

Authored personality remains baseline authority. Learned disposition state changes only through deterministic bounded evidence contracts; LLM cognition remains proposal-only.

## Autonomy Livelock Watchdog v1 — COMPLETE

PR #170's bounded watchdog remains installed for repeated authoritative action/target pair-validation livelock. It does not recover provider/API/quota/rate-limit or unrelated failures and must not grow into a general action chooser.

## Current verified deployment

Latest runtime deployment: **Deploy #236 / run `31920905305` SUCCESS**.

Runtime PR: **#178 — Autonomy Intent Continuity v1**
- final tested head: `563e102c6a9d73ea2f39e828da6329840632ef79`;
- merge: `0cf9a38e7fadafa178f1f69f9f5b7013cbd1961f`;
- **CI #940 / run `31920821319`: SUCCESS**;
- **583 passed in 58.57s**;
- fresh DB init/status healthy; schema v5;
- all automatic production-copy acceptance gates succeeded without retry.

Production readback after Deploy #236:
- service active/healthy;
- schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **1x**;
- Darian was naturally **sleeping in Darian's Master Suite**;
- deploy output exposed sim time only as `2025-05-07T***:27:00+00:00`; do not guess the masked hour;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

No `autonomy_intent_v1:` row was present in deploy readback. Deploy/init did not fabricate purpose state; no live intent is claimed.

Natural Preference Adaptation evidence remained present but is not overinterpreted as established preference state.

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
- Do not automatically deepen autonomy planning after the intent exemplar.
- Do not infer a missing foundation merely because an existing one lacks exhaustive depth.
- No relationship-system expansion by default.
- No giant planner/task graph, universal episodic-memory engine, weather/economy/vehicles merely for completeness, hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, or real-world weapon instructions.
- Do not fabricate production actions/actors/casualties solely for proof.

## Exact resume point

**Overall Workflow/Foundation Review v1 is active. Autonomy Intent Continuity v1, the first structural gap selected by that review, is COMPLETE through PR #178 final head `563e102c6a9d73ea2f39e828da6329840632ef79`, merge `0cf9a38e7fadafa178f1f69f9f5b7013cbd1961f`, CI #940 with 583 passed, and Deploy #236 SUCCESS. Production is healthy at schema v5, autonomy normal, retry null, pending action present, speed 1x; Darian was naturally sleeping in the Master Suite. The sim-time hour was masked in deploy output (`2025-05-07T***:27:00+00:00`). No synthetic intent state was created. Continue the read-only Overall Workflow/Foundation Review and select the next actual cross-system gap from current canonical/live evidence rather than automatically deepening planning.**
