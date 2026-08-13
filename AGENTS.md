# Observer Sandbox Repository Instructions

## Startup

Before making material changes, read `NEW_CHAT_BOOTSTRAP.md` and treat newer repository/runtime evidence as authoritative over remembered chat context.

Also read the directly relevant source/config files for the task. For architecture work, read `docs/ARCHITECTURE.md`; for Telegram work, read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; for living-needs, recovery, world-resource or item-effect work, read `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`; for character-profile work, inspect `config/characters/` and the profile schema modules; for deployment/runtime work, inspect `.github/workflows/` and `deploy/`.

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

## Living physiology and item-effect contract

All basic living-needs and recovery changes must preserve `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

- Recovery-labelled actions must improve the intended need after passive drift.
- Every basic physiological stat must retain a reachable restoration path.
- Food/drink/shower effects belong to authored world/item effect profiles rather than prompt prose or Telegram handlers.
- `action_options()` must expose relevant authored effects to cognition while the deterministic engine remains authoritative.
- Do not add a restorative capability without its deterministic effect definition and regression coverage.
- Because autonomy persists pending actions across restarts, world/capability/effect changes must account for currently pending plans before removing or invalidating targets.

## Telegram presentation contract

Every new or modified Creator-facing Telegram message must follow the presentation rules in `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.

Telegram output is a human-facing observer UI, not a raw log or database dump. New commands and callbacks must therefore reuse the shared formatting conventions rather than introducing one-off raw output.

At minimum:

- simulated timestamps shown to users use `dd-mm-yyyy (Day) hh:mm AM/PM` in 12-hour format;
- canonical ISO timestamps remain unchanged in storage/runtime internals;
- prefer human-readable entity names over internal ids in normal views;
- use concise sections, whitespace, icons, and restrained decoration for scanability;
- use friendly labels such as Yes/No or ON/OFF rather than raw booleans where appropriate;
- default activity/history views emphasize meaningful universe/character events and suppress engine/control bookkeeping noise;
- large datasets are sectioned or paginated instead of dumped into one message;
- presentation changes must not move business logic into Telegram handlers.

Tests for Telegram features should validate these presentation contracts where relevant.

## Scope discipline

Observer Sandbox is intentionally small and modular. Do not reproduce EIDOLON/Simiverse-scale orchestration or subsystem sprawl unless the Creator explicitly asks for it. Prefer bounded, testable increments with stable extension points.
