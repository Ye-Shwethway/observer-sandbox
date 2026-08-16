# Overall Workflow / Foundation Review v1

Status: ACTIVE REVIEW — FIRST GAP CLOSED

## Purpose

After all Character Profile sections reached minimum-unlocked v1 and the Adaptive Character Disposition Foundation closed v1, this review re-audits the cross-system runtime before deeper local feature work.

The review applies the vertical-completeness rule: do not rebuild a foundation merely because it is not exhaustive. A candidate is minimum-present when the canonical runtime already has an authoritative reusable contract, represented evidence, and an integration path that can support later depth.

## Audit matrix

| Foundation | Classification | Canonical evidence | Minimum conclusion |
| --- | --- | --- | --- |
| Generic action/task lifecycle | CLOSED v1 | `action_definitions`, first-class `action_instances`, deterministic validation/completion, represented skill-task contracts | Definition/instance separation and action boundaries are authoritative. |
| Resources / inventory / state consequences | CLOSED v1 | schema-v5 `inventory_stacks`, Inventory Operations v1, resource-aware cognition, represented consequence state | Quantity/depletion and typed Creator operations are operational; economy/encumbrance are later depth. |
| Environment / world context | CLOSED v1 | world graph, dynamic `located_at`, topology-aware movement, reachable-location awareness | Current environment participates meaningfully in legal options and cognition. Weather and broad Tahoe traversal are deferred features, not missing core sockets. |
| Knowledge / familiarity | CLOSED v1 minimum | Object Familiarity / Inspect Utility Guard v1, recent interaction evidence | Unknown objects can be inspected; established functional/prior-interaction familiarity suppresses pointless repeat inspection. Full episodic memory is later work. |
| Inter-character participation | CLOSED v1 socket | action participants, event participants, co-location/consent validation, controlled H2H generalization | Generic represented multi-actor participation exists. Rich relationships/group synchronization remain later depth. |
| Event / lifecycle handling | CLOSED v1 | event UUID/action/location/causal parent/state-change envelope and participant index | Committed state changes emit linked queryable evidence. |
| Longer-horizon progression / decay | CLOSED v1 exemplars | physical progression/detraining plus adaptive habit/interest/preference/personality lifecycles | Architecture proves persisted cross-time development and decay at multiple timescales. |
| Profile -> cognition/runtime integration | CLOSED v1 | minimum profile unlock checkpoint, capability awareness, personality/preferences/habits/skills cognition context | Current profile foundation is runnable; exhaustive field mechanics are later depth. |
| Autonomy planning / purpose continuity | **CLOSED v1 minimum** | Autonomy Intent Continuity v1, PR #178 | A bounded actor-scoped purpose can now survive a purposeful movement boundary and reach the next cognition call without overriding ordinary validation. |

## First gap closure — Autonomy Intent Continuity v1

The initial review confirmed that autonomy was robust at one decision boundary but lacked authoritative cross-action purpose state. `action_instances.intent` stored one action's reason, `actor_runtime` stored scheduler state, and recent events supplied history only.

PR #178 closes that minimum gap with a deliberately small bridge:

- one actor-scoped active intent at most;
- purposeful represented `move` may establish a bounded intent from its committed reason;
- next cognition receives compact intent guidance, never authority;
- legal action options, physiological needs and safety remain stronger than intent;
- movement continuation is bounded to four planned movement steps;
- self-care may interrupt without automatically deleting purpose;
- the first ordinary local follow-up clears only after represented completion;
- intent older than 12 simulated hours self-expires at the next free decision boundary;
- persistence uses existing `runtime_state`; schema stays v5;
- core `autonomy.autonomy_tick` remains unchanged behind the thin wrapper.

Checkpoint:
- PR #178 final head `563e102c6a9d73ea2f39e828da6329840632ef79`;
- CI #940 / run `31920821319`: **583 passed in 58.57s**;
- all automatic production-copy acceptance gates green without retry;
- merge `0cf9a38e7fadafa178f1f69f9f5b7013cbd1961f`;
- Deploy #236 / run `31920905305`: SUCCESS;
- production healthy at schema v5, autonomy normal, retry null, pending action present, speed 1x;
- Darian naturally sleeping in the Master Suite at deploy readback;
- deploy log exposed sim time only as `2025-05-07T***:27:00+00:00`, so the masked hour is not inferred;
- no `autonomy_intent_v1:` row appeared, confirming deploy/init did not manufacture a live intent.

See `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`.

## Review continuation

Do **not** automatically deepen planning now. The first selected gap is closed; return to read-only review and identify the next actual cross-system deficiency from canonical/live evidence.

Remaining review should distinguish between:
- a genuinely missing foundation;
- a minimum-present foundation that merely lacks depth;
- a deliberately deferred product domain.

Potential reinspection areas include environment/world dynamics, episodic knowledge continuity, generalized multi-actor synchronization, schedule/routine continuity, and any remaining generic action/state integration seams. These are audit candidates only, not pre-authorized implementation targets.

## Explicit non-goals

This review does not authorize a giant planner, task graph, quest engine, relationship expansion, universal episodic-memory engine, weather system, economy, vehicles, broad Tahoe expansion, or deterministic story chooser.
