# Item Batch AI Retry Fix

Status: IMPLEMENTED ON TEST — ACCEPTANCE PENDING

This fix closes three Telegram Creator Studio integration gaps found during live Item Batch testing:

- Item Batch AI uses the configured Creator Creation AI binding and now carries a stricter item-v1 batch contract prompt/schema.
- Batch AI validation/generation failures remain visible and retry the Item Batch prompt instead of silently falling back to the Single Item prompt.
- Creator Studio native Telegram `typing` chat action now wraps the underlying dynamic Studio router used by Character, Location, Single Item, and Item Batch AI paths, refreshing while synchronous AI generation is running.

No Item runtime, canonical transmigration, or autonomy behavior is changed.
