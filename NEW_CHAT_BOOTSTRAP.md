# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-16

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Default workflow:
`branch -> focused tests + final PR CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

## Current canonical checkpoint

**Intelligent Mind Engine Foundation v1 is COMPLETE / DEPLOYED.**

Latest runtime evidence:
- PR #214 — `Add Intelligent Mind Engine Foundation v1`
- final tested PR head: `a08faaeaf5852ec44ea4aab92f78c746db5d18e8`
- CI #982 / run `31951775815`: SUCCESS
- Public Readiness Security Audit #139: SUCCESS
- Inventory Foundation v1 Acceptance #67: SUCCESS
- merge: `71b280191e91c7314180e992bb0beaf0c734d97a`
- Deploy #254 / run `31951861684`: SUCCESS
- deployment verification (`sync -> install/configure cognition -> restart -> verify`): SUCCESS
- schema: **v8**
- mind schema: **v1**

`main` and `test` were synchronized at the runtime merge before this docs-only continuity checkpoint.

## Required cognition / mind / memory read order

1. `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md`
2. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
3. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
4. `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`
5. task-relevant world/profile/runtime docs only.

## Canonical Mind Engine rule

The Mind Engine is now the shared character-owned substrate for future internal cognition.

Preserve:

`world truth != perception != memory != mind state/thought != intention/plan != action proposal != action authority`

**Every future subsystem that can materially influence character perception, interpretation, thought, affect, active concerns, goals, intentions, planning, social cognition, communication or relationship appraisal must read and align with `docs/INTELLIGENT_MIND_ENGINE_FOUNDATION_V1.md` before implementation.**

This also applies to external-world systems when they feed cognition, especially weather/environment, economy/money, media/information, communication, obligations/schedules and social systems.

Do not create parallel hidden mind/planner/thought stores when the state belongs to this architecture.

## Mind Engine Foundation v1 — deployed scope

Foundation v1 is intentionally behavior-neutral.

Generic schema now provides:
- `mental_cycles` — bounded character mental-processing boundaries;
- `mental_episodes` — structured thought/processing units;
- `mental_artifacts` — shared persistent/semi-persistent concerns/goals/intentions/plans/social inferences/appraisals/working items;
- `mental_links` — typed provenance/association links to represented memories/events/entities/actions/mental records.

Initial episode vocabulary:
- `task_focused`
- `spontaneous`
- `reflective`
- `prospective`
- `social`
- `evaluative`

Reserved artifact vocabulary:
- `concern`
- `goal`
- `intention`
- `plan`
- `social_inference`
- `appraisal`
- `working_item`

Thin generic runtime API can create/read/update/link foundation records and returns bounded active mental context.

Important: **current autonomy does not automatically create mental cycles or thoughts yet.** No planner or thought generator was activated by MIND-F0, and current action selection behavior remains unchanged.

## Cognition Context vs Mind

Keep them separate:
- **Cognition Context** — raw compact context actually injected into a model decision; currently retains the latest three snapshots.
- **Mind** — structured actor-owned internal mental state/episodes/artifacts through the new foundation schema.

Raw prompt injection is not represented thought merely because the model saw it.

Future Telegram observability direction:
- `📖 Profile`
- `🗃️ Memory`
- future `Mind` surface
- owner-only `🧠 Cognition Context`

No Telegram Mind browser is implemented yet.

## Memory architecture remains authoritative

Preserve:
`event/world truth != actor memory trace != currently recalled cognition context != action authority`.

Human Memory Dynamics v1 remains deployed with recent/consolidated/remote/faded lifecycle, strength/detail decay, sleep-bounded consolidation, cue-driven recall and individual Memory Ability traits.

Thought is not automatically memory. Prospective thought is not automatically intention or plan.

## External world / mental appraisal rule

Do not implement direct arbitrary mental modifiers such as:
- `rain -> mood -5`
- `low cash -> anxiety +10`
- `negative news -> sadness +20`

Preferred flow:

`represented external fact -> exposure/perception -> character-relative appraisal -> mental episode/artifact/affect -> possible intention/action`

World systems own their facts; Mind owns internal interpretation.

## Universal autonomy invariant

Character-specific authoring may seed represented facts/state but must not command future behavior.

No named-character autonomy policy, bespoke routine, destination steering, anti-repetition counter-prompt, memory formula or mental script may be introduced.

Mental artifacts may influence cognition but never bypass deterministic action validation.

## Estate boundary

Estate-first scope remains active. South Lake Tahoe/public/backcountry/water expansion remains paused.

No traversable continuation exists from:
- Main Security Gate to public road;
- Concealed Forest Passage to Tahoe backcountry;
- Hidden Dock to water travel.

## Next architecture phase

Do **not** jump directly to a large planner.

Recommended next discussion/implementation sequence from the canonical Mind contract:
1. decide which minimum **World Input Foundations** are needed first (weather/environment, money/economy, media/information, communication exposure, obligations as evidence requires);
2. implement the first **Mental Episode Runtime** that can emit a small structured thought bundle at meaningful cognition/action boundaries without continuous LLM polling;
3. add attention/appraisal/active concerns;
4. then intention;
5. then bounded planning;
6. later social cognition/communication and relationship adaptation.

## Exact resume point

**MIND-F0 is deployed. Reconcile the live Mind Foundation v1 schema/contract first. Before implementing the first real thinking runtime, discuss which minimum world-input foundations should be built next and how the first Mental Episode Runtime should consume them. All future cognition-affect-planning-social work must align with the canonical Mind Engine contract.**
