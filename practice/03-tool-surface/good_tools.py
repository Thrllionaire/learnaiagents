"""Lesson 03 — the task-shaped tool surface.

One tool, shaped like the question a human would ask, returning language instead
of storage. Compare against naive_tools.py: same loop, same model, same question.

    uv run python practice/03-tool-surface/good_tools.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import anthropic

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

DATA = json.loads((Path(__file__).parent / "data.json").read_text())

QUESTION = (
    "Has Priya Raman had an order delivered later than promised, "
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
    customer = get_customer(customer_name)
    orders = list_orders(customer["uuid"])

    late = [o for o in orders if o["shipped_at_epoch_ms"] > o["promised_at_epoch_ms"]]
    open_tickets = [
        t
        for t in DATA["tickets"]
        if t["state_code"] == 1 and t["customer_uuid"] == customer["uuid"]
    ]

    # Everything below is the actual redesign: the model gets names, dates and
    # states, never uuids, enum codes or epoch milliseconds.
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


def get_customer(customer_name: str) -> str:
    for c in DATA["customers"]:
        if c["full_name"] == customer_name:
            return c
    return "null"


def list_orders(customer_uuid: str) -> str:
    return [o for o in DATA["orders"] if o["customer_uuid"] == customer_uuid]


def list_tickets(customer_uuid: str) -> str:
    return json.dumps(
        [t for t in DATA["tickets"] if t["customer_uuid"] == customer_uuid]
    )


TOOLS = {
    "list_late_orders_and_tickets": list_late_orders_and_tickets,
}


# ------------------------------------------------------- the loop + the meter


def run_agent(user_input: str) -> str:
    """Lesson 01's loop, with the accounting from Lesson 02 and a call trace."""
    messages = [{"role": "user", "content": user_input}]
    api_calls = 0
    in_tokens = 0
    out_tokens = 0
    trace = []

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
                trace.append(block.name)
                try:
                    output = TOOLS[block.name](**block.input)
                    results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": output,
                        }
                    )
                except Exception as e:
                    results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {e}",
                            "is_error": True,
                        }
                    )

        messages.append({"role": "user", "content": results})

    answer = next((b.text for b in response.content if b.type == "text"), "")

    print("tool calls  :", len(trace), "->", " -> ".join(trace) or "(none)")
    print("API calls   :", api_calls)
    print("input tokens:", in_tokens)
    print("output tokens:", out_tokens)
    print("-" * 60)
    return answer


if __name__ == "__main__":
    print(run_agent(QUESTION))
    # print(list_late_orders_and_tickets("Priya Raman"))
