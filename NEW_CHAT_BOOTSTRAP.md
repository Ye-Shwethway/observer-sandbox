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

Latest runtime deployment: **Deploy #227 / run `31895171211` SUCCESS**, Solo Sexual Regulation Naturalism v2, PR #163 merge `13c57933b8136c014f6940b2647c2acdbc3b8eac`.

Final tested head: `b9d7ee05f52555417afb9fc1272e0d921657be6b`.

Validation:
- final **CI #929 / run `31895111772` SUCCESS**, **538 passed**;
- fresh DB init/status healthy; schema v5;
- Solo Regulation Naturalism v2 Acceptance #23, Thorne Estate Training Environment #9, Research Action Semantics #29, Strength Live Cycle #82, and Public Readiness Security #113 all green;
- earlier final CI exposed only stale world-revision assertions plus an incorrect older-age fixture after 535 passing tests; those were fixed narrowly without changing runtime logic;
- no deliberate post-merge duplicate full suite.

Production readback after Deploy #227:
- service active/healthy; autonomy enabled, normal mode, retry null, pending action present;
- speed **5x** at readback;
- world revision `thorne-estate-v3.4-private-activity-semantics`;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy;
- sim time `2025-05-07T10:54:00+00:00`;
- Darian was in the Top-Class Home Gym, current action `idle`, energy 81.586, fatigue 24.277, sleepiness 23.9;
- no production self-satisfaction action was forced or accelerated for proof.

## Solo Sexual Regulation Naturalism v2 — COMPLETE

The earlier v1 behavioral cadence was over-conservative: age was only an adult yes/no gate, good recovery supplied no positive contribution, release pressure rebuilt too slowly, and generic `world.access=private` was incorrectly treated as the whole privacy model.

Naturalism v2 corrects the baseline without adding a quota or forcing behavior.

Current drive uses:
- authored libido as primary stable authority;
- bounded adult life-stage bonus;
- positive recovery bonus for good energy / low fatigue / low sleepiness;
- represented resident-scope solitude bonus;
- libido-shaped release-recency recovery;
- trailing-24-hour saturation penalty;
- adverse recovery penalties only when state is meaningfully poor.

The anti-loop guard is **2 simulated hours**. It is a pacing guard, not a clinical refractory-period claim. For Darian's authored young/high-libido/healthy/solitary state, a same-day repeat can be legal when state supports it; cognition remains free to choose other actions.

Privacy suitability is independent of generic room access via `world.metadata.private_activity`:
- Darian Master Suite/Bathroom remain valid;
- multiple secluded estate spaces such as Library, Training Hall, Home Gym and secure/restricted rooms can qualify when authorized and alone;
- Quasi's Room and Guest Rooms are explicitly unsuitable despite `access=private`.

Reachable safe private locations are now discovered across the normal location graph with BFS rather than only one edge. Normal movement is still required.

See `docs/SOLO_SEXUAL_REGULATION_NATURALISM_V2.md`.

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

Do not deepen Skills now. Treat Naturalism v2 as the corrected Sexual-section baseline.

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

**Vertical-completeness policy is active. Solo Sexual Regulation Naturalism v2 is complete through PR #163 final head `b9d7ee05f52555417afb9fc1272e0d921657be6b`, merge `13c57933b8136c014f6940b2647c2acdbc3b8eac`, CI #929 with 538 passed, and Deploy #227 / run `31895171211` SUCCESS. Production is healthy at schema v5/world revision `thorne-estate-v3.4-private-activity-semantics`; at readback Darian was in the Home Gym at `2025-05-07T10:54:00+00:00`, speed 5x, with no fabricated private action. Skills remains CLOSED v1. Resume with the Remaining Profile Minimum Unlock Sweep and do not deepen Skills yet.**
