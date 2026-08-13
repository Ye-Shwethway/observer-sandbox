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

Status on this branch: **IMPLEMENTED / ACCEPTANCE VERIFIED; merge PR #35 to make canonical**.

Canonical mechanism:
- `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`;
- `.github/workflows/reusable-production-copy-validation.yml`;
- `scripts/validation/production_copy.py`;
- `scripts/validation/create_disposable_db_copy.py`;
- feature validators under `scripts/validation/`;
- `AGENTS.md` requires reuse instead of feature-local SSH/SQLite/deploy reinvention.

Standard path:
`candidate -> CI -> reusable disposable production-copy acceptance -> all green -> merge -> canonical deploy only if runtime-affecting -> read-only production verification`.

Safety uses capability isolation:
- live SQLite opened with `mode=ro` + `PRAGMA query_only=ON`;
- SQLite backup API creates a writable disposable copy;
- feature validator receives only the copy through `OBSERVER_SANDBOX_DB`;
- model/Telegram credentials are omitted;
- production may continue normal autonomy during acceptance, so whole-file before/after equality is not a safety requirement.

Verified branch evidence:
- CI #498 run `31711075396` SUCCESS;
- Production Copy Protocol Acceptance #4 run `31711075572` SUCCESS;
- Validation Release Standardization Acceptance #4 run `31711075579` SUCCESS.

The earlier Strength-specific acceptance workflow is historical evidence only, not the template for new work. If the shared mechanism becomes insufficient, update the protocol/helper/workflow + self-test first rather than creating a feature-local fork.

Docs/test/validation-tooling-only changes do not need ceremonial production deployment. Runtime-affecting accepted changes deploy only through `.github/workflows/deploy.yml` by workflow dispatch or `deploy/RELEASE` marker.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- service `observer-sandbox`
- SQLite schema v4
- world revision `thorne-estate-v3.1-food-resolution`
- Darian autonomy enabled / normal / wake-on-demand
- global speed Creator-controlled; always re-read live when exact cadence matters
- Gemini cognition preserved
- Telegram connected private Creator observer

Production continues autonomously.

## Thorne Estate canon

`docs/DARIAN_MANSION_REFERENCE.md` is the durable Creator-provided source behind the current estate environment.

Current policy is **interior-first**. Training Hall / Top-Class Home Gym enrichment is approved next. Exterior traversal, private lake access, outdoor tactical course and broader Tahoe traversal remain deferred runnable surfaces even though they are canonical mansion facts.

## Strength progression checkpoint

Strength progression mutation flow is active and the complete live-cycle exemplar is closed.

Key chain:
`Free Weights -> effective workload -> Strength stimulus -> level/ceiling -> saturation -> recovery -> detraining -> preview -> idempotent settlement -> action-boundary activation`.

Live-cycle validation status: **COMPLETE / PRODUCTION-COPY VALIDATED / NO TUNING REQUIRED**.

Evidence:
- PR #33 merge `02e7ddd640d727189b643092219fab95d7bb4ac0`;
- validation #9 `31709316031` SUCCESS;
- CI #491 `31709315939` SUCCESS;
- real Free Weights stimulus event `202`: `48.06` effective min -> `0.801` units;
- first eligible copied settlement at `49.8h`;
- level factor `0.01`, saturation `0.806256551`, recovery factor `1.0`;
- expected gain `0.001614528743...`, recorded `+0.001614529`;
- copied Strength `90.0 -> 90.001615`;
- one-time consumption, correct history authority and same-boundary no-op verified;
- no formula/constants tuning required.

`Profile -> Recovery` observability remains deployed/live verified.

## Physiological autonomy checkpoint

Hunger, thirst, energy, sleepiness, cleanliness and fatigue participate in causal resolution. Fatigue >=55 is strong; >=70 is critical and matches the hard training gate. `rest`/`sleep` resolve fatigue; deterministic inspect/use repetition guards are deployed.

Creator live evidence confirmed Rest reduced fatigue from `70.8` to `66.5`. Telegram Character Update changes include Fatigue.

## Profile expansion direction

Current profile remains intentionally static-heavy. Approved direction after environment/method enrichment:
1. Stamina progression exemplar;
2. physical attribute batches only where semantics are structurally equivalent;
3. skills progression exemplar + batches;
4. body composition/measurement progression as a separate architecture family;
5. cognitive/social/emotional families later when meaningful action evidence exists.

Equipment/training methods provide workload evidence; they do not own progression formulas.

## Exact resume point

After PR #35 merges, resume **Thorne Estate Interior / Training Environment Expansion**.

Use the mansion canon + schema-v4 world/object contract. Prove one equipment/content exemplar, then batch structurally equivalent Training Hall / Top-Class Home Gym items in one bounded slice. Preserve interior-only traversal. Do not add Stamina/non-Strength mutation yet.

For its production-copy acceptance, use the new reusable validation protocol rather than creating another custom SSH/DB-copy workflow.

Then proceed to **Training Methods / Semantics Expansion**, followed by **Stamina Progression Exemplar**.
