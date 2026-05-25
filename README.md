# coffee-agent

A toy agent built with [BurrMCP](https://github.com/msradam/burrmcp): a coffee
ordering workflow defined as a [Burr](https://burr.dagworks.io/) state machine
and served as an [MCP](https://modelcontextprotocol.io/) server. An LLM drives
it one transition at a time, and the server enforces the order of operations.

```mermaid
stateDiagram-v2
    [*] --> take_order
    take_order --> add_modifier
    take_order --> pay
    take_order --> cancel
    add_modifier --> add_modifier
    add_modifier --> pay
    add_modifier --> cancel
    pay --> fulfill
    fulfill --> [*]
    cancel --> [*]
```

This diagram is the contract. The agent can only move along these edges; the
server refuses any step that is not a reachable transition. The workflow lives
in the state machine, not in a prompt the model has to remember. Pay before
ordering, or fulfill before paying, and the response is a structured refusal
listing the actions that are actually reachable.

An LLM drives it over MCP. Here fast-agent connects a Llama-3.3-70B model
(on Together) and the model calls the `step` tool to walk the order:

![coffee-agent driven by an LLM](demos/coffee-agent-agent.gif)

The same workflow is observable from the terminal. `coffee-agent render` prints
the graph; `coffee-agent sessions show` replays a recorded run, refusals in red:

![coffee-agent observability](demos/coffee-agent.gif)

## Build it yourself

This whole repo is about 90 lines. The shape:

1. `src/coffee_agent/app.py` defines the Burr graph (five `@action`s and the
   transitions between them).
2. `src/coffee_agent/cli.py` wraps it in BurrMCP's `build_cli` so the package
   ships a `coffee-agent` command with the graph baked in.
3. `pyproject.toml` depends on `burrmcp` and registers the console script.

## Install

```bash
git clone https://github.com/msradam/coffee-agent.git
cd coffee-agent
uv venv --python 3.13
uv pip install -e .
```

`coffee-agent serve` now runs the MCP server over stdio. You usually do not run
it directly; an MCP client launches it for you (below).

## Run it as an agent

The repo ships an `.mcp.json` pointing a client at `coffee-agent serve`. Pick a
client:

### Claude Code (zero extra install if you have it)

```bash
claude mcp add --transport stdio coffee-agent -- uv run coffee-agent serve
claude
```

Then ask: "Order a latte with an extra shot and pay for it." Claude calls the
`step` tool to walk the graph.

### fast-agent (a terminal REPL, Python)

The repo ships a `fastagent.config.yaml` defining this server, so:

```bash
uvx fast-agent-mcp go --servers coffee-agent -m "Order a latte and pay for it, then fulfill the order."
```

It uses Gemini by default (set `GOOGLE_API_KEY`). To drive it with a Together
model instead, set `GENERIC_API_KEY` and add
`--model generic.meta-llama/Llama-3.3-70B-Instruct-Turbo`. For a fully local
run, point the config's `generic.base_url` at Ollama.

### MCPJam (one npx command, free hosted models, browser playground)

```bash
npx @mcpjam/inspector
```

Add the server with command `uv` and args `run coffee-agent serve`, then chat in
the playground.

## Watch what it did

Every step is recorded to Burr's tracker. From the repo:

```bash
uv run coffee-agent sessions ls
uv run coffee-agent sessions show         # per-step timeline, refusals in red
uv run coffee-agent watch                 # live-tail a running session
```

`coffee-agent` inherits these observability commands from BurrMCP.

## License

Apache 2.0. Built on [BurrMCP](https://github.com/msradam/burrmcp),
[Apache Burr](https://github.com/apache/burr), and
[FastMCP](https://github.com/jlowin/fastmcp).
