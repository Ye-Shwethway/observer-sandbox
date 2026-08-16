# Autonomy Intent Continuity v1

Status: IMPLEMENTATION CANDIDATE

## Problem

Observer Sandbox already has strong single-action autonomy: cognition sees current state and legal options, proposes one action, deterministic runtime validates and schedules it, completion commits state and wakes cognition again.

The missing minimum foundation is cross-action purpose continuity. `action_instances.intent` is the reason for one action, while `actor_runtime` persists only scheduler state. Recent event reasons provide history but do not identify an authoritative ongoing purpose.

A common example is purposeful movement: cognition can see a useful resource in a reachable room and choose to move toward it, but the next cognition boundary must currently reconstruct why the movement happened.

## Contract

Autonomy Intent Continuity v1 adds one bounded actor-scoped intent overlay without changing action legality or simulation authority.

Authority:

`committed purposeful movement -> bounded persisted intent -> next cognition context -> ordinary legal follow-up -> intent settlement`

Key invariants:

- deterministic runtime owns intent persistence;
- the LLM still proposes only ordinary actions/reasons through the existing decision contract;
- no new action vocabulary is added;
- no action/target/resource becomes legal because of an intent;
- physiological needs, safety and authoritative `action_options` override intent guidance;
- intent state is distinct from the authored profile and from the current pending action;
- initialization/deployment preserves active runtime intent rather than reseeding it;
- v1 uses existing `runtime_state`; schema remains v5.

## Exemplar lifecycle

### Start

When no intent is active, a committed `move` proposal with a concrete destination and a meaningful short reason may establish an active intent. The reason is normalized and bounded to a compact summary.

Ordinary non-movement actions do not spontaneously create sticky goals.

### Continue

If another movement step is selected while the intent is active, the same intent may continue. Movement continuation is capped at four planned movement steps. Crossing the bound abandons the intent rather than creating a navigation/planner loop.

### Self-care interruption

Basic physiological/self-care actions (`sleep`, `eat`, `drink`, `shower`, `rest`) may temporarily interrupt the purpose without automatically deleting it. This ensures intent never outranks needs.

### Finish

The first ordinary local non-movement follow-up is treated as the bounded fulfillment/exit boundary. The intent remains visible while that action is in progress and clears only when the represented action completes.

This does not claim the runtime understands arbitrary semantic goal completion. V1 deliberately proves only the cross-action purpose bridge needed for purposeful movement and immediate follow-up.

### Staleness

An active intent older than 12 simulated hours is removed at the next free decision boundary. This prevents deploy-surviving stale intent from becoming permanent character scripting.

## Cognition surface

The next decision receives compact `autonomy_intent` context:

- active/inactive;
- intent id;
- summary;
- origin/destination;
- movement-step count;
- interruption count;
- explicit guidance that intent is not an order and cannot override needs, safety or legal action options.

Internal intent transition metadata is stored on the planned action in `conditions.autonomy_intent_transition` so the completion boundary can deterministically settle the same intent without parsing model prose again.

## Runtime integration

Production service routing uses a thin intent-aware wrapper around the existing core `autonomy.autonomy_tick`.

The core scheduler remains unchanged. The wrapper:

1. expires stale intent only at a free decision boundary;
2. injects compact intent context before cognition;
3. decorates the already-proposed `Action` with deterministic intent-transition metadata;
4. calls the unchanged core scheduler/validator;
5. commits start/continuation/interruption only after an action is successfully planned;
6. clears a finish transition only after the represented follow-up action completes.

This keeps scheduling, leases, retries, validation, action instances and consequences under the existing tested authority.

## Non-goals

V1 does not add:

- arbitrary LLM goal-state writes;
- multi-goal prioritization;
- plan trees or task graphs;
- quests/jobs/projects;
- long-term commitments;
- semantic success scoring;
- deterministic action selection;
- relationship goals;
- broad episodic memory;
- a generic planner framework.

The slice is complete when focused regression coverage and the normal final CI/deploy/readback prove that the purpose bridge persists across an action boundary without weakening existing action validation or autonomy continuity.
