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

## Conditions / Modifiers

### Active Modifier Runtime Foundation v1 — COMPLETE

See `docs/ACTIVE_MODIFIER_RUNTIME_V1.md`.

PR #180 closes the second actual gap selected by the Overall Workflow/Foundation Review:
- the existing `active_modifiers` persistence socket now has a deterministic numeric resolver;
- half-open simulated-time activation and expiry;
- `stack`, `replace`, `max`, and `min` stack semantics;
- exact explicit context conditions only;
- first consumer is bounded to the six established living-state fields surfaced by `snapshot()`;
- effective values can influence existing cognition/needs/training/action-legality paths;
- raw authoritative physiology remains separate so temporary effects do not become permanent state;
- no modifier producer, authoring UI, universal bonus system or schema change.

Existing Training Readiness and Cognitive Performance contracts remain independent domain-specific modifier systems.

## Overall Workflow/Foundation Review — ACTIVE

See `docs/OVERALL_WORKFLOW_FOUNDATION_REVIEW_V1.md`.

Current audit classifications:
- generic action/task lifecycle: CLOSED v1;
- resources/inventory/state consequences: CLOSED v1;
- environment/world context: CLOSED v1 minimum;
- knowledge/object familiarity: CLOSED v1 minimum;
- inter-character participation: CLOSED v1 socket;
- event/lifecycle handling: CLOSED v1;
- longer-horizon progression/decay: CLOSED v1 exemplars;
- profile -> cognition/runtime integration: CLOSED v1;
- autonomy purpose continuity: CLOSED v1 minimum through PR #178;
- persistent temporary modifier lifecycle: CLOSED v1 minimum through PR #180.

Routine/schedule reinspection also found meaningful authored time-window + simulation-time + physiological-priority influence already present. A full schedule sequence ledger is later depth unless new evidence establishes a missing invariant.

Do not infer that the review itself is finished. Return to read-only canonical/live evidence and select the next genuine cross-system gap rather than deepening a just-closed foundation.

## Current verified deployment

Latest runtime deployment: **Deploy #237 / run `31921444434` SUCCESS**, Active Modifier Runtime Foundation v1.

Runtime PR #180:
- final tested head `49000d37542ec80cf489f8bd5c78876aaba16201`;
- **CI #941 / run `31921368331`: SUCCESS**;
- **590 passed in 58.12s**;
- fresh DB init/status healthy; schema v5;
- Minimum Training Stimulus Acceptance #27: SUCCESS;
- Strength Live Cycle Validation v1 #83: SUCCESS;
- Solo Regulation Naturalism v2 Acceptance #30: SUCCESS;
- merge `74a0d9db25b3249192c24954feed11a45a7c961d`;
- Deploy #237 SUCCESS.

Verified production readback after Deploy #237:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action preserved;
- speed **1x**;
- Darian remained naturally **sleeping in Darian's Master Suite**;
- living state: cleanliness 98.491, energy 88.791, fatigue 6.305, hunger 7.578, sleepiness 58.55, thirst 23.15;
- deploy log exposed sim time only as `2025-05-07T***:27:00+00:00`; the masked hour is not inferred;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

The deploy workflow did not query `active_modifiers` row count. Do not claim a verified production row count or naturally active modifier without a separate readback.

## Deferred boundaries

No giant planner/task graph, relationship-system expansion by default, universal episodic-memory engine, weather/economy/vehicle systems merely for completeness, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, deep weapon taxonomy, quests/jobs, real-world weapon instructions, arbitrary LLM profile mutation, synthetic production actors/actions solely for proof, modifier authoring UI, status-effect taxonomy, or arbitrary universal bonus engine.

## Exact resume point

**Overall Workflow/Foundation Review v1 is active. Its first two identified structural gaps are now closed: Autonomy Intent Continuity v1 through PR #178 / Deploy #236, and Active Modifier Runtime Foundation v1 through PR #180 final head `49000d37542ec80cf489f8bd5c78876aaba16201`, CI #941 with 590 passed, merge `74a0d9db25b3249192c24954feed11a45a7c961d`, and Deploy #237 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action preserved and speed 1x; Darian remained naturally sleeping in the Master Suite. The deploy log masked the sim-time hour (`2025-05-07T***:27:00+00:00`). No live active-modifier row count is claimed. Resume by continuing the read-only Overall Workflow/Foundation Review and select the next actual cross-system gap from evidence; do not automatically deepen planning, modifiers, or routine scheduling.**