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

Latest runtime deployment: **Deploy #226 / run `31893586685` SUCCESS**, Skills Closure Batch v1, PR #161 merge `7cbc92a38ee8b3f5d8220c6e33ff0c4d00f157b4`.

Final tested head: `f502e7e0e0f438b2dfac9ffab01c547ef1b255b9`.

Validation:
- final **CI #923 / run `31893520852` SUCCESS**;
- fresh DB init/status healthy; schema v5;
- Skill Progression Foundation, Skill Evidence Semantics, Skill Definition Format/Refactor, Tactical progression, Strength Live Cycle, and Public Readiness Security gates all green;
- first full CI attempt exposed only four stale progression contract assertions after 531 passing tests; they were updated narrowly;
- no manual repeated full-suite rerun was requested.

Production readback after Deploy #226:
- service active/healthy; autonomy enabled, normal mode, retry null, pending action present;
- speed **10x** at readback;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram configuration healthy;
- sim time `2025-05-07T06:24:00+00:00`;
- Darian was naturally training in the Top-Class Home Gym;
- Field Medicine 75/A, Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills 85.167/A;
- no production Field Medicine practice or casualty was fabricated for proof.

This morning training state also confirms that the earlier circadian correction has advanced beyond the old early-evening sleep lock.

## Skills section — CLOSED v1

Skills is **minimum-unlocked and closed for the current vertical-completeness pass**.

Frozen learned Skills:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` remains a derived/non-executable parent over Bladed Weapons + Firearms and has no direct XP. Hidden legacy `weapons` is compatibility only.

All seven learned Skills now have authoritative score/grade semantics, profile/cognition visibility, meaningful represented application where safely runnable, and a legitimate learning path.

Field Medicine closure adds:
- `field_medicine_scenario_practice`;
- explicit simulation-safe `skill_practice` learning evidence;
- dedicated Training Hall scenario simulator;
- no live casualty requirement for practice;
- no casualty creation, diagnosis/treatment graph, or application=>XP shortcut.

Real Field Medicine assessment/stabilization remains casualty-context-bound.

Skill-like Attribute/compatibility fields are not automatically independent Skills. Deeper Skill trees are deferred until a represented task actually requires them.

See `docs/SKILLS_CLOSURE_V1.md`.

Metadata note: active Field Medicine learning authority is the explicit progression/practice registries. The older universal Skill Definition learning-evidence description was not comprehensively refactored in the closure batch; treat that as deferred metadata normalization, never as implicit application-to-XP authority.

## Next canonical phase

**Remaining Profile Minimum Unlock Sweep — REVIEW/IMPLEMENT NEXT.**

Do not deepen Skills now.

Review all remaining Character Profile sections:
- identity
- appearance
- body
- attributes
- recovery
- sexual
- personality
- preferences
- background

For each, classify:
1. already minimum-unlocked;
2. closure-only gap;
3. missing meaningful runtime influence.

Then batch equivalent gaps rather than creating one PR per section.

Likely grouping, subject to fresh repository inspection:
- **Mature closure:** Body + Attributes + Recovery + Sexual — substantial foundations already exist; audit/close rather than rewrite.
- **Canonical/context:** Identity + Appearance + Personality + Preferences + Background — add only the smallest real cognition/action influence required where missing.

Static/canonical values do not need artificial mutation just to count as simulated. Their valid runtime role may be stable context that affects cognition, feasibility, choice, or presentation.

## After the profile sweep

Once every profile section is minimum-unlocked, review missing cross-cutting workflow foundations before deepening any section. Candidate areas include profile-to-cognition influence, generic task/action lifecycle, inventory/resources/consequences, environment context, knowledge/familiarity, inter-character participation, event/lifecycle handling, long-horizon progression/decay, and autonomy goal continuity.

Choose exact order from future repository/live evidence.

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

**Vertical-completeness policy is active. Skills Closure Batch v1 is complete through PR #161 final head `f502e7e0e0f438b2dfac9ffab01c547ef1b255b9`, merge `7cbc92a38ee8b3f5d8220c6e33ff0c4d00f157b4`, CI #923, and Deploy #226 / run `31893586685` SUCCESS. Skills is CLOSED v1. Production is healthy; at readback Darian was naturally training at `2025-05-07T06:24:00+00:00`, speed 10x, and Field Medicine remained 75/A without fabricated practice/casualty. Review and batch the remaining nine profile sections next; do not deepen Skills.**
