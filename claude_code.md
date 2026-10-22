# Claude Code

Add the Deduped MCP server to Claude Code with one line (use the absolute path to your copy of `deduped_mcp.py`):

```sh
claude mcp add deduped -- python3 /absolute/path/to/deduped_mcp.py
```

Make it available in every project:

```sh
claude mcp add --scope user deduped -- python3 /absolute/path/to/deduped_mcp.py
```

Check it with `claude mcp list`, then ask: "Find a Deduped use case for turning PDFs into a searchable knowledge base."
