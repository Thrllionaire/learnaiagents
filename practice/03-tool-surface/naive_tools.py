"""Lesson 03 — the endpoint-shaped tool surface.

Four tools, one per "route", each returning the stored record verbatim. This is
what wrapping an API gets you, and it is the baseline you are going to beat.

Read the four definitions before you run this. Predict the number of tool calls
it takes to answer QUESTION, and write the prediction in NOTES.md first.

    uv run python practice/03-tool-surface/naive_tools.py
"""

import json
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
        "name": "list_customers",
        "description": "Lists all customers.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_customer",
        "description": "Gets a customer record.",
        "input_schema": {
            "type": "object",
            "properties": {"customer_uuid": {"type": "string"}},
            "required": ["customer_uuid"],
        },
    },
    {
        "name": "list_orders",
        "description": "Lists orders for a customer.",
        "input_schema": {
            "type": "object",
            "properties": {"customer_uuid": {"type": "string"}},
            "required": ["customer_uuid"],
        },
    },
    {
        "name": "list_tickets",
        "description": "Lists tickets for a customer.",
        "input_schema": {
            "type": "object",
            "properties": {"customer_uuid": {"type": "string"}},
            "required": ["customer_uuid"],
        },
    },
]


def list_customers() -> str:
    return json.dumps(DATA["customers"])


def get_customer(customer_uuid: str) -> str:
    for c in DATA["customers"]:
        if c["uuid"] == customer_uuid:
            return json.dumps(c)
    return "null"


def list_orders(customer_uuid: str) -> str:
    return json.dumps(
        [o for o in DATA["orders"] if o["customer_uuid"] == customer_uuid]
    )


def list_tickets(customer_uuid: str) -> str:
    return json.dumps(
        [t for t in DATA["tickets"] if t["customer_uuid"] == customer_uuid]
    )


TOOLS = {
    "list_customers": list_customers,
    "get_customer": get_customer,
    "list_orders": list_orders,
    "list_tickets": list_tickets,
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
