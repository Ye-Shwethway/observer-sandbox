# Development and Release Protocol

Status: ACTIVE MINIMAL CONTRACT

## Default workflow

Use the shortest reliable path:

`branch -> focused/impact-aware CI -> merge to main -> automatic deploy -> read-only production check`

Do not add release ceremony unless a concrete failure mode requires it.

## Before merge

- Run the smallest task-relevant tests while implementing.
- PR CI uses conservative changed-scope test selection when the changed source/config paths can be mapped safely.
- Shared core, schema/migration, CI-selector, package-config, or otherwise unmapped runtime changes automatically fall back to the full suite.
- Full-suite fallback uses pytest-xdist parallel execution and remains a valid final checkpoint; do not force the sequential full suite by default.
- Every PR CI run keeps `sandboxctl init` and `sandboxctl status` smoke checks.
- The scheduled/manual `Full Regression` workflow runs the complete parallel suite and reports the slowest tests without blocking ordinary feature delivery.
- Add focused tests for the behavior being changed.
- Review the diff and obvious production impact before merging.
- Use a disposable production DB copy only when the change is genuinely state-sensitive, migration-heavy, or otherwise risky enough that local tests and CI are not sufficient.

Production-copy validation is optional infrastructure, not a mandatory gate for every feature. Legacy disposable-copy acceptance workflows should be `workflow_dispatch`-only unless a concrete current risk justifies restoring an automatic PR gate.

## CI performance contract

The normal development feedback path must scale with the changed surface instead of total repository test count.

- `scripts/select_ci_tests.py` is the conservative impact selector.
- A confident feature-family match runs only the selected pytest files.
- Directly changed test files are always included.
- Unknown or cross-cutting runtime/config paths fail safe to the complete parallel suite.
- CI workflow/package/selector changes also force a complete parallel suite so the CI architecture proves itself before merge.
- Superseded PR CI runs are cancelled through workflow concurrency.
- Python dependency downloads use the setup-python pip cache.
- Specialized acceptance workflows should trigger only for their direct domain contracts; broad shared-helper path triggers that merely duplicate CI should be removed.

The full regression safety net is preserved; it is no longer the mandatory sequential bottleneck for every isolated PR.

## Deploy

`.github/workflows/deploy.yml` is the only normal production deploy implementation.

A push to `main` that changes runtime-relevant files automatically deploys:

- `src/**`
- `config/**`
- `pyproject.toml`
- `deploy/observer-sandbox.service`
- `.github/workflows/deploy.yml`

`workflow_dispatch` remains available for an explicit redeploy when the operator surface supports it.

There is no normal release-marker step, no second release PR, and no deploy-authorization helper.

The deploy workflow owns application sync/install, DB initialization/migration, cognition bootstrap preservation, service restart, status checks, and Telegram connectivity verification.

## After deploy

Perform a concise read-only production check of the things materially affected by the change. Do not create synthetic production actions merely to prove a deployment.

## Safety boundary

Keep the essential safety rules only:

- Do not intentionally accelerate production for testing.
- Do not directly edit live profile/progression/world state as a test fixture.
- Do not send validation-induced model or Telegram traffic unless the feature itself requires an explicitly authorized live integration test.
- Prefer Git revert/rollback when a merged change proves bad in production.

## Optional production-copy validation

The reusable production-copy workflow and SQLite backup helpers may still be used for high-risk stateful work. When used, mutate only the disposable copy and keep model/Telegram side effects disabled.

Do not create feature-specific SSH/copy/deploy frameworks. If ordinary CI plus focused tests are enough, stop there.

## Development policy

Favor forward progress and small reversible changes over defensive process layers. Every extra gate must justify its maintenance and retry cost with a concrete reliability benefit.
