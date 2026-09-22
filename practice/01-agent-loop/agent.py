import anthropic

client = anthropic.Anthropic()

# 1. THE TOOL SCHEMAS — what the model is allowed to ask for.
#    The description is prompt, not documentation. The model reads it.
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


# 2. THE DISPATCH TABLE — your side of the contract.
def get_weather(location: str) -> str:
    return f"8°C, light rain, wind 20km/h in {location}"


def get_time(timezone: str) -> str:
    return f"The time in {timezone} is 12:00 PM."


TOOLS = {"get_weather": get_weather, "get_time": get_time}


def run_agent(user_input: str) -> str:
    # 3. THE TRANSCRIPT — the agent's entire within-run memory.
    messages = [{"role": "user", "content": user_input}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=16000,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        print(response.stop_reason, [b.type for b in response.content])
        # 4. THE BRANCH — the model decides whether the loop continues.
        if response.stop_reason != "tool_use":
            break
        print(response.to_json())
        # Append the assistant turn VERBATIM — tool_use blocks intact.
        messages.append({"role": "assistant", "content": response.content})

        # Execute every requested tool. Claude may request several at once;
        # all their results must come back in ONE user message.
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(block.name)
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
                    # Errors go BACK to the model, not up the stack.
                    results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {e}",
                            "is_error": True,
                        }
                    )

        messages.append({"role": "user", "content": results})

    return next(b.text for b in response.content if b.type == "text")


print(run_agent("What's the weather in Tokyo and what time is it there?"))
