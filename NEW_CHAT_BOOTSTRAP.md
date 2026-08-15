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

**Minimum-unlocked does not mean immutable.** Personality, preferences, hobbies/interests, and habits have developmental lifecycles. The active human-continuity work is the **Adaptive Character Disposition Foundation**.

Canonical order:

`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> slow Personality Plasticity`

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md`.

## Adaptive disposition status

### Habit Formation/Extinction exemplar v1 — COMPLETE

PR #167 established deterministic habit adaptation from completed represented behavior plus context. Same-day repetition is diminished, development/decay is gradual, history is retained, cognition receives compact state, and runtime-learned rows survive ordinary init/deploy.

### Hobby / Interest Lifecycle v1 — COMPLETE

PR #172 establishes the next exemplar. See `docs/HOBBY_INTEREST_LIFECYCLE_V1.md`.

Current contract:
- only completed target-based voluntary `read` and `use` engagements are interest evidence in v1;
- one engagement creates an emerging interest, not an instant hobby;
- repeated engagement across distinct days can progress emerging -> recurring -> established;
- short-interval repetition receives reduced weight;
- `character_preferences(type='interest')` is learned-interest lifecycle authority;
- established learned interests project to the active `character_hobbies` surface;
- dormancy/lapse can remove that active projection without deleting interest history;
- authored canonical hobbies are independent baseline rows and remain untouched;
- the LLM reads disposition context but cannot directly mutate lifecycle state.

No schema migration was required.

### Next adaptive slice

**Preference Adaptation v1** — minimum-foundation depth only. It should strengthen/weaken preferences from legitimate repeated voluntary choice/outcome evidence, avoid single-event flips, preserve canonical starting baselines, and keep deterministic runtime as mutation authority.

## Autonomy Livelock Watchdog v1 — COMPLETE

The earlier Training Hall freeze was an action/target decision livelock rather than a service crash or provider call-limit event. PR #170's bounded watchdog remains installed: repeated authoritative pair-validation livelocks may recover only from the already-shaped legal action surface, while provider/API/quota/rate-limit and other unrelated failures remain fail-closed under existing contracts.

See `docs/AUTONOMY_LIVELOCK_WATCHDOG_V1.md`.

## Current verified deployment

Latest runtime deployment: **Deploy #233 / run `31899884337` SUCCESS**.

Runtime PR: **#172 — Hobby / Interest Lifecycle v1**
- final tested head: `05388eba4c6e9e4870b3eb0e927c0247c0e68f06`
- merge: `3822332c0fb5bca7295e83e0cc0bcebf06973be8`
- **CI #937 / run `31899806440`: SUCCESS**
- **560 passed in 37.15s**
- fresh DB init/status healthy; schema v5.

One automatic Skill Progression Foundation production-copy gate initially failed before validator execution because SSH was reset by the server. Only that failed job was retried; staging and the actual disposable production-copy validator then succeeded. No runtime code was changed for the transient infrastructure failure and the full Python suite was not deliberately repeated.

Production readback after Deploy #233:
- service active/healthy;
- schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **5x**;
- sim time `2025-05-07T17:19:00+00:00`;
- Darian was naturally idle in the Top-Class Home Gym at readback;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram configuration/API healthy.

No `read`/`use` action was forced in production to manufacture Hobby/Interest evidence. Treat a naturally formed learned hobby as unproven until normal runtime produces the required evidence.

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
- Do not infer a hobby from training, physiological need resolution, or one-off curiosity.
- No relationship-system expansion by default.
- No hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, or real-world weapon instructions.
- Do not fabricate production actions/actors/casualties solely for proof.

## Exact resume point

**Adaptive Character Disposition Foundation now has two completed exemplars: Habit Formation/Extinction v1 and Hobby/Interest Lifecycle v1. Hobby/Interest Lifecycle is deployed through PR #172 final head `05388eba4c6e9e4870b3eb0e927c0247c0e68f06`, merge `3822332c0fb5bca7295e83e0cc0bcebf06973be8`, CI #937 with 560 passed, and Deploy #233 SUCCESS. Production is healthy at schema v5, autonomy normal, retry null, pending action present, speed 5x, sim time `2025-05-07T17:19:00+00:00`. No synthetic hobby proof was created. Continue with Preference Adaptation v1 at minimum-foundation depth.**
