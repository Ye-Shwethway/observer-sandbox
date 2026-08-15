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

## Current development direction

The active roadmap is **profile-first**: make Character Profile sections meaningfully participate in simulation before expanding relationship or broader multi-character systems.

Current focus: **Skills**.

Relationship-oriented expansion and the previously proposed casualty handoff/lifecycle-end producer are deferred until additional represented-character work resumes. Existing participant, consent, colocation, casualty, and lifecycle primitives remain valid reusable foundations.

## Current verified deployment

Latest runtime deployment: **Deploy #219 / run `31885774198` SUCCESS**, Survival Skill Progression Producer v1, PR #148 merge `8e094c542d1664f09deb6492ff7dbcb357f95111`.

Final tested PR head: `159afdb3ccda6fd1745148f160954c8c1c7a71d9`.

Validation:
- **CI #888 / run `31885722183` SUCCESS**;
- full suite: **500 passed in 34.75s**;
- fresh DB init/status succeeded;
- schema remains v5;
- Skill Progression Foundation, Skill Evidence Semantics, Skill Definition, Tactical Planning progression, and Strength validation gates passed.

Verified production readback after Deploy #219:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, 1x, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time was `2025-05-06T10:33:00+00:00`;
- Darian was naturally moving while located in the Kitchen;
- Survival remained `85 / A`; no production practice was forced merely to prove progression.

Exact Survival learning semantics are CI/fixture evidence. Production deployment proves safe loading and continuity only.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. Runtime application/consequence/lifecycle evidence is not automatically learning evidence.

Production parent Skills:
- H2H `90 / S`
- Weapons `87 / A`
- Survival `85 / A`
- Tactical Planning `92 / S`
- Technology `82 / A`
- Field Medicine `75 / A`.

## Current Skills coverage

### Hand-to-Hand Combat
- represented controlled striking/grapple applications exist;
- progression exists through structured Training Method evidence;
- represented sparring currently requires a second distinct consenting colocated character;
- no injury/casualty production from controlled H2H.

### Weapons
- capability/application definitions exist for familiar melee and ranged weapon employment;
- **represented runtime is still missing**;
- progression producer is still missing;
- lethality, hostile use, and casualty generation remain deferred.

### Survival
- represented application runtimes exist for field navigation and field sustainment;
- **explicit solo-usable progression now exists** through:
  - `field_navigation_practice`;
  - `field_sustainment_practice`.
- both are purpose-built simulation-safe `practice` targets in the Training Hall;
- ordinary obstacle-course use and represented Survival application evidence do not automatically grant Survival XP;
- settlement uses the existing generic idempotent Skill progression engine.

### Tactical Planning
- represented assess and maneuver-planning runtimes exist;
- structured progression exists.

### Technology
- represented known-fault diagnostic runtime exists;
- explicit `systems_diagnostic_practice` progression exists.

### Field Medicine
- read-only casualty assessment and bounded stabilization runtimes exist;
- both require a represented casualty character/context;
- progression producer remains deferred;
- casualty handoff/lifecycle-end producer remains deferred with multi-character work.

## Current casualty foundation — preserved but not active priority

Existing bounded flow remains:

`typed represented fall -> casualty lifecycle state -> read-only Field Medicine assessment -> optional bounded stabilization -> explicit lifecycle-end event still required for clear`

Risk reaching zero does not auto-clear and does not assert healing. No Injury Engine, wound taxonomy, diagnosis engine, definitive treatment, death/incapacity, random accidents, or automatic Field Medicine XP is implied.

## Next development sequence

1. **Weapons Simulation-Safe Runtime v1 — REVIEW NEXT / not yet implemented.**
2. Reconcile existing Weapons definitions, represented task patterns, available represented weapon/training resources, and safe target primitives.
3. Implement the smallest solo-usable represented training/simulation application for familiar weapon employment.
4. Prefer one bounded exemplar; batch a structurally equivalent melee/ranged follow-on only when the shared invariant is proven.
5. Keep the runtime training/simulation-safe: no hostile target, lethality, injury, casualty generation, or non-consensual combat.
6. Application evidence must remain separate from learning evidence; do not award Weapons XP merely for use.
7. After safe represented Weapons application coverage is proven, review **Weapons Progression Producer v1** as the next Skills-section gap.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, Weapons lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, second competency score, economy/jobs/quests, or synthetic production actors/targets solely for proof.

## Exact resume point

**Survival Skill Progression Producer v1 is complete through PR #148 final tested head `159afdb3ccda6fd1745148f160954c8c1c7a71d9`, merge `8e094c542d1664f09deb6492ff7dbcb357f95111`, CI #888 / run `31885722183` with 500 passing tests plus fresh-DB init/status and all relevant Skill/Strength gates green, and Deploy #219 / run `31885774198` SUCCESS. Survival now has explicit simulation-safe navigation and sustainment practice producers using the existing structured `skill_practice` evidence and idempotent Skill settlement path; generic activity and represented application evidence remain non-learning evidence. No live practice was forced for proof. Review Weapons Simulation-Safe Runtime v1 next.**
