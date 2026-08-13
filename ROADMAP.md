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
- Privileged direct interventions follow `docs/CREATOR_CONTROL_POLICY.md`.
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

Avoid speculative subsystem construction. Existing schema-v4 sockets are extension points, not instructions to pre-build inventory, memory, relationships, weather, combat, grading, Creator-control or other engines before a concrete runnable slice needs them.

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

The current Profile Browser shows authoritative raw values without speculative grade badges. Future grading should attach without restructuring that browser.

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

Status: CORE OBSERVER/BROWSING PATH LIVE / P2.3 EXPANDS SLICE-BY-SLICE

### P2.1 — Mobile Observer MVP

Status: LIVE

Private role-aware bot, status/watch/history/character/home/control commands, polished presentation, persistent default-ON notification preferences and successful action-completion push implementation.

### P2.2 — Browse the Sandbox

Status: COMPLETE / LIVE UX VERIFIED

P2.2 was delivered as a sequence of independent runnable checkpoints.

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

Status: COMPLETE / LIVE UX VERIFIED

Implemented minimum scope:
- Characters -> Darian current-state view exposes a separate Profile entry;
- Profile opens a read-only section menu generated from represented profile data;
- initial sections: Identity, Appearance, Body, Attributes, Personality, Skills, Preferences & Habits, Background;
- scalar profile values come from `character_profile_values` joined to `profile_field_definitions`;
- skills/preferences/hobbies/habits come from their normalized profile collection tables;
- `private` and `intimate` sensitivity fields are excluded from this ordinary profile browser at the query layer;
- current runtime state remains distinct from profile truth;
- values are rendered human-readably, including height and common units;
- no grade badges are shown yet; future grading remains a separate derived layer;
- no second-character selection/session persistence is added while Darian remains the only production autonomous character.

Acceptance evidence:
- profile read-query contract commit `2d9c43ad5d66cae0d9ff0e6d4f6c474599afa012`;
- Telegram profile presentation commit `db9f8702fc812a81f447f74d6e9e21d91b8419d5`;
- Telegram integration commit `0fd68b22a7d5a8b7d360dc8a617124753b5b3847`;
- focused browser tests commit `d926687d443bc6e5e841ef3c06d1a293d82ca71a`;
- CI #272 / run `31668499392` SUCCESS;
- Deploy #119 / run `31668483842` SUCCESS;
- Creator browsed the deployed profile sections and confirmed the UI/navigation was good.

P3 may extend this proven browser with narrow live-state sections when a concrete behavior needs them. Such an extension does not reopen the base P2.2 acceptance.

### P2.3 — Creator Control Expansion

Status: FIRST SLICE IMPLEMENTED / CI-VALIDATED / DEPLOYED / PRODUCTION MUTATION VERIFIED — TELEGRAM UI CHECK PENDING

P2.3 remains slice-by-slice only. Do not implement a broad admin console.

#### P2.3.1 — Restore Basic Stats

Purpose: provide one safe Creator-authority intervention when slow real-time recovery makes live observation/development impractical.

Implemented minimum scope:
- reusable actor-scoped `restore_basic_stats()` backend;
- restores Energy `75`, Hunger `20`, Thirst `15`, Sleepiness `15`, Cleanliness `80`, Fatigue `0`;
- preserves simulation time, location, profile canon, autonomy enabled state and autonomy mode;
- cancels stale pending action, clears lease/retry and sets wake reason `creator_basic_stats_restored` so cognition can re-evaluate;
- normal field ownership remains with the needs/physiology/living engines; Creator authority authorizes the intervention rather than becoming permanent field authority;
- appends a `creator_basic_stats_restored` audit event with before/after/state changes/request source;
- CLI: `sandboxctl creator restore-basic-stats --character <id>`;
- Telegram owner-only `/restorestats [character_id]`;
- Telegram owner-only `🩺 Restore Basic Stats` button with explicit confirmation screen;
- allowed users neither receive the button nor pass server-side mutation authorization;
- guarded `.github/workflows/creator-control.yml` uses the same backend; its initial push automatically restored production once and persisted a marker so later workflow edits do not accidentally reapply it.

Evidence:
- backend `89cb9f4b37726a7a6bdda9770ec252fbaa3e12ca`;
- CLI `e35fb37fd45f9bc81af6943c59da5c64153a256c`;
- Telegram `583141d9f20849dac69671de5972960eed27e9c3`;
- focused tests `a4f825838ce93ed28ac5b95794d630dccc29854b`;
- engine-ownership/lease refinement `ceae7247abcbe0a40fe65602e1bb3f970028a73c`;
- CI #292 / run `31670662395` SUCCESS;
- Deploy #126 / run `31670662394` SUCCESS;
- workflow `d6ce3328f2a3b5b8314dd9e74054ab9681a6ff0f`;
- Creator Control #1 / run `31670700838` SUCCESS.

Live production restore evidence from `2026-08-13T05:33:26Z`:
- before: Energy `39.498`, Hunger `29.081`, Thirst `35.835`, Sleepiness `35.335`, Cleanliness `100.0`, Fatigue `0.0`, action `rest`;
- after: Energy `75.0`, Hunger `20.0`, Thirst `15.0`, Sleepiness `15.0`, Cleanliness `80.0`, Fatigue `0.0`, action `idle`;
- location remained Master Bathroom;
- sim time remained `2025-05-01T14:50:00+00:00`;
- pending rest action `9d11373e-b3cd-4425-b3e2-3152687ca1bb` was cancelled;
- autonomy remained enabled/normal, unpaused, `1x`.

Canonical contract: `docs/CREATOR_CONTROL_POLICY.md`.

Future potential slices remain owner user management, provider/model browsing/rebinding, richer runtime/history controls and notification categories. Each must be independently runnable and useful.

## P3 — First Richer Simulation Vertical Slice

Status: FIRST SLICE COMPLETE / LIVE UX VERIFIED

### P3.1 — Minimum Systemic Training Fatigue / Recovery

This is the first post-v4 proof of the minimum-runnable expansion pattern. It activates one already-reserved profile-domain field rather than building a broad training subsystem.

Implemented behavior:
- `physiology.fatigue` is live simulated state on `0..100`, higher is worse;
- passive time reduces fatigue by `1.5/hour`;
- training adds `20/hour` before passive drift (net `+18.5` for a one-hour training action);
- rest reduces fatigue by `7/hour` before passive drift (net `-8.5` for a one-hour rest action);
- sleep, idle and read also provide small/strong recovery according to `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`;
- `train` is removed from action options and rejected by deterministic validation at fatigue `>=70`;
- baseline morning training is not elected at fatigue `>=55`, and high fatigue prioritizes recovery;
- fatigue changes are included in first-class action/event state changes;
- the Telegram Profile gains a read-only `Recovery` section showing current `Systemic fatigue` without copying the live value into canonical profile tables.

Explicitly deferred:
- strength/proficiency gains;
- hypertrophy/body progression;
- muscle-group soreness;
- workout programming/exercise taxonomy;
- injury probability;
- grading/tier progression;
- a general training-adaptation framework.

Implementation/evidence:
- core simulation commit `cd126b42833802c0f9dba9b8169d389b98464172`;
- Recovery observer commit `5a424fe23ccb83552dcde2cca02d23050736b51f`;
- default-zero Recovery refinement `a114a396112feeed6c5da37c03dfec13ba493df4`;
- focused training/recovery tests `86b36a722da19460fe7d09d38911b36de103eb6e` plus follow-up coverage;
- Profile Browser Recovery integration regression `1fb5e4a270a753a1940dc1cc2fa75c030948125e`;
- CI #282 / run `31669206182` SUCCESS after aligning the Profile Browser contract;
- CI #284 / run `31669332087` SUCCESS for the final acceptance-workflow revision;
- Deploy #120 delivered the fatigue engine; Deploy #122 / run `31669140421` delivered the latest Recovery observer source and completed successfully;
- P3 Training Recovery Acceptance #2 / run `31669332118` SUCCESS on a disposable production DB copy with **zero model calls**;
- bounded acceptance proved fatigue `0.0 -> 18.5` after 60m training, then `18.5 -> 10.0` after 60m rest, and proved fatigue `75` blocks training in both option generation and validation;
- the acceptance copy did not mutate production;
- Creator opened the deployed Recovery section and confirmed `Systemic fatigue` and navigation were good.

Do not automatically expand P3.1 into a full training system. Select the next minimum runnable slice separately.

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

**P3.1 is COMPLETE / LIVE UX VERIFIED. P2.3.1 Restore Basic Stats is implemented, deployed and already used successfully against production. Creator should test the Telegram owner flow `Characters -> Darian -> 🩺 Restore Basic Stats -> confirmation`. Because the production restore has already been applied once, confirming again would intentionally perform another restore; backing out after checking the confirmation screen is sufficient to validate the UI without changing state again. If the UI is good, mark P2.3.1 LIVE UX VERIFIED and select the next independent minimum-runnable slice.**

No additional core/schema refinement is required. Preserve 1x wake-on-demand production autonomy, globally scoped ids, locked unfinished boundaries, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules, profile/runtime separation, grading-as-future-derived capability, typed/audited Creator-control authority and per-user notification preferences.
