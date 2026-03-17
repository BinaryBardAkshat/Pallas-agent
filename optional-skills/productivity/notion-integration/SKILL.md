# Notion Integration

## Description
Read from and write to Notion databases, pages, and workspaces using the Notion API. Create structured database entries, update existing pages, and search across your Notion workspace.

## When to Use
- Logging tasks, bugs, or project updates to a Notion database
- Reading Notion pages to extract information for analysis
- Creating new pages or database entries from structured data
- Syncing agent outputs (research, code reviews, reports) directly into Notion
- Querying Notion databases for project tracking or reporting

## Instructions
**Setup**: Requires `NOTION_API_KEY` (integration token) and `NOTION_DATABASE_ID` for database operations.

To get these:
1. Go to https://www.notion.so/my-integrations → Create integration → Copy token
2. Share your Notion database/page with the integration
3. Copy the database ID from the URL: `notion.so/<workspace>/<DATABASE_ID>?v=...`

**Creating a database entry**:
```python
# Use terminal or web tool to POST to Notion API
terminal(command="""curl -X POST https://api.notion.com/v1/pages \\
  -H "Authorization: Bearer $NOTION_API_KEY" \\
  -H "Notion-Version: 2022-06-28" \\
  -H "Content-Type: application/json" \\
  -d '{"parent": {"database_id": "<DB_ID>"}, "properties": {"Name": {"title": [{"text": {"content": "Task Title"}}]}}}'
""")
```

**Querying a database**:
```python
terminal(command="""curl -X POST https://api.notion.com/v1/databases/<DB_ID>/query \\
  -H "Authorization: Bearer $NOTION_API_KEY" \\
  -H "Notion-Version: 2022-06-28" \\
  -d '{}'
""")
```

**Reading a page**:
```python
terminal(command="curl https://api.notion.com/v1/blocks/<PAGE_ID>/children -H 'Authorization: Bearer $NOTION_API_KEY' -H 'Notion-Version: 2022-06-28'")
```

**Best practices**:
- Always check if the property exists before writing to a database
- Use ISO 8601 dates for date properties
- Break long content into multiple paragraph blocks (2000 char limit per block)
- Confirm database schema before creating entries

## Examples
- "Log this bug report to my Notion bug tracker database"
- "Create a new project page in Notion with the spec I just wrote"
- "Read my Notion tasks database and summarize what's overdue"
- "Add these research findings as a new page in my Notion research database"

## Requirements
- Terminal tool or web tool
- NOTION_API_KEY environment variable
- NOTION_DATABASE_ID environment variable (for database operations)
