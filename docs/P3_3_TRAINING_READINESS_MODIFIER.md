# P3.3 — Minimum Training Readiness Modifier

Status: COMPLETE / DEPLOYED / CREATOR LIVE UX VERIFICATION PENDING

## Purpose

Activate one concrete schema-v4 modifier path for training without building a universal modifier subsystem.

## Rule

Conditions continue to decide whether an action is legal. Modifiers change the magnitude/quality/cost/risk of an otherwise legal action.

For the first slice, training readiness is derived from existing authoritative live state only:

- energy
- thirst
- sleepiness
- systemic fatigue

No new canonical physiology fields are introduced.

## Readiness calculation

Each input contributes a normalized `0..1` readiness component. A comfortable baseline receives `1.0` for that component; deterioration toward the existing strong/critical or training-block thresholds reduces it toward `0.0`.

- energy: `75+ -> 1.0`, `20 or below -> 0.0`
- thirst: `25 or below -> 1.0`, `75+ -> 0.0`
- sleepiness: `25 or below -> 1.0`, `80+ -> 0.0`
- fatigue: `20 or below -> 1.0`, `70+ -> 0.0`

Overall readiness is the arithmetic mean of the four components, clamped to `0..1`.

## First real consequence

Training fatigue cost is multiplied by:

`1.0 + (1.0 - readiness) * 0.5`

Therefore:

- readiness `1.0` -> fatigue-cost multiplier `1.0x`
- readiness `0.5` -> `1.25x`
- readiness `0.0` -> `1.5x`

The existing hard training block at systemic fatigue `>=70` remains authoritative and unchanged.

The derived readiness and multiplier are persisted with action modifier/outcome evidence so observer surfaces and later slices can inspect what shaped the action without overwriting raw actor state.

Telegram Profile -> Recovery exposes the current derived `Training readiness` value alongside systemic fatigue. This remains a derived observer view, not a canonical profile/stat field.

## Explicit non-goals

- no universal cross-domain modifier resolver
- no injury/soreness model
- no stimulant/supplement model
- no nutrition adaptation engine
- no equipment/facility quality modifier
- no strength/skill progression
- no hypertrophy/body progression
- no grading/tier implementation
- no schema v5

## Acceptance and deployment evidence

P3 Training Readiness Acceptance #5 / run `31673341881` succeeded on merged candidate source against a disposable production DB copy with zero model calls.

Verified values:

- healthy inputs: energy `80`, thirst `15`, sleepiness `15`, fatigue `0`
  - readiness `1.000`
  - fatigue-cost multiplier `1.000x`
  - one-hour training fatigue after passive recovery: `18.5`
- degraded but legal inputs: energy `50`, thirst `45`, sleepiness `45`, fatigue `40`
  - readiness `0.595` / Telegram Recovery `59.5%`
  - fatigue-cost multiplier `1.202x`
  - one-hour resulting fatigue: `62.54`
- systemic fatigue `70` still blocks training deterministically.
- action-instance/outcome modifier persistence was verified.
- the disposable acceptance did not mutate production.

The acceptance harness itself was hardened during this slice so pre-deploy candidate source is exercised against a production-state copy rather than accidentally importing the older deployed package. Deterministic action lookup removed same-second ordering ambiguity.

After acceptance, `deploy/RELEASE` was advanced by commit `9b8b59b86696515829508b532558ffce1134c507` (`release accepted P3.3 to production`). Deploy Observer Sandbox #129 / run `31673382889` succeeded.

Production deploy readback verified:

- service active / healthy
- SQLite schema v4
- autonomy enabled / normal / unpaused / `1.0x`
- existing Gemini cognition binding preserved
- Telegram API connected and owner/allowed-user configuration present
- live actor state remained valid after restart.

Creator live Telegram UX verification is still pending. Do not mark this slice `LIVE UX VERIFIED` until the Creator confirms the deployed Recovery presentation is correct.
