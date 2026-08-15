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

Latest runtime deployment: **Deploy #218 / run `31884823120` SUCCESS**, Field Medicine Assessment Read-Only Runtime v1, PR #146 merge `14274e409b36242eef376356f025d11749819e0f`.

Final tested PR head: `34708ef13076640e71ff5727f5444a2da3468ab9`.

Validation:
- **CI #883 / run `31884762399` SUCCESS**;
- **494 tests passed in 36.93s**;
- fresh DB `init` and `status` succeeded;
- schema remains v5;
- all relevant represented-task, Skill, Strength, eating, and nutrition acceptance workflows passed.

Production readback after Deploy #218:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, 1x, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram token/API/owner/allowed-user configuration healthy;
- sim time naturally advanced to `2025-05-06T10:10:00+00:00`;
- Darian was naturally `shower`ing in the Master Bathroom;
- no live casualty, accident, assessment session, assessment action, or stabilization was created/forced for proof.

Exact Field Medicine assessment behavior is CI/ephemeral-fixture evidence. Production deployment proves safe loading and integration only; it is not evidence that a live medical assessment occurred.

Production parent Skill values remain:
- H2H 90/S
- Weapons 87/A
- Survival 85/A
- Tactical Planning 92/S
- Technology 82/A
- Field Medicine 75/A.

## Recent completed casualty / Skill chain

- Represented Consequence State Foundation v1 — PR #138 / Deploy #214
- Field Medicine Stabilization Consequence Consumer v1 — PR #140 / Deploy #215
- Casualty State Origin & Lifecycle Contract v1 — PR #142 / Deploy #216
- Represented Accident Casualty Producer v1 — PR #144 / Deploy #217
- **Field Medicine Assessment Read-Only Runtime v1 — PR #146 / Deploy #218.**

## Current casualty flow

The project now has one bounded end-to-end casualty path:

`typed represented fall -> casualty lifecycle state -> read-only Field Medicine assessment -> optional bounded stabilization consequence -> explicit lifecycle-end event required for clear`

### Origin

`record_represented_accident_casualty(...)` currently supports only `represented_fall` with finite abstract risk classes:
- low -> 25
- moderate -> 50
- high -> 75

It emits `represented_accident_occurred` with explicit participant role `casualty`, then atomically invokes the canonical lifecycle owner to create only simulated `medical.deterioration_risk`.

No free-form accident prose, wound diagnosis, incapacity, death, or autonomous random accident is authorized.

### Read-only Field Medicine assessment

Task: `field_medicine_assess_field_casualty_v1`
Application: `field_medicine.assess_field_casualty`
Action verb: shared generic `assess`
Target definition: `represented_task:field_medicine_casualty_assessment_session_v1`

Requirements:
- exact represented assessment-session target;
- exactly one distinct represented casualty participant;
- actor and casualty colocated;
- casualty already has numeric simulated `medical.deterioration_risk` in `0..100`.

The assessment reads the existing risk and reports an abstract pressure band only:
- 0 -> `none`
- >0..33 -> `low`
- >33..66 -> `moderate`
- >66..100 -> `high`

It creates application evidence but does not create/mutate casualty state, create diagnosis, perform treatment, settle a consequence, or award Field Medicine XP. Darian's current Field Medicine 75/A yields `solid` assessment effectiveness in the bounded v1 contract.

`assess` is intentionally shared vocabulary. Domain dispatch is by exact represented target definition, not the verb, target name, or prose. Tactical assessment still dispatches to Tactical Planning; the medical assessment target dispatches to Field Medicine; unknown `assess` target definitions fail closed.

Ordinary action physiology may still progress during an assessment. `read_only` means the Field Medicine assessment consumer does not mutate the casualty's medical state or infer diagnosis/treatment.

### Stabilization

Task: `field_medicine_stabilize_for_evacuation_v1`
Action: `stabilize`

Requires one distinct colocated casualty with pre-existing simulated deterioration state and explicit represented `field_medical_supplies`. The only authorized consequence is deterministic reduction of `medical.deterioration_risk`. Darian's current Field Medicine 75/A maps to `solid` and a v1 reduction of 20 points. No diagnosis, definitive treatment, supply depletion, or XP is implied.

### Lifecycle end

`clear_casualty_state(...)` already requires a separate explicit casualty-bound source event with resolution kind `evacuated_or_handed_off` or `casualty_context_resolved`. Risk reaching zero never auto-clears and never asserts healing.

## Hard boundaries

- no Injury Engine, wounds/bleeding taxonomy, diagnosis engine, definitive-treatment graph, death/incapacity model, or automatic deterioration/recovery;
- controlled H2H remains scored-only and non-casualty-producing;
- Weapons harm/lethality remains deferred;
- no autonomous random accidents;
- no medical-resource depletion;
- no automatic Field Medicine XP;
- no production casualty/session/action manufactured merely for proof.

## Next canonical direction

**Represented Casualty Handoff / Lifecycle-End Consumer v1 — REVIEW NEXT / not yet implemented.**

The lifecycle clear API exists, but there is no real represented domain producer yet for a legitimate `evacuated_or_handed_off` or `casualty_context_resolved` source event. Review the smallest typed handoff/context-resolution producer that can explicitly bind the casualty and invoke `clear_casualty_state(...)` without implying healing or building a treatment/evacuation engine.

Preserve:
- explicit represented casualty and causal source event;
- no clear merely because risk reaches zero;
- handoff/context resolution != healing or definitive treatment;
- no automatic XP;
- no synthetic production casualty for proof.

## Exact resume point

**Field Medicine Assessment Read-Only Runtime v1 is complete through PR #146 final tested head `34708ef13076640e71ff5727f5444a2da3468ab9`, merge `14274e409b36242eef376356f025d11749819e0f`, CI #883 / run `31884762399` with 494 passing tests plus fresh-DB init/status and all relevant acceptance gates green, and Deploy #218 / run `31884823120` SUCCESS. The casualty stack now supports a typed represented-fall origin -> lifecycle-owned simulated deterioration state -> exact-target read-only Field Medicine assessment -> existing bounded stabilization reduction, while shared `assess` dispatch is definition-bound and unknown assess targets fail closed. No live casualty or assessment was fabricated. Review the first real lifecycle-end/handoff producer next.**
