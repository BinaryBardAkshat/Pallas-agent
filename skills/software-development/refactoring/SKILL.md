# Refactoring

## Description
This skill guides Pallas through safe, incremental refactoring using tests as a safety net. It prevents "big bang" rewrites that break things by enforcing small, verifiable transformations with a clear goal at each step.

## When to Use
- When code is hard to understand, extend, or test
- When there is duplication that should be consolidated
- When a module has grown too large and needs to be split
- When preparing legacy code for a new feature without rewriting everything at once

## Instructions
You are refactoring, not rewriting. The external behavior must not change. Every step must leave the code in a working, passing state.

**Phase 1 — Establish a Safety Net**
Before changing anything:
1. Run the existing test suite. Record the pass/fail count.
2. If test coverage is below 60% for the code being refactored, write tests first using the test-writing skill.
3. If no tests exist and writing them would take too long, at minimum write a characterization test: capture the current output for representative inputs and assert it doesn't change.

Do not proceed if you cannot verify correctness after each step.

**Phase 2 — Identify the Refactoring Target**
Classify what needs to change:
- `EXTRACT`: A block of code should become its own function or class
- `RENAME`: A name is misleading or inconsistent
- `MOVE`: Code belongs in a different module or class
- `SIMPLIFY`: A complex expression or nested structure can be flattened
- `DEDUPLICATE`: The same logic appears in multiple places
- `DECOMPOSE`: A function does too many things and should be split

State the target and classification before beginning.

**Phase 3 — Apply Transformations Incrementally**
Apply one transformation at a time. After each:
1. Run the test suite — all tests must still pass
2. Review the diff — it should be small and obviously safe
3. Commit or checkpoint the state

Example sequence for extracting a function:
1. Copy the block into a new function, call it from the original location
2. Run tests
3. Remove the original block, leaving only the call
4. Run tests
5. Move the function to its final location
6. Run tests

**Phase 4 — Naming and Documentation**
After structural changes are stable:
- Rename variables and functions to reflect their new, cleaner purpose
- Update or remove outdated comments
- Add a docstring to any newly extracted function that didn't have one

**Phase 5 — Final Review**
Compare the before and after:
- Is the code meaningfully easier to read?
- Are there any test failures?
- Did complexity decrease (cyclomatic complexity, function length, nesting depth)?
- Did you accidentally change behavior anywhere?

**Hard Rules:**
- Never combine a refactoring commit with a behavior change — keep them separate
- Never refactor and fix a bug in the same step
- If a refactoring step causes test failures, revert it and choose a smaller step

## Examples
- "This function is 200 lines long — help me break it up safely."
- "There's duplicated validation logic in three places, help me extract it."
- "Refactor this class to use composition instead of inheritance."
