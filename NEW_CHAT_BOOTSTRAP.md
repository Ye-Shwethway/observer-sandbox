# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then task-relevant contracts.

Core/runtime/schema/action: `docs/ARCHITECTURE.md` + `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.
Spatial: `docs/WORLD_LOCATION_NODE_MODEL.md`.
Character/profile: `docs/CHARACTER_PROFILE_SCHEMA.md`.
Telegram: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` + `docs/TELEGRAM_NOTIFICATION_POLICY.md`.
Needs/effects/training recovery: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.
Future grading: `docs/FUTURE_GRADING_SYSTEM.md`.

Authority: current Creator instruction > canonical repo > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > old chat/memory. Never conflate committed, CI-validated, deployed, DB-applied and Creator-live-UX-verified states.

## Development policy — minimum runnable expansion

Schema v4 was the deliberate one-time broad foundation refinement. Normal development now follows:

`minimum required state -> minimum behavior/query -> minimum Creator-facing surface -> focused tests -> deploy/readback -> Creator acceptance -> next slice`.

Do not pre-build large inventory, grading, memory, relationship, environment, combat, training or regional systems merely because extension sockets exist. Avoid the Simiverse-style failure mode where extensive subsystem work accumulates before runnable checkpoints.

## Production baseline

- Repo: `Ye-Shwethway/observer-sandbox`
- VPS app: `/opt/observer-sandbox`
- DB: `/var/lib/observer-sandbox/observer.sqlite3`
- systemd: `observer-sandbox`
- SQLite schema: v4
- world root: `world_observer_universe`
- estate: `loc_thorne_estate`
- world identity revision: `thorne-estate-v3.0-scoped-ids`
- Darian autonomy: enabled / normal / 1x / wake-on-demand
- Telegram: live private Creator observer; notifications default ON per authorized user

Production continues autonomously. Re-read live state whenever exact current Darian action/stats matter.

## LEGO runtime foundation

Canonical expression:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

Schema v4 provides actor-scoped runtime, first-class action definitions/instances, concurrency-safe one-universe time, richer event linkage, definition->instance sockets, effects/modifier persistence sockets and generic `located_at` semantics.

Do not perform another broad foundation rewrite unless a concrete runnable feature proves a missing invariant.

## Future grading direction — RESERVED, NOT IMPLEMENTED

The Creator wants a future universal grading/progression language similar in spirit to the earlier Simiverse concept, useful across character attributes, skills, items, locations/facilities, quests/challenges and unlock conditions.

Current decision:
- no schema v5 now;
- schema v4 is sufficient for later additive grading;
- preserve authoritative raw values/state;
- grades normally derive from a named grading scheme rather than replacing raw values;
- grading must be cross-domain and presentation-independent;
- exact tiers/thresholds/caps/unlock rules are intentionally not frozen yet;
- first grading work must be one minimum-runnable domain slice, then expand only after acceptance.

Canonical note: `docs/FUTURE_GRADING_SYSTEM.md`.

## World/location state

Current hierarchy:
`world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`.

IDs are globally scoped and path-independent. `contains` = structural hierarchy, `connected_to` = traversal, `located_at` = dynamic presence. Estate exterior remains locked/non-traversable. Later `loc_south_lake_tahoe` can be inserted above the estate without renaming existing nodes.

## P2 Telegram Observer — proven browsing path

### Estate Browser
Status: COMPLETE / LIVE UX VERIFIED.

Creator successfully navigated Universe -> Thorne Estate -> floor -> room and observed Darian through the live Estate browser.

### Item/Object Browser
Status: COMPLETE / LIVE UX VERIFIED.

Room objects open readable detail views with definition/instance awareness, capabilities, authored effects and Back-to-room navigation. Creator confirmed the live flow.

Evidence:
- CI #265 / run `31667412478` SUCCESS
- Deploy #116 / run `31667377479` SUCCESS

### Character Profile Browser
Status: COMPLETE / LIVE UX VERIFIED.

Base flow:
`Characters -> Darian -> Profile -> section -> Back`.

Base sections proven by Creator:
- Identity
- Appearance
- Body
- Attributes
- Personality
- Skills
- Preferences & Habits
- Background

Data ownership:
- canonical/static scalar profile values: `character_profile_values` + `profile_field_definitions`
- normalized skills/preferences/hobbies/habits: collection tables
- live runtime/domain state remains separate from canonical profile values
- ordinary profile filters out `private` and `intimate` fields
- no grade badges yet
- no second-character Telegram session persistence yet.

Evidence:
- profile query `2d9c43ad5d66cae0d9ff0e6d4f6c474599afa012`
- Telegram integration `0fd68b22a7d5a8b7d360dc8a617124753b5b3847`
- CI #272 / run `31668499392` SUCCESS
- Deploy #119 / run `31668483842` SUCCESS
- Creator confirmed the deployed profile navigation and values were good.

P2.2 browsing is therefore COMPLETE / LIVE UX VERIFIED. P2.3 Creator-control expansion remains later and slice-by-slice only.

## P3.1 — Minimum Systemic Training Fatigue / Recovery

Status: IMPLEMENTED / CI-VALIDATED / DEPLOYED / BOUNDED ACCEPTANCE PASSED — CREATOR RECOVERY-VIEW CHECK PENDING.

Purpose: first post-v4 proof that a richer behavior can activate one dormant ontology field and become runnable/observable without building a giant subsystem.

Live state:
- `physiology.fatigue`, `0..100`, higher = worse;
- already existed in profile ontology; now activated as simulated generic field owned by `physiology_engine`;
- default observer/runtime value is `0.0` before first persisted change;
- do not seed this value in deploy-time runtime defaults because doing so would reset accumulated production fatigue.

Deterministic tuning:
- passive fatigue recovery `-1.5/hour`;
- train `+20/hour` before passive drift -> one-hour net `+18.5`;
- rest `-7/hour` before passive drift -> one-hour net `-8.5`;
- sleep `-10/hour`, idle `-2/hour`, read `-1/hour` before passive drift;
- train options and direct validation are blocked at fatigue `>=70`;
- baseline normal morning training is not selected at fatigue `>=55`;
- high fatigue prioritizes recovery;
- action/event state changes include fatigue.

Telegram:
- Profile now has a read-only `Recovery` section;
- it displays `Systemic fatigue` from live generic fields while using the profile definition for label/metadata;
- it does not copy live fatigue into `character_profile_values`.

Explicit non-goals for P3.1:
- no strength gain;
- no hypertrophy/body progression;
- no per-muscle soreness;
- no workout programming/exercise taxonomy;
- no injury-probability system;
- no grading/tier progression;
- no general training-adaptation framework.

Implementation evidence:
- core `cd126b42833802c0f9dba9b8169d389b98464172`
- Recovery observer `5a424fe23ccb83552dcde2cca02d23050736b51f`
- default-zero refinement `a114a396112feeed6c5da37c03dfec13ba493df4`
- Profile/Recovery regression `1fb5e4a270a753a1940dc1cc2fa75c030948125e`
- docs contract `abe910280b50ea2e7ce2df87a93d42c4b52bb209`
- P3 acceptance workflow final `c1c70bfda444003cde39c4fb5b227a95e21d3674`
- CI #282 / run `31669206182` SUCCESS
- CI #284 / run `31669332087` SUCCESS
- Deploy #120 delivered the fatigue engine
- Deploy #122 / run `31669140421` delivered the latest Recovery observer source and succeeded
- P3 Training Recovery Acceptance #2 / run `31669332118` SUCCESS.

Bounded acceptance #2 used a disposable production DB copy and **zero model calls**:
- before fatigue `0.0`
- after 60m train fatigue `18.5`
- after 60m rest fatigue `10.0`
- fatigue `75` blocked train both in options and deterministic validation.

The disposable acceptance did not mutate production. Production readback at `2026-08-13T05:09:04Z` remained:
- schema v4 healthy
- autonomy enabled / normal
- paused false
- speed `1.0x`
- cognition decision calls `21`
- valid pending action id
- Darian at Master Bathroom with current action `shower`
- current production fatigue `0.0` at that readback.

## Exact resume point

**Creator checks `Characters -> Darian -> Profile -> Recovery` in Telegram and confirms `Systemic fatigue` plus Back navigation are readable. If good, mark P3.1 LIVE UX VERIFIED. Do not automatically expand the training subsystem; select the next independent minimum-runnable slice separately.**

Preserve 1x wake-on-demand production autonomy, scoped ids, locked unfinished boundaries, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules, notification preferences, profile/runtime separation, grading-as-future-derived capability and the minimum-runnable expansion policy.
