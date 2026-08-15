# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Current Creator instruction, current canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #218 / run `31884823120` SUCCESS**, Field Medicine Assessment Read-Only Runtime v1, PR #146 merge `14274e409b36242eef376356f025d11749819e0f`.

Final tested PR head: `34708ef13076640e71ff5727f5444a2da3468ab9`.

Validation:
- **CI #883 / run `31884762399` SUCCESS**;
- full suite: **494 passed in 36.93s**;
- fresh DB `sandboxctl init` succeeded;
- fresh DB `sandboxctl status` healthy;
- schema remains v5;
- represented-task, Skill, Strength, eating, and nutrition acceptance gates all passed.

Verified production readback after Deploy #218:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, 1x, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time advanced naturally to `2025-05-06T10:10:00+00:00`;
- Darian was naturally `shower`ing in the Master Bathroom;
- no production casualty, accident, assessment session/action, or stabilization was fabricated or forced for proof.

Exact assessment semantics are CI/ephemeral-fixture evidence. Production deployment proves safe install/init/service continuity only.

Production parent Skills remain authoritative:
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

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. Runtime application/consequence/lifecycle evidence is not automatically learning evidence.

## Completed recent execution chain

1. Represented Consequence State Foundation v1 — PR #138 / Deploy #214
2. Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215
3. Casualty State Origin & Lifecycle Contract v1 — PR #142 / Deploy #216
4. Represented Accident Casualty Producer v1 — PR #144 / Deploy #217
5. **Field Medicine Assessment Read-Only Runtime v1 — PR #146 / Deploy #218.**

## Current casualty flow

### 1. Typed casualty origin

`record_represented_accident_casualty(...)` currently supports exactly one accident kind: `represented_fall`.

Finite abstract initialization classes:
- `low -> 25`
- `moderate -> 50`
- `high -> 75`

Canonical path:
`typed represented fall -> represented_accident_occurred with casualty role -> initialize_casualty_state(...) -> simulated medical.deterioration_risk`

The producer requires stable incident identity, exact represented casualty and location, explicit sim time, finite accident/risk classes, and uses an atomic savepoint. It does not accept free-form accident prose or create wounds, diagnoses, incapacity, death, or treatment state.

### 2. Read-only Field Medicine assessment

Task: `field_medicine_assess_field_casualty_v1`
Application: `field_medicine.assess_field_casualty`
Action: shared `assess`
Exact target definition: `represented_task:field_medicine_casualty_assessment_session_v1`

Requirements:
- exact assessment-session target;
- one distinct represented casualty participant;
- actor/casualty colocation;
- existing numeric simulated `medical.deterioration_risk` in `0..100`.

The runtime reads existing deterioration state and maps it only to an abstract pressure band:
- `0 -> none`
- `>0..33 -> low`
- `>33..66 -> moderate`
- `>66..100 -> high`

It emits represented Skill application evidence only. It cannot create/mutate casualty state, diagnose, treat, settle a consequence, or award Field Medicine XP. Darian's current Field Medicine 75/A maps to `solid` assessment effectiveness.

`assess` is reusable vocabulary rather than domain identity. Exact represented target definition selects the consumer:
- tactical assessment target -> Tactical Planning;
- Field Medicine assessment target -> Field Medicine;
- unknown `assess` target -> fail closed.

Ordinary actor physiology still progresses normally during actions. `read_only` is scoped to the casualty medical domain.

### 3. Bounded stabilization consequence

Task: `field_medicine_stabilize_for_evacuation_v1`
Action: `stabilize`

Requires one distinct colocated casualty with pre-existing simulated deterioration state plus explicit represented `field_medical_supplies`. It can reduce only `medical.deterioration_risk` through the generic represented consequence foundation. Darian's current 75/A Field Medicine maps to `solid`, reducing risk by 20 points in v1.

No diagnosis, definitive treatment, medical-supply depletion, or XP is implied.

### 4. Casualty lifecycle end

`clear_casualty_state(...)` already exists and only clears lifecycle-owned deterioration state after a separate explicit casualty-bound source event with resolution kind:
- `evacuated_or_handed_off`
- `casualty_context_resolved`

Risk reaching zero does not auto-clear and does not assert healing.

## Explicit boundaries

No Injury Engine, broad Hazard Engine, wounds/bleeding taxonomy, diagnosis engine, definitive-treatment graph, death/incapacity model, automatic deterioration/recovery, autonomous random accidents, Weapons lethality, controlled-H2H injury generation, medical-resource depletion, automatic Field Medicine XP, or synthetic production casualty fixtures.

## Next development sequence

1. **Represented Casualty Handoff / Lifecycle-End Consumer v1 — REVIEW NEXT / not yet implemented.**
2. Reconcile the lifecycle clear API and current event/world primitives.
3. Select the smallest typed represented handoff/context-resolution producer that emits an explicit source event binding the casualty and invokes `clear_casualty_state(...)`.
4. Handoff/context resolution must not imply healing, diagnosis resolution, or definitive treatment.
5. Do not clear merely because deterioration risk reaches zero.
6. Keep lifecycle/application/consequence evidence separate from learning evidence; no automatic XP.
7. Do not create/force a production casualty merely for validation.

## Deferred boundaries

No hostile/non-consensual Combat Engine, Weapons lethality system, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, automatic random-accident scheduler, universal active-modifier evaluator, full Knowledge Engine, second competency score, economy/jobs/quests, or synthetic production actor/casualty fixtures as side effects of the next slice.

## Exact resume point

**Field Medicine Assessment Read-Only Runtime v1 is complete through PR #146 final tested head `34708ef13076640e71ff5727f5444a2da3468ab9`, merge `14274e409b36242eef376356f025d11749819e0f`, CI #883 / run `31884762399` with 494 passing tests plus fresh-DB init/status and all relevant acceptance gates green, and Deploy #218 / run `31884823120` SUCCESS. The casualty stack now supports typed represented-fall origin -> lifecycle-owned simulated deterioration state -> exact-target read-only Field Medicine assessment -> existing bounded stabilization consequence; shared `assess` dispatch is target-definition-authoritative and unknown targets fail closed. No live casualty or assessment was fabricated. Review a real represented handoff/lifecycle-end producer next.**
