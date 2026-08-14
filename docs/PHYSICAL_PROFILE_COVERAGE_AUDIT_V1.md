# Physical Profile Coverage Audit v1

Status: COMPLETE — PHYSICAL PROFILE COMPLETION GATE CLOSED

## Purpose

This audit separates fields that are genuinely complete from fields that merely exist in schema or canonical seed data.

A physical/profile field is classified as one of:
- `canonical_structural` — authored stable anatomy/appearance;
- `derived` — computed from authoritative fields and not independently progressed;
- `simulated_dynamic` — runtime state owned by a deterministic engine;
- `lifecycle_driven` — slow structural or long-term physiological state;
- `intentionally_static` — deliberately static for current scope;
- `coverage_gap` — semantics imply dynamic/derived behavior but the owning implementation is incomplete.

Canonical machine-readable classification: `config/physical_profile_coverage.v1.json`.

## Complete structural/body coverage

### Body composition

Complete:
- Weight and body-fat percentage — BC-2 simulated authority;
- lean mass, fat mass and BMI — derived from current composition/height;
- no second weight-decay authority.

### Structural height

Complete through Height Lifecycle v1:
- developmental growth when applicable;
- ordinary adult structural stability;
- bounded age-related later-life decline;
- no daily posture/compression noise written into structural stature.

### Circumferences

Complete for current scope through BC-3 + Training Anatomy + Regional Measurement Detraining:
- neck;
- shoulders;
- chest;
- waist;
- hips;
- relaxed/flexed biceps;
- triceps;
- forearms;
- thighs;
- calves.

Training-acquired post-activation excess can regress regionally without crossing authored activation anatomy, and systemic FFM loss is not double-counted.

### Male structural sexual anatomy and long-term erectile physiology

Complete for current scope:
- structural length/girth lifecycle;
- authored adult genetic structural targets;
- required male canonical `baseline_erectile_function`;
- required male canonical `erection_firmness_cap`;
- age-linked long-term functional decline only where lifecycle policy applies;
- momentary erection/arousal remains separate runtime state.

Darian exemplar inputs are 10.0 in length, 5.0 in girth, 95/100 baseline erectile function and 98/100 firmness cap. These are character-specific data, not universal constants.

## Physical Presentation Closure v1

The original audit found four misleading/incomplete representations. They are now closed without introducing a broad appearance or health engine.

### Abdominal structure vs visible definition

`body.abdominal_structure` is now the authored structural fact. Darian's canonical value is `rare 8-pack configuration`.

`body.abdominal_definition` is now a deterministic materialized derived value. It is refreshed from current body-fat percentage relative to the actor's authored sustainable body-fat floor:
- within 1.5 percentage points of the floor: `peak definition`;
- within 4 points: `high definition`;
- within 7 points: `moderate definition`;
- otherwise: `limited definition`.

The thresholds are relative to the actor's own authored floor rather than universal sex/population appearance cutoffs. The derived value is a presentation cache under `appearance_engine`, not an independent progression authority.

This prevents a body-composition change from leaving a permanently stale canonical “well-defined” description while preserving structural abdominal configuration independently.

### Baseline skin quality

`appearance.skin_quality` no longer advertises a nonexistent live physiology engine. It is classified as intentionally static baseline appearance under `profile_core` until a real health/skin current-state model is justified.

### PARS

`appearance.pars` is the authored canonical physical-appeal anchor under `profile_core`, rather than a fake derived field owned by a nonexistent appearance engine. A future context-sensitive appearance/presentation score may be added separately without silently changing the canonical attractiveness anchor.

### Genital sensitivity

`sexual_anatomy.sensitivity` remains an intimate current-physiology field under `sexual_physiology_engine`, but is explicitly deferred until sexual/health context supplies real evidence. It is not an alias for the separate RAPS-SA sensitivity trait and does not block structural physical-profile completion.

## Intentional deferrals that do not block the gate

The following are valid future context/health domains and remain explicit rather than being populated with fake static values:
- injury and illness systems;
- resting/current heart rate;
- blood pressure;
- body temperature;
- sexual-context transitions for arousal, erectile state, momentary firmness and current genital sensitivity.

## Completion gate

**Physical Profile Completion Gate: COMPLETE for current scope.**

The gate closes because all represented physical facts now have truthful ownership/classification and the audit has no unresolved representation blockers. Deferred health/context domains are separate future systems rather than contradictions in currently represented profile facts.

The next canonical work is Telegram Profile schema-driven section UX, followed by Skill Progression.

## Acceptance

Closure acceptance proves:
- Darian's authored rare 8-pack structure is preserved independently from visible definition;
- visible abdominal definition follows authoritative body-composition inputs deterministically;
- skin-quality and PARS schema authority no longer claim nonexistent engines;
- genital sensitivity remains intimate and explicitly context-deferred rather than aliased to RAPS-SA;
- `config/physical_profile_coverage.v1.json` has no required blockers and marks physical completion true;
- disposable production-copy validation performs no live production mutation or model/Telegram call.
