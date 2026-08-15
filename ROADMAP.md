# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Runtime/code/config plus verified live production are authoritative over remembered chat.
- AI proposes structured cognition; deterministic engines validate and mutate.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are exemplars, never reusable-engine identity.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #213 / run `31880471063` SUCCESS**, Controlled H2H Interaction Pattern Generalization v1, PR #136 merge `be34324e87e68c54c5d6f80f9448bf5f24381172`.

Verified post-deploy production evidence:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, 1x, retry `null`;
- a pending autonomous action exists;
- cognition binding remained `gemini-3.1-flash-lite`; Groq fallback bootstrap remained healthy;
- Telegram API connectivity remained healthy;
- production `sandboxctl init` succeeded with the generalized controlled-H2H action vocabulary/config active;
- live state continued naturally at `train` in the Home Gym at sim time `2025-05-06T08:05:00+00:00`;
- no live `spar` action was forced for validation;
- no production sparring/grappling partner or represented session fixture was fabricated solely for proof.

Exact grappling-session runtime behavior is proven by full CI, fresh-DB `init`/`status`, and focused ephemeral-fixture tests. Production deployment/init proves the generalized code/config path loaded successfully; production does not contain a fabricated grappling session merely to permit a live action proof. Keep those evidence claims distinct.

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

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. Legacy RAPS skill-like fields remain compatibility/provenance only and are not independent Skill truth.

## Completed Skill / cognition / represented-task chain

1. H2H Skill Progression v1 — PR #104 / Deploy #196
2. Tactical Planning Skill Progression — PR #106 / Deploy #197
3. Skill Evidence Semantics / Technology practice — PR #108 / Deploy #198
4. Skill Definition & Capability Framework — PR #110
5. Skill Creation Format / Technology definition — PR #111 / Deploy #199
6. Skill Application Requirements — PR #113 / Deploy #200
7. Technology Capability Resolution — PR #115 / Deploy #201
8. Actor-backed Skill Capability Adapter — PR #117 / Deploy #202
9. Represented Skill Task Contract v1 — PR #119 / Deploy #203
10. Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
11. Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
12. Cognition Capability Awareness v1 — PR #124 / Deploy #206
13. Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
14. Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
15. Sanitized Autonomy Error Readback — PR #127, corrected by PR #128
16. Training Movement Contract Normalization v1 — PR #129 / Deploy #209
17. Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
18. Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
19. Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212
20. Controlled H2H Interaction Pattern Generalization v1 — PR #136 / Deploy #213.

Canonical execution stack now includes:
- Skill definition/application/capability + actor adapter;
- represented Skill task registry + exact instance resolver;
- cognition capability-awareness projection;
- bounded cognitive/performance modifier resolver;
- generic low-risk represented-Skill runtime reuse;
- generalized controlled-H2H multi-actor authorization/runtime path;
- immutable application-evidence path separate from learning evidence.

## Current six gameplay-grade umbrella Skills

Applications:
- H2H: `engage_unarmed_striking`, `control_unarmed_grapple`
- Weapons: `employ_familiar_melee_weapon`, `employ_familiar_ranged_weapon`
- Survival: `navigate_field_environment`, `establish_field_sustainment`
- Tactical Planning: `assess_tactical_situation`, `plan_tactical_maneuver`
- Technology: `diagnose_known_system_fault`
- Field Medicine: `assess_field_casualty`, `stabilize_for_evacuation`.

## Represented Skill runtime state

### Low-risk represented pattern — complete and batched

Technology diagnostic and Tactical assessment established the initial `required_resource_mode: any|none` exemplars. PR #133 then applied the proven pattern in one batch to Tactical maneuver planning plus both Survival applications. These remain simulation/application evidence only with no movement execution, shelter mutation, represented-resource consumption, consequence-state mutation, or automatic XP.

### Controlled H2H interaction pattern — complete for current H2H application surface

PR #134 proved the first bounded multi-actor authorization invariant with controlled striking. PR #136 generalized that exemplar instead of creating a second bespoke engine.

Shared action: `spar`.

Exact represented session target selects the H2H application:
- striking task `h2h_controlled_striking_spar_v1` -> `hand_to_hand_combat.engage_unarmed_striking` -> consequence `scored_contact_only`;
- grappling task `h2h_controlled_grapple_spar_v1` -> `hand_to_hand_combat.control_unarmed_grapple` -> consequence `scored_positional_control_only`.

Shared deterministic interaction boundaries:
- represented session remains the exact object target;
- exactly one opponent is carried in `Action.participants`;
- opponent must be a distinct represented character;
- opponent must be colocated;
- opponent must explicitly expose `controlled_sparring_consent`;
- authorization is deterministic and separate from Skill/performance scoring;
- target definition selects exactly one authorized controlled-H2H task/application;
- no hostile/non-consensual use is authorized;
- no injury, incapacity, persistent restraint, or participant target-state mutation occurs;
- no production partner/session fixture is seeded solely for validation.

H2H Skill score remains parent learned-capability authority. Striking and grappling each have exact bounded performance contracts using Reflexes + Agility + Focus only. IQ is intentionally absent and legacy `raps_pa.combat_skill` remains excluded.

## Cognition and IQ boundary

Cognition receives a read-only semantic projection of actor Skill state plus canonical Skill definitions/applications, behavioral anchors, supported challenges, context/resource expectations, and explicit limits.

IQ/supporting Attributes are task-specific performance context only when a declared modifier contract names them. They cannot create Knowledge, proficiency, missing resources/context, consent, authorization, supported challenge capability, restraint authority, injury state, or consequences.

## Subskill policy

Current application families are the initial subskill-like gameplay surface, not independently scored child Skills.

Do not split parent scores into invented child values. Promote a true child Skill only when:
1. the task family is meaningfully separable;
2. legitimate learning evidence can distinguish it;
3. progression/retention can be independently owned;
4. parent/child aggregation and migration semantics are explicit.

`component_skills` remains empty for the current six definitions.

## Learning-evidence state

Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation evidence;
- Technology — `systems_diagnostic_practice`.

Controlled striking/grappling application evidence remains immutable application evidence only and does not automatically become H2H XP.

Weapons, Survival and Field Medicine have semantic definitions but no active progression producer. Do not invent progression merely because represented gameplay exists.

## Training movement operational correction

PR #129 remains the production contract:
- authored method + no movement subcatalog -> auxiliary movement labels canonicalize to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound target -> fail closed.

## Next development sequence

1. **Represented Consequence State Foundation v1 — PROPOSED NEXT / not yet implemented.**
2. First inspect current state/effect/event primitives and define the smallest generic boundary between a validated represented-task outcome and a deterministic consequence/state transition.
3. Do not build a giant Combat Engine or full Injury Engine. The foundation should be domain-neutral enough to support later bounded consumers while remaining explicit about target, state field/effect, duration/lifecycle where relevant, validation, mutation ownership, and emitted evidence/events.
4. Preserve the distinction between performance outcome and consequence. High Skill or a strong outcome must not independently authorize or manufacture a state mutation.
5. Prefer one bounded, low-complexity exemplar if a genuinely new state-transition invariant is required; batch structurally equivalent consequence consumers only after that invariant is proven.
6. A likely later sequence is consequence-state foundation -> Field Medicine consequence consumer -> Weapons safety/resource exemplar, but each remains subject to exact live-contract inspection before implementation.
7. Keep application evidence separate from learning evidence and do not auto-award XP.
8. Do not add independently scored child Skills or fabricate production characters/actions for proof.

## Deferred boundaries

No hostile/non-consensual combat engine, full injury engine, persistent restraint/incapacity system, Weapons lethality system, Field Medicine casualty-treatment mutation, full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior rewrite, deep crafting, detailed endocrine expansion, second production character solely for testing, or Tahoe exterior traversal as side effects of the next foundation slice.

## Exact resume point

**Controlled H2H Interaction Pattern Generalization v1 is complete through PR #136 merge `be34324e87e68c54c5d6f80f9448bf5f24381172` / Deploy #213 run `31880471063` SUCCESS. Both current H2H applications now reuse one exact-target-driven `spar` interaction path with explicit participant consent/colocation and application-specific bounded outcomes, without injury/restraint mutation or automatic XP. The proposed next architectural seam is Represented Consequence State Foundation v1: inspect existing state/effect/event primitives, then design the smallest generic validated outcome -> consequence/state-change boundary before adding Field Medicine or Weapons consequence consumers.**
