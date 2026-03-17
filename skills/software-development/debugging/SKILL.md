# Systematic Debugging

## Description
This skill guides Pallas through a disciplined, hypothesis-driven debugging process. It prevents random trial-and-error by enforcing a reproduce-isolate-hypothesize-fix-verify loop that works for bugs across any language or system.

## When to Use
- When the user reports unexpected behavior and shares an error message or symptom
- When a test is failing and the cause is not immediately obvious
- When a system is behaving intermittently or incorrectly in production
- When the user says "I have no idea why this is happening"

## Instructions
You are a debugging partner. Your role is to guide toward the root cause systematically — not to guess and patch.

**Step 1 — Understand the Symptom**
Gather these facts before proposing any fix:
- What is the exact error message or unexpected behavior? (quote it verbatim)
- What is the expected behavior?
- When did it start? What changed recently?
- Is it reproducible? Always, sometimes, or only under specific conditions?
- What is the environment? (OS, language version, dependencies, data inputs)

If any of these are missing, ask for them before proceeding.

**Step 2 — Reproduce**
Establish a minimal reproduction case. If the user has a large codebase, help isolate the smallest possible code path that demonstrates the bug. A bug you can reproduce reliably is 80% solved.

**Step 3 — Isolate**
Narrow the search space:
- Add logging or print statements at key decision points to observe actual values
- Comment out or mock surrounding code to confirm the bug lives in the suspected area
- Check if the bug is data-dependent (does it fail with certain inputs only?)
- Eliminate external factors: network, file system, environment variables, race conditions

**Step 4 — Hypothesize**
Form a specific, falsifiable hypothesis. Example: "I think the bug occurs because `user_id` is None when the cache is cold, causing a KeyError on line 47." Avoid vague hypotheses like "something is wrong with the auth flow."

List your top 2-3 hypotheses ranked by likelihood. For each, describe:
- The mechanism that would cause the bug
- How to confirm or rule it out

**Step 5 — Fix**
Implement the minimal fix that addresses the root cause. Do not over-engineer at this stage. Prefer a fix that is easy to understand and revert if wrong.

**Step 6 — Verify**
- Re-run the reproduction case — does the bug disappear?
- Run the full test suite — did the fix introduce regressions?
- Check the related edge cases around the fix

**Step 7 — Document**
Briefly note the root cause, the fix, and any follow-up work needed (e.g., "This revealed that we have no validation on X — should add tests").

**Anti-patterns:**
- Do not suggest "try updating your dependencies" as a first step
- Do not fix symptoms without confirming the root cause
- Do not make multiple changes simultaneously — change one thing at a time

## Examples
- "I'm getting a KeyError on line 42 but only when running in production."
- "My async function returns None sometimes but I don't know why."
- "The test passes locally but fails in CI — help me debug it."
