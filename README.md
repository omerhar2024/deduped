# Deduped MCP server: AI use cases for trending GitHub AI repos

[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-com.dedupedai%2Fdeduped--mcp-blue)](https://registry.modelcontextprotocol.io/v0.1/servers?search=com.dedupedai)
[![Remote MCP](https://img.shields.io/badge/remote%20MCP-streamable%20HTTP-brightgreen)](https://dedupedai.com/mcp)
[![No auth](https://img.shields.io/badge/auth-none-success)](https://dedupedai.com/developers/?utm_source=github&utm_medium=readme)
[![Glama](https://img.shields.io/badge/Glama-listed-8A2BE2)](https://glama.ai/mcp/connectors/com.dedupedai/deduped-mcp)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Use cases on Deduped](https://dedupedai.com/badge/deduped/deduped-mcp.svg)](https://dedupedai.com/developers/?utm_source=github&utm_medium=readme)

A free, read-only **Model Context Protocol (MCP) server** that turns the hottest AI repos on GitHub into practical, step by step use cases with copy and paste agent prompts, plus a deduplicated daily AI news brief.

- **Remote endpoint:** `https://dedupedai.com/mcp` (Streamable HTTP, no API key, no account)
- **Official MCP Registry name:** `com.dedupedai/deduped-mcp`
- **Also here:** a single-file local stdio server, `deduped_mcp.py`
- Works with Claude Code, Claude Desktop, Cursor, ChatGPT, VS Code, Windsurf and any MCP client

## Tools

| Tool | What it does |
| --- | --- |
| `search_use_cases(query, category?, limit?)` | Find use cases for a task. Returns id, title, summary, repo and page url |
| `get_use_case(id)` | Steps, a copy and paste agent prompt, requirements, risks, caveat and repo url |
| `hot_repos(limit?)` | Hottest AI repos of the last 90 days, best first, with a plain English line each |
| `today_news()` | Today's AI news brief, each story once |

All four tools are read-only. Data is rebuilt daily from the free public Deduped API (`https://dedupedai.com/api/v1`).

## Quick install (remote, nothing to install)

### Claude Code

```sh
claude mcp add --transport http deduped https://dedupedai.com/mcp
```

Add `--scope user` to make it available in every project. Check with `claude mcp list`.

### Claude Desktop

Option A, custom connector: Settings, then Connectors, then **Add custom connector**. Name `Deduped`, URL `https://dedupedai.com/mcp`.

Option B, config file. Add this to `claude_desktop_config.json` and restart (needs Node.js for `npx`):

```json
{
  "mcpServers": {
    "deduped": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://dedupedai.com/mcp"]
    }
  }
}
```

### Cursor

[![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en/install-mcp?name=deduped&config=eyJ1cmwiOiJodHRwczovL2RlZHVwZWRhaS5jb20vbWNwIn0=)

Or add this to `~/.cursor/mcp.json` (or `.cursor/mcp.json` in your project):

```json
{
  "mcpServers": {
    "deduped": {
      "url": "https://dedupedai.com/mcp"
    }
  }
}
```

### ChatGPT

1. Settings, then Apps and Connectors, then Advanced settings: turn on **Developer mode**.
2. Create a connector. Name `Deduped`, MCP server URL `https://dedupedai.com/mcp`, Authentication **No authentication**.
3. In a chat, pick Developer mode and enable the Deduped connector.

### VS Code (GitHub Copilot agent mode)

```sh
code --add-mcp '{"name":"deduped","type":"http","url":"https://dedupedai.com/mcp"}'
```

Or in `.vscode/mcp.json`:

```json
{
  "servers": {
    "deduped": { "type": "http", "url": "https://dedupedai.com/mcp" }
  }
}
```

### Windsurf and other clients

Any client that speaks Streamable HTTP: `{ "mcpServers": { "deduped": { "serverUrl": "https://dedupedai.com/mcp" } } }` (Windsurf uses `serverUrl`, most others use `url`). For stdio-only clients, use `npx -y mcp-remote https://dedupedai.com/mcp` or the local server below.

## Local stdio server (optional)

1. Get `deduped_mcp.py`, or clone:

   ```sh
   git clone https://github.com/omerhar2024/deduped.git
   cd deduped
   ```

2. Install the MCP SDK (Python 3.10+): `pip install -r requirements.txt` (or `pip install mcp`).

3. Self test (offline, fake data): `python3 deduped_mcp.py --selftest`

4. Point your client at it:

   ```sh
   claude mcp add deduped -- python3 /absolute/path/to/deduped_mcp.py
   ```

   Claude Desktop and Cursor JSON: see `claude_desktop_config.example.json` and `cursor_mcp.example.json`. More in `claude_code.md`.

Settings: `DEDUPED_API_BASE` (default `https://dedupedai.com/api/v1`), `DEDUPED_CACHE_S` (response cache in seconds, default 600).

## Example prompts

- "Find a Deduped use case for turning a folder of PDFs into a searchable knowledge base, then give me the steps."
- "What are the 5 hottest AI repos right now and what is each one good for?"
- "Show me practical use cases for voice cloning and the agent prompt for the best one."
- "Summarize today's AI news from Deduped."

## Plain JSON API

No MCP client? Every use case, hot repo and news item is a static JSON file:

```sh
curl -s https://dedupedai.com/api/v1/index.json
```

OpenAPI 3.1 spec: https://dedupedai.com/api/openapi.json

## Links

- Developers and API docs: https://dedupedai.com/developers/?utm_source=github&utm_medium=readme
- Browse use cases: https://dedupedai.com/use-cases/?utm_source=github&utm_medium=readme
- Hot AI repos: https://dedupedai.com/repos/?utm_source=github&utm_medium=readme
- Free daily email: https://dedupedai.com/join/?utm_source=github&utm_medium=readme
- Questions: hello@dedupedai.com

## Notes

Use cases are AI-generated from each repo's README and can be wrong. The repos belong to their owners and keep their own licenses. When you show a use case to a person, link its url. Disclaimer: https://dedupedai.com/disclaimer/

Keywords: mcp, mcp-server, model-context-protocol, remote-mcp, ai, ai-agents, github-trending, ai-use-cases, ai-news, claude, cursor, chatgpt

License: MIT
