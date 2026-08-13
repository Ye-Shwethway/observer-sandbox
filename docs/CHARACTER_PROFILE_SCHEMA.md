# Character Profile Schema

## Purpose

Observer Sandbox uses a deep profile ontology so characters can become progressively more life-like without rebuilding persistence. A field may exist before its simulation engine exists; it remains canonical/static until an authorized engine activates it.

## Storage model

Character profile ontology is intentionally separate from scheduler/runtime-control state.

Profile/domain tables include:
- `profile_field_definitions`
- `character_profiles`
- `character_profile_values`
- `character_profile_history`
- `character_preferences`
- `character_habits`
- `character_routines`
- `character_skills`
- `character_relationship_state`.

The generic `fields` table remains available for entity/domain state with explicit mode/authority.

**Do not store autonomy scheduler bookkeeping in profile fields.** Schema v4 `actor_runtime` owns per-actor autonomy enabled/mode, pending action reference, lease, retry/backoff and cognition wake telemetry. First-class action state belongs to `action_instances`. Universe-wide time/speed/pause belongs to global runtime state.

This separation matters when multiple characters become autonomous: a character profile describes who the character is and domain state they carry; actor runtime describes how their current cognition/action scheduler is operating.

## Domains

The profile ontology includes identity/chronology, body composition/measurements, detailed appearance, intimate anatomy/physiology, RAPS attributes, social/emotional traits, living physiology, fatigue/soreness/injury/illness/recovery, physical limits, personality/motivation/background and narrative goal/arc state.

Variable-length preferences, habits, routines, skills and relationships use normalized collection tables rather than hundreds of scalar entity columns.

## Sensitivity

Sensitive/intimate fields are represented explicitly and tagged through sensitivity metadata. Sensitivity affects presentation/access policy, not whether the simulation can represent the state. Telegram/UI may require deliberate private-profile views before displaying intimate fields.

## Progressive simulation and authority

Each field carries a mode:
- `canonical` — manually authoritative
- `static` — represented, not actively simulated
- `derived` — calculated from other facts
- `simulated` — actively updated by an authorized engine.

Examples:
- height -> canonical / `profile_core`
- age -> derived / `time_engine`
- hunger -> simulated / `needs_engine`
- body fat -> future simulated / `physiology_engine`
- measurements -> future simulated / `body_progression_engine`
- intimate physiology -> future simulated / `sexual_physiology_engine`
- injury state -> future simulated / `injury_engine`.

Domain engines may mutate only fields they own. LLMs never receive arbitrary profile-write authority.

## Composable-runtime relationship

Profile state is one input to the LEGO runtime:

`Actor profile/state + Action + Place + Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.

Actions may read profile/domain fields as prerequisites or modifiers, but action history belongs to events/action instances rather than being embedded into the profile. Temporary sourced effects should use the shared modifier contract rather than silently rewriting canonical traits.

## Future grading relationship

Observer Sandbox is expected to gain a cross-domain grading/progression layer later. Character attributes and skills are likely early consumers, but grading must not become a second source of truth for the profile.

Default rule:
- the underlying profile value remains authoritative;
- a grade is normally a derived evaluation under a named grading scheme;
- changing grade thresholds must not silently rewrite the raw profile value;
- Telegram/profile presentation may display grade badges later, but presentation must not own grading logic.

Do not add speculative grade columns to profile tables during P2.2.4. The first grading implementation must be a separate minimum-runnable slice driven by a concrete use case and follow `docs/FUTURE_GRADING_SYSTEM.md`.

## Conflict policy

Source disagreements are value-reconciliation issues, not reasons to weaken the ontology. New imports must not silently overwrite canonical values. Conflicting historical values remain traceable through source/revision/history metadata.

## Extension rule

New character domains should normally add field definitions/collection structures and an explicit engine authority, not restructure the actor identity or scheduler tables. Keep Profile, Actor Runtime, Action Instances and Events distinct.