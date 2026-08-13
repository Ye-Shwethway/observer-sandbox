# Observer Sandbox — New Chat Bootstrap

Status: **READY FOR NEW CHAT TRANSITION**
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Required task references:
- validation/release/deployment: `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`;
- Thorne Estate environment: `docs/DARIAN_MANSION_REFERENCE.md` + `docs/WORLD_LOCATION_NODE_MODEL.md`;
- character profile/progression: `docs/CHARACTER_PROFILE_SCHEMA.md`;
- Strength live-cycle evidence: `docs/STRENGTH_LIVE_CYCLE_VALIDATION_V1.md`;
- training methods: `config/training_methods.v1.json` + `src/observer_sandbox/training_methods.py`.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Mandatory development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one genuinely new invariant, then batch only structurally equivalent follow-ons.

All dry-run/regression/acceptance/tuning/accelerated simulation uses a disposable production DB copy. Never accelerate production for validation. Never induce validation Telegram/model side effects. Production changes only after all-green merge/deploy; post-deploy verification is read-only unless the Creator separately authorizes a control mutation.

## Validation & Release Workflow Standardization v1

Status: **COMPLETE / CANONICAL / SYSTEM-LEVEL CONTRACT / ACCEPTANCE VERIFIED**.

Canonical merge: PR #35, main `98844eede24ceb30eaf478f79d1bee872ad180eb`, post-merge CI #504 `31711704581` SUCCESS.

Standard path:
`candidate -> CI -> reusable disposable production-copy acceptance -> all green -> merge -> canonical deploy only if runtime-affecting -> read-only production verification`.

Safety uses capability isolation: live SQLite opens `mode=ro` + `PRAGMA query_only=ON`; SQLite backup creates a writable disposable copy; validator receives only that copy; model/Telegram credentials are omitted.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- service `observer-sandbox`
- SQLite schema v4
- world revision `thorne-estate-v3.2-training-environment`
- Darian autonomy enabled / normal / wake-on-demand
- latest Deploy #156 readback speed: `3.0x`; Creator-controlled, so re-read whenever exact cadence matters
- Gemini cognition: `gemini-3.5-flash-lite`, preserved
- Telegram connected private Creator observer

Production continues autonomously.

## Thorne Estate Training Environment Expansion v1

Status: **COMPLETE / PRODUCTION-COPY ACCEPTED / DEPLOYED / LIVE READBACK VERIFIED**.

World revision remains `thorne-estate-v3.2-training-environment`. Training Hall and Top-Class Home Gym now expose the bounded richer equipment surface, while exterior/Tahoe traversal remains locked.

Evidence: feature PR #36 merge `58c5ea4621c1cc920c09c998eb0fa351bc9a3279`; acceptance #1 `31713866507` SUCCESS; release PR #37 merge `15085ba84a0e5c494608e0f623029fcc36cc8134`; Deploy #155 `31714205133` SUCCESS.

## Training Method Semantics v1

Status: **COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED / LIVE HEALTH READBACK VERIFIED**.

A versioned authored catalog `config/training_methods.v1.json` now describes all 16 current train-capable Thorne Estate targets with:
- stable method id/name;
- family;
- workload channels;
- descriptive tags.

The method layer is descriptive only. It does **not** own progression domains, stimulus weights, attribute formulas, recovery, decay, or settlement.

Cognition receives authored method metadata through `enrich_training_action_options`; the action decision schema remains unchanged. Completed `train` events are enriched with deterministic `training_method` evidence derived from target + already-proven effective training load.

Key isolation proofs:
- treadmill `steady_state_cardio` emits conditioning method evidence and no Strength stimulus;
- Free Weights emits `free_weight_strength` method evidence while preserving the existing Free Weights-only Strength stimulus mapping;
- no Stamina/non-Strength mutation was added.

Acceptance evidence:
- feature PR #38 merge `5551296b031da15587d68cb15ca8ea543c0bbbaa`;
- exact-head CI #518 `31717340539` SUCCESS;
- Training Method Semantics v1 Acceptance #2 `31717340834` SUCCESS;
- Causal Need Resolution v2 compatibility #19 `31717340427` SUCCESS;
- Fatigue Causal Recovery compatibility #8 `31717340432` SUCCESS;
- production-copy acceptance verified all 16 method targets;
- treadmill 30 planned min -> 25.44 effective min at 0.848 effectiveness, no Strength stimulus;
- Free Weights 60 planned min -> 49.26 effective min at 0.821 effectiveness, Strength mapping preserved;
- model calls `0`, Telegram calls `0`, production mutation `false`;
- release PR #39 merge `621af58217d988da62cac175d94eea76018056c7`;
- Deploy #156 `31717736989` SUCCESS;
- post-release CI #521 `31717736996` SUCCESS;
- live readback: service active/healthy, schema v4, world revision v3.2, autonomy enabled/normal, Gemini binding preserved, Telegram connected.

## Strength progression checkpoint

Strength progression mutation flow is active and the complete live-cycle exemplar is closed.

Key chain:
`Free Weights -> effective workload -> Strength stimulus -> level/ceiling -> saturation -> recovery -> detraining -> preview -> idempotent settlement -> action-boundary activation`.

Live-cycle validation: **COMPLETE / PRODUCTION-COPY VALIDATED / NO TUNING REQUIRED**.

Evidence: PR #33 merge `02e7ddd640d727189b643092219fab95d7bb4ac0`; validation #9 `31709316031` SUCCESS; CI #491 `31709315939` SUCCESS. Real Free Weights event `202` produced `0.801` stimulus; copied first eligible settlement at `49.8h` matched formula (`+0.001614529`) and moved copied Strength `90.0 -> 90.001615` once, with replay protection intact.

## Physiological autonomy checkpoint

Hunger, thirst, energy, sleepiness, cleanliness and fatigue participate in causal resolution. Fatigue >=55 is strong; >=70 is critical and matches the hard training gate. `rest`/`sleep` resolve fatigue; deterministic inspect/use repetition guards are deployed. Telegram Character Update changes include Fatigue.

## Approved expansion direction

1. Strength full-cycle validation — COMPLETE.
2. Thorne Estate Training Environment Expansion — COMPLETE / DEPLOYED.
3. Training Methods / Semantics Expansion — COMPLETE / DEPLOYED.
4. **Stamina Progression Exemplar — NEXT.**
5. Batch structurally equivalent physical attributes only after Stamina is green.
6. Skills progression exemplar + batches.
7. Body composition/measurement progression as a separate architecture family.
8. Cognitive/social/emotional families later when meaningful action evidence exists.

Equipment and methods provide composable workload evidence; they do not own progression formulas.

## Exact resume point

Resume **Stamina Progression Exemplar**.

Use the new authored training-method evidence as input, but make Stamina its own progression-family exemplar. Define and prove its own stimulus mapping, adaptation difficulty, recovery/realization and detraining semantics before activating mutation. Do not blindly inherit Strength formulas merely because both are 0..100 physical attributes.

Prefer one clear conditioning method as the first real stimulus source (for example `steady_state_cardio`) and add other conditioning methods only after structural equivalence is proven. All simulation/acceptance/tuning remains on a disposable production DB copy; production must not be accelerated or directly edited for progression validation.
