"""System 3: AI Agent = LLM + Tools + Loop.

The agent can:
1. Reason about the user's request.
2. Select an appropriate tool.
3. Access private project data through the tool.
4. Observe the tool result.
5. Continue reasoning and calling tools.
6. Return a final answer.
"""

import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a personal project management assistant.

The user has a private project tracker containing information that
the language model cannot directly access.

IMPORTANT RULES:

1. Never invent private project information.
2. Whenever the user asks about a project's status, hours, deadline,
   priority, or other private project information, use the available
   tools.
3. Use calculator for arithmetic.
4. You may call multiple tools when a question requires information
   from multiple projects.
5. After observing tool results, continue reasoning if more information
   is required.
6. If the question does not require private data, answer directly.
7. Give a concise final answer after completing the required tool calls.

Available projects can be discovered using list_projects().
"""


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # -------------------------------------------------
        # 1. REASON
        # -------------------------------------------------

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0,
        )

        message = response.choices[0].message


        # -------------------------------------------------
        # 2. FINISHED?
        # -------------------------------------------------

        if not message.tool_calls:

            return message.content.strip()


        # -------------------------------------------------
        # 3. ADD ASSISTANT TOOL REQUEST
        # -------------------------------------------------

        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        }
                    }
                    for call in message.tool_calls
                ]
            }
        )


        # -------------------------------------------------
        # 4. ACT + OBSERVE
        # -------------------------------------------------

        for call in message.tool_calls:

            name = call.function.name

            arguments = json.loads(
                call.function.arguments or "{}"
            )

            function = TOOL_FUNCTIONS.get(name)

            if function:

                result = function(**arguments)

            else:

                result = f"Unknown tool: {name}"


            if verbose:

                print(
                    f"  step {step}: "
                    f"{name}({arguments}) -> {result}"
                )


            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result),
                }
            )


    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        print("A:", agent(question))

        print("-" * 70)