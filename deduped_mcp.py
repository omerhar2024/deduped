#!/usr/bin/env python3
"""Deduped MCP server: practical AI use cases from hot GitHub AI repos, the hot repos and today's AI news.

Single file. Speaks MCP over stdio using the official `mcp` Python package and only READS the free public
static JSON API at https://dedupedai.com/api/v1 over HTTPS. No key, no account, nothing is written anywhere.

Tools: search_use_cases, get_use_case, hot_repos, today_news.

Usage:
  pip install mcp
  python3 deduped_mcp.py              # serve MCP over stdio
  python3 deduped_mcp.py --selftest   # offline self test with fake data (no network, no mcp package needed)

Env: DEDUPED_API_BASE (default https://dedupedai.com/api/v1), DEDUPED_CACHE_S (default 600 seconds).
License: MIT
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

__version__ = "0.1.0"
API = os.environ.get("DEDUPED_API_BASE", "https://dedupedai.com/api/v1").rstrip("/")
CACHE_S = int(os.environ.get("DEDUPED_CACHE_S") or 600)
UA = "deduped-mcp/%s (+https://dedupedai.com/developers/)" % __version__
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*--[a-z0-9][a-z0-9-]*$")
STOP = {"a", "an", "the", "to", "for", "with", "and", "or", "of", "in", "my", "i", "how", "use"}
_cache = {}


def http_fetch(path):
    """GET API/path and parse JSON, cached for CACHE_S seconds."""
    now = time.time()
    hit = _cache.get(path)
    if hit and now - hit[0] < CACHE_S:
        return hit[1]
    req = urllib.request.Request(API + "/" + path, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        doc = json.loads(r.read().decode("utf-8"))
    _cache[path] = (now, doc)
    return doc


# The fetch function in use. The self test swaps it for a fake one.
FETCH = http_fetch


def _words(s):
    return re.findall(r"[a-z0-9]+", (s or "").lower())


def search_use_cases(query, category=None, limit=8):
    """Search the use case catalog. Returns ids, titles, summaries, repos and page urls."""
    items = FETCH("search.json").get("items", [])
    q = set(_words(query)) - STOP
    out = []
    for it in items:
        if category and category.lower() not in (it.get("c") or "").lower():
            continue
        fields = [(it.get("t"), 3.0), (it.get("rt"), 2.5), (it.get("r"), 2.0), (it.get("s"), 1.5),
                  (it.get("o"), 1.0), (it.get("w"), 1.0), (it.get("c"), 0.5)]
        score = 0.0
        for text, wgt in fields:
            ws = set(_words(text))
            score += wgt * sum(1 for t in q if t in ws or any(w.startswith(t) for w in ws if len(t) > 3))
        if q and score == 0:
            continue
        score += 0.5 * (it.get("sc") or 0) + (0.3 if it.get("b") else 0) + (0.2 if it.get("f") else 0)
        out.append((score, it))
    out.sort(key=lambda x: -x[0])
    base = API.rsplit("/api/", 1)[0]
    n = max(1, min(int(limit or 8), 25))
    return [{"id": it["id"], "title": it.get("t"), "summary": it.get("s"), "repo": it.get("r"),
             "category": it.get("c"), "best": it.get("b"), "seen_in_the_wild": it.get("f"),
             "url": base + it.get("u", "")} for _, it in out[:n]]


def get_use_case(id):
    """One use case with steps, a copy and paste agent prompt, requirements, risks and the repo url."""
    if not ID_RE.match(id or ""):
        raise ValueError("id must look like repo-slug--use-case-slug (from search_use_cases)")
    doc = FETCH("usecases/%s.json" % id)
    keep = ("id", "title", "repo", "repo_url", "summary", "who", "problem", "outcome", "steps", "agent_prompt",
            "requirements", "risks", "caveat", "difficulty", "time", "agents", "seen_in_the_wild", "url",
            "disclaimer")
    return {k: doc.get(k) for k in keep if k in doc}


def hot_repos(limit=10):
    """The hottest AI repos on GitHub right now, best first."""
    items = [x for x in FETCH("repos.json").get("items", []) if x.get("show", True)]
    n = max(1, min(int(limit or 10), 50))
    return [{k: x.get(k) for k in ("repo", "title", "what", "language", "stars", "gain", "url", "use_cases", "uc_n")}
            for x in items[:n]]


def today_news():
    """Today's deduped AI news brief."""
    d = FETCH("news.json")
    return {"date": d.get("date"), "subject": d.get("subject"), "url": d.get("url"),
            "items": [{k: x.get(k) for k in ("rank", "title", "category", "coverage_tag", "body", "story_url")}
                      for x in d.get("items", [])]}


def _safe(fn, *args, **kwargs):
    """Run a tool and turn network or input errors into a readable message for the model."""
    try:
        return fn(*args, **kwargs)
    except urllib.error.HTTPError as ex:
        if ex.code == 404:
            return {"error": "Not found. Use search_use_cases to get a valid id."}
        return {"error": "HTTP %s from %s" % (ex.code, API)}
    except (TypeError, ValueError, OSError) as ex:
        return {"error": "%s: %s" % (type(ex).__name__, ex)}


def serve():
    """Start the MCP stdio server. Imports `mcp` only here."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        sys.stderr.write("The mcp package is missing. Install it with: pip install mcp\n")
        sys.exit(1)

    app = FastMCP("deduped", instructions=(
        "Use search_use_cases to find a practical AI use case for the user's task, then get_use_case for steps "
        "and an agent prompt. Link the use case url when you show it."))

    @app.tool(name="search_use_cases")
    def t_search(query: str, category: str = "", limit: int = 8) -> dict:
        """Search Deduped's catalog of practical AI use cases generated from hot GitHub AI repos.
        Returns ids, titles, summaries and page urls. Then call get_use_case for steps and an agent prompt.
        category is an optional filter, e.g. Research, Content, Software and DevOps. limit is 1 to 25."""
        res = _safe(search_use_cases, query, category or None, limit)
        return res if isinstance(res, dict) else {"items": res}

    @app.tool(name="get_use_case")
    def t_get(id: str) -> dict:
        """One use case: who it is for, steps, a copy and paste agent prompt, requirements, risks, caveat and
        the repo url. id comes from search_use_cases, e.g. owner-repo--use-case-slug."""
        return _safe(get_use_case, id)

    @app.tool(name="hot_repos")
    def t_hot(limit: int = 10) -> dict:
        """The hottest AI repos on GitHub right now (last 90 days, best first), with a plain English line each.
        limit is 1 to 50."""
        res = _safe(hot_repos, limit)
        return res if isinstance(res, dict) else {"items": res}

    @app.tool(name="today_news")
    def t_news() -> dict:
        """Today's deduped AI news brief: the top stories, each once, with category and a short summary."""
        return _safe(today_news)

    app.run()


FAKE = {
    "search.json": {"items": [
        {"id": "acme-voice--clone-a-voice", "t": "Clone a voice for narration", "s": "Make narration audio.",
         "r": "acme/voice", "c": "Content", "u": "/use-cases/acme-voice/#clone-a-voice", "sc": 1, "b": True},
        {"id": "acme-docs--pdf-search", "t": "Searchable PDF knowledge base", "s": "Ask questions over PDFs.",
         "r": "acme/docs", "c": "Research", "u": "/use-cases/acme-docs/#pdf-search", "sc": 2},
    ]},
    "usecases/acme-docs--pdf-search.json": {"id": "acme-docs--pdf-search", "title": "Searchable PDF knowledge base",
                                            "steps": ["Install", "Index", "Ask"], "agent_prompt": "Set it up.",
                                            "internal": "dropped"},
    "repos.json": {"items": [{"repo": "acme/docs", "title": "docs", "stars": 10},
                             {"repo": "acme/hidden", "show": False},
                             {"repo": "acme/voice", "title": "voice", "stars": 5}]},
    "news.json": {"date": "2026-01-01", "subject": "Today", "url": "https://dedupedai.com/x/",
                  "items": [{"rank": 1, "title": "Story", "category": "Models", "extra": 1}]},
}


def _fake_fetch(path):
    if path not in FAKE:
        raise urllib.error.HTTPError(API + "/" + path, 404, "Not Found", None, None)
    return FAKE[path]


def selftest():
    """Exercise every tool against fake data. No network and no mcp package needed."""
    global FETCH
    old, FETCH = FETCH, _fake_fetch
    try:
        r = search_use_cases("searchable pdf knowledge")
        assert r and r[0]["id"] == "acme-docs--pdf-search", r
        assert r[0]["url"] == API.rsplit("/api/", 1)[0] + "/use-cases/acme-docs/#pdf-search", r[0]["url"]
        assert search_use_cases("voice", category="content")[0]["repo"] == "acme/voice"
        assert search_use_cases("nothingmatcheshere") == []
        assert len(search_use_cases("", limit=1)) == 1
        u = get_use_case("acme-docs--pdf-search")
        assert u["steps"] == ["Install", "Index", "Ask"] and "internal" not in u, u
        try:
            get_use_case("../etc/passwd")
            raise AssertionError("bad id accepted")
        except ValueError:
            pass
        assert "Not found" in _safe(get_use_case, "acme-docs--missing")["error"]
        h = hot_repos(5)
        assert [x["repo"] for x in h] == ["acme/docs", "acme/voice"], h
        n = today_news()
        assert n["date"] == "2026-01-01" and n["items"][0] == {"rank": 1, "title": "Story", "category": "Models",
                                                                "coverage_tag": None, "body": None,
                                                                "story_url": None}, n
    finally:
        FETCH = old
    print("selftest ok")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    if "--version" in sys.argv[1:]:
        print(__version__)
        sys.exit(0)
    serve()
