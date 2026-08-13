# Current Action ETA Observability

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / CREATOR LIVE UX VERIFICATION PENDING

## Purpose

Let the Creator see when a currently pending autonomous action is expected to finish without artificially advancing universe time or waiting for the next proactive completion notification.

## Creator-facing behavior

Telegram character surfaces (`/darian`, `/watch`, and the character browser card) now combine the ordinary character summary with actor-scoped pending-action metadata and display, when an action is pending:

- friendly current action target;
- planned simulated duration;
- approximate full real wait at the recorded planning speed;
- expected simulated completion timestamp;
- approximate remaining real time derived from the action's durable `due_wall_time`.

The Runtime `/status` surface exposes the same timing block.

No pending action means no ETA is invented.

Example:

`🎬 Action     Read → Field Manual`

`⏱ Duration   10 sim min • ~10 min real @ 1x`

`⏳ Expected   01-05-2025 (Thursday) 04:30 PM`

`⌛ Remaining  ~5 min real`

This is observer presentation only. It does not change simulation time, action duration, scheduler behavior, DB schema, action validity, or cognition.

## Relation to proactive Character Update notifications

The proactive completion-notification contract remains separate and mandatory: when the normal next decision boundary succeeds, the same `CHARACTER UPDATE` push includes the newly planned next action, duration and expected update time. Current-action ETA observability adds an on-demand way to inspect that timing before the next push arrives.

## Evidence

- PR #7 merge: `17200b1468753f17f10e3951b2f2c474bef32989`.
- PR CI #344 / run `31678482152`: SUCCESS.
- Main CI #346 / run `31678671631`: SUCCESS.
- Current Action ETA Acceptance #2 / run `31678671655`: SUCCESS on candidate source + config against a disposable production DB copy; zero model calls; character and runtime ETA presentation proven; production DB unchanged.
- Release commit: `70399f872ca35960989c3257a0735eb063b26253`.
- Deploy #133 / run `31678730719`: SUCCESS.
- Post-deploy readback: service healthy, schema v4, autonomy enabled/normal/unpaused/1x, actor pending action preserved, Gemini cognition binding preserved, Telegram API connected.

The first acceptance attempt failed only because the candidate staging omitted the repository `config/` directory; no failed candidate was deployed.

## Boundary

This release does not introduce deterministic duration profiles, change action timing semantics, advance time, add new actions, or change long-term training/progression systems.
