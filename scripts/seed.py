"""Seed one coffee-agent session for the demo recording.

Walks the FSM through a refusal (qty=0) and a clean order, so
`coffee-agent sessions show` has a red row and green rows to render.
"""

from __future__ import annotations

import asyncio

from fastmcp import Client

from theodosia import ServingMode, mount
from coffee_agent.app import build_application


async def main() -> None:
    server = mount(build_application(), mode=ServingMode.STEP, name="coffee-agent")
    async with Client(server) as client:

        async def step(action, **inputs):
            await client.call_tool("step", {"action": action, "inputs": inputs})

        await step("take_order", item="latte", qty=0)  # refusal: action_error
        await step("take_order", item="latte", qty=1)
        await step("add_modifier", modifier="oat_milk")
        await step("pay", amount=6)
        await step("fulfill")


if __name__ == "__main__":
    asyncio.run(main())
