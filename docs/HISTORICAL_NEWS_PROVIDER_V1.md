# W4.1 Historical News Provider v1

Status: ACTIVE IMPLEMENTATION CONTRACT

## Purpose

Provide simulation-time historical real-world news evidence for W4 without treating a third-party feed or AI output as omniscient character knowledge.

Provider flow:

`universe simulation time -> GDELT GAL historical files -> normalized external evidence -> W4 information items -> optional AI editorial bulletin -> W0 TV publication/stimulus`.

## Provider

The initial provider is the GDELT Article List (GAL) historical dataset. GAL exposes timestamped gzipped newline-delimited JSON files under a UTC minute-addressed archive.

The adapter uses bounded lookback retrieval from the universe simulation time. Missing minute files are normal provider gaps and are skipped. Retrieval is bounded to avoid continuous or unbounded archive scanning.

Imported records preserve:
- GDELT provider identity/reference;
- outlet/source identity;
- title;
- bounded description when supplied;
- source URL;
- published/observed timestamp;
- language when supplied;
- GAL archive timestamp provenance.

Duplicate URLs are suppressed within one retrieval.

## Historical-time rule

News evidence is selected from represented simulation time, not host wall-clock time. Current-day headlines must not leak into an earlier simulated date merely because they are current on the server.

## Editorial layer

The optional AI editorial role receives only bounded normalized W4 source records. It may choose up to six and produce structured headline/summary text while preserving source item ids.

The deterministic fallback uses the source records directly if no News Generation AI binding exists or inference fails.

## Authority

GDELT records establish that represented source material was observed/published by the external evidence provider. They do not independently prove every underlying claim objectively true.

AI editorial text has no independent world-truth authority.

W4.1 never creates exposure, Memory, Mind state, belief or action authority by fetching news.

## Non-goals

- full-day exhaustive ingestion;
- paid news API dependence;
- article-body scraping;
- copyright mirroring;
- automated fact adjudication;
- political belief generation;
- continuous news polling every simulation tick.
