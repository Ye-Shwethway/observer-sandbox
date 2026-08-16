# Human Memory Dynamics v1

Status: **CANONICAL / DEPLOYED**

## Purpose

Extend Character Memory Foundation v1 from durable actor-owned storage/retrieval into a small, explainable human-like memory lifecycle that distinguishes recent traces from consolidated long-term memory, permits gradual forgetting without deleting historical records, and allows individual characters to differ in mnemonic ability independently of IQ.

This is a simulation abstraction informed by cognitive-memory research. It is not a literal neurological model. Runtime constants are simulation calibrations, not medical or neuroscientific claims.

## Research-informed design anchors

The implementation follows broad findings rather than copying any one laboratory model:

- autobiographical/episodic remembering shows stable individual differences;
- emotional arousal can increase retention, while exact peripheral detail may still weaken;
- sleep supports consolidation of selected recent memories;
- successful retrieval can reinforce later accessibility;
- forgetting may be loss of accessibility/precision rather than proof that the original event ceased to exist.

## Authority separation

Preserve four distinct layers:

1. **World/event truth** — what objectively happened in represented simulation.
2. **Memory trace** — what the actor encoded and how strongly/accessibly it is retained.
3. **Retrieved cognition context** — what the actor can currently recall under present cues.
4. **Current action authority** — what deterministic runtime permits now.

A faded memory never rewrites event truth. Remembered geography never grants topology/access. A forgotten event remains in immutable event history.

## Memory profile traits

Memory ability is not derived from IQ.

Character Profile exposes four independent 0..100 traits:

- `memory.working_memory` — capacity to hold/manipulate currently active information; reserved mainly for future Mind/Planning use in v1.
- `memory.encoding` — quality with which experience becomes a durable trace.
- `memory.retention` — resistance of stored traces to loss of accessibility over time.
- `memory.recall` — ability to retrieve an existing trace from partial/contextual cues.

These are authored character facts. Runtime uses a neutral fallback only if a character lacks an authored value. No engine path derives them directly from IQ.

Current factual Darian seed, stored through the same generic memory-profile contract used by any character:
- Working Memory: 86
- Encoding: 89
- Retention: 84
- Recall: 91

These values are character data, not behavior rules.

## Memory state model

Each memory keeps durable identity/provenance plus dynamic trace state:

- `lifecycle_stage`: `recent | consolidated | remote | faded`;
- `memory_strength`: 0..1 — accessibility/gist strength;
- `detail_strength`: 0..1 — precision/contextual-detail strength;
- `emotional_arousal`: 0..1 — encoded emotional intensity;
- `personal_relevance`: 0..1 — actor-relative significance;
- `consolidated_sim_time`: nullable;
- `last_dynamics_sim_time`: last simulation-time settlement point.

Existing `salience`, `confidence`, `recall_count`, and `last_recalled_sim_time` remain distinct.

`memory_strength` is not truth probability. `confidence` is represented certainty; `memory_strength` is retrieval accessibility.

## Encoding

New episodic memories begin as `recent` traces.

Initial strength uses represented event salience, structured memory signals, and character encoding ability. Ordinary actions default to low emotional arousal and moderate personal relevance unless the event producer supplies stronger structured signals.

Example event metadata:

```json
{
  "memory_signals": {
    "emotional_arousal": 0.9,
    "personal_relevance": 0.95
  }
}
```

The runtime must not infer trauma, happiness, grief or other high-intensity states from an action name alone.

## Recent vs long-term memory

Recent and long-term memory are lifecycle states of the same actor-owned trace, not separate histories.

Canonical flow:

`experience -> recent trace -> consolidation -> consolidated/remote trace -> possible fading -> cue-driven recall/reinforcement`

Represented sleep acts as a consolidation boundary. Settlement is chronological:

`encoded event -> sleep boundary -> consolidation -> current simulation time`

Only eligible memories that existed before the represented sleep boundary may be consolidated by that sleep. Semantic seed knowledge starts consolidated because it represents established pre-runtime knowledge rather than a newly experienced episode.

## Continuous forgetting

Forgetting is continuous and simulation-time based. Dynamics settle lazily at read/retrieval/consolidation boundaries; there is no background timer process.

Decay is influenced by:

- lifecycle stage — recent traces are less stable than consolidated traces;
- character retention ability;
- salience and personal relevance;
- emotional arousal — stronger protection of gist than exact peripheral detail;
- prior successful recall/rehearsal through bounded reinforcement.

A low-strength memory becomes `faded`; it is not deleted. `detail_strength` normally weakens at least as quickly as gist strength.

## Recall and cueing

Stored memory is not automatically recallable memory.

Current accessibility combines:

- `memory_strength`;
- character `memory.recall`;
- decision relevance;
- represented current location/entity/action cues.

Very low-strength memories normally fail ordinary recall. Strong matching cues may surface them again. Only selected memories count as successful recalls.

Successful recall:

- increments `recall_count`;
- updates `last_recalled_sim_time`;
- provides small bounded strength/detail reinforcement;
- may reactivate a faded trace;
- never rewrites source-event truth or fabricates new semantic content.

V1 is deterministic for reproducibility; it does not roll random dice for every recall attempt.

## Spatial semantic memory and generic recall

Spatial familiarity is now semantic Character Memory. However, the known-world projection already supplies the actor's represented map separately to cognition.

Therefore generic relevant-memory retrieval does **not** repeatedly inject every known spatial-memory row. A `spatial_familiarity` semantic memory enters generic recall only when the current represented location directly cues it. This prevents stable map knowledge from crowding fresh episodic memories and works for existing production rows without rewriting their stored history.

Known geography remains planning knowledge only; exact movement authority still comes from current deterministic `action_options`.

## Remote memory

A sufficiently old, retained consolidated trace may be classified `remote`. This is a lifecycle/presentation classification, not a promise of perfect detail.

## Telegram observability

Character-level buttons are visually distinct:

- `📖 Profile`
- `🗃️ Memory`
- owner-only `🧠 Cognition Context`

Memory view remains read-only and dynamically settles at current simulation time. It shows:

- Active / Episodic / Knowledge counts;
- Recent / Long-term / Faded counts;
- lifecycle stage;
- Strength and Detail percentages;
- salience, confidence and recall count;
- related represented entities.

Telegram does not mutate, restore, delete or force-recall memories.

## Profile UX

Character Profile includes `🧩 Memory Ability` as its own domain. Memory traits are not automatically equivalent to intelligence or a Skill.

## Non-goals

M3 does not implement:

- false-memory generation;
- PTSD or other clinical psychiatric simulation;
- dream content;
- detailed sleep-stage neuroscience;
- semantic abstraction/reflection from repeated episodes;
- procedural memory;
- a daily/weekly planner;
- character-specific remembering rules;
- vector embeddings.

## Planning handoff

Future Minimal Mind / Planning may consume memory with the required distinction:

`stored != currently recallable`

A planner should receive bounded currently retrievable memories plus separately authoritative present state, rather than perfect access to the whole memory database.

## Verified deployment

M3 shipped through PR #212.

- final tested head: `1cad8d9188e49f42f9c00b8026eccd917a9fc073`
- CI #980 / run `31950039890`: SUCCESS
- Strength Live Cycle Validation #102: SUCCESS
- Inventory Foundation Acceptance #65: SUCCESS
- Skill Evidence Semantics Acceptance #51: SUCCESS
- Skill Progression Foundation Acceptance #68: SUCCESS
- Technology Diagnostic Task Runtime Acceptance #42: SUCCESS
- Attribute Grading Batch 1 Acceptance #50: SUCCESS
- Read-Only Grading Proof Acceptance #51: SUCCESS
- Solo Regulation Naturalism v2 Acceptance #49: SUCCESS
- merge: `b8343d12b5204a0f3a049cbfb7632b617df77495`
- Deploy #253 / run `31950111179`: SUCCESS
- deployment verification (`sync -> install/configure cognition -> restart -> verify`): SUCCESS
- schema: **v7**

## Acceptance status

**COMPLETE / DEPLOYED.**
