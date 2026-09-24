#!/usr/bin/env python3
"""Independent MCP conformance check for server.py using the *official* MCP client SDK.

The unit tests in test_server.py call handle_request() directly, so they prove the
JSON-RPC shapes but not that a real MCP client can actually talk to the server.
This script spawns `server.py` as a subprocess and drives it with
`mcp.client.stdio.stdio_client` + `ClientSession` — a third-party implementation of
the protocol. If a real client can initialize, list tools and call them, the server
is conformant, not just self-consistent.

Run with the SDK venv (not the box venv):

    experiments/mcp/.venv/bin/python experiments/mcp/conformance_check.py

Exits non-zero on failure and prints every check it made.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).resolve().parent
SERVER = HERE / "server.py"

EXPECTED_TOOLS = {
    "list_free_models",
    "get_fastest_free_model",
    "get_most_reliable_free_model",
    "check_model_status",
}

checks = []


def check(name, ok, detail=""):
    checks.append((name, ok, detail))
    flag = "PASS" if ok else "FAIL"
    print(f"[{flag}] {name}" + (f" — {detail}" if detail else ""))


async def main():
    env = dict(os.environ)
    # Force the remote path so we also prove the server works on a machine that is
    # not the observatory box (no local board file).
    env["FREEMCP_STATUS_PATH"] = "/nonexistent/not-this-box/status.json"
    env.setdefault("FREEMCP_REMOTE_URL", "https://freellmwatch.xyz/api/status.json")

    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)], env=env)

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            check(
                "initialize handshake",
                init.server_info.name == "freellm-mcp",
                f"serverInfo={init.server_info.name} protocol={init.protocol_version}",
            )

            listed = await session.list_tools()
            names = {t.name for t in listed.tools}
            check("tools/list", names >= EXPECTED_TOOLS, f"got {sorted(names)}")
            for t in listed.tools:
                check(
                    f"tool schema non-empty: {t.name}",
                    bool(t.description) and isinstance(t.input_schema, dict),
                    (t.description or "")[:60],
                )

            fast = await session.call_tool("get_fastest_free_model", {})
            check("call get_fastest_free_model (isError flag)", not fast.is_error)
            fast_payload = json.loads(fast.content[0].text)
            check(
                "fastest model has measured throughput",
                isinstance(fast_payload.get("tokens_per_s"), (int, float)),
                f"{fast_payload.get('model_id')} = {fast_payload.get('tokens_per_s')} tok/s",
            )
            check(
                "payload carries provenance",
                "Free LLM Watch" in json.dumps(fast_payload),
                "measured_by present",
            )

            allm = await session.call_tool("list_free_models", {})
            all_payload = json.loads(allm.content[0].text)
            n = all_payload.get("total", 0)
            check("call list_free_models", n > 10, f"{n} models returned")
            check(
                "every model row has status + provider",
                all(m.get("status") and m.get("provider") for m in all_payload["models"]),
            )

            # A model id straight from the roster, so the tool is exercised end to end.
            sample_id = all_payload["models"][0]["model_id"]
            one = await session.call_tool("check_model_status", {"model_id": sample_id})
            one_payload = json.loads(one.content[0].text)
            check(
                "call check_model_status",
                one_payload.get("model_id") == sample_id,
                f"{sample_id} -> status={one_payload.get('status')}",
            )

            missing = await session.call_tool("check_model_status", {"model_id": "no/such-model:free"})
            missing_payload = json.loads(missing.content[0].text)
            check(
                "unknown model id degrades gracefully",
                "error" in missing_payload,
                str(missing_payload.get("error"))[:70],
            )

            bad = await session.call_tool("not_a_tool", {})
            check("unknown tool raises a protocol error", bool(bad.is_error), "isError=True")

    failed = [n for (n, ok, _) in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception as exc:  # noqa: BLE001 - we want the reason printed
        print(f"CONFORMANCE CHECK CRASHED: {type(exc).__name__}: {exc}")
        sys.exit(2)
