# Self-Healing Agent

## Description
Automatically detect, diagnose, and repair failures in running systems, code, or infrastructure. The agent monitors for errors, identifies root causes, applies fixes, and verifies the fix worked — all without human intervention.

## When to Use
- CI/CD pipeline failures that follow recurring patterns
- Automated repair of failing unit or integration tests
- Dependency resolution issues (version conflicts, missing packages)
- Configuration drift in infrastructure
- Automated bug fixing in well-tested codebases

## Instructions
When operating in self-healing mode, follow this loop:

1. **Detect**: Identify the failure signal — error message, failing test, crashed process, or anomalous metric.

2. **Diagnose**:
   - Read error messages and stack traces carefully
   - Run `terminal(command="pytest tests/ 2>&1 | tail -50")` or similar to capture full context
   - Search memory for previous similar failures: `memory(action="search", query="error: <error type>")`
   - Check recent changes: `terminal(command="git log --oneline -10")`

3. **Hypothesize**: Form a ranked list of likely root causes (most likely first). Do NOT guess randomly.

4. **Repair**:
   - Start with the highest-probability hypothesis
   - Make the minimal targeted fix
   - Document what you changed and why in a comment or commit message

5. **Verify**:
   - Re-run the failing test/process
   - Confirm the fix works and has not introduced regressions
   - Run the full test suite if available: `terminal(command="pytest tests/ -v")`

6. **Learn**: Store the fix in memory so future occurrences can be resolved faster.

**Escalation rule**: If 3 fix attempts fail, report the issue with full diagnostics rather than continuing to guess.

## Examples
- "The test suite is failing, auto-fix it"
- "My Flask app crashes on startup, diagnose and fix it"
- "The Docker build is broken, fix it without changing the application logic"

## Requirements
- Terminal tool with write access to the codebase
- File tool for reading and editing source files
- Memory tool for storing and recalling fixes
