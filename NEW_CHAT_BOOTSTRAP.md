# Observer Sandbox — New Chat Bootstrap

Status: **READY FOR NEW CHAT TRANSITION**
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one genuinely new structural invariant with a bounded exemplar; once green, batch structurally equivalent follow-ons in the same branch/PR. Preferred closeout is one focused regression suite, one disposable production-copy dry-run covering every batched case, iterative fixes if needed, one merge, one deploy/readback. Do not return to per-item PR/deploy cycles for equivalent expansion.

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

Creator live-verified the initial no-stimulus state. At that point the UI correctly showed Strength `90.000000`, no recent Strength stimulus, zero recovery realization, bootstrap settlement, inactive detraining because no qualifying Strength-stimulus history existed, and the next boundary after first qualifying Strength stimulus.

Wording polish is deployed:
- `Level adaptation factor` replaces ambiguous `Level gain factor`;
- bootstrap settlement displays `Bootstrap · no stat change`;
- no-history detraining explicitly says no qualifying Strength stimulus history yet;
- no-stimulus adaptation/next-boundary wording explicitly says qualifying Strength stimulus.

Evidence:
- Observability PR #25 merge `d291e77f4c290bc4b0487888e52a4c6063349f36`, CI #457 `31699319018` SUCCESS, Deploy #151 `31699394074` SUCCESS;
- wording polish PR #26 merge `ebf18df5cc728ea600490f4b23da6e8bc35096ef`, CI #462 `31700255690` SUCCESS, release `fb45466d61494dbe066c47a39f17a48ef240ddd3`, Deploy #152 `31700418122` SUCCESS.

Opening Recovery is read-only: it does not mutate raw Strength, consume stimulus, or write progression evidence.

## Causal physiological need resolution

Hunger v1 and Thirst v2 are **Creator live verified**.

### v3 — complete current five-need family

Status: **COMPLETE / CI VERIFIED / PRODUCTION-COPY COMPATIBILITY VERIFIED / DEPLOYED**.

Accelerated exemplar+batch pattern:
- exemplar: Energy proved low-is-bad directionality using intrinsic recovery effects;
- same-PR batch: Sleepiness + Cleanliness;
- Hunger/Thirst regressions stayed green;
- one PR and one deploy.

Priority authority:
`sleepiness -> energy -> thirst -> hunger -> cleanliness`, with critical ahead of strong.

Current behavior:
- strong Sleepiness -> causal rest/sleep; critical Sleepiness -> sleep only, routing toward Bed when necessary;
- low Energy -> causal recovery that raises Energy;
- strong Thirst -> authored drink resolver;
- strong Hunger -> authored eat resolver;
- poor Cleanliness -> authored shower resolver;
- direct object effects and intrinsic per-hour effects both count as causal evidence.

Evidence: PR #24 merge `e1e6d79479fa4d2ae837c395ec3b2fdb7391dc8f`; CI #451 `31698384623` SUCCESS; production-copy compatibility acceptance #12 `31698384587` SUCCESS; Deploy #150 `31698521410` SUCCESS.

Strict note: v3 batch-specific Energy/Sleepiness/Cleanliness cases are fully covered by CI, while the reused production-copy harness did not enumerate every new v3 case. Future equivalent batches should use one production-copy matrix covering every batched item when workflow writes are available.

## Other proven state

- Browse Sandbox/Profile — LIVE UX VERIFIED.
- Runtime Speed Control + ETA — LIVE UX VERIFIED.
- deterministic duration planning — DEPLOYED.
- Research exemplar + Monitor semantics batch — DEPLOYED.
- Attribute grading — Strength exemplar + 36 compatible 0..100 fields DEPLOYED.
- IQ, Skills, and Body remain separate grading/progression families.
- Body measurements/composition must not inherit flat Attribute or Strength-progression logic by default.

## Next proposed slice

### Strength Progression Live Cycle Validation & Tuning v1

Goal: validate the first complete real progression cycle before reusing progression infrastructure for another domain.

Required flow:
1. re-read current live runtime, Strength, fatigue/readiness, recent Strength stimulus, speed, and pending action;
2. observe or safely arrange one normal **Free Weights** session without directly editing Strength;
3. capture the emitted Strength stimulus and Recovery diagnostics immediately afterward;
4. allow simulated recovery to proceed naturally, using Creator-approved runtime speed controls if useful rather than directly editing progression state;
5. inspect diagnostics around the 6h and 48h recovery boundaries when practical;
6. verify the first eligible automatic settlement at an action-completion boundary;
7. compare observed stimulus, level adaptation factor, saturation, recovery factor, predicted scale, and actual settlement delta against the v1 formulas;
8. verify raw Strength/history/event evidence and replay/idempotency remain correct;
9. tune constants **only if observed evidence shows a concrete mismatch**; otherwise keep the formulas unchanged and mark the cycle validated.

This is primarily a validation/tuning slice, not a new progression-domain implementation. Do not add another stat domain during it. Do not fabricate stimulus or directly set Strength merely to make the test pass. Prefer a bounded accelerated observation over broad new architecture.

After this cycle is validated, propose the next physical progression domain. Its first item must still prove domain-specific stimulus mapping/recovery/decay semantics before batch expansion.

## Exact resume point

Start **Strength Progression Live Cycle Validation & Tuning v1** from current live production state. Treat newer repository and live-runtime evidence as authoritative. Keep exemplar-first/batch-by-pattern as the development default. Body measurements/composition remain a separate architecture line.
