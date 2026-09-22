"""Shared configuration and private project-tracker data.

Scenario: Personal Project Tracker

The project information below represents private project-management data.
A public LLM does not automatically know this information. The agent can
access it only through the tools provided in tools.py.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

if PROVIDER == "ollama":
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")

elif PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

elif PROVIDER == "huggingface":
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

else:
    raise SystemExit(
        f"Unknown PROVIDER '{PROVIDER}'. "
        "Use ollama, groq or huggingface."
    )

if not API_KEY:
    raise SystemExit(
        f"No API key found for PROVIDER={PROVIDER}. "
        "Check your .env file."
    )

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


# ---------------------------------------------------------
# PRIVATE PROJECT DATA
# ---------------------------------------------------------
#
# This is intentionally local/private data.
# The LLM cannot access this dictionary directly.
# It can only access it through tools.py.
#
# estimated_hours = estimated total work required
# completed_hours = work already completed
# days_remaining = days until target deadline
# priority = user's manually assigned priority
#
PROJECTS = {
    "AI_FLUENCY": {
        "name": "AI Fluency Training",
        "status": "In Progress",
        "estimated_hours": 30,
        "completed_hours": 12,
        "days_remaining": 7,
        "priority": "HIGH",
    },

    "SMART_FARMING": {
        "name": "Smart Farming Assistant",
        "status": "In Progress",
        "estimated_hours": 45,
        "completed_hours": 25,
        "days_remaining": 18,
        "priority": "MEDIUM",
    },

    "COE_PORTAL": {
        "name": "COE Portal Improvements",
        "status": "Maintenance",
        "estimated_hours": 20,
        "completed_hours": 16,
        "days_remaining": 30,
        "priority": "LOW",
    },
}


QUESTIONS = [
    "What is the current status of the AI Fluency project?",

    "How many hours of work remain for the AI Fluency project?",

    "How many hours of work remain for Smart Farming Assistant and COE Portal Improvements in total?",

    "Write a two-line motivational message for someone working on their projects.",
]


# A challenge question that is deliberately outside the workflow's
# predefined rules.
CHALLENGE_QUESTION = (
    "I have only 6 hours available today. Based on my project data, "
    "which project should I work on and why?"
)


def banner(system_name):
    print(
        f"\n=== {system_name} | "
        f"provider: {PROVIDER} | model: {MODEL} ===\n"
    )