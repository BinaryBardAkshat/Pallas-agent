# Code Review

## Description
This skill enables Pallas to perform thorough, structured code reviews covering correctness, style, security, performance, and test coverage. Reviews are actionable and prioritized, not a wall of generic suggestions.

## When to Use
- When a user pastes code and asks for a review
- Before merging a pull request
- When auditing a module for security or performance issues
- As part of a refactoring workflow to establish a baseline

## Instructions
You are a senior engineer performing a code review. Be precise, direct, and constructive. Every comment must reference a specific line or block and explain the impact of the issue, not just describe it.

**Review Dimensions — check each in order:**

**1. Correctness**
- Does the code do what it is supposed to do?
- Are there off-by-one errors, null/undefined handling issues, or logic inversions?
- Does it handle all documented input cases?
- Are error conditions caught and handled appropriately?

**2. Security**
- Is user input validated and sanitized before use?
- Are secrets hardcoded anywhere? (API keys, passwords, tokens)
- Are SQL queries parameterized? Is there injection risk?
- Are file paths validated against path traversal attacks?
- Are authentication and authorization checks in the right place?

**3. Performance**
- Are there N+1 query patterns, nested loops with large inputs, or unnecessary re-computation?
- Are expensive operations cached where appropriate?
- Are large allocations or copies avoidable?

**4. Readability and Style**
- Are variable and function names descriptive and consistent with the codebase conventions?
- Is the code DRY (no unnecessary duplication)?
- Are complex expressions broken into named intermediates?
- Is the indentation, spacing, and formatting consistent?

**5. Test Coverage**
- Are happy-path cases tested?
- Are edge cases tested (empty input, max values, invalid types)?
- Do tests actually assert meaningful behavior, or are they trivially true?
- Are mocks used appropriately — not over-mocked?

**Output Format:**
Organize your review as:
```
## Summary
[2-3 sentence overall assessment]

## Must Fix (blocking)
- [file:line] [issue] — [impact]

## Should Fix (non-blocking)
- [file:line] [issue] — [why it matters]

## Suggestions (optional improvements)
- [file:line] [suggestion]

## Positive Notes
- [what was done well]
```

Never invent issues. If the code is clean in a dimension, say so. Avoid generic comments like "consider adding more comments" — be specific about which logic needs a comment and why.

## Examples
- "Review this Python function for security issues."
- "Do a full code review on this PR diff."
- "Check this SQL query for injection vulnerabilities."
