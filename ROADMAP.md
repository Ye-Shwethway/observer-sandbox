# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Prefer **vertical completeness before local depth**.
- Never manipulate production merely to manufacture evidence.
- Verification is focused-first. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite.

## Character Profile checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1.

Adaptive Character Disposition Foundation is COMPLETE v1:
`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`.

Do not reopen local psychology merely for depth.

## Skills — CLOSED v1

Frozen learned Skill surface:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is derived/non-executable; hidden legacy `weapons` is compatibility only.

## Overall Workflow/Foundation Review — COMPLETE / CLOSED v1

See `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`.

The bounded final closure pass found **no additional blocking foundation gap**. Do not continue open-ended gap hunting by default.

Four evidence-selected structural gaps were closed during the review:
1. **Autonomy Intent Continuity v1** — PR #178 / Deploy #236.
2. **Active Modifier Runtime Foundation v1** — PR #180 / Deploy #237.
3. **Action Condition Runtime Foundation v1** — PR #182 / Deploy #238.
4. **Participant-Aware Recent Event Context v1** — PR #184 / Deploy #239.

Current minimum foundation classifications:
- generic action/task lifecycle: CLOSED v1;
- resources/inventory/state consequences: CLOSED v1;
- environment/world context: CLOSED v1 minimum;
- knowledge/object familiarity: CLOSED v1 minimum;
- inter-character participation: CLOSED v1 socket;
- event/lifecycle handling: CLOSED v1;
- participant-aware recent event cognition: CLOSED v1 minimum;
- longer-horizon progression/decay: CLOSED v1 exemplars;
- profile -> cognition/runtime integration: CLOSED v1;
- autonomy purpose continuity: CLOSED v1 minimum;
- persistent temporary modifier lifecycle: CLOSED v1 minimum;
- action-definition prerequisite runtime: CLOSED v1 minimum.

Routine/schedule reinspection found meaningful authored time-window + simulation-time + physiological-priority influence already present. A full sequence ledger remains later depth.

## Active phase — Creator Feature Planning

The project has moved from foundation-gap review to explicit product feature planning and minimum-runnable feature slices.

For each desired feature:
1. define the user-visible capability and why it matters;
2. identify dependencies on current runtime contracts;
3. separate minimum-runnable behavior from later depth;
4. rank against other requested features by value, dependency, implementation cost and runtime risk;
5. use one bounded exemplar only for a genuinely new invariant, then batch equivalent follow-ons.

A deferred capability is not a foundation defect. Reopen the foundation review only if a concrete feature exposes a cross-system invariant that cannot currently be represented or executed safely.

### Completed Creator feature slice — Telegram Cognition Context Inspector v1

Status: **COMPLETE / DEPLOYED**.

See `docs/TELEGRAM_COGNITION_CONTEXT_INSPECTOR_V1.md`.

The owner-only Telegram viewer now exposes the actual compact cognition context captured immediately before production model injection, keeps the latest three actor-scoped snapshots, distinguishes primary and corrective-retry injections, recursively renders future context keys, and uses a single-message Prev/Next pager for long snapshots instead of Telegram message splitting.

Runtime PR #187:
- final tested head `b4e0248b5fbf1d4fbc65c62181b8d1bfb74dc8ff`;
- CI #950 / run `31929295850`: SUCCESS;
- **605 passed in 45.27s**;
- fresh DB init/status healthy; schema v5;
- final-head task-relevant acceptance workflows green;
- merge `c1ee61ad335ea3fd37509e868c8b406e20d714b7`;
- Deploy #240 / run `31929343421`: SUCCESS.

No production cognition call was fabricated solely to populate the viewer. Its bounded snapshot history begins naturally on the next real cognition injection.

## Current verified deployment

Latest runtime deployment: **Deploy #240 / run `31929343421` SUCCESS**, Telegram Cognition Context Inspector v1.

Verified production readback after Deploy #240:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action `09c5b034-d175-48db-87c5-32557993561e` preserved;
- speed **1x**;
- Darian remained naturally **sleeping in Darian's Master Suite**;
- living state: cleanliness 98.491, energy 88.791, fatigue 6.305, hunger 7.578, sleepiness 58.55, thirst 23.15;
- deploy log exposed sim time only as `2025-05-07T***:27:00+00:00`; the masked hour is not inferred;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

## Deferred boundaries

No giant planner/task graph, relationship-system expansion by default, universal episodic-memory engine, witness model, weather/economy/vehicle systems merely for completeness, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, deep weapon taxonomy, quests/jobs, arbitrary LLM profile mutation, synthetic production actors/actions solely for proof, modifier authoring UI, status-effect taxonomy, arbitrary universal bonus engine, or universal condition/expression language.

These may become explicit feature candidates where appropriate; they are not automatically authorized by foundation closure.

## Exact resume point

**Overall Workflow/Foundation Review v1 remains COMPLETE / CLOSED. Telegram Cognition Context Inspector v1 is the first completed Creator feature slice after foundation closure: PR #187, final head `b4e0248b5fbf1d4fbc65c62181b8d1bfb74dc8ff`, CI #950 with 605 passing tests, merge `c1ee61ad335ea3fd37509e868c8b406e20d714b7`, and Deploy #240 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action preserved and speed 1x. No synthetic cognition call was made to populate the viewer; snapshots begin on the next real production cognition injection. Next work is the next Creator-prioritized feature, not generic gap hunting.**
