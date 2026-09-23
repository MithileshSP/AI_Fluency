"""Day 2: Self-consistency on a Personal Project Tracker calculation.

The same reasoning question is run several times with a non-zero
temperature. The final answers are extracted and the majority answer
is reported.
"""

import sys
import os
from collections import Counter

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day_1_Task")
    )
)

from config import client, MODEL, banner
from cot_compare import COT_PROMPT


RUNS = 5
TEMPERATURE = 0.8

QUESTION = (
    "I have three projects requiring 18, 20, and 4 hours respectively. "
    "If I can spend 6 hours today and want to divide my time "
    "proportionally according to the remaining workload, "
    "how many hours should I allocate to each project?"
)


def final_answer(text):
    """Extract the text after the last 'Final Answer:' line."""
    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()

    return text.splitlines()[-1].strip() if text.strip() else "(empty)"


def run_many(question, runs=RUNS, temperature=TEMPERATURE):
    answers = []

    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": COT_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
        )

        answer = final_answer(response.choices[0].message.content)
        print(f"run {attempt}: {answer}")
        answers.append(answer)

    return answers


if __name__ == "__main__":
    banner("DAY 2: SELF-CONSISTENCY")

    print("QUESTION:")
    print(QUESTION)
    print()
    print(f"Running {RUNS} attempts with temperature={TEMPERATURE}\n")

    answers = run_many(QUESTION)

    winner, count = Counter(answers).most_common(1)[0]

    print("\n--- SUMMARY ---")
    print(f"Majority answer: {winner}")
    print(f"Frequency: {count}/{len(answers)}")

    print("\nAll extracted answers:")
    for index, answer in enumerate(answers, start=1):
        print(f"{index}. {answer}")
