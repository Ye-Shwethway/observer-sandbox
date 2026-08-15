# Casualty State Origin & Lifecycle Contract v1

Status: implemented exemplar

## Purpose

Field Medicine stabilization v1 consumes a pre-existing simulated field:

`medical.deterioration_risk`

This contract owns the missing lifecycle seam: how that field may be created and how the represented casualty context may later end. It deliberately does not model injuries, diagnoses, definitive treatment, death, incapacity, bleeding, or recovery.

## Canonical ownership

Implementation:
`src/observer_sandbox/casualty_state_lifecycle.py`

V1 field authority:
`casualty_state_runtime`

V1 field source:
`casualty-state-origin-lifecycle-v1`

No schema migration is required. The contract composes existing schema-v5 primitives:
- `fields` for the one simulated casualty-state value;
- `events` for source and lifecycle evidence;
- `event_participants` for explicit casualty identity;
- `caused_by_event_id` for causal linkage;
- `state_changes_json` for create/delete evidence.

## Origin contract

`initialize_casualty_state(...)` may create `medical.deterioration_risk` only when:
- the casualty is an existing represented character;
- a source event already exists;
- that exact source event explicitly binds the character as event participant role `casualty`;
- the requested origin kind is one of the finite V1 origin kinds;
- the risk is numeric and within `0..100`;
- the deterioration field does not already exist.

V1 origin kinds:
- `represented_domain_consequence`
- `represented_environmental_hazard`
- `represented_accident`

Success creates exactly one field:
- field key: `medical.deterioration_risk`
- mode: `simulated`
- authority: `casualty_state_runtime`
- source: `casualty-state-origin-lifecycle-v1`

Success also emits `casualty_state_initialized`, causally linked to the source event and carrying explicit before/after state-change evidence.

The API never infers casualty state from model prose, event wording, Skill score, combat narration, or generic capabilities.

## Lifecycle clear contract

`clear_casualty_state(...)` ends the represented casualty context only when:
- an explicit source event already exists;
- that event explicitly binds the character with role `casualty`;
- the existing deterioration field is simulated state owned by this V1 lifecycle authority/source;
- the resolution kind is one of the finite V1 resolution kinds.

V1 resolution kinds:
- `evacuated_or_handed_off`
- `casualty_context_resolved`

Success deletes only `medical.deterioration_risk` and emits `casualty_state_cleared` causally linked to the explicit resolution source event.

Clearing a casualty context does not assert healing, diagnosis resolution, or definitive treatment.

## Important zero-risk boundary

`medical.deterioration_risk == 0` does not automatically clear casualty state.

Stabilization reducing risk to zero means only that the represented deterioration-risk dimension reached zero. It does not prove the casualty is healed or that the field-medical context has ended. Lifecycle clearing therefore requires a separate explicit handoff/context-resolution source event.

## Idempotency and transaction boundary

Initialization and clearing are savepoint-atomic.

Retries are idempotent per source event + casualty + lifecycle operation:
- the same origin source event cannot create the field twice;
- the same resolution source event cannot emit multiple clear events.

The contract never overwrites a pre-existing deterioration field and never deletes state owned by another authority/source.

## Evidence boundary

Lifecycle events set `learning_evidence: false`.

They do not award Field Medicine XP and do not create Skill application evidence. They are world-state lifecycle evidence only.

## Non-goals

V1 does not add:
- an Injury Engine;
- wound or bleeding taxonomy;
- diagnosis state;
- definitive-treatment state;
- death/incapacity state;
- automatic deterioration over time;
- automatic recovery;
- automatic casualty creation from H2H or Weapons;
- medical-resource depletion;
- real-world medical guidance;
- production casualty fixtures solely for proof.

## Next expansion rule

A real domain producer may later invoke this contract only after its own exact deterministic event/authorization semantics are defined. Do not make controlled H2H a casualty producer merely to exercise this API. Weapons consequences remain a separate structural decision.
