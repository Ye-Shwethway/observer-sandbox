# Telegram Cognition Context Inspector v1

Status: CANDIDATE v1

## Purpose

Give the Creator a read-only, human-readable view of the compact runtime context actually prepared for character cognition calls.

## Contract

- capture the same compact runtime context produced by `_compact_prompt_state(...)` immediately before each production cognition call;
- keep only the latest three actor-scoped injection snapshots in existing `runtime_state`;
- snapshot `1` is newest, followed by `2` and `3`;
- primary cognition and bounded corrective retry are separate real injections and are labeled separately;
- `dry_run_model_decision()` does not capture snapshots and remains mutation-free;
- Telegram exposes the inspector only to the configured owner/Creator;
- the Character page places `Cognition Context` immediately below `Profile`;
- Telegram is display-only: no context editing, replay, resend, override, model call, simulation advancement, or state mutation is reachable from the viewer;
- the renderer recursively humanizes the captured context rather than maintaining a subsystem whitelist, so future top-level or nested cognition keys appear automatically;
- a small label map improves wording for known sections while unknown keys always fall back to generic human-readable labels;
- long snapshots use a single-message pager. The viewer edits one Telegram message between pages rather than splitting a snapshot across multiple messages;
- switching between snapshots resets to page 1.

## Persistence

No schema migration. The bounded ring is stored under:

`cognition_context_snapshots_v1:<character_id>`

Each entry records capture wall time, simulation time, cognition role, injection type, configured provider/model, known action vocabulary, and the exact compact runtime context.

## Privacy

Cognition context can contain private profile or runtime material. The inspector is therefore owner-only even when ordinary Observer Telegram access is granted to additional users. Direct callback access fails closed for non-owners.

## Explicit non-goals

- no prompt editor;
- no context injection control;
- no full provider request/response transcript;
- no token accounting subsystem;
- no long-term cognition archive beyond the latest three injections;
- no Telegram-specific registry of cognition subsystems.
