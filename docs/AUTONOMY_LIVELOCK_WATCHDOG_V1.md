# Autonomy Livelock Watchdog v1

## Purpose

Prevent a healthy Observer Sandbox service from leaving simulation time frozen when model cognition repeatedly proposes an action/target pair outside the deterministic runtime's authoritative `action_options`.

This is a continuity guard, not a replacement decision-maker.

## Trigger

The watchdog is eligible only when all of the following are true:

- autonomy is in normal mode;
- there is no pending action;
- the current model proposal and its bounded corrective retry both remain outside authoritative `action_options`;
- at least two immediately preceding `autonomy_error` events at the same simulation boundary are decision-stage `ValueError` events whose message identifies the same authoritative-pair validation family;
- the resulting current failure would therefore be the third consecutive pair-validation failure.

## Recovery

The runtime reuses the already-enriched, already-shaped authoritative action surface created for the current cognition boundary.

- When a strong/critical physiological need is active, need-resolution shaping has already reduced the surface to a local resolver action or legal first-hop movement. The watchdog chooses deterministically from that legal surface.
- When no strong physiological need is active, `idle` is preferred as the lowest-risk continuity fallback, then targetless `rest`, then another legal option only if neither exists.
- The resulting action still passes normal deterministic `validate_action` before scheduling.
- Recovery provenance is attached to the action conditions as `autonomy_recovery.source = autonomy-livelock-watchdog-v1`, so the ordinary action-start event remains auditable.

## Explicit exclusions

The watchdog does not recover:

- provider/API/rate-limit/quota failures;
- completion-stage failures;
- schedule-stage failures;
- unrelated `ValueError` failures;
- canary runs.

Those remain fail-closed under their existing retry/fallback contracts.

## Design boundary

The watchdog never invents a target, bypasses validation, teleports the actor, or converts planning-only resource awareness into an actionable target. It can only select an option already present in the current authoritative runtime surface.

The intent is to break a cognition livelock while preserving deterministic simulation authority and returning subsequent choices to normal model cognition after the recovered action boundary.
