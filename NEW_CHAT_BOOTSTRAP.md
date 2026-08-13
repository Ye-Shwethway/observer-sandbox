# Observer Sandbox — New Chat Bootstrap

Status: **READY FOR NEW CHAT TRANSITION**
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

For Thorne Estate world/environment work, also read `docs/DARIAN_MANSION_REFERENCE.md`. It is the canonical Creator-provided mansion reference behind the current estate environment.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one genuinely new structural invariant with a bounded exemplar; once green, batch structurally equivalent follow-ons in the same branch/PR. Preferred closeout is one focused regression suite, one disposable production-copy dry-run covering every batched case, iterative fixes if needed, one merge, one deploy/readback. Do not return to per-item PR/deploy cycles for equivalent expansion.

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

`docs/DARIAN_MANSION_REFERENCE.md` now preserves the finalized Creator-provided Darian's Mansion / Thorne Estate source that the current estate environment is based on.

Current world policy is **interior-first**. The existing estate structure is valid but intentionally incomplete relative to the mansion reference. Training Hall and Top-Class Home Gym enrichment is now an approved near-term expansion after the Strength live-cycle validation closes. Exterior estate traversal, private lake access, outdoor tactical obstacle course and broader Tahoe traversal remain deferred runnable surfaces even though they are canonical mansion facts.

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
- first live settlement was bootstrap-only and preserved Strength 90.

## Strength Progression Observability v1

Status: **COMPLETE / DEPLOYED / CREATOR LIVE UX VERIFIED**.

`Profile -> Recovery` exposes read-only diagnostics:
- Strength raw at six-decimal precision;
- recent qualifying Strength stimulus over 72h;
- level adaptation factor;
- saturation yield;
- recovery realization and adaptation status;
- latest settlement delta/time;
- detraining/grace status;
- next progression boundary.

Opening Recovery is read-only: it does not mutate raw Strength, consume stimulus, or write progression evidence.

## Causal physiological need resolution

Hunger, thirst, energy, sleepiness, cleanliness and fatigue now participate in causal resolution. Fatigue is a first-class recovery need: >=55 is strong, >=70 is critical and matches the hard training gate. `rest`/`sleep` resolve fatigue, while high-fatigue cognition cannot substitute training-adjacent inspect/use loops for recovery.

Current authored priority is:
`sleepiness -> energy -> fatigue -> thirst -> hunger -> cleanliness`, with critical needs ahead of strong needs.

Creator live evidence after deployment confirmed Darian selected recovery and a Rest completion notification showed fatigue decreasing from 70.8 to 66.5. Telegram `CHARACTER UPDATE -> Changes` now includes Fatigue deltas.

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

1. **Strength Progression Live Cycle Validation & Tuning v1** — close the existing progression exemplar using disposable production-copy validation only.
2. **Thorne Estate Interior / Training Environment Expansion** — enrich the mansion interior, especially the Training Hall and Top-Class Home Gym, using `docs/DARIAN_MANSION_REFERENCE.md`; use exemplar-first then batch-by-pattern.
3. **Training Methods / Semantics Expansion** — expand beyond a flat generic `train` surface into richer method evidence while still avoiding new non-Strength stat mutation.
4. **Character Simulation Unlock Expansion** — begin with a Stamina progression exemplar, then batch only structurally equivalent physical attributes; follow with skills, body composition/measurements, and later cognitive/social/emotional families.

Environment/equipment expansion must not own attribute progression formulas. Equipment and training methods provide composable action/workload evidence; domain engines decide domain-specific stimulus, recovery, decay and mutation.

## Next slice — Strength Progression Live Cycle Validation & Tuning v1

Goal: validate the first complete real progression cycle before reusing progression infrastructure for another domain.

Required flow:
1. re-read current live runtime, Strength, fatigue/readiness, recent Strength stimulus, speed, and pending action without mutation;
2. copy the current production DB to a disposable validation DB;
3. use real copied Free Weights completion/stimulus evidence where available; do not fabricate Strength stimulus or directly set Strength;
4. inspect copied Recovery diagnostics immediately after qualifying stimulus;
5. let recovery proceed through ordinary action semantics on the disposable copy; accelerated simulation is permitted only on the copy;
6. inspect the <=6h, 6..48h and >=48h recovery boundaries when practical;
7. verify the first eligible automatic settlement only at an action-completion boundary;
8. compare actual stimulus, level adaptation factor, saturation, recovery factor and settlement delta against the v1 formulas;
9. verify raw Strength/history/event evidence, consumed IDs, duplicate-credit suppression and same-boundary idempotency;
10. tune constants only if concrete evidence shows a mismatch; otherwise preserve formulas and mark the cycle validated;
11. after all-green merge/deploy, perform read-only production health/runtime readback only.

Production runtime acceleration, direct progression edits, fabricated stimulus and validation-induced Telegram activity are prohibited.

## Exact resume point

Start **Strength Progression Live Cycle Validation & Tuning v1** under the disposable production-copy validation policy. After it closes, do **Thorne Estate interior/training-environment enrichment**, then **training-method semantics expansion**, then begin **Stamina as the next progression exemplar** before physical-attribute batch expansion.
