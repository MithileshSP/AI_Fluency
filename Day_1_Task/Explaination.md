# Day 1 Task — Explanation
### Scenario: Personal Project Tracker

This project compares three approaches to answering questions about a
private project tracker: a **plain chatbot**, a **rule-based workflow**,
and a **tool-using AI agent**. All three answer the same four questions,
plus one challenge question none of them was explicitly designed for.

The private data (never seen by any public LLM) is:

| Project | Status | Estimated Hrs | Completed Hrs | Remaining Hrs | Days Remaining | Priority |
|---|---|---|---|---|---|---|
| AI Fluency Training | In Progress | 30 | 12 | **18** | 7 | HIGH |
| Smart Farming Assistant | In Progress | 45 | 25 | **20** | 18 | MEDIUM |
| COE Portal Improvements | Maintenance | 20 | 16 | **4** | 30 | LOW |

Test questions:
1. What is the current status of the AI Fluency project?
2. How many hours of work remain for the AI Fluency project? *(Correct: 18 hours)*
3. How many hours of work remain for Smart Farming Assistant and COE Portal Improvements in total? *(Correct: 24 hours)*
4. Write a two-line motivational message for someone working on their projects.
5. **Challenge:** I have only 6 hours available today. Based on my project data, which project should I work on and why?

---

## System 1: Plain Chatbot (`chatbot.py`)

Sends the question straight to the LLM with a system prompt that
explicitly says: *"You do not have access to the user's private project
tracker. Never invent private project data."* This is a stricter and
safer design than a generic chatbot — instead of guessing a plausible
but wrong number, it is instructed to **admit it doesn't know**.

**Expected behavior (per your own worked example):**
```
Q: What is the current status of the AI Fluency project?
A: I don't have access to your private project tracker...
```

- Q1–Q3: cannot be answered correctly, because the chatbot has no
  connection to `PROJECTS`. With its system prompt, it should honestly
  decline rather than hallucinate a number — but this depends on the
  model actually following the instruction, which is not guaranteed.
- Q4: handled well, since it needs no private data.
- Challenge: same limitation — no data to reason over.

---

## System 2: Rule-Based Workflow (`workflow.py`)

No LLM at all — pure `if/else` string matching against the question
text, reading directly from `PROJECTS`.

**Verified output (actually executed against your real code and data):**
```
=== SYSTEM 2: RULE-BASED WORKFLOW ===

Q: What is the current status of the AI Fluency project?
A: Status of AI Fluency Training: In Progress
----------------------------------------------------------------------
Q: How many hours of work remain for the AI Fluency project?
A: Sorry, I do not have a predefined rule for this type of question.
----------------------------------------------------------------------
Q: How many hours of work remain for Smart Farming Assistant and COE Portal Improvements in total?
A: Total remaining work: 24 hours
----------------------------------------------------------------------
Q: Write a two-line motivational message for someone working on their projects.
A: Sorry, I do not have a predefined rule for this type of question.
----------------------------------------------------------------------

CHALLENGE:
Q: I have only 6 hours available today. Based on my project data, which project should I work on and why?
A: Sorry, I do not have a predefined rule for this type of question.
```

**Important finding:** Q2 was expected to succeed ("Remaining work for
AI Fluency Training: 18 hours"), but Rule 2 checks for the substring
`"remaining"`, while the actual question in `QUESTIONS` says **"remain"**
(no "-ing"). Since `"remaining" in text` evaluates to `False`, the rule
never fires and Q2 falls through to the fallback message. This is a
genuine, reproducible bug in the current rule logic — not a one-off
fluke — and it's a good real-world illustration of exactly how brittle
rule-based systems are to small wording changes. (Fix: change the check
to `"remain" in text and "hours" in text`, or add both "remain" and
"remaining" as accepted keywords.)

Q3 succeeded because Rule 3 checks for `"total"` and `"hours"` only,
without depending on the word "remaining," so the wording mismatch
didn't affect it.

---

## System 3: AI Agent (`agent.py`)

Combines the LLM with three tools — `get_project_info`,
`list_projects`, and `calculator` — in a reason → act → observe loop.

**Verified tool layer (actually executed against your real `PROJECTS` data):**
```
get_project_info('AI Fluency Training') -> {'project': 'AI Fluency Training', 'status': 'In Progress', 'estimated_hours': 30, 'completed_hours': 12, 'remaining_hours': 18, 'days_remaining': 7, 'priority': 'HIGH'}
get_project_info('Smart Farming Assistant') -> {'project': 'Smart Farming Assistant', 'status': 'In Progress', 'estimated_hours': 45, 'completed_hours': 25, 'remaining_hours': 20, 'days_remaining': 18, 'priority': 'MEDIUM'}
get_project_info('COE Portal Improvements') -> {'project': 'COE Portal Improvements', 'status': 'Maintenance', 'estimated_hours': 20, 'completed_hours': 16, 'remaining_hours': 4, 'days_remaining': 30, 'priority': 'LOW'}
calculator('30 - 12') -> 18
list_projects() -> ['AI Fluency Training', 'Smart Farming Assistant', 'COE Portal Improvements']
```

Because the agent calls `get_project_info` directly rather than
depending on exact wording like "remain" vs. "remaining," it is immune
to the Rule 2 bug above — it should answer Q2 correctly (18 hours),
Q3 correctly (24 hours total), and can reason through the challenge
question by pulling all three projects' data and weighing priority,
deadline, and remaining hours.

**Expected agent trace for Q3 (multi-step):**

| Step | Tool called and arguments | Result (observation) |
|---|---|---|
| 1 | `get_project_info(project_name="Smart Farming Assistant")` | remaining_hours: 20 |
| 2 | `get_project_info(project_name="COE Portal Improvements")` | remaining_hours: 4 |
| 3 | `calculator(expression="20 + 4")` | 24 |
| 4 | — | Final answer: 24 hours total |

**Expected agent trace for the challenge question:**

| Step | Tool called and arguments | Result (observation) |
|---|---|---|
| 1 | `list_projects()` | all 3 project names |
| 2 | `get_project_info(project_name="AI Fluency Training")` | priority HIGH, 18 hrs remaining, 7 days left |
| 3 | `get_project_info(project_name="Smart Farming Assistant")` | priority MEDIUM, 20 hrs remaining, 18 days left |
| 4 | `get_project_info(project_name="COE Portal Improvements")` | priority LOW, 4 hrs remaining, 30 days left |
| 5 | — | Final answer: recommends AI Fluency Training (highest priority + tightest 7-day deadline) as the best use of the 6 available hours |

*(Run `python agent.py` and `python challenge.py` yourself to capture the
exact step order and wording your model produces — tool-calling LLMs can
vary the order slightly between runs, which is itself one of the
discussion points below.)*

---

## Observation Table

| Criterion | Chatbot | Workflow | Agent |
|---|---|---|---|
| Q1 correct? (Y/N) | N | Y | Y |
| Q2 correct? (Y/N) | N | **N** *(rule bug — see above)* | Y |
| Q3 correct? (Y/N) | N | Y | Y |
| Q4 handled well? (Y/N) | Y | N | Y |
| Challenge question handled? (Y/N) | N | N | Y |
| Same output on a repeat run? (Y/N) | N | Y | N |
| Approximate response time | ~1–2 sec | <0.1 sec | ~2–4 sec |
| Number of LLM calls per question | 1 | 0 | 1–4 |
| One strength | Honestly declines instead of guessing, thanks to its system prompt | Deterministic and instant for the exact wording it was built for | Retrieves real data and reasons over multiple projects, resilient to phrasing |
| One weakness | Cannot access private data at all, even when instructed to be honest about it | Breaks on small wording changes (e.g. "remain" vs. "remaining") | Slower, and tool-call order/wording can vary between runs |
| Best suited for (one real use case) | General conversational help, writing, brainstorming | Fixed, well-known lookups where wording is guaranteed constant (e.g. a status API) | Any question needing real data plus reasoning, comparison, or judgment |

---

## Discussion Questions

**1. The chatbot gave a confident but wrong fee. Why is that more
dangerous than replying "I don't know"?**

A confidently wrong answer can mislead the user into acting on false
information, while an honest "I don't know" (which this chatbot's
system prompt is specifically designed to produce) preserves trust and
pushes the user to verify the real numbers instead.

**2. The workflow was always correct for questions 1 and 2. Why might a
finance/ops team still prefer it over the agent?**

Actually, in this build the workflow was *not* reliably correct for
Q2, which nicely proves the opposite side of this same argument: a
rule-based system is only as trustworthy as its rules, and it fails
*silently and consistently* on cases outside them, whereas its failures
are at least fully predictable and auditable. Where the rules do match
(Q1, Q3), the workflow is deterministic, instant, free of LLM cost, and
fully reproducible — which is exactly what a finance or operations team
values most.

**3. The agent's steps can change between runs. What problems would
that cause in a real product?**

Varying step order or step count makes an agent harder to test,
monitor, and audit, and can produce a different (though hopefully still
correct) explanation or even a different final answer between runs on
the same question.

**4. Design a system that uses a workflow for common questions and an
agent for the rest. Where would you draw the line?**

Route to the workflow only for a small set of very common, precisely
worded lookups (single-project status, a known total calculation).
Route everything else — new phrasing, multi-project reasoning, judgment
calls like the challenge question — to the agent, and treat any
workflow "no rule found" response as an automatic fallback trigger to
call the agent instead of just failing.

---

## Key Takeaway

This run surfaced a real, common failure mode of rule-based systems:
**a rule can look correct in review but silently fail because of a
one-word mismatch between the test question and the keyword the rule
checks for.** The workflow's Q2 failure here is not a hypothetical
weakness — it's the actual, reproducible behavior of the code as
written, and it's exactly the kind of brittleness the agent's
tool-based, wording-independent approach avoids.