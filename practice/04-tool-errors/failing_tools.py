"""Lesson 04 — what the model is actually told when your tool fails.

This is your own good_tools.py from Lesson 03, unchanged, with two additions:

  * a customer name on the command line, so you can drive it into failure
  * the loop now prints every tool_result exactly as the model receives it

The bugs are deliberate. Do not fix them until you have read what the model
was handed and what it told the user as a result.

    uv run python practice/04-tool-errors/failing_tools.py "Priya Raman"
    uv run python practice/04-tool-errors/failing_tools.py "Marcus Dubois"
    uv run python practice/04-tool-errors/failing_tools.py "priya raman"
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

DATA = json.loads((Path(__file__).parent / "data.json").read_text())

QUESTION = (
    "Has {name} had an order delivered later than promised, "
    "and is there an open ticket about it?"
)


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
    """Epoch milliseconds -> the date a human would write."""
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).date().isoformat()


def list_late_orders_and_tickets(customer_name: str) -> str:
    customer = get_customer(customer_name)          # <- fails on a case mismatch
    orders = list_orders(customer["uuid"])

    # <- fails when shipped_at_epoch_ms is null (an order that has not shipped)
    late = [o for o in orders if o["shipped_at_epoch_ms"] > o["promised_at_epoch_ms"]]
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
    return "null"


def list_orders(customer_uuid: str):
    return [o for o in DATA["orders"] if o["customer_uuid"] == customer_uuid]


TOOLS = {
    "list_late_orders_and_tickets": list_late_orders_and_tickets,
}


# ------------------------------------------------------- the loop + the meter


def run_agent(user_input: str) -> str:
    """Lesson 03's loop. The only change: it shows you what the model was told."""
    messages = [{"role": "user", "content": user_input}]
    api_calls = 0
    in_tokens = 0
    out_tokens = 0
    errors = 0

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        api_calls += 1
        in_tokens += response.usage.input_tokens
        out_tokens += response.usage.output_tokens

        if response.stop_reason != "tool_use":
            break

        messages.append({"role": "assistant", "content": response.content})

        results = []
        for block in response.content:
            if block.type == "tool_use":
                try:
                    result = {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": TOOLS[block.name](**block.input),
                    }
                except Exception as e:
                    errors += 1
                    result = {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"Error: {e}",
                        "is_error": True,
                    }

                # This is the whole point of the file: read what the model reads.
                print(f"  -> {block.name}({block.input})")
                print(f"     is_error : {result.get('is_error', False)}")
                print(f"     content  : {result['content']}")
                results.append(result)

        messages.append({"role": "user", "content": results})

    answer = next((b.text for b in response.content if b.type == "text"), "")

    print("-" * 68)
    print("API calls   :", api_calls)
    print("tool errors :", errors)
    print("input tokens:", in_tokens)
    print("output tokens:", out_tokens)
    print("-" * 68)
    return answer


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Priya Raman"
    print(f"QUESTION: {QUESTION.format(name=name)}\n")
    print("ANSWER TO THE USER:\n" + run_agent(QUESTION.format(name=name)))
