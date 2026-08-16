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

Persistent repository branches are **only `main` and `test`**.

Default to the shortest reliable loop:

`develop on test -> focused tests + final CI/PR -> merge test into main -> automatic deploy when runtime-affecting -> read-only production check -> sync test to final main checkpoint when needed`

Do **not** create per-slice `agent/*` branches in normal development. A temporary branch is allowed only for a genuinely exceptional isolation need explicitly approved by the Creator, and it must be deleted immediately after merge/closure.

Follow `docs/PRODUCTION_VALIDATION_AND_RELEASE_PROTOCOL.md`.

- During implementation, run the smallest task-relevant tests/gates that cover the changed contracts. Do not repeatedly run the full suite while iterating.
- Use the repository full CI suite as a final code/runtime PR checkpoint, not as the default inner development loop. A second full-suite run requires a concrete reason such as a broad shared-runtime change or unresolved cross-domain regression.
- Docs-only changes do not require the full Python suite.
- Do not create extra release PRs, release-marker ceremony, deploy-authorization helpers, or duplicate compatibility gates by default.
- Disposable production-copy validation is optional. Use it only when a stateful/migration/runtime risk cannot be covered adequately by tests and CI.
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

Follow `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`, `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`, `docs/HUMAN_MEMORY_DYNAMICS_V1.md`, and `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

- Character-specific behavioral hard-coding is forbidden.
- Character-specific files/data may seed represented facts/state, not command future behavior.
- Do not add named-character autonomy prompts, bespoke daily-routine rules, destination preferences, anti-repetition counter-prompts, or behavior patches.
- Autonomous behavior must emerge from universal systems consuming profile/state, needs/physiology, time, environment, affordances, history, goals, relationships, memory/learning, mental state and deterministic constraints.
- A new character must not require a new autonomy policy or character-specific behavior branch.
- Actor-known spatial facts belong to generic semantic Character Memory. Do not reintroduce named-character spatial-familiarity files or loader paths.

## Character memory

- Events/world state remain objective truth; memory is actor-owned knowledge/experience; retrieved memory is bounded cognition context; `action_options` remain execution authority.
- Initial character-specific factual knowledge may be represented through the shared semantic-memory seed contract, not bespoke loaders.
- Memory must not grant topology, access, possession, capability, resources or actions absent from deterministic state.
- Keep memory dynamic and inspectable; do not dump the entire store into model context.
- Preserve `stored memory != currently recallable memory`.

## Intelligent Mind Engine — mandatory alignment

`docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md` is the canonical integration contract for character mental cognition.

**Before implementing any future subsystem that can materially affect character perception, interpretation, thought, affect, active concerns, goals, intentions, planning, social cognition, communication or relationship appraisal, read and align with the Mind Engine contract first.**

This includes future weather/environment appraisal, economy/money concerns, media/information exposure, communication, scheduling/obligations and social systems when they feed character cognition.

Preserve:

`world truth != perception != memory != mind state/thought != intention/plan != action proposal != action authority`

- Do not create competing hidden mind/planner/thought stores when the state belongs to the Mind Engine.
- Integrate through bounded typed input/output sockets; do not dump all world/memory/history into every model call.
- Mental artifacts may influence cognition but never bypass deterministic action validation.
- Thought is not automatically memory; prospective thought is not automatically intention or plan.
- External facts should flow through represented exposure/perception and character-relative appraisal rather than direct arbitrary behavior modifiers.
- Future social dialogue should use perception/interpretation/social-cognition stages rather than direct chatbot ping-pong or arbitrary utterance-to-relationship mutations.
- Avoid a giant monolithic mind module. Add bounded modules against the shared schema/contracts.

## World stimulus / exposure — mandatory world-input alignment

`docs/WORLD_STIMULUS_EXPOSURE_FOUNDATION_V1.md` is the canonical contract for externally available signals that may feed character cognition.

**Before implementing weather/environment, media/information, money/economy notices, communication delivery, obligations/reminders, devices or other world-side cognition inputs, read and align with both the World Stimulus/Exposure contract and the Mind Engine contract.**

Preserve:

`world/event truth != stimulus availability != character exposure != perception/interpretation != appraisal/thought != memory != action authority`

- A world fact must not become character knowledge merely because it exists.
- Stimulus eligibility queries do not automatically record exposure.
- Exposure means a signal reached the actor boundary; it does not prove understanding, belief, importance, durable memory or behavioral change.
- Do not inject every active world stimulus into cognition.
- World-input producers must document authoritative source truth, stimulus creation, scope, exposure proof, perception handoff and retirement/expiry.
- Phones, televisions, computers, internet access, radios and similar channels are represented world entities/resources when their possession, location, access or capabilities matter. Add them when a concrete world-input consumer needs them; do not treat them as magical omniscient channels.
- Do not create parallel weather/media/message exposure stores when the common W0 contract fits.

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
- **Observability parity is part of vertical completeness.** When a new subsystem introduces authoritative state that is meaningfully useful to the Creator and a relevant Telegram observer surface exists, the same bounded slice must expose that state there or explicitly document why Telegram presentation is not relevant yet. Do not leave Creator-useful state implemented but invisible by default.
- Route presentation by represented entity semantics rather than creating one giant dashboard: character-owned state belongs on character/owner views, location/property state on location views, and object/item state on object or inventory detail views. Cross-domain summaries are additive, not substitutes for entity-local detail.
- Telegram remains read-only for observer presentation. Displaying a value must not create exposure, cognition, memory, economic mutations, or other simulation side effects.
- Access/sensitivity rules remain authoritative. Observability parity never means exposing private or intimate state to a role that is not permitted to see it.

## Expansion policy

Use exemplar-first only when a genuinely new invariant is introduced. Once a pattern is proven, batch structurally equivalent follow-ons in one reviewable change.

Add world elements such as devices, network access, accounts, calendars or communication endpoints when an active feature actually needs them. Expand the represented world in the same bounded slice rather than inventing unrepresented affordances in cognition.

Do not force a production-copy acceptance or separate deploy ceremony for every batch. Use focused tests, CI, merge, and the standard deploy unless concrete risk requires more.

## Scope discipline

Observer Sandbox is intentionally small and modular. Do not recreate EIDOLON/Simiverse-scale subsystem sprawl. Build bounded, understandable, reversible slices.
