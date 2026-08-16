# Overall Workflow / Foundation Review v1

Status: REVIEWED — NEXT GAP SELECTED

## Purpose

After all Character Profile sections reached minimum-unlocked v1 and the Adaptive Character Disposition Foundation closed v1, this review re-audits the cross-system runtime before any deeper local feature work.

The review applies the vertical-completeness rule: do not rebuild a foundation merely because it is not exhaustive. A candidate is considered minimum-present when the current canonical runtime already has an authoritative reusable contract, represented evidence, and an integration path that can support later depth.

## Audit matrix

| Foundation | Classification | Canonical evidence | Minimum conclusion |
| --- | --- | --- | --- |
| Generic action/task lifecycle | CLOSED v1 | `action_definitions`, first-class `action_instances`, deterministic validation/completion, represented skill-task contracts | Definition/instance separation and action boundaries are already authoritative. |
| Resources / inventory / state consequences | CLOSED v1 | schema-v5 `inventory_stacks`, Inventory Operations v1, resource-aware cognition, represented consequence state | Quantity/depletion and typed Creator operations are operational; economy/encumbrance remain later depth. |
| Environment / world context | CLOSED v1 | world graph, dynamic `located_at`, topology-aware movement, reachable-location awareness | Current environment participates meaningfully in legal options and cognition. Weather and broad Tahoe traversal remain deferred features, not missing core sockets. |
| Knowledge / familiarity | CLOSED v1 minimum | Object Familiarity / Inspect Utility Guard v1, recent interaction evidence | Unknown objects can be inspected; established functional/prior-interaction familiarity suppresses pointless repeat inspection. Full episodic memory remains later work. |
| Inter-character participation | CLOSED v1 socket | action participants, event participants, co-location/consent validation, controlled H2H generalization | Generic represented multi-actor participation exists. Rich relationships and group synchronization remain later depth. |
| Event / lifecycle handling | CLOSED v1 | event UUID/action/location/causal parent/state-change envelope and participant index | Committed state changes can emit linked queryable evidence. |
| Longer-horizon progression / decay | CLOSED v1 exemplars | physical progression/detraining plus adaptive habit/interest/preference/personality lifecycles | The architecture already proves persisted cross-time development and decay at multiple timescales. |
| Profile -> cognition/runtime integration | CLOSED v1 | minimum profile unlock checkpoint, capability awareness, personality/preferences/habits/skills cognition context | Current profile foundation is runnable; missing exhaustive field-specific mechanics are later depth. |
| Autonomy planning / purpose continuity | MINIMUM IMPLEMENTATION REQUIRED | current actor runtime persists one pending action/retry/wake state; recent events preserve history, but no authoritative ongoing purpose crosses action boundaries | This is the highest-leverage remaining cross-system gap. |

## Confirmed autonomy gap

Current autonomy is robust at a single decision boundary:

`observe -> choose one legal action -> validate -> persist one pending action -> complete -> clear pending -> wake cognition again`

`action_instances.intent` stores the reason for that one action. `actor_runtime` stores the pending action, lease, retry/backoff, cognition statistics and wake reason. Neither is an authoritative multi-action purpose.

Recent events expose prior action reasons to cognition, but historical inference is not the same as persisted active intent. A purposeful move toward another room therefore depends on the next model call re-inferring why the character moved rather than receiving a compact authoritative continuation signal.

This matters because reachable-location awareness explicitly supports purposeful movement to distant resources. Without a bridge across the movement boundary, the runtime has the pieces for multi-step behavior but not the minimum continuity contract connecting them.

## Selected next slice

**Autonomy Intent Continuity v1** is selected as the next minimum-runnable cross-system foundation.

The v1 boundary is deliberately smaller than a planner:

- one actor-scoped active intent at most;
- purposeful represented movement is the exemplar start signal;
- the committed action reason becomes a bounded intent summary;
- the next cognition boundary receives that intent as guidance, never as authority;
- legal action options, physiological needs and safety remain stronger than intent;
- additional movement may continue it within a small bound;
- ordinary local follow-up completion ends it;
- basic self-care may interrupt it without automatically erasing it;
- stale/looping intent self-clears;
- persistence uses existing runtime state; no schema migration is required.

## Explicit non-goals

This review does not authorize a giant planner, task graph, quest engine, relationship expansion, universal episodic-memory engine, weather system, economy, vehicles, broad Tahoe expansion, or deterministic story chooser.

After the intent-continuity exemplar is proven, return to this foundation review and select the next actual gap from evidence rather than continuing to deepen autonomy planning automatically.
