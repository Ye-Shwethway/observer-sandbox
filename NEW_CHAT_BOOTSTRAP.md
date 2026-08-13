# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one structural invariant, then batch equivalent follow-ons in the same branch/PR. Preferred closeout is one disposable production-copy batch dry-run, iterative fixes if needed, one merge, one deploy/readback. Avoid per-item PR/deploy cycles for structurally identical expansion.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- systemd `observer-sandbox`
- SQLite schema v4
- world revision `thorne-estate-v3.1-food-resolution`
- Darian autonomy enabled / normal / wake-on-demand
- global speed is Creator-controlled and must be re-read live
- Gemini cognition preserved
- Telegram connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current action/stats/speed matter.

## Strength progression v1

First complete active stat-mutation exemplar.

Chain:
`Free Weights -> effective workload -> Strength stimulus -> level/ceiling difficulty -> saturation -> recovery -> detraining -> preview -> idempotent settlement -> automatic action-boundary activation`.

Key semantics:
- Strength stimulus = `effective_minutes / 60` from Free Weights only;
- level factor = `clamp((effective_ceiling-current)/effective_ceiling,0,1)^2`;
- saturation = `1/(1+0.3*S)` over 72 simulated hours;
- recovery: zero <=6h, ramp to full at 48h, fatigue >=70 hard-block;
- detraining: 14-day grace then slow asymptotic decay pressure;
- six-decimal raw mutation, audited settlement events, consumed-stimulus replay protection;
- first live settlement was bootstrap-only and preserved Strength 90.

## Causal physiological need resolution

Hunger v1 and Thirst v2 are **Creator live verified**.

### v3 — complete current five-need family

Status: **COMPLETE / CI VERIFIED / PRODUCTION-COPY COMPATIBILITY VERIFIED / DEPLOYED**.

Accelerated development pattern used:
- exemplar: **Energy** proved low-is-bad directionality using intrinsic recovery effects;
- same-PR batch: **Sleepiness + Cleanliness**;
- Hunger/Thirst regressions stayed green;
- one PR and one deploy.

Priority authority remains:
`sleepiness -> energy -> thirst -> hunger -> cleanliness`, with critical ahead of strong.

Current behavior:
- strong Sleepiness -> causal rest/sleep; critical Sleepiness -> sleep only, routing toward Bed when necessary;
- low Energy -> causal recovery that raises Energy;
- strong Thirst -> authored drink resolver;
- strong Hunger -> authored eat resolver;
- poor Cleanliness -> authored shower resolver, routing toward Shower;
- both direct object effects and intrinsic per-hour action effects count as causal evidence;
- no second need-scoring system is introduced.

Evidence:
- PR #24 merge `e1e6d79479fa4d2ae837c395ec3b2fdb7391dc8f`;
- CI #451 `31698384623` SUCCESS;
- existing disposable production-copy Causal Need Resolution compatibility acceptance #12 `31698384587` SUCCESS;
- release `ab60e3d1f95100324bcaa638299eef1ba32e5036`;
- Deploy #150 `31698521410` SUCCESS.

Strict note: the existing production-copy acceptance harness exercised the deployed causal-resolution path on a live DB copy but did not enumerate every new v3 Energy/Sleepiness/Cleanliness matrix case. Those batch-specific cases are covered by full CI. Future equivalent batches should prefer a single production-copy matrix harness covering every batched case when the workflow write path is available.

## Other proven state

- Browse Sandbox/Profile — LIVE UX VERIFIED.
- Runtime Speed Control + ETA — LIVE UX VERIFIED.
- deterministic duration planning — DEPLOYED.
- Research exemplar + Monitor batch — DEPLOYED.
- Attribute grading — Strength exemplar + 36 compatible 0..100 fields DEPLOYED.
- IQ, Skills, and Body remain separate grading/progression families.
- Body measurements/composition must not inherit flat attribute or Strength progression logic by default.

## Exact resume point

**Strength Progression Observability v1**.

Before adding another progression domain, expose recent Strength stimulus, recovery/eligibility, saturation, level factor, latest settlement/delta, detraining/grace state, and next progression boundary in a Creator-facing read-only view. Observe/tune the live exemplar before reusing progression infrastructure elsewhere.
