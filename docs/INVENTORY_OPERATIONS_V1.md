# Inventory Operations v1

Status: CANDIDATE / CI + PRODUCTION-COPY VERIFIED

## Purpose

Inventory Operations v1 makes the schema-v5 inventory foundation operational without turning inventory into a Darian/Thorne-Estate-specific subsystem.

Darian's Estate is the first production exemplar only. The reusable inventory query/control contract is universe-wide and entity-id driven.

## Universal observer invariant

Creator-facing inventory browsing MUST support inventory related to arbitrary universe entities rather than one named home or character.

Canonical Telegram hierarchy:

`Inventory -> Locations | Characters | Containers | All Stocks -> selected scope -> stack detail`

The backend accepts stable entity ids. It does not contain a `Darian's Estate inventory` code path.

- **Locations** may expose stock contained anywhere in their structural descendants.
- **Characters** may expose stock they own/carry/equip plus related inventory containers.
- **Containers** may be fixed or movable and expose their contained stacks.
- **All Stocks** provides a universe-wide stack view independent of location/character selection.

A location/character with no related stock is still a valid inventory scope and may report an empty inventory.

Synthetic non-Estate location and non-Darian character/backpack tests are required regression guards for this invariant.

## Wealthy Estate reserve baseline

Until outside-world purchasing, replenishment, vendors and currency exist, the Thorne Estate receives one explicit Creator-approved reserve migration suitable for a wealthy, well-stocked residence.

Migration revision: `thorne-estate-wealthy-food-reserve-v1`
Mode: `ensure_minimum`

Minimum stock:
- apples: 120 pieces;
- bananas: 90 pieces;
- cooked chicken breast: 30,000 g;
- cooked white rice: 36,000 g;
- eggs: 240 pieces;
- oats: 15,000 g;
- plain Greek yogurt: 16,000 g;
- mixed vegetables: 30,000 g;
- olive oil: 8,000 g;
- whey protein powder: 10,000 g.

This migration is **not automatic restocking**. A durable runtime marker makes it one-time only. After it has applied, ordinary initialize/deploy must preserve subsequent depletion and Creator changes exactly as the existing no-refill invariant requires.

The explicit baseline emits `creator_inventory_stock_baseline_applied` audit evidence.

## Read/query service

Reusable inventory APIs provide:
- all active stacks;
- inventory related to an arbitrary entity id;
- location/character/container scope listing;
- stack detail including definition, quantity/unit, owner and storage container.

The query layer reuses canonical relations and schema-v5 stack state. Telegram does not query SQLite directly.

## Telegram surface

`/start -> Inventory` and `/inventory` expose the same universe-wide observer model.

Authorized observer users may browse inventory. Browsing is read-only.

Stack detail shows:
- human-readable item name;
- quantity/unit;
- reusable definition id;
- current container;
- owner;
- container kind/mobility where available.

Pagination/sectioning belongs to Telegram presentation only and must not constrain the underlying inventory model.

## Creator replenishment control

Owner-only stock replenishment is the first typed inventory mutation.

Backend operation: `replenish_inventory_stack(stack_id, quantity, ...)`

Rules:
- existing stack only;
- quantity must be positive and bounded;
- adds to current quantity; does not silently set/reset stock;
- does not create definitions/stacks;
- does not change ownership or containment;
- does not advance simulation time;
- independent of LLM cognition;
- records `creator_inventory_replenished` with requester, authority, item/definition, before/after quantity, unit, owner, container and physical location.

Telegram owner UI requires an explicit confirmation step before applying a button-driven replenishment. Allowed users can browse but cannot mutate. Server-side authorization remains authoritative even when mutation buttons are hidden.

A typed owner `/replenish <stack_id> <quantity>` command is also available for deliberate direct control.

## Validation evidence on PR #73 candidate

Final implementation candidate before canonical-doc synchronization: `63dc759f1bfac3406135a051d1a4feb91eca98fe`.

- CI #629: SUCCESS; 230 tests passed; fresh DB init/status succeeded on schema v5.
- Inventory Foundation Acceptance #7: SUCCESS; schema-v5 no-refill/definition-instance foundation remains intact.
- Inventory Operations Acceptance #3: SUCCESS on a disposable production copy.

Production-copy acceptance established:
- source live SQLite opened read-only/query-only;
- production DB not mutated by validation;
- schema 5 -> 5;
- simulation time preserved;
- world revision preserved;
- actor runtime preserved;
- body weight/BF preserved;
- wealthy reserve migrated apples to 120 on the disposable copy;
- after a test reduction to 113, ordinary re-init left them at 113;
- typed Creator replenish +24 produced 137;
- replenishment physical location resolved generically to `loc_thorne_estate_kitchen`;
- model calls 0;
- Telegram API calls 0.

## Non-goals

Inventory Operations v1 does not add:
- economy/currency;
- vendors, shopping or transactions;
- automatic replenishment;
- spoilage/expiration;
- recipes/cooking graph;
- encumbrance or capacity simulation;
- general item creation/deletion/transfer UI;
- generalized training-equipment migration;
- Eating Behavior v1;
- schema v6.

## Next dependency

After this slice is deployed/read back, proceed to **Eating Behavior v1** using the universal inventory/food definition layer. Natural intake/energy evidence must then be observed before BC-2 body-composition mutation is activated.
