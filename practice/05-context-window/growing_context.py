"""Lesson 05 -- watch one conversation's input tokens grow, turn by turn.

Same tool as Lesson 03's good_tools.py, exact-match and all -- that bug is
not this lesson's problem. What's different: this is ONE conversation, five
user turns deep, and `messages` is never reset between them. Every turn
resends everything before it: the tool schema, every past question, every
past tool call and result.

    uv run python practice/05-context-window/growing_context.py

Your job (see NOTES.md) is not to fix a bug. It's to:
  1. record how input tokens grow turn over turn
  2. add compaction -- and see what it costs you to add it
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import anthropic

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

DATA = json.loads((Path(__file__).parent / "data.json").read_text())

# Five turns, one conversation. Each depends on customers named in an
# earlier turn -- turn 4 needs turn 1-3's answers; turn 5 needs all of them.
CONVERSATION = [
    "Has Priya Raman had an order delivered later than promised, and is "
    "there an open ticket about it?",
    "Now check Marcus Dubois the same way.",
    "And Sofia Almeida?",
    "Of the three, whose open ticket is the most urgent?",
    "Write a one-paragraph summary of all three customers' delivery status, "
    "for a handoff to the next support agent.",
]


# ---------------------------------------------------------------- the surface

TOOL_SCHEMAS = [
    {
        "name": "list_late_orders_and_tickets",
        "description": (
            "Given a customer's full name, returns their late deliveries and "
            "their currently open support tickets in a single call. Use this "
            "when investigating a delivery complaint. An order counts as late "
            "when it shipped after its promised date; orders that have not "
            "shipped at all are NOT included. Open means not yet closed - "
            "closed and pending tickets are not returned. Dates are ISO "
            "(YYYY-MM-DD) and days_late is a whole number of days. Does not "
            "cover billing, order contents, or ticket history."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_name": {
                    "type": "string",
                    "description": (
                        "The customer's full name as it appears on the account, "
                        "e.g. 'Priya Raman'. Matched exactly."
                    ),
                }
            },
            "required": ["customer_name"],
        },
    },
]

PRIORITY = DATA["enums"]["ticket_priority_code"]


def _day(epoch_ms: int) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).date().isoformat()


def list_late_orders_and_tickets(customer_name: str) -> str:
    customer = get_customer(customer_name)
    orders = list_orders(customer["uuid"])
    late = [
        o
        for o in orders
        if o["shipped_at_epoch_ms"]
        and o["shipped_at_epoch_ms"] > o["promised_at_epoch_ms"]
    ]
    open_tickets = [
        t
        for t in DATA["tickets"]
        if t["state_code"] == 1 and t["customer_uuid"] == customer["uuid"]
    ]
    return json.dumps(
        {
            "customer": customer["full_name"],
            "late_orders": [
                {
                    "item": o["sku"],
                    "promised": _day(o["promised_at_epoch_ms"]),
                    "delivered": _day(o["shipped_at_epoch_ms"]),
                    "days_late": round(
                        (o["shipped_at_epoch_ms"] - o["promised_at_epoch_ms"])
                        / 86_400_000
                    ),
                }
                for o in late
            ],
            "open_tickets": [
                {
                    "subject": t["subject"],
                    "opened": _day(t["opened_at_epoch_ms"]),
                    "priority": PRIORITY[str(t["priority_code"])],
                }
                for t in open_tickets
            ],
        }
    )


def get_customer(customer_name: str):
    for c in DATA["customers"]:
        if c["full_name"] == customer_name:
            return c
    raise ValueError(f"No customer named '{customer_name}'")


def list_orders(customer_uuid: str):
    return [o for o in DATA["orders"] if o["customer_uuid"] == customer_uuid]


TOOLS = {"list_late_orders_and_tickets": list_late_orders_and_tickets}


# ------------------------------------------------------------- the exercise


def compact(messages: list) -> tuple[list, int]:
    """Summarize `messages` into a single message.

    Also returns what THIS CALL cost in input tokens. Compaction is not
    free: to compress the history, it must first send the full history
    it's compressing -- once, at full price -- so that cost has to be
    counted in the total, not thrown away.
    """
    _, answer, tokens = run_turn(
        messages,
        "Summarize the conversation so far into a single message for a support agent.",
    )
    return [{"role": "user", "content": answer}], tokens


def run_turn(messages: list, user_input: str) -> tuple[list, str, int]:
    """Runs one user turn to completion (including any tool calls inside
    it) against the growing `messages` list. Returns the updated messages,
    the model's final text answer, and the total input tokens spent on
    THIS turn (which may be more than one API call if tools were used)."""
    messages = messages + [{"role": "user", "content": user_input}]
    turn_input_tokens = 0

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        turn_input_tokens += response.usage.input_tokens

        if response.stop_reason != "tool_use":
            answer = next((b.text for b in response.content if b.type == "text"), "")
            return messages, answer, turn_input_tokens

        messages = messages + [{"role": "assistant", "content": response.content}]
        results = []
        for block in response.content:
            if block.type == "tool_use":
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": TOOLS[block.name](**block.input),
                    }
                )
        messages = messages + [{"role": "user", "content": results}]


if __name__ == "__main__":
    messages: list = []
    total_input_tokens = 0  # lifetime total for the whole run -- never reset
    last_turn_tokens = 0  # size of the window on the most recent call --
    # this is what decides whether to compact, not
    # the lifetime total

    for i, user_input in enumerate(CONVERSATION, start=1):
        if last_turn_tokens > 2000:
            messages, compaction_tokens = compact(messages)
            total_input_tokens += compaction_tokens
            print(f"\n[compaction fired -- cost {compaction_tokens} input tokens]")

        messages, answer, turn_tokens = run_turn(messages, user_input)
        total_input_tokens += turn_tokens
        last_turn_tokens = turn_tokens

        print(f"\n{'=' * 68}")
        print(f"TURN {i}: {user_input}")
        print(f"{'-' * 68}")
        print(answer)
        print(f"{'-' * 68}")
        print(f"messages in context : {len(messages)}")
        print(f"input tokens (this turn) : {turn_tokens}")
        print(f"input tokens (lifetime total): {total_input_tokens}")
