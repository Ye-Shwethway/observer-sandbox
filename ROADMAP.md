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

Latest runtime deployment: **Deploy #214 / run `31880931750` SUCCESS**, Represented Consequence State Foundation v1, PR #138 merge `ba662010cdf19b078eb6a82c54674250534fab99`.

Verified post-deploy production evidence:
- service active/healthy; schema remains v5;
- production `sandboxctl init` succeeded;
- autonomy enabled, normal mode, 1x, retry `null`, with a pending action;
- cognition binding remained `gemini-3.1-flash-lite`; Groq fallback bootstrap remained healthy;
- Telegram bot token/owner/allowed-user configuration remained present and Telegram API connectivity remained healthy;
- live state continued naturally to sim time `2025-05-06T08:35:00+00:00`;
- Darian was naturally `rest`ing in the Home Gym at readback;
- no represented consequence was forced in production;
- no production character/action/state fixture was fabricated solely for proof.

The foundation's exact mutation/idempotency/rollback behavior is proven by CI and ephemeral fresh-DB tests. Production deploy/init proves that the new runtime library loads safely. Keep those evidence claims distinct.

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
12. **Represented Consequence State Foundation v1 — PR #138 / Deploy #214.**

Canonical execution stack now includes:
- Skill definition/application/capability + actor adapter;
- represented Skill task registry + exact instance resolver;
- cognition capability-awareness projection;
- bounded cognitive/performance modifier resolver;
- low-risk represented-Skill runtime reuse;
- generalized controlled-H2H explicit multi-actor authorization/runtime path;
- immutable application-evidence path separate from learning evidence;
- domain-neutral represented consequence-state application foundation.

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

PR #138 / Deploy #214 implemented the minimum generic bridge:

`validated represented task -> deterministic consequence authorization -> bounded simulated-state mutation -> causal event evidence`

Implementation: `src/observer_sandbox/represented_consequence_state.py`.
Canonical design note: `docs/REPRESENTED_CONSEQUENCE_STATE_FOUNDATION_V1.md`.

V1 deliberately composes existing schema-v5 primitives rather than inventing a new subsystem:
- `fields` remains generic state storage;
- only pre-existing fields with `mode='simulated'` are mutable through this API;
- `action_instances` remains source-action authority;
- `events.state_changes_json`, `action_id`, `location_id`, `caused_by_event_id`, and `event_participants` remain consequence evidence/causality primitives;
- `active_modifiers` remains a future socket and is not activated globally by this slice.

A `ConsequenceAuthorization` must explicitly bind:
- consequence id;
- exact represented task id already persisted on the completed source action;
- subject id;
- subject relationship: `actor`, `target`, or `participant`;
- finite state mutation list.

Supported immediate operations reuse the established effect vocabulary:
`add`, `multiply`, `set`, `clamp_min`, `clamp_max`.

Hard boundaries:
- source action must already be completed and have its `action_completed` event;
- represented-task id must match exactly;
- subject must actually be the declared actor/target/participant;
- consequence application cannot create new state fields;
- canonical/static/derived fields fail closed;
- Skill score, IQ, performance quality, model prose, or generic capability cannot independently authorize mutation;
- field authority/source metadata are preserved; consequence provenance is carried by the event;
- successful application emits `represented_consequence_applied` causally linked to the source completion event;
- consequence evidence sets `learning_evidence: false` and awards no Skill XP;
- application is savepoint-atomic and idempotent per action/consequence/task/subject tuple.

CI #863 passed **465 tests** plus fresh DB `init` and `status` with schema v5.

## Cognition / evidence boundary

Cognition receives read-only semantic capability awareness. Supporting Attributes and IQ affect performance only through explicit task-specific contracts after deterministic feasibility. They cannot create Knowledge, proficiency, consent, resources, authorization, state fields, or consequences.

Runtime application/consequence evidence is not learning evidence. Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival, and Field Medicine definitions do not activate XP by themselves.

## Next development sequence

1. **First Real Represented Consequence Consumer — REVIEW NEXT / not yet implemented.**
2. Reconcile the exact current consequence-capable candidate contracts before choosing the exemplar. Field Medicine remains a likely candidate because it naturally owns assessment/stabilization semantics, but it is not pre-authorized by this roadmap text.
3. Select one consumer only if it introduces a meaningful real state transition that fits the new foundation without requiring a giant domain engine.
4. If Field Medicine is selected, first define the minimum represented casualty state and treatment authorization contract; do not infer injury state from prose or fabricate a casualty in production.
5. Keep Weapons separate unless/until its resource/safety/target/consequence contract is explicitly reconciled; Weapons risk/lethality is a distinct structural question.
6. Do not turn H2H scored sparring into injury/restraint state merely to exercise the foundation.
7. Prefer one bounded exemplar; batch only structurally equivalent consequence consumers after it passes.
8. Keep application/consequence evidence separate from learning evidence; no automatic XP.

## Deferred boundaries

No hostile/non-consensual combat engine, full Injury Engine, persistent restraint/incapacity system, Weapons lethality system, broad casualty simulator, universal active-modifier evaluator, full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior rewrite, deep crafting, second production character solely for testing, or Tahoe exterior traversal as side effects of the next slice.

## Exact resume point

**Represented Consequence State Foundation v1 is complete through PR #138 merge `ba662010cdf19b078eb6a82c54674250534fab99` / Deploy #214 run `31880931750` SUCCESS. The generic deterministic seam now exists for exact represented-task authorization -> bounded pre-existing simulated-field mutation -> causal state-change event, with savepoint rollback and retry idempotency. No live consequence was forced in production. Next reconcile candidate domain contracts and choose the first real consequence consumer; do not assume Field Medicine or Weapons semantics without reading the exact current contracts first.**
