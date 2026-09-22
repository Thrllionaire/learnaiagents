"""Lesson 02 — the same answer, with you holding the control flow.

No loop. No `tools=`. You decide which functions to call, you call them, and the
model does the one thing it is uniquely good at: turning two facts into a
sentence. One API call, and you could draw this flowchart before seeing the input.

    uv run python practice/02-workflow-vs-agent/workflow.py
"""

import anthropic

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

QUESTION = "What's the weather in Tokyo and what time is it there?"


def get_weather(location: str) -> str:
    return f"8°C, light rain, wind 20km/h in {location}"


def get_time(timezone: str) -> str:
    return f"The time in {timezone} is 12:00 PM."


def run_workflow(user_input: str) -> str:
    # The predefined code path. You chose these two calls at design time; nothing
    # about the input can change which ones run.
    weather = get_weather("Tokyo")
    time = get_time("Asia/Tokyo")

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Answer the question using only these facts.\n\n"
                    f"Weather: {weather}\n"
                    f"Time: {time}\n\n"
                    f"Question: {user_input}"
                ),
            }
        ],
    )

    print("WORKFLOW")
    print("  API calls    : 1")
    print("  input tokens :", response.usage.input_tokens)
    print("  output tokens:", response.usage.output_tokens)
    print("-" * 60)
    return next((b.text for b in response.content if b.type == "text"), "")


if __name__ == "__main__":
    print(run_workflow(QUESTION))
