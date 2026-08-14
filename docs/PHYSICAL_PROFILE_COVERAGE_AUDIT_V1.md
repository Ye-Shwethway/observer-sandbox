# Physical Profile Coverage Audit v1

Status: ACTIVE AUDIT CONTRACT

## Purpose

This audit closes the Physical Profile Completion Gate by separating fields that are genuinely complete from fields that merely exist in schema or canonical seed data.

A physical/profile field is classified as one of:
- `canonical_structural` — authored stable anatomy/appearance;
- `derived` — computed from authoritative inputs and never independently mutated;
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

## Intentional deferrals that do not block physical-profile structure

The following are valid schema/runtime domains but do not need implementation merely to claim structural physical-profile coverage:
- injury and illness systems;
- resting/current heart rate;
- blood pressure;
- body temperature;
- sexual-context transitions for arousal, erectile state and momentary firmness.

These are future health/context systems. Their absence must remain explicit, not silently replaced with static fake values.

## Required follow-up findings

The audit found four fields whose current representation can become contradictory or whose declared authority is not actually implemented.

### 1. `body.abdominal_definition`

Current problem: canonical text such as “well-defined 8-pack” can remain unchanged while body-fat/composition changes.

Required direction: derive/present abdominal definition from current body composition plus authored anatomy/visibility traits. Do not mutate it as an independent progression stat.

### 2. `appearance.skin_quality`

Current problem: schema assigns `physiology_engine`, but no deterministic physiology/health/appearance implementation owns it.

Required direction: either implement a bounded current-state derivation from supported health/recovery/nutrition evidence or explicitly reclassify it as intentionally static until such evidence exists. Do not leave a fake dynamic authority.

### 3. `appearance.pars`

Current problem: schema marks PARS derived under `appearance_engine`, but current authored compatibility values are not a live appearance derivation.

Required direction: establish the minimal derived appearance contract, keeping stable facial structure separate from mutable body/state presentation. The engine must not allow body-composition change to silently contradict the displayed overall physical appeal semantics.

### 4. `sexual_anatomy.sensitivity`

Current problem: schema assigns `sexual_physiology_engine`, but there is no current-state/lifecycle owner for this field. Darian also has the distinct RAPS-SA sensitivity score, which must not be silently treated as the same physiological variable.

Required direction: define the physiological field’s semantics and canonical/runtime authority before relationship gameplay consumes it. Avoid duplicate-authority aliasing with `raps_sa.sensitivity`.

## Completion gate

The audit itself does **not** mark the Physical Profile Completion Gate complete.

Gate becomes complete only when the four required follow-up fields above are either:
1. given a real deterministic/derived owner consistent with their semantics; or
2. explicitly reclassified as intentionally static with a truthful authority where dynamic simulation is not yet justified.

Deferred context/health domains do not block the gate because they are separate future systems rather than contradictions in currently represented profile facts.

After this gate closes, the next canonical work remains Telegram Profile schema-driven section UX, followed by Skill Progression.

## Acceptance

Audit acceptance must prove:
- every in-scope body, appearance, sexual-anatomy and physical-genetic field has an explicit classification;
- intimate fields preserve sensitivity classification;
- known lifecycle-owned fields are not mislabeled as canonical-only;
- the four required follow-ups remain machine-readable blockers until resolved;
- no runtime/profile value is mutated by the audit itself.
