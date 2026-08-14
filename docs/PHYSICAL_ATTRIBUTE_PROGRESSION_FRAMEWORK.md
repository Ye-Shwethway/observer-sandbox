# Physical Attribute Progression Framework v1

Status: ACTIVE DEVELOPMENT

## Purpose

Physical Attribute Progression Framework v1 extracts the shared deterministic lifecycle already proven separately by Strength, Stamina and Agility, then uses one actor-generic policy-driven engine for the remaining physical attributes: Speed, Reflexes, Endurance and Flexibility.

Darian is the first production exemplar. His current scores and training history are inputs, not constants in the engine. The same framework must operate on any compatible actor id with the required profile fields and authored evidence.

## Shared lifecycle

The reusable progression form is:

`actor_id + current profile value + eligible completed-action evidence + attribute policy + recovery/context + limits -> settlement + profile history + event evidence`

The shared lifecycle is:
1. scan completed-action evidence for the selected actor and attribute policy;
2. exclude stimulus events already consumed by prior settlements;
3. require the attribute-specific recovery interval and a valid systemic recovery state;
4. apply level difficulty and recent-stimulus saturation;
5. realize bounded positive adaptation up to the configured natural ceiling;
6. integrate detraining over eligible inactivity windows;
7. write the profile value/history only when the authoritative value actually changes;
8. write an auditable attribute-scoped settlement event and advance the cursor.

The first settlement for a newly activated attribute is bootstrap-only: historical evidence through that boundary is consumed without changing the score. Deployment therefore cannot award retroactive gains from old sessions.

## Compatibility with Strength, Stamina and Agility

Strength, Stamina and Agility remain on their already-proven v1 implementations in this slice. They are not forcibly migrated merely to make the source tree look uniform. Their behavior established the lifecycle above; the new generic engine is the minimum safe extraction for structurally equivalent follow-ons.

A later consolidation may move proven domains onto the shared implementation only if it has a concrete benefit and preserves their domain-specific evidence/recovery semantics.

## Policy layer

Canonical policy: `config/physical_attribute_progression.v1.json`.

The engine contains no Darian branch and no hard-coded profile starting values. Attribute policies define field key, eligible training method ids/weights, stimulus normalization, recovery interval, level curve, saturation window, ceiling and detraining parameters.

Current v1 evidence contracts:

- **Speed** — `speed_agility_drills` from the Speed & Agility Station. This represents acceleration/movement-velocity practice.
- **Reflexes** — `ai_combat_simulation` from the AI Combat Simulation System. v1 deliberately requires reactive authored simulation rather than crediting every combat drill.
- **Endurance** — sustained mixed-work methods: `heavy_bag_rounds`, `obstacle_conditioning`, and `combat_pit_drills`. Pure aerobic treadmill/rowing/altitude work is excluded so Endurance does not duplicate Stamina.
- **Flexibility** — `mobility_stretching` from the Mobility & Stretching Area in the Home Gym. The target exists specifically because the previous world had no causally valid flexibility evidence surface.

Training Method Semantics remains evidence metadata only; it does not own progression formulas.

## Stamina versus Endurance

Stamina remains the cardiovascular/work-capacity reserve primarily trained by pure conditioning methods.

Endurance measures sustained performance under accumulated mixed workload and fatigue. It therefore uses prolonged mixed combat/obstacle conditioning rather than silently inheriting Stamina's aerobic evidence set.

The two attributes may correlate in a richer future physiology model, but v1 keeps their causal evidence distinct instead of double-crediting one workout to two semantically identical engines.

## Recovery, saturation and detraining

A stimulus remains pending until its configured full-recovery interval has elapsed. Systemic fatigue hard-blocks positive realization, and the existing recovery-quality function scales adaptation while preserving deterministic authority.

Recent same-domain training reduces marginal gain through a saturation factor. Detraining begins only after an attribute-specific grace period and is integrated across simulated time, with new valid training resetting the inactivity segment.

A settlement consumes a stimulus only when it is mature and eligible for realization. High fatigue or insufficient recovery therefore does not destroy evidence.

## Runtime activation

`service.py` runs the existing Strength/Stamina/Agility settlement hooks after a completed action, then invokes the new physical-attribute batch once at the same completed-action boundary. The framework is event-driven; it does not create extra cognition/model calls and it does not run on wall-clock polling alone.

Settlement failures remain isolated from autonomy scheduling just like the existing progression hooks. The simulation/action engine remains authoritative for the completed action itself.

## World/evidence addition

World revision `thorne-estate-v3.3-physical-attribute-training` adds one bounded train-capable object to the existing Home Gym:

- `obj_thorne_estate_gym_mobility_stretching` — **Mobility & Stretching Area**

Training Method Semantics maps it to `mobility_stretching` with movement/range-of-motion metadata. No new location, inventory subsystem or schema migration is required.

## Acceptance boundary

The slice is acceptable when:
- one shared actor-generic engine serves all four new attributes;
- a synthetic non-Darian actor can progress through the same engine without Darian identity leakage;
- evidence selection remains attribute-specific and Stamina-like pure cardio is not credited to Endurance;
- Flexibility has a real trainable world resource and authored training method;
- bootstrap consumes historical evidence without retroactive score mutation;
- replay at the same settlement boundary is idempotent;
- profile history and settlement events identify the exact attribute/source;
- existing Strength/Stamina/Agility behavior remains compatible;
- relevant CI and corrected stateful acceptance harnesses are green;
- no schema v5 or validation-induced provider call is introduced.

## Production verification

Deployment/readback verifies service health, schema v4, world revision, cognition/fallback preservation and presence of the new trainable resource. Do not accelerate production or inject a training action merely to force a live attribute gain. Natural completed actions will establish bootstrap settlements first; subsequent naturally occurring eligible training/recovery may provide live progression evidence.
