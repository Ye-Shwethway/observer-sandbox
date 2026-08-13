# Observer Sandbox — New Chat Bootstrap

Status: **READY FOR NEW CHAT TRANSITION**
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

For Thorne Estate world/environment work, also read `docs/DARIAN_MANSION_REFERENCE.md`. It is the canonical Creator-provided mansion reference behind the current estate environment.

For Strength progression validation evidence, read `docs/STRENGTH_LIVE_CYCLE_VALIDATION_V1.md`.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one genuinely new structural invariant with a bounded exemplar; once green, batch structurally equivalent follow-ons in the same branch/PR. Preferred closeout is one focused regression suite, one disposable production-copy dry-run covering every batched case, iterative fixes if needed, one merge, one deploy/readback.

All dry-run, unit/regression/acceptance, tuning and accelerated simulation must use a disposable copy of the production DB. Production is reserved for all-green merge/deploy and read-only post-deploy verification. Never accelerate production for validation and never induce validation Telegram traffic from the live runtime.

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

## Thorne Estate canonical environment reference

`docs/DARIAN_MANSION_REFERENCE.md` preserves the finalized Creator-provided Darian's Mansion / Thorne Estate source that the current estate environment is based on.

Current world policy is **interior-first**. The existing estate structure is valid but intentionally incomplete relative to the mansion reference. The approved next implementation phase is Training Hall / Top-Class Home Gym and directly related interior equipment enrichment. Exterior estate traversal, private lake access, outdoor tactical obstacle course and broader Tahoe traversal remain deferred runnable surfaces even though they are canonical mansion facts.

## Strength progression v1 — active mutation exemplar

Chain:
`Free Weights -> effective workload -> Strength stimulus -> level/ceiling difficulty -> saturation -> recovery -> detraining -> preview -> idempotent settlement -> automatic action-boundary activation`.

Key semantics:
- Strength stimulus = `effective_minutes / 60` from Free Weights only;
- level factor = `clamp((effective_ceiling-current)/effective_ceiling,0,1)^2`;
- saturation = `1/(1+0.3*S)` over 72 simulated hours;
- recovery: zero <=6h, ramp to full at 48h, state-quality gated, fatigue >=70 hard-block;
- detraining: 14-day grace then slow asymptotic decay pressure;
- six-decimal raw mutation, audited settlement events, consumed-stimulus replay protection;
- first production settlement was bootstrap-only and preserved Strength 90.

### Strength Progression Live Cycle Validation v1

Status: **COMPLETE / PRODUCTION-COPY VALIDATED / NO TUNING REQUIRED**.

Clean validation evidence:
- PR #33 merged as `02e7ddd640d727189b643092219fab95d7bb4ac0`;
- Strength Live Cycle Validation v1 #9 run `31709316031` SUCCESS;
- CI #491 run `31709315939` SUCCESS;
- production opened read-only; SQLite backup API created the disposable validation copy;
- real unconsumed Free Weights Strength stimulus event `202` at `2025-05-02T12:36:00+00:00`;
- effective training `48.06` min -> stimulus `0.801`;
- copied first eligible settlement at stimulus age `49.8h`;
- level factor `0.01`, saturation `0.806256551`, recovery factor `1.0`;
- expected gain about `0.0016145287433775`, recorded `+0.001614529`;
- copied raw Strength `90.0 -> 90.001615`;
- event `202` consumed once, same-boundary replay skipped, history authority correct;
- `model_calls=0`, `telegram_calls=0`, `production_mutated=false`;
- no progression constants or formulas changed.

The validation runner and workflow are canonical at:
- `scripts/strength_live_cycle_validation_v1.py`;
- `.github/workflows/strength-live-cycle-validation-v1.yml`.

## Strength Progression Observability v1

Status: **COMPLETE / DEPLOYED / CREATOR LIVE UX VERIFIED**.

`Profile -> Recovery` exposes six-decimal raw Strength, recent qualifying stimulus, level adaptation factor, saturation yield, recovery realization/status, latest settlement, detraining/grace status and next boundary. Opening Recovery is read-only.

## Causal physiological need resolution

Hunger, thirst, energy, sleepiness, cleanliness and fatigue participate in causal resolution. Fatigue >=55 is strong, >=70 is critical and matches the hard training gate. `rest`/`sleep` resolve fatigue, and high-fatigue cognition cannot substitute training-adjacent inspect/use loops for recovery.

Current authored priority:
`sleepiness -> energy -> fatigue -> thirst -> hunger -> cleanliness`, with critical needs ahead of strong needs.

Creator live evidence confirmed Darian selected recovery and Rest reduced fatigue from `70.8` to `66.5`. Telegram `CHARACTER UPDATE -> Changes` includes Fatigue deltas.

## Other proven state

- Browse Sandbox/Profile — LIVE UX VERIFIED.
- Runtime Speed Control + ETA — LIVE UX VERIFIED.
- deterministic duration planning — DEPLOYED.
- Research exemplar + Monitor semantics batch — DEPLOYED.
- Attribute grading — Strength exemplar + 36 compatible 0..100 fields DEPLOYED.
- IQ, Skills, and Body remain separate grading/progression families.
- Body measurements/composition must not inherit flat Attribute or Strength-progression logic by default.

## Approved expansion sequence

The Creator approved this order:

1. **Strength Progression Live Cycle Validation & Tuning v1** — COMPLETE; no tuning required.
2. **Thorne Estate Interior / Training Environment Expansion** — NEXT; enrich the mansion interior, especially Training Hall and Top-Class Home Gym, against `docs/DARIAN_MANSION_REFERENCE.md`; use exemplar-first then batch-by-pattern.
3. **Training Methods / Semantics Expansion** — expand beyond a flat generic `train` surface into richer method evidence while still avoiding new non-Strength stat mutation.
4. **Character Simulation Unlock Expansion** — begin with a Stamina progression exemplar, then batch only structurally equivalent physical attributes; follow with skills, body composition/measurements, and later cognitive/social/emotional families.

Environment/equipment expansion must not own attribute progression formulas. Equipment and training methods provide composable action/workload evidence; domain engines decide domain-specific stimulus, recovery, decay and mutation.

## Exact resume point

Start **Thorne Estate Interior / Training Environment Expansion** from the canonical mansion reference and current schema-v4 world/object contracts.

First prove one equipment/content expansion exemplar, then batch structurally equivalent gym/training-hall objects in the same bounded slice. Preserve the interior-only traversal boundary. Do not add Stamina or other non-Strength attribute mutation during this environment slice.

After environment enrichment, do **Training Methods / Semantics Expansion**, then begin **Stamina Progression Exemplar** before physical-attribute batch expansion.
