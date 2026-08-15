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
`branch -> focused tests + final PR CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

During implementation use the smallest task-relevant tests/gates. Do not repeatedly run the full suite. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes skip the full Python suite; do not deliberately repeat a full suite after merge when the already-tested PR is sufficient.

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence.

## Strategic mode — vertical completeness first

The active Creator direction is:

**minimum unlock every Character Profile section first, complete the overall system workflow/foundations, then return later to deepen individual sections.**

Follow `docs/MINIMUM_PROFILE_UNLOCK_POLICY_V1.md`.

A minimum-unlocked section needs authoritative state, at least one meaningful runtime influence, and persistence/presentation where relevant. Exhaustive mechanics, deep taxonomies, and bespoke engines per field are not required during this pass.

Batch structurally equivalent work. Avoid repetitive one-field/one-PR or one-application/one-PR cadence unless a genuinely new invariant needs an exemplar.

## Current verified deployment

Latest runtime deployment: **Deploy #225 / run `31892433699` SUCCESS**, Firearms Progression Producer v1, PR #159 merge `d759ef7903f889517e76a48b803fba83bba09ba0`.

Final tested head: `1553621a93e52cb52e948a856dec99a49bd4fc23`.

Validation:
- final **CI #918 / run `31892374935` SUCCESS**;
- Skill Progression Foundation, Skill Evidence Semantics, Skill Definition Format/Refactor, Tactical progression, and Strength Live Cycle gates all green;
- production init/status healthy; schema v5.

Production readback after Deploy #225:
- service active/healthy; autonomy enabled, normal mode, retry null, pending action preserved;
- speed **30x** at readback;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram configuration healthy;
- sim time `2025-05-06T18:56:00+00:00`;
- Darian remained naturally sleeping in Darian's Master Suite because the action was pending before the circadian correction;
- Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production weapon practice/application was fabricated for proof.

## Circadian stabilization

**Circadian Sleep Rhythm Stabilization v1** is complete through PR #158, merge `f63786c5f0f3d4c4b2098a0c6dc37d9ced9180db`, Deploy #224.

Ordinary 16-hour wakefulness no longer creates a strong overnight-sleep signal at any clock time. The normal 07:00–22:00 wake window resists ordinary early sleep, while 22:00–07:00 provides the normal circadian sleep pull. Severe >=20h wakefulness or critical raw sleepiness can override timing. The pre-existing pending sleep was deliberately not rewritten.

## Skills v1 scope freeze

Learned Skills in the minimum v1 pass:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is a derived/non-executable parent over Bladed Weapons + Firearms and has no direct XP.

Skill-like compatibility/Attribute fields such as combat skill, weapons proficiency, survival skill, powerlifting capacity, focus/precision, practical skills, technological aptitude, and medical knowledge are not automatically independent Skills.

Current coverage:
- H2H: represented applications + progression active.
- Bladed: simulation-safe application + explicit progression complete.
- Firearms: simulation-safe application + explicit progression complete.
- Survival: represented application + explicit progression complete.
- Tactical Planning: represented application + progression complete.
- Technology: represented application + explicit progression complete.
- Field Medicine: casualty-context assessment/stabilization exists; minimum progression remains the final learned-Skill closure item.

## Active implementation

**Skills Closure Batch v1 — AUTHORIZED / ACTIVE.**

One batch should:
- add one abstract simulation-safe Field Medicine practice producer using the proven `skill_practice` evidence pattern;
- progress only `field_medicine` without requiring or fabricating a live casualty;
- keep real assessment/stabilization casualty-context-bound and application evidence separate from learning evidence;
- verify the frozen seven-Skill surface and compatibility classifications;
- close **Skills section minimum-unlocked / CLOSED v1**;
- avoid deep Skill trees, Injury Engine, treatment graph, H2H rewrite, hostile combat, or relationship expansion.

After this batch, leave Skills and begin the **Remaining Profile Minimum Unlock Sweep** across identity, appearance, body, attributes, recovery, sexual, personality, preferences, and background. Existing mature sections receive closure review rather than rewrites; canonical/contextual sections receive only the smallest real runtime influence required by policy.

## Hard boundaries

- no relationship system expansion during the current minimum profile pass;
- no hostile/non-consensual combat engine;
- no weapon lethality/injury/casualty side effects;
- no real-world weapon instructions;
- no Injury Engine or deep weapon taxonomy;
- no generic use/application => XP shortcut;
- no H2H hierarchy rewrite as a side effect;
- no fabricated production actors/actions/casualties merely for proof.

## Exact resume point

**Vertical-completeness policy is active. Firearms Progression Producer v1 is deployed through PR #159 / merge `d759ef7903f889517e76a48b803fba83bba09ba0` / CI #918 / Deploy #225. Skills v1 is frozen to seven learned Skills plus derived Weapon Mastery. Complete Skills Closure Batch v1 in one batch by adding minimum simulation-safe Field Medicine progression and verifying/classifying the existing surface; then mark Skills CLOSED v1 and move immediately to the Remaining Profile Minimum Unlock Sweep.**
