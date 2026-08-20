# Item AI Self-Correction v1

Status: LOCKED CREATOR UX CONTRACT

Single Item AI and Item Batch AI use the same bounded self-correction policy.

Flow:

`Creator intent -> structured candidate -> canonicalization -> deterministic validation -> one correction attempt on rejection -> deterministic validation -> draft or visible failure`

Rules:
- deterministic validation remains authoritative;
- the runtime never silently repairs conflicting physical facts;
- the first deterministic rejection reason is returned to the same structured-output model with the same schema and Creator intent;
- the model must generate a fresh complete candidate rather than patching around the validator;
- at most one automatic correction attempt is allowed;
- if the corrected candidate still fails, the Creator sees the final validation error;
- no Sandbox or canonical state is written before a valid draft is produced and explicitly approved;
- this policy is shared by Single Item and Item Batch AI creation.
