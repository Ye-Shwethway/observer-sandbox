# Production Validation and Release Protocol v1

Status: ACTIVE SYSTEM CONTRACT

## Purpose

This is the single canonical contract for production-copy acceptance and production release. Feature work must reuse it instead of inventing new SSH, staging, SQLite-copy, or deploy mechanics per PR.

Canonical lifecycle:

`candidate -> CI -> disposable production-copy acceptance -> all green -> merge -> deploy only if runtime-affecting -> read-only production verification`

Validation never accelerates or intentionally mutates live production.

## Canonical implementation

- `.github/workflows/reusable-production-copy-validation.yml` — shared Actions transport/staging wrapper.
- `scripts/validation/production_copy.py` — canonical SQLite read-only + backup library.
- `scripts/validation/create_disposable_db_copy.py` — thin CLI adapter used by Actions.
- `scripts/validation/*.py` — feature-specific validators containing domain assertions only.
- `.github/workflows/validation-release-standardization-acceptance.yml` — acceptance exemplar for this protocol.
- `.github/workflows/deploy.yml` — only canonical production deploy implementation.
- `deploy/RELEASE` — explicit release marker when marker-driven deployment is used.

`AGENTS.md` makes reuse mandatory. If the protocol needs to change, update the shared contract/helper/workflow first and let callers inherit the change. Do not fork infrastructure logic unless a concrete invariant cannot be represented by the shared path.

## Safety model

Production is autonomous and may legitimately advance while acceptance runs. **Before/after live DB equality is therefore not a valid generic safety invariant.**

Safety is structural:

1. live SQLite is opened with URI `mode=ro`;
2. `PRAGMA query_only=ON` is also enabled;
3. SQLite backup creates a consistent writable snapshot;
4. the feature validator receives only the disposable path through `OBSERVER_SANDBOX_DB`;
5. candidate source/config is staged under a unique `/tmp` directory rather than installed over production;
6. model/API/Telegram credentials are removed from the validator environment;
7. validators perform no systemd/service or Creator-control operations;
8. the staged candidate and disposable DB are removed after the run.

Feature validators must never independently open `/var/lib/observer-sandbox/observer.sqlite3` or another live mutation surface.

`production_mutated_by_validation=false` means validation had no writable live-DB capability. It does not claim normal autonomous production state remained byte-for-byte unchanged while validation ran.

## Candidate and CI

Implement the bounded feature on a branch from current canonical `main`.

Before production-copy acceptance:

- normal CI must run;
- focused unit/regression tests must cover the changed invariant;
- unit/regression tests must not contact production, models, Telegram, or other external side-effect services.

## Disposable production-copy acceptance

When production-state compatibility or simulation behavior matters, create a thin caller workflow that invokes `.github/workflows/reusable-production-copy-validation.yml`.

The reusable workflow owns:

1. candidate checkout;
2. validator-path validation (`scripts/validation/*.py` only);
3. SSH configuration;
4. staging the complete candidate tree to a unique VPS `/tmp` directory, excluding `.git`, `.venv`, runtime-data and caches;
5. disposable DB creation through the shared helper;
6. binding `OBSERVER_SANDBOX_DB` to the copy only;
7. staged candidate `PYTHONPATH` / config binding;
8. model/API/Telegram credential stripping;
9. feature-validator execution;
10. cleanup.

This removes per-feature quoting, partial staging, ad-hoc `cp`, and repeated SSH boilerplate.

### Thin caller pattern

```yaml
jobs:
  acceptance:
    uses: ./.github/workflows/reusable-production-copy-validation.yml
    with:
      validator_path: scripts/validation/validate_example_v1.py
    secrets: inherit
```

Do not repeat SSH setup, `/tmp` staging, SQLite-copy creation, credential stripping, or cleanup in feature workflows.

### Feature validator contract

A feature validator must:

- live under `scripts/validation/`;
- read only `OBSERVER_SANDBOX_DB` as its mutable database;
- require `OBSERVER_VALIDATION_DISPOSABLE=1` when mutation/acceleration is used;
- treat that DB as disposable;
- use staged candidate source/config;
- avoid model, Telegram, HTTP, email, or other network side effects;
- avoid systemd/service and Creator-control operations;
- never read/write live production SQLite directly;
- never change live speed, pause, autonomy, pending actions, leases, cognition binding, profile/progression state, or world state;
- never fabricate production evidence when the claim requires naturally occurring copied production evidence;
- print concise machine-readable evidence;
- exit non-zero on failed invariants.

Copied state may be deterministically prepared only when explicitly part of the authorized test claim and not presented as naturally occurring production evidence.

## Failure classification

Classify failures before changing feature behavior:

1. **shared infrastructure defect** — staging, backup, cleanup, SSH, shared workflow/helper contract;
2. **validator defect** — wrong evidence surface, fixture assumption, assertion bug;
3. **candidate implementation defect** — actual runtime behavior mismatch;
4. **production-data precondition absent** — required real copied evidence does not currently exist.

Fix 1–2 without tuning domain behavior. Tune runtime behavior only for 3 with concrete evidence. For 4, report the missing precondition or use an explicitly authorized copied-state setup when appropriate.

Never weaken assertions merely to obtain green status.

## Merge and evidence status

Merge only after all required CI and production-copy acceptance checks are green. Always distinguish authored/committed, CI-validated, production-copy accepted, merged, deployed, and live-verified states.

## Deploy decision

### No deploy

Documentation, validation scripts/workflows, and test-only tooling do not require ceremonial production deployment.

### Runtime-affecting deploy

For source/config/schema/runtime changes:

1. merge accepted feature work to `main`;
2. deploy accepted `main` only through `.github/workflows/deploy.yml`;
3. use workflow dispatch or update `deploy/RELEASE` with explicit accepted evidence;
4. never create a feature-specific deploy implementation;
5. perform post-deploy readback only after standard deploy succeeds.

The standard deploy workflow owns application sync/install, DB init/migration, cognition bootstrap preservation, service restart, health/status checks, and Telegram connectivity verification.

## Release marker contract

When `deploy/RELEASE` is used, record at minimum:

- release identifier;
- exact accepted `main` SHA;
- required acceptance workflow/run identifiers;
- status `accepted-for-production`.

Never point the release marker at an unaccepted branch head. Updating it is a release action, not a validation mechanism.

## Post-deploy verification

Post-deploy checks are read-only unless the Creator explicitly authorizes a control mutation. Verify only material release evidence such as service health, schema/world revision, cognition/provider binding, Telegram connectivity, exact current speed, and feature-specific read-only state.

Never accelerate production, fabricate validation actions, directly edit progression/profile state, or generate validation-induced Telegram traffic.

## Exemplar/batch integration

- first genuinely new invariant: one exemplar + focused validator + one production-copy acceptance;
- equivalent follow-ons: one bounded batch + one regression suite + one validator covering the batch + one production-copy acceptance + one merge + one deploy if runtime-affecting.

## Updating the protocol

When repeated evidence shows this mechanism is insufficient, update this document, shared helper/workflow, focused tests, and protocol acceptance probe in the same PR. Prove the revised shared path before feature branches consume it. Do not carry feature-local infrastructure forks forward.
