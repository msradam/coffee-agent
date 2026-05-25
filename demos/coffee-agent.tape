# Demo: coffee-agent render + sessions show, Rose Pine.
# Record with: vhs demos/coffee-agent.tape

Output demos/coffee-agent.gif

Set Shell "bash"
Set Theme "rose-pine"
Set FontSize 16
Set Width 1200
Set Height 560
Set Padding 20
Set TypingSpeed 28ms

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

# The graph is the contract.
Type "coffee-agent render"
Sleep 600ms
Enter
Sleep 3s

# Seed a session off-camera (after render, so it is the most-recent one).
Hide
Type "python scripts/seed.py >/dev/null 2>&1"
Enter
Sleep 4s
Type "clear"
Enter
Show

# The recorded walk: a refusal (red) then the clean path.
Type "coffee-agent sessions show --project coffee-agent"
Sleep 600ms
Enter
Sleep 2s
Screenshot demos/coffee-agent.png
Sleep 2s
