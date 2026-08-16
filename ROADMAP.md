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
- Verification is focused-first. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite; do not deliberately repeat the full suite after merge.

## Character Profile checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1.

Minimum-unlocked means authoritative state plus meaningful runtime/cognition influence and appropriate persistence/rendering. It does not mean exhaustive local mechanics.

## Adaptive Character Disposition Foundation — COMPLETE v1

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`.

Completed sequence:
`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`

- PR #167: Habit Formation/Extinction v1.
- PR #172: Hobby/Interest Lifecycle v1.
- PR #174: Preference Adaptation v1.
- PR #176: Slow Personality Plasticity v1.

Authored personality remains the stable baseline; preferences/hobbies/habits/personality adapt only through their deterministic bounded evidence contracts. Do not deepen psychology next without a broader foundation reason.

## Skills — CLOSED v1

Frozen learned Skill surface:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is a derived/non-executable parent over Bladed Weapons + Firearms. Hidden legacy `weapons` is compatibility only.

## Autonomy continuity

### Livelock Watchdog v1 — COMPLETE

PR #170 provides a bounded recovery path for repeated authoritative action/target pair-validation livelock only. It is not a deterministic story chooser and does not recover provider/API/quota/rate-limit or unrelated failures.

### Autonomy Intent Continuity v1 — COMPLETE

See `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`.

PR #178 closes the first gap selected by the Overall Workflow/Foundation Review:
- one bounded actor-scoped active intent at most;
- purposeful `move` may establish short cross-action purpose state;
- next cognition receives compact guidance only;
- action legality, needs and safety always remain authoritative;
- up to four movement steps may continue the purpose;
- self-care may interrupt without forcing abandonment;
- ordinary local follow-up clears only after represented completion;
- stale intent expires after 12 simulated hours at the next free decision boundary;
- persistence uses existing `runtime_state`; schema remains v5;
- core `autonomy.autonomy_tick` remains unchanged behind the thin wrapper.

## Overall Workflow/Foundation Review — ACTIVE

See `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`.

Initial audit classifications:
- generic action/task lifecycle: CLOSED v1;
- resources/inventory/state consequences: CLOSED v1;
- environment/world context: CLOSED v1 minimum;
- knowledge/object familiarity: CLOSED v1 minimum;
- inter-character participation: CLOSED v1 socket;
- event/lifecycle handling: CLOSED v1;
- longer-horizon progression/decay: CLOSED v1 exemplars;
- profile -> cognition/runtime integration: CLOSED v1;
- autonomy purpose continuity: was the highest-leverage gap and is now CLOSED v1 through PR #178.

Do not infer that the review itself is finished. Return to read-only canonical/live evidence and select the next genuine cross-system gap rather than automatically deepening planning.

## Current verified deployment

Latest runtime deployment: **Deploy #236 / run `31920905305` SUCCESS**, Autonomy Intent Continuity v1.

Runtime PR #178:
- final tested head `563e102c6a9d73ea2f39e828da6329840632ef79`;
- **CI #940 / run `31920821319`: SUCCESS**;
- **583 passed in 58.57s**;
- fresh DB init/status healthy; schema v5;
- all automatic production-copy acceptance gates green without retry;
- merge `0cf9a38e7fadafa178f1f69f9f5b7013cbd1961f`;
- Deploy #236 SUCCESS.

Verified production readback after Deploy #236:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **1x**;
- Darian was naturally **sleeping in Darian's Master Suite**;
- deploy log exposed sim time only as `2025-05-07T***:27:00+00:00`; the masked hour is not inferred;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

No `autonomy_intent_v1:` row appeared in the deploy readback. Deploy/init therefore did not fabricate an active purpose; natural production intent remains unclaimed until a qualifying purposeful `move` occurs.

Existing ordinary Preference Adaptation evidence remained present, including one-day evidence for the Media Console/Sofa and repeated same-day Personal Desk use. These are not overinterpreted as established preferences.

## Deferred boundaries

No giant planner/task graph, relationship-system expansion by default, universal episodic-memory engine, weather/economy/vehicle systems merely for completeness, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, deep weapon taxonomy, quests/jobs, real-world weapon instructions, arbitrary LLM profile mutation, or synthetic production actors/actions solely for proof.

## Exact resume point

**Overall Workflow/Foundation Review v1 is active. Its first identified structural gap, Autonomy Intent Continuity v1, is COMPLETE through PR #178 final head `563e102c6a9d73ea2f39e828da6329840632ef79`, CI #940 with 583 passed, merge `0cf9a38e7fadafa178f1f69f9f5b7013cbd1961f`, and Deploy #236 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action present and speed 1x; Darian was naturally sleeping in the Master Suite. The deploy log masked the sim-time hour (`2025-05-07T***:27:00+00:00`). No synthetic intent state was created. Resume by continuing the read-only Overall Workflow/Foundation Review and select the next actual cross-system gap from evidence; do not automatically deepen autonomy planning.**
