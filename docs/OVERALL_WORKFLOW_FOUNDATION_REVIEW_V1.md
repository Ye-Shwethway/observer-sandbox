# Overall Workflow / Foundation Review v1

Status: ACTIVE REVIEW — FOUR GAPS CLOSED

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
| Participant-aware recent event cognition | **CLOSED v1 minimum** | `event_participants`, Participant-Aware Recent Event Context v1, PR #184 | A represented non-actor participant receives the shared event in the same bounded cognition recent-event window without broad memory inference. |
| Longer-horizon progression / decay | CLOSED v1 exemplars | physical progression/detraining plus adaptive habit/interest/preference/personality lifecycles | Architecture proves persisted cross-time development and decay at multiple timescales. |
| Profile -> cognition/runtime integration | CLOSED v1 | minimum profile unlock checkpoint, capability awareness, personality/preferences/habits/skills cognition context | Current profile foundation is runnable; exhaustive field mechanics are later depth. |
| Autonomy planning / purpose continuity | **CLOSED v1 minimum** | Autonomy Intent Continuity v1, PR #178 | A bounded actor-scoped purpose can survive a purposeful movement boundary and reach the next cognition call without overriding ordinary validation. |
| Persistent temporary modifier lifecycle | **CLOSED v1 minimum** | `active_modifiers`, Active Modifier Runtime Foundation v1, PR #180 | Time-bounded numeric modifiers resolve deterministically into effective living-state reads without overwriting authoritative base state. |
| Action-definition prerequisite runtime | **CLOSED v1 minimum** | `action_definitions.conditions_json`, Action Condition Runtime Foundation v1, PR #182 | Authored bounded prerequisites shape legal options and direct deterministic validation through one fail-closed generic seam. |

## First gap closure — Autonomy Intent Continuity v1

PR #178 closes the minimum cross-action purpose gap with one actor-scoped bounded intent. Purposeful represented movement may establish it; cognition receives guidance only; needs, safety, and legal options stay authoritative; self-care can interrupt it; ordinary represented completion clears it; stale intent expires after 12 simulated hours; persistence uses existing `runtime_state`; schema remains v5.

Checkpoint: final head `563e102c6a9d73ea2f39e828da6329840632ef79`; CI #940 / run `31920821319` with 583 passed; merge `0cf9a38e7fadafa178f1f69f9f5b7013cbd1961f`; Deploy #236 / run `31920905305` SUCCESS.

See `docs/AUTONOMY_INTENT_CONTINUITY_V1.md`.

## Second gap closure — Active Modifier Runtime Foundation v1

PR #180 turns the existing `active_modifiers` persistence socket into a bounded deterministic numeric resolver with simulated-time activation/expiry and `stack`/`replace`/`max`/`min` policies. Its first consumer remains the six established living-state fields; effective reads influence existing runtime paths while raw physiology stays authoritative. No producer, authoring UI, universal bonus engine, or schema change was added.

Checkpoint: final head `49000d37542ec80cf489f8bd5c78876aaba16201`; CI #941 / run `31921368331` with 590 passed; merge `74a0d9db25b3249192c24954feed11a45a7c961d`; Deploy #237 / run `31921444434` SUCCESS.

See `docs/ACTIVE_MODIFIER_RUNTIME_V1.md`.

## Third gap closure — Action Condition Runtime Foundation v1

PR #182 makes `action_definitions.conditions_json` executable through one bounded fail-closed prerequisite evaluator. V1 supports a conjunctive `all` list with primitive comparisons only. The existing `train` fatigue guard now lives in canonical definition data as `physiology.fatigue < 70`; legal option shaping and direct validation consume the same contract; proposal `Action.conditions` remains non-authoritative instance metadata. Schema remains v5.

Checkpoint: final head `fd86ef8a7a1d40fd58e42922e6fe7678a9bee1cf`; CI #943 / run `31921888887` with 596 passed; merge `a79d5930b0fb206139d9c8359f3e35aa9499b68e`; Deploy #238 / run `31922007671` SUCCESS.

See `docs/ACTION_CONDITION_RUNTIME_V1.md`.

## Fourth gap closure — Participant-Aware Recent Event Context v1

The next read-only pass found a narrow integration mismatch between existing event authority and cognition. `event_participants` already indexed represented shared events, including non-actor roles, but `ModelDecisionProvider._recent_events()` only selected `events.actor_id = character_id`. A character could therefore participate authoritatively in a shared event yet fail to receive that event in its next bounded cognition history.

PR #184 closes that minimum gap:
- recent events are relevant when the character is either primary actor or an authoritative `event_participants` member;
- the existing bounded recent-event window and chronological ordering remain unchanged;
- cognition receives the represented primary `actor_id` and its own persisted `participation_role`;
- actor-owned events remain visible exactly once despite actor participant indexing;
- legacy actor-owned events without participant rows fall back to role `actor`;
- unrelated characters receive nothing merely from event existence or co-location;
- no event write path, schema, relationship state, witness model, social interpretation, long-term memory, or memory scoring was added.

Checkpoint:
- PR #184 final head `09f629b197b55f0abc8271e22e86a9a11f2cab0c`;
- CI #944 / run `31924499307`: **600 passed in 44.52s**;
- Cognition Capability Awareness #24, Solo Regulation Naturalism v2 #33, Eating Behavior #46, Training Movement Contract Normalization #14, and Research Action Semantics #45 all green;
- merge `13d4a9270f3c372a5180438f92f13441d98e804a`;
- Deploy #239 / run `31924581764`: SUCCESS;
- production healthy at schema v5 with autonomy normal, retry null, pending action preserved, and speed 1x;
- Darian remained naturally sleeping in Darian's Master Suite at readback.

No production shared event was fabricated for proof. The read-side participant semantics are established by regression/CI; deployment readback establishes runtime continuity.

See `docs/PARTICIPANT_RECENT_EVENT_CONTEXT_V1.md`.

## Review continuation

Do **not** automatically deepen planning, modifiers, condition syntax, routine scheduling, participant history, relationships, or memory now. The first four selected gaps are closed; return to read-only review and identify the next actual cross-system deficiency from canonical/live evidence.

Remaining review must distinguish between:
- a genuinely missing foundation;
- a minimum-present foundation that merely lacks depth;
- a deliberately deferred product domain.

Routine/schedule reinspection already confirms authored time windows plus current sim-time and physiological priority shape cognition meaningfully. The new participant-aware recent-event slice also closes the immediate shared-event cognition seam without authorizing a universal episodic-memory layer.

Potential reinspection areas include environment/world dynamics and remaining generic action/state integration seams. Generalized group synchronization and broad episodic memory remain later-depth candidates unless concrete evidence establishes a missing minimum invariant.

## Explicit non-goals

This review does not authorize a giant planner, task graph, quest engine, relationship expansion, universal episodic-memory engine, witness model, weather system, economy, vehicles, broad Tahoe expansion, deterministic story chooser, modifier authoring UI, status-effect taxonomy, arbitrary universal bonus engine, or universal condition/expression language.
