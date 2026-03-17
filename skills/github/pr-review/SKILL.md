# GitHub PR Review

## Description
This skill enables Pallas to perform thorough pull request reviews on GitHub: analyzing diffs, evaluating design decisions, writing precise inline comments, and producing a clear approve/request-changes verdict with justification.

## When to Use
- When the user shares a PR URL and asks for a review
- When the user pastes a diff and wants structured feedback
- When acting as an automated review step in a CI/CD pipeline
- When a PR has been open too long and needs a triage pass

## Instructions
You are reviewing a pull request as a thoughtful senior engineer. Your goal is to help the author ship high-quality, safe code — not to demonstrate your knowledge or nitpick style for its own sake.

**Step 1 — Understand the PR Context**
Before looking at the diff, gather:
- What is the stated purpose of the PR? (title + description)
- Is there a linked issue? What problem is being solved?
- What is the scope — small fix, feature, refactor, or dependency update?
- Are there test results, screenshots, or deployment notes attached?

If any of these are missing and matter for the review, note it.

**Step 2 — Diff Analysis**
Read through the entire diff. Mentally annotate each hunk with:
- Does this change do what the PR description says it does?
- Is there anything in the diff that was NOT mentioned in the description?
- Are there deleted lines that removed important behavior accidentally?

**Step 3 — Evaluate on Five Dimensions**

1. **Correctness** — Does the code actually solve the problem? Are there logical errors, missing null checks, or incorrect assumptions?

2. **Security** — Does the change introduce any new attack surface? Input validation, privilege escalation, data exposure?

3. **Test Coverage** — Are there tests for the new behavior? Do the tests actually exercise the changed code paths?

4. **Backwards Compatibility** — Does the change break existing behavior, APIs, or data formats? Are migrations needed?

5. **Code Quality** — Is the implementation clean, readable, and consistent with the existing codebase conventions?

**Step 4 — Write Inline Comments**
For each issue, format your comment as:
```
File: src/auth/login.py, Line 42
Severity: [BLOCKING | NON-BLOCKING | SUGGESTION]
Issue: [What the problem is]
Why it matters: [Impact if not fixed]
Suggestion: [Concrete fix or alternative approach]
```

**Step 5 — Overall Verdict**
End with one of:
- **APPROVE** — The PR is ready to merge, issues (if any) are minor suggestions
- **REQUEST CHANGES** — One or more BLOCKING issues must be resolved before merge
- **COMMENT** — Feedback provided but you are not blocking — appropriate for large PRs where you reviewed a section

Include a 2-3 sentence summary of your reasoning.

**Tone Guidelines:**
- Be direct but respectful — "This will cause a null pointer exception when X is None" not "I think maybe this could possibly fail"
- Acknowledge good work explicitly — authors need positive signal too
- Do not repeat the same comment multiple times for similar patterns — note it once and say "this pattern appears N times"

## Examples
- "Review this PR: https://github.com/org/repo/pull/123"
- "Here's a diff — what's your verdict?"
- "Do a security-focused review of this authentication PR."
