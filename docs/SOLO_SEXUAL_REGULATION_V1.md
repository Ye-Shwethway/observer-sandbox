# Solo Sexual Regulation v1

Status: IMPLEMENTED / VALIDATION PENDING

## Purpose

Activate one bounded adult solo sexual-behavior loop before Relationship System work, so current sexual physiology is a real simulation domain rather than only static profile data.

This slice is intentionally non-graphic and relationship-independent.

## Invariant

`adult actor + authored libido + release recency + current recovery state + authorized private/alone context -> bounded solo-regulation drive -> cognition may propose self_satisfaction -> deterministic validation -> temporary sexual physiology + immutable action evidence -> rolling 7-day count`

The behavior is discretionary. There is no target frequency and no rule that a healthy actor must perform it a fixed number of times per week.

## Inputs

Reusable current inputs:
- `raps_sa.libido`;
- completed `self_satisfaction` action history;
- current energy, fatigue and sleepiness;
- simulation time;
- current location;
- world `access=private` metadata;
- resident relation establishing authorized home scope;
- current character colocation.

The engine does **not** infer testosterone from gym attendance, body composition, Strength, or other athletic traits. No testosterone/endocrine engine is introduced by this slice.

## Adult and privacy gates

The action is unavailable unless:
- actor age at current simulation time is at least 18;
- current location is authored `private`;
- actor is within a location ancestry where that actor has a `resident` relation;
- no other represented character is colocated there;
- current drive meets the bounded action threshold;
- the anti-loop behavioral cooldown has elapsed.

The cooldown is a simulation pacing guard, not a medical refractory-period claim.

## Cognition

`ModelDecisionProvider` adds a structured `solo_sexual_regulation` context containing:
- adult eligibility;
- current non-clinical drive;
- recent rolling count/release recency;
- current private/aloneness state;
- reachable safe private rooms;
- explicit guidance that the behavior is legitimate but discretionary and never a quota.

The generic decision prompt explicitly tells cognition:
- only choose `self_satisfaction` when it appears in authoritative `action_options`;
- stronger physiological/safety needs remain higher priority;
- if drive is meaningful but the current room is not safe/private, ordinary movement to a reachable private room may be considered first.

The model never mutates physiology directly.

## Runtime physiology

When a validated action instance begins, the engine materializes temporary owner-only runtime values:
- `sexual_state.solo_regulation_drive`;
- `sexual_state.arousal_level`;
- `sexual_anatomy.erection_firmness`;
- `sexual_anatomy.erectile_state`.

Current firmness is bounded by the actor's authored baseline erectile function and firmness cap. Structural penis length/girth and long-term capacity fields are not changed by the behavior.

At completion:
- arousal/firmness enter a bounded `subsiding` presentation;
- drive is reduced;
- the completed action becomes immutable evidence;
- `raps_sa.self_satisfaction_weekly` is recomputed as a rolling trailing-seven-day count from completed actions.

Later ordinary action boundaries refresh drive and return temporary arousal/erectile presentation to baseline after the bounded subsiding interval.

## Observer privacy

The action is classified `intimate` at the observer policy layer.

Owner:
- can see the action in history/current/pending views;
- can receive proactive completion notifications;
- can inspect drive, rolling weekly count and current sexual physiology in the owner-only Sexual Anatomy & Physiology profile section.

Allowed non-owner observer:
- does not receive intimate completion notifications;
- does not see the intimate action in history or recent-location activity;
- sees a generic `Private Activity` placeholder if an intimate action is currently/pending;
- cannot open the owner-only sexual profile section.

Detailed solo-regulation evidence is attached only to the intimate action's own event/outcome, not copied into every ordinary action event.

## Deferred

Still deferred:
- partnered sexual behavior;
- Relationship System integration;
- attraction/partner selection;
- explicit fantasy/content simulation;
- testosterone/endocrine simulation;
- fertility/reproductive mechanics;
- clinical sexual-health/pathology modeling;
- any permanent anatomy change caused by ordinary sexual activity.

## Acceptance

Acceptance must prove on disposable state/production-copy evidence:
- adult gate;
- private + resident + alone gate;
- cognition receives private-context guidance;
- self-satisfaction appears only when currently legal;
- action-start temporary physiology materializes;
- completion updates rolling evidence and temporary post-state;
- immediate repetition is blocked by the bounded pacing guard;
- post-state returns to baseline on later action boundaries;
- trailing-seven-day metric expires naturally;
- structural anatomy/long-term capacity are unchanged;
- owner can observe the domain;
- allowed non-owner observer cannot discover intimate history/notification details;
- no model call is needed for deterministic settlement;
- live production is never accelerated merely to manufacture a natural occurrence.
