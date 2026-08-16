# Telegram Cognition Context Inspector v1

Status: COMPLETE v1 / DEPLOYED

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

## Validation and deployment checkpoint

Runtime PR: **#187 — Telegram Cognition Context Inspector v1**

- final tested head: `b4e0248b5fbf1d4fbc65c62181b8d1bfb74dc8ff`;
- CI #950 / run `31929295850`: **SUCCESS**;
- full suite: **605 passed in 45.27s**;
- fresh DB init/status: healthy, schema v5;
- final-head automatic acceptance workflows for cognition capability awareness, eating behavior, inventory operations, research action semantics, solo regulation naturalism, and training movement contract normalization: **SUCCESS**;
- merge: `c1ee61ad335ea3fd37509e868c8b406e20d714b7`;
- Deploy #240 / run `31929343421`: **SUCCESS**.

Production readback after Deploy #240 confirmed:
- service active/healthy; schema v5;
- autonomy enabled in normal mode, retry null, pending action preserved;
- speed 1x;
- Darian remained naturally sleeping in Darian's Master Suite;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot token, API connection, owner identity and allowed-user configuration healthy.

No synthetic production cognition call was made solely to populate the new viewer. Snapshot history therefore begins to populate on the next real production cognition injection, preserving the existing simulation state.

## Explicit non-goals

- no prompt editor;
- no context injection control;
- no full provider request/response transcript;
- no token accounting subsystem;
- no long-term cognition archive beyond the latest three injections;
- no Telegram-specific registry of cognition subsystems.
