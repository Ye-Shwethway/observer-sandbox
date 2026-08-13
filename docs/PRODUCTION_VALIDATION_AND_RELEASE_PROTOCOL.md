# Production Validation and Release Protocol v2

Status: ACTIVE SYSTEM CONTRACT

## Purpose

This is the single canonical contract for production-copy acceptance and production release.

Normal runtime lifecycle:

`candidate -> CI -> disposable production-copy acceptance -> all green -> merge PR to main -> automatic canonical deploy -> read-only production verification`

A second release-marker PR is **not** part of the normal runtime release path.

## Canonical implementation

- `.github/workflows/reusable-production-copy-validation.yml` — shared production-copy acceptance transport.
- `scripts/validation/production_copy.py` and `create_disposable_db_copy.py` — read-only live SQLite backup primitive.
- `scripts/validation/*.py` — feature assertions only.
- `scripts/validation/deploy_trigger_policy.py` — executable deploy authorization policy.
- `.github/workflows/deploy.yml` — only production deploy implementation.
- `deploy/RELEASE` — exceptional/manual release fallback, not normal ceremony.

`AGENTS.md` makes these paths mandatory.

## Validation safety

Production-copy validation is structurally isolated:

1. live SQLite is opened `mode=ro` with `query_only=ON`;
2. SQLite backup creates a writable disposable snapshot;
3. feature validators receive only the copied DB via `OBSERVER_SANDBOX_DB`;
4. staged candidate source/config lives under a unique `/tmp` root;
5. model/API/Telegram credentials are stripped;
6. validators do not operate systemd, Creator controls, or production runtime state;
7. temporary candidate/copy state is cleaned after the run.

Validation may mutate or accelerate only the disposable copy. `production_mutated_by_validation=false` means the validator had no writable production capability; normal autonomous production may still advance concurrently.

## Candidate and acceptance

Implement a bounded feature on a branch from current `main`.

Before merge:

- normal CI must be green;
- focused regression tests must cover the changed invariant;
- production-state compatibility must use the reusable production-copy workflow when relevant;
- feature-specific validators belong under `scripts/validation/` and must not reimplement SSH, staging, SQLite copy, credential stripping, or cleanup.

Classify failures before changing behavior:

1. shared infrastructure defect;
2. validator/fixture defect;
3. candidate implementation defect;
4. missing production-data precondition.

Do not tune domain behavior for categories 1–2 and never weaken assertions merely to obtain green status.

## Merge contract

Merge runtime-affecting work only after all required PR checks are green. Normal repository work uses merge commits; direct runtime pushes to `main` are not a production release path.

Always distinguish authored, CI-validated, production-copy accepted, merged, deployed, and live-verified states.

## Automatic production deploy

`.github/workflows/deploy.yml` automatically runs on `main` pushes that touch runtime-affecting paths:

- `src/**`
- `config/**`
- `pyproject.toml`
- `deploy/observer-sandbox.service`

Before any production operation, the workflow calls `scripts/validation/deploy_trigger_policy.py`.

For a runtime-path push, that policy authorizes deployment only when the main push is a normal GitHub PR merge commit (`Merge pull request #...`). A direct runtime push is rejected by the deploy workflow instead of being silently released.

This means the normal successful feature path is exactly:

`accepted PR -> merge -> deploy`

There is no second release PR or marker edit.

The standard deploy workflow owns application sync/install, DB initialization/migration, cognition bootstrap preservation, service restart, health/status checks, and Telegram connectivity verification.

## Fallback release paths

Two exceptional/manual paths remain available:

- `workflow_dispatch` — explicit redeploy/current-main operation when an operator surface supports it;
- `deploy/RELEASE` — explicit marker-driven fallback.

The release marker may be used for recovery, migration from the old protocol, or another concrete exceptional need. It is not required after every accepted feature merge.

When `deploy/RELEASE` is used, record at minimum the release identifier, exact accepted main SHA, required acceptance run identifiers, and `status: accepted-for-production`.

## No-deploy changes

Documentation, tests, validation scripts/workflows, and other non-runtime tooling do not auto-deploy. Editing `.github/workflows/deploy.yml` itself also does not ceremonially deploy the application.

## Post-deploy verification

Post-deploy production verification is read-only unless the Creator separately authorizes a control mutation. Check only material release evidence: service health, schema/world revision, cognition/provider binding, Telegram connectivity, exact current speed, and relevant feature readback.

Never accelerate production, fabricate production validation actions, directly edit profile/progression state, or generate validation-induced Telegram traffic.

## Exemplar and batch policy

- genuinely new invariant: one exemplar + focused regression + one production-copy acceptance;
- structurally equivalent follow-ons: one bounded batch + one regression suite + one production-copy acceptance + one merge; runtime-affecting batch auto-deploys once after merge.

## Updating this protocol

Repeated release friction is evidence that the shared mechanism is incomplete. Update this document, the executable shared policy/workflow, and its self-test together; prove the revised path before depending on it for feature work. Do not carry feature-local infrastructure forks forward.
