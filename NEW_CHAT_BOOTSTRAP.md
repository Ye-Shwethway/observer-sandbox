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

Latest runtime deployment: **Deploy #213 / run `31880471063` SUCCESS**, Controlled H2H Interaction Pattern Generalization v1, PR #136 merge `be34324e87e68c54c5d6f80f9448bf5f24381172`.

Post-deploy evidence:
- service active/healthy, schema v5;
- autonomy enabled in normal mode at 1x with retry `null` and a pending action;
- cognition binding remained `gemini-3.1-flash-lite`; Groq fallback bootstrap remained healthy;
- Telegram API connectivity remained healthy;
- production initialization completed successfully with generalized controlled-H2H code/config active;
- live state continued naturally at `train` in the Home Gym at sim time `2025-05-06T08:05:00+00:00`;
- no live `spar` action was forced for proof;
- no production striking/grappling partner or represented session fixture was fabricated solely for validation.

Exact grappling behavior is proven by full CI, fresh-DB `init`/`status`, and focused ephemeral-fixture tests. Production deploy/init proves the generalized path loaded successfully; do not overstate this as a live grappling action proof.

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

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. Legacy RAPS skill-like fields are compatibility/provenance only.

Current application families are the subskill-like gameplay surface. **Do not create independently scored child Skills yet.**

## Completed current execution chain

Recent Skill/runtime line:
- Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
- Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
- Cognition Capability Awareness v1 — PR #124 / Deploy #206
- Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
- Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
- sanitized autonomy-error readback — PR #127, corrected by PR #128
- Training Movement Contract Normalization v1 — PR #129 / Deploy #209
- Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
- Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
- Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
- Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213.

## Represented Skill runtime state

### Low-risk represented pattern — complete and batched

Technology diagnostic and Tactical assessment established the initial represented-task exemplars. PR #133 applied that pattern to Tactical maneuver planning and both Survival applications without movement execution, shelter/resource mutation, consequence state, or automatic XP.

### Controlled H2H interaction pattern — current H2H application surface complete

PR #134 proved explicit multi-actor authorization with controlled striking. PR #136 generalized the runtime rather than adding a separate grappling engine.

One generic action remains authoritative: `spar`.

Exact represented session definition selects the application:
- `h2h_controlled_striking_spar_v1` -> `engage_unarmed_striking` -> `scored_contact_only`;
- `h2h_controlled_grapple_spar_v1` -> `control_unarmed_grapple` -> `scored_positional_control_only`.

Both reuse:
- exact represented object target;
- one distinct character participant through `Action.participants`;
- colocation;
- explicit `controlled_sparring_consent`;
- deterministic authorization separate from Skill/performance;
- parent H2H Skill authority;
- bounded task-specific performance modifiers;
- immutable application evidence separate from learning evidence.

Neither path authorizes hostile/non-consensual use or mutates injury, incapacity, persistent restraint, or participant target state. Production still receives no fabricated partner/session fixture.

H2H striking and grappling modifier contracts both use Reflexes + Agility + Focus only. IQ is intentionally absent and legacy `raps_pa.combat_skill` remains excluded.

## Cognition / IQ state

Cognition receives read-only semantic capability awareness: definition scope/exclusions, application families, behavioral anchors, challenge/context/resource boundaries, and relevant performance context.

IQ is not Skill or Knowledge. It can only affect an explicit task-specific modifier contract after deterministic Skill/task feasibility is established. It cannot create consent, authorization, resources, missing context, knowledge, restraint authority, injury state, or consequences.

## Evidence boundary

Runtime application completion may emit immutable `skill_application_evidence`. That is **not learning evidence** and does not automatically award XP.

Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Controlled striking and grappling application evidence do not become H2H XP automatically. Weapons, Survival and Field Medicine definitions do not activate XP by themselves.

## Training movement recovery contract

PR #129 remains active:
- authored training method with no movement subcatalog -> auxiliary `training_movements` canonicalizes to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound target -> fail closed.

## Next canonical direction

**Represented Consequence State Foundation v1 is the proposed next architectural slice; it is not yet implemented.**

Before implementation, inspect current state/effect/event primitives and define the smallest generic seam between a validated represented-task outcome and an authorized deterministic consequence/state transition.

Do not jump to a full Combat Engine or Injury Engine. Preserve:
- performance outcome != consequence authorization;
- exact target/context/participant/resource authority;
- deterministic mutation ownership;
- explicit bounded state/effect lifecycle where applicable;
- consequence events/evidence tied to the action that caused them;
- Skill score and supporting Attributes cannot independently authorize state mutation;
- application evidence != learning evidence;
- no invented child Skill scores;
- no synthetic production character/action used merely for proof.

A likely later sequence is consequence-state foundation -> Field Medicine consequence consumer -> Weapons safety/resource exemplar, but each must be re-checked against current canonical contracts before implementation.

## Exact resume point

**Controlled H2H Interaction Pattern Generalization v1 is complete through PR #136 merge `be34324e87e68c54c5d6f80f9448bf5f24381172` / Deploy #213 run `31880471063` SUCCESS. Both current H2H applications now reuse one exact-target-driven `spar` path with explicit participant consent/colocation and application-specific bounded outcomes, with no injury/restraint mutation or automatic XP. Reconcile current repo/production, then inspect existing state/effect/event primitives and design the minimum Represented Consequence State Foundation v1 before adding Field Medicine or Weapons consequence consumers.**
