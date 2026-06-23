from anthropic import Anthropic
from tools import ticket_classifier

# Initialize client
client = Anthropic()

# Register available Python functions
tool_functions = {
    "classify_ticket": ticket_classifier
}

# Tool definition
tools = [
    {
        "name": "classify_ticket",
        "description": "Classify a support ticket and return the requested fields.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticket_text": {
                    "type": "string",
                    "description": "The full text of the support ticket to classify."
                },
                "fields_needed": {
                    "type": "array",
                    "description": "List of classification fields to return. Valid values are product_area, severity, and intent.",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["ticket_text", "fields_needed"]
        }
    }
]

# Initial conversation
messages = [
    {
        "role": "user",
        "content": (
            "From: sarah.chen@globalcorp.com Subject: Cannot access SSO login — entire team locked out Our team of 40 has been unable to log in via SSO since 09:00 this morning. We have a client demo in 3 hours. This is completely blocking us."
        )
    }
]

iteration = 1

while True:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    print(f"Iteration {iteration}")
    print(f"Stop reason: {response.stop_reason}")

    # MANDATORY: append assistant response immediately
    messages.append(
        {
            "role": "assistant",
            "content": response.content
        }
    )

    if response.stop_reason == "end_turn":
        final_text = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        print("\nFinal Response:")
        print(final_text)
        break

    elif response.stop_reason == "tool_use":
        tool_results = []

        for block in response.content:
            if block.type != "tool_use":
                continue

            tool_name = block.name
            tool_input = block.input

            result = tool_functions[tool_name](**tool_input)

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                }
            )

        messages.append(
            {
                "role": "user",
                "content": tool_results
            }
        )

    iteration += 1