# Observer Sandbox — New Chat Bootstrap

Status: **READY FOR NEW CHAT TRANSITION**
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Required task references:
- validation/release/deployment: `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`;
- Thorne Estate environment: `docs/DARIAN_MANSION_REFERENCE.md` + `docs/WORLD_LOCATION_NODE_MODEL.md`;
- character profile/progression: `docs/CHARACTER_PROFILE_SCHEMA.md`;
- Strength live-cycle evidence: `docs/STRENGTH_LIVE_CYCLE_VALIDATION_V1.md`.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Mandatory development policy

Use minimum runnable expansion plus **exemplar-first, then batch-by-pattern**. Prove one genuinely new invariant, then batch only structurally equivalent follow-ons.

All dry-run/regression/acceptance/tuning/accelerated simulation uses a disposable production DB copy. Never accelerate production for validation. Never induce validation Telegram/model side effects. Production changes only after all-green merge/deploy; post-deploy verification is read-only unless the Creator separately authorizes a control mutation.

## Validation & Release Workflow Standardization v1

Status: **COMPLETE / CANONICAL / SYSTEM-LEVEL CONTRACT / ACCEPTANCE VERIFIED**.

Canonical merge:
- PR #35;
- main merge `98844eede24ceb30eaf478f79d1bee872ad180eb`;
- post-merge CI #504 run `31711704581` SUCCESS.

Canonical mechanism:
- `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`;
- `.github/workflows/reusable-production-copy-validation.yml`;
- `scripts/validation/production_copy.py`;
- `scripts/validation/create_disposable_db_copy.py`;
- feature validators under `scripts/validation/`;
- `AGENTS.md` requires reuse instead of feature-local SSH/SQLite/deploy reinvention.

Standard path:
`candidate -> CI -> reusable disposable production-copy acceptance -> all green -> merge -> canonical deploy only if runtime-affecting -> read-only production verification`.

Safety uses capability isolation: live SQLite opens `mode=ro` + `PRAGMA query_only=ON`; SQLite backup creates a writable disposable copy; validator receives only that copy; model/Telegram credentials are omitted. Production may continue normal autonomy during acceptance, so byte-for-byte live DB equality is not a generic safety requirement.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- service `observer-sandbox`
- SQLite schema v4
- world revision `thorne-estate-v3.2-training-environment`
- Darian autonomy enabled / normal / wake-on-demand
- latest deploy readback speed: `2.0x`; Creator-controlled, so re-read whenever exact cadence matters
- Gemini cognition: `gemini-3.5-flash-lite`, preserved
- Telegram connected private Creator observer

Production continues autonomously.

## Thorne Estate canon

`docs/DARIAN_MANSION_REFERENCE.md` is the durable Creator-provided source behind the current estate environment. Current policy remains **interior-first**; exterior traversal, private lake access, outdoor tactical course and broader Tahoe traversal remain deferred runnable surfaces.

### Training Environment Expansion v1

Status: **COMPLETE / PRODUCTION-COPY ACCEPTED / DEPLOYED / LIVE READBACK VERIFIED**.

World revision: `thorne-estate-v3.2-training-environment`.

Added 12 scoped `train + inspect` objects without schema change or new progression ownership.

Training Hall:
- AI Combat Simulation System;
- Indoor Obstacle Course;
- Combat Pit;
- VR Tactical Simulator.

Top-Class Home Gym:
- Olympic Weightlifting Platform;
- Power Rack;
- Adjustable Bench;
- Strength Machine Circuit;
- High-Speed Treadmill;
- Rowing Ergometer;
- Speed & Agility Station;
- Altitude Training Chamber.

Existing Free Weights, Heavy Bag, Combat Mat and Practice Dummy remain.

Evidence:
- feature PR #36 merge `58c5ea4621c1cc920c09c998eb0fa351bc9a3279`;
- CI #512 run `31713866160` SUCCESS;
- Activity Semantics compatibility #14 run `31713866127` SUCCESS;
- Thorne Estate Training Environment v1 Acceptance #1 run `31713866507` SUCCESS;
- acceptance used the canonical reusable production-copy workflow on first run;
- copied world revision `v3.1 -> v3.2`, all 12 new objects/containment verified;
- runtime state and Darian dynamic state preserved;
- exterior boundary preserved;
- existing Drinking Water effect preserved;
- model calls `0`, Telegram calls `0`, production writable validation capability `0`;
- release PR #37 merge `15085ba84a0e5c494608e0f623029fcc36cc8134`;
- Deploy #155 run `31714205133` SUCCESS;
- production readback: healthy, schema v4, world revision v3.2, autonomy enabled/normal, Gemini binding preserved, Telegram connected.

New training objects currently reuse generic `train` workload semantics only. Strength stimulus remains deliberately exclusive to Free Weights. No Stamina, skill, or other non-Strength progression mutation was added.

## Strength progression checkpoint

Strength progression mutation flow is active and the complete live-cycle exemplar is closed.

Key chain:
`Free Weights -> effective workload -> Strength stimulus -> level/ceiling -> saturation -> recovery -> detraining -> preview -> idempotent settlement -> action-boundary activation`.

Live-cycle validation: **COMPLETE / PRODUCTION-COPY VALIDATED / NO TUNING REQUIRED**.

Evidence: PR #33 merge `02e7ddd640d727189b643092219fab95d7bb4ac0`; validation #9 `31709316031` SUCCESS; CI #491 `31709315939` SUCCESS. Real Free Weights event `202` produced `0.801` stimulus; copied first eligible settlement at `49.8h` matched formula (`+0.001614529`) and moved copied Strength `90.0 -> 90.001615` once, with replay protection intact.

`Profile -> Recovery` observability remains deployed/live verified.

## Physiological autonomy checkpoint

Hunger, thirst, energy, sleepiness, cleanliness and fatigue participate in causal resolution. Fatigue >=55 is strong; >=70 is critical and matches the hard training gate. `rest`/`sleep` resolve fatigue; deterministic inspect/use repetition guards are deployed. Telegram Character Update changes include Fatigue.

## Approved expansion direction

1. Strength full-cycle validation — COMPLETE.
2. Thorne Estate Training Environment Expansion — COMPLETE / DEPLOYED.
3. **Training Methods / Semantics Expansion — NEXT.**
4. Stamina progression exemplar.
5. Batch structurally equivalent physical attributes only after the exemplar is green.
6. Skills progression exemplar + batches.
7. Body composition/measurement progression as a separate architecture family.
8. Cognitive/social/emotional families later when meaningful action evidence exists.

Equipment and methods provide composable workload evidence; they do not own progression formulas.

## Exact resume point

Resume **Training Methods / Semantics Expansion**.

Goal: replace the currently flat generic `train` evidence surface with bounded, data-driven training-method evidence tied to equipment capabilities while preserving the generic Action model and existing Strength behavior.

First prove one new method-semantic exemplar, then batch only structurally equivalent follow-ons. Do not add Stamina/non-Strength mutation in this slice. All production-copy acceptance must use the reusable validation protocol.
