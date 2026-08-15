# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Current Creator instruction, current repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic engines validate and mutate.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are exemplars, never reusable-engine identity.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #215 / run `31881627886` SUCCESS**, Field Medicine Stabilization Consequence Consumer v1, PR #140 merge `2c5f7602dc6263caa74658ae2fadd65aa4857124`.

Final tested PR head: `512f588df3e1b8256f61958a9336e5c0d3b8d17a`.

Verified validation evidence:
- **CI #868 / run `31881576876` SUCCESS**;
- full suite: **472 passed**;
- fresh DB `sandboxctl init` succeeded;
- fresh DB `sandboxctl status` healthy, schema v5;
- Represented Skill Task Contract v1 Acceptance #17 succeeded;
- Represented Skill Task Instance v1 Acceptance #15 succeeded;
- Technology Diagnostic Task Runtime v1 Acceptance #15 succeeded;
- Strength Live Cycle Validation v1 #49 succeeded;
- Inventory Foundation, Eating Behavior, Nutrition & Energy, Skill Evidence Semantics, and Skill Progression acceptance lanes all succeeded.

Verified post-deploy production evidence:
- service active/healthy; schema remains v5;
- production `sandboxctl init` succeeded;
- autonomy enabled, normal mode, 1x, retry `null`, with a pending action;
- cognition binding remained `gemini-3.1-flash-lite`; Groq fallback bootstrap remained healthy;
- Telegram bot token/owner/allowed-user configuration remained present and Telegram API connectivity remained healthy;
- live state remained naturally at sim time `2025-05-06T08:35:00+00:00` during deployment readback;
- Darian was naturally `rest`ing in the Home Gym at readback;
- no production casualty, represented stabilization session, or field-medical-supply fixture was fabricated solely for proof;
- no live `stabilize` action or represented consequence was forced in production.

Exact Field Medicine stabilization consequence behavior is proven by full CI and ephemeral fresh-DB fixtures. Production deploy/init proves that the new action vocabulary, task registry, runtime module, and event integration load safely. Keep those evidence claims distinct.

Production parent Skill state remains authoritative:
- H2H `90 / S`
- Weapons `87 / A`
- Survival `85 / A`
- Tactical Planning `92 / S`
- Technology `82 / A`
- Field Medicine `75 / A`.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. Legacy RAPS skill-like fields remain compatibility/provenance only.

## Completed current execution chain

Recent canonical line:
1. Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
2. Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
3. Cognition Capability Awareness v1 — PR #124 / Deploy #206
4. Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
5. Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
6. Sanitized Autonomy Error Readback — PR #127 corrected by PR #128
7. Training Movement Contract Normalization v1 — PR #129 / Deploy #209
8. Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
9. Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
10. Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
11. Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213
12. Represented Consequence State Foundation v1 — PR #138 / Deploy #214
13. **Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215.**

Canonical execution stack now includes:
- Skill definition/application/capability + actor adapter;
- represented Skill task registry + exact instance resolver;
- cognition capability-awareness projection;
- bounded cognitive/performance modifier resolver;
- low-risk represented-Skill runtime reuse;
- generalized controlled-H2H explicit multi-actor authorization/runtime path;
- immutable application-evidence path separate from learning evidence;
- domain-neutral represented consequence-state application foundation;
- first real domain consumer of that consequence foundation through bounded Field Medicine stabilization.

## Represented Skill runtime state

### Low-risk represented pattern — complete and batched

Technology diagnostic and Tactical assessment established the initial represented-task exemplars. PR #133 reused that pattern for Tactical maneuver planning plus both Survival applications without movement execution, shelter/resource mutation, consequence-state mutation, or automatic XP.

### Controlled H2H interaction pattern — current H2H application surface complete

One generic action remains authoritative: `spar`.

Exact represented session definition selects the H2H application:
- `h2h_controlled_striking_spar_v1` -> `hand_to_hand_combat.engage_unarmed_striking` -> `scored_contact_only`;
- `h2h_controlled_grapple_spar_v1` -> `hand_to_hand_combat.control_unarmed_grapple` -> `scored_positional_control_only`.

Both reuse exact represented target binding, one distinct colocated consenting character participant, parent H2H Skill authority, bounded task-specific modifiers, and immutable application evidence. Neither path authorizes hostile/non-consensual use or mutates injury, incapacity, persistent restraint, or participant state.

H2H performance uses Reflexes + Agility + Focus where declared. IQ is intentionally absent and legacy `raps_pa.combat_skill` is excluded.

## Represented Consequence State Foundation v1 — complete

PR #138 / Deploy #214 implemented the generic bridge:

`validated represented task -> deterministic consequence authorization -> bounded simulated-state mutation -> causal event evidence`

Implementation: `src/observer_sandbox/represented_consequence_state.py`.
Canonical design note: `docs/REPRESENTED_CONSEQUENCE_STATE_FOUNDATION_V1.md`.

The foundation composes schema-v5 primitives:
- `fields` remains generic state storage;
- only pre-existing fields with `mode='simulated'` are mutable through this API;
- `action_instances` remains source-action authority;
- events retain state-change evidence, action/location identity, causal parent, and participants;
- `active_modifiers` remains a future socket and is not activated globally.

A `ConsequenceAuthorization` must explicitly bind consequence id, exact represented task id already persisted on the completed source action, subject id, subject relationship (`actor`, `target`, or `participant`), and a finite mutation list.

Supported immediate operations reuse the established effect vocabulary:
`add`, `multiply`, `set`, `clamp_min`, `clamp_max`.

Hard boundaries:
- source action must already be completed and have its `action_completed` event;
- represented-task id must match exactly;
- subject must actually be the declared actor/target/participant;
- consequence application cannot create new state fields;
- canonical/static/derived fields fail closed;
- Skill score, IQ, performance quality, model prose, or generic capability cannot independently authorize mutation;
- field authority/source metadata are preserved;
- successful application emits `represented_consequence_applied` causally linked to the source completion event;
- consequence evidence is not learning evidence and awards no Skill XP;
- application is savepoint-atomic and retry-idempotent.

## Field Medicine Stabilization Consequence Consumer v1 — complete

PR #140 / Deploy #215 is the first real represented consequence consumer.

Represented task registry revision: `represented-skill-tasks-v1.5`.

Task:
`field_medicine_stabilize_for_evacuation_v1`

Action vocabulary:
`stabilize`

Application:
`field_medicine.stabilize_for_evacuation`

Exact represented-session contract:
- target entity type: object;
- target definition: `represented_task:field_medicine_stabilization_session_v1`;
- target capabilities: `stabilize`, `field_medical_context`, `evacuation_or_handoff_needed`;
- exactly one distinct casualty character participant;
- casualty must be colocated with actor;
- casualty must already expose pre-existing numeric `medical.deterioration_risk` in range 0..100 with field mode `simulated`;
- one or more explicitly represented local or carried resource objects must collectively expose `field_medical_supplies`.

V1 consequence scope is intentionally one field only:
`medical.deterioration_risk`.

The stabilization runtime:
- resolves the exact represented task through the existing represented Skill task instance resolver;
- keeps the parent Field Medicine Skill score as learned-capability authority;
- resolves a bounded stabilization result;
- persists immutable `skill_application_evidence`;
- only after the source `action_completed` event exists, calls the generic consequence foundation;
- authorizes the casualty participant as consequence subject;
- applies one bounded `set` mutation to the pre-existing simulated deterioration-risk field;
- emits causally linked `represented_consequence_applied` evidence;
- preserves the casualty field's existing authority/source metadata;
- remains atomic and retry-idempotent through the generic foundation.

Current Darian exemplar behavior in ephemeral tests:
- Field Medicine `75 / A` resolves a `solid` stabilization result;
- example deterioration risk `60 -> 40`;
- this is test evidence only and is not a production casualty event.

Explicit non-goals / boundaries:
- no injury or wound taxonomy;
- no bleeding model;
- no diagnosis state creation;
- no definitive-treatment completion state;
- no death/incapacity simulation;
- no automatic casualty-state creation;
- no medical-resource depletion/durability yet;
- no real-world medical-advice surface;
- no Field Medicine XP from application or consequence evidence;
- no production casualty/session/supply seed solely for validation.

## Cognition / evidence boundary

Cognition receives read-only semantic capability awareness. Supporting Attributes and IQ affect performance only through explicit task-specific contracts after deterministic feasibility. They cannot create Knowledge, proficiency, consent, resources, authorization, state fields, or consequences.

Field Medicine stabilization v1 intentionally does not introduce a new IQ/medical-knowledge modifier contract. Parent Field Medicine Skill remains the bounded capability authority for this exemplar; consequence authorization remains separately deterministic.

Runtime application/consequence evidence is not learning evidence. Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival, and Field Medicine definitions do not activate XP by themselves.

## Next development sequence

1. **Casualty State Origin & Lifecycle Contract v1 — REVIEW NEXT / not yet implemented.**
2. The stabilization consumer deliberately requires a pre-existing simulated `medical.deterioration_risk`; the next architectural question is which domain authority may create/initialize that state and how its lifecycle is represented.
3. Define the smallest explicit casualty-state origin contract before adding broader Field Medicine assessment, diagnosis, treatment, deterioration, or recovery mechanics.
4. Do not solve this by building a full Injury Engine. Prefer one bounded casualty-state origin/lifecycle exemplar with clear source event, ownership, state initialization, mutation authority, and cleanup/recovery boundary.
5. Do not infer casualty state from model prose, Skill score, generic combat outcomes, or ordinary events.
6. Keep Weapons separate until its exact resource/safety/target/consequence contract is reconciled; Weapons lethality remains a distinct structural question.
7. Do not turn controlled H2H sparring into injury/restraint state merely to manufacture a casualty producer.
8. Batch only structurally equivalent casualty-state producers after one bounded origin invariant is proven.
9. Keep application/consequence evidence separate from learning evidence; no automatic XP.

## Deferred boundaries

No hostile/non-consensual combat engine, full Injury Engine, persistent restraint/incapacity system, Weapons lethality system, broad casualty simulator, bleeding/wound taxonomy, definitive-treatment engine, universal active-modifier evaluator, full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior rewrite, deep crafting, second production character solely for testing, or Tahoe exterior traversal as side effects of the next slice.

## Exact resume point

**Field Medicine Stabilization Consequence Consumer v1 is complete through PR #140 final tested head `512f588df3e1b8256f61958a9336e5c0d3b8d17a`, merge `2c5f7602dc6263caa74658ae2fadd65aa4857124`, CI #868 / run `31881576876` with 472 passing tests plus fresh-DB init/status, and Deploy #215 / run `31881627886` SUCCESS. The first real consequence consumer now proves exact represented stabilization task + one colocated casualty participant + explicit field-medical-supply resource -> bounded mutation of only pre-existing simulated `medical.deterioration_risk` -> causal consequence event, with no diagnosis, definitive treatment, resource depletion, XP, or fabricated production casualty. Next review the missing casualty-state origin/lifecycle authority before expanding medical consequence semantics.**
