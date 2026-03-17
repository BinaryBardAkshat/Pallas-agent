# Pallas Self-Improvement

## Description
This skill enables Pallas to reflect on past sessions, identify capability gaps, and iteratively improve its own skill definitions and behavioral patterns. It treats self-improvement as a structured engineering task rather than vague introspection.

## When to Use
- After completing a complex task where something went wrong or felt inefficient
- When the user says "remember this for next time" or "you should always do X"
- During scheduled end-of-week reviews of agent performance
- When Pallas detects a recurring pattern of mistakes or suboptimal responses

## Instructions
You are performing a structured self-improvement cycle. Follow these steps precisely.

**Step 1 — Session Reflection**
Retrieve the last N conversation turns or session summaries from memory. Identify:
- Tasks that required multiple correction rounds (user said "no, actually..." more than once)
- Tool calls that failed or produced unexpected output
- Responses the user rated poorly or explicitly corrected
- Topics where you had to say "I don't know" or gave a hedged, low-confidence answer

**Step 2 — Gap Classification**
Classify each identified gap into one of these categories:
- `KNOWLEDGE`: Missing factual or domain knowledge
- `SKILL`: A procedure or workflow you don't have a good template for
- `TOOL`: A tool you used incorrectly or a tool that is missing
- `BEHAVIOR`: A recurring stylistic or decision-making flaw (e.g., over-explaining, skipping verification steps)

**Step 3 — Improvement Action**
For each gap, choose the appropriate remediation:
- `KNOWLEDGE` → Add a note to memory with the correct information and source
- `SKILL` → Draft or update a SKILL.md file in the appropriate skills directory
- `TOOL` → Log a tool improvement request with specific description of what is needed
- `BEHAVIOR` → Add a behavioral rule to your persistent system context with clear trigger condition

**Step 4 — Write the Improvement**
When writing or updating a SKILL.md:
- Be specific about the trigger condition (when to activate this skill)
- Write instructions in imperative, procedural style
- Include at least one concrete example
- Keep instructions under 400 words — conciseness signals clarity

**Step 5 — Verify and Commit**
After writing the improvement, simulate applying it to the original failing scenario. Ask: "Would this instruction have prevented the failure?" If not, revise. Log the improvement with a timestamp and the original failure case for traceability.

**Anti-patterns to avoid:**
- Do not write overly generic instructions ("be more careful")
- Do not add redundant skills that duplicate existing ones — check first
- Do not remove existing skills without archiving them

## Examples
- "Reflect on this week's sessions and update your skills if anything felt off."
- "You kept forgetting to confirm before deleting files — fix that behavior."
- "Write a skill for the thing you just learned about how to handle rate limits."
