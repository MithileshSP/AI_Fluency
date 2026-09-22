"""Challenge question.

This question is intentionally outside the predefined workflow rules.

The agent should use the private project data and reason about which
project deserves the user's limited available time.
"""

from config import CHALLENGE_QUESTION
from workflow import workflow
from agent import agent


print("Q:", CHALLENGE_QUESTION)

print(
    "\nWorkflow :",
    workflow(CHALLENGE_QUESTION)
)

print(
    "\nAgent    :",
    agent(CHALLENGE_QUESTION)
)