# Vibe Project Kickoff

## Trigger

Use when a developer gives a new project idea, a vague product goal, or asks to start a Vibe Coding workflow.

## Purpose

Convert a vague idea into confirmed first-version requirements without overwhelming the developer.

## Required Inputs

- Developer's original goal
- Current repository context, if any
- `prompt.md`
- `docs/ai/requirements/REQUIREMENT_LEDGER.md`

## Boundaries

- Do not write product code before requirement confirmation.
- Ask at most `3-5` key questions per round.
- Use ordinary language and options with impact notes.

## Steps

1. Restate the goal in plain language.
2. Classify the project type.
3. Recommend light, standard, strict, or custom mode.
4. Identify likely risks and non-goals.
5. Record raw and normalized requirements.
6. Ask the next `3-5` key questions.
7. Wait for confirmation before architecture planning.

## Outputs

- Updated requirement ledger
- Pending confirmation list
- Suggested mode and agency level

## Verification

- Requirements have explicit status and evidence.
- Developer can understand the options.
- No code implementation has started.

## Failure Handling

If the idea is too vague, provide examples and choices. If risk is high, switch to strict confirmation flow.
