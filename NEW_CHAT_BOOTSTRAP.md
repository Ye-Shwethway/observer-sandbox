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
- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Research Action Semantics v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Activity Semantics Batch 1 (`monitor`) — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Read-Only Grading Strength Exemplar — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.

## Grading state

`raps-100-proof-v1` is a named derived-only proof family for explicitly opted-in compatible 0..100 Attributes fields. Raw profile values remain authoritative; grade metadata is derived at query time and displayed by Telegram without profile mutation or schema v5.

Attribute Grading Batch 1 covers 36 explicit fields across Physical, Mental, Intellectual (except IQ), Social and Verbal Charisma sections. Explicit membership prevents future numeric fields from silently inheriting this scheme.

Separate grading families are mandatory where semantics differ:
- `raps_ia.iq` is excluded because its scale differs;
- Skills are excluded because score/progression/experience semantics may differ;
- Body measurements/composition are excluded and require a **separate exemplar + batch**. Do not reuse flat attribute thresholds by default; body grading may depend on units, stature/proportion context, composition and/or genetic ceilings.

Evidence: Strength exemplar PR #12 merge `d0bdabc1faaede8adb6c3e8dd29a9b5ff9ba3cb3`, acceptance `31683547092`, Deploy #138 `31683632205`; Attribute Batch PR #13 merge `76bcf7fe7225a9504909f9d939bbcdd673bac7c6`, CI #386 SUCCESS, batch acceptance `31683936844`, release `d14cae7ef88fc9e157caa5fa0b930f36aba3cf77`, Deploy #139 `31684009154` SUCCESS.

## Time and planning state

Action duration remains integer simulated minutes with minimum 1 minute. `1 sim min @ 3600x` remains a positive `1/60` real-second due interval. Sleep remains intentionally unclamped until nap/night-sleep semantics are separated.

## Exact resume point

Attribute grading is live and the body-family separation is locked. Next choose one of two bounded paths:
1. **Body grading exemplar** with its own calculation semantics, then batch compatible body fields only after that exemplar is proven; or
2. **Minimum Training Stimulus** on one target/domain, leaving body grading deferred.

Do not mix Body, IQ or Skills into the existing attribute grading family merely because their values are numeric.
