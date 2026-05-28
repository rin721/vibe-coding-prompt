# Execution Slice Runner

## Trigger

Use when the developer asks for the next implementation step, a current slice is clearly selected, or state files show a slice in progress.

## Inputs

- Current status.
- Execution slice definition.
- Requirement ledger.
- Test report.
- Knowledge search results when available.

## Steps

1. Read current state.
2. Confirm the current legal execution slice.
3. Check allowed and forbidden files.
4. Perform only the slice goal.
5. Run slice verification.
6. Update test evidence, status, and handoff.
7. Stop if scope, risk, or authority expands.

## Outputs

- Implemented slice changes.
- Verification evidence.
- Updated state and handoff.

## Failure Handling

If state is ambiguous, generate a state diagnosis instead of guessing. If the same issue fails three times, mark blocked and request confirmation.
