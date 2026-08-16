# Overall Workflow / Foundation Review v1

Status: ACTIVE REVIEW — THREE GAPS CLOSED

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
| Autonomy planning / purpose continuity | **CLOSED v1 minimum** | Autonomy Intent Continuity v1, PR #178 | A bounded actor-scoped purpose can survive a purposeful movement boundary and reach the next cognition call without overriding ordinary validation. |
| Persistent temporary modifier lifecycle | **CLOSED v1 minimum** | `active_modifiers`, Active Modifier Runtime Foundation v1, PR #180 | Time-bounded numeric modifiers now resolve deterministically into effective living-state reads without overwriting authoritative base state. |
| Action-definition prerequisite runtime | **CLOSED v1 minimum** | `action_definitions.conditions_json`, Action Condition Runtime Foundation v1, PR #182 | Authored bounded prerequisites shape legal options and direct deterministic validation through one fail-closed generic seam. |

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
- Deploy #236 / run `31920905305`: SUCCESS.

See `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`.

## Second gap closure — Active Modifier Runtime Foundation v1

The next read-only pass distinguished domain-specific modifiers from the persisted generic modifier socket. Training Readiness and Cognitive Performance were already real runtime behavior, but `active_modifiers` itself only proved storage/query structure; it had no generic effective-value resolver.

PR #180 closes that gap at minimum scope:
- generic numeric resolution over the existing `active_modifiers` table;
- half-open simulation-time activation/expiry;
- deterministic `stack`, `replace`, `max`, and `min` stack policies;
- exact caller-supplied contextual conditions only;
- first runtime consumer limited to energy, hunger, thirst, sleepiness, cleanliness and fatigue;
- effective snapshot values participate through existing cognition/need/training/action-legality paths;
- raw authoritative physiology remains separate, so temporary effects are not baked into persistent base state;
- no modifier producer, authoring UI, hidden Skill/IQ bonus system or schema change.

Checkpoint:
- PR #180 final head `49000d37542ec80cf489f8bd5c78876aaba16201`;
- CI #941 / run `31921368331`: **590 passed in 58.12s**;
- Minimum Training Stimulus Acceptance #27, Strength Live Cycle Validation v1 #83 and Solo Regulation Naturalism v2 Acceptance #30 all green;
- merge `74a0d9db25b3249192c24954feed11a45a7c961d`;
- Deploy #237 / run `31921444434`: SUCCESS;
- production healthy at schema v5 with autonomy/pending action preserved and no runtime reset.

The deploy workflow did not query `active_modifiers` row count, so this review does not claim a verified production row count or naturally active modifier.

See `docs/ACTIVE_MODIFIER_RUNTIME_V1.md`.

## Third gap closure — Action Condition Runtime Foundation v1

The following read-only pass found a narrower composability seam: `action_definitions.conditions_json` existed in persistence and reads, but generic option shaping and direct deterministic validation did not execute it. The existing training-fatigue rule therefore remained a hard-coded `train` branch rather than authored definition authority.

PR #182 closes that minimum gap:
- one bounded fail-closed prerequisite evaluator over action-definition conditions;
- v1 accepts one conjunctive `all` list with `lt`, `lte`, `gt`, `gte`, `eq`, and `ne` primitive clauses;
- first available values are current location plus the six established effective living-state fields;
- canonical `train` now owns `physiology.fatigue < 70` in its action definition;
- `action_options()` and `validate_action()` consume the same prerequisite contract;
- malformed shapes, unknown fields, unsupported operators and unavailable values fail closed;
- existing `Action.conditions` remains represented per-instance metadata and cannot authorize a proposal;
- Active Modifier Runtime composes through the effective living-state snapshot without rewriting raw physiology;
- canonical definition conditions resynchronize on initialize; schema remains v5;
- no expression language, scripts, nested boolean trees, cross-entity predicates, authoring UI, new action vocabulary or character-specific branch was added.

Checkpoint:
- PR #182 final head `fd86ef8a7a1d40fd58e42922e6fe7678a9bee1cf`;
- final CI #943 / run `31921888887`: **596 passed in 46.28s**;
- Research Action Semantics #43, Strength Live Cycle Validation v1 #85, Solo Regulation Naturalism v2 #32, Inventory Foundation v1 #49 and Minimum Training Stimulus #29 all green;
- merge `a79d5930b0fb206139d9c8359f3e35aa9499b68e`;
- Deploy #238 / run `31922007671`: SUCCESS;
- production healthy at schema v5 with autonomy normal, retry null, pending action preserved and speed 1x;
- Darian remained naturally sleeping in Darian's Master Suite at readback.

The first final-CI attempt found only a stale assertion expecting the superseded bespoke `"systemic fatigue"` text. The runtime contract was already behaving correctly; the assertion was aligned to the generic condition semantics and CI #943 then passed 596/596.

See `docs/ACTION_CONDITION_RUNTIME_V1.md`.

## Review continuation

Do **not** automatically deepen planning, modifiers or action-condition syntax now. The first three selected gaps are closed; return to read-only review and identify the next actual cross-system deficiency from canonical/live evidence.

Remaining review should distinguish between:
- a genuinely missing foundation;
- a minimum-present foundation that merely lacks depth;
- a deliberately deferred product domain.

Routine/schedule reinspection already confirms authored time windows plus current sim-time and physiological priority shape cognition meaningfully; absence of a full sequence ledger is not by itself a missing minimum foundation.

Potential reinspection areas include environment/world dynamics, episodic knowledge continuity, generalized multi-actor synchronization, and any remaining generic action/state integration seams. These are audit candidates only, not pre-authorized implementation targets.

## Explicit non-goals

This review does not authorize a giant planner, task graph, quest engine, relationship expansion, universal episodic-memory engine, weather system, economy, vehicles, broad Tahoe expansion, deterministic story chooser, modifier authoring UI, status-effect taxonomy, arbitrary universal bonus engine, or universal condition/expression language.
