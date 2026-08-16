# Telegram Universe Observability v1

Status: IMPLEMENTED — PENDING FINAL CI / DEPLOY

## Purpose

Expose represented universe weather and geographic context to the Creator through the existing Telegram `/start -> Universe` observer surface without granting characters knowledge or changing travel authority.

## Navigation

`Universe` is now domain-oriented:

- `Weather`
- `Regions`
- `Locations`

This deliberately avoids an extra `Geography` menu layer while only one region is represented. A dedicated Geography hub may be introduced later if region/location categories become large enough to justify another navigation level.

### Weather

The Weather view reads the already represented environment state for the current simulation time.

It does **not** fetch the external provider on button press and does not own weather production.

It shows:
- simulation time;
- South Lake Tahoe provider sampling context;
- condition;
- temperature;
- precipitation kind/intensity;
- wind;
- visibility;
- cloud cover;
- daylight/light level;
- validity window;
- historical-provider versus synthetic-fallback provenance.

Preserve:

`Creator reads weather != character exposure != perception != memory != mind`.

### Regions

The initial observer geography hierarchy exposes:

`South Lake Tahoe -> Thorne Estate`

This aligns with `WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`, which defines `loc_south_lake_tahoe` as the future structural regional parent of `loc_thorne_estate` when bounded Tahoe geography is actually implemented.

For this observer slice, South Lake Tahoe is **regional context metadata only**. `loc_south_lake_tahoe` is not inserted into the runtime entity/containment/travel graph, and no public-road, backcountry or water route is opened.

### Locations

The Locations view contains currently represented top-level simulation locations. Today that includes Thorne Estate, which continues into the existing recursive Estate campus/floor/room/object browser.

## Semantic distinction

- **Region**: geographic context and grouping for Creator observability.
- **Location**: represented simulation place with existing world/runtime semantics.
- **Travel topology**: separate authored relations/route authority; never inferred from observer hierarchy.

This distinction lets the UI adopt the future South Lake Tahoe hierarchy now while preserving the intentional Estate-only travel boundary.

## Configuration

Observer-only geographic grouping lives in:

`config/worlds/geography.observer.v1.json`

It is presentation/context metadata, not movement authority.

## Acceptance

Required proofs:
- Universe exposes Weather, Regions and Locations separately;
- Locations contains Thorne Estate;
- Regions exposes South Lake Tahoe then Thorne Estate;
- no `loc_south_lake_tahoe` runtime entity is invented by this slice;
- no Estate-to-Tahoe travel relation is created;
- Weather renders current represented environment data and provenance;
- synthetic fallback is visibly identified as non-historical truth;
- viewing Weather does not create character exposure, Memory or Mind records;
- existing Estate recursive browser remains intact.
