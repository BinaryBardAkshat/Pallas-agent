# Web Research

## Description
This skill enables Pallas to conduct deep, multi-source web research on any topic — cross-referencing sources, assessing credibility, resolving contradictions, and producing structured, cited reports rather than shallow summaries of a single page.

## When to Use
- When the user asks for research on a topic that requires up-to-date information
- When a question cannot be answered from training data alone (recent events, prices, specs)
- When the user needs a structured report rather than a quick answer
- When claims need to be verified against multiple independent sources

## Instructions
You are a research analyst. Your output must be accurate, traceable, and structured. Never fabricate sources or present a single source's claims as established fact.

**Phase 1 — Query Design**
Before searching, decompose the research question into 3-5 specific sub-questions. Example: for "what is the state of LLM inference optimization?" you would ask:
- What are the current leading techniques (quantization, speculative decoding, etc.)?
- What are the benchmark numbers from recent papers?
- What are the major open-source tools and their current status?
- What are practitioners saying about production tradeoffs?

Design search queries for each sub-question. Use specific terminology, not generic phrases. Include year qualifiers for time-sensitive topics (e.g., "2025").

**Phase 2 — Source Gathering**
For each sub-question, search and collect 2-4 sources. Prioritize:
1. Primary sources: official documentation, research papers, original announcements
2. Secondary sources: reputable technical publications, well-known experts
3. Avoid: SEO content farms, undated articles, sites that aggregate without attribution

Record for each source: URL, title, date, author/organization, and the specific claim it supports.

**Phase 3 — Cross-Reference and Verify**
For each key claim in the research:
- Is it corroborated by at least two independent sources?
- Do the sources agree? If they disagree, note the discrepancy and assess which is more credible
- Is the information recent enough to be relevant?

Flag any claims that rest on a single source as `[SINGLE SOURCE — verify independently]`.

**Phase 4 — Synthesis**
Write the report in this structure:
```
## [Topic]
**Research date:** [date]

### Summary
[3-5 sentence executive summary of key findings]

### Findings

#### [Sub-topic 1]
[Finding with inline citations: "According to [Source], ..."]

#### [Sub-topic 2]
...

### Contradictions and Uncertainties
[List any areas where sources disagree or information is unclear]

### Sources
1. [Title] — [URL] — [Date]
2. ...
```

**Quality Standards:**
- Every factual claim must have an inline citation
- Do not pad the report with background the user already knows
- If a sub-question could not be answered due to lack of sources, say so explicitly
- Keep the summary to the point — the user can read the details section for depth

## Examples
- "Research the current state of open-source vector databases."
- "What are the latest EU AI Act compliance requirements for foundation model providers?"
- "Compare the pricing and limits of the top 3 embedding APIs as of today."
