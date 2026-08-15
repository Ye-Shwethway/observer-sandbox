# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Python/SQLite runtime and live world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutation.
- Telegram is an observer/control adapter, never a simulation engine.
- Preserve the LEGO runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are first rich production exemplars, never reusable-engine identity.
- Reusable runtime/cognition/progression/query/control/inventory/nutrition/training logic is actor/entity/definition-id driven.
- Prefer minimum-runnable reversible slices.
- Use one bounded exemplar for a genuinely new invariant, then batch structurally equivalent follow-ons.
- Default flow: `branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Use production-copy validation for concrete stateful/migration risk; never accelerate or directly mutate production merely to manufacture acceptance evidence.
- Internal audit receipts remain queryable evidence; user-facing activity/history surfaces should expose character activity rather than engine bookkeeping.

## Current verified deployment baseline

Latest runtime deployment: **Deploy #196 / run `31869399038` SUCCESS**, Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar, PR #104 merge `a8c86705700f689024c75fe91e00be9361ae557a`.

Post-merge:
- main CI #790 / run `31869399041`: SUCCESS;
- Skill Progression Foundation v1 Acceptance #3 / run `31869399147`: SUCCESS on main.

Deploy readback at approximately `2026-08-15T06:25:31Z` verified:
- service healthy/active;
- schema version 5;
- autonomy enabled in normal mode at 1.0x;
- Telegram API connected with owner/allowed-user configuration present;
- Gemini `gemini-3.1-flash-lite` remained the primary cognition binding;
- Groq `qwen/qwen3.6-27b` remained tested fallback evidence;
- live Hand-to-Hand query presentation remained at its represented pre-progression baseline after initialization/bootstrap, proving no retroactive score jump occurred during deploy.

No live combat session was forced or accelerated to manufacture a Skill Progression occurrence. Natural future eligible combat practice may supply live occurrence evidence.

## Completed foundations

Current completed runtime/profile foundations include:
- schema v4 composable runtime foundation, operationally extended by schema v5 inventory stacks;
- P0/P0.5 runtime/provider foundation;
- P1 continuous autonomy;
- P2 Telegram Observer/Profile/Control and P2.3 Creator AI Control v1;
- Runtime Cognition Fallback v1;
- Telegram Home lifecycle;
- Universal Character Engine;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard;
- fatigue/recovery, targeted training, readiness/effectiveness/effective load;
- Minimum Training Stimulus + Session Load/Recovery Guard;
- causal needs + sleep/circadian behavior;
- Physical Attribute Progression Framework v1 for Strength, Stamina, Agility, Speed, Reflexes, Endurance and Flexibility;
- universal inventory/eating/nutrition slices through Meal Choice Intelligence;
- BC-2 Body Composition and BC-3 Body Measurement progression;
- Training Method Semantics v2;
- Training Anatomy / Movement Semantics v1;
- Regional Measurement Detraining v1;
- Height Lifecycle v1;
- Sexual Anatomy & Physiology Lifecycle v1;
- Male Erectile Physiology Canonical Contract;
- Physical Profile Coverage Audit v1;
- Physical Presentation Closure v1;
- Telegram Profile Schema-Driven UX;
- Solo Sexual Regulation v1;
- Universal Profile Grading Framework v1 + Profile Grading Coverage v1;
- Character Change Observability & Notification Foundation v1;
- **Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar**.

Detailed semantics and historical validation evidence live in the corresponding canonical docs rather than being duplicated exhaustively in this roadmap.

## Item / eating foundation

Invariant:
`universal definition -> concrete stack -> reachable action context -> structured quantity -> deterministic validation -> state transition + immutable evidence`

Completed:
- Inventory Foundation v1 — PR #71 / Deploy #177;
- Inventory Operations v1 — PR #73 / Deploy #178;
- Food Nutrition Semantics & Visibility v1 — PR #74 / Deploy #179;
- Eating Behavior v1 — PR #76 / Deploy #180;
- Meal Choice Intelligence v1 — PR #77 / Deploy #181.

Do not add automatic restocking, economy/currency or generalized crafting as side effects of unrelated slices.

## Body / physical profile authority

Canonical authority remains:
- Weight/BF/FM/FFM — BC-2;
- circumferences — BC-3 + Training Anatomy + Regional Detraining;
- structural Height — Height Lifecycle;
- structural male sexual anatomy — Sexual Anatomy Lifecycle;
- long-term erectile baseline/cap — Sexual Physiology/canonical male profile contract;
- current sexual state — context-driven runtime physiology;
- composition-linked visible abdominal definition — derived presentation;
- stable appearance anchors remain canonical until a real dynamic owner exists;
- broader health vitals/injury/illness are future domains, not fake static simulation.

Research locks remain:
- no static universal `3500 kcal = 1 lb` rule;
- Weight/FM/FFM/BF% are coupled;
- genetics are character-specific potential envelopes;
- protein/energy availability constrain lean adaptation;
- circumference progression combines body composition with regional resistance context;
- regional detraining may reverse only post-activation training-acquired excess;
- detailed fluid/glycogen/endocrine/micronutrient simulation remains deferred.

Relevant deployments:
- BC-2 — PR #78 / Deploy #182;
- BC-3 — PR #82 / Deploy #183;
- Training Method Semantics v2 — PR #84 / Deploy #184;
- Training Anatomy / Movement Semantics v1 — PR #86 / Deploy #185;
- Regional Measurement Detraining — PR #88 / Deploy #186;
- Male Erectile Physiology Canonical Contract — PR #92 / Deploy #189;
- Physical Presentation Closure — PR #94 / Deploy #191;
- Telegram Profile Schema-Driven UX — PR #95 / Deploy #192;
- Solo Sexual Regulation v1 — PR #97 / Deploy #193.

## Universal Profile Grading Framework v1 — COMPLETE / DEPLOYED

Canonical:
- `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md`
- `docs/PROFILE_GRADING_COVERAGE_V1.md`
- `docs/READ_ONLY_GRADING_PROOF.md`

Core invariant:
`authoritative current value(s) + explicit named grading scheme + scheme-specific context -> derived grade metadata -> generic consumers`

Shared vocabulary:
`E Beginner -> D Novice -> C Capable -> B Skilled -> A Advanced -> S Expert -> SS Elite -> SSS Master -> X Mythic -> XX Transcendent`.

Current rules:
- grades never persist as competing truth;
- numeric field != automatically gradeable;
- IQ remains outside current RAPS grading;
- Skills grade from `character_skills.score`; persisted `tier` is not grading authority;
- raw Body dimensions remain descriptive/ungraded;
- Body v1 grades selected derived waist/shoulders, waist/hips and waist/height references;
- chest/waist remains context-only;
- no `larger = better` body rule and no hard-coded popularized golden ratio;
- health, general aesthetics, bodybuilding/classic-physique and modelling may later use different named schemes over the same raw state.

Checkpoint: PR #100 / Deploy #194.

## Character Change Observability & Notification Foundation v1 — COMPLETE / DEPLOYED

Canonical: `docs/CHARACTER_CHANGE_OBSERVABILITY_V1.md`.

Core invariant:
`authoritative mutation/history -> domain-aware cumulative delta -> significance policy -> grade-transition check -> presentation ledger -> Profile delta UX + eligible aggregated notification`

Current rules:
- progression engines retain full precision;
- microscopic deltas accumulate rather than disappearing;
- initial significance defaults: RAPS/Skill `0.10`, body circumference `0.05 in`, Height `0.10 in`, Weight `0.25 lb`, Body Fat `0.10` percentage point, ratios `0.01`;
- grade transitions are immediately significant;
- Profile shows `▲/▼`, with `🟢/🔴` only where beneficial/detrimental semantics are justified;
- ordinary stat pushes are aggregated and debounced to one per recipient/character per 5 real minutes;
- grade transitions bypass the ordinary debounce;
- failed sends do not consume pending significance;
- current/default actor stat notifications default ON; future actors default OFF;
- `/statnotify` and Character-page toggle provide per-character control;
- explicit OFF→ON/global notification toggles reset baselines and never replay historical backlog;
- profile-less actors no-op safely.

Checkpoint: PR #102 / Deploy #195.

## Skill Progression Foundation v1 — COMPLETE / DEPLOYED / LIVE-ACTIVATED

Canonical: `docs/SKILL_PROGRESSION_FOUNDATION_V1.md`.

Authority:
- `character_skills.score` = current learned-skill proficiency;
- `character_skills.experience` = accumulated legitimate post-activation learning evidence;
- persisted `tier` = legacy/compatibility only;
- read-time grade comes from `skill-proficiency-100-v1`;
- model prose, Telegram and generic action names are not progression authority.

Core invariant:
`completed skill-relevant training evidence + effective duration + method relevance + current proficiency + recent-practice saturation -> effective learning units -> bounded score/experience settlement + immutable audit event`

Hand-to-Hand exemplar consumes existing immutable Training Method evidence for configured combat methods such as Heavy Bag, Combat Mat, Technical Dummy, AI Combat Simulation and Combat Pit drills. Non-combat training such as free weights does not improve Hand-to-Hand merely because the action type is `train`.

Progression behavior:
- zero-gain bootstrap occurs at ordinary initialize/deploy boundary;
- historical eligible action evidence is cursor-consumed without retroactive XP or score mutation;
- future legitimate eligible training can progress score/experience;
- recent-practice saturation and current-proficiency diminishing returns bound growth;
- consumed action IDs cannot be credited twice;
- canonical reseeding preserves progression-active/experienced skill state and extra learned skills;
- internal settlement receipts remain audit evidence, not user-facing Recent Activity;
- existing grading/change-observability/notification layers automatically consume authoritative skill-score changes.

Legacy skill-like RAPS fields (`combat_skill`, `weapons_proficiency`, `survival_skill`, etc.) are not independent live progression authorities. The Hand-to-Hand exemplar leaves `raps_pa.combat_skill` as a legacy compatibility snapshot rather than creating a second mutation path.

Validation:
- PR #104 final tested head `bc0dd277013c9cbed727fa48880dc2ff1258cc20`;
- CI #789 / `31869352929` SUCCESS;
- focused production-copy Skill Progression Acceptance #2 / `31869352985` SUCCESS;
- Public Readiness Security Audit #58 SUCCESS;
- merge `a8c86705700f689024c75fe91e00be9361ae557a`;
- Deploy #196 / `31869399038` SUCCESS;
- post-merge CI #790 / `31869399041` SUCCESS;
- main Skill Progression Acceptance #3 / `31869399147` SUCCESS.

Production was not trained/accelerated merely to prove a live occurrence.

## Solo Sexual Regulation v1 — COMPLETE / DEPLOYED

Canonical: `docs/SOLO_SEXUAL_REGULATION_V1.md`.

Current v1 remains adult-only/private-alone, with authored baseline libido + release recency + immediate recovery state driving bounded solo-regulation availability. Stress is not a prerequisite or mandatory trigger. No testosterone surrogate, fixed weekly quota, partnered behavior, structural-anatomy mutation or special deterministic stress/mood/sleep reward is introduced.

During PR #104, the production-copy validator was corrected so acceptance establishes deterministic eligible preconditions only on the disposable copy instead of depending on whatever live cooldown/recovery timing happened to be copied. Production remains untouched.

## Public repository security

`Ye-Shwethway/observer-sandbox` is PUBLIC.

Canonical: `docs/PUBLIC_REPOSITORY_SECURITY.md`, `SECURITY.md`.

- VPS-backed PR validation must fail closed for fork-originated PRs.
- Sensitive/intimate production values must not be dumped into public logs merely for evidence.
- Disposable-copy validation may establish test preconditions; live production must not be mutated to manufacture proof.

## Next development sequence

1. **Skill Progression follow-on batch by proven evidence pattern — NEXT**;
2. remaining Skill Progression batches where legitimate evidence sources exist;
3. Skill Retention / Reacquisition when justified;
4. intellectual attributes;
5. mental/emotion dynamics;
6. broader relationship/social systems and partnered/contextual sexual behavior;
7. broad Mind/Behavior architecture only after enough real feature families justify it.

## Skill Progression follow-on batch — NEXT

The new structural invariant is proven. Do **not** repeat one branch/PR/deploy per skill.

Before selecting the batch, inspect current represented skills and existing evidence systems and group only structurally equivalent mappings. Candidate represented skills include Weapons, Survival, Tactical Planning, Technology and Field Medicine, but inclusion requires a legitimate current evidence source.

Batch policy:
- reuse `character_skills.score` / `experience` authority;
- reuse the same bootstrap/idempotency/reseed safety;
- configure skill-to-evidence/method mappings rather than hard-coding actor identity;
- Training Method evidence may support combat-practice skills;
- Research/action evidence may support technical/cognitive skills only where semantics are already concrete enough;
- fieldcraft/practical skills require real action evidence rather than invented learning from inactivity or generic prose;
- do not add a skill merely to fill the batch;
- do not activate Skill Retention/Decay as a side effect;
- do not synchronize legacy RAPS aliases as competing mutable truth; handle alias derivation/cleanup deliberately.

The minimum next runnable slice should therefore be the **largest coherent batch that reuses already-existing authoritative evidence channels without inventing new major subsystems**.

## Deferred boundaries

Do not add as side effects:
- broad Mind/Behavior Engine;
- Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health expansion;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- automatic restocking, deep recipes, economy/currency, generalized crafting;
- detailed endocrine/micronutrient/organ simulation;
- partnered sexual behavior before that family is explicitly entered;
- estate exterior/Tahoe traversal.

## Exact resume point

Re-read live production and current canonical repository first.

**Skill Progression Foundation v1 — Hand-to-Hand Combat exemplar is complete/deployed through PR #104 / Deploy #196. The next canonical development slice is a Skill Progression follow-on batch by proven evidence pattern.**

Start by inventorying the remaining represented skills against already-existing immutable action/training/research evidence. Batch only mappings that can be justified from current engine evidence; defer skills that would require a new major subsystem.
