# Production Validation and Release Protocol v1

Status: ACTIVE SYSTEM CONTRACT

## Purpose

This document is the single canonical repository contract for pre-merge production-copy validation and production release. Feature work must reuse this protocol instead of inventing a new SSH / SQLite-copy / deploy sequence in each PR.

The safety invariant is:

`candidate change -> CI -> disposable production-copy validation -> all green -> merge -> deploy only when runtime-affecting -> read-only production verification`

Validation never accelerates or mutates the live production runtime.

## Authority and reusable implementation

The protocol is implemented by:

- `.github/workflows/reusable-production-copy-validation.yml` — shared GitHub Actions transport/staging/SSH wrapper;
- `scripts/validation/run_on_production_copy.py` — shared SQLite read-only backup/copy lifecycle, live fingerprint guard and validator launcher;
- feature-specific validator scripts — only domain assertions and copied-DB simulation logic.

`AGENTS.md` makes reuse mandatory. If this protocol needs to change, update the shared contract/helper/workflow first and then let feature wrappers inherit the change. Do not copy/paste and fork infrastructure logic unless a concrete invariant cannot be represented by the shared path.

## Validation lifecycle

### 1. Candidate branch

Implement the bounded feature on a branch from current canonical `main`.

### 2. CI

Run normal repository CI and focused regression tests. Unit/regression tests must not contact production or external model/Telegram services.

### 3. Disposable production-copy acceptance

When production-state compatibility or simulation behavior matters, create a thin feature workflow that calls `.github/workflows/reusable-production-copy-validation.yml`.

The reusable workflow:

1. checks out the candidate PR head;
2. configures SSH from existing repository secrets;
3. stages candidate `src/`, `config/`, and validation scripts under a unique `/tmp` directory on the VPS;
4. runs `scripts/validation/run_on_production_copy.py` using the production SQLite path only as a read-only source;
5. the helper opens production SQLite with `mode=ro`, records a deterministic live fingerprint, and uses SQLite's backup API to create a disposable temporary database;
6. it exports only the disposable DB through `OBSERVER_SANDBOX_DB` to the feature validator;
7. feature-specific simulation/mutation assertions execute against the copy;
8. the helper re-reads the live DB and fails if its fingerprint changed during validation;
9. temporary files are removed.

The acceptance result must explicitly demonstrate `production_mutated=false` (or equivalent unchanged fingerprint evidence).

### 4. Feature validator contract

A feature validator must:

- read its DB path from `OBSERVER_SANDBOX_DB`;
- treat that DB as disposable;
- use candidate source through `PYTHONPATH` rather than modifying `/opt/observer-sandbox`;
- avoid model, Telegram, HTTP, email, or other network side effects;
- avoid systemd/service operations;
- never read/write the live production SQLite path directly;
- never change live speed, pause, autonomy, pending actions, leases, cognition binding, or Creator controls;
- never fabricate production evidence when the acceptance claim requires real copied production evidence;
- print concise machine-readable evidence for the assertions it proves;
- exit non-zero on any failed invariant.

Feature validators may freely accelerate simulated time or mutate copied state when the test requires it.

## Failure handling

A failed acceptance run is a development signal, not permission to alter production.

Classify failures before changing feature behavior:

1. **shared infrastructure defect** — quoting, staging, backup, cleanup, SSH, helper contract;
2. **validator defect** — wrong evidence surface, fixture assumption, assertion bug;
3. **candidate implementation defect** — actual runtime behavior mismatch;
4. **production-data precondition absent** — required real evidence does not currently exist.

Fix categories 1–2 without changing domain constants. Tune feature/runtime behavior only for category 3 with concrete evidence. For category 4, report the missing precondition or use an already-authorized deterministic copied-state setup only when the acceptance claim does not require naturally occurring production evidence.

Do not weaken assertions merely to make a run green.

## Merge and release

### Validation/docs/tooling-only change

If the merged change cannot affect installed runtime behavior or production config/schema, merge after green CI/acceptance and do **not** trigger a production deploy merely for ceremony.

Examples:
- documentation;
- validation scripts/workflows;
- test-only tooling.

### Runtime-affecting change

After all required CI and production-copy acceptance checks are green:

1. merge the accepted feature PR to `main`;
2. deploy the accepted `main` only through the canonical `.github/workflows/deploy.yml` path — workflow dispatch or an explicit `deploy/RELEASE` marker;
3. do not create a feature-specific deploy implementation;
4. perform post-deploy verification as observation/readback, not validation mutation.

The standard deploy workflow owns application sync/install, cognition bootstrap preservation, service restart, health/status readback and Telegram connectivity check.

## Post-deploy verification

Post-deploy checks are read-only unless the Creator explicitly authorized a control mutation.

Verify only what is material to the release, commonly:

- service active/healthy;
- schema/world revision when relevant;
- configured cognition/provider binding preserved;
- Telegram connection healthy when relevant;
- exact current production speed read from live state rather than assumed;
- feature-specific read-only evidence.

Do not accelerate production, fabricate actions, directly edit progression/profile state, or generate validation Telegram traffic.

## Exemplar/batch integration

The repository's exemplar-first / batch-by-pattern rule composes with this protocol:

- first genuinely new invariant: one exemplar, focused validator, one production-copy acceptance;
- equivalent follow-ons: one bounded batch, one focused regression suite, one feature validator covering every batched item, one production-copy acceptance, one merge and one deploy when runtime-affecting.

## Updating the protocol

Change this protocol only when repeated evidence shows the shared mechanism is insufficient or unsafe.

When changing it:

1. update this document;
2. update the shared helper/workflow in the same PR;
3. add/adjust focused tests for the shared contract;
4. validate the shared path without modifying production;
5. update `AGENTS.md`/bootstrap references only if the calling contract changed.

Feature branches should then consume the updated shared mechanism rather than carrying local compatibility workarounds.
