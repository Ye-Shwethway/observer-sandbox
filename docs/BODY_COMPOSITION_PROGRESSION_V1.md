# Body Composition Progression v1 — BC-2

Status: **IMPLEMENTATION CANDIDATE**
Synchronized: 2026-08-14

## Purpose

Activate `body.weight_lb` and `body.body_fat_pct` as coupled simulated fields using persisted nutrition/expenditure/training evidence, without retroactive mutation or an LLM-owned physiology path.

Core invariant:

`actor profile + complete bounded energy/nutrition evidence + resistance-training evidence + recovery + genetic envelope -> deterministic daily FM/FFM settlement -> coupled Weight/BF history + audit event`

`weight = fat mass + fat-free mass`

`body_fat_pct = 100 * fat mass / weight`

Fat mass, fat-free mass and BMI remain derived views rather than independently persisted state.

## Activation boundary

The first post-deployment completed-action boundary bootstraps BC-2 for the actor:

- current numerical Weight and Body Fat are preserved exactly;
- both fields switch to `mode=simulated`, authority `physiology_engine`;
- activation writes auditable profile-history rows and a `body_composition_progression_settled` bootstrap event;
- all pre-activation nutrition/training history is excluded from future mutation.

There is no retroactive gain/loss on activation.

## Settlement cadence and evidence gate

v1 uses 24 simulated-hour windows.

A window mutates composition only when BC-1 reports complete evidence with at least 95% covered action time and no required missing intake/expenditure evidence.

If a window is incomplete:

- Weight/BF do not change;
- an explicit `deferred_incomplete_evidence` audit event records the missing/coverage context;
- the cursor advances past that incomplete window so one historical gap cannot permanently block all future complete windows.

Missing evidence is never interpreted as a calorie deficit.

## Passive energy partition

For small daily settlements, v1 uses the canonical Forbes/Hall first-order direction:

`dFFM/dBW = 10.4 / (10.4 + FM_kg)`

The energy density of the resulting mixed tissue change uses:

- fat-mass change: 39.5 MJ/kg;
- lean-mass change: 7.6 MJ/kg.

These values follow Hall's bounded body-composition treatment and deliberately replace a fixed `3500 kcal = 1 lb` rule.

The passive partition component is capped at 0.5 lb absolute body-weight change per 24-hour settlement as a simulation plausibility guard. This is a clamp, not a claim that real tissue change normally reaches that value.

Primary references:

- Hall KD. *Body fat and fat-free mass inter-relationships: Forbes's theory revisited.* Br J Nutr. 2007. PMID 17367567, PMCID PMC2376748.
- Hall KD. *What is the required energy deficit per unit weight loss?* Int J Obes. 2008. PMID 17848938, PMCID PMC2376744.
- Chow CC, Hall KD. *The dynamics of human body weight change.* PLoS Comput Biol. 2008. PMID 18369435.

## Resistance-training recomposition

Resistance-training lean adaptation is deliberately separate from passive energy partition.

Only completed training-method evidence whose `workload_channels` contains `resistance` qualifies. Cardio, combat-only, tactical and mobility sessions do not silently become hypertrophy stimulus.

The bounded daily lean-adaptation signal is constrained by:

- resistance effective minutes;
- protein availability, saturating at the policy reference of 1.6 g/kg/day rather than increasing without bound;
- energy availability, fading to zero around a 500 kcal/day deficit;
- current recovery quality;
- character-specific genetic FFM headroom derived from the authored lean-condition body-weight ceiling and sustainable BF floor when available.

The v1 pre-modifier maximum is 0.03 lb FFM/day, then multiplied by all constraints and genetic saturation. This is a conservative simulation rate limit, not a population promise.

The small RT recomposition energy cost is financed from fat-energy stores at the Hall tissue-energy-density ratio and cannot push the character through the authored sustainable BF floor.

Protein/energy references:

- Morton RW et al. Br J Sports Med. 2018. PMID 28698222, PMCID PMC5867436.
- Murphy C, Koehler K. Scand J Med Sci Sports. 2022. PMID 34623696.

## Genetic and plausibility guards

Character genetics are an envelope, never an instantaneous snap target.

For actors with `genetics.weight_lean_max_lb` and `genetics.body_fat_floor_pct`, the engine derives a potential FFM ceiling from that lean-condition envelope. Adaptation smoothly saturates as current FFM approaches it.

The body-fat floor is treated as a sustainable lower envelope. It prevents settlement from driving FM beneath the character-specific floor, but does not make that floor a universal medical law.

Broad hard safety bounds also reject implausible Weight/BF output.

## Atomicity and audit

A successful settlement writes Weight and Body Fat together inside one SQLite savepoint/transaction.

Each changed field receives a `character_profile_history` row. The settlement event snapshots:

- start/end sim time;
- complete BC-1 energy/nutrition window;
- resistance effective minutes;
- Forbes partition share and tissue-energy density;
- passive FM/FFM deltas;
- protein/training/energy/recovery/headroom factors;
- RT FFM gain and FM energy cost;
- fat-floor guard state;
- old/new Weight, BF, FM, FFM and BMI.

No extra model call occurs.

## Universal-character rule

The reusable engine contains no Darian branch. Darian is the first production-complete actor because his profile already contains Weight, BF, Height and explicit genetic envelopes.

An actor lacking an explicit genetic envelope uses a conservative uncertainty factor rather than inheriting Darian's values.

## Validation

Required before production activation:

- activation preserves numerical Weight/BF while switching simulation ownership;
- complete 24h evidence creates bounded coupled mutation;
- incomplete evidence creates no body mutation;
- only resistance workload channels contribute RT lean adaptation;
- FM + FFM = Weight and BF% derives consistently;
- both profile fields/history/event commit atomically;
- disposable production-copy acceptance succeeds with zero live-production mutation;
- full CI and inherited physical-progression acceptance remain green.

## Explicit non-goals

BC-2 does not add:

- regional body measurements — BC-3;
- fluid/glycogen fluctuation;
- endocrine or micronutrient simulation;
- disease/clinical weight-management logic;
- crude sex hypertrophy multipliers;
- schema migration;
- additional LLM calls;
- broad Mind/Behavior engines.

## Next slice

After production activation/readback, proceed to **BC-3 — Body Measurement Progression Batch** so the remaining circumference fields can become simulated from composition + regional training/anatomical/genetic context rather than body weight alone.
