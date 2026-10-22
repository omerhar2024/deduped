[![Use cases on Deduped](https://dedupedai.com/badge/deduped/deduped-mcp.svg)](https://dedupedai.com/developers/?utm_source=github&utm_medium=readme)

# deduped-mcp

Deduped turns the hottest AI repos on GitHub into practical, step by step use cases, plus a deduplicated daily AI news brief.

This is a single-file MCP server that gives Claude Desktop, Cursor, Claude Code or any MCP client read-only access to the free public Deduped API (`https://dedupedai.com/api/v1`). No API key, no account.

## Tools

| Tool | What it does |
| --- | --- |
| `search_use_cases(query, category?, limit?)` | Find use cases for a task. Returns id, title, summary, repo and page url |
| `get_use_case(id)` | Steps, a copy and paste agent prompt, requirements, risks, caveat and repo url |
| `hot_repos(limit?)` | Hottest AI repos of the last 90 days, best first, with a plain English line each |
| `today_news()` | Today's AI news brief, each story once |

## Remote endpoint (nothing to install)

Clients that speak Streamable HTTP can use the hosted server at `https://dedupedai.com/mcp` (same 4 tools, no auth):

```sh
claude mcp add --transport http deduped https://dedupedai.com/mcp
```

In Cursor or other JSON configs: `{ "mcpServers": { "deduped": { "url": "https://dedupedai.com/mcp" } } }`

The single-file local server below does the same over stdio.

## Install

1. Get `deduped_mcp.py`: download it from this repo (open the file, then "Download raw file"), or clone:

   ```sh
   git clone <url of this repo>
   cd deduped-mcp
   ```

2. Install the MCP SDK (Python 3.10+):

   ```sh
   pip install -r requirements.txt
   ```

   or simply `pip install mcp`.

3. Check it works (offline, uses fake data):

   ```sh
   python3 deduped_mcp.py --selftest
   ```

4. Run it (your MCP client normally starts it for you):

   ```sh
   python3 deduped_mcp.py
   ```

## Claude Desktop

Add this to `claude_desktop_config.json` (see `claude_desktop_config.example.json`) and restart Claude Desktop:

```json
{
  "mcpServers": {
    "deduped": {
      "command": "python3",
      "args": ["/absolute/path/to/deduped_mcp.py"]
    }
  }
}
```

## Cursor

Add the same block to `~/.cursor/mcp.json` or `.cursor/mcp.json` in your project (see `cursor_mcp.example.json`).

## Claude Code

```sh
claude mcp add deduped -- python3 /absolute/path/to/deduped_mcp.py
```

More in `claude_code.md`.

## Example prompts

- "Find a Deduped use case for turning a folder of PDFs into a searchable knowledge base, then give me the steps."
- "What are the 5 hottest AI repos right now and what is each one good for?"
- "Show me practical use cases for voice cloning and the agent prompt for the best one."
- "Summarize today's AI news from Deduped."

## Settings

- `DEDUPED_API_BASE`: default `https://dedupedai.com/api/v1`
- `DEDUPED_CACHE_S`: response cache in seconds, default 600

## Links

- Developers and API docs: https://dedupedai.com/developers/?utm_source=github&utm_medium=readme
- Sign up for the Deduped email: https://dedupedai.com/join/?utm_source=github&utm_medium=readme
- Questions: hello@dedupedai.com

## Notes

Use cases are AI-generated from each repo's README and can be wrong. The repos belong to their owners and keep their own licenses. When you show a use case to a person, link its url. Disclaimer: https://dedupedai.com/disclaimer/

License: MIT
