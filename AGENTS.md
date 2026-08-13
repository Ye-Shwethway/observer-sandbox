# Observer Sandbox Repository Instructions

## Startup

Before material work, read `NEW_CHAT_BOOTSTRAP.md` and the directly relevant canonical docs. Newer repository and verified runtime evidence override remembered chat context.

## Authority order

1. Explicit current Creator instruction.
2. Current canonical repository contracts/config/schema.
3. Verified live runtime/database evidence.
4. Current CI/deploy evidence.
5. `NEW_CHAT_BOOTSTRAP.md`.
6. Older chat memory.

## Development workflow

Default to the shortest reliable loop:

`branch -> focused tests + CI -> merge -> automatic deploy when runtime-affecting -> read-only production check`

Follow `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`.

- Do not create extra release PRs, release-marker ceremony, deploy-authorization helpers, or duplicate compatibility gates by default.
- Disposable production-copy validation is optional. Use it only when a stateful/migration/runtime risk cannot be covered adequately by local tests and CI.
- When production-copy validation is used, reuse the existing shared helper/workflow instead of inventing new SSH/copy infrastructure.
- Runtime-affecting changes deploy through `.github/workflows/deploy.yml` after merge to `main`.
- Prefer small reversible changes and Git revert/rollback over defensive process layers.
- A new gate must have a concrete reliability benefit worth its maintenance/retry cost.

## Continuity

Update `NEW_CHAT_BOOTSTRAP.md` after material repository or verified runtime changes. Distinguish committed, tested, merged, deployed, and live-verified states.

## Composable runtime contract

Preserve the LEGO rule:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

- LLMs propose structured actions; they do not mutate arbitrary DB/world state directly.
- Universe-global state stays separate from actor scheduler/cognition state.
- Actions are first-class `action_instances` referencing data-driven definitions.
- Prefer reusable definition/effect metadata over character-specific switch logic.
- Events retain action/location/state-change linkage and participants where relevant.
- Definitions, instances, and runtime state remain distinct.

## Creator controls

Privileged direct mutations follow `docs/CREATOR_CONTROL_POLICY.md`.

- Creator controls are typed administrative interventions, not character actions.
- LLMs never receive Creator-control authority.
- Successful privileged mutations remain auditable.
- Avoid unrestricted arbitrary-field/SQL-style control surfaces.

## World model

Spatial/world changes follow `docs/WORLD_LOCATION_NODE_MODEL.md`.

- Locations are recursively nestable graph nodes.
- Entity IDs are technical identities, not display names.
- `contains` is structural containment; `connected_to` is traversable topology; `located_at` is dynamic presence.
- Locked/unimplemented boundaries have no traversable edge.
- Routing derives from relations rather than hard-coded room pairs.

## Physiology and effects

Living-needs/item-effect changes follow `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

- Recovery actions must deterministically improve their intended need after drift.
- Effects are authored data, not prompt prose.
- Cognition may see effect summaries; the deterministic engine remains authoritative.

## Telegram presentation

Creator-facing Telegram output follows `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.

- Use friendly entity names and concise sections.
- Keep canonical ISO time internal; use the approved human-readable time format in UI.
- Hide engine bookkeeping from normal history views.
- Presentation stays downstream of generic query/control services.

## Expansion policy

Use exemplar-first only when a genuinely new invariant is introduced. Once a pattern is proven, batch structurally equivalent follow-ons in one reviewable change.

Do not force a production-copy acceptance or separate deploy ceremony for every batch. Use focused tests, CI, merge, and the standard deploy unless concrete risk requires more.

## Scope discipline

Observer Sandbox is intentionally small and modular. Do not recreate EIDOLON/Simiverse-scale subsystem sprawl. Build bounded, understandable, reversible slices.
