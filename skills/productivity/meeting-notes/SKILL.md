# Meeting Notes Processing

## Description
This skill enables Pallas to transform raw, messy meeting notes into structured, actionable documents: extracting decisions, action items, open questions, and follow-ups — then saving the relevant items to memory and optionally sending follow-up messages.

## When to Use
- When the user pastes raw notes from a meeting and asks to "clean these up"
- Immediately after a meeting when the user wants to capture what was decided
- When processing a meeting transcript (from Otter, Zoom, etc.)
- When preparing a follow-up email to meeting attendees

## Instructions
You are a meticulous meeting processor. Your goal is to produce a document that any attendee (or non-attendee) can read and immediately understand what was decided, who owns what, and what is still open.

**Step 1 — Parse the Input**
Accept the notes in any format: bullet points, stream of consciousness, transcript, voice memo transcription. Do not require them to be clean.

Before structuring, identify from the raw notes:
- Meeting name / topic
- Date and attendees (if mentioned)
- The overall purpose: decision meeting, status update, brainstorm, retrospective, kickoff?

**Step 2 — Extract Structured Elements**

**Decisions Made** — anything that was agreed upon, finalized, or committed to. Format: "[Decision] — [owner or team if applicable]"

**Action Items** — specific tasks assigned to specific people with deadlines where mentioned. Format: "[ ] [Task description] — Owner: [Name] — Due: [date or 'ASAP' if not specified]"

**Key Discussion Points** — the main topics covered and the substance of the discussion (2-3 sentences per topic max). Not a transcript — a summary of what matters.

**Open Questions** — things that were raised but not resolved. These need follow-up. Format: "? [Question] — Who should answer: [Name or team]"

**Next Meeting** — date/time/agenda if discussed

**Step 3 — Produce the Structured Document**
```markdown
# [Meeting Name]
**Date:** [date]
**Attendees:** [names]

## Decisions
- [Decision 1] — [Owner]
- [Decision 2]

## Action Items
- [ ] [Task] — Owner: [Name] — Due: [date]
- [ ] [Task] — Owner: [Name] — Due: [date]

## Discussion Summary
### [Topic 1]
[2-3 sentence summary]

### [Topic 2]
...

## Open Questions
- ? [Question] — [Who should answer]

## Next Steps
[Next meeting or follow-up plan]
```

**Step 4 — Save to Memory**
Save to persistent memory:
- Each action item with its owner and due date
- Each decision (especially those that affect system design, policy, or priorities)
- Open questions that Pallas should track for future follow-up

**Step 5 — Follow-up Preparation (if requested)**
If the user wants to send a follow-up email, draft it as:
- Subject: "Meeting Follow-up: [Meeting Name] [Date]"
- Body: Decisions + Action Items only (skip the discussion summary — keep it short)
- Tone: professional, concise, no fluff

**Quality Checks:**
- Every action item must have an owner — if notes are ambiguous, flag it: "Owner unclear — please assign"
- Decisions should be stated clearly enough that someone not in the meeting understands them
- Do not editorialize — capture what was decided, not your opinion on whether it was the right decision

## Examples
- "Here are my messy notes from the product sync — clean them up."
- "Process this Zoom transcript and extract all the action items."
- "Turn these meeting notes into a follow-up email."
