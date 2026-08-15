# Slow Personality Plasticity v1

Status: IMPLEMENTED CANDIDATE

## Purpose

Slow Personality Plasticity v1 completes the minimum Adaptive Character Disposition Foundation without turning personality into a fast-changing reward score.

Canonical personality remains the authored baseline. Runtime experience may only add a small persisted overlay after a long, semantically relevant evidence horizon.

## Authority

`represented completion / explicit represented outcome -> registered trait-evidence channel -> long-horizon ledger -> bounded overlay -> cognition`

The LLM is proposal-only. It cannot create traits, choose evidence valence, mutate ledgers, or rewrite canonical profile text.

## V1 exemplar

V1 intentionally proves one reusable channel only:

- authored baseline trait: `disciplined`
- automatic positive evidence: completed represented `train` actions, registered as `completed_deliberate_training`
- optional explicit positive outcome channel: `represented_self_regulation_outcome`
- optional explicit opposing outcome channel: `represented_counter_discipline_outcome`

This is an exemplar, not a claim that every training action universally measures personality or that every personality trait should receive an action mapping.

A trait must both:
1. exist in the actor's authored `personality.primary_traits`; and
2. have an explicitly registered evidence channel.

The runtime therefore cannot manufacture a new personality trait through generic evidence.

## Long-horizon gate

Personality is intentionally slower than preferences, hobbies/interests, and habits.

For an overlay to become cognition-visible, evidence must satisfy all of:

- signed score magnitude at least `14`;
- effective evidence at least `14`;
- at least `14` distinct evidence days;
- at least `21` simulated days between first and current evidence.

Same-day repetitions have personality evidence weight `0`. They remain countable as observations for audit but do not accelerate the long-horizon gate.

Once eligible, overlay magnitude begins small and remains capped at `0.15`. Initial eligibility produces only a `0.02` overlay. Canonical trait text is never rewritten.

## Reversal / softening

Opposing evidence is never inferred from omission, inactivity, a missed routine, or an action the character did not choose.

Negative evidence requires an explicit registered represented-outcome producer. Existing positive evidence must first be neutralized; a softened overlay appears only after sufficient signed evidence accumulates in the opposite direction under the same long-horizon gate.

This makes reversal much slower than ordinary preference reversal and prevents one dramatic event from instantly changing personality.

## Persistence and cognition

The evidence ledger is persisted under `runtime_state` keys prefixed with:

`personality_plasticity_v1:`

No schema migration is required; schema remains v5.

Cognition receives only compact established context under:

`character.personality.slow_adaptation`

Example:

```json
[
  {
    "trait": "disciplined",
    "direction": "strengthened",
    "magnitude": "slight",
    "overlay": 0.02
  }
]
```

Internal signed score, evidence counts, source timings, and mutation instructions are not exposed to cognition.

## Non-goals

V1 does not add:

- a generic Big Five or clinical psychology engine;
- arbitrary new personality traits;
- automatic negative inference from missed actions;
- personality mutation from preferences or hobbies merely because they changed;
- universal reward/penalty scoring;
- relationship-driven personality mechanics;
- trauma modeling;
- instant personality flips;
- destructive edits to canonical profile data;
- Darian-only branching in the generic runtime.

Additional traits should be added only when a represented runtime contract provides semantically defensible evidence, using the same bounded overlay pattern rather than broad guesswork.
