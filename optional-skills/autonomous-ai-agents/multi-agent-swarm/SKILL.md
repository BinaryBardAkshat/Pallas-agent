# Multi-Agent Swarm

## Description
Orchestrate multiple specialized sub-agents working in parallel or in sequence to tackle complex, multi-faceted tasks. Each agent in the swarm has a focused role, reducing context bloat and improving overall output quality.

## When to Use
- Tasks that can be decomposed into independent parallel workstreams
- Research tasks that require gathering from multiple sources simultaneously
- Code projects requiring simultaneous implementation of multiple modules
- When a single agent's context window would overflow for very large tasks
- Competitive analysis, due diligence, or comprehensive audits

## Instructions
When you receive a complex task that benefits from parallel execution:

1. **Decompose** the task into 2-5 independent sub-tasks. Each sub-task should be self-contained and produce a concrete output.

2. **Assign roles** to each sub-agent:
   - Research Agent: web search and information gathering
   - Code Agent: implementation and file writing
   - Analysis Agent: data processing and synthesis
   - Review Agent: quality checking and validation

3. **Use the `delegate` tool** for each sub-task:
   ```
   delegate(task="Research the top 5 competitors of X and summarize their pricing", tools=["web"])
   delegate(task="Implement the UserAuth class based on the spec", tools=["file", "terminal"])
   ```

4. **Synthesize results**: Collect all sub-agent outputs and merge them into a coherent final deliverable. Resolve any conflicts or inconsistencies.

5. **Validate**: Run a final review pass on the combined output.

**Important constraints:**
- Sub-agents cannot call `delegate` themselves (no recursive swarms)
- Each sub-agent has a 5-minute timeout
- Sub-agent output is capped at 10,000 characters
- Keep sub-tasks clearly scoped — ambiguous tasks produce poor results

## Examples
- "Research and write a comprehensive competitive analysis of the top 5 CRM tools"
- "Simultaneously implement the frontend and backend for this login feature"
- "Audit this codebase for security vulnerabilities, performance issues, and code quality problems"

## Requirements
- ANTHROPIC_API_KEY or GOOGLE_API_KEY (for sub-agents)
- The `delegate` tool must be registered in the agent's toolset
