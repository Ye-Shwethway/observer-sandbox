# Character Profile Schema

## Purpose

Observer Sandbox uses a deep profile ontology from the beginning so characters can become progressively more life-like without rebuilding persistence. A field may exist before its simulation engine exists. Such a field remains canonical/static until an authorized engine activates it.

The initial ontology is a union of the supplied Darian profile formats plus the Observer Sandbox architecture decisions already made for needs, physiology, injuries, recovery, memory-ready state and progressive body simulation.

## Storage model

The profile system is intentionally split into schema and values:

- `profile_field_definitions`: stable ontology; field type, unit, domain, default mode, authority, sensitivity.
- `character_profiles`: one rich profile attached to a character entity.
- `character_profile_values`: current per-character values.
- `character_profile_history`: append-oriented change history for canonical corrections and simulation changes.
- `character_preferences`: likes/dislikes/interests/aversions.
- `character_habits`: habitual behavior and strength/frequency metadata.
- `character_routines`: ordered routine activities and conditions.
- `character_skills`: extensible skill registry, score/tier/experience.
- `character_relationship_state`: directed relationship state between characters.

The older generic `fields` table remains part of the core entity system. Character-specific rich profile state should use the profile ontology rather than adding hundreds of columns to `entities`.

## Domains

The initial ontology contains first-class fields for:

- identity and chronology
- body composition and detailed measurements
- face, hair, eyes, skin, facial hair, chest hair and distinctive appearance
- sexual anatomy and sexual physiology
- RAPS physical, mental, intellectual, sexual and verbal-charisma attributes
- social/emotional traits
- energy, hunger, hydration and sleepiness
- fatigue, soreness, injury, illness and recovery
- genetic maxima / physical limits
- personality, motivation and background
- narrative goal/arc state

Preferences, habits, routines, skills and relationships are normalized into dedicated tables because they are variable-length collections rather than scalar profile fields.

## Intimate fields

Sexual anatomy is not hidden in notes or discarded. It is represented explicitly and marked `sensitivity='intimate'`. Initial fields include penis length, girth, erection firmness, genital sensitivity, libido, arousal control, sexual endurance, performance, experience, weekly self/partnered satisfaction counts and genetically fixed genital measurements.

Sensitivity is a presentation/access metadata property; it does not remove the data from simulation. Telegram/UI layers can later require an explicit private-profile view before displaying intimate fields.

## Progressive simulation

Each field carries a mode and authority:

- `canonical`: manually defined authoritative fact.
- `static`: present but not currently simulated.
- `derived`: calculated from other facts.
- `simulated`: actively updated by an engine.

Examples:

- height -> canonical / `profile_core`
- age -> derived / `time_engine`
- hunger -> static then simulated / `needs_engine`
- body fat -> static then simulated / `physiology_engine`
- chest/biceps/thigh measurements -> static then simulated / `body_progression_engine`
- erection firmness/sensitivity -> static then simulated / `sexual_physiology_engine`
- injury state -> static then simulated / `injury_engine`

This lets future modules activate individual domains without changing character identity or schema.

## Conflict policy for Darian source material

The supplied Darian files contain historical value differences. The ontology is therefore built from the union of all fields, while value import is deliberately separate and conflict-aware. A newer import must not silently overwrite a canonical value merely because another historical source contains a different number.

Examples in the supplied material include differences in IQ, body-fat percentage, genital length and historical attribute scores. These are value-reconciliation issues, not schema omissions.

Before Darian is instantiated as the first live character, a canonical seed profile will be created from the latest approved values and every conflicting historical source value will remain traceable through source/revision metadata rather than silently merged.

## Extension rule

New domains should normally be added as field definitions or collection tables, not by restructuring existing character tables. Engines obtain explicit authority over fields; LLM agents never write arbitrary profile values directly.
