# Profile Minimum Unlock Sweep v1

Status: IMPLEMENTED IN PR

## Goal

Close the current vertical-completeness pass for every Character Profile section without inventing a bespoke engine for static/canonical domains.

Minimum unlock follows `docs/MINIMUM_PROFILE_UNLOCK_POLICY_V1.md`: authoritative state, meaningful runtime/cognition influence, and persistence/presentation where relevant.

## Classification

| Section | Classification | Minimum runtime basis |
| --- | --- | --- |
| Identity | minimum-unlocked after this batch | canonical profile state; name and DOB were already consumed; compact identity context is now available to cognition |
| Appearance | minimum-unlocked after this batch | canonical profile state and observer presentation; compact stable appearance/self-presentation context now reaches cognition without granting mutation authority |
| Body | already minimum-unlocked | authoritative body/profile values, body composition/measurement progression, training/body runtime effects and profile presentation |
| Attributes | already minimum-unlocked | authoritative Attribute values, declared task/performance modifiers, progression where implemented, cognition/profile visibility |
| Recovery | already minimum-unlocked | fatigue/sleep/energy recovery state directly shapes action availability, training readiness and cognition |
| Sexual | already minimum-unlocked | Sexual Anatomy/Physiology profile state plus Solo Sexual Regulation Naturalism v2 and deterministic private-action physiology |
| Personality | already minimum-unlocked | canonical traits/motivation/complexity already consumed by autonomous cognition |
| Preferences | already minimum-unlocked | persisted likes/dislikes, hobbies and habits already consumed by autonomous cognition |
| Background | minimum-unlocked after this batch | canonical origins/history remains stable but now reaches cognition as bounded context for character-grounded decisions |
| Skills | already minimum-unlocked / CLOSED v1 | authoritative learned scores, represented application and legitimate learning paths; see `docs/SKILLS_CLOSURE_V1.md` |

## Canonical-context batch

`ModelDecisionProvider._character_context()` now provides structured, compact context for:

- identity: name, date of birth, sex, gender, current status;
- appearance: distinctive features, eye/hair presentation, facial hair and PARS;
- personality: traits, primary motivation and complexity notes;
- background: origins;
- preferences/hobbies/habits;
- skills.

The context is read-only. It does not let the LLM mutate profile fields, invent state, or bypass deterministic action validation.

Sensitive identity data that is not needed for ordinary cognition, such as sexual orientation, is not copied into this general character context.

## Boundaries

This closure does not add:

- a dedicated Appearance Engine or Background Engine;
- biography simulation or memory reconstruction;
- relationship mechanics;
- cosmetic progression;
- arbitrary profile mutation by the LLM;
- new Skill depth;
- a universal personality reward model.

Static/canonical fields remain stable when stability is their legitimate simulation role.

## Completion meaning

Once this batch is merged/deployed/verified, every Character Profile section satisfies the minimum vertical-completeness standard. The next phase is an evidence-driven review of missing cross-cutting workflow foundations before deepening any single profile domain.
