"""The `coffee-agent` command, built on burrmcp's build_cli.

`coffee-agent serve` mounts the graph as an MCP server (no target needed,
the graph is baked in). `coffee-agent sessions ls` / `show` / `watch`
inspect the tracker store, same as `burrmcp`.
"""

from __future__ import annotations

from burrmcp.cli import build_cli, run

from coffee_agent.app import build_application

cli = build_cli(
    "coffee-agent",
    application=build_application,
    help="Coffee-ordering agent: a Burr state machine served over MCP.",
    server_name="coffee-agent",
)


def main() -> int:
    return run(cli)
