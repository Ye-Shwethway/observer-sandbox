# Future Cross-Domain Grading System

Status: RESERVED FOR FUTURE MINIMUM-RUNNABLE SLICE

## Purpose

Observer Sandbox is expected to gain a universal grading/progression language later for characters, attributes, skills, items, locations/facilities, quests/challenges, unlock requirements and other gradeable subjects.

This is a future capability, not an authorization to build a grading engine now.

The current schema-v4 foundation is considered sufficient. Do **not** introduce another broad schema refinement merely to pre-build grading.

## Architectural rules

1. Grading is cross-domain and composable. Do not hard-code independent grading logic separately into character profiles, skills, items, locations, quests or Telegram views.
2. Preserve the underlying authoritative value/state. A grade is normally a derived evaluation of that value under a named grading scheme unless a concrete domain explicitly defines grade itself as canonical state.
3. Grading must be presentation-independent. Telegram may display a grade badge later, but Telegram must never own the grading rule.
4. A grading scheme may later participate in LEGO-runtime validation/conditions, for example skill/attribute/facility requirements for an action or unlock.
5. Do not assume one numeric mapping works for every domain. Character attributes, item quality, facility quality, skill progression and quest difficulty may share a grade vocabulary while using domain-specific evaluators.
6. If a future implementation needs persisted grading structures, add them additively around schema v4 rather than rewriting existing entity/profile/action/event identity.

## Simiverse reference direction

The earlier Simiverse design treated universal grading/tiering as a reusable progression concept rather than a single character-only display feature. Observer Sandbox may reuse that conceptual direction, but must implement it through the project's current minimum-runnable policy rather than importing a large grading subsystem wholesale.

Exact tier names, thresholds, caps and unlock rules are intentionally **not** frozen here. Reconcile them from the chosen future use case and authoritative project direction when the first grading slice is authorized.

## First future runnable slice

When grading becomes useful to a concrete feature, start with exactly one narrow domain, for example:

`existing character attribute value -> grading evaluator -> human-readable grade -> Telegram profile display`

Acceptance should prove that one grade is deterministically derived and observable without changing the underlying raw value. Only then expand grading to skills, items, locations, quests or unlock requirements one domain at a time.

## Current P2 profile-browser rule

P2.2.4 Character Profile Browser must display the existing authoritative profile values without speculative grade badges. The future grading layer should be attachable later without restructuring the profile browser's data ownership.