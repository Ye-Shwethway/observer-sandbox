# Body Aesthetic Proportion & Grade Targeting v2

Status: **APPROVED DESIGN CONTRACT — DOCS FIRST / RUNTIME NOT YET IMPLEMENTED**

## Purpose

Extend Creator Character Profile Editing & Grade Targeting so the Body Measurements section can be retargeted by grade without pretending that larger absolute measurements are inherently better.

The Body model grades **proportion quality**, not raw size.

Canonical direction:

`authoritative raw body measurements -> sex-aware derived ratios -> named reference profile -> per-ratio evaluations -> weighted Body composite grade`

Creator inverse targeting runs the same contract in reverse:

`requested Body grade -> target ratio region -> constrained preserve-shape solver -> proposed raw measurements -> forward re-evaluation -> preview -> explicit Apply`

Raw measurements remain authoritative. Ratios and grades remain read-time derived.

This contract extends `docs/CREATOR_PROFILE_EDITING_GRADE_TARGETING_V1.md`; it does not create a second profile editor or persisted grade authority.

---

## Core principles

### 1. Raw size is not a monotonic grade

Do not grade ordinary circumference fields using `larger = better` logic.

Examples:
- a 48-inch chest is not automatically better than a 44-inch chest;
- an 18-inch arm is not automatically better than a 16-inch arm;
- larger thighs/calves are not automatically more aesthetic.

The same measurement can produce a different visual result depending on height, skeletal frame, waist, neighboring measurements, sex-specific morphology, and overall balance.

Therefore:

`raw measurement != aesthetic grade`

`derived proportional relationship -> aesthetic reference evaluation`

### 2. Aesthetic reference is not universal biological truth

The project must not encode one culture-independent immutable formula for human beauty.

Canonical wording:

> **sex-aware aesthetic reference profile informed by empirical attractiveness research and explicit project calibration**

Every target metric must distinguish:
- **empirical anchor** — supported direction, predictor, or approximate optimum from published research;
- **project calibration** — the exact bounded S-band chosen by Observer Sandbox for deterministic grading where literature does not establish one universal interval.

Reference metadata must expose this distinction.

### 3. Male and female reference profiles are separate

Never obtain the female scheme by mechanically inverting or reusing the male scheme.

Initial registry identities:
- `body-aesthetic-male-v2`
- `body-aesthetic-female-v2`

The registry must be extensible without character-specific code.

Character selection is based on represented canonical sex/body-profile facts, not name or hard-coded character identity.

### 4. Health context stays separate from aesthetics

Waist-to-height ratio is useful health/central-adiposity context, but it is not an aesthetic beauty score.

NICE adult guidance classifies waist-to-height ratio:
- 0.40–0.49: healthy central adiposity;
- 0.50–0.59: increased central adiposity;
- >=0.60: high central adiposity.

Observer Sandbox may retain this as a health/context grade or constraint, but the Body **aesthetic** composite must not silently treat health classification as an attractiveness law.

---

## Evidence basis and evidence limits

This contract is deliberately conservative about what research proves.

### Male evidence anchors

Published work supports:
- waist-to-chest ratio (WCR) as an important predictor of male bodily attractiveness;
- lower WCR / stronger inverted-triangle torso as generally preferred in the studied populations;
- an experimentally manipulated low WCR around 0.70 receiving higher attractiveness ratings in one study;
- waist-to-hip ratio around 0.80 as an optimum in one visual-perception study;
- broad shoulders and waist slimness as attractive male torso cues.

The literature does **not** establish one universally exact chest, shoulder, arm, thigh, or calf circumference target for every height/frame/population.

### Female evidence anchors

Published work supports:
- waist-to-hip ratio (WHR) as a meaningful female-body attractiveness cue in many experimental settings;
- approximately 0.70 receiving the highest attractiveness rating among 0.6/0.7/0.8/0.9 conditions in one study;
- female attractiveness depending on multiple interacting body measures rather than WHR alone;
- bust-to-underbust, bust-to-waist, waist-to-hip, weight/body-volume and related shape variables contributing in different studies;
- meaningful cultural/methodological variation in the relative importance of BMI/body volume versus WHR.

Therefore v2 must not claim `female attractiveness = WHR alone`.

### Canonical source references

Implementation/docs may cite the following stable research identifiers rather than embedding unsupported claims:

Male:
- Coy, Green & Price (2014), *Body Image*, PMID **24958664** — low male waist-to-chest ratio and perceived attractiveness/dominance/fitness.
- Swami et al. (2007), PMID **17345919** — male WCR primary attractiveness cue in British/Greek samples.
- Fan et al. (2005), PMID **15705545** — VHI primary cue in sample; reported male WHR optimum around 0.8.
- Horvath (1981), PMID **7212994** — broad shoulders and waist slimness positively rated in male physiques.

Female:
- Del Zotto et al. (2020), PMID **30347463** — manipulated female WHR, highest rating at 0.7 among tested values.
- Gründl et al. (2009), PMID **19319075** — multiple body-measurement ratios jointly predict female attractiveness.
- Pokrywka et al. (2006), PMID **17283934** — BMI and WHR alone are insufficient; other measurements contribute.
- Swami & Tovée (2005), PMID **18089180** — cross-cultural variation and strong BMI/body-size contribution.

Health/context:
- NICE NG246 (current guideline): adult waist-to-height central-adiposity classification.

These sources justify the direction and calibration anchors. Exact project S-bands remain project calibration unless a source directly establishes the interval.

---

## Body metric registry

Each metric definition must include conceptually:

```text
metric_key
reference_profile
numerator_field
denominator_field
display_direction
role = primary_aesthetic | secondary_balance | health_context
weight
target_band
calibration_kind = empirical_anchor | empirical_plus_project | project_calibration
evidence_note
inverse_enabled
```

No grading algorithm should switch on a character name.

---

## Male reference profile v2

### Primary aesthetic metrics

#### A. Waist / Chest

Canonical key:
`body.waist_to_chest_ratio`

Derived from:
`body.waist_in / body.chest_in`

Display may additionally show the intuitive inverse `Chest / Waist`.

Role:
**primary aesthetic**

Evidence:
Male WCR is repeatedly reported as an important cue; lower WCR generally corresponds to a stronger inverted-triangle torso in the studied samples. A value around 0.70 is a useful empirical anchor, but published literature does not justify treating one exact number as universally optimal.

Initial S-band policy:
- use a bounded band centered near the empirical 0.70 anchor;
- exact v2 numeric band is a **project calibration**, not a universal beauty law;
- calibration must be acceptance-tested against representative body profiles before runtime activation.

Recommended initial calibration candidate for implementation validation:
`0.68 .. 0.74`

This candidate is not considered final empirical truth merely because it appears in the project configuration.

#### B. Waist / Shoulders

Canonical key:
`body.waist_to_shoulders_ratio`

Derived from:
`body.waist_in / body.shoulders_in`

Role:
**primary aesthetic**

Existing v1 project band `0.55 .. 0.65` is retained as an initial project calibration because it captures the intended V-taper relationship and existing project continuity. It must be labeled project-calibrated rather than falsely described as a universally established scientific interval.

#### C. Waist / Hips

Canonical key:
`body.waist_to_hips_ratio`

Derived from:
`body.waist_in / body.hips_in`

Role:
**secondary/primary-supporting aesthetic**

Evidence anchor:
one study reported an optimum around 0.80 for male WHR.

Recommended initial project S-band candidate:
`0.78 .. 0.84`

Again, this is an empirical anchor plus project band, not a universal law.

### Secondary muscular-balance metrics

The following relationships are useful for preserving balanced physique shape but do not currently have sufficiently strong universal evidence for exact attractiveness bands:

- arm / chest;
- forearm / arm;
- thigh / waist;
- calf / arm or calf / thigh;
- chest / height;
- shoulders / height.

V2 policy:
- may be represented as **secondary balance metrics**;
- exact bands, if activated, are project calibration;
- they must have lower composite weight than torso silhouette metrics;
- they must not be described as scientifically proven universal ideals;
- v2 inverse solver may initially use them as soft preservation constraints instead of grade-driving metrics.

This lets the solver preserve the character's muscular distribution without inventing unsupported absolute-size grades.

---

## Female reference profile v2

Female grading requires a separate metric registry.

### Primary aesthetic metric

#### A. Waist / Hips

Canonical key:
`body.waist_to_hips_ratio`

Role:
**primary aesthetic**

Evidence anchor:
WHR around 0.70 has strong historical and experimental support as an attractive condition in several study designs, while other studies show that body mass/volume and cultural context can be equally or more important.

Recommended initial project S-band candidate:
`0.67 .. 0.73`

This must be labeled **empirical anchor + project calibration**.

### Additional female metrics

Research supports multi-factor interpretation involving measurements such as:
- bust / waist;
- bust / underbust;
- waist / hip;
- weight/body volume relative to height;
- leg/torso and other shape relationships.

However, Observer Sandbox must not invent missing anatomy/profile fields solely to satisfy a grading formula.

Activation rule:
- a metric becomes grade-driving only when its authoritative raw inputs exist in the shared profile ontology;
- if bust/underbust or equivalent inputs are absent, the engine omits those metrics rather than fabricating values;
- the female composite must expose which metrics were actually available.

Shoulder/hip balance or limb-proportion measures may later be project-calibrated secondary metrics, but are not required for the minimum v2 runtime.

### Female composite caution

A female Body grade must never be represented as a scientifically objective ranking of a person's worth or universal attractiveness.

It is a project-defined visualization/profile grading system based on represented proportions and explicit calibration.

---

## Grade-distance model

Body ratios use a **target-range** family, not monotonic scoring.

For a target interval `[low, high]`:
- inside target region -> S;
- increasing normalized distance outside the target region -> A/B/C/D/E.

The current target-distance mechanism may be reused if it remains deterministic and symmetric around the reference band.

V2 should preserve the existing E/D/C/B/A/S presentation vocabulary for body composites unless/until higher body grades are explicitly defined.

Do not automatically map SS/SSS/X/XX to increasingly extreme ratios. Extreme deviation from an aesthetic target must never become a higher grade merely because a raw dimension is larger or smaller.

---

## Weighted Body aesthetic composite

The current equal-letter-average Body composite is sufficient for v1 observability but too coarse for inverse grade targeting.

V2 composite must be weighted by metric role.

### Male initial weighting policy

Target conceptual distribution:
- torso silhouette primary metrics: **majority weight**;
- secondary muscular-balance metrics: **supporting weight**;
- health/context metrics: **not part of aesthetic score by default**.

Recommended minimum implementation weights when only current primary ratios are available:
- Waist / Chest: 0.45
- Waist / Shoulders: 0.35
- Waist / Hips: 0.20

When additional validated secondary metrics are activated, primary-torso metrics must retain the majority of total aesthetic weight.

### Female initial weighting policy

Until multiple evidence-supported represented inputs exist:
- WHR may be the primary grade-driving metric;
- additional represented bust/waist/underbust or body-volume metrics are added only when their authoritative fields exist and their calibration is documented;
- do not pad a composite with fake or unavailable measures.

Composite output must include coverage metadata so `S from 1 available metric` is distinguishable from `S from a richer 4-metric evaluation`.

### Health context

Waist/height remains separately visible.

It may constrain obviously incoherent inverse proposals where appropriate, but its health grade is not silently averaged into the aesthetic composite.

---

## Body grade targeting

Creator UX target:

`Character -> Profile -> Edit Profile -> Body Measurements -> Grade Target -> E..S -> Preserve / Normalize`

The universe pause/edit-session semantics from `docs/TELEGRAM_CREATOR_PROFILE_EDIT_UX_V1.md` remain unchanged.

Body targeting is still preview-first and atomic.

### Forward verification is mandatory

The inverse solver never writes a grade.

It proposes raw measurements, then the ordinary Body grading engine recomputes:
- all derived ratios;
- each ratio grade;
- weighted Body composite.

If the resulting composite does not equal the requested grade, preview creation fails safely.

---

## Preserve-shape inverse solver — default

Preserve mode is the preferred Body workflow.

Goal:

> Find the nearest valid raw measurement vector that reaches the requested Body grade while preserving the character's existing silhouette and muscular distribution as much as possible.

Conceptual optimization:

`minimize sum(weight_i * normalized_change_i^2) + proportion_drift_penalties`

subject to:
- requested target-grade region;
- sex-aware active reference profile;
- hard field validity constraints;
- anchor-field constraints;
- raw measurements remain positive/valid;
- existing canonical cross-field constraints;
- forward grading verifies the target.

The implementation may use a small deterministic search/optimization routine; it must not use an LLM to invent measurements.

### What preserve means

Preserve mode should minimize unnecessary change to:
- current relative upper/lower-body muscularity;
- current limb-to-torso balance;
- current chest/shoulder relationship except where required by target ratios;
- current overall scale relative to height/frame;
- fields unrelated to active grading constraints.

It should distribute necessary change rather than solve every ratio by distorting one field when a smaller balanced multi-field adjustment exists.

---

## Anchor policy

### Hard anchors by default

Do not change during Body grade targeting unless a future explicit advanced override says otherwise:
- canonical sex/body reference profile selector;
- height;
- represented skeletal/frame facts that are not ordinary soft-tissue measurements.

### Soft anchors

Change only when necessary and penalize larger movement:
- shoulder circumference/breadth representation;
- hip/frame-sensitive measurements;
- body weight where included in a future solver.

### Freely adjustable within valid bounds

Typical circumference variables may be adjusted by the inverse solver when represented:
- chest;
- waist;
- biceps/arms;
- forearms;
- thighs;
- calves;
- other soft-tissue circumference fields explicitly opted into the Body solver.

Actual field classification must come from registry metadata, not field-name string hacks scattered through UI/runtime.

---

## Normalize mode

Body Normalize is explicit and secondary.

It may move primary grade-driving ratios toward deterministic representative points inside the target band's requested grade region, then solve raw measurements around those targets.

Normalize is allowed to reduce more of the existing individual body shape than Preserve.

It must still:
- retain hard anchors;
- respect sex-aware profile selection;
- preserve validity;
- forward-verify the requested grade;
- preview every raw measurement change.

Preserve remains the default UI choice.

---

## Chest/Waist upgrade requirement

Current v1 behavior exposes Chest / Waist only as ungraded derived context.

V2 must upgrade this relationship for male profiles:

- canonical grading direction: `waist / chest`;
- display may show both `Waist / Chest` and inverse `Chest / Waist` for readability;
- male WCR participates in the aesthetic composite and inverse solver;
- female chest/bust relationships require the female-specific metric definition and must not reuse male muscular-chest semantics.

This explicitly fixes the existing v1 gap.

---

## Measurement coverage and missing data

Body grading/targeting must be coverage-aware.

Rules:
- never invent missing raw measurements;
- never assume a sex-specific metric is meaningful if required inputs are absent;
- display active metric count / eligible metric count in diagnostic or preview metadata;
- composite can be computed from a documented minimum metric set;
- Body inverse targeting must reject when there is insufficient represented data to solve safely.

Minimum male targetable set for initial runtime:
`height + shoulders + chest + waist + hips`

Minimum female targetable set for initial runtime:
`height + waist + hips`, with richer female targeting enabled automatically as additional supported represented inputs exist.

---

## Creator preview requirements

Before Apply, show:
- character;
- sex-aware reference profile used;
- requested Body target grade;
- Preserve/Normalize mode;
- current Body composite and metric coverage;
- projected Body composite and metric coverage;
- active ratio grades old -> new;
- every raw measurement old -> proposed;
- hard anchors left unchanged;
- any unsupported/unavailable metrics omitted and why;
- health/context warning when relevant without treating it as aesthetic authority.

Apply uses the existing Creator profile atomic mutation/reconciliation pipeline.

Creator Body targeting must not emit ordinary earned-progression notifications for direct control changes.

---

## Progression, Memory, Cognition and future Mind reconciliation

The existing Creator Profile Editing v1 reconciliation contract applies unchanged:
- raw profile history/audit is retained;
- progression/change notification baselines re-anchor;
- direct Creator changes are not announced as organically earned body progression;
- no broad Character Memory wipe;
- only explicitly profile-derived stale semantic self-knowledge may be retired;
- unrelated episodic/semantic Memory remains;
- historical Cognition Context is never rewritten;
- future cognition reads the new authoritative measurements;
- once Mind F2-F7 exist, only invalidated active Mind artifacts are reevaluated by their owning subsystem; historical Mental Episodes remain historical records.

No Body grade-target operation is a character action or autobiographical event.

---

## Telegram UX

Extend the existing paused edit UX; do not create a separate Body editor.

Preferred path:

`Characters -> Character -> Profile -> Edit Profile -> Body Measurements`

For Creator only, Body Measurements should expose:
- individual `Edit Value` as today;
- `Grade Target` once v2 inverse runtime is implemented.

Grade Target flow:
1. choose E/D/C/B/A/S;
2. default `Preserve Shape` or explicit `Normalize`;
3. receive complete preview;
4. Apply / Cancel;
5. editing session remains paused until `Done Editing`.

Authorized non-owner observers remain read-only.

---

## Implementation structure direction

Avoid a monolithic body editor.

Recommended boundaries:
- `grading.py` or a bounded body-grading module owns sex-aware metric/reference definitions and forward evaluation;
- a separate bounded Body inverse-target solver owns raw-measurement proposal generation;
- `creator_profile_edit.py` remains generic Creator proposal/apply authority;
- Telegram only routes/selects/displays and never implements grading math;
- no character-specific implementation branches.

The same forward evaluator used for ordinary Profile display must verify every inverse proposal.

---

## Runtime acceptance requirements

When implementation begins, focused tests must prove at minimum:

1. raw body measurements remain ungraded as monotonic `larger = better` values;
2. male Waist/Chest is promoted from context-only to a target-range graded metric;
3. sex-aware registry selects male/female reference semantics generically;
4. male forward grading evaluates current authoritative ratios and weighted composite deterministically;
5. female forward grading uses only represented supported metrics and exposes coverage;
6. Waist/Height remains separate health/context classification rather than aesthetic composite authority;
7. `Body -> Grade B -> Preserve` produces a deterministic raw-measurement proposal whose forward evaluation is Grade B;
8. Preserve changes the smallest reasonable set/magnitude of measurements and keeps hard anchors unchanged;
9. Normalize reaches the target while remaining explicit and deterministic;
10. insufficient measurement coverage rejects safely without inventing values;
11. preview shows all changed raw values and ratio/composite consequences before mutation;
12. Apply remains atomic and uses existing Creator audit/reconciliation semantics;
13. Body targeting from Telegram remains inside the paused Creator edit session and does not auto-resume after Apply;
14. allowed non-owner users cannot enter Body grade targeting;
15. no Darian-specific solver path exists;
16. no LLM call is required for grading or inverse solving;
17. full existing grading/profile/autonomy regression remains green.

Production acceptance must not deliberately distort Darian merely to prove the control. Disposable initialized data is sufficient for mutation acceptance; production verification may remain read-only unless the Creator intentionally chooses a real correction.

---

## Non-goals for v2

Do not add:
- universal objective-beauty claims;
- ethnicity/culture-specific character steering;
- monotonic raw circumference grades;
- persisted Body grade labels;
- extreme measurements receiving higher grades merely for being extreme;
- one male ratio reused as female anatomy semantics;
- fabricated bust/underbust/body-volume values;
- LLM-generated measurements;
- Darian-specific proportions;
- automatic body progression or physique redesign merely because grade targeting exists;
- a second profile mutation store;
- broad Memory reset;
- Mind Engine behavior.

---

## Approved product sequence

This is a bounded refinement inserted before MIND-F2 because the Creator has explicitly chosen to complete Body grade targeting while the Creator Profile Editing architecture is active.

Sequence:

`Body Aesthetic Proportion & Grade Targeting v2 docs -> forward grading/registry refinement -> deterministic inverse Body solver -> paused Telegram Body Grade Target UX -> focused tests + final CI -> merge/deploy/verify -> continuity sync -> MIND-F2`

No next real production character seed is authorized by this refinement.
