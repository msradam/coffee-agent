# Demo: an LLM (via fast-agent) driving coffee-agent over MCP, Rose Pine.
# Record with: GOOGLE_API_KEY=... vhs demos/coffee-agent-agent.tape
# Needs a Gemini key in the environment (not stored here).

Output demos/coffee-agent-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 14
Set Width 1240
Set Height 760
Set Padding 20
Set TypingSpeed 24ms

Hide
Type "export VIRTUAL_ENV_DISABLE_PROMPT=1"
Enter
Type "source .venv/bin/activate >/dev/null 2>&1 || true"
Enter
Type `export PS1="(coffee-agent) > "`
Enter
Type "clear"
Enter
Show

Type `uvx fast-agent-mcp go --servers coffee-agent --model generic.meta-llama/Llama-3.3-70B-Instruct-Turbo -m "Order a latte and pay 5 dollars, then fulfill the order."`
Sleep 600ms
Enter
Sleep 28s
Screenshot demos/coffee-agent-agent.png
