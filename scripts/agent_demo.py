"""Paced replay of an LLM driving coffee-agent over MCP.

A live agent run scrolls past too fast to read, so this replays the real
sequence of tool calls at a readable cadence. The actions and state are what a
fast-agent + Llama-3.3-70B run actually produced; only the pacing is added.
"""

from __future__ import annotations

import sys
import time

from rich.console import Console
from rich.theme import Theme

THEME = Theme(
    {
        "ok": "bold #9ccfd8",
        "action": "bold #c4a7e7",
        "muted": "#6e6a86",
        "subtle": "#908caa",
        "accent": "#ebbcba",
        "prompt": "bold #f6c177",
    }
)
console = Console(theme=THEME)

PROMPT = "Order a latte and pay 5 dollars, then fulfill the order."
STEPS = [
    ("take_order", "item=latte, qty=1", "ordered"),
    ("pay", "amount=5", "paid"),
    ("fulfill", "", "fulfilled  · terminal"),
]


def main() -> None:
    if sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
        time.sleep(0.4)
    console.print(f"[muted](coffee-agent) >[/] [prompt]{PROMPT}[/]")
    time.sleep(1.1)
    console.print()
    console.print("[subtle]the model reads burr://graph, then drives the FSM one step at a time:[/]")
    console.print()
    time.sleep(1.0)
    for action, args, state in STEPS:
        console.print(
            f"  [subtle]→[/] [muted]step[/] [action]{action:<12}[/] [subtle]{args:<22}[/]",
            end="",
        )
        time.sleep(0.7)
        console.print(f"  [ok]✓[/]  [subtle]{state}[/]")
        time.sleep(0.9)
    console.print()
    time.sleep(0.4)
    console.print("[muted]3 tool calls · the server enforced every transition · order fulfilled[/]")


if __name__ == "__main__":
    main()
