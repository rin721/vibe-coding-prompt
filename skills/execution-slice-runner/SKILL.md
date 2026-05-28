# Execution Slice Runner

## Trigger

Use when the developer says "next step", "继续", "下一步", or asks the Agent to proceed.

## Purpose

Find and execute the current unique legal execution slice.

## Required Inputs

- `docs/ai/state/STATUS.md`
- `docs/ai/state/status.json`
- `docs/ai/tasks/EXECUTION_SLICES.md`
- `docs/ai/tasks/execution_slices.json`
- `docs/ai/requirements/REQUIREMENT_LEDGER.md`

## Boundaries

- Do not invent a task if the current slice is unclear.
- Do not expand allowed files or tools without confirmation.
- Do not skip quality gates.

## Steps

1. Run `python -m vibe_coding_infra next`.
2. If the result is `complete`, report completion.
3. If the result is `diagnosis_required`, produce a status diagnosis and stop.
4. If a slice is selected, read its boundaries and verification.
5. Execute only inside the slice.
6. Run required checks.
7. Update status, task, test report, and handoff notes.

## Outputs

- Execution report
- Updated status files
- Test or validation evidence

## Verification

- Selected slice is unique.
- Modified files are within `allowed_files`.
- Checks passed or failure is recorded.

## Failure Handling

After three failed repair attempts on the same issue, mark the slice `blocked` and write a blocking report.
