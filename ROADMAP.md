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

Latest runtime deployment: **Deploy #216 / run `31883480633` SUCCESS**, Casualty State Origin & Lifecycle Contract v1, PR #142 merge `47caf1851934a45158dc1840e9a57ff3d5549c2f`.

Final tested PR head: `f9a6eaf3e8347c34e5b9201ddf910e39eff1e149`.

Validation:
- **CI #872 / run `31883433021` SUCCESS**;
- full suite: **480 passed**;
- fresh DB `sandboxctl init` succeeded;
- fresh DB `sandboxctl status` healthy;
- schema remains v5.

Verified production readback after Deploy #216:
- service active/healthy; production `sandboxctl init` succeeded; schema v5;
- autonomy enabled, normal mode, 1x, retry `null`, with a pending action;
- cognition primary binding remained Gemini `gemini-3.1-flash-lite`; Groq fallback `qwen/qwen3.6-27b` remained healthy;
- Telegram bot/API/owner/allowed-user configuration remained healthy;
- live sim time advanced naturally to `2025-05-06T09:40:00+00:00`;
- Darian was naturally `move`ing in the Living Room at readback;
- no production casualty entity/state/lifecycle event/action was fabricated or forced for proof.

Exact casualty lifecycle create/clear semantics are proven by CI and ephemeral fixtures. Production deployment proves the new module loads safely without disturbing the live runtime. Do not overstate deployment as proof of a live casualty lifecycle event.

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

1. Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
2. Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
3. Cognition Capability Awareness v1 — PR #124 / Deploy #206
4. Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
5. Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
6. Training Movement Contract Normalization v1 — PR #129 / Deploy #209
7. Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
8. Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
9. Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
10. Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213
11. Represented Consequence State Foundation v1 — PR #138 / Deploy #214
12. Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215
13. **Casualty State Origin & Lifecycle Contract v1 — PR #142 / Deploy #216.**

## Represented consequence / Field Medicine state

### Consequence foundation

`validated represented task -> deterministic consequence authorization -> bounded simulated-state mutation -> causal event evidence`

The generic consequence foundation mutates only pre-existing simulated fields and cannot create state implicitly. Skill score, IQ, performance quality, model prose, or generic capability cannot independently authorize consequence mutation.

### Field Medicine stabilization consumer

Task: `field_medicine_stabilize_for_evacuation_v1`
Action: `stabilize`
Application: `field_medicine.stabilize_for_evacuation`

It requires one distinct colocated casualty participant with pre-existing simulated `medical.deterioration_risk`, plus explicit represented `field_medical_supplies`. V1 consequence scope remains only deterioration-risk reduction. No diagnosis, definitive treatment, resource depletion, or Field Medicine XP is implied.

## Casualty State Origin & Lifecycle Contract v1 — complete

Implementation: `src/observer_sandbox/casualty_state_lifecycle.py`.
Design note: `docs/CASUALTY_STATE_ORIGIN_LIFECYCLE_V1.md`.

This slice owns only the lifecycle of `medical.deterioration_risk` and composes existing schema-v5 primitives. No new table/schema migration was added.

### Origin

`initialize_casualty_state(...)` may create the field only when:
- the subject is an existing represented character;
- an explicit source event already exists;
- that exact source event binds the subject in `event_participants` with role `casualty`;
- origin kind is one of the finite V1 kinds;
- risk is numeric within `0..100`;
- the field does not already exist.

Finite V1 origin kinds:
- `represented_domain_consequence`
- `represented_environmental_hazard`
- `represented_accident`

Successful origin creates exactly:
- field: `medical.deterioration_risk`
- mode: `simulated`
- authority: `casualty_state_runtime`
- source: `casualty-state-origin-lifecycle-v1`

It emits `casualty_state_initialized` causally linked to the source event, with explicit create state-change evidence and `learning_evidence: false`.

No casualty state may be inferred from model prose, event wording, Skill score, generic combat output, or generic capability.

### Clear / lifecycle end

`clear_casualty_state(...)` requires a separate explicit source event binding the same character as role `casualty`, a finite V1 resolution kind, and an existing deterioration field owned by this exact lifecycle authority/source.

Finite resolution kinds:
- `evacuated_or_handed_off`
- `casualty_context_resolved`

Success deletes only `medical.deterioration_risk` and emits `casualty_state_cleared` causally linked to the resolution source event.

Important boundary: `medical.deterioration_risk == 0` does **not** auto-clear casualty state. Zero risk does not prove healing or definitive treatment; explicit handoff/context resolution is still required.

Origin and clear are savepoint-atomic and retry-idempotent. The lifecycle API cannot overwrite a pre-existing field and cannot clear state owned by another authority/source.

### Explicit non-goals

No Injury Engine, wound/bleeding taxonomy, diagnosis state, definitive-treatment state, death/incapacity state, automatic deterioration/recovery, automatic H2H casualty generation, Weapons lethality, medical-resource depletion, real-world medical advice, or automatic XP was added.

## Controlled H2H boundary

Current controlled striking/grappling remain scored-only and explicitly non-injurious at the persistent-state layer. Do not turn controlled sparring into a casualty producer merely to exercise the lifecycle API.

## Next development sequence

1. **First Real Casualty-State Producer — REVIEW NEXT / not yet implemented.**
2. Reconcile current represented action/event/domain contracts and select the smallest legitimate producer that can emit a deterministic source event and invoke `initialize_casualty_state(...)`.
3. Prefer a bounded represented accident/environmental-hazard producer if a current reusable domain contract supports it; do not invent a giant hazard/injury subsystem merely for a demo.
4. Field Medicine assessment should observe/interpret casualty state, not manufacture the casualty state it is assessing.
5. Keep controlled H2H non-casualty-producing unless a future explicitly authorized structural change says otherwise.
6. Keep Weapons separate: weapon availability, target/context, safety, and harmful consequence semantics remain a distinct high-risk review.
7. Do not seed a production casualty or force a live event merely to prove the producer.
8. Batch follow-on producers only after one bounded producer invariant is proven.

## Deferred boundaries

No hostile/non-consensual Combat Engine, full Injury Engine, Weapons lethality system, broad casualty simulator, bleeding/wound taxonomy, definitive-treatment engine, universal active-modifier evaluator, full Knowledge Engine, second competency score, economy/jobs/quests, deep crafting, or synthetic production actor/casualty fixtures as side effects of the next slice.

## Exact resume point

**Casualty State Origin & Lifecycle Contract v1 is complete through PR #142 final tested head `f9a6eaf3e8347c34e5b9201ddf910e39eff1e149`, merge `47caf1851934a45158dc1840e9a57ff3d5549c2f`, CI #872 / run `31883433021` with 480 passing tests plus fresh-DB init/status, and Deploy #216 / run `31883480633` SUCCESS. The runtime now has a deterministic typed owner for explicit source-event casualty binding -> creation of only simulated `medical.deterioration_risk` -> causal lifecycle evidence, plus separate explicit handoff/context-resolution -> lifecycle clear. Risk zero does not auto-clear, no healing is asserted, and no live casualty was fabricated. Review the first legitimate real casualty-state producer next.**
