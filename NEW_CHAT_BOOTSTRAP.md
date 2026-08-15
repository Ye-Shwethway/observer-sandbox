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

Default workflow:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #216 / run `31883480633` SUCCESS**, Casualty State Origin & Lifecycle Contract v1, PR #142 merge `47caf1851934a45158dc1840e9a57ff3d5549c2f`.

Final tested PR head: `f9a6eaf3e8347c34e5b9201ddf910e39eff1e149`.

Validation:
- **CI #872 / run `31883433021` SUCCESS**;
- **480 tests passed**;
- fresh DB `init` and `status` succeeded;
- schema remains v5.

Production readback after Deploy #216:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, 1x, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram connected with owner/allowed-user configuration present;
- sim time naturally advanced to `2025-05-06T09:40:00+00:00`;
- Darian was naturally `move`ing in the Living Room;
- no live casualty entity/state/lifecycle event/action was created or forced for proof.

Exact casualty-state origin/clear behavior is CI/ephemeral-fixture evidence. Production deployment proves the module loads safely; it is not evidence that a real live casualty lifecycle occurred.

Production parent Skill values remain:
- H2H 90/S
- Weapons 87/A
- Survival 85/A
- Tactical Planning 92/S
- Technology 82/A
- Field Medicine 75/A.

## Recent completed chain

- Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
- Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
- Cognition Capability Awareness v1 — PR #124 / Deploy #206
- Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
- Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
- Training Movement Contract Normalization v1 — PR #129 / Deploy #209
- Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
- Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
- Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
- Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213
- Represented Consequence State Foundation v1 — PR #138 / Deploy #214
- Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215
- **Casualty State Origin & Lifecycle Contract v1 — PR #142 / Deploy #216.**

## Current casualty/consequence architecture

Generic represented consequence mutation remains:
`validated represented task -> deterministic consequence authorization -> bounded pre-existing simulated-state mutation -> causal event evidence`.

Field Medicine stabilization remains the first real consequence consumer:
- task `field_medicine_stabilize_for_evacuation_v1`;
- action `stabilize`;
- one distinct colocated casualty participant;
- explicit represented `field_medical_supplies`;
- casualty already has simulated `medical.deterioration_risk`;
- authorized consequence only reduces that field;
- no diagnosis, definitive treatment, resource depletion, or XP.

## Casualty State Origin & Lifecycle Contract v1

Implementation: `src/observer_sandbox/casualty_state_lifecycle.py`.
Design note: `docs/CASUALTY_STATE_ORIGIN_LIFECYCLE_V1.md`.

The lifecycle contract owns only `medical.deterioration_risk` creation and lifecycle end. It uses existing schema-v5 `fields`, `events`, `event_participants`, causal links, and structured state-change evidence; no migration was added.

### Origin

`initialize_casualty_state(...)` requires:
- existing represented character;
- pre-existing explicit source event;
- exact source event participant binding with role `casualty`;
- finite origin kind;
- numeric risk `0..100`;
- deterioration field absent.

Finite origin kinds:
- `represented_domain_consequence`
- `represented_environmental_hazard`
- `represented_accident`

It creates only:
`medical.deterioration_risk`, mode `simulated`, authority `casualty_state_runtime`, source `casualty-state-origin-lifecycle-v1`.

Success emits `casualty_state_initialized` causally linked to the source event. Model prose, event wording, Skill score, combat narration, and generic capabilities cannot create casualty state.

### Clear

`clear_casualty_state(...)` requires a separate explicit source event binding the same character as `casualty`, a finite resolution kind, and state owned by this lifecycle contract.

Finite resolution kinds:
- `evacuated_or_handed_off`
- `casualty_context_resolved`

Success removes only `medical.deterioration_risk` and emits `casualty_state_cleared` causally linked to the resolution event.

`medical.deterioration_risk == 0` does **not** auto-clear. Zero deterioration risk does not assert healing, diagnosis resolution, or definitive treatment.

Origin and clear are savepoint-atomic and retry-idempotent. The API neither overwrites another authority's field nor clears state owned elsewhere. Lifecycle evidence is `learning_evidence: false`.

## Controlled H2H boundary

Controlled striking/grappling remain scored-only and do not create persistent injury/casualty state. Do not convert controlled sparring into a casualty producer merely to exercise this API.

## Next canonical direction

**First Real Casualty-State Producer — REVIEW NEXT / not yet implemented.**

Reconcile current represented action/event/domain contracts and choose the smallest legitimate producer that can emit a deterministic source event with explicit `casualty` participant binding and then invoke `initialize_casualty_state(...)`.

Preserve:
- no casualty state inferred from prose or generic outcomes;
- Field Medicine assessment observes state rather than manufacturing it;
- controlled H2H remains non-casualty-producing;
- Weapons remains a separate high-risk resource/target/safety/consequence review;
- prefer a bounded represented accident/environmental-hazard exemplar if an existing contract genuinely supports it;
- do not create a giant Injury/Hazard Engine;
- no production casualty fixture or forced event solely for validation;
- lifecycle/application/consequence evidence != learning evidence.

## Exact resume point

**Casualty State Origin & Lifecycle Contract v1 is complete through PR #142 head `f9a6eaf3e8347c34e5b9201ddf910e39eff1e149`, merge `47caf1851934a45158dc1840e9a57ff3d5549c2f`, CI #872 / run `31883433021` with 480 passing tests plus fresh-DB init/status, and Deploy #216 / run `31883480633` SUCCESS. The typed lifecycle authority now permits only explicit causal source-event + casualty-role binding to create simulated `medical.deterioration_risk`, and only a separate explicit handoff/context-resolution event may clear lifecycle-owned state. Risk zero never auto-clears and no live casualty was fabricated. Review the first legitimate real casualty-state producer next.**
