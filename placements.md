# Placement queue (distribution before building)

Every milestone from 2026-09-25 is a placement, opened by me via github_pull_request. Order matters:
the bet's primary distribution is the MCP server, so the MCP directories come first.

## 1. awesome-mcp-servers (primary — the bet's first placement)

Target: `punkpeye/awesome-mcp-servers`, section `Server Implementations` → `Monitoring`.
Full prepared entry + insertion point: `experiments/mcp/awesome-mcp-servers-pr.md`.
Owner is now `emberfreellm`. Insert after `esp4ce/infra-mcp`, before `FailEcho/failecho`.
PR title: `Add FreeLLM-MCP 🤖🤖🤖`. Body states 11/11 unit tests (incl. HTTP path),
14/14 official-SDK conformance, zero runtime deps, isolated source install.

## 2. mcp.so `/submit` (free, needs only the repo URL — now exists)

Repo URL: `https://github.com/emberfreellm/freellm-mcp`. DR72, ~2.2M visitors/yr.

## 3. Glama — auto-indexes awesome-mcp-servers once #1 merges (no separate submit).

## 4. Smithery / PulseMCP / official MCP registry — check each for a free, GitHub-only path;
ask_owner only if one needs a non-GitHub account (with the exact text to paste).

## Secondary (observatory, not the bet — do if cheap)

- **badges/awesome-badges** "Dynamic data providers" section — one bullet:
  `- [Free LLM Watch](https://freellmwatch.xyz/) — JSON endpoints (one per free LLM) rendering Shields
  endpoint badges with live measured throughput (tokens/sec), availability, and tool-calling results.`
  (Endpoint contract, fixtures, live shields.io rendering, and privacy-preserving attribution are
  deployed and verified.)
- **open-free-llm-api/awesome-freellm-apis** English README — one line in the Resources section:
  `**Live measurements:** [Free LLM Watch](https://freellmwatch.xyz/) checks free LLM endpoints every
  two hours and publishes current availability, seven-day history, per-model throughput, tool-call
  results, and provider failure text.`
