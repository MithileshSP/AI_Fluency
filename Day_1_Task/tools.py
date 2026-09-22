"""Tools available to the AI agent.

The agent cannot directly access PROJECTS from the prompt.
It must use these tools to retrieve private project information.
"""

import ast
import operator

from config import PROJECTS


# ---------------------------------------------------------
# TOOL 1: GET PROJECT INFORMATION
# ---------------------------------------------------------

def get_project_info(project_name: str) -> str:
    """Return private information about a project."""

    key = project_name.strip().upper().replace(" ", "_")

    # Allow common aliases
    aliases = {
        "AI_FLUENCY_TRAINING": "AI_FLUENCY",
        "AI_FLUENCY": "AI_FLUENCY",
        "SMART_FARMING": "SMART_FARMING",
        "SMART_FARMING_ASSISTANT": "SMART_FARMING",
        "COE_PORTAL": "COE_PORTAL",
        "COE_PORTAL_IMPROVEMENTS": "COE_PORTAL",
    }

    key = aliases.get(key, key)

    project = PROJECTS.get(key)

    if project is None:
        return f"Unknown project: {project_name}"

    return str({
        "project": project["name"],
        "status": project["status"],
        "estimated_hours": project["estimated_hours"],
        "completed_hours": project["completed_hours"],
        "remaining_hours": (
            project["estimated_hours"]
            - project["completed_hours"]
        ),
        "days_remaining": project["days_remaining"],
        "priority": project["priority"],
    })


# ---------------------------------------------------------
# TOOL 2: LIST ALL PROJECTS
# ---------------------------------------------------------

def list_projects() -> str:
    """Return the names of all projects in the private tracker."""

    return str([
        project["name"]
        for project in PROJECTS.values()
    ])


# ---------------------------------------------------------
# TOOL 3: SAFE CALCULATOR
# ---------------------------------------------------------

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _evaluate(node):

    if isinstance(node, ast.Constant) and isinstance(
        node.value,
        (int, float)
    ):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression safely."""

    try:
        result = _evaluate(
            ast.parse(
                expression,
                mode="eval"
            ).body
        )

        return str(result)

    except Exception as error:
        return f"Calculator error: {error}"


# ---------------------------------------------------------
# FUNCTION REGISTRY
# ---------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_project_info": get_project_info,
    "list_projects": list_projects,
    "calculator": calculator,
}


# ---------------------------------------------------------
# TOOL SCHEMAS PROVIDED TO THE LLM
# ---------------------------------------------------------

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_project_info",
            "description": (
                "Get private information about a project including "
                "status, estimated hours, completed hours, remaining "
                "hours, deadline in days, and priority."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": (
                            "Name of the project, such as "
                            "AI Fluency Training, Smart Farming Assistant, "
                            "or COE Portal Improvements."
                        )
                    }
                },
                "required": ["project_name"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "list_projects",
            "description": (
                "List all projects available in the private project tracker."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Perform arithmetic calculations using +, -, *, / "
                "and parentheses."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    },
]


if __name__ == "__main__":

    print("\n=== TOOL TESTS ===\n")

    print(
        "get_project_info('AI Fluency Training') ->",
        get_project_info("AI Fluency Training")
    )

    print(
        "get_project_info('Smart Farming Assistant') ->",
        get_project_info("Smart Farming Assistant")
    )

    print(
        "calculator('30 - 12') ->",
        calculator("30 - 12")
    )

    print(
        "list_projects() ->",
        list_projects()
    )