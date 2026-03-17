# Academic Paper Analysis

## Description
Systematically analyze academic papers, research articles, and technical reports. Extract key contributions, methodology, results, limitations, and citations. Produce structured summaries suitable for literature reviews or research synthesis.

## When to Use
- Reviewing papers before incorporating their findings into work
- Conducting a literature review across multiple papers
- Extracting datasets, baselines, or benchmarks from ML/CS papers
- Understanding the methodology of a specific approach
- Fact-checking claims against primary sources

## Instructions
When analyzing an academic paper, follow this structured approach:

**Step 1: Obtain the paper**
- If a URL is provided: `web(query="<url>")` to fetch the abstract and content
- If a PDF path is provided: `file(action="read", path="<path>")`
- For arXiv papers: fetch `https://arxiv.org/abs/<id>` for abstract, `https://arxiv.org/pdf/<id>` for full text

**Step 2: Extract structured information**

Produce a summary with these sections:

```markdown
## Paper Summary

**Title**:
**Authors**:
**Year**:
**Venue**: (journal/conference)
**arXiv/DOI**:

### Core Contribution
[1-3 sentence answer to: what is the key new idea or result?]

### Problem Statement
[What problem does this paper solve? Why is it hard?]

### Methodology
[How did they solve it? Key technical details.]

### Results
[Key quantitative results. Include baselines for comparison.]

### Limitations & Future Work
[What the authors acknowledge as limitations]

### Key Citations
[3-5 most important cited works worth reading next]

### Relevance Assessment
[How does this relate to the user's current task/research?]
```

**Step 3: For literature reviews (multiple papers)**
- Maintain a comparison table of methods, datasets, and metrics
- Identify consensus findings vs. contested claims
- Note chronological progression of ideas

**Step 4: Store findings**
Use `memory(action="store", content="Paper: <title>. Key finding: <finding>")` to save for future retrieval.

## Examples
- "Analyze this arXiv paper and give me a structured summary"
- "Compare these 3 papers on transformer architectures"
- "Extract all the benchmark results from this ML paper"
- "Do a literature review on retrieval-augmented generation"

## Requirements
- Web tool (for fetching papers)
- File tool (for local PDFs)
- Memory tool (for storing findings)
