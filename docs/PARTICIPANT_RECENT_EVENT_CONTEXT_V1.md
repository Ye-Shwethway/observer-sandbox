# Participant-Aware Recent Event Context v1

Status: **COMPLETE v1 / DEPLOYED**

## Why this slice exists

The event foundation already persisted authoritative `event_participants` rows for represented shared events, including actor and non-actor participant roles. Cognition's bounded `recent_events` read, however, selected only rows where the current character was `events.actor_id`.

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

- Actor-owned events remain visible once; the actor's automatic participant index does not duplicate them.
- Unrelated characters do not receive the event.
- No event is inferred from co-location alone.
- No relationship state, witness model, social interpretation, long-term episodic memory, memory scoring, or new event type is introduced.
- Existing event persistence remains unchanged; schema remains v5.
- The slice is read-side only.

## Focused regression

Coverage proves:
- an actor-owned event remains visible exactly once with role `actor`;
- a non-actor participant receives a shared event with its persisted role;
- an unrelated character receives no event merely because the event exists;
- the existing limit and chronological ordering work across a mix of actor-owned and participant events.

## Production checkpoint

PR #184 completed this foundation.

- final tested head: `09f629b197b55f0abc8271e22e86a9a11f2cab0c`;
- **CI #944 / run `31924499307`: SUCCESS**;
- **600 passed in 44.52s**;
- fresh DB initialize/status healthy; schema v5;
- Cognition Capability Awareness v1 Acceptance #24: SUCCESS;
- Solo Regulation Naturalism v2 Acceptance #33: SUCCESS;
- Eating Behavior v1 Acceptance #46: SUCCESS;
- Training Movement Contract Normalization v1 Acceptance #14: SUCCESS;
- Research Action Semantics Acceptance #45: SUCCESS;
- merge: `13d4a9270f3c372a5180438f92f13441d98e804a`;
- **Deploy #239 / run `31924581764`: SUCCESS**.

Production readback after Deploy #239 confirmed:
- service active and healthy;
- schema v5;
- autonomy enabled in normal mode with retry null and pending action preserved;
- speed 1x;
- Darian remained naturally sleeping in Darian's Master Suite;
- living state: cleanliness 98.491, energy 88.791, fatigue 6.305, hunger 7.578, sleepiness 58.55, thirst 23.15;
- deploy output exposed sim time only as `2025-05-07T***:27:00+00:00`; the masked hour is not inferred;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram bot/API/owner/allowed-user configuration healthy.

No production shared event was fabricated solely to prove this read-side contract. Participant visibility is proven by focused regression and CI; the production readback establishes deployment and runtime continuity only.

## Non-goals

V1 does not add relationship state, a witness/visibility engine, social interpretation, generalized group coordination, long-term episodic memory, memory scoring, or new event semantics.
