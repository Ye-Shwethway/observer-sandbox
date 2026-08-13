# Autonomy Breadth and Time Observability

Status: DEPLOYED / ACCEPTANCE VERIFIED / CREATOR LIVE BEHAVIOR VERIFICATION PENDING

## Purpose

Correct the observed production pattern where Darian repeatedly selected Kitchen/Pantry/Refrigerator/Stove interactions because the existing estate exposed far more actionable objects in the kitchen than in other meaningful rooms, while also making autonomous action timing visible to the Creator.

## World breadth

The existing Thorne Estate topology is preserved. No exterior traversal or new action vocabulary is added.

The world seed now contains 27 object instances. Added purposeful fixtures include:

- Personal Desk — Master Suite;
- Media Console — Living Room;
- Research Desk — Library & Study;
- Workshop Bench — Garage & Workshop;
- Surveillance Console — Surveillance & Intelligence Hub;
- Secure Communications Terminal — Secure Communications Room;
- Combat Mat and Practice Dummy — Training Hall;
- Diagnostic Station — Medical Bay;
- Equipment Bench — Armory & Storage;
- Supply Shelves — Food Supply Storage;
- Emergency Console — Underground Bunker.

These reuse existing generic capabilities such as `inspect`, `use`, `read`, and `train`. The acceptance probe proves legal non-kitchen action targets in seven previously sparse purposeful rooms.

## Autonomy breadth guidance

Darian autonomy policy revision is `darian-autonomy-p1-v1.4-breadth-duration-aware`.

When physiological needs are comfortable, cognition is instructed to:

- avoid serial same-room generic `inspect`/`use` loops without a changing purpose;
- avoid treating kitchen appliance inspection or meal planning as default productive behavior;
- use wider estate activities exposed by the environment, including research, workshop, equipment, intelligence/communications, medical checks, and training where appropriate.

This changes available choices and guidance, not deterministic personality scripting. Actual behavioral diversity remains model-selected and requires live observation rather than being claimed from CI alone.

## Time semantics

Action time remains linear and deterministic:

- an action with `duration_minutes = N` advances that action interval by `N` simulated minutes;
- scheduling wall wait is `duration_minutes × 60 / speed` seconds;
- therefore at production `1x`, one simulated minute is approximately one real minute between normal action boundaries.

Generic runtime compatibility bounds remain intentionally broad (`inspect` 1–60; `use` 1–120) so a deploy cannot invalidate a pre-existing pending action planned under the prior contract.

Normal cognition guidance is narrower:

- simple inspection: normally 2–6 simulated minutes;
- simple object use: normally 2–10 simulated minutes;
- longer `use` duration requires a concrete sustained purpose.

A future deterministic per-action/per-target duration-profile system remains separate work if observed model guidance is insufficient.

## Telegram completion notification

The proactive contract remains one push per committed action. Planning alone does not create another notification.

After an action completes, the service resolves the next normal decision boundary immediately and the same completion message may show:

- completed action duration;
- approximate real wait at the recorded speed;
- next planned action and target;
- next action duration;
- expected simulated timestamp for the next action-completion update.

Example structure:

`⏱ Took 5 sim min • ~5 min real @ 1x`

`⏭ Next: Move → Living Room`

`⏱ Duration 5 sim min • ~5 min real @ 1x`

`⏳ Expected update: 01-05-2025 (Thursday) 03:30 PM`

The ETA is an estimate for the currently planned action. Runtime failure/backoff, pause, service interruption, or later control intervention can delay or invalidate it.

## Safety and evidence

The first acceptance attempt failed only because of SSH/heredoc SQL quoting in the acceptance harness; production was not deployed from that failed gate.

Final evidence:

- PR #5 merged at `ac19e132bc5fa10688bb54e69fe885b1ae196510`;
- PR #5 CI #332 / run `31676550067` SUCCESS;
- pending-action safety correction PR #6 merged at `29be3e8d70d99b23f17380a7bfd4d5adf8a07101`;
- PR #6 CI #334 / run `31676811535` SUCCESS;
- final accepted main `802b17fce70f9d3b28d29fd2dc56267b17f3fb9f`;
- main CI #336 / run `31676984174` SUCCESS;
- Autonomy Breadth and Time Acceptance #2 / run `31676984134` SUCCESS;
- acceptance: 27 objects, 7 non-kitchen target rooms, inspect guidance 2–6, simple-use guidance 2–10, pending-compatible runtime bounds, timing UI visible, zero model calls, production DB unchanged;
- release commit `7163284d19df19cda252437563d13c83d939b197`;
- Deploy #132 / run `31677053654` SUCCESS;
- production readback: service healthy, schema v4, autonomy enabled/normal/unpaused/1x, existing pending action preserved, Gemini cognition binding preserved, Telegram API connected.

## Explicit non-goals

This release does not add:

- a new action taxonomy;
- deterministic per-target duration profiles;
- inventory/resource depletion;
- exterior/Tahoe traversal;
- long-term training stimulus/progression;
- grading/tier progression;
- schema v5.

Creator live observation is still required to decide whether the broader world and v1.4 policy produce enough behavioral diversity in normal production.