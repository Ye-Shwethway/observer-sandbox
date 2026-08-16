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

- During implementation, run the smallest task-relevant tests/gates that cover the changed contracts. Do not repeatedly run the full suite while iterating.
- Use the repository full CI suite as a final code/runtime PR checkpoint, not as the default inner development loop. A second full-suite run requires a concrete reason such as a broad shared-runtime change or unresolved cross-domain regression.
- Docs-only changes do not require the full Python suite.
- Do not create extra release PRs, release-marker ceremony, deploy-authorization helpers, or duplicate compatibility gates by default.
- Disposable production-copy validation is optional. Use it only when a stateful/migration/runtime risk cannot be covered adequately by local tests and CI.
- When production-copy validation is used, reuse the existing shared helper/workflow instead of inventing new SSH/copy infrastructure.
- Runtime-affecting changes deploy through `.github/workflows/deploy.yml` after merge to `main`.
- Prefer small reversible changes and Git revert/rollback over defensive process layers.
- A new gate must have a concrete reliability benefit worth its maintenance/retry cost.

## Vertical completeness policy

Follow `docs/MINIMUM_PROFILE_UNLOCK_POLICY_V1.md`.

Current strategic priority is **vertical completeness before local depth**:

`minimum unlock all profile sections -> verify overall workflow -> deepen highest-value gaps`

- A minimum-unlocked profile section needs authoritative state, meaningful runtime influence, and persistence/presentation where relevant.
- Do not require exhaustive mechanics, deep taxonomies, or one bespoke subsystem per field during the minimum pass.
- Once a structural invariant is proven, batch equivalent fields/Skills/sections rather than creating repetitive PR/deploy cycles.
- Compatibility or skill-like fields are not automatically independent Skills or engines.
- Deferred depth is acceptable when explicitly classified; fake completeness is not.

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

## Universal character autonomy

Follow `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md` and `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`.

- Character-specific behavioral hard-coding is forbidden.
- Character-specific files/data may seed represented facts/state, not command future behavior.
- Do not add named-character autonomy prompts, bespoke daily-routine rules, destination preferences, anti-repetition counter-prompts, or behavior patches.
- Autonomous behavior must emerge from universal systems consuming profile/state, needs/physiology, time, environment, affordances, history, goals, relationships, memory/learning, and deterministic constraints.
- A new character must not require a new autonomy policy or character-specific behavior branch.
- Actor-known spatial facts belong to generic semantic Character Memory. Do not reintroduce named-character spatial-familiarity files or loader paths.

## Character memory

- Events/world state remain objective truth; memory is actor-owned knowledge/experience; retrieved memory is bounded cognition context; `action_options` remain execution authority.
- Initial character-specific factual knowledge may be represented through the shared semantic-memory seed contract, not bespoke loaders.
- Memory must not grant topology, access, possession, capability, resources or actions absent from deterministic state.
- Keep memory dynamic and inspectable; do not dump the entire store into model context.
- Do not fake future consolidation, forgetting or planning with arbitrary character-specific timers/rules.

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
