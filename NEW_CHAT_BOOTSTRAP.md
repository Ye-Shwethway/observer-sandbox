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

The **Adaptive Character Disposition Foundation is COMPLETE v1 at minimum-foundation depth**:

`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`

See `docs/ADAPTIVE_CHARACTER_DISPOSITION_FOUNDATION.md` and `docs/SLOW_PERSONALITY_PLASTICITY_V1.md`.

Do not deepen local psychology next. Resume with a read-only **Overall Workflow/Foundation Review** and select the next minimum cross-system foundation from actual canonical/live gaps.

## Adaptive disposition status

### Habit Formation/Extinction v1 — COMPLETE

PR #167 established deterministic habit adaptation from completed represented behavior plus stable context, with gradual formation, diminished short-interval repetition, dormancy/lapse without deleting history, persistence, and cognition visibility.

### Hobby / Interest Lifecycle v1 — COMPLETE

PR #172 established bounded voluntary `read` / `use` interest evidence, gradual lifecycle establishment/dormancy/lapse, separate learned-interest authority, established hobby projection, canonical hobby preservation, and deterministic mutation authority.

### Preference Adaptation v1 — COMPLETE

PR #174 established medium-plastic signed preference evidence, gradual dynamic `like` / `dislike` projection, neutral-band reversal, no negative inference from non-selection/inactivity, canonical preference preservation, persistence, and cognition visibility.

### Slow Personality Plasticity v1 — COMPLETE

PR #176 established a deliberately slower authored-trait overlay model.

Current contract:
- canonical `personality.primary_traits` remains the authored baseline and is never rewritten;
- v1 exemplar adapts only the already-authored `disciplined` trait through explicitly registered evidence channels;
- completed represented `train` is the automatic positive exemplar via `completed_deliberate_training`;
- arbitrary traits and arbitrary evidence kinds are rejected;
- same-day repetition has personality evidence weight 0;
- visible drift requires score/effective evidence >=14, at least 14 distinct evidence days, and at least 21 simulated days of horizon;
- first eligible overlay is 0.02 and total overlay is capped at 0.15;
- negative/softening evidence requires an explicit represented registered outcome and is never inferred from omission or inactivity;
- opposing evidence must cross neutral and accumulate over the same long horizon before softening;
- compact established state reaches cognition under `personality.slow_adaptation` while the internal evidence ledger stays runtime-only;
- persistence uses existing `runtime_state`; schema remains v5;
- LLM cognition has no mutation authority.

## Autonomy Livelock Watchdog v1 — COMPLETE

PR #170's bounded watchdog remains installed for repeated authoritative action/target pair-validation livelock. It does not grow into a general deterministic story chooser and does not recover provider/API/quota/rate-limit or unrelated failures.

## Current verified deployment

Latest runtime deployment: **Deploy #235 / run `31901325402` SUCCESS**.

Runtime PR: **#176 — Slow Personality Plasticity v1**
- final tested head: `0874bb301b432201895b82465b0fd275b0bb0945`
- merge: `c5a4f7cfa84965fe656070e54663c27f3ab8796f`
- **CI #939 / run `31901212644`: SUCCESS**
- **574 passed in 80.08s**
- fresh DB init/status healthy; schema v5.

Three automatic production-copy gates initially failed before validator execution because of infrastructure-only SSH/staging connection resets: Height Lifecycle, Eating Behavior, and Sexual Anatomy/Physiology. Only those failed jobs were retried; all three actual disposable production-copy validators then succeeded. No runtime code changed for the transient failures and the full Python suite was not deliberately repeated.

Production readback after Deploy #235:
- service active/healthy;
- schema v5;
- autonomy enabled, normal mode, retry null, pending action present;
- speed **1x**;
- sim time `2025-05-07T19:44:00+00:00`;
- Darian was naturally in `self_satisfaction` in Darian's Master Suite;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram configuration/API healthy.

Natural runtime had also accumulated isolated one-day Preference Adaptation evidence for completed `read` / `use` actions; these are evidence only and are not claimed as established preferences.

No `personality_plasticity_v1:` row appeared in Deploy #235 readback. Deploy/init therefore did not fabricate personality evidence. No live personality overlay is claimed; ordinary runtime must naturally satisfy the long-horizon contract first.

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
- Do not repeatedly run the full suite.
- Do not make personality/preferences/hobbies/habits fixed forever-fields, but do not deepen them without a broader foundation reason.
- Do not permit arbitrary direct LLM disposition mutation.
- Do not infer negative preferences/personality evidence from non-selection, inactivity, or missed routines.
- Personality plasticity must remain materially slower than preference adaptation.
- No relationship-system expansion by default.
- No hostile/non-consensual combat engine, weapon lethality, universal Injury/Hazard Engine, deep weapon taxonomy, or real-world weapon instructions.
- Do not fabricate production actions/actors/casualties solely for proof.

## Next phase — Overall Workflow/Foundation Review

Perform a read-only canonical + production audit first. Candidate areas to inspect include generic action/task lifecycle, resources/inventory/state consequences, environment/world context, knowledge/familiarity, inter-character participation, event/lifecycle handling, longer-horizon progression/decay, autonomy planning/goal continuity, and any remaining profile-to-cognition/runtime integration gaps.

Treat these as audit candidates, not assumed deficiencies. Let current contracts/source/live evidence determine actual gaps, then choose the smallest number of structurally coherent implementation batches.

## Exact resume point

**Adaptive Character Disposition Foundation is COMPLETE v1: Habit Formation/Extinction, Hobby/Interest Lifecycle, Preference Adaptation, and Slow Personality Plasticity are all implemented at minimum depth. The latest runtime slice is Slow Personality Plasticity v1 through PR #176 final head `0874bb301b432201895b82465b0fd275b0bb0945`, merge `c5a4f7cfa84965fe656070e54663c27f3ab8796f`, CI #939 with 574 passed, and Deploy #235 SUCCESS. Production is healthy at schema v5, autonomy normal, retry null, pending action present, speed 1x, sim time `2025-05-07T19:44:00+00:00`; Darian was naturally in `self_satisfaction` in the Master Suite. No synthetic personality evidence was created and no live personality overlay is claimed. Resume with a read-only Overall Workflow/Foundation Review before any local-depth work.**
