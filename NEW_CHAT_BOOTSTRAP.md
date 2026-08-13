# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one structural pattern end-to-end; once green/deployed, equivalent follow-ons should normally use one branch/PR, one focused test suite, one pre-merge disposable production-copy dry-run covering the whole batch, iterative fixes if needed, then one merge and one deploy/readback.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- systemd `observer-sandbox`
- SQLite schema v4
- world root `world_observer_universe`
- estate `loc_thorne_estate`
- world revision `thorne-estate-v3.1-food-resolution`
- Darian autonomy enabled / normal / wake-on-demand
- global speed is Creator-controlled and must be re-read live
- Gemini cognition binding preserved
- Telegram connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current action/stats/speed matter.

## Proven progression state

Strength progression v1 is the first **complete active stat-mutation exemplar**.

Chain:
`Free Weights -> effective workload -> Strength stimulus -> level/ceiling difficulty -> saturation -> recovery -> detraining -> preview -> idempotent settlement -> bounded automatic activation`.

Key semantics:
- Strength stimulus = `effective_minutes / 60` from Free Weights only.
- level factor = `clamp((effective_ceiling-current)/effective_ceiling,0,1)^2`.
- recent-stimulus saturation = `1/(1+0.3*S)` over 72 simulated hours.
- recovery = zero <=6h, ramp to full at 48h, state-quality gated, fatigue >=70 hard-block.
- detraining = 14-day grace, then slow `1-exp(-overdue_days/60)` exposure scaled by `(current/effective_ceiling)^2`.
- positive proof scale = `0.25 * stimulus * level * saturation * recovery * adaptation_rate_multiplier`.
- negative proof rate = `0.02 * integrated detraining pressure-days * level exposure * detraining/decay modifiers`.
- special modifiers remain abstract and factorized; no real-world drug dosing guidance.

## Settlement safety

- first settlement is non-mutating bootstrap and consumes pre-feature Strength stimulus evidence;
- later eligible stimulus is consumed at most once;
- positive stimulus requires >=48 simulated hours and fatigue <70;
- detraining is integrated across exact unsettled simulated time and resets at Strength-training events;
- same-boundary replay is a no-op;
- every cursor advance is audited via `strength_progression_settled`;
- actual mutation writes `character_profile_history` and six-decimal simulated Strength authority `strength-progression-settlement-v1`.

## Automatic activation

Status: **DEPLOYED / LIVE BOOTSTRAP VERIFIED**.

Activation is checked only after an action completes:
- no cursor -> bootstrap once;
- eligible recovered unconsumed Strength stimulus -> settle immediately at next action-completion boundary;
- otherwise pure detraining checkpoint at most once per 24 simulated hours when Strength-training history exists;
- short/same boundaries skip; the 2-second service poll never acts as a progression clock.

Evidence:
- settlement core PR #20 merge `d6c94c90aec354faedd42656c42d078cb5bd42a3`, CI #420, acceptance #2 `31688789743`, Deploy #146 `31688891757`;
- activation PR #21 merge `71f00e2850c9c47f0875f012fd68bb131e4b6247`, CI #425, acceptance #1 `31689247542`, release `8d8eeee737cd901dd229090ec26eba099d9350fa`, Deploy #147 `31689319524` SUCCESS;
- live service automatically created first settlement event id `161` at sim time `2025-05-02T09:23:00+00:00`, bootstrap `true`;
- Strength remained `90.0 -> 90.0`, mode/authority remained static/attribute-engine because bootstrap itself does not mutate;
- explicit verifier call then skipped as `same_or_older_boundary`, proving duplicate-bootstrap suppression;
- service remained active/healthy, schema v4, autonomy normal.

Future eligible Free Weights Strength evidence may now cause tiny decimal raw Strength gains after recovery; prolonged inactivity may cause bounded decay after the grace curve.

## Causal Need Resolution

### Food Resolution Guard v1

Status: **COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / CREATOR LIVE BEHAVIOR VERIFIED**.

The original production incident (`Inspect -> Supply Shelves` repeated under strong hunger) is fixed. Food Supply Storage contains distinct `Stored Food Provisions` with authored `eat` effects (hunger -50, energy +8, thirst +2), while `Supply Shelves` remain inspect-only. Creator subsequently confirmed live hunger resolution worked.

Evidence: PR #22 merge `6117b4b8f08ae3afc8d0db6849a7aa061a34b51f`; Food Resolution Guard Acceptance #4 `31691041378` SUCCESS; CI #435 `31691041444` SUCCESS; release `0906d3c06961482fa6c327caf9cfd8e172e51d12`; Deploy #148 `31691179483` SUCCESS.

### Causal Need Resolution v2 — thirst + hunger

Status: **COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED; CREATOR LIVE THIRST VERIFICATION PENDING**.

A second live incident showed hunger resolving while thirst remained strong (~55), followed by `Train -> Combat Mat`. v2 generalizes deterministic causal shaping to the two proven domains:
- thirst -> authored `drink` actions reducing `needs.thirst`;
- hunger -> authored `eat` actions reducing `needs.hunger`.

`needs_attention` remains the priority authority. The guard acts only when the highest-priority active need is supported; it never skips an unsupported higher-priority need. A supported need exposes only a local authored resolver or shortest-path movement toward the nearest resolver. Thus Training Hall may be a transit hop toward water, but training is not exposed while strong thirst is the active supported priority.

Reason grounding is also tightened: cognition must not claim an action resolves a physiological need when authored effects leave that need unchanged or worsen it. Stored Food Provisions therefore cannot truthfully be described as hydration because their authored thirst effect is positive.

Evidence: PR #23 merge `4a0c5d67f0ed9460fc319702fa846a676090c606`; Causal Need Resolution v2 Acceptance #11 `31692492180` SUCCESS; CI #446 `31692492232` SUCCESS; release `5763818a20277b684a688df0d15bf488dbfc49e9`; Deploy #149 `31692592830` SUCCESS.

## Other proven state

- P2.2 Browse Sandbox + profile/browser UI — LIVE UX VERIFIED.
- Runtime Speed Control + ETA observability — LIVE UX VERIFIED.
- deterministic action-duration profiles — DEPLOYED.
- Research exemplar + Monitor semantics batch — DEPLOYED.
- read-only grading: Strength exemplar + 36 compatible 0..100 Attribute fields — DEPLOYED.
- IQ, Skills and Body grading remain separate families.
- Body measurements/composition remain a separate architecture line and must not inherit flat attribute or Strength-progression logic by default.

## Exact resume point

First observe the deployed Causal Need Resolution v2 at the next relevant strong-thirst decision boundary. Once live thirst behavior is confirmed, return to Strength progression follow-up. Recommended progression decision remains:
1. **Strength Progression Observability v1** — Creator-facing read-only view of recent stimulus, recovery/eligibility, saturation, latest settlement/delta and next progression boundary, then observe/tune live behavior; or
2. select the next physical progression domain and first prove its stimulus mapping/domain semantics before batching anything.

Do not batch other stats solely because Strength settlement infrastructure now exists.
