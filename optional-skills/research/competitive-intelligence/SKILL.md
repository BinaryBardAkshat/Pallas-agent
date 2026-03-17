# Competitive Intelligence

## Description
Research and analyze competitors, market positioning, pricing, and product features. Produce actionable competitive intelligence reports that help with strategic decision-making, product planning, and positioning.

## When to Use
- Before a product launch or feature decision
- Evaluating market entry opportunities
- Understanding competitor pricing and packaging
- Monitoring competitor announcements and changes
- Building a battle card or competitive positioning document

## Instructions
When conducting competitive intelligence research:

**Step 1: Define scope**
Clarify with the user:
- Who is the target company/product?
- Who are the known competitors? (if not, discover them)
- What dimensions matter? (pricing, features, tech stack, team size, funding, etc.)

**Step 2: Research each competitor**

For each competitor, research:
- **Product**: What do they offer? Key features? Differentiators?
- **Pricing**: Plans, tiers, pricing model (seat-based, usage-based, flat rate)?
- **Market position**: Who are their customers? What segment do they target?
- **Strengths**: What are they genuinely good at?
- **Weaknesses**: Where do customers complain? (check G2, Capterra, Reddit, HackerNews)
- **Recent news**: Funding, launches, leadership changes

```python
web(query="<competitor name> pricing 2026")
web(query="<competitor name> reviews site:g2.com OR site:reddit.com")
web(query="<competitor name> funding announcement")
```

**Step 3: Build comparison matrix**

```markdown
| Feature/Dimension | Us | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| Pricing (starter) | | | | |
| Key differentiator | | | | |
| Target customer | | | | |
| Integration count | | | | |
| Free tier | | | | |
```

**Step 4: Synthesize insights**
- Where are gaps in the market that no competitor fills?
- Where is the user's product clearly superior?
- Where does the user's product need to improve to compete?
- What messaging resonates with the target customer?

**Step 5: Store findings** in memory for future reference.

## Examples
- "Research our top 5 competitors and build a comparison matrix"
- "What is Notion's pricing strategy compared to alternatives?"
- "Find weaknesses in Competitor X that we can address in our positioning"
- "Monitor recent news about our main competitors"

## Requirements
- Web tool (extensive web search required)
- Memory tool (for storing findings across sessions)
