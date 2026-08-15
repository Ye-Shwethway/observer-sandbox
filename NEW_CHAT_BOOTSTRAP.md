# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-16

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

**Minimum-unlocked does not mean immutable.** Personality, preferences, hobbies/interests, and habits have developmental lifecycles. The active human-continuity work is the **Adaptive Character Disposition Foundation**.

Canonical order:

`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> slow Personality Plasticity`

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`.

## Adaptive disposition status

### Habit Formation/Extinction exemplar v1 — COMPLETE

PR #167 established deterministic habit adaptation from completed represented behavior plus context. Same-day repetition is diminished, development/decay is gradual, history is retained, cognition receives compact state, and runtime-learned rows survive ordinary init/deploy.

### Hobby / Interest Lifecycle v1 — COMPLETE

PR #172 established the next exemplar. See `docs/HOBBY_INTEREST_LIFECYCLE_V1.md`.

Current contract keeps learned interest authority separate from established hobby projection, uses only completed target-based voluntary `read` / `use` evidence in v1, diminishes short-interval repetition, supports gradual establishment/dormancy/lapse, preserves canonical hobbies, and leaves mutation authority deterministic.

### Preference Adaptation v1 — COMPLETE

PR #174 established medium-plastic preference adaptation. See `docs/PREFERENCE_ADAPTATION_V1.md`.

Current contract:
- completed voluntary target-based `read` / `use` engagement supplies conservative positive evidence;
- one engagement does not create an instant visible preference;
- short-interval repetition is diminished;
- non-selection, inactivity, and unrelated actions never count as negative evidence;
- negative evidence requires an explicit represented aversive/outcome producer through the signed evidence API;
- signed per-target evidence persists under `runtime_state` namespace `preference_adaptation_v1:`;
- sufficiently repeated evidence materializes dynamic `like` or `dislike` projections in `character_preferences`;
- opposing evidence must cross a neutral band before reversal;
- canonical authored preferences remain untouched;
- established dynamic preferences reach cognition through the existing preference surface;
- LLM cognition cannot mutate preference state directly.

No schema migration was required.

### Next adaptive slice

**Slow Personality Plasticity v1** — minimum-foundation depth only. Personality must remain substantially more stable than preferences: ordinary single actions/events must never rewrite traits. Any drift must require accumulated long-horizon evidence, remain small and bounded, preserve the authored baseline, persist across deploy/init, and reach cognition without granting the LLM mutation authority.

## Autonomy Livelock Watchdog v1 — COMPLETE

The earlier Training Hall freeze was an action/target decision livelock rather than a service crash or provider call-limit event. PR #170's bounded watchdog remains installed: repeated authoritative pair-validation livelocks may recover only from the already-shaped legal action surface, while provider/API/quota/rate-limit and other unrelated failures remain fail-closed under existing contracts.

See `docs/AUTONOMY_LIVELOCK_WATCHDOG_V1.md`.

## Current verified deployment

Latest runtime deployment: **Deploy #234 / run `31900505874` SUCCESS**.

Runtime PR: **#174 — Preference Adaptation v1**
- final tested head: `6396ab34d190cfa894b69dcb9bdd52c743b4b02a`
- merge: `c72807dab416f64d459f4e4863efc15ce02c09e7`
- **CI #938 / run `31900387940`: SUCCESS**
- **566 passed in 114.85s**
- fresh DB init/status healthy; schema v5.

Three automatic production-copy gates initially failed during staging because SSH/rsync was reset before validator execution: Body Composition, Sexual Anatomy/Physiology, and Body Measurement. Only those failed jobs were retried; all three actual disposable production-copy validators then succeeded. No runtime code was changed for the transient infrastructure failures and the full Python suite was not deliberately repeated.

Production readback after Deploy #234:
- service active/healthy;
- schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **5x**;
- sim time `2025-05-07T18:09:00+00:00`;
- Darian was naturally **reading in the Living Room**;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram configuration/API healthy.

The in-progress natural `read` action is not evidence of an established learned preference until its represented completion settles through the runtime contract. No production action or negative outcome was fabricated for proof.

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

## Development boundaries

- LLM proposes; deterministic runtime validates/mutates.
- Do not let the watchdog grow into a general deterministic story chooser.
- Do not make personality/preferences/hobbies/habits fixed forever-fields.
- Do not permit arbitrary direct LLM disposition mutation.
- Do not infer negative preferences from non-selection or inactivity.
- Personality plasticity must be much slower than preference adaptation and must not react to ordinary single events.
- No relationship-system expansion by default.
- No hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, or real-world weapon instructions.
- Do not fabricate production actions/actors/casualties solely for proof.

## Exact resume point

**Adaptive Character Disposition Foundation now has three completed slices: Habit Formation/Extinction v1, Hobby/Interest Lifecycle v1, and Preference Adaptation v1. Preference Adaptation is deployed through PR #174 final head `6396ab34d190cfa894b69dcb9bdd52c743b4b02a`, merge `c72807dab416f64d459f4e4863efc15ce02c09e7`, CI #938 with 566 passed, and Deploy #234 SUCCESS. Production is healthy at schema v5, autonomy normal, retry null, pending action present, speed 5x, sim time `2025-05-07T18:09:00+00:00`; Darian was naturally reading in the Living Room. No synthetic preference proof was created. Continue with Slow Personality Plasticity v1 at minimum-foundation depth.**
