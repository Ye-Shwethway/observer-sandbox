# Causal Need Resolution v2

Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED

## Incident

After Food Resolution Guard v1 fixed repeated hunger inspection, production showed a second gap: Darian ate Stored Food Provisions at strong hunger while thirst was already strong, the meal's authored effects increased thirst, and autonomy then resumed training without resolving thirst.

Observed sequence:

- Food Supply Storage: `Eat -> Stored Food Provisions`
- hunger materially resolved;
- thirst rose from about 51.9 to 54.9 because the meal has authored `needs.thirst +2` plus passive drift;
- Darian moved to Training Hall;
- autonomy selected `Train -> Combat Mat` while thirst remained strong.

The generated reason also incorrectly claimed the food would address thirst even though its authored effect worsens thirst.

## Root cause

Food Resolution Guard v1 deliberately implemented deterministic causal shaping for hunger only. Strong thirst remained soft cognition guidance, so training and other discretionary options could reappear while thirst was still above the authored strong threshold (`>=50`).

The previous hunger-only guard also bypassed same-level authored need ordering when hunger and thirst were both strong.

## v2 behavior

Causal need shaping now supports two proven domains:

- thirst -> authored `drink` action reducing `needs.thirst`;
- hunger -> authored `eat` action reducing `needs.hunger`.

`decision_signals.needs_attention` remains the priority authority. The guard acts only when the highest-priority active need is a supported domain; it never skips over an unsupported higher-priority need.

For a supported strong/critical need:

1. if a local authored resolver exists, expose only resolver actions that actually reduce that need;
2. otherwise expose only shortest-path first-hop movement toward the nearest room containing an authored resolver;
3. if no authored resolver or route exists, preserve original options rather than deadlocking autonomy.

This means a move through Training Hall may still be the correct first hop from Food Supply Storage, but `Train -> Combat Mat` is unavailable while strong thirst remains the active supported priority.

## Reason grounding

Autonomy policy now explicitly forbids claiming that an action improves a physiological need when its authored effects leave that need unchanged or worsen it. Stored Food Provisions may resolve hunger, but they must not be described as hydration because their authored thirst effect is positive.

## Non-goals

- no deterministic guard yet for sleepiness, energy, or cleanliness;
- no inventory/resource depletion;
- no new schema;
- no arbitrary need scoring system beyond the existing authored priority order.

## Acceptance and deployment

Disposable production-copy acceptance proved, without model calls:

- when thirst and hunger are both strong at the observed levels, authored same-level ordering selects thirst first;
- from Food Supply Storage the only exposed action is causal movement toward a drinking-water resolver;
- at Training Hall with thirst around 55, no training option is exposed;
- at Kitchen the only local causal resolver is `Drink -> Drinking Water`;
- drinking reduces thirst below the strong threshold;
- live production DB is not mutated by the acceptance harness.

Evidence:
- PR #23 merge `4a0c5d67f0ed9460fc319702fa846a676090c606`;
- CI #446 `31692492232` SUCCESS;
- Causal Need Resolution v2 Acceptance #11 `31692492180` SUCCESS;
- release `5763818a20277b684a688df0d15bf488dbfc49e9`;
- Deploy #149 `31692592830` SUCCESS.

Production deploy readback remained healthy: schema v4, autonomy enabled/normal/unpaused, Gemini cognition binding preserved, Telegram connected. A pre-existing `Train -> Combat Mat` action planned before deployment was intentionally not cancelled; the v2 guard applies from the next cognition boundary onward.
