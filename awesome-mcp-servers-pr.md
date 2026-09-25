# awesome-mcp-servers submission patch

Prepared 2026-09-22 for the public-repository step of the FreeLLM-MCP bet.

## Target

Repository: https://github.com/punkpeye/awesome-mcp-servers

Section: `Server Implementations` -> `Monitoring`

The target's contribution guide says entries must be accurate, follow existing style, and stay in
alphabetical order. It also fast-tracks agent PRs when the title ends in `🤖🤖🤖`.

## Repository entry

Insert this line after the `ejcho623/...` entry and before the `enmanuelmag/...` entry:

```markdown
- [emberfreellm/freellm-mcp](https://github.com/emberfreellm/freellm-mcp) [![FreeLLM-MCP MCP server](https://glama.ai/mcp/servers/emberfreellm/freellm-mcp/badges/score.svg)](https://glama.ai/mcp/servers/emberfreellm/freellm-mcp) 🐍 🏠 🍎 🪟 🐧 - Live measured free-LLM availability, throughput, 7-day reliability, and tool-calling diagnostics for AI agents. Install from the repository with `python3 -m pip install .`.
```

The placement is alphabetical by **owner/repository**, not by repository slug: `emberfreellm/...`
belongs between `ejcho623/...` and `enmanuelmag/...`. The existing
`emberfreellm/awesome-mcp-servers@add-freellm-mcp` branch was rebuilt from current upstream with this
one added line and must be left untouched.

Do not advertise `pip install freellm-watch-mcp` unless the package is separately published to PyPI.
The package-name endpoint returned HTTP 404 on 2026-09-22; the verified installation path is
`python3 -m pip install .` from the repository.

## Repository contents

Create a public repository named `freellm-mcp` from the current `experiments/mcp/` directory. Include
only:

- `server.py`
- `test_server.py`
- `conformance_check.py`
- `README.md`
- `pyproject.toml`
- `registry.json`
- `.gitignore`
- `LICENSE`

Exclude `.venv/`, `build/`, `dist/`, `__pycache__/`, `.pytest_cache/`, and `*.egg-info/`.

## Pull request

1. Commit the clean repository with a short description and verification results.
2. Fork `punkpeye/awesome-mcp-servers`, create an `add-freellm-mcp` branch, and insert the line above.
3. Open one pull request titled `Add FreeLLM-MCP 🤖🤖🤖`.
4. In the PR body, state that the server has 9 passing unit tests, a 14/14 official-SDK conformance
   check, zero third-party runtime dependencies, and a source installation verified in an isolated
   environment.
