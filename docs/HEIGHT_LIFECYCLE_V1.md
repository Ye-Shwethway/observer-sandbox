# Height Lifecycle v1

Status: implementation contract

## Purpose

Height is a structural lifecycle value, not an ordinary training circumference and not a daily random physiological variable.

Invariant:

`actor DOB/sex + current structural height + authored genetic height envelope + simulation time -> developmental growth | adult stability | age-related decline -> bounded structural height settlement`

The engine is actor-independent and contains no Darian branch.

## Biological foundation

Longitudinal bone growth occurs at epiphyseal growth plates and ends when growth plates senesce/fuse. Pubertal growth and growth-plate fusion are controlled by endocrine and local factors; after fusion, ordinary longitudinal bone growth is complete.

Longitudinal adult cohorts also show real age-related stature loss, distinct from birth-cohort effects. Published estimates differ on exact onset/rate, so this v1 uses a conservative configurable approximation rather than claiming one universal curve.

Primary references used for the v1 policy:
- Cho JH, Jung HW, Shim KS. *Growth plate closure and therapeutic interventions*. Clin Exp Pediatr. 2024. PMID 39463341.
- van der Eerden BCJ, Karperien M, Wit JM. *Systemic and local regulation of the growth plate*. Endocr Rev. 2003. PMID 14671005.
- Sorkin JD, Muller DC, Andres R. *Longitudinal change in height of men and women*. Am J Epidemiol. 1999. PMID 10547143.
- Huang W et al. *Physical Stature Decline and the Health Status of the Elderly Population in England*. Econ Hum Biol. 2014/2015. PMCID PMC4103973.

## Activation

Activation preserves the authored numerical height exactly and changes ownership to `height_lifecycle_engine`.

The activation event records:
- activation height;
- age;
- lifecycle phase;
- genetic maximum;
- settlement cursor.

For Darian's current adult exemplar, 76.0 in is preserved and the correct phase is `adult_stable`.

Missing DOB, height or genetic-height envelope fails closed as `deferred_missing_inputs`; the engine does not claim the field.

## Phases

### Developmental growth

Before the configurable maturity age, height may increase toward `genetics.height_max_in`.

Growth is bounded simultaneously by:
- remaining genetic headroom;
- maximum inches per simulated year;
- a fraction of remaining headroom realizable per year;
- per-settlement absolute clamp.

The engine never grows structural height beyond the authored maximum.

This is a simulation envelope, not a clinical prediction model and not a substitute for bone-age/puberty/endocrine data. A future richer developmental model may add those signals without changing the actor-independent authority boundary.

### Adult stability

After developmental maturity and before the configured decline age, ordinary structural height is stable.

A stable settlement is a valid lifecycle result, not missing functionality. No random daily drift is introduced.

### Age-related decline

From the configured decline age, the engine permits slow age-linked structural stature loss. v1 uses small sex-conditioned annual fractions inspired by longitudinal population observations, with a configurable older-age acceleration and hard absolute/lifetime bounds.

Pathological height loss from fracture, severe osteoporosis, spinal deformity or other disease is not inferred from age alone and remains deferred to evidence-backed health/injury integration.

## Cadence

Height settles no more often than every 90 simulated days. This avoids meaningless action-by-action numerical noise for a slow structural variable.

## Structural vs observed height

`body.height_in` is structural stature.

Temporary within-day variation from posture, spinal compression/decompression, measurement technique or similar effects is intentionally excluded. If needed later, it should be represented as a separate observed/current-height field rather than rewriting structural height.

## Ordering

The service settles Height Lifecycle before BC-2 Body Composition. If structural height legitimately changes, downstream BMI/height-dependent derived views can therefore consume the current stature.

## Validation

Acceptance must prove:
- adult Darian activation preserves 76.0 in numerically;
- an adult plateau remains exactly stable over time;
- a synthetic younger non-Darian actor grows toward but never beyond an authored height maximum;
- a synthetic older non-Darian actor undergoes slow bounded decline;
- missing lifecycle inputs fail closed without claiming authority;
- ordinary deployment/re-seed cannot overwrite a simulated height after activation;
- no extra model call or schema migration is introduced.

## Deferred

- bone-age or Tanner-stage simulation;
- endocrine disorders/treatments;
- growth-plate injury;
- osteoporosis/vertebral-compression pathology;
- daily observed-height fluctuation;
- skeletal deformity mechanics.
