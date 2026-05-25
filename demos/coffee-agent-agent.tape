# Demo: an LLM driving coffee-agent over MCP, replayed at a readable pace.
# Record with: vhs demos/coffee-agent-agent.tape

Output demos/coffee-agent-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 18
Set Width 1100
Set Height 440
Set Padding 24
Set TypingSpeed 24ms

Hide
Type "source .venv/bin/activate >/dev/null 2>&1 || true"
Enter
Type "python scripts/agent_demo.py"
Enter
Sleep 500ms
Show
Sleep 9s
Screenshot demos/coffee-agent-agent.png
