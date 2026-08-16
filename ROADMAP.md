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

### Action Condition Runtime Foundation v1 — COMPLETE

See `docs/ACTION_CONDITION_RUNTIME_V1.md`.

PR #182 closes the third actual gap selected by the Overall Workflow/Foundation Review:
- `action_definitions.conditions_json` is now executable through one bounded fail-closed prerequisite evaluator;
- v1 supports exactly one conjunctive `all` list with primitive `lt`, `lte`, `gt`, `gte`, `eq`, and `ne` clauses;
- first available values are current location plus the six established effective living-state fields;
- malformed contracts, unknown fields and unsupported operators fail closed;
- the existing `train` systemic-fatigue legality boundary is now canonical definition data: `physiology.fatigue < 70`;
- `action_options()` and `validate_action()` consume the same prerequisite contract;
- proposal `Action.conditions` remains represented per-instance metadata and cannot authorize behavior;
- Active Modifier Runtime composes through effective snapshot state while raw physiology remains unchanged;
- initialize resynchronizes canonical definition conditions; schema remains v5;
- no universal expression language, scripts, nested boolean trees, cross-entity predicates, authoring UI or new action vocabulary.

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
- persistent temporary modifier lifecycle: CLOSED v1 minimum through PR #180;
- action-definition prerequisite runtime: CLOSED v1 minimum through PR #182.

Routine/schedule reinspection also found meaningful authored time-window + simulation-time + physiological-priority influence already present. A full schedule sequence ledger is later depth unless new evidence establishes a missing invariant.

Do not infer that the review itself is finished. Return to read-only canonical/live evidence and select the next genuine cross-system gap rather than deepening a just-closed foundation.

## Current verified deployment

Latest runtime deployment: **Deploy #238 / run `31922007671` SUCCESS**, Action Condition Runtime Foundation v1.

Runtime PR #182:
- final tested head `fd86ef8a7a1d40fd58e42922e6fe7678a9bee1cf`;
- **CI #943 / run `31921888887`: SUCCESS**;
- **596 passed in 46.28s**;
- fresh DB init/status healthy; schema v5;
- Research Action Semantics Acceptance #43: SUCCESS;
- Strength Live Cycle Validation v1 #85: SUCCESS;
- Solo Regulation Naturalism v2 Acceptance #32: SUCCESS;
- Inventory Foundation v1 Acceptance #49: SUCCESS;
- Minimum Training Stimulus Acceptance #29: SUCCESS;
- merge `a79d5930b0fb206139d9c8359f3e35aa9499b68e`;
- Deploy #238 SUCCESS.

The preceding CI attempt exposed one stale assertion still expecting the old bespoke `"systemic fatigue"` message. Runtime behavior was already correct; the assertion was aligned to the generic action-condition contract and final CI passed 596/596.

Verified production readback after Deploy #238:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, retry null, pending action preserved;
- speed **1x**;
- Darian remained naturally **sleeping in Darian's Master Suite**;
- living state: cleanliness 98.491, energy 88.791, fatigue 6.305, hunger 7.578, sleepiness 58.55, thirst 23.15;
- deploy log exposed sim time only as `2025-05-07T***:27:00+00:00`; the masked hour is not inferred;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

No production state was manipulated solely to prove action-condition behavior.

## Deferred boundaries

No giant planner/task graph, relationship-system expansion by default, universal episodic-memory engine, weather/economy/vehicle systems merely for completeness, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, deep weapon taxonomy, quests/jobs, real-world weapon instructions, arbitrary LLM profile mutation, synthetic production actors/actions solely for proof, modifier authoring UI, status-effect taxonomy, arbitrary universal bonus engine, or universal condition/expression language.

## Exact resume point

**Overall Workflow/Foundation Review v1 is active. Its first three identified structural gaps are now closed: Autonomy Intent Continuity v1 through PR #178 / Deploy #236, Active Modifier Runtime Foundation v1 through PR #180 / Deploy #237, and Action Condition Runtime Foundation v1 through PR #182 final head `fd86ef8a7a1d40fd58e42922e6fe7678a9bee1cf`, CI #943 with 596 passed, merge `a79d5930b0fb206139d9c8359f3e35aa9499b68e`, and Deploy #238 SUCCESS. Production is healthy at schema v5 with autonomy normal, retry null, pending action preserved and speed 1x; Darian remained naturally sleeping in the Master Suite. The deploy log masked the sim-time hour (`2025-05-07T***:27:00+00:00`). Resume by continuing the read-only Overall Workflow/Foundation Review and selecting the next actual cross-system gap from evidence; do not automatically deepen planning, modifiers, action-condition syntax, or routine scheduling.**
