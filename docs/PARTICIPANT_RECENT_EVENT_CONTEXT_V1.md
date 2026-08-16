# Participant-Aware Recent Event Context v1

Status: IMPLEMENTATION CANDIDATE

## Why this slice exists

The event foundation already persists authoritative `event_participants` rows for represented shared events, including the actor and non-actor participant roles. Cognition's bounded `recent_events` read, however, only selected rows where the current character was `events.actor_id`.

That left a cross-system seam: a character could participate authoritatively in a shared represented event but not receive that event in the next bounded cognition context unless they were the primary actor.

## V1 contract

`ModelDecisionProvider._recent_events()` treats an event as relevant when either:
- the character is the event actor; or
- the character has an authoritative row in `event_participants` for that event.

The existing recent-event window remains authoritative and bounded. Results remain chronological within the selected newest window.

Each cognition-visible recent event also exposes:
- `actor_id` — the represented primary actor;
- `participation_role` — the current character's authoritative event role, with `actor` fallback for legacy actor-owned events that predate participant indexing.

## Compatibility and boundaries

- Actor-owned events remain visible once; the actor's automatic participant index must not duplicate them.
- Unrelated characters do not receive the event.
- No event is inferred from co-location alone.
- No relationship state, witness model, social interpretation, long-term episodic memory, memory scoring, or new event type is introduced.
- Existing event persistence remains unchanged; schema remains v5.
- The slice is read-side only and does not mutate production state merely to prove behavior.

## Focused regression

Coverage proves:
- an actor-owned event remains visible exactly once with role `actor`;
- a non-actor participant receives a shared event with its persisted role;
- an unrelated character receives no event merely because the event exists;
- the existing limit and chronological ordering work across a mix of actor-owned and participant events.

## Completion rule

The slice is complete when the focused regression and the normal one-time final PR CI pass, automatic task-relevant acceptance remains healthy, the runtime-affecting merge deploys normally, and read-only production verification confirms service/runtime continuity without fabricating a shared event for proof.
