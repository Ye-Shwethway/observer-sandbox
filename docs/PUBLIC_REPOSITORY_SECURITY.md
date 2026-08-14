# Public Repository Security

Status: **CANONICAL OPERATIONAL SECURITY CONTRACT**
Synchronized: 2026-08-14

## Purpose

Observer Sandbox may be published as a public GitHub repository so standard GitHub-hosted Actions runners can be used without private-repository minute consumption. Publication is allowed only while production credentials and privileged workflows remain outside the public trust boundary.

GitHub documents that standard GitHub-hosted runners are free and unlimited for public repositories. GitHub also documents that making a repository public exposes the code plus existing Actions history/logs and disables push rulesets, so repository protection must be re-verified immediately after the visibility change.

Official references:
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository

## Credential boundary

Secrets must never be repository content.

Production credentials are stored only as GitHub Actions repository secrets and, after deployment, in `/var/lib/observer-sandbox/secrets.env` on the VPS with mode `0600`.

Sensitive values include at minimum:
- `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`;
- Gemini, Groq, NanoGPT, OpenAI and OpenRouter API keys;
- Telegram bot token;
- any future password/private key/token that authorizes external access.

The repository ignores `.env`, `secrets.env`, common private-key files, SQLite/runtime databases and backups. Runtime databases are never repository artifacts.

## Full-history publication gate

`scripts/validation/validate_public_readiness_security.py` scans the complete reachable Git history, not only the current tree. The audit checks high-confidence credential/token signatures, risky secret filenames and public-workflow hazards without printing potential secret values.

The validation workflow checks out with `fetch-depth: 0`. Publication is blocked if the audit finds a credential-shaped value or prohibited workflow construct. A finding requires investigation and credential rotation before publication; deleting the current file alone is not sufficient if a live secret existed in history.

GitHub secret-scanning alerts remain an additional defense and should be enabled/verified after publication. They do not replace this repository-owned gate.

## Public-fork trust boundary

Fork-originated pull requests are untrusted.

Rules:
- `pull_request_target` is prohibited;
- production repository secrets are never intentionally exposed to fork PRs;
- reusable production-copy validation has an explicit same-repository guard for `pull_request` events;
- external fork PRs may run ordinary non-secret CI only after the repository's configured contributor approval policy;
- deployment/runtime-control/manual VPS workflows remain trusted-owner/write-access operations;
- no pull-request code from a fork is executed in a job that has VPS credentials.

The explicit fork guard is defense in depth on top of GitHub's default behavior of withholding repository secrets from fork-originated pull requests.

## GitHub Actions permissions

Repository Actions settings should use **Read repository contents and packages permissions** as the default `GITHUB_TOKEN` policy. Individual workflows may request a narrower required write permission only when a concrete operation needs it.

Security-sensitive workflows should declare `permissions: contents: read` when they do not need repository writes.

## Visibility-change checklist

Before changing visibility:
1. merge the Public Readiness Hardening slice;
2. require the full-history Public Readiness Security Audit to pass;
3. confirm no live credential is stored in repository content;
4. confirm production-copy validation has the fork guard;
5. confirm deploy/runtime credentials still exist only in GitHub Actions Secrets.

Immediately after changing Private -> Public:
1. verify repository visibility reports Public;
2. Settings -> Actions -> General: keep default workflow token read-only;
3. set fork pull-request workflow approval to require approval for all outside contributors when available;
4. enable/verify Secret scanning and Push protection;
5. re-enable/recreate `main` branch/ruleset protections because GitHub disables push rulesets on private-to-public visibility change;
6. ensure direct pushes/force pushes to `main` are blocked according to the project policy;
7. run one ordinary CI workflow and verify it uses a standard GitHub-hosted runner;
8. re-check Actions billing/usage after the public run to confirm private included minutes are no longer being consumed by that standard-runner job.

## Existing Actions history

GitHub states that Actions history and logs become public when repository visibility changes to public. Current deploy workflows pass secrets through the GitHub `secrets` context and do not intentionally print their values. Exact secret values are masked by GitHub when recognized, but logs should never be treated as a secret store.

Operational status, simulated state and non-secret infrastructure topology may appear in historical logs and are accepted as public project information under the Creator's current publication decision. A live credential finding is not accepted.

## Scope boundary

This hardening does not make arbitrary unreviewed workflow changes safe. Any future workflow that adds elevated permissions, `pull_request_target`, third-party privileged code, new secret-bearing PR behavior, or a new deployment channel must be reviewed against this contract.
