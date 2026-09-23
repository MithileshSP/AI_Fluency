"""Day 2: ReAct trace using the Personal Project Tracker tools from Day 1.

The question intentionally does not contain the private project data.
The agent must use the tools from Day_1_Task to retrieve the information
and then reason over the observations.
"""

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day_1_Task")
    )
)

from agent import agent


QUESTION = (
    "Which project should I prioritize today based on my private "
    "project tracker? Consider remaining work, days remaining, "
    "and priority. Explain why."
)


if __name__ == "__main__":
    print("=== DAY 2: ReAct AGENT TRACE ===\n")
    print("QUESTION:")
    print(QUESTION)
    print("\n--- AGENT ACTIONS AND OBSERVATIONS ---")

    answer = agent(QUESTION, max_steps=8, verbose=True)

    print("\n--- FINAL ANSWER ---")
    print(answer)
