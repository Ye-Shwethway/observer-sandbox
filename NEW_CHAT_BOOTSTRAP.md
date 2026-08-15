# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

## Workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence. Darian/Thorne Estate are exemplars only.

## Current verified deployment

Latest runtime deployment: **Deploy #215 / run `31881627886` SUCCESS**, Field Medicine Stabilization Consequence Consumer v1, PR #140 merge `2c5f7602dc6263caa74658ae2fadd65aa4857124`.

Final tested PR head: `512f588df3e1b8256f61958a9336e5c0d3b8d17a`.

Validation:
- **CI #868 / run `31881576876` SUCCESS**;
- **472 tests passed**;
- fresh DB `init` succeeded;
- fresh DB `status` healthy, schema v5;
- represented-task contract/instance, Technology Diagnostic, Strength, Inventory, Eating, Nutrition & Energy, Skill Evidence, and Skill Progression acceptance lanes all succeeded.

Post-deploy evidence:
- service active/healthy, schema v5;
- production `sandboxctl init` succeeded;
- autonomy enabled in normal mode at 1x with retry `null` and a pending action;
- cognition binding remained `gemini-3.1-flash-lite`; Groq fallback bootstrap remained healthy;
- Telegram bot/API/owner/allowed-user configuration remained healthy;
- live state remained naturally at sim time `2025-05-06T08:35:00+00:00` during deployment readback;
- Darian was naturally `rest`ing in the Home Gym;
- no production casualty, stabilization session, medical-supply fixture, `stabilize` action, or consequence was fabricated/forced for proof.

Exact stabilization/consequence mutation behavior is proven by full CI and ephemeral fresh-DB fixtures. Production deployment/init proves the runtime path loaded safely; do not overstate that as a live casualty-treatment proof.

Production parent Skill values remain:
- H2H 90/S
- Weapons 87/A
- Survival 85/A
- Tactical Planning 92/S
- Technology 82/A
- Field Medicine 75/A.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. Legacy RAPS skill-like fields remain compatibility/provenance only. Do not create independently scored child Skills yet.

## Completed current execution chain

Recent canonical line:
- Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
- Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
- Cognition Capability Awareness v1 — PR #124 / Deploy #206
- Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
- Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
- Sanitized Autonomy Error Readback — PR #127 corrected by PR #128
- Training Movement Contract Normalization v1 — PR #129 / Deploy #209
- Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
- Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
- Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
- Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213
- Represented Consequence State Foundation v1 — PR #138 / Deploy #214
- **Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215.**

## Represented Consequence State Foundation v1

Implementation: `src/observer_sandbox/represented_consequence_state.py`.
Design note: `docs/REPRESENTED_CONSEQUENCE_STATE_FOUNDATION_V1.md`.

Canonical seam:

`validated represented task -> deterministic consequence authorization -> bounded simulated-state mutation -> causal event evidence`

Boundary:
- source action must be completed and have an `action_completed` event;
- represented-task id must match exactly;
- consequence subject must actually be the declared actor/target/participant;
- only pre-existing `fields` rows with `mode='simulated'` may be changed;
- new state fields are not created implicitly;
- canonical/static/derived truth fails closed;
- field authority/source metadata is preserved;
- success emits `represented_consequence_applied` causally linked to the source completion event;
- consequence evidence is not learning evidence;
- application is savepoint-atomic and retry-idempotent.

Supported immediate operations:
`add`, `multiply`, `set`, `clamp_min`, `clamp_max`.

Skill score, IQ, supporting Attributes, performance quality, model prose, or generic capability never independently authorizes consequence mutation.

## Field Medicine Stabilization Consequence Consumer v1

Represented task registry revision:
`represented-skill-tasks-v1.5`.

Task:
`field_medicine_stabilize_for_evacuation_v1`

Action:
`stabilize`

Application:
`field_medicine.stabilize_for_evacuation`

Required represented contract:
- exact session object definition `represented_task:field_medicine_stabilization_session_v1`;
- target capabilities `stabilize`, `field_medical_context`, `evacuation_or_handoff_needed`;
- exactly one distinct casualty character participant;
- casualty colocated with actor;
- casualty already has numeric `medical.deterioration_risk` in 0..100 as pre-existing `simulated` state;
- explicit local or carried represented resource exposes `field_medical_supplies`.

Authorized V1 consequence only:
`medical.deterioration_risk` reduction.

The runtime resolves Field Medicine capability, persists immutable application evidence, then after the source completion event exists calls the generic consequence foundation to mutate only the authorized casualty participant field and emit causal consequence evidence.

Darian's current Field Medicine `75 / A` resolves the bounded `solid` exemplar class; ephemeral tests prove example `medical.deterioration_risk` `60 -> 40`. That is test evidence only, not a production casualty event.

Hard non-goals:
- no injury/wound taxonomy;
- no bleeding model;
- no diagnosis state creation;
- no definitive treatment state;
- no death/incapacity simulation;
- no automatic casualty-state creation;
- no medical-resource depletion/durability;
- no real-world medical advice surface;
- no Field Medicine XP from application/consequence evidence;
- no synthetic production casualty/session/supply fixture for proof.

## Controlled H2H state

One generic action remains authoritative: `spar`.

Exact represented session selects the current H2H application:
- `h2h_controlled_striking_spar_v1` -> `engage_unarmed_striking` -> `scored_contact_only`;
- `h2h_controlled_grapple_spar_v1` -> `control_unarmed_grapple` -> `scored_positional_control_only`.

Both require exact represented object target plus one distinct colocated character participant with explicit `controlled_sparring_consent`. Skill/performance scoring is separate from authorization. Neither path mutates injury, incapacity, persistent restraint, or participant state and neither authorizes hostile/non-consensual use.

Do not convert controlled sparring into a casualty producer merely to exercise medical or consequence systems.

## Evidence boundary

Runtime application and consequence evidence are not learning evidence and do not automatically award XP.

Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival and Field Medicine definitions do not activate XP by themselves.

Field Medicine stabilization v1 intentionally adds no IQ/medical-knowledge modifier contract. Parent Field Medicine Skill remains the bounded learned-capability authority for this exemplar while consequence authorization is separately deterministic.

## Next canonical direction

**Casualty State Origin & Lifecycle Contract v1 — REVIEW NEXT / not yet implemented.**

The stabilization consumer deliberately requires pre-existing simulated `medical.deterioration_risk`. The next missing seam is explicit ownership of how represented casualty state is created/initialized, which event or domain authority may create it, and how that state later resolves or clears.

Preserve:
- no casualty state inferred from model prose, Skill score, generic combat output, or ordinary event text;
- no automatic injury state from controlled H2H;
- no giant Injury Engine as the default solution;
- one bounded origin/lifecycle exemplar before any batch expansion;
- exact source event/state ownership and deterministic initialization;
- pre-existing simulated-state protection for consumers;
- application/consequence evidence != learning evidence;
- no synthetic production casualty merely for proof.

Keep Weapons separate until its exact resource/safety/target/consequence contract is reconciled. Weapons lethality is a distinct structural question.

## Exact resume point

**Field Medicine Stabilization Consequence Consumer v1 is complete through PR #140 final tested head `512f588df3e1b8256f61958a9336e5c0d3b8d17a`, merge `2c5f7602dc6263caa74658ae2fadd65aa4857124`, CI #868 / run `31881576876` with 472 passing tests and fresh-DB init/status, and Deploy #215 / run `31881627886` SUCCESS. The first real consequence consumer now proves exact represented stabilization task + one colocated casualty participant + explicit field-medical-supply resource -> bounded mutation of only pre-existing simulated `medical.deterioration_risk` -> causal consequence event, with no diagnosis, definitive treatment, resource depletion, XP, or fabricated production casualty. Review casualty-state origin/lifecycle authority next before expanding medical consequence semantics.**
