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

Latest runtime deployment: **Deploy #214 / run `31880931750` SUCCESS**, Represented Consequence State Foundation v1, PR #138 merge `ba662010cdf19b078eb6a82c54674250534fab99`.

Post-deploy evidence:
- service active/healthy, schema remains v5;
- production `sandboxctl init` succeeded;
- autonomy enabled in normal mode at 1x with retry `null` and a pending action;
- cognition binding remained `gemini-3.1-flash-lite`; Groq fallback bootstrap remained healthy;
- Telegram bot/API/owner/allowed-user configuration remained healthy;
- live state advanced naturally to sim time `2025-05-06T08:35:00+00:00`;
- Darian was naturally `rest`ing in the Home Gym at readback;
- no represented consequence was forced for proof;
- no production character/action/state fixture was fabricated solely for validation.

Exact consequence mutation, rollback and retry-idempotency behavior is proven by full CI and fresh-DB ephemeral tests. Production deployment/init proves the new library loaded safely; do not overstate that as a live consequence-mutation proof.

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
- **Represented Consequence State Foundation v1 — PR #138 / Deploy #214.**

## Controlled H2H state

One generic action remains authoritative: `spar`.

Exact represented session selects the current H2H application:
- `h2h_controlled_striking_spar_v1` -> `engage_unarmed_striking` -> `scored_contact_only`;
- `h2h_controlled_grapple_spar_v1` -> `control_unarmed_grapple` -> `scored_positional_control_only`.

Both require an exact represented object target plus one distinct colocated character participant with explicit `controlled_sparring_consent`. Skill/performance scoring is separate from authorization. Neither path mutates injury, incapacity, persistent restraint, or participant state and neither authorizes hostile/non-consensual use.

## Represented Consequence State Foundation v1

Implementation: `src/observer_sandbox/represented_consequence_state.py`.
Design note: `docs/REPRESENTED_CONSEQUENCE_STATE_FOUNDATION_V1.md`.

Canonical seam:

`validated represented task -> deterministic consequence authorization -> bounded simulated-state mutation -> causal event evidence`

The foundation reuses schema-v5 primitives rather than adding a new consequence subsystem.

A `ConsequenceAuthorization` must explicitly bind:
- consequence id;
- exact represented task id already persisted on the completed source action;
- subject id;
- subject role: `actor`, `target`, or `participant`;
- finite mutation list.

State boundary:
- source action must be completed and have its `action_completed` event;
- task id must match exactly;
- subject must actually occupy the declared action relationship;
- only pre-existing `fields` rows with `mode='simulated'` may be changed;
- no new state fields are created implicitly;
- canonical/static/derived truth fails closed;
- field authority/source metadata is preserved.

Supported immediate operations reuse the existing effect vocabulary:
`add`, `multiply`, `set`, `clamp_min`, `clamp_max`.

Evidence/transaction boundary:
- success emits `represented_consequence_applied` tied to the source `action_id` and `action_completed` event via `caused_by_event_id`;
- before/after mutation evidence is stored in structured state changes;
- consequence evidence is `learning_evidence: false` and awards no Skill XP;
- SQLite savepoint semantics prevent partial multi-field writes;
- retries are idempotent per action/consequence/task/subject tuple and do not double-apply additive or multiplicative effects.

CI #863 passed **465 tests** plus fresh DB `init` and `status`; schema remains v5.

Skill score, IQ, supporting Attributes, performance quality, model prose, or generic capability never independently authorizes consequence mutation.

## Evidence boundary

Runtime application and consequence evidence are not learning evidence and do not automatically award XP.

Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival and Field Medicine definitions do not activate XP by themselves.

## Next canonical direction

**First Real Represented Consequence Consumer — REVIEW NEXT / not yet implemented.**

First reconcile the exact current candidate domain contracts before choosing the exemplar. Field Medicine remains a likely candidate because casualty assessment/stabilization naturally owns explicit state semantics, but that is not implementation authorization by itself and must be checked against the current definition/task/resource contracts.

Preserve:
- performance outcome != consequence authorization;
- exact target/context/participant/resource authority;
- deterministic mutation ownership;
- pre-existing simulated state only unless a later domain slice explicitly owns state creation/migration;
- consequence events causally tied to the action that caused them;
- Skill score/supporting Attributes cannot manufacture state mutation;
- application/consequence evidence != learning evidence;
- no invented child Skill scores;
- no synthetic production casualty/character/action merely for proof.

Keep Weapons separate until its exact resource/safety/target/consequence contract is reconciled. Do not turn controlled H2H sparring into injury or restraint state merely to exercise the new foundation.

## Exact resume point

**Represented Consequence State Foundation v1 is complete through PR #138 merge `ba662010cdf19b078eb6a82c54674250534fab99` / Deploy #214 run `31880931750` SUCCESS. The generic deterministic seam now exists for exact represented-task authorization -> bounded mutation of pre-existing simulated fields -> causal state-change event, with atomic rollback and retry idempotency. No live consequence was forced in production. Reconcile current candidate domain contracts, then choose the first real represented consequence consumer rather than assuming Field Medicine or Weapons semantics from memory.**
