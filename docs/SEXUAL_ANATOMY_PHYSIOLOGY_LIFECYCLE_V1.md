# Sexual Anatomy & Physiology Lifecycle v1

Status: implementation contract

## Purpose

Sexual anatomy mixes slow structural development with context-dependent physiology. The engine keeps those concepts separate.

Invariant:

`developmental/genetic structural anatomy + age + optional authored long-term erectile capacity -> bounded structural lifecycle + bounded functional-capacity lifecycle`

Momentary arousal and erection state remain context-driven sexual physiology and are not inferred from ordinary actions.

## Structural anatomy

v1 covers the represented male structural fields:
- `sexual_anatomy.penis_length_in`;
- `sexual_anatomy.penis_girth_in`.

The corresponding genetics fields represent authored adult structural targets, not gym-style trainable maxima.

### Developmental phase

Before the configured maturity age, a represented younger male may develop toward the authored adult target. Growth is bounded by remaining headroom, annual fractional realization and per-settlement clamps. It never exceeds the authored target.

Pubertal research supports androgen-dependent external genital development and strong association with pubertal stage. The v1 envelope is intentionally simple and is not a clinical Tanner-stage prediction model.

### Adult phase

After maturity, ordinary structural dimensions are stable.

The engine intentionally does **not** impose a generic age-related shrink rule on adult structural length/girth. Adult anthropometry studies do not show a consistent enough age relationship to justify deterministic structural loss from age alone.

Pathology, surgery, injury, endocrine disease or other specific causes may later alter structural anatomy only with explicit evidence and a separate policy.

## Long-term erectile functional capacity

The existing profile schema distinguishes momentary `erection_firmness` from longer-term `baseline_erectile_function` and an individual `erection_firmness_cap`.

When both long-term fields are authored/present, v1 supports slow age-linked decline in baseline erectile function after the configured age threshold, bounded by the individual cap and settlement clamps. This is a simulation capacity score, not a clinical questionnaire or diagnosis.

If either baseline or cap is missing, the functional lifecycle is deferred. The engine does not invent an individual sexual-function score from body measurements, RAPS values, training history or population averages.

Longitudinal male-aging studies support age-associated decline in sexual/erectile function, while erection physiology depends on integrated vascular, neurologic and cavernosal smooth-muscle responses.

## Current physiological presentation

Existing fields such as:
- `sexual_anatomy.erectile_state`;
- `sexual_anatomy.erection_firmness`;
- `sexual_state.arousal_level`;

remain context-dependent simulated state under `sexual_physiology_engine`.

This lifecycle does not change them from ordinary eating, training, showering, resting or other unrelated actions. Future sexual-context behavior may drive those states from explicit arousal/interaction/health evidence.

## Activation

Activation preserves represented adult structural measurements numerically and transfers their ownership to `sexual_anatomy_lifecycle_engine`.

For Darian's current exemplar:
- length remains 10.0 in;
- girth remains 5.0 in;
- phase is `adult_stable`;
- no baseline erectile-function/cap score is invented because those values are not currently authored.

All fields are intimate and retain profile sensitivity enforcement.

## Cadence and persistence

The lifecycle settles no more frequently than every 90 simulated days.

Events use `sexual_anatomy_physiology_lifecycle_settled` and record structural phase/values, optional functional projection, state changes and mutation status.

No schema migration or extra LLM call is introduced.

## Scientific references

Primary/review literature used to bound v1:
- Rey RA et al. *The Role of Androgen Signaling in Male Sexual Development at Puberty*. Endocrinology. 2021. PMID 33211805.
- Soydan H et al. *Cross-sectional analysis of penile length in males 13 to 15 years old according to pubertal development stages*. J Urol. 2012. PMID 22902017.
- Dean RC, Lue TF. *Physiology of Penile Erection and Pathophysiology of Erectile Dysfunction*. Urol Clin North Am. 2005. PMID 16291031.
- Travison TG et al. *Changes in sexual function in middle-aged and older men: longitudinal data from the Massachusetts Male Aging Study*. J Am Geriatr Soc. 2004. PMID 15341552.
- Shiri R et al. *The rate of deterioration of erectile function increases with age*. Scand J Urol. 2019. PMID 31023125.
- Promodu K et al. *Penile length in the flaccid and erect states*. J Urol. 1996. PMID 8709382.
- Aslan Y et al. / Habous et al.-type adult anthropometry literature is treated cautiously because age-size associations differ across cohorts; no universal adult structural shrink curve is encoded.

## Validation

Acceptance must prove:
- Darian's adult 10.0/5.0 structural values are preserved exactly on activation;
- adult structural values remain stable without arbitrary age shrink;
- a synthetic pubertal non-Darian male develops toward but never beyond authored adult targets;
- an older synthetic actor with explicitly authored functional baseline/cap can undergo slow bounded functional decline;
- missing functional baseline/cap remains missing rather than being invented;
- privacy/intimate sensitivity remains unchanged;
- production-copy activation does not mutate live production.

## Deferred

- sexual-context arousal/erection behavior transitions;
- pathology/surgery/injury structural effects;
- endocrine disease/treatment models;
- fertility/testicular physiology;
- ejaculation/refractory-period physiology;
- pelvic-floor or medication-specific effects;
- relationship/partner sexual behavior systems.
