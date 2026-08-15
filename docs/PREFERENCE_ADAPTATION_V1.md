# Preference Adaptation v1

Status: IMPLEMENTED CANDIDATE

## Purpose

Preference Adaptation v1 adds the minimum deterministic lifecycle needed for preferences to develop from lived evidence without granting the LLM direct profile-mutation authority.

## Authority flow

`completed represented action/outcome -> signed evidence -> persisted adaptation ledger -> established preference projection -> cognition`

The LLM proposes actions only. It never writes preference score, valence, or status.

## Positive evidence

V1 deliberately uses only repeated completed target-based `read` and `use` actions as automatic positive evidence. These are voluntary discretionary engagement signals already represented by the runtime.

A single engagement is evidence only. It does not immediately create a visible `like` preference.

Same-day repetition receives diminished weight so repeated short-loop actions cannot instantly manufacture a strong preference.

## Negative evidence

Absence of choice, inactivity, or choosing another option is **not** negative preference evidence.

Negative evidence requires an explicit represented aversive/outcome producer and enters through the signed evidence API with `valence=-1`. V1 provides the deterministic contract but does not invent a generic aversive-outcome engine or fabricate negative production events.

## Persistence and projection

Per-target signed evidence lives in `runtime_state` under the `preference_adaptation_v1:` namespace. This ledger persists evidence count, effective evidence, distinct evidence days, signed score, and last evidence provenance.

Only sufficiently repeated cross-day evidence materializes an active preference in `character_preferences`:

- positive established score -> `like`
- negative established score -> `dislike`

Canonical authored preferences remain untouched.

## Weakening and reversal

Opposing represented evidence moves the signed score gradually toward neutral. An established preference is removed from the active projection only after entering the neutral band. Continued opposite evidence must then cross the establishment threshold on the other side before reversal occurs.

Therefore `like -> dislike` and `dislike -> like` are multi-evidence transitions, never instant flips.

## Non-goals

V1 does not add:

- arbitrary LLM preference writes;
- negative evidence from non-selection;
- food enjoyment inference from merely satisfying hunger;
- automatic preference decay from inactivity alone;
- relationship preferences;
- a universal satisfaction/aversion engine;
- personality mutation;
- synthetic production evidence for proof.

## Completion standard

Preference Adaptation v1 is complete when regression evidence proves:

1. one voluntary engagement does not create an instant visible preference;
2. repeated cross-day positive evidence can establish a `like`;
3. same-day repetition is diminished;
4. unrelated actions/non-selection create no negative evidence;
5. explicit represented negative evidence weakens through neutral before reversal;
6. canonical preferences remain intact;
7. adaptation ledger and established projection survive reinitialization;
8. established dynamic preferences reach existing cognition preference context.
