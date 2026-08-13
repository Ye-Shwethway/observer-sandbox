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
- world revision `thorne-estate-v3.0-scoped-ids`
- Darian autonomy enabled / normal / wake-on-demand
- global speed is Creator-controlled and must be re-read live
- Gemini cognition binding preserved
- Telegram connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current action/stats/speed matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation.

## Proven feature state

- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.
- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.
- Adaptation Curve v1 — COMPLETE / DEPLOYED / READ-ONLY.
- Stimulus Saturation / Diminishing Returns v1 — COMPLETE / DEPLOYED / READ-ONLY.
- Recovery Realization v1 — COMPLETE / DEPLOYED / READ-ONLY.
- Detraining / Prolonged-Untrained Decay v1 — COMPLETE / DEPLOYED / READ-ONLY.
- Adaptation Preview v1 — COMPLETE / DEPLOYED / READ-ONLY.
- Strength Progression Settlement v1 Core — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / NOT AUTOMATICALLY ACTIVE.
- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Research Action Semantics v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Activity Semantics Batch 1 (`monitor`) — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Read-Only Grading Strength Exemplar — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.

## Strength progression state

Current chain:
`Free Weights -> effective workload -> Strength stimulus -> level/ceiling difficulty -> recent-stimulus saturation -> recovery realization -> detraining pressure -> positive/negative preview -> idempotent settlement core`.

Key formulas / contracts:
- stimulus: `effective_minutes / 60`;
- level factor: `clamp((effective_ceiling-current)/effective_ceiling,0,1)^2`;
- saturation: `1/(1+0.3*recent_strength_stimulus)` over 72 sim hours;
- recovery: zero <=6h, linear to full at 48h, state-quality gated, fatigue >=70 hard-block;
- detraining: 14-day grace, then `1-exp(-overdue_days/60)`, scaled by `(current/effective_ceiling)^2`;
- preview positive proof scale: `0.25 * stimulus * level * saturation * recovery * adaptation_rate_multiplier`;
- preview negative proof rate: `0.02 * decay_pressure * preview_days * decay_rate_multiplier`.

Special modifiers stay abstract and factorized (ceiling, positive-rate, recovery, detraining-pressure, negative-rate). Do not implement real-world drug dosing/medical guidance.

## Strength settlement core

`settle_strength_progression()` exists in production but is **not service-wired**.

Safety invariants:
- first call is non-mutating bootstrap and consumes pre-feature historical Strength stimulus evidence;
- later positive stimulus is credited at most once via consumed event ids;
- positive stimulus remains pending until >=48 sim hours and fatigue <70;
- detraining is analytically integrated over the exact unsettled simulated-time interval and reset by Strength training events;
- same-boundary replay is a no-op;
- every cursor advance is `strength_progression_settled` audit evidence;
- every actual mutation writes `character_profile_history`;
- mutated Strength becomes six-decimal simulated authority `strength-progression-settlement-v1`, bounded 0..100;
- derived grade continues to read raw Strength.

Evidence: PR #20 merge `d6c94c90aec354faedd42656c42d078cb5bd42a3`; CI #420 SUCCESS; acceptance #2 `31688789743` SUCCESS on disposable live DB copy; release `028f1bf4506f2a0192a2df987d1c3cb24b8a4fe5`; Deploy #146 `31688891757` SUCCESS.

## Activation rule

Do not call settlement every tight service tick. The next slice must activate it at bounded simulation boundaries.

Preferred policy:
- bootstrap once when automatic activation first observes no settlement history;
- thereafter settle immediately when an eligible unconsumed Strength stimulus exists;
- otherwise evaluate pure detraining at most once per simulated day;
- action-completion is a suitable trigger/check boundary, but no-op event spam must remain bounded;
- automatic activation requires its own pre-merge production-copy acceptance and one production deploy/readback.

## Grading state

`raps-100-proof-v1` is derived-only for 36 explicitly opted-in compatible 0..100 Attributes fields. Body measurements remain a separate grading family; IQ and Skills remain separate scale/progression families.

## Exact resume point

Resume with **Strength Progression Automatic Activation v1**. Keep this as the first and only mutation activation exemplar. Do not batch other attributes/skills/body progression into it. The settlement core is already deployed but production Strength must remain unchanged until the activation slice is separately accepted and deployed.
