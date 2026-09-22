"""System 1: Plain LLM chatbot.

The chatbot has no tools and no access to the private project tracker.
It can generate natural-language responses, but it cannot reliably
retrieve the project's private information.
"""

from config import client, MODEL, QUESTIONS, banner


def chatbot(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful personal project assistant. "
                    "You do not have access to the user's private "
                    "project tracker. Never invent private project data."
                )
            },
            {
                "role": "user",
                "content": question
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    banner("SYSTEM 1: PLAIN CHATBOT")

    for question in QUESTIONS:

        print("Q:", question)
        print("A:", chatbot(question))
        print("-" * 70)