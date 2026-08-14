# Body Composition Progression — Research Foundation

Status: **CANONICAL RESEARCH / IMPLEMENTATION PREREQUISITE**
Synchronized: 2026-08-14

## Purpose

Define the physiological evidence and simulation boundaries that must exist before `body.weight_lb` and `body.body_fat_pct` become live simulated fields.

Darian is the first detailed exemplar. The engine must remain actor-generic and reusable for future characters with different sex, age, body size, training history and genetic potential.

This document deliberately separates:

1. **human physiology evidence** — population/experimental findings;
2. **character potential** — canonical individual profile data;
3. **world/content nutrition** — authored food/meal properties;
4. **deterministic simulation policy** — bounded approximations chosen for the runtime.

Population averages must not silently become immutable individual facts.

## Evidence conclusions

### 1. Weight change is dynamic, not a fixed calories-per-pound rule

The classic static `3500 kcal = 1 lb` rule is not appropriate as a general simulation law. NIH/NIDDK work by Hall and colleagues models body-weight change dynamically: energy imbalance changes both fat mass (FM) and fat-free mass (FFM), while energy expenditure and tissue partitioning adapt over time.

The Hall/Forbes two-compartment relationship is useful as a bounded first-order partition model for small settlement intervals:

- FM and FFM usually change together during energy imbalance;
- the fraction of weight change represented by FFM depends strongly on current fat mass;
- the Forbes differential relationship is approximately `dFFM/dBW = 10.4 / (10.4 + FM_kg)`;
- Hall extended the relationship for macroscopic weight changes and incorporated it into dynamic energy-balance models.

For a simulator, use small bounded settlement intervals rather than pretending one constant energy density applies to all weight change.

Primary/official references:
- Hall KD. *Body fat and fat-free mass inter-relationships: Forbes's theory revisited.* Br J Nutr. 2007. PMID 17367567, PMCID PMC2376748.
- Hall KD. *What is the required energy deficit per unit weight loss?* Int J Obes. 2008. PMID 17848938, PMCID PMC2376744.
- Chow CC, Hall KD. *The dynamics of human body weight change.* PLoS Comput Biol. 2008. PMID 18369435, PMCID PMC2266991.
- Hall KD et al. *Quantification of the effect of energy imbalance on bodyweight.* Lancet. 2011. Referenced by the NIDDK Body Weight Planner research page.
- NIDDK, *Research Behind the Body Weight Planner*.

### 2. Sex matters, but not as a crude hypertrophy multiplier

Men and women have different typical absolute lean/fat mass and fat distribution. However, when the same resistance-training intervention is compared, relative hypertrophy responses are often similar; males may gain more absolute tissue because the starting muscle mass is larger.

Therefore:
- sex may participate in resting-energy/reference-body-composition calculations;
- sex-specific population reference ranges are useful plausibility context;
- do **not** encode `male hypertrophy multiplier > female hypertrophy multiplier` as a universal rule.

References:
- Roberts BM et al. *Sex Differences in Resistance Training: A Systematic Review and Meta-Analysis.* J Strength Cond Res. 2020. PMID 32218059.
- Refalo MC et al. *Sex differences in absolute and relative changes in muscle size following resistance training in healthy adults.* PeerJ. 2025. PMID 40028215, PMCID PMC11869894.
- Kelly TL et al. *Estimates of body composition with DXA in adults* (NHANES 1999-2004). Am J Clin Nutr. 2009. PMID 19812179.

### 3. Age matters, but response variance remains large

Age influences body composition and energy expenditure. Older adults can still hypertrophy meaningfully with resistance training, although several datasets show attenuation of some muscle-size responses with advancing age. Individual variation is large enough that age must be a modifier/context term, not a deterministic destiny.

The runtime should therefore:
- derive age from DOB/sim time;
- allow age to influence resting energy expenditure and later recovery/anabolic policy where evidence supports it;
- avoid a sharp age cliff;
- keep individual genetic/training-history factors separate from chronological age.

References:
- Ahtiainen JP et al. *Heterogeneity in resistance training-induced muscle strength and mass responses in men and women of different ages.* Age. 2016. PMID 26767377, PMCID PMC5005877.
- Jones MD et al. *Sex Differences in Adaptations in Muscle Strength and Size Following Resistance Training in Older Adults.* Sports Med. 2021. PMID 33332016.
- Moliné M et al. *Effects of body composition on age- and sex-related differences in resting metabolic rate from a healthy aging cohort.* Exp Gerontol. 2026. PMID 41759925.

### 4. Genetics should be an individual potential envelope, not a population hard cap

Lean mass and muscular response have meaningful heritable components, but genetic response is polygenic and highly individual. Recent and historical work supports substantial inter-individual variability rather than one universal natural-muscle ceiling.

Runtime rule:
- genetic potential comes from character canonical profile/config when available;
- population FFMI/FMI distributions are plausibility references, not hard maxima;
- adaptation should saturate as the character approaches their own canonical potential envelope;
- if a character lacks explicit genetic potential, use conservative population-informed defaults with uncertainty rather than copying Darian.

Darian already has useful canonical fields:
- `genetics.weight_lean_min_lb`
- `genetics.weight_lean_max_lb`
- `genetics.body_fat_floor_pct`
- height and body-measurement maxima.

For Darian, `weight_lean_*` is treated as a **lean-condition body-weight envelope**, not literal fat-free mass. A future body-composition engine may derive a corresponding potential FFM envelope using the character's sustainable low-body-fat condition; it must not rename the stored canonical fact or silently reinterpret it as raw FFM.

References:
- Forbes GB et al. *Lean body mass in twins.* Metabolism. 1995. PMID 7476332.
- Arden NK, Spector TD. *Genetic influences on muscle strength, lean body mass, and bone mineral density: a twin study.* J Bone Miner Res. 1997. PMID 9421240.
- Gu Z et al. *Genome-Wide Association Study of Lean Body Mass Response to Resistance Training in Young Asians.* J Cachexia Sarcopenia Muscle. 2026. PMID 42455518.
- Hubal MJ et al. *Variability in muscle size and strength gain after unilateral resistance training.* Med Sci Sports Exerc. 2005. PMID 15947721.

### 5. Nutrition and energy balance are required causal inputs

The current Observer Sandbox `eat` action changes abstract needs such as hunger/energy but does not persist calorie or macronutrient intake. Those need scores are not interchangeable with kcal or protein grams.

Body composition must therefore **not** infer fat gain/loss directly from `needs.hunger` or `needs.energy`.

Before live FM/FFM progression, add a minimum reusable nutrition/energy evidence layer:
- authored nutrition profiles for edible resources/meals;
- energy intake evidence (kcal) from completed eating actions;
- protein evidence sufficient to modulate resistance-training lean-mass adaptation;
- activity/rest expenditure estimation tied to action duration and actor physiology;
- settlement windows that aggregate evidence without mutating profile values on every meal/minute.

Protein is a modifier, not an unlimited anabolic accelerator. A large meta-regression found no further resistance-training FFM benefit above roughly 1.6 g/kg/day total protein on average. Energy deficits impair lean-mass gain; a meta-regression found deficits around 500 kcal/day prevented lean-mass gains on average, while strength gains could still occur.

References:
- Morton RW et al. *Protein supplementation and resistance-training-induced gains in muscle mass and strength.* Br J Sports Med. 2018. PMID 28698222, PMCID PMC5867436.
- Murphy C, Koehler K. *Energy deficiency impairs resistance training gains in lean mass but not strength.* Scand J Med Sci Sports. 2022. PMID 34623696.

### 6. Activity energy expenditure should use authored action intensity, not one global multiplier

The 2024 Adult Compendium of Physical Activities provides MET values for many activities and explicitly treats MET as a ratio of work metabolic rate to resting metabolic rate. It also warns that the standard 1-MET assumption does not fully account for differences in age, body size, sex and lean mass.

Runtime direction:
- estimate actor resting expenditure from actor physiology/demographics;
- map action/method categories to bounded MET/intensity values;
- scale activity expenditure relative to the actor's resting expenditure rather than assuming every actor burns the same kcal/min;
- use the Older Adult Compendium/reference policy for older actors when that support is implemented.

Reference:
- Herrmann SD et al. *2024 Adult Compendium of Physical Activities: A third update of the energy costs of human activities.* J Sport Health Sci. 2024. PMID 38242596.
- Compendium of Physical Activities, 2024 adult and older-adult tables.

Useful current values include sleeping 1.0 MET, sitting/eating ~1.5 MET, showering 2.0 MET, moderate walking ~3.5-3.8 MET, moderate resistance training ~3.5-5 MET and vigorous resistance/bodybuilding ~6 MET. Exact runtime mappings must be documented simulation policy rather than presented as direct measurements of every possible in-universe action.

## Required body-composition state model

Minimum two-compartment representation:

- `weight`
- `fat mass (FM)`
- `fat-free mass (FFM)`
- `body-fat %`

with invariants:

`weight = FM + FFM`

`body_fat_pct = 100 * FM / weight`

The current profile already declares:
- `body.weight_lb`
- `body.body_fat_pct`
- `body.lean_mass_lb` (derived)
- `body.fat_mass_lb` (derived)
- `body.bmi` (derived).

No schema v5 is required for the first body-composition engine.

`body.lean_mass_lb`, `body.fat_mass_lb`, and BMI should remain derivable views unless a concrete runtime invariant later requires independent persistence.

## Progression architecture

Target causal form:

`actor profile + age/sex + nutrition evidence + completed activity/training evidence + recovery/context + current FM/FFM + genetic potential -> bounded daily/periodic composition settlement -> weight/BF history + audit event`

Rules:
- deterministic engine owns mutation;
- LLM never writes weight/body-fat directly;
- evidence is actor-scoped;
- no Darian-specific branch;
- no retroactive gain when the engine is first activated;
- first live activation bootstraps at the current sim boundary;
- later settlements consume only new evidence;
- every settlement records enough inputs/factors to audit the result;
- implausibly large single-window changes are clamped/rejected;
- genetic floor/ceiling affects saturation/guardrails, not instantaneous snapping;
- body-fat floor is a sustainable lower envelope, not permission for negative fat mass or an absolute medical law for every human.

## Population plausibility references

FFMI/FMI and DXA reference curves can detect wildly implausible states, but must not be used as universal caps because they vary with sex, age, ethnicity/population and athletic status.

References:
- Schutz Y et al. *Fat-free mass index and fat mass index percentiles in Caucasians aged 18-98 y.* Int J Obes. 2002. PMID 12080449.
- Kelly TL et al. NHANES DXA body composition reference data. PMID 19812179.
- Xiao Z et al. Sex- and age-specific DXA body-composition indices in Chinese adults. PMID 27473103, PMCID PMC5602044.

## Immediate implementation sequence

### BC-0 — Simulated profile re-seed safety

Before activating weight/BF, ordinary initialization/deployment must preserve any profile field already owned by a simulation engine (`mode=simulated`). Canonical seed import initializes inactive fields but does not reset live engine-owned state.

### BC-1 — Minimum Nutrition & Energy Balance Evidence

Add the smallest reusable evidence substrate:
- nutrition profile catalog for edible targets;
- completed-eat kcal/protein evidence or equivalent immutable settlement evidence;
- actor-specific resting expenditure estimate;
- action/method intensity mapping;
- aggregate energy/protein/activity evidence over a bounded settlement window;
- no body-composition mutation yet unless all evidence/coverage invariants are satisfied.

### BC-2 — Body Composition Progression Exemplar

Activate coupled `body.weight_lb` + `body.body_fat_pct` for one exemplar actor through the universal engine:
- derive starting FM/FFM;
- use bounded energy partitioning inspired by Hall/Forbes over short settlement intervals;
- resistance-training lean adaptation is separately constrained by training evidence, protein/energy availability, training status and personalized genetic headroom;
- no crude sex hypertrophy multiplier;
- age/sex are inputs only where evidence supports their effect;
- settlement writes both coupled profile fields atomically and records audit history/event.

### BC-3 — Measurement Progression Batch

Only after BC-2 is live/validated, map body-composition and regional training adaptation into circumference changes (waist, chest, arms, thighs, etc.) with anatomical ratio/measurement-specific evidence. Do not derive all circumferences from weight alone.

## Explicit non-goals for the exemplar

Do not add as side effects:
- detailed endocrine simulation;
- menstrual-cycle/hormone-state engine;
- organ-by-organ metabolic model;
- micronutrient engine;
- exact fluid/glycogen fluctuation model;
- obesity/clinical disease treatment simulator;
- universal injury model;
- schema v5.

These may be layered later if a concrete gameplay/simulation requirement justifies them.
