"""Lesson 02 — the agent, with a meter on it.

Lesson 01's agent, unchanged, plus the accounting: API calls, input tokens,
output tokens. The model owns the control flow; you are paying for that.

    uv run python practice/02-workflow-vs-agent/agent_measured.py
"""

import anthropic

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

QUESTION = "What's the weather in Tokyo and what time is it there?"


TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city. Returns temperature, "
        "conditions, and wind speed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name, e.g. Paris"},
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_time",
        "description": "Get the current time in a timezone.",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "IANA timezone, e.g. Asia/Tokyo",
                },
            },
            "required": ["timezone"],
        },
    },
]


def get_weather(location: str) -> str:
    return f"8°C, light rain, wind 20km/h in {location}"


def get_time(timezone: str) -> str:
    return f"The time in {timezone} is 12:00 PM."


TOOLS = {"get_weather": get_weather, "get_time": get_time}


def run_agent(user_input: str) -> str:
    messages = [{"role": "user", "content": user_input}]
    api_calls = 0
    in_tokens = 0
    out_tokens = 0

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
                output = TOOLS[block.name](**block.input)
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output,
                    }
                )

        messages.append({"role": "user", "content": results})

    answer = next((b.text for b in response.content if b.type == "text"), "")

    print("AGENT")
    print("  API calls    :", api_calls)
    print("  input tokens :", in_tokens)
    print("  output tokens:", out_tokens)
    print("-" * 60)
    return answer


if __name__ == "__main__":
    print(run_agent(QUESTION))
