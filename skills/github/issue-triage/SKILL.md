# GitHub Issue Triage

## Description
This skill enables Pallas to triage GitHub issues systematically: applying labels, assessing priority, identifying duplicates, requesting missing reproduction steps, and routing issues to the right people or milestones.

## When to Use
- When processing a backlog of new or unlabeled issues
- When a user asks "what should we work on next?"
- When a new issue comes in and needs to be assessed before it sits idle
- When doing a periodic issue grooming session

## Instructions
You are performing issue triage. Your goal is to ensure every issue has enough information to act on, is correctly categorized, and is assigned an appropriate priority.

**Step 1 — Read and Classify**
For each issue, determine the type:
- `BUG`: Something that worked and now doesn't, or behaves incorrectly
- `FEATURE`: A request for new functionality
- `IMPROVEMENT`: An enhancement to existing functionality
- `QUESTION`: A support request or clarification needed
- `DOCS`: Documentation is missing or incorrect
- `CHORE`: Dependency updates, CI fixes, cleanup

Apply the corresponding label.

**Step 2 — Check for Duplicates**
Search existing issues for similar reports. Look for:
- Same error message
- Same feature being requested
- Same component mentioned

If a duplicate is found: comment "Duplicate of #[issue number]", apply the `duplicate` label, and close the issue.

**Step 3 — Assess Completeness**
For `BUG` reports, verify these are present:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, version, relevant config)
- Error messages or logs

If any are missing, apply `needs-more-info` label and post a comment requesting the specific missing information. Use this template:
```
Thanks for the report! To help us investigate, could you provide:
- [ ] Steps to reproduce
- [ ] Your environment (OS, version)
- [ ] The full error message/stack trace
```

**Step 4 — Priority Assessment**
Assign priority based on impact and urgency:
- `P0 — Critical`: Data loss, security vulnerability, complete feature broken in production
- `P1 — High`: Important feature broken, significant user impact, no workaround
- `P2 — Medium`: Feature degraded, workaround exists, affects some users
- `P3 — Low`: Minor inconvenience, cosmetic, rarely triggered edge case

**Step 5 — Routing**
- If the issue touches a specific module or component, apply the appropriate component label
- If it relates to an existing milestone, add it to that milestone
- If it is a good first issue for new contributors, add `good-first-issue` and ensure the description is complete

**Step 6 — Triage Summary**
After processing a batch of issues, produce a summary:
```
Triaged: N issues
  Bugs (P0): N
  Bugs (P1-P3): N
  Features: N
  Duplicates closed: N
  Needs more info: N
```

## Examples
- "Triage the 10 most recent issues in this repo."
- "Is issue #234 a duplicate? Find related issues."
- "Label and prioritize all unlabeled issues."
