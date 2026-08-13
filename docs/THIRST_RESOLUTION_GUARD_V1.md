# Thirst Resolution Guard v1

Status: BUG-FIX CANDIDATE

## Incident

After Food Resolution Guard v1 successfully resolved strong hunger, production showed Darian at Food Supply Storage with thirst still above the authored strong threshold. The completed meal changed thirst from about 51.9 to 54.9, then autonomy moved toward Training Hall and began training instead of resolving hydration.

## Root cause

`shape_action_options_for_needs()` was deliberately hunger-only. The policy already classified thirst >=50 as a strong physiological recovery condition, and authored drinking-water effects already existed, but the deterministic causal resolver did not cover thirst. Once hunger cleared, generic movement/training options were therefore exposed again while thirst remained strong.

## Fix

Extend the existing causal need-resolution pattern from hunger to thirst without changing schema or physiology state.

- supported hunger resolver: `eat` reducing `needs.hunger`;
- supported thirst resolver: `drink` reducing `needs.thirst`;
- local resolver available -> expose only the authored recovery action;
- no local resolver -> expose only shortest-path first-hop movement toward the nearest room containing an authored resolver;
- no authored resolver/route -> preserve ordinary options rather than deadlocking autonomy.

Priority compatibility:

- supported critical needs outrank strong needs;
- unsupported critical needs remain under the broader cognition policy and are not skipped by this guard;
- when hunger and thirst are both merely strong, preserve the already accepted hunger-first behavior from Food Resolution Guard v1;
- once hunger clears, strong thirst becomes the next causal recovery goal before discretionary training/study/routine behavior.

No new water object is required: the Kitchen already contains `Drinking Water` with an authored `drink` effect reducing thirst by 55, and the Master Bathroom sink is also a valid authored hydration affordance.

## Acceptance

Reproduce the Creator-observed post-meal state on a disposable production DB copy:

- Food Supply Storage;
- hunger about 13.7 (resolved);
- thirst about 54.9 (still strong);
- cleanliness about 40.5 (also strong but lower in the existing authored signal order).

Prove:

1. strong thirst prevents training from being exposed;
2. from Food Supply Storage, only causal movement toward a nearest authored hydration resolver is exposed;
3. in Kitchen, only `Drink -> Drinking Water` is exposed while thirst remains strong;
4. drinking lowers thirst below the strong threshold;
5. the prior hunger+thirst incident still preserves accepted hunger-first behavior;
6. no model call is required for acceptance;
7. no production DB mutation is performed by the acceptance harness.
