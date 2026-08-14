# Security Policy

## Sensitive material

Do not commit API keys, Telegram bot tokens, SSH private keys, VPS credentials, `.env` / `secrets.env` files, runtime databases, or production backups.

Production credentials belong only in GitHub Actions repository secrets and the protected runtime secret file on the VPS. Pull requests must never require contributors to provide production credentials.

## GitHub Actions trust boundary

- `pull_request_target` is prohibited.
- Fork-originated pull requests are untrusted and must not reach production-copy validation, deployment, runtime-control, or other VPS-backed jobs.
- Ordinary public-fork CI receives no production repository secrets.
- Production deployment is restricted to trusted `main` pushes or an explicit trusted manual run.
- Repository `GITHUB_TOKEN` permissions should remain read-only by default; grant narrower write permissions only to a workflow that concretely needs them.

## Reporting a vulnerability

Do not publish a live credential or exploitable production detail in a public issue. Use GitHub private vulnerability reporting when it is enabled for this repository, or contact the repository owner privately.

If a credential may have been exposed, revoke/rotate it first and investigate history/log exposure second.
