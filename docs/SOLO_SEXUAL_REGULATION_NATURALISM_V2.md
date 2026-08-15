# Solo Sexual Regulation Naturalism v2

Status: IMPLEMENTED / VALIDATING

## Purpose

Correct the over-conservative Solo Sexual Regulation v1 pacing model without introducing a quota, relationship system, endocrine simulation, or explicit-content mechanics.

The v1 privacy gate also conflated generic room access with private-activity suitability. v2 separates those concepts and lets cognition reason about appropriate secluded locations through the normal world graph.

## Corrected invariant

`adult actor + authored libido + adult life-stage + current recovery + represented home solitude + release recency + recent same-day saturation + authorized private-activity context -> bounded current drive -> cognition may choose self_satisfaction`

The action remains discretionary. The runtime does not target a weekly or daily frequency and does not force a character to act when the option is legal.

## Drive model

Naturalism v2 keeps authored `raps_sa.libido` as the primary stable input and adds bounded contextual terms:

- adult life-stage bonus, used as a gameplay vitality heuristic rather than a clinical or population-frequency rule;
- positive recovery bonus when energy is good and fatigue/sleepiness are low;
- represented resident-scope solitude bonus when no other represented character occupies the actor's home scope;
- release-recency pressure that rebuilds faster for higher authored libido;
- recent trailing-24-hour saturation penalty that grows after each completed release;
- stronger fatigue, sleepiness and low-energy penalties only when those states are meaningfully adverse.

This fixes the v1 asymmetry where good health supplied no positive contribution while poor state supplied penalties.

The anti-loop behavioral cooldown is reduced from 6 hours to 2 hours. It remains only a simulation pacing guard, not a medical refractory-period claim. After the guard expires, the current drive threshold still decides whether the option is legal.

For a high-libido, young, well-recovered and solitary adult exemplar such as Darian, a same-day repeat may therefore become legal. Multiple same-day occurrences are possible when state supports them, while the increasing trailing-24-hour penalty prevents an unbounded loop. Cognition still decides whether to take the option.

## Privacy suitability

`world.access` is no longer treated as the complete privacy model.

Locations may now author `world.metadata.private_activity` through world seed metadata. Current supported policies are:

- `resident_private` — actor-resident personal space;
- `secluded` / `secluded_when_alone` — suitable when authorized and no other represented character is present;
- other values such as `personal_other` or `guest_reserved` — explicitly unsuitable for this actor's private activity.

The Thorne Estate now marks multiple plausible secluded spaces independently of bathroom semantics, including the Library & Study and selected restricted rooms such as the Training Hall, Home Gym, Garage, secure rooms and bunker. Darian's Master Suite and Master Bathroom remain valid personal spaces. Quasi's Room and Guest Rooms are explicitly excluded despite generic `access=private`.

This keeps the rule character/world-driven rather than bathroom-hard-coded.

## Reachability

The cognition context now searches the normal `connected_to` graph breadth-first for reachable safe private-activity locations instead of exposing only directly adjacent rooms. Returned candidates include graph distance so cognition can prefer nearby choices without bypassing normal movement.

## Explainability

The owner-only cognition context exposes non-clinical drive components:

- libido base;
- age bonus;
- recovery bonus;
- solitude bonus;
- release pressure;
- recent-24-hour penalty;
- adverse-state penalties;
- current libido-shaped ramp hours.

This is runtime explainability, not a diagnostic model.

## Preserved boundaries

Naturalism v2 does not add:

- a required daily/weekly frequency;
- partnered behavior or Relationship System integration;
- attraction/partner selection;
- testosterone/endocrine inference;
- fertility/reproduction mechanics;
- sexual pathology/clinical diagnosis;
- automatic mood/stress/sleep effects;
- structural anatomy change;
- explicit fantasy/content simulation.

Structural anatomy and authored long-term erectile capacity remain unchanged by ordinary solo behavior.

## Acceptance target

Focused acceptance must prove:

- young/high-libido/well-recovered state receives positive age/recovery contributions;
- the resident-scope solitude term is represented;
- same-day repeat can become legal after the bounded cooldown for Darian's authored high-drive state;
- recent trailing-24-hour activity increases saturation penalty;
- multiple non-bathroom estate spaces are privacy-suitable;
- generic `access=private` alone is insufficient when metadata marks another person's room;
- reachable safe spaces are discovered beyond one graph edge;
- observer privacy and rolling 7-day evidence remain intact;
- structural anatomy/long-term capacity remain unchanged;
- validation uses disposable state and never forces live production behavior.
