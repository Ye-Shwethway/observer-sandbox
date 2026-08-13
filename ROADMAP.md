# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap audit: 2026-08-13 — aligned to schema v4 and minimum-runnable expansion.

## Global product principles

- Python/SQLite runtime/world state is authoritative.
- AI proposes structured cognition; it never directly mutates arbitrary world state.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Cognition remains wake-on-demand; no periodic LLM heartbeat by default.
- Core simulation follows `docs/ARCHITECTURE.md` and the LEGO rule:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- World identity/topology follows `docs/WORLD_LOCATION_NODE_MODEL.md`.
- Physiology/effects follow `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.
- Telegram presentation follows `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.
- Future cross-domain grading/progression follows `docs/FUTURE_GRADING_SYSTEM.md` when a concrete grading slice is authorized.

## Development policy — MINIMUM RUNNABLE EXPANSION

Schema v4 is the one-time broad foundation refinement. From this point forward, normal development must expand through the smallest useful runnable vertical slice.

Each new slice should normally contain only:
1. the minimum new canonical data/state required by the feature;
2. the minimum deterministic/query/runtime behavior required to make it work;
3. the minimum Creator-facing observation/control surface needed to use or inspect it;
4. focused tests and a bounded acceptance path;
5. deployment/readback when the slice affects production.

A slice is complete when that narrow feature is independently runnable/observable. Do **not** wait for a whole phase containing several future features before declaring a usable checkpoint.

Avoid speculative subsystem construction. Existing schema-v4 sockets are extension points, not instructions to pre-build inventory, memory, relationships, weather, combat, grading or other engines before a concrete runnable slice needs them.

Prefer:
`one small feature -> run -> observe -> validate -> keep -> next feature`

over:
`large documentation/schema subsystem -> many dependent features -> eventual runnable state`.

Do not repeat the schema-v4 broad-foundation pass unless a future concrete feature proves that a core invariant is actually missing.

## Core composition / schema v4 — PRE-EXPANSION GATE COMPLETE

Canonical audit: `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.

Implemented foundation:
- SQLite schema v4;
- actor-scoped autonomy/pending/lease/retry/cognition in `actor_runtime`;
- universe-global pause/speed/time/world kept separate;
- data-driven `action_definitions`;
- first-class `action_instances` with actor/place/target/participants/resources/conditions/modifiers/time/status/outcome;
- concurrent actions do not double-advance the one universe clock;
- richer event linkage with action/location/state changes/participants/causal socket;
- reusable `entity_definitions` -> concrete `entities` instance path;
- immediate effect operations add/multiply/set/clamp;
- `active_modifiers` persistence socket with timing/source/stack policy;
- generic dynamic `located_at` contract plus distinct ownership/possession semantics;
- service enumerates active actor runtimes instead of assuming Darian-only scheduling;
- action notifications resolve actual actor identity rather than hard-coding Darian.

Deferred intentionally until their feature slices: inventory quantity/depletion/durability, full active-modifier evaluation across domains, rich relationship/memory/environment engines, complex multi-party synchronization/combat and universal grading evaluation.

Acceptance evidence:
- multi-actor/concurrency/definition-instance/modifier/event tests included in CI;
- bounded schema-v4 accelerated production-copy recovery acceptance run #5 succeeded with `needs_acceptable=true` without mutating production;
- production readback showed schema 4, autonomy ON/normal, 1x and a valid actor-scoped pending action.

## Future grading / progression — RESERVED, NO SCHEMA CHANGE NOW

Observer Sandbox is expected to gain a reusable grading/progression language later for character attributes, skills, items, locations/facilities, quests/challenges, unlock requirements and other gradeable subjects.

Current decision:
- schema v4 remains sufficient; do not introduce schema v5 merely to pre-build grading;
- preserve the authoritative underlying raw value/state;
- a grade is normally a derived evaluation under a named grading scheme unless a concrete domain explicitly defines grade itself as canonical state;
- grading must remain cross-domain and presentation-independent rather than being hard-coded independently into profile, skill, item, location, quest or Telegram code;
- exact tier vocabulary, thresholds, caps and unlock rules are intentionally deferred until the first concrete grading use case;
- first implementation must be a minimum-runnable grading slice in one domain, then expand domain-by-domain only after acceptance.

P2.2.4 Profile Browser intentionally shows authoritative raw profile values without speculative grade badges. Future grading should attach without restructuring that browser.

Canonical note: `docs/FUTURE_GRADING_SYSTEM.md`.

## World / location graph

Current root: `world_observer_universe`; estate: `loc_thorne_estate`.
Spatial/resource ids are globally scoped and path-independent. `contains` is structural hierarchy, `connected_to` traversal, `located_at` dynamic presence. Future `loc_south_lake_tahoe` can be inserted above the estate; future `loc_quasi_home` can be a sibling. Estate exterior remains locked/non-traversable.

## P0 — Foundation & Remote Control

Status: COMPLETE / LIVE VERIFIED

## P0.5 — AI Provider Layer

Status: FOUNDATION COMPLETE

Dynamic provider/model catalogs and bindings are established; current Darian cognition uses the configured Gemini binding.

## P1 — Living Darian Minimum

Status: CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING PASSED

Includes wake-on-demand scheduler, validated actions, persistent state, five-stat recovery, authored item/resource effects, graph routing, accelerated disposable acceptance and schema-v4 composable runtime foundation.

## P2 — Telegram Observer

Status: ACTIVE

### P2.1 — Mobile Observer MVP

Status: LIVE

Private role-aware bot, status/watch/history/character/home/control commands, polished presentation, persistent default-ON notification preferences and successful action-completion push implementation.

### P2.2 — Browse the Sandbox

Status: IN PROGRESS

P2.2 is a sequence of **independent runnable checkpoints**, not one large acceptance bundle.

#### P2.2.1 — Observer Home + inline navigation

Status: COMPLETE / DEPLOYED

#### P2.2.2 — Location hierarchy / Thorne Estate

**P2.2.2A — Interior node foundation + scoped identity reset**
Status: COMPLETE / LIVE VERIFIED

**P2.2.2B — Minimum Telegram Estate Browser**
Status: COMPLETE / LIVE UX VERIFIED

Implemented minimum scope:
- Universe -> Thorne Estate -> floor/zone -> room through stable `loc:*` callbacks;
- room/location detail renders occupants with current action, objects, exits and recent location activity when available;
- Back follows the canonical `contains` parent and Home remains globally available;
- locked exterior is shown with a lock/unavailable presentation but is not a movement affordance;
- observer queries use the generic `located_at` resolver for current occupants and query schema-v4 event `location_id` for recent location activity;
- Telegram remains a formatting/navigation adapter; no world logic moved into handlers.

Acceptance evidence:
- CI #260 / run `31666982672` SUCCESS;
- Deploy #114 / run `31666950518` SUCCESS;
- Creator exercised the deployed Telegram navigation and confirmed it worked, including observing Darian in the Kitchen through the Estate browser.

#### P2.2.3 — Minimum Item/Object Browser

Status: COMPLETE / LIVE UX VERIFIED

Implemented minimum scope:
- room object rows are actionable `obj:*` callbacks;
- object detail shows human-readable name, concrete-instance/definition status, current location, effective capabilities and authored effects;
- definition-backed entities use `entities.definition_id -> entity_definitions` when present, while current instance-only fixtures remain valid;
- current location resolves through the generic dynamic/static location contract;
- authored effect values are rendered by action and stat, including schema-v4 add/multiply/set/clamp forms;
- Back returns to the actual containing/current room and Home remains globally available;
- no quantity, stacks, depletion, durability, inventory mutation or ownership mutation was added.

Acceptance evidence:
- object query contract commit `715a575642012c7aaef92cc26d27e8d8ba69ce8a`;
- Telegram object browser commit `b26423aa1bc67ad239eb9059042e3efe5479d41c`;
- focused browser tests commit `835f90a3bfbe13e165fa90187712ddc4da564dd7`;
- CI #265 / run `31667412478` SUCCESS;
- Deploy #116 / run `31667377479` SUCCESS;
- Creator exercised the deployed object detail/back flow in Telegram and confirmed it worked.

#### P2.2.4 — Character Profile Browser (single-character minimum)

Status: IMPLEMENTED / CI-VALIDATED / DEPLOYED — CREATOR UI ACCEPTANCE PENDING

Implemented minimum scope:
- Characters -> Darian current-state view now exposes a separate Profile entry;
- Profile opens a read-only section menu generated from represented profile data;
- first sections: Identity, Appearance, Body, Attributes, Personality, Skills, Preferences & Habits, Background;
- scalar profile values come from `character_profile_values` joined to `profile_field_definitions`;
- skills/preferences/hobbies/habits come from their normalized profile collection tables;
- `private` and `intimate` sensitivity fields are excluded from this ordinary profile browser at the query layer;
- current runtime state remains distinct from profile truth;
- values are rendered human-readably, including height and common units;
- no grade badges are shown yet; future grading remains a separate derived layer;
- no second-character selection/session persistence is added while Darian remains the only production autonomous character.

Acceptance evidence:
- future grading direction doc commit `f3cf9438aa84b68bfca230ca0392b5dd4ff3604f`;
- profile read-query contract commit `2d9c43ad5d66cae0d9ff0e6d4f6c474599afa012`;
- Telegram profile presentation commit `db9f8702fc812a81f447f74d6e9e21d91b8419d5`;
- Telegram integration commit `0fd68b22a7d5a8b7d360dc8a617124753b5b3847`;
- focused browser tests commit `d926687d443bc6e5e841ef3c06d1a293d82ca71a`;
- CI #272 / run `31668499392` SUCCESS;
- Deploy #119 / run `31668483842` SUCCESS for the Telegram integration.

Acceptance remaining for **P2.2.4 only**:
- Creator opens Darian -> Profile in Telegram;
- Creator browses several sections and confirms values/layout/back navigation are readable;
- sensitive/private fields remain absent from the normal profile browser.

### P2.3 — Creator Control Expansion

Status: LATER / SLICE-BY-SLICE ONLY

Potential slices: owner user management, provider/model browsing/rebinding, richer runtime/history controls and notification categories.

Each must be independently runnable and useful. Do not implement the full P2.3 list as one project-sized batch.

## P3 — First Richer Simulation Vertical Slice

Status: LATER

This now comes **before** broad Rich State & Memory work.

Choose exactly one bounded simulation capability when ready (for example a small training-adaptation, sleep/recovery refinement, or another concrete domain selected at that time).

Required shape:
- add only the state/definitions the chosen behavior needs;
- use existing action/event/modifier/field-authority contracts;
- make the deterministic behavior runnable;
- expose enough state/history in Telegram to observe it;
- run focused accelerated/bounded acceptance;
- keep all unrelated future-domain work deferred.

Do not create a general-purpose rich-state framework merely because schema v4 has extension sockets.

## P4 — Context / Memory / Relationship Slice When Behavior Requires It

Status: LATER

Memory, richer relationships or other contextual state are **demand-driven**, not a prerequisite mega-phase.

Implement the smallest one only when a concrete autonomous behavior or observer use case cannot be expressed well without it. A first slice may be very small (for example one event-derived memory/context mechanism or one relationship state transition) and must be runnable/observable before expansion.

No bulk memory ontology, relationship engine or background reflection loop is authorized by this roadmap entry.

## P5 — Second Production Character

Status: LATER

Quasi becomes the second full autonomous character after the single-character observer/profile surfaces are proven and after at least one post-v4 vertical feature has validated the incremental-development pattern.

Schema v4 already removes the old Darian-only scheduler blocker; therefore P5 should be a **character onboarding slice**, not another core-runtime rewrite.

Minimum runnable P5 should initially include only:
- canonical Quasi entity/profile seed required for runtime;
- actor runtime row and cognition binding/policy;
- valid initial location/state;
- independent wake-on-demand autonomy using existing scheduler/action contracts;
- Telegram Characters list gains actual selection only now that a second production character exists;
- bounded two-actor concurrency/behavior acceptance.

Defer advanced Darian–Quasi relationship simulation, synchronized group actions and shared memory until separate later slices prove they are needed.

## Later world expansion — South Lake Tahoe

Status: AFTER ESTATE/CHARACTER FOUNDATION IS PROVEN

Do not turn regional expansion into a giant world-authoring phase.

When opened, first runnable slice should only:
- add `loc_south_lake_tahoe` above/relevant to the existing estate graph;
- unlock one small external traversal path/destination;
- prove movement, location observation and return path;
- keep the rest of Tahoe frozen/unimplemented behind non-traversable boundaries.

Expand destination-by-destination afterward.

## Current resume point

**Creator should exercise P2.2.4 Character Profile Browser in Telegram: Characters -> Darian -> Profile -> several sections -> back. If the deployed read-only profile surfaces are good, close P2.2.4 before selecting the next independently runnable slice.**

No additional core/schema work is required for the current browser path. Universal grading is documented as a future additive capability, not a reason for another broad foundation pass now. Preserve 1x wake-on-demand production autonomy, globally scoped ids, locked unfinished boundaries, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules and per-user notification preferences.
