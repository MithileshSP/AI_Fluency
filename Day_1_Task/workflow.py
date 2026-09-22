"""System 2: Rule-based workflow.

This system does not use an LLM.

It follows predefined rules for a limited set of project-tracker
questions. It can access private data directly because the rules
are connected to the local project database.
"""

import re

from config import PROJECTS, QUESTIONS


def workflow(question):

    text = question.lower()

    # -----------------------------------------------------
    # RULE 1: STATUS OF A PROJECT
    # -----------------------------------------------------

    if "status" in text:

        if "ai fluency" in text:

            project = PROJECTS["AI_FLUENCY"]

            return (
                f"Status of {project['name']}: "
                f"{project['status']}"
            )

        if "smart farming" in text:

            project = PROJECTS["SMART_FARMING"]

            return (
                f"Status of {project['name']}: "
                f"{project['status']}"
            )

        if "coe portal" in text:

            project = PROJECTS["COE_PORTAL"]

            return (
                f"Status of {project['name']}: "
                f"{project['status']}"
            )


    # -----------------------------------------------------
    # RULE 2: REMAINING HOURS FOR ONE PROJECT
    # -----------------------------------------------------

    if "remaining" in text and "hours" in text:

        if "ai fluency" in text:

            project = PROJECTS["AI_FLUENCY"]

            remaining = (
                project["estimated_hours"]
                - project["completed_hours"]
            )

            return (
                f"Remaining work for {project['name']}: "
                f"{remaining} hours"
            )

        if "smart farming" in text:

            project = PROJECTS["SMART_FARMING"]

            remaining = (
                project["estimated_hours"]
                - project["completed_hours"]
            )

            return (
                f"Remaining work for {project['name']}: "
                f"{remaining} hours"
            )

        if "coe portal" in text:

            project = PROJECTS["COE_PORTAL"]

            remaining = (
                project["estimated_hours"]
                - project["completed_hours"]
            )

            return (
                f"Remaining work for {project['name']}: "
                f"{remaining} hours"
            )


    # -----------------------------------------------------
    # RULE 3: TOTAL REMAINING HOURS FOR TWO PROJECTS
    # -----------------------------------------------------

    if "total" in text and "hours" in text:

        if (
            "smart farming" in text
            and "coe portal" in text
        ):

            smart_farming = PROJECTS["SMART_FARMING"]

            coe_portal = PROJECTS["COE_PORTAL"]

            smart_remaining = (
                smart_farming["estimated_hours"]
                - smart_farming["completed_hours"]
            )

            coe_remaining = (
                coe_portal["estimated_hours"]
                - coe_portal["completed_hours"]
            )

            total = smart_remaining + coe_remaining

            return (
                f"Total remaining work: {total} hours"
            )


    # -----------------------------------------------------
    # NO MATCHING RULE
    # -----------------------------------------------------

    return (
        "Sorry, I do not have a predefined rule "
        "for this type of question."
    )


if __name__ == "__main__":

    print(
        "\n=== SYSTEM 2: RULE-BASED WORKFLOW ===\n"
    )

    for question in QUESTIONS:

        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)