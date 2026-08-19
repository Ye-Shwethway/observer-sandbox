# Creator Studio Structured AI Timeout — I4.2.1

Status: IMPLEMENTATION CONTRACT
Date: 2026-08-19

## Problem

Full schema-backed Character drafts can legitimately take longer than ordinary autonomy decisions. The shared HTTP helper previously imposed a 45-second read timeout, causing Creator Studio to reject otherwise valid Character prompts with `The read operation timed out`.

## Contract

- ordinary autonomy decisions keep the existing 45-second transport timeout;
- structured generation uses a separate bounded 120-second timeout;
- the timeout is forwarded through both Gemini and OpenAI-compatible structured-generation paths;
- no automatic retry is performed after a read timeout, avoiding duplicate provider work/cost when the first request may still be executing server-side;
- Creator Studio input/session state remains available for an explicit retry after failure;
- no schema, canonical state, sandbox state, or autonomy behavior changes are introduced by this slice.
