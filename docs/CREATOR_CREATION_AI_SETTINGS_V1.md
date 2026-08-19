# Creator Creation AI Settings v1

Status: IMPLEMENTATION CONTRACT
Date: 2026-08-19

## Purpose

Keep Creator-facing AI configuration organized as independent role bindings while the number of AI-assisted systems grows.

Canonical Telegram hierarchy:

`Creator Settings -> AI Settings -> Character AI / News Generation AI / Creator Creation AI`

Creator Settings remains the broader owner-only configuration surface. AI Settings is the upper layer for model/provider roles; diagnostics and future non-AI Creator controls do not need to compete with individual AI roles at the same level.

## Independent role bindings

### Character AI

Owns autonomous character cognition bindings:
- primary cognition;
- fallback cognition.

### News Generation AI

Owns represented news-generation/editorial binding. It does not replace Character AI and does not establish objective world truth.

### Creator Creation AI

Owns AI assistance for Creator Creation workflows.

Initial binding contract:
- scope type: `engine`;
- scope id: `creator_creation`;
- role: `creator_creation_assist`.

It is intentionally independent from Character AI and News Generation AI. Changing one role must not mutate either of the others.

## Authority boundary

Creator Creation AI is a proposal generator, never canonical mutation authority.

Its future normal flow is:

`Creator prompt -> structured creation proposal -> schema validation -> Creation Sandbox preview/revise/reroll -> explicit sandbox approval`

Canonical universe activation is a separate later operation:

`sandbox creation -> target-universe compatibility validation -> transmigration preview -> explicit Creator transmigration approval -> atomic canonical activation`

Therefore:
- model output cannot directly write canonical universe state;
- model output cannot bypass Creation Sandbox;
- model output cannot approve its own proposal;
- model output cannot approve transmigration;
- a successful AI model probe changes no active binding until Creator explicitly saves it;
- a saved Creator Creation AI binding only selects the assistant model, not a creation permission.

## v1 implementation boundary

This slice provides:
- the AI Settings upper layer;
- Creator Creation AI provider/model selection;
- real structured-output capability probe;
- explicit Save & Activate after successful probe;
- independent role binding;
- sandbox-only proposal validation foundation.

This slice does **not** yet provide the full Creator Studio prompt/reroll/edit workflow. That belongs to the later Creation Sandbox / Telegram Creator Studio implementation after isolated staging persistence exists.

## UX rule

The Creator must always be able to distinguish:
- selecting/configuring an AI model;
- generating a draft;
- approving a draft into Creation Sandbox;
- transmigrating a tested sandbox object into a target universe.

Those are separate authority transitions and must never be collapsed into one button or one AI call.
