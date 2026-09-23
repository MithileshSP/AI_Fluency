"""Day 2: Direct Prompting vs Chain-of-Thought on the Personal Project Tracker.

The private project data is NOT included in these questions. This script
tests how prompt structure affects multi-step reasoning when all required
facts are already present in the question.
"""

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day_1_Task")
    )
)

from config import client, MODEL, banner


QUESTIONS = [
    (
        "Q1 - Daily work calculation",
        "I have 18 hours remaining on a project and 7 days left. "
        "If I work for 2 hours per day for the first 5 days, "
        "how many hours will remain for the final 2 days?"
    ),
    (
        "Q2 - Proportional workload allocation",
        "I have three projects requiring 18, 20, and 4 hours respectively. "
        "If I can spend 6 hours today and want to divide my time "
        "proportionally according to the remaining workload, "
        "how many hours should I allocate to each project?"
    ),
    (
        "Q3 - Priority reasoning from supplied facts",
        "Three projects have the following information: "
        "Project A has 18 hours remaining, 7 days left, and HIGH priority; "
        "Project B has 20 hours remaining, 18 days left, and MEDIUM priority; "
        "Project C has 4 hours remaining, 30 days left, and LOW priority. "
        "Which project should receive attention first if deadline and priority "
        "are both important? Explain briefly."
    ),
]


DIRECT_PROMPT = (
    "You are a helpful project-management assistant. "
    "Answer the user's question directly. Give the final answer clearly. "
    "Do not provide a step-by-step derivation."
)

COT_PROMPT = (
    "You are a helpful project-management assistant. "
    "Solve the problem using explicit numbered calculation/reasoning steps. "
    "Keep the reasoning concise and relevant to the question. "
    "After the steps, write the last line exactly as: "
    "Final Answer: <answer>"
)


def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("DAY 2: DIRECT PROMPTING VS CHAIN-OF-THOUGHT")

    for number, (title, question) in enumerate(QUESTIONS, start=1):
        print("=" * 78)
        print(f"{title}")
        print(f"QUESTION: {question}\n")

        print("--- WITHOUT CoT / DIRECT PROMPTING ---")
        print(ask(DIRECT_PROMPT, question))
        print()

        print("--- WITH CoT / STRUCTURED REASONING ---")
        print(ask(COT_PROMPT, question))
        print()
