# Telegram Creator AI Safe Diagnostics v1

Status: IMPLEMENTED ON TEST

Creator-facing Telegram command failures must preserve actionable exception detail instead of collapsing every failure to an exception class name.

For command-path failures the presentation contract is:

`Observer command failed safely:`
`<ExceptionClass>: <sanitized detail>`
`Cause: <safe parser cause>` when available.

The diagnostic layer may expose provider HTTP status/reason and bounded provider error text already carried by the runtime exception. It must not expose authorization headers, bearer credentials, API keys, tokens, secrets, raw traceback, or unbounded response bodies.

This is diagnostic presentation only. It does not weaken fail-closed behavior, change AI authority, bypass deterministic validation, or mutate Sandbox/canonical state.
