# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: **2026-08-19**

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:

`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches are `main` and `test`.

Default workflow:

`develop on test -> focused tests + final PR CI -> merge test into main -> automatic deploy when runtime-affecting -> production verification -> continuity sync -> test/main synchronization`.

Never claim production deployment without independent deploy/runtime evidence.

## Current repository checkpoint

### PR #281 — Creator Creation I0/I1 Foundation

Merged:
`c60ba00921e1a14132c4422d1e96eed2e623b2ab`

Final head:
`51ef1c5267bc8d963bbf498d3b67c17bfa7f86ab`

Evidence:
- CI #1071 — **SUCCESS**
- Skill Progression Foundation v1 Acceptance #109 — **SUCCESS**
- no schema migration.

Initial CI #1069 reached `792 passed / 2 failed`. Both failures were stale/overly literal test expectations after the approved AI Settings hierarchy change. Narrow expectation alignment produced final green CI #1071; runtime architecture did not require redesign.

I0 now provides generic Creator authority precedence and profile seed import uses it directly.

Canonical precedence:

`Creator-approved live state > simulation-derived live state > canonical seed/default`.

Ordinary seed/import/reinitialization may initialize missing or unclaimed baseline state but must not silently overwrite Creator-owned or simulated live state.

I1 now provides a shared sandbox-only creation proposal envelope with initial Character and Location sockets. Direct `target_scope = canonical` requests fail closed.

No Creation Sandbox persistence, canonical creation/transmigration, or new real character exists yet.

## AI Settings hierarchy

Canonical Telegram structure:

`Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI`.

Creator Creation AI has its own independent binding:
- scope type `engine`;
- scope id `creator_creation`;
- role `creator_creation_assist`.

Its capability probe is structured and non-mutating. The model may eventually draft Creation Sandbox proposals, but AI model configuration does not grant creation or canonical write authority.

Canonical docs:
- `docs/CREATOR_CREATION_AI_SETTINGS_V1.md`
- `docs/CREATOR_CREATION_I0_I1_ACCEPTANCE_V1.md`

## Prior completed Creator controls

### PR #278 — Creator Override Persistence & Progression Re-anchor Correctness v1

Merged:
`b50fdc9abb7670ad9e473c24901d154a3816b171`

Evidence:
- CI #1067 — SUCCESS
- Skill Progression Foundation v1 Acceptance #105 — SUCCESS.

Closed:
- Creator-controlled profile values survive ordinary seed import/reinitialize;
- Creator edits re-anchor progression so old evidence cannot replay against corrected values;
- grade-only evaluator changes do not emit false CHARACTER PROGRESSION.

### PR #279 — Body Preserve Shape Completeness v2.1

Merged:
`4a176c2d53670e0415957272ed034a1e26d70500`

Evidence:
- CI #1068 — SUCCESS
- Strength Live Cycle Validation #124 — SUCCESS.

Body Preserve Shape now propagates target-grade adjustment through represented muscular circumferences while retaining deterministic forward-grade verification and hard anchors such as height.

## Creator Staging & Transmigration architecture

Core principle:

> **Create anywhere safely; canon nowhere automatically.**

All Creator-created things — Character, Location, Quest, Job, Skill, Item, Organization, Service, world element, future system/rule descriptors and future socket types — first belong to isolated Creation Sandbox state.

Architecture:

`Creator intent -> structured proposal -> sandbox validation -> explicit sandbox approval -> isolated sandbox object -> test/revise/reroll -> target-universe validation -> transmigration preview -> explicit Creator approval -> atomic canonical activation`.

Creation Sandbox uses **shared engine, isolated state**.

Shared where appropriate:
- schemas;
- validators;
- deterministic grading/runtime helpers;
- approved universe rules.

Isolated:
- mutable entities/objects;
- events;
- autonomy membership;
- relationships;
- world graph mutations;
- notifications.

Sandbox objects may be reset, rerolled, cloned, revised, archived or deleted without affecting canon.

## Target-universe compatibility

Schema validity alone is insufficient for transmigration.

Before canonical activation, validate:
- schema and dependencies;
- references;
- target-universe ontology;
- realism/genre/rule policy;
- capabilities and runtime requirements;
- canonical conflicts;
- forbidden assumptions.

Therefore:

> **schema-valid does not imply universe-compatible.**

Example: supernatural powers or impossible-physics systems may be valid sandbox experiments but must be rejected for the current realism-constrained universe unless its policy explicitly allows them. A future fantasy universe may accept them under a different universe profile.

Transmigration must be atomic. Failure produces zero canonical writes.

Canonical architecture docs:
- `docs/UNIVERSAL_CREATION_SOCKET_FOUNDATION_V1.md`
- `docs/CREATOR_STAGING_TRANSMIGRATION_ARCHITECTURE_V1.md`
- `docs/CREATOR_CREATION_FULL_ROADMAP_V1.md`
- `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`.

## Immediate implementation route

- I0 generic Creator authority hardening — **COMPLETE / MERGED**;
- I1 universal proposal/socket core — **COMPLETE / MERGED**;
- I2 isolated Creation Sandbox persistence/lifecycle — **NEXT**;
- I3 Character + Location sandbox vertical proof;
- I4 minimum Telegram Creator Studio with Manual + AI Draft, preview/edit/reroll and explicit sandbox approval;
- I5 sandbox-specific Telegram notifications/observer surface;
- I6 target-universe compatibility/transmigration planning boundary;
- then resume MIND-F2.

Do not implement every creation type before returning to Mind. Character + Location are the first vertical proof; later sockets expand by the same registry pattern.

## Second-character gate remains closed

Do not add or transmigrate another real production character into the current universe before:
1. W0-W5/perception foundations remain healthy;
2. Creator profile/body controls remain stable;
3. minimum Creator Creation staging threshold is complete;
4. MIND-F2..F7 minimum foundations are complete;
5. Relationship Adaptation foundation is complete;
6. A3.3 interim planning scaffolding is reconciled;
7. Foundation Completion Review v2 passes;
8. Creator explicitly approves that character's canonical transmigration.

Sandbox Characters do not violate this gate because they have no canonical-universe membership.

## Mind Engine continuation

Canonical:
`docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`.

MIND-F2 remains the next Mind slice but is intentionally deferred until the minimum Creator Creation staging threshold exists.

Then:

`MIND-F2 -> F3 Attention/Appraisal/Active Concerns -> F4 Intention -> F5 Planning -> F6 Social Cognition/Communication -> F7 Relationship Adaptation -> Foundation Completion Review v2 -> next real character transmigration proposal`.

## Existing world/runtime locks

Completed external-input minimum stack remains W0-W5 plus Perception Foundation v1.

A3.3 Bounded Multi-Step Destination Intent remains deployed. Continue read-only natural observation; do not force Darian outside. When F4/F5 activate, reconcile interim route-purpose scaffolding into canonical Mind intention/planning.

Estate-first spatial scope remains active unless Creator explicitly expands it.

## Production evidence boundary

Latest independently recorded production checkpoint in continuity remains Perception Foundation v1 / Deploy #289:
- PR #269;
- CI #1054 / run `32045634180`: SUCCESS;
- merge `ebe5bb923c90c77dd878bd6e485e20d7fc68dea7`;
- Deploy #289 / run `32045825836`: SUCCESS;
- service/runtime/SQLite/Telegram/cognition recovery healthy;
- schema v15.

PRs #278/#279/#281 are repository-verified as described above. Do not invent newer deploy success until independent push-deploy/runtime evidence is available.

## Exact resume point

**PR #281 is merged at `c60ba00921e1a14132c4422d1e96eed2e623b2ab` after CI #1071 SUCCESS and Skill Progression Acceptance #109 SUCCESS. I0/I1 now provide generic Creator authority precedence, sandbox-only Character/Location proposal sockets, independent Creator Creation AI configuration/probe, and the `Creator Settings -> AI Settings` hierarchy. No sandbox persistence or canonical creation exists yet. Next authorized implementation slice: I2 — isolated Creation Sandbox persistence/lifecycle. Do not add another canonical character.**