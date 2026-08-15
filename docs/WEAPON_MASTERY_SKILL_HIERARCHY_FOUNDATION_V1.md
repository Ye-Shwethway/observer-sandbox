# Weapon Mastery Skill Hierarchy Foundation v1

Status: COMPLETE

## Purpose

Replace the flat gameplay meaning of the historical `weapons` umbrella score with a clean parent/component Skill structure before represented weapon runtime work begins.

Canonical v1 hierarchy:

`Weapon Mastery` (derived parent)
- `Bladed Weapons` (learned component)
- `Firearms` (learned component)

The hierarchy intentionally stops at weapon-family level. Knife, sword, handgun, rifle, shotgun, bow, and other deeper disciplines are not created until simulation actually needs them.

## Authority model

`Bladed Weapons` and `Firearms` are the learned proficiency authorities.

`Weapon Mastery` is a derived profile/cognition summary only. It:
- is the equal-weight mean of its current component Skill scores;
- cannot receive direct XP;
- cannot independently authorize a represented task;
- is excluded from the overall Skills aggregate so the same learned competency is not counted twice.

This establishes the reusable parent/component invariant without changing H2H.

## Legacy migration

The historical umbrella state was:

`weapons = 87`

The historical record does not prove distinct Bladed Weapons and Firearms scores. V1 therefore initializes both components to `87` only as a **compatibility baseline**.

That initialization is explicitly not evidence that both specializations were independently measured at 87. Metadata records:
- the legacy umbrella source key and value;
- that the baseline is compatibility inheritance;
- that distinct historical specialization evidence is absent.

After initialization, component state is independent. Existing component score, experience, and learning metadata are never overwritten by later ordinary initialization/deployment.

The old `weapons` row remains temporarily as a hidden compatibility projection for code paths that still reference the historical Skill Definition. Its score tracks the current derived parent value, it is hidden from Character Profile, and cognition ignores it. It is not learning authority.

## Profile semantics

The Skills profile exposes:
- `Weapon Mastery` as `derived` parent;
- `Bladed Weapons` and `Firearms` as learned components.

The hidden `weapons` compatibility projection is not displayed.

The overall Skills grade includes learned component Skills but excludes the derived parent. Splitting an umbrella Skill therefore does not create a second parent contribution on top of its children.

## Cognition semantics

Cognition receives hierarchy-aware read-only context for all three canonical hierarchy nodes.

The parent explicitly reports that it is non-executable. Component awareness reports learned specialization proficiency but no represented weapon applications are activated by this foundation.

The legacy `weapons` compatibility projection is omitted from cognition to avoid duplicate/conflicting capability context.

## Runtime and safety boundary

This foundation adds **no weapon action runtime**.

It does not add:
- hostile or non-consensual combat;
- lethality;
- injury/casualty generation;
- weapon resource consumption;
- automatic XP from weapon use;
- safe-practice progression yet;
- deeper weapon-family trees.

The historical `employ_familiar_melee_weapon` and `employ_familiar_ranged_weapon` definition entries remain compatibility semantics until follow-on represented runtime slices explicitly move them onto the new component Skill authorities.

## Validation and deployment

Runtime PR: **#150**

Final tested head:
`d4c23e77e24d6a7f6c75146b78ecab81be34d662`

Merge:
`d2616db5cf08e496b66c3f939ae3b2dcbf1560c4`

CI: **#894 / run `31886921670` SUCCESS**
- 506 tests passed in 41.06s;
- fresh DB init/status succeeded;
- schema v5;
- Cognition Capability Awareness, Skill Progression, Skill Evidence, Grading, Strength, Inventory, and Technology acceptance lanes passed.

The first CI attempt exposed only stale grading expectations plus a test precision mismatch; both were corrected without changing the hierarchy architecture.

Deployment: **#220 / run `31886986845` SUCCESS**.

Production deploy verification:
- production init succeeded and therefore executed hierarchy reconciliation;
- service active/healthy; schema v5;
- autonomy remained enabled in normal mode at 1x with retry null and a pending action;
- Gemini `gemini-3.1-flash-lite` primary cognition binding was preserved;
- Groq `qwen/qwen3.6-27b` fallback remained healthy;
- Telegram bot/API/owner/allowed-user configuration remained healthy;
- live sim time was `2025-05-06T10:48:00+00:00` and Darian was naturally eating in the Kitchen;
- no weapon action, training target, practice action, harm event, or synthetic actor was forced for production proof.

Exact component migration, parent derivation, profile/cognition projection, and idempotency semantics are CI/fresh-DB evidence. The deploy workflow did not separately dump the live hierarchy rows, so deployment is evidence of safe production reconciliation/loading rather than a fabricated live weapon activity proof.

## Next development direction

Review **Bladed Weapons Simulation-Safe Runtime v1** next.

That slice should:
- move the historical familiar-melee application meaning onto `bladed_weapons` as actual represented capability authority;
- introduce one exact solo-safe represented training/simulation target and exact bladed-weapon resource capability;
- keep `weapon_mastery` non-executable;
- emit application evidence without automatic XP;
- add no hostile target, lethality, injury, casualty generation, or broad Combat/Injury Engine.

After that invariant is proven, review a Bladed Weapons progression producer and then reuse the pattern for Firearms.
