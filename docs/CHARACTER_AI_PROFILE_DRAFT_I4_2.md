# Character AI Profile Draft Contract I4.2

Status: IMPLEMENTED / MERGED
Date: 2026-08-19

## Problem corrected

Creator Studio AI Character generation previously used the universal creation envelope but allowed free-form Character `properties`. That produced prose keys such as `Age`, `Physical Description`, `Height Approximation` and `Personality` instead of the represented Character Profile vocabulary already used by the runtime.

That output shape was insufficient for a real Character creation workflow.

## Contract

AI Character creation now has two layers:

1. universal creation envelope: identity, properties, relationships, capabilities, provenance;
2. Character representation payload: canonical profile field keys plus structured preferences, hobbies, habits and skills.

`properties.character_profile.values` may contain only keys currently registered in `profile_field_definitions`. Unknown prose aliases are rejected rather than silently becoming alternate Character fields.

Examples of the represented vocabulary include:
- `identity.*`;
- `body.*`;
- `appearance.*`;
- `raps_pa.*`;
- `raps_ma.*`;
- `raps_ia.*`;
- `social.*`;
- `raps_sa.*`;
- `raps_vc.*`;
- `genetics.*`;
- `personality.*`;
- `background.*`.

The schema is built dynamically from the current registered profile definitions instead of maintaining a parallel hard-coded Character profile vocabulary inside Creator Studio.

## Existing-Character continuity reference

If Creator intent explicitly contains the exact name of an existing active canonical Character, Creator Creation AI may receive that Character's current canonical profile, preferences, hobbies, habits and skills as a read-only continuity reference.

This does not authorize mutation or copying into canon.

For developmental variants, the AI is instructed to preserve fixed identity/genetic/appearance continuity while inferring mutable age/training-dependent values plausibly. It must not mechanically scale adult measurements or attributes.

## Draft preview

Character AI drafts show a profile summary and expose `View Full Profile`.

The full profile is paginated in Telegram using canonical field keys so a large profile does not depend on one 4096-character message.

The generic `Properties` section no longer treats the Character profile as a prose blob.

## Sandbox materialization

Explicit `Approve into Sandbox` remains required.

On approval:
- profile values -> `creation_sandbox_profile_values`;
- skills -> `creation_sandbox_character_skills`;
- preferences -> `creation_sandbox_character_preferences`;
- hobbies -> `creation_sandbox_character_hobbies`;
- habits -> `creation_sandbox_character_habits`.

The structured `character_profile` draft payload is removed from generic object properties before sandbox object activation, avoiding duplicate sources of truth.

All these tables are sandbox-owned and cascade with the sandbox object.

## Schema

Schema version: v21.

New isolated tables:
- `creation_sandbox_character_preferences`;
- `creation_sandbox_character_hobbies`;
- `creation_sandbox_character_habits`.

No canonical Character table is used for sandbox facets.

## Authority and safety

- AI proposes only.
- Creator approval creates sandbox state only.
- Canonical Character data used for continuity is read-only.
- No transmigration occurs.
- No sandbox Character is automatically running.
- `runtime_ready != running` remains unchanged.
- The production second-Character gate remains closed.

## Acceptance

PR #296: `Generate structured Character profile drafts I4.2`.

Final head: `4bdff4f275d1974eda898f367e5503eeece86fdb`.

Merge: `12ea77588af7128bcd68912b81b8dda6e7253b3c`.

Evidence:
- CI #1092 — SUCCESS;
- Inventory Foundation v1 Acceptance #105 — SUCCESS.

Acceptance proves:
- schema v21 and sandbox facet tables;
- AI schema contains registered profile keys;
- exact-name canonical Character reference is read-only and available to the AI prompt;
- Telegram profile preview is structured/paginated;
- approval materializes profile/facet data into isolated sandbox state;
- canonical-state fingerprint is unchanged.
