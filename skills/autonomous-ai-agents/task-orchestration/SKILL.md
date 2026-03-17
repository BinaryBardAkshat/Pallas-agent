# Task Orchestration

## Description
This skill enables Pallas to decompose complex, multi-step tasks into a structured execution plan, track progress across steps, handle failures gracefully, and report status clearly throughout execution. It is the backbone of any agentic workflow that spans more than two or three tool calls.

## When to Use
- When a user request requires more than 3 sequential actions to complete
- When a task involves branching logic (if X then do Y, else Z)
- When subtasks may fail independently and the overall task should still recover
- When the user needs visibility into progress on a long-running task

## Instructions
You are the orchestrator. Your job is to plan, execute, monitor, and recover — not just to do.

**Phase 1 — Decomposition**
Before taking any action, write out a task plan in this format:
```
TASK: [top-level goal]
SUBTASKS:
  1. [action] → expected output
  2. [action] → expected output
  ...
DEPENDENCIES: [list which subtasks depend on outputs of other subtasks]
RISK POINTS: [steps most likely to fail and why]
```
Show this plan to the user if the task is ambiguous or high-stakes. Proceed directly if the task is clear and low-risk.

**Phase 2 — Execution**
Execute subtasks in dependency order. For each subtask:
- State what you are about to do before doing it (one line)
- Execute the action
- Verify the output matches the expected output
- Mark the subtask as DONE, FAILED, or SKIPPED

Use a running status block you update after each step:
```
[DONE]  1. Fetched repo metadata
[DONE]  2. Cloned repository
[RUNNING] 3. Running test suite
[ ]     4. Generate report
```

**Phase 3 — Failure Recovery**
When a subtask fails:
1. Capture the exact error message
2. Classify the failure: `TRANSIENT` (retry), `DEPENDENCY` (fix upstream), `FATAL` (abort and report), `USER_INPUT_NEEDED` (pause and ask)
3. For TRANSIENT failures, retry up to 2 times with a brief wait
4. For DEPENDENCY failures, fix the upstream subtask before retrying
5. Never silently skip a failed subtask — always surface it

**Phase 4 — Completion Report**
When all subtasks are resolved, produce a summary:
- What was accomplished
- What failed (if anything) and why
- Any follow-up actions the user should take
- Time or tool calls consumed (if relevant)

**Constraints:**
- Do not start Phase 2 if Phase 1 produced a plan with unresolvable ambiguities
- Do not proceed past a FATAL failure without explicit user authorization
- Keep the status block visible — never bury it in prose

## Examples
- "Set up a new Python project: create the repo, scaffold the directory structure, install dependencies, and run the initial test suite."
- "Research three competitors, summarize their pricing, and write a comparison table."
- "Refactor the auth module, run tests after each change, and open a PR when done."
