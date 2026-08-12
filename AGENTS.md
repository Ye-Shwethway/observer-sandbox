# Observer Sandbox Repository Instructions

## Startup

Before making material changes, read `NEW_CHAT_BOOTSTRAP.md` and treat newer repository/runtime evidence as authoritative over remembered chat context.

Also read the directly relevant source/config files for the task. For architecture work, read `docs/ARCHITECTURE.md`; for character-profile work, inspect `config/characters/` and the profile schema modules; for deployment/runtime work, inspect `.github/workflows/` and `deploy/`.

## Continuity rule

`NEW_CHAT_BOOTSTRAP.md` is the durable cross-chat handoff and must remain synchronized with the project.

After every material repository or verified runtime change, update `NEW_CHAT_BOOTSTRAP.md` in the same work session/change set. Material changes include architecture decisions, schema changes, canonical character changes, provider/model behavior, roadmap status, deployment/runtime topology, workflow behavior, live verification state, and the next resume point.

Do not update it for trivial typo-only edits unless the edit changes a stated project fact.

Never confuse these states:

- authored/committed in GitHub;
- CI-validated;
- deployed to VPS;
- migration/schema applied to the live database;
- live-runtime verified.

The bootstrap must state the strongest level actually proven.

## Authority order

1. Explicit current Creator instruction.
2. Current canonical repository config/schema and architecture contracts.
3. Verified live VPS/runtime/database evidence.
4. Deployed repository/workflow evidence.
5. Current CI/test evidence.
6. `NEW_CHAT_BOOTSTRAP.md`.
7. Older handoffs or chat/model memory.

Chat/model memory is context only and must not override newer repository or live evidence.

## Scope discipline

Observer Sandbox is intentionally small and modular. Do not reproduce EIDOLON/Simiverse-scale orchestration or subsystem sprawl unless the Creator explicitly asks for it. Prefer bounded, testable increments with stable extension points.
