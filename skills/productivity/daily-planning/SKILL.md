# Daily Planning

## Description
This skill enables Pallas to facilitate a complete daily planning session: reviewing open tasks, assessing priorities, building a realistic time-blocked schedule, and closing the day with a brief review. It accounts for energy levels, meetings, and carryover from yesterday.

## When to Use
- First thing in the morning when the user wants to plan their day
- When the user feels overwhelmed and doesn't know where to start
- At the end of the day for a review and handoff to tomorrow
- When the user says "help me plan today" or "what should I focus on?"

## Instructions
You are the user's thinking partner for daily planning. Your job is to help them make intentional choices about time — not to create a perfect schedule they will abandon by 10am.

**Morning Planning Session**

**Step 1 — Situational Awareness**
Ask or retrieve from memory:
- What meetings or fixed commitments exist today? (times, durations)
- What carried over from yesterday that was not completed?
- Are there any deadlines today or tomorrow?
- How is the user's energy and focus level today? (High / Medium / Low)

**Step 2 — Task Inventory**
List all candidate tasks from:
- Open todos in memory
- Items explicitly mentioned by the user
- Any follow-ups from yesterday's review

For each task, note:
- Estimated time (be realistic — most people underestimate by 2x)
- Priority: `URGENT+IMPORTANT`, `IMPORTANT`, `URGENT`, `NEITHER`
- Energy required: Deep work (requires focus) vs. Shallow work (can do while tired)

**Step 3 — Time Blocking**
Build the day block by block:
1. Place fixed commitments first (meetings, calls)
2. Place the most important deep work task in the highest-energy window (usually morning)
3. Place shallow work (email, admin, review) in post-lunch or low-energy windows
4. Leave 20% of the day unscheduled as buffer — things always take longer
5. Flag tasks that won't fit today — explicitly defer them to tomorrow or a specific future date

Present the schedule in this format:
```
09:00 - 10:30 | [DEEP WORK] Draft technical spec for auth redesign
10:30 - 11:00 | Buffer / email
11:00 - 12:00 | [MEETING] Sprint planning
12:00 - 13:00 | Lunch
13:00 - 14:30 | [DEEP WORK] Code review backlog
14:30 - 15:00 | [SHALLOW] Slack + async replies
15:00 - 16:00 | [TASK] Deploy staging build
16:00 - 16:30 | End-of-day review
```

**Step 4 — Identify the One Thing**
Ask: "If you only accomplish one thing today, what would make today a success?" This becomes the protected priority that cannot be displaced.

**Evening Review Session**

At end of day (or when user asks for EOD review):
1. What was completed? (celebrate briefly)
2. What was not completed and why? (reschedule or drop)
3. What surprised you today? (unexpected tasks, meetings that ran long)
4. What needs to happen first thing tomorrow?
5. Save a brief summary to memory as tomorrow's starting context

**Principles:**
- A schedule with 5 tasks is better than one with 15
- If everything is urgent, nothing is — help the user make real priority choices
- Never shame the user for not completing things — adjust and move forward

## Examples
- "Help me plan my day."
- "I have 4 hours of meetings and a deadline at 5pm — help me figure out what's realistic."
- "Let's do my end of day review."
