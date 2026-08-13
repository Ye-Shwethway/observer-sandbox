# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-13

## Product principles

- Python/SQLite runtime/world state is authoritative.
- AI proposes structured cognition; it never directly mutates arbitrary world state.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Cognition remains wake-on-demand; no periodic LLM heartbeat by default.
- Canonical runtime composition:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Schema v4 is the current composable foundation. Do not introduce schema v5 without a concrete missing invariant.
- Development proceeds by minimum runnable vertical slices, not subsystem-first expansion.

## Development policy — minimum runnable expansion

Each feature should normally contain only:
1. minimum new canonical/runtime state required;
2. minimum deterministic/query behavior;
3. minimum Creator-facing observation/control surface if needed;
4. focused tests;
5. disposable production-copy acceptance when runtime behavior matters;
6. deploy/readback;
7. Creator UX acceptance when a Creator-facing surface changes.

Prefer:
`one small feature -> run -> observe -> validate -> keep -> next feature`

over broad speculative subsystem construction.

## Foundation — COMPLETE

Schema v4 provides:
- universe-global runtime state separated from actor-scoped runtime;
- actor autonomy/pending/lease/retry/cognition state;
- data-driven action definitions;
- first-class action instances with place/target/participants/resources/conditions/modifiers/outcome;
- concurrency-safe one-universe simulation time;
- linked events/state changes/participants;
- entity definition -> instance sockets;
- generic immediate effects and durable active-modifier sockets;
- globally scoped spatial/resource ids and generic `located_at` semantics.

No broad foundation rewrite is currently required.

## P0 — Foundation & Remote Control

Status: COMPLETE / LIVE VERIFIED.

## P0.5 — AI Provider Layer

Status: FOUNDATION COMPLETE.

Dynamic provider/model catalogs and bindings exist. Darian currently preserves the configured Gemini cognition binding through production deploys.

## P1 — Living Darian Minimum

Status: CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING PASSED.

Wake-on-demand scheduling, validated living actions, deterministic needs/effects, graph routing, first-class actions/events, and schema-v4 actor-scoped runtime are live.

## P2 — Telegram Observer

### P2.1 — Mobile Observer MVP
Status: LIVE.

Private role-aware observer/control bot, history/status/watch/control commands, and proactive action notifications are established.

### P2.2 — Browse the Sandbox
Status: COMPLETE / LIVE UX VERIFIED.

Proven live surfaces:
- Estate/location hierarchy browsing;
- room occupant/object/recent-activity observation;
- object detail browsing with definition/instance awareness and authored effects;
- Character Profile browser with canonical/static profile data separated from live runtime state.

### P2.3 — Creator Control Expansion
Status: FIRST SLICE COMPLETE / LIVE UX VERIFIED.

#### P2.3.1 — Restore Basic Stats
Status: COMPLETE / LIVE UX VERIFIED.

Typed/audited restore control resets basic living state while preserving profile canon, simulation time, location, autonomy enabled state/mode, and domain ownership. It cancels stale pending actions, clears lease/retry state, writes an audit event, and reuses the same backend from CLI, owner-only Telegram confirmation flow, and guarded Actions workflow.

Do not expand this into arbitrary field editing or a generic admin console.

## P3 — Richer Simulation Vertical Slices

Status: P3.1–P3.4 delivered at the evidence levels below.

### P3.1 — Minimum Systemic Training Fatigue / Recovery
Status: COMPLETE / LIVE UX VERIFIED.

- activates live `physiology.fatigue` on `0..100`;
- training raises fatigue; rest/sleep/ordinary time recover it;
- fatigue `>=70` blocks training deterministically;
- normal baseline training stops being elected at fatigue `>=55`;
- Telegram Profile -> Recovery exposes live systemic fatigue.

No strength gain, hypertrophy, soreness/injury, exercise programming, or grading was added.

### P3.2 — Minimum Targeted Training Session
Status: COMPLETE / ACCEPTANCE VERIFIED.

- Home Gym Heavy Bag and Free Weights are real legal `train` targets when co-located and capability-valid;
- cognition receives legal target/action pairs from generic options;
- target persists through pending action, `action_instances.target_id`, and completion event evidence;
- Telegram/history resolves friendly target names.

Evidence includes merge `9d4b7995f9213638641db5b0cedf062b438e8b43`, main CI #302, and P3 Targeted Training Acceptance #1.

### P3.3 — Minimum Training Readiness Modifier
Status: COMPLETE / DEPLOYED / LIVE UX VERIFIED.

Canonical detail: `docs/P3_3_TRAINING_READINESS_MODIFIER.md`.

Readiness derives from existing energy, thirst, sleepiness, and systemic fatigue. It changes training fatigue cost without replacing the existing hard fatigue condition.

Reference degraded state:
- energy `50`, thirst `45`, sleepiness `45`, fatigue `40`;
- readiness `0.595`;
- fatigue-cost multiplier `1.202x`;
- resulting one-hour fatigue `62.54`.

Evidence:
- P3 Training Readiness Acceptance #5 / run `31673341881` SUCCESS, zero model calls;
- Deploy #129 / run `31673382889` SUCCESS;
- Creator tested Telegram Recovery readiness and confirmed it works.

### P3.4 — Minimum Training Effectiveness Outcome
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical detail: `docs/P3_4_TRAINING_EFFECTIVENESS.md`.

P3.4 adds a positive training outcome signal without mutating progression:
- `readiness` = pre-action state summary;
- `fatigue_cost_multiplier` = physiological cost;
- `effectiveness` = useful training-stimulus fraction recorded in action/outcome evidence.

For v1:
`effectiveness = readiness`.

Persistence uses existing schema-v4 paths:
- `action_instances.modifiers_json`;
- completion `outcome_json.modifiers`;
- `action_completed` event payload modifiers.

Regression coverage proves no skill score/tier/experience mutation.

Evidence:
- PR #3 merged at `ea69d5c0f81bf5500fca9b4d6ea62a251fbdcd9f`;
- PR CI #317 SUCCESS;
- main CI #318 / run `31673822574` SUCCESS;
- P3 Training Effectiveness Acceptance #1 / run `31673822547` SUCCESS, zero model calls, disposable production copy unchanged;
- release commit `818752a5976d988fcd3445ed3f0cc984f637d1cb`;
- Deploy #130 / run `31673858850` SUCCESS.

P3.4 adds no new standalone Telegram row. Effectiveness is now a reusable first-class outcome socket for a future bounded consumer.

## Next P3 slice — SELECT SEPARATELY

Do not automatically turn effectiveness into a broad progression engine.

Good next minimum-runnable candidates include:
- one small Creator-facing session/history readout that exposes effectiveness evidence; or
- one tightly bounded progression proof consuming effectiveness in exactly one domain.

Whichever is chosen must remain independently testable and must not silently expand into universal training, grading, or adaptation.

## P4 — Context / Memory / Relationship Slice

Status: LATER / DEMAND-DRIVEN.

Implement only when a concrete autonomous behavior or observer use case cannot be expressed without it. No bulk memory ontology, relationship engine, or background reflection loop is authorized by roadmap status alone.

## P5 — Second Production Character

Status: LATER.

Quasi is the intended second full autonomous production character after the single-character observer/runtime foundation and post-v4 vertical-slice pattern are sufficiently proven.

Minimum P5 should initially reuse existing runtime contracts for:
- canonical Quasi entity/profile seed;
- actor runtime row and cognition binding;
- valid initial location/state;
- independent wake-on-demand autonomy;
- Telegram character selection;
- bounded two-actor concurrency acceptance.

Advanced Darian–Quasi relationship simulation, synchronized group actions, and shared memory remain separate later slices.

## Later world expansion — South Lake Tahoe

Status: AFTER ESTATE/CHARACTER FOUNDATION IS PROVEN.

First regional slice should add only one small external traversal path/destination and prove movement/observation/return. Keep the rest of Tahoe frozen behind non-traversable boundaries until subsequent slices.

## Current resume point

P2.2 browsing and P2.3.1 Creator Restore Control are LIVE UX VERIFIED. P3.1 fatigue/recovery and P3.3 readiness are LIVE UX VERIFIED. P3.2 targeted training is acceptance verified. P3.4 training effectiveness is merged, main-CI verified, disposable-acceptance verified, and deployed successfully.

The next task is to choose one new minimum runnable slice. Preserve schema v4, 1x wake-on-demand autonomy, globally scoped ids, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed/audited Creator control, and incremental modifier/progression expansion only through concrete runnable needs.
