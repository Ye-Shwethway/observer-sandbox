# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Current Creator instruction, current repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #217 / run `31884052059` SUCCESS**, Represented Accident Casualty Producer v1, PR #144 merge `1068432c1933aa189f9ec4af5b7d33c86c54877d`.

Final tested PR head: `5c380474d4b92a091b9af09cf48e9954aaf4ac4b`.

Validation:
- **CI #876 / run `31884011651` SUCCESS**;
- full suite: **486 passed in 27.59s**;
- fresh DB `sandboxctl init` succeeded;
- fresh DB `sandboxctl status` healthy;
- schema remains v5.

Verified production readback after Deploy #217:
- service active/healthy; production `sandboxctl init` succeeded; schema v5;
- autonomy enabled, normal mode, 1x, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback remained healthy;
- Telegram bot/API/owner/allowed-user configuration remained healthy;
- live sim time advanced naturally to `2025-05-06T09:50:00+00:00`;
- Darian was naturally `idle` in Darian's Master Suite;
- no production accident/fall/casualty state/lifecycle event was fabricated or forced for proof.

Exact accident-producer semantics are proven by CI and ephemeral fixtures. Production deployment proves safe install/init/service continuity only.

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

1. Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
2. Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
3. Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213
4. Represented Consequence State Foundation v1 — PR #138 / Deploy #214
5. Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215
6. Casualty State Origin & Lifecycle Contract v1 — PR #142 / Deploy #216
7. **Represented Accident Casualty Producer v1 — PR #144 / Deploy #217.**

## Current casualty / consequence stack

### Represented consequence foundation

`validated represented task -> deterministic consequence authorization -> bounded pre-existing simulated-state mutation -> causal event evidence`

The generic consequence API cannot implicitly create state and cannot derive mutation authority from Skill score, IQ, prose, performance quality, or generic capability.

### Casualty lifecycle

Implementation: `src/observer_sandbox/casualty_state_lifecycle.py`.

Canonical origin:
`explicit source event + participant role casualty -> lifecycle-owned creation of simulated medical.deterioration_risk -> causal lifecycle event`.

Canonical clear:
`separate explicit casualty-bound handoff/context-resolution event -> lifecycle-owned deletion of medical.deterioration_risk`.

Risk zero never auto-clears and does not assert healing, diagnosis resolution, or definitive treatment.

### Field Medicine stabilization

Task: `field_medicine_stabilize_for_evacuation_v1`
Action: `stabilize`
Application: `field_medicine.stabilize_for_evacuation`

It requires one distinct colocated casualty with pre-existing simulated `medical.deterioration_risk` plus explicit represented `field_medical_supplies`. Authorized consequence scope remains deterioration-risk reduction only. No diagnosis, definitive treatment, resource depletion, or Field Medicine XP is implied.

## Represented Accident Casualty Producer v1 — complete

Implementation: `src/observer_sandbox/represented_accident_casualty.py`.
Design note: `docs/REPRESENTED_ACCIDENT_CASUALTY_PRODUCER_V1.md`.

This is the first legitimate real casualty-state producer.

Canonical path:

`typed represented accident -> represented_accident_occurred -> explicit casualty-role binding -> initialize_casualty_state(...) -> casualty_state_initialized`

V1 proves exactly one accident kind:
- `represented_fall`.

Finite abstract deterioration-risk classes:
- `low -> 25`
- `moderate -> 50`
- `high -> 75`

These are simulation pressure classes only and do not encode wounds, diagnoses, incapacity, death, or treatment advice.

`record_represented_accident_casualty(...)` requires:
- stable `incident_id`;
- existing represented character casualty;
- existing spatial location;
- casualty's current location exactly matches the declared accident location;
- explicit simulation time;
- finite accident kind;
- finite risk class.

No free-form accident narrative is accepted by the producer API.

The source event itself mutates no state and explicitly records no injury/diagnosis/incapacity creation. It binds the character with participant role `casualty`, then calls the canonical lifecycle owner to initialize the abstract deterioration state.

Source-event creation and lifecycle initialization share one SQLite savepoint. Failure rolls the source event back. Stable `incident_id` makes identical retries idempotent and conflicting reuse fails closed.

### Explicit non-goals

No autonomous random accidents, probability tables, universal Hazard Engine, Injury Engine, wound/bleeding taxonomy, diagnosis state, death/incapacity state, automatic deterioration/recovery, controlled-H2H casualty generation, Weapons lethality, Field Medicine XP, or production casualty fixture was added.

## Controlled H2H boundary

Controlled striking/grappling remain scored-only and non-casualty-producing. Do not retrofit persistent injury merely to exercise medical systems.

## Next development sequence

1. **Field Medicine Assessment Read-Only Runtime v1 — REVIEW NEXT / not yet implemented.**
2. Reconcile the existing `field_medicine.assess_field_casualty` application and current represented-task contracts.
3. Add the smallest represented assessment task/runtime that reads an explicitly represented casualty's existing `medical.deterioration_risk` without creating or mutating it.
4. Assessment output should be informational/application evidence only unless a separately defined consequence contract later authorizes mutation.
5. Do not turn assessment into a diagnosis engine or treatment graph.
6. Keep Field Medicine application evidence separate from learning evidence; no automatic XP.
7. Do not seed or force a production casualty solely for validation.
8. Batch structurally equivalent read-only assessment follow-ons only after one bounded exemplar is proven.

## Deferred boundaries

No hostile/non-consensual Combat Engine, Weapons lethality system, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, automatic random-accident scheduler, universal active-modifier evaluator, full Knowledge Engine, second competency score, economy/jobs/quests, or synthetic production actor/casualty fixtures as side effects of the next slice.

## Exact resume point

**Represented Accident Casualty Producer v1 is complete through PR #144 final tested head `5c380474d4b92a091b9af09cf48e9954aaf4ac4b`, merge `1068432c1933aa189f9ec4af5b7d33c86c54877d`, CI #876 / run `31884011651` with 486 passing tests plus fresh-DB init/status, and Deploy #217 / run `31884052059` SUCCESS. The first real casualty-state producer now proves typed `represented_fall` + stable incident identity + exact represented casualty/location + finite abstract risk class -> explicit source event with casualty role -> atomic canonical lifecycle initialization of only simulated `medical.deterioration_risk`, with no injury diagnosis, incapacity, XP, autonomous random accident, or fabricated production casualty. Review Field Medicine assessment as a read-only represented consumer next.**
