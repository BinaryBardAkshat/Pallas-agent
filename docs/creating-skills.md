# Creating Skills

Skills are Markdown instruction files that extend Pallas's behavior for specific domains or workflows. They are loaded on demand, not baked into the system prompt, which keeps the base context lean.

---

## Skill Markdown Format

A skill is a single `SKILL.md` file inside a named directory. The directory name is the skill's identifier. Example structure:

```
~/.pallas/skills/
└── code-review/
    └── SKILL.md
```

A complete `SKILL.md` uses these sections:

```markdown
# Skill Name

## Description
Two or three sentences explaining what this skill does and when it helps.

## When to Use
- Bullet list of situations that should trigger this skill
- Keep each bullet short and specific

## Instructions
Detailed instructions written for the agent (not the user).
This section is injected into the agent's context verbatim.
Use imperative language: "Always...", "Never...", "First do X, then Y."

## Examples
- "Review the PR at github.com/..."
- "Check this function for security issues"
- "Audit the SQL queries in db.py"

## Requirements
- Any environment variables needed (e.g., GITHUB_TOKEN)
- Any tools that must be available (e.g., `terminal` with git installed)
- Any Python packages (e.g., `pip install semgrep`)
```

---

## Full SKILL.md Template

```markdown
# [Skill Name]

## Description
[What this skill does. What problem it solves. Who benefits from it.]

## When to Use
- [Trigger scenario 1]
- [Trigger scenario 2]
- [Trigger scenario 3]

## Instructions
You are operating in [Skill Name] mode. Follow these steps precisely:

1. [First action]
2. [Second action]
3. [Third action]

Always [important constraint].
Never [important prohibition].

Output format: [describe expected output shape]

## Examples
- "[Example prompt 1]"
- "[Example prompt 2]"
- "[Example prompt 3]"

## Requirements
- Tools: [list required tools]
- Env vars: [list required environment variables, or "None"]
- Packages: [list required Python packages, or "None"]
```

---

## Skill Categories

Pallas ships with built-in skills organized into these categories. Custom skills can be placed in any category or a new one — the category directory name has no functional impact.

| Category | Examples |
|---|---|
| `software-development` | Code review, refactoring, test generation |
| `research` | Paper analysis, competitive intel, summarization |
| `productivity` | Obsidian sync, Notion integration, task planning |
| `github` | PR creation, issue triage, release notes |
| `mlops` | Training pipeline, model evaluation, deployment |
| `creative` | Copywriting, blog posts, marketing briefs |
| `domain` | Legal, medical, finance domain-specific reasoning |
| `media` | Image captioning, video summarization |
| `note-taking` | Meeting notes, knowledge base entry |
| `autonomous-ai-agents` | Multi-agent orchestration, self-healing agents |

---

## How Skills Are Loaded

1. `SkillCommands` in `pallas_core/skill_commands.py` reads `~/.pallas/skills/`
2. It lists all subdirectories and checks each for a `SKILL.md` file
3. When `SkillManagerTool` is invoked with `action=invoke`, it calls `invoke_skill_prompt(name, user_query)`
4. This returns a combined string: skill content + user request, which is prepended to the next LLM call

```python
class SkillCommands:
    def list_skills(self) -> List[str]:
        return sorted(d.name for d in self.skills_dir.iterdir() if d.is_dir())

    def invoke_skill_prompt(self, name: str, user_query: str) -> str:
        content = self.get_skill(name)
        return (
            f"You have a skill called '{name}'. Follow these instructions precisely:\n\n"
            f"{content}\n\n"
            f"User request: {user_query}"
        )
```

---

## Installing Skills

### Install a built-in skill

Built-in skills live in the `skills/` directory of the repository. Copy any of them into `~/.pallas/skills/`:

```bash
cp -r skills/software-development/code-review ~/.pallas/skills/
```

Or use the CLI (v0.2.0+):

```bash
pallas skills install code-review
```

### Install from optional-skills

The `optional-skills/` directory contains more advanced packs not installed by default:

```bash
cp -r optional-skills/research/academic-paper-analysis ~/.pallas/skills/
```

### Create a new skill interactively (v0.2.0+)

```bash
pallas skills create
```

This scaffolds a new `SKILL.md` in `~/.pallas/skills/<name>/` using the template above.

### Verify a skill is loaded

```bash
pallas skills list
```

---

## Writing Effective Instructions

The `## Instructions` section is the most important part. It is injected directly into the agent's context, so quality matters.

**Be specific about output format.** If you want a table, say so. If you want JSON, include an example schema.

**Use numbered steps for sequential workflows.** The agent follows numbered lists more reliably than prose paragraphs.

**Reference tools by name.** Writing "use the `terminal` tool to run `git log`" is more reliable than "check the git history".

**Keep the skill focused.** A skill that tries to do too many things will dilute all of them. Create separate skills for separate workflows.

**Test with real examples.** After creating a skill, run one of your `## Examples` prompts and verify the agent behaves as expected.
