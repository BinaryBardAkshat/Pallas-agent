# Obsidian Sync

## Description
Read, write, search, and organize notes in an Obsidian vault. Create structured notes with proper frontmatter, maintain backlinks, and keep your knowledge base organized using Obsidian's markdown conventions.

## When to Use
- Saving research findings, meeting notes, or project documentation to Obsidian
- Searching your vault for related notes or past research
- Creating daily notes, project pages, or MOCs (Maps of Content)
- Organizing and tagging notes in bulk
- Extracting and summarizing information from existing vault notes

## Instructions
When working with an Obsidian vault:

**Configuration**: The vault path must be set. Ask the user: "What is the path to your Obsidian vault?" if `OBSIDIAN_VAULT_PATH` is not set in the environment, or look for common paths (`~/Documents/Obsidian`, `~/Obsidian`, `~/vault`).

**Reading notes**:
```
file(action="read", path="<vault_path>/<note>.md")
```

**Writing a new note** — always include frontmatter:
```markdown
---
title: Note Title
date: 2026-03-17
tags: [tag1, tag2]
aliases: []
---

# Note Title

Content here...

## Related
- [[Related Note 1]]
- [[Related Note 2]]
```

**Searching the vault**:
```
terminal(command="grep -r 'search term' '<vault_path>' --include='*.md' -l")
```

**Creating a daily note**:
- Path: `<vault_path>/Daily Notes/YYYY-MM-DD.md`
- Use today's date from system

**Conventions to follow**:
- Use `[[WikiLinks]]` for internal links
- Use `#tags` for inline tagging
- Keep file names in `kebab-case` or `Title Case`
- Never delete existing content without confirmation

## Examples
- "Save these research notes to my Obsidian vault under Research/AI"
- "Find all my notes about Python and summarize them"
- "Create a project page for Project X in my vault"
- "Add today's meeting notes to my daily note"

## Requirements
- File tool with read/write access to vault directory
- Terminal tool for search
- OBSIDIAN_VAULT_PATH env var (optional, will ask if missing)
