# Development and Release Protocol

Status: ACTIVE MINIMAL CONTRACT

## Default workflow

Use the shortest reliable path:

`branch -> CI/tests -> merge to main -> automatic deploy -> read-only production check`

Do not add release ceremony unless a concrete failure mode requires it.

## Before merge

- Run the normal CI/test suite.
- Add focused tests for the behavior being changed.
- Review the diff and obvious production impact before merging.
- Use a disposable production DB copy only when the change is genuinely state-sensitive, migration-heavy, or otherwise risky enough that local tests are not sufficient.

Production-copy validation is optional infrastructure, not a mandatory gate for every feature.

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
