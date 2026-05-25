"""Coffee ordering as a Burr state machine.

Shape::

    take_order --> [add_modifier loop] --> pay --> fulfill
               \\-> cancel  (reachable from any pre-pay state)

The agent drives one transition at a time over MCP. The server enforces
the graph: paying before ordering, or fulfilling before paying, comes back
as a structured refusal listing the actions that are reachable.
"""

from __future__ import annotations

from typing import Literal

from burr.core import ApplicationBuilder, State, action
from burr.core.action import Condition

from theodosia import tracker

BASE_PRICE = 5.0
MODIFIER_PRICE = {"extra_shot": 1.0, "oat_milk": 1.0, "syrup": 1.0}


@action(reads=[], writes=["stage", "item", "qty", "modifiers", "total"])
def take_order(state: State, item: str, qty: int = 1) -> State:
    """Place a new coffee order.

    Args:
        item: Drink name, e.g. "latte", "americano".
        qty: Number of drinks; defaults to 1.
    """
    if qty < 1:
        raise ValueError(f"qty must be >= 1; got {qty}")
    return state.update(
        stage="ordered", item=item, qty=qty, modifiers=[], total=BASE_PRICE * qty
    )


@action(reads=["modifiers", "total"], writes=["modifiers", "total"])
def add_modifier(state: State, modifier: Literal["extra_shot", "oat_milk", "syrup"]) -> State:
    """Add one modifier to the order. Loops until the agent moves on.

    Args:
        modifier: One of "extra_shot", "oat_milk", "syrup". Each adds $1.00.
    """
    return state.update(
        modifiers=[*state["modifiers"], modifier],
        total=state["total"] + MODIFIER_PRICE[modifier],
    )


@action(reads=["stage", "total"], writes=["stage", "paid_amount"])
def pay(state: State, amount: float) -> State:
    """Pay for the placed order.

    Args:
        amount: Payment amount. The expected total is in state.total.
    """
    if amount < state["total"]:
        raise ValueError(f"amount {amount} is less than total {state['total']}")
    return state.update(stage="paid", paid_amount=amount)


@action(reads=["stage"], writes=["stage"])
def fulfill(state: State) -> State:
    """Mark the order fulfilled. Terminal."""
    return state.update(stage="fulfilled")


@action(reads=["stage"], writes=["stage"])
def cancel(state: State) -> State:
    """Cancel the order. Terminal; only reachable pre-pay."""
    return state.update(stage="cancelled")


def build_application():
    """Build the coffee-order Burr Application."""
    ordered = Condition.expr("stage == 'ordered'")
    paid = Condition.expr("stage == 'paid'")
    return (
        ApplicationBuilder()
        .with_actions(
            take_order=take_order,
            add_modifier=add_modifier,
            pay=pay,
            fulfill=fulfill,
            cancel=cancel,
        )
        .with_transitions(
            ("take_order", "pay", ordered),
            ("take_order", "add_modifier", ordered),
            ("take_order", "cancel", ordered),
            ("add_modifier", "pay", ordered),
            ("add_modifier", "add_modifier", ordered),
            ("add_modifier", "cancel", ordered),
            ("pay", "fulfill", paid),
        )
        .with_tracker(tracker("coffee-agent"))
        .with_state(stage="new")
        .with_entrypoint("take_order")
        .build()
    )
