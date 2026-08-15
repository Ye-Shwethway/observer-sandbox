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

Do not repeatedly run the full suite. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes skip the Python suite. Use **exemplar-first, then batch-by-pattern** and prefer vertical completeness before local depth.

## Strategic checkpoint

All Character Profile sections are minimum-unlocked v1 and Skills remains CLOSED v1.

**Minimum-unlocked does not mean immutable.** Personality, preferences, hobbies/interests, and habits have developmental lifecycles. The current human-continuity work is the **Adaptive Character Disposition Foundation**.

Canonical order:

`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> slow Personality Plasticity`

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`.

## Adaptive disposition status

### Habit Formation/Extinction exemplar v1 — COMPLETE

PR #167 established deterministic habit adaptation:
- completed represented behavior + context supplies evidence;
- same-day repetitions have diminishing weight;
- habit strength/status develops gradually;
- established habits may become dormant/lapsed through long non-reinforcement without deleting history;
- cognition receives habit-dynamics context;
- LLM cognition does not mutate habit state directly.

Initialization/deploy was also corrected so runtime preferences/hobbies/habits are not deleted and reseeded. Canonical profile values are starting baselines, not perpetual reset values.

### Next adaptive slice

**Hobby/Interest Lifecycle v1** is the next planned exemplar. Keep it minimum-foundation depth: formation/maintenance/dormancy/lapse from legitimate engagement evidence, not a giant leisure/identity engine.

## Autonomy Livelock Watchdog v1 — COMPLETE

A real production freeze occurred while Darian was in the Training Hall at sim time `2025-05-07T15:04:00+00:00`.

Diagnosis:
- service process remained active;
- this was not a provider call-limit/rate-limit crash;
- no pending action existed;
- cognition repeatedly proposed `move -> loc_thorne_estate_food_storage` outside the current need-shaped authoritative `action_options`;
- repeated decision-stage `ValueError` events reached 256-second backoff and simulation progress stopped.

PR #168 added one bounded corrective model retry. PR #169 made reachable-resource awareness planning-only. The live model still repeated the invalid pair, so PR #170 added a deterministic continuity breaker.

Current watchdog contract:
- only the third consecutive same-sim-boundary authoritative pair-validation failure is eligible;
- normal mode only; canary remains fail-closed;
- no recovery for HTTP/provider/API/quota/rate-limit, schedule, completion, or unrelated failures;
- choose only from the current already-shaped authoritative `action_options`;
- physiology need shaping remains authoritative;
- discretionary fallback prefers `idle`, then `rest`;
- normal deterministic `validate_action` still applies;
- recovery provenance is attached in action conditions.

See `docs/AUTONOMY_LIVELOCK_WATCHDOG_V1.md`.

## Current verified deployment

Latest runtime deployment: **Deploy #232 / run `31899099486` SUCCESS**.

Runtime PR: **#170 — Autonomy Livelock Watchdog v1**
- final tested head: `efe4814483cb997c941555e40de879532058938a`
- merge: `b17fbb7fe77e3d4e79f71d0b9a526244ef81c9ff`
- **CI #936 / run `31899038839`: SUCCESS**
- **554 passed in 38.40s**
- fresh DB init/status healthy; schema v5
- Cognition Capability Awareness, Research Action Semantics, Training Movement Contract Normalization, Eating Behavior, and Solo Regulation Naturalism gates green.

Production recovery proof after Deploy #232:
- service active;
- retry state cleared from eight failures to `null`;
- first readback showed pending action `71ab5f8e-...`;
- later readback showed a different pending action `9b02ef99-...`;
- therefore the recovered action completed and autonomy progressed across another action boundary instead of remaining at the frozen decision boundary.

Historical autonomy-error events are retained; recovery did not erase evidence or fabricate a proof action.

## Character Profile / Skills baseline

Profile sections minimum-unlocked:
- Identity
- Appearance
- Body
- Attributes
- Recovery
- Sexual
- Personality
- Skills
- Preferences
- Background

Skills CLOSED v1 learned leaves:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is derived/non-executable; hidden legacy `weapons` is compatibility only.

## Sexual baseline

Solo Sexual Regulation Naturalism v2 remains active: authored libido plus bounded positive young-adult/recovery/solitude context, libido-shaped release recovery, trailing-24h saturation, 2h anti-loop pacing, authored private-activity semantics, and graph-based safe-private-location awareness. No daily/weekly quota exists.

## Development boundaries

- LLM proposes; deterministic runtime validates/mutates.
- Do not let the watchdog grow into a general deterministic story chooser.
- Do not make personality/preferences/hobbies/habits fixed forever-fields.
- Do not permit arbitrary direct LLM disposition mutation.
- No relationship-system expansion by default.
- No hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, or real-world weapon instructions.
- Do not fabricate production actions/actors/casualties solely for proof.

## Exact resume point

**Adaptive Character Disposition Foundation is active. Habit Formation/Extinction exemplar v1 is complete and runtime adaptive disposition survives deploy/init. A production Training Hall freeze was diagnosed as an autonomy action/target livelock, not a system crash or LLM call-limit event. Autonomy Livelock Watchdog v1 is deployed through PR #170 final head `efe4814483cb997c941555e40de879532058938a`, merge `b17fbb7fe77e3d4e79f71d0b9a526244ef81c9ff`, CI #936 with 554 passed, and Deploy #232 SUCCESS. Production retry cleared and two successive pending action IDs proved action-boundary progress resumed. Continue with Hobby/Interest Lifecycle v1 at minimum-foundation depth.**
