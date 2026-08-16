# Universal Character Autonomy Contract v1

Status: ACTIVE ARCHITECTURE CONTRACT

## Core invariant

Character-specific behavioral hard-coding is forbidden.

Character-specific authoring is limited to represented seed/state facts such as identity, body/profile, personality traits, biography, initial skills, possessions, relationships, preferences, hobbies, initial habits, and initial world knowledge where a temporary bootstrap is still required.

Autonomous behavior must emerge from universal systems consuming represented character state plus world state and history.

Canonical direction:

`character seed/state + needs/physiology + time + environment + affordances + recent history + goals + relationships + memory/learning + deterministic constraints -> universal cognition -> proposed action -> deterministic validation/mutation`

## Forbidden patterns

Do not author or inject rules such as:
- a named character normally trains at a particular time;
- a named character should prefer a particular room, destination, activity, recovery pattern, or lifestyle option;
- a named character should counterbalance an observed behavior by following a bespoke prompt instruction;
- a named character receives a custom autonomy prompt because current autonomous behavior is undesirable.

Do not solve behavior imbalance by stacking character-specific counter-prompts.

## Allowed character-specific seed/state

Character-specific data may describe what is true about the character rather than what the runtime should command them to do. Examples include:
- identity and biography;
- physical and mental profile values;
- personality traits and motivations;
- authored preferences/hobbies;
- initial learned Skills;
- relationships and possessions;
- initial habits where historically established;
- initial knowledge/familiarity as temporary authored state until the relevant progression system owns it.

Universal runtime systems decide how those facts influence behavior.

## Universal policy

`config/autonomy/universal.autonomy-policy.v1.json` is the shared cognition policy for every registered actor.

It may encode universal safety, causal-grounding, physiological-priority, repetition, duration, circadian, validation, and reasoning rules. It must not bind to an `entity_id`, character name, character-specific routine, named private location, or bespoke behavior target.

Character-specific preference should enter cognition through represented profile/state surfaces, not through alternate policy files.

## World affordances

World-authored affordances are generic environmental facts. A location can support `walk`, `relax`, `observe`, training, resource use, or other actions without forcing any particular character to choose them.

Character/world interaction should be resolved from generic affordances plus character state, knowledge, history, and universal decision systems.

## Spatial familiarity migration debt

`config/characters/darian.spatial_familiarity.v1.json` is retained temporarily only because a general memory/discovery system does not yet own initial and evolving spatial knowledge.

This file is explicitly transitional, not the desired long-term design.

When the general Memory System / discovery-learning layer is implemented:
1. migrate Darian's currently valid initial spatial knowledge into the generic memory/knowledge initialization model;
2. preserve world-truth vs actor-known-world vs current-action-authority separation;
3. make discovery, familiarity change, reinforcement and forgetting universal runtime processes where supported;
4. remove `darian.spatial_familiarity.v1.json` and any Darian-specific loader/path dependency;
5. do not replace it with another named-character cognition policy file.

Until that migration, the spatial familiarity seed must remain factual initial knowledge only and must not contain behavioral instructions.

## Acceptance rule

A new character should be able to enter the simulation by providing character seed/state data without requiring a new autonomy policy, character-specific behavior branch, named-character prompt, or bespoke daily routine implementation.
