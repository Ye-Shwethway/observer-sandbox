# Semantic Spatial Memory Migration v1

Status: IMPLEMENTATION CONTRACT

## Goal

Move factual initial spatial familiarity from the temporary named-character bootstrap into the generic Character Memory system without changing objective world truth, traversal authority, concealed-location semantics, or autonomous behavior policy.

## Canonical ownership after migration

- objective geography/topology: world entities, spatial-container fields and relations;
- actor-known geography: active `semantic` Character Memory records with `knowledge_kind=spatial_familiarity`;
- current executable movement: deterministic `action_options` only.

No named-character spatial-familiarity config or loader is authoritative after this migration.

## Generic initialization

`config/memory/initial.semantic.v1.json` is a shared initial-knowledge source. Character blocks may contain character-specific factual knowledge, but the format and loader are character-generic.

Each initial known location becomes one semantic memory containing:
- `knowledge_kind=spatial_familiarity`;
- `location_id` and represented location name;
- familiarity level `unknown|aware|familiar|intimate`;
- `secret` independently from familiarity;
- factual basis/provenance.

Seed memories use deterministic technical IDs and `INSERT OR IGNORE` semantics so repeated initialization cannot overwrite later learned/evolved memory state.

Initial knowledge predates observation: `event_sim_time` records the canonical world bootstrap known-since time while `encoded_sim_time` records when the Memory System materialized the record.

## Compatibility projection

Existing cognition APIs (`location_known`, `location_familiarity`, `spatial_familiarity_context`, action-option filtering) remain available, but derive their state from semantic memory queries rather than `world.spatial_familiarity` character fields.

This preserves downstream cognition behavior while removing the named storage path.

## Migration cleanup

After semantic seed rows exist:
- remove legacy `world.spatial_familiarity` field state if present;
- remove legacy `spatial_familiarity_revision` runtime marker;
- record generic `initial_semantic_memory_revision`;
- delete `config/characters/darian.spatial_familiarity.v1.json`;
- remove any default path/load dependency on that file.

## Non-goals

This slice does not implement:
- automatic location discovery;
- familiarity reinforcement/decay;
- forgetting;
- full memory consolidation;
- daily/weekly planning;
- Tahoe/world expansion;
- character-specific outing or training policy.

Those capabilities may build on semantic memory later through generic systems.

## Acceptance

Migration is accepted when:
- all valid pre-migration known Estate locations have equivalent familiarity levels;
- concealed/secret known locations remain known only to the actor while generic preview hiding remains intact;
- an unknown newly connected hidden location remains absent from autonomous cognition;
- initialization is idempotent and does not overwrite an evolved semantic memory;
- a second character can use the same generic seed contract without a new loader/policy;
- no `world.spatial_familiarity` field remains after initialization;
- `config/characters/darian.spatial_familiarity.v1.json` no longer exists;
- existing deterministic reachability and action authority remain unchanged.
