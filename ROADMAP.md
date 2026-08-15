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
- Development verification is focused-first: use task-relevant tests/gates while iterating and reserve the full suite for the final code/runtime PR checkpoint unless broader risk justifies another run. Docs-only changes do not need the full Python suite.

## Strategic development mode — vertical completeness first

The Creator has explicitly prioritized **overall workflow completeness before subsystem depth**.

Canonical sequence:

`minimum unlock all Character Profile sections -> verify overall system workflow -> deepen highest-value systems later`

Follow `docs/MINIMUM_PROFILE_UNLOCK_POLICY_V1.md`.

Minimum unlock means real, not cosmetic: authoritative state + at least one meaningful runtime influence + persistence/presentation where relevant. It does not require exhaustive mechanics, deep taxonomies, multiple bespoke applications, or a dedicated subsystem for every field.

Batch structurally equivalent work. Do not return to one-field/one-PR or one-Skill-application/one-PR cadence unless a genuinely new invariant requires an exemplar.

## Current verified deployment

Latest runtime deployment: **Deploy #225 / run `31892433699` SUCCESS**, Firearms Progression Producer v1, PR #159 merge `d759ef7903f889517e76a48b803fba83bba09ba0`.

Final tested PR head: `1553621a93e52cb52e948a856dec99a49bd4fc23`.

Validation:
- final PR **CI #918 / run `31892374935` SUCCESS**;
- task-relevant Skill Progression, Skill Evidence, Skill Definition, Skill Definition Refactor, Tactical Planning progression, and Strength Live Cycle gates all succeeded;
- the prior CI #917 had exactly one stale global progression-revision assertion after 531 passing tests; only that assertion was corrected;
- no manual repeated full-suite rerun was requested;
- production init/status succeeded; schema remains v5.

Verified production readback after Deploy #225:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, retry null, pending action preserved;
- runtime speed was **30x** at readback;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time remained `2025-05-06T18:56:00+00:00` because the pre-existing overnight sleep action was still pending;
- Darian remained naturally sleeping in Darian's Master Suite;
- Bladed Weapons remained 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production firearm practice/application was fabricated for proof.

### Circadian stabilization checkpoint

Before Firearms progression, **Circadian Sleep Rhythm Stabilization v1** shipped through PR #158, merge `f63786c5f0f3d4c4b2098a0c6dc37d9ced9180db`, Deploy #224.

The sleep-pressure model no longer treats ordinary 16-hour wakefulness as a strong sleep signal at any clock time. Ordinary accumulated wakefulness becomes strongly sleep-promoting in the authored 22:00–07:00 night window, while severe >=20h wakefulness or critical raw sleepiness can still override the daytime wake window. The sleep action already pending before that deploy was deliberately not cancelled or rewritten.

## Skill authority / ontology

- learned leaf/component `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- derived parent Skills summarize components and are not independent learning/task authority;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. Runtime application evidence is not automatically learning evidence.

### Skills v1 ontology freeze

The current v1 learned Skill scope is intentionally shallow:

- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is a derived/non-executable parent over Bladed Weapons + Firearms. Hidden legacy `weapons` remains only a compatibility projection.

Skill-like profile/Attribute compatibility fields such as combat skill, weapons proficiency, survival skill, powerlifting capacity, focus/precision, practical skills, technological aptitude, and medical knowledge are **not automatically promoted into separate Skills** during the minimum pass.

Add deeper child Skills only when a future represented task needs distinct authority/progression.

### Current Skills coverage

- **Hand-to-Hand Combat** — represented controlled striking/grapple applications + progression active; second-character sparring remains conditional on a distinct consenting colocated actor.
- **Bladed Weapons** — simulation-safe represented application + explicit practice progression complete.
- **Firearms** — simulation-safe represented application + explicit practice progression complete.
- **Survival** — represented field navigation/sustainment + explicit solo progression active.
- **Tactical Planning** — represented assessment/planning + structured progression active.
- **Technology** — represented known-fault diagnostic + explicit systems-diagnostic progression active.
- **Field Medicine** — read-only casualty assessment + bounded stabilization active; minimum learning producer remains the one missing Skills-v1 closure item.
- **Weapon Mastery** — derived parent, intentionally no direct application/XP.

## Immediate implementation — Skills Closure Batch v1

**Authorized and active.** Complete this as one batch rather than another chain of micro-slices.

Scope:
1. add one simulation-safe, abstract Field Medicine practice producer using the already-proven explicit `skill_practice` evidence pattern;
2. progress only `field_medicine`; do not require a live casualty or fabricate a production casualty for learning proof;
3. keep real assessment/stabilization applications casualty-context-bound and separate from learning evidence;
4. classify legacy/skill-like profile fields as compatibility/Attribute values rather than spawning new Skill entities;
5. verify all seven learned v1 Skills have authoritative score/grade semantics, cognition/profile visibility, meaningful represented application where safely runnable, and a legitimate learning path;
6. mark **Skills section minimum-unlocked / CLOSED v1** when the batch passes;
7. no deep weapon tree, H2H rewrite, Injury Engine, treatment graph, or new relationship system.

Use focused tests while iterating and one final PR CI checkpoint by default.

## Next development phase — Remaining Profile Minimum Unlock Sweep

After Skills Closure Batch v1, do **not** deepen Skills further. Move across the remaining Character Profile sections using section-sized batches.

Target sections:
- identity
- appearance
- body
- attributes
- recovery
- sexual
- personality
- preferences
- background

Body/Attributes/Recovery/Sexual already have substantial foundations and should receive minimum-closure review rather than broad rewrites. Identity/Appearance/Personality/Preferences/Background should receive the smallest real runtime influence needed to satisfy the minimum-unlock policy.

Prefer batching structurally similar canonical/contextual sections together when safe rather than one PR per section.

## After the profile sweep

Once every Character Profile section is minimum-unlocked, perform an overall workflow/foundation review before local deepening.

Likely cross-cutting foundation areas include:
- profile -> cognition influence;
- generic action/task lifecycle;
- resources/inventory/consequences;
- environment/world context;
- knowledge/familiarity;
- inter-character participation;
- event/lifecycle handling;
- long-horizon progression/decay;
- autonomy planning and goal continuity.

Ordering must be selected from repository/live evidence at that future checkpoint rather than prebuilding all of them now.

## CI cadence

- focused task-relevant tests/gates during implementation;
- one final full CI checkpoint for code/runtime PRs by default;
- no deliberate second full-suite run merely because an already-tested PR merged to `main`;
- docs-only pull requests skip the full Python suite;
- manual full reruns only when broader risk actually warrants one.

Some specialized acceptance workflows may still run automatically on matching pushes; do not mistake those for manually requested full-suite loops.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, H2H hierarchy rewrite, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, or synthetic production actors/actions solely for proof.

## Exact resume point

**Vertical-completeness mode is now authoritative. Firearms Progression Producer v1 is complete through PR #159 / merge `d759ef7903f889517e76a48b803fba83bba09ba0` / CI #918 / Deploy #225. Skills v1 ontology is frozen to seven learned Skills plus derived Weapon Mastery. Implement Skills Closure Batch v1 next: add minimum simulation-safe Field Medicine progression, verify/classify the current Skill surface, close Skills v1, then move immediately into the Remaining Profile Minimum Unlock Sweep instead of deepening Skills.**
