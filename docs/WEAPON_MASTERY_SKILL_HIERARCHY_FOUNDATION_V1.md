# Weapon Mastery Skill Hierarchy Foundation v1

Status: implementation candidate

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
- is the weighted mean of its current component Skill scores (equal weights in v1);
- cannot receive direct XP;
- cannot independently authorize a represented task;
- is excluded from the overall Skills aggregate so the same learned competency is not counted twice.

This establishes the reusable parent/component invariant without changing H2H yet.

## Legacy migration

Darian currently has historical umbrella state:

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

The historical `employ_familiar_melee_weapon` and `employ_familiar_ranged_weapon` definition entries remain compatibility semantics until a follow-on represented runtime slice explicitly moves them onto the new component Skill authorities.

## Next development direction

After this foundation passes and deploys, review the first **Bladed Weapons simulation-safe represented runtime/progression exemplar**. It should prove one exact represented training context/resource contract without activating harm semantics. Structurally equivalent Firearms work may then follow by pattern.
