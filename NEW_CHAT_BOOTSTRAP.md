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
- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Research Action Semantics v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Activity Semantics Batch 1 (`monitor`) — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Read-Only Grading Strength Exemplar — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.

## Training progression state

Current short-term chain:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology -> session stimulus evidence`.

Minimum Training Stimulus v1 is intentionally narrow:
- Free Weights train session only;
- Strength domain only;
- `stimulus_units = effective_minutes / 60`;
- persisted as `training_stimulus` in completed action outcome and matching event payload;
- Heavy Bag and all other targets emit no Strength stimulus in v1;
- raw `raps_pa.strength` and its derived grade remain unchanged;
- no accumulated stimulus, adaptation, hypertrophy/body mutation, or schema v5.

Evidence: PR #14 merge `3578de12ebc750aca397b16f01f8bd368e1af11a`; CI #393 SUCCESS; Minimum Training Stimulus Acceptance #2 `31685799302` SUCCESS against a disposable production DB copy; release `22f8a3d7776137cb72d2926caac37d1002e6d8ed`; Deploy #140 `31685928444` SUCCESS.

## Grading state

`raps-100-proof-v1` is derived-only for 36 explicitly opted-in compatible 0..100 Attributes fields. Raw values remain authoritative.

Separate grading families remain mandatory:
- IQ excluded because its scale differs;
- Skills excluded because score/progression/experience semantics may differ;
- Body measurements/composition require a **separate exemplar + batch** and must not inherit flat attribute thresholds by default.

## Time and planning state

Action duration remains integer simulated minutes with minimum 1 minute. `1 sim min @ 3600x` remains a positive `1/60` real-second due interval. Sleep remains intentionally unclamped until nap/night-sleep semantics are separated.

## Exact resume point

**Minimum Training Stimulus v1 is live.** The next bounded candidate is **Minimum Adaptation/Progression v1 — Free Weights + Strength only**.

Before any Strength mutation, explicitly define how session stimulus plus recovery/time produce adaptation, including diminishing returns and tiny deterministic raw-value changes. Do not jump directly from one session to a large attribute gain. Body grading remains a separate deferred family unless Creator explicitly redirects.
