# Human Memory Dynamics v1

Status: ACTIVE IMPLEMENTATION CONTRACT

## Purpose

Extend Character Memory Foundation v1 from durable actor-owned storage/retrieval into a small, explainable human-like memory lifecycle that distinguishes recent traces from consolidated long-term memory, permits gradual forgetting without deleting historical records, and allows individual characters to differ in mnemonic ability independently of IQ.

This is a simulation abstraction informed by cognitive-memory research. It is not a literal neurological model and must remain small enough to inspect and tune.

## Research-informed design anchors

The implementation follows these broad findings rather than copying any one laboratory model:

- human autobiographical/episodic remembering shows stable individual differences;
- emotional arousal can increase retention, but does not preserve every peripheral detail equally;
- sleep supports consolidation of selected recent memories, especially behaviorally relevant material;
- successful retrieval can alter/reinforce later accessibility;
- forgetting is often loss of accessibility/precision rather than evidence that the original event never occurred.

Implementation constants are simulation calibrations, not medical/neuroscientific claims.

## Authority separation

Preserve:

1. **World/event truth** — what objectively happened in represented simulation.
2. **Memory trace** — what the actor encoded and how strongly/accessibly it is retained.
3. **Retrieved cognition context** — what the actor can currently recall under present cues.
4. **Current action authority** — what deterministic runtime permits now.

A faded or inaccurate memory must never rewrite event truth. A remembered location never grants topology/access. A forgotten event remains present in immutable event history.

## Memory profile traits

Memory ability is not derived from IQ.

Character Profile gains four independent 0..100 traits:

- `memory.working_memory` — capacity to hold/manipulate currently active information; reserved for later Mind/Planning consumers in v1.
- `memory.encoding` — quality with which an experience becomes a durable trace.
- `memory.retention` — resistance of stored traces to loss of accessibility over time.
- `memory.recall` — ability to retrieve an existing trace from partial/contextual cues.

These are authored character facts. Runtime may use neutral fallback values when a legacy/new character lacks an authored value, but must not infer them directly from IQ.

## Memory state model

Each memory keeps durable identity/provenance plus dynamic trace state:

- `lifecycle_stage`: `recent | consolidated | remote | faded`;
- `memory_strength`: 0..1 — accessibility/gist strength;
- `detail_strength`: 0..1 — precision/contextual-detail strength;
- `emotional_arousal`: 0..1 — encoded emotional intensity;
- `personal_relevance`: 0..1 — actor-relative significance;
- `consolidated_sim_time`: nullable;
- `last_dynamics_sim_time`: last simulation-time settlement point.

Existing `salience`, `confidence`, `recall_count`, `last_recalled_sim_time` remain useful and distinct.

`memory_strength` is not objective truth probability. `confidence` is the actor's represented certainty; `memory_strength` is retrieval accessibility.

## Encoding

New episodic memories begin as `recent` traces.

Initial strength is affected by:

`base event salience + emotional arousal + personal relevance + character encoding ability`

Ordinary actions default to low emotional arousal and moderate personal relevance unless structured event metadata supplies stronger memory signals. The runtime must not invent trauma/happiness merely from an action name.

A future event producer may provide structured memory signals such as:

```json
{
  "memory_signals": {
    "emotional_arousal": 0.9,
    "personal_relevance": 0.95
  }
}
```

Values are clamped 0..1 and remain actor-relative signals, not clinical diagnoses.

## Recent vs long-term memory

Recent and long-term memory are lifecycle states of the same actor-owned trace, not separate objective histories.

Canonical flow:

`experience -> recent trace -> consolidation -> long-term/remote trace -> possible fading -> cue-driven recall/reinforcement`

V1 uses represented sleep as a meaningful consolidation opportunity rather than promoting every memory after a fixed wall-clock deadline.

After a completed sleep action, eligible recent episodic memories are settled and may transition to `consolidated`. Higher salience/relevance/arousal and stronger encoding improve the retained trace. Sleep does not guarantee perfect preservation.

Semantic seed knowledge begins consolidated because it represents established pre-runtime knowledge rather than a newly experienced episode.

## Continuous forgetting

Forgetting is continuous and simulation-time based.

The system settles trace strength lazily at read/retrieval/consolidation boundaries instead of running background jobs.

Decay rate is influenced by:

- lifecycle stage: recent traces are less stable than consolidated traces;
- character retention ability;
- salience and personal relevance;
- emotional arousal protects gist more than exact peripheral detail;
- prior successful recalls/rehearsals provide bounded reinforcement.

No memory is deleted merely because it became hard to recall.

When `memory_strength` falls below the ordinary-accessibility floor, the record becomes `faded`. It remains stored and can still be reactivated by sufficiently strong contextual/entity cues.

`detail_strength` normally decays at least as quickly as gist strength. Emotional significance must not imply perfect forever-detail.

## Recall and cueing

Retrieval remains bounded and character-scoped.

Candidate accessibility combines:

- current `memory_strength`;
- character `memory.recall`;
- existing relevance score (salience, recency, current location, current actions);
- entity/location cue matches.

A low-strength memory can therefore fail ordinary recall yet become retrievable when the actor returns to the same represented place/entity context.

Only selected memories count as successfully recalled.

Successful recall:

- updates `last_recalled_sim_time` and `recall_count`;
- provides small bounded reinforcement to memory/detail strength;
- never raises strength above 1.0;
- may move a `faded` trace back to an accessible long-term stage when evidence supports recall.

V1 does not fabricate false memories or change semantic content during reconsolidation.

## Remote memory

A consolidated trace may be classified `remote` after substantial represented time if it remains sufficiently strong. This is a presentation/lifecycle classification, not a promise that exact details remain intact.

The runtime must use continuous age/strength logic rather than a fixed "all memories become remote on day N" behavioral rule.

## Telegram observability

Character-level surfaces must be visually distinct:

- `📖 Profile`
- `🧠 Memory`
- owner-only `💭 Cognition Context`

Memory rows should expose lifecycle/strength in concise observer-friendly form where useful, while event truth remains available through History.

Memory view is read-only. Telegram must not mutate, restore, delete or force-recall character memories.

## Profile UX

Memory traits appear as a normal Character Profile domain rather than hidden engine configuration.

They are character facts and therefore viewable through existing Profile browsing/grading conventions. They are not automatically equivalent to intelligence or a Skill.

## Determinism and reproducibility

M3 uses deterministic accessibility ranking. It does not roll random dice for every recall attempt. Character-to-character differences emerge from profile traits and represented memory state/cues while tests remain reproducible.

Stochastic recall may be considered later only if deterministic dynamics prove visibly too mechanical.

## Non-goals

M3 does not implement:

- false-memory generation;
- PTSD/clinical psychiatric simulation;
- dream content;
- detailed sleep-stage neuroscience;
- semantic abstraction/reflection from repeated episodes;
- procedural memory;
- a daily/weekly planner;
- fixed character-specific remembering rules;
- vector embeddings.

## Planning handoff

After M3, Minimal Mind / Planning may consume memory with the correct distinction:

`stored != currently recallable`

A planner should see only bounded currently retrievable memories, plus separately authoritative present state. This prevents the character from behaving like a perfect database query engine.

## Acceptance

M3 is accepted when:

- profile schema exposes independent memory traits without deriving them from IQ;
- new episodic traces start recent with dynamic strength/detail state;
- established semantic seed knowledge starts consolidated;
- represented sleep can consolidate recent memories generically;
- simulation-time settlement gradually weakens traces according to retention/significance;
- faded memories remain stored rather than deleted;
- contextual cues and character recall ability affect retrieval accessibility;
- successful recall provides bounded reinforcement;
- Telegram uses distinct Memory and Cognition Context icons and shows dynamic memory state;
- behavior remains character-agnostic;
- existing event truth/action authority remains unchanged.
