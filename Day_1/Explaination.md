# Day 1 — Chatbot vs. Workflow vs. Agent

This project compares three different approaches to answering fee-related
questions for an AI course catalog:

1. **System 1 — Chatbot** (`chatbot.py`): A plain LLM-based chatbot with no
   tools, backed by `openai/gpt-oss-120b` via Groq.
2. **System 2 — Rule-based Workflow** (`workflow.py`): A deterministic,
   no-LLM system driven by fixed rules.
3. **System 3 — AI Agent** (`agent.py`): An LLM agent that can call tools
   (`get_course_fee`, `calculator`) to reason step-by-step and produce an
   answer.

A helper module, `tools.py`, exposes the two functions used by the agent:
`get_course_fee(course_code)` and `calculator(expression)`.

`check_setup.py` verifies that the environment (Python version, provider,
model) is configured correctly and that the model can be called
successfully.

---

## Setup Verification

```
python3 check_setup.py
```

| Item | Value |
|---|---|
| Python version | 3.14.7 |
| Provider | groq |
| Model | openai/gpt-oss-120b |
| Result | SETUP OK |

---

## Tool Functions (`tools.py`)

```
get_course_fee('ai202')            -> 18000
calculator('(12000 + 18000) * 0.9') -> 27000.0
calculator('15000 - 12000')         -> 3000
```

---

## System 1: Chatbot (`chatbot.py`)

A free-form conversational LLM with **no tools and no access to real fee
data**. It answers purely from language generation.

**Behavior observed:**
- Could not answer "What is the fee for AI202?" — it did not know the
  actual value and instead asked clarifying questions (institution,
  student status, term).
- Could not compute the total fee for CS101 and AI202, since it did not
  have the base fee values and had to ask the user to supply them.
- Could not compare DS303 and CS101 fees for the same reason.
- Did handle the open-ended "welcome message" question well, since that
  doesn't require factual/tool data.

---

## System 2: Rule-Based Workflow (`workflow.py`)

A deterministic system with **hard-coded rules and no LLM calls**.

```
Q: What is the fee for AI202?
A: Fee for AI202: Rs. 18,000

Q: What is the total fee for CS101 and AI202 after a 10% scholarship?
A: Total fee: Rs. 27,000

Q: Is DS303 more expensive than CS101, and by how much?
A: Sorry, I do not have a rule for this type of question.

Q: Write a two-line welcome message for new AI students.
(no rule exists — not handled)
```

**Behavior observed:**
- Correct and instant for the two questions it had rules for.
- Failed completely on any question outside its predefined rule set
  (the comparison question and the open-ended welcome message).

---

## System 3: AI Agent (`agent.py`)

An LLM agent (same model as the chatbot) that can call the `get_course_fee`
and `calculator` tools and chain multiple steps together.

```
Q: What is the fee for AI202?
  step 1: get_course_fee({'course_code': 'AI202'}) -> 18000
A: The fee for AI202 is ₹18,000.

Q: What is the total fee for CS101 and AI202 after a 10% scholarship?
  step 1: get_course_fee({'course_code': 'CS101'}) -> 12000
  step 2: get_course_fee({'course_code': 'AI202'}) -> 18000
  step 3: calculator({'expression': '30000*0.9'}) -> 27000.0
A: The total fee after applying the 10% scholarship is ₹27,000.

Q: Is DS303 more expensive than CS101, and by how much?
  step 1: get_course_fee({'course_code': 'DS303'}) -> 15000
  step 2: get_course_fee({'course_code': 'CS101'}) -> 12000
  step 3: calculator({'expression': '15000-12000'}) -> 3000
A: Yes, DS303 is more expensive than CS101 by ₹3,000.

Q: Write a two-line welcome message for new AI students.
A: Welcome to the exciting world of AI — where curiosity meets innovation!
   Get ready to explore, create, and shape the future with cutting-edge technology.
```

**Behavior observed:**
- Correctly answered all fee lookup and comparison questions by
  autonomously choosing and chaining the right tools.
- Also handled the open-ended welcome-message question well, since it can
  still fall back on plain language generation when no tool is needed.

### Agent Trace (example: total fee for CS101 + AI202 after 10% scholarship)

| Step | Tool called and arguments | Result (observation) |
|---|---|---|
| 1 | `get_course_fee(course_code="CS101")` | 12000 |
| 2 | `get_course_fee(course_code="AI202")` | 18000 |
| 3 | `calculator(expression="(12000 + 18000) * 0.9")` | 27000.0 |
| 4 | — | Final answer: ₹27,000 |

---

## Observation Table

| Criterion | Chatbot | Workflow | Agent |
|---|---|---|---|
| Q1 correct? (Y/N) | N | Y | Y |
| Q2 correct? (Y/N) | N | Y | Y |
| Q3 correct? (Y/N) | N | N | Y |
| Q4 handled well? (Y/N) | Y | N | Y |
| Challenge question handled? (Y/N) | N/A | N | Y |
| Same output on a repeat run? (Y/N) | N | Y | N |
| Approximate response time | ~1–2 sec | <0.1 sec | ~2–4 sec |
| Number of LLM calls per question | 1 | 0 | 1–2 |
| One strength | Natural language generation | Deterministic and reliable | Flexible tool-based reasoning |
| One weakness | Can hallucinate private data | Rigid rules | Less predictable / more complex |
| Best suited for (one real use case) | General conversational assistant | Fixed fee / transaction lookup | Complex tasks requiring tools |

---

## Discussion Questions

**1. The chatbot gave a confident but wrong fee. Why is that more
dangerous than replying "I don't know"?**

A confident wrong answer can mislead users because they may trust it and
make decisions based on incorrect information. "I don't know" clearly
communicates uncertainty and allows the user to verify the information.

**2. The workflow was always correct for questions 1 and 2. Why might a
finance office still prefer it over the agent?**

A rule-based workflow is deterministic, predictable, easy to audit, and
produces the same result for the same input. Financial systems often
prioritize reliability and traceability over flexibility.

**3. The agent's steps can change between runs. What problems would that
cause in a real product?**

Changing steps can make the system less predictable and harder to test,
debug, audit, and reproduce. An agent might also select a different tool
or make unnecessary tool calls.

**4. Design a system that uses a workflow for common questions and an
agent for the rest. Where would you draw the line?**

Use predefined workflows for known, repetitive, high-confidence
operations, such as fee lookup, payment status, and standard account
information. Use an agent when the request requires multiple tools,
reasoning, or flexible interpretation.

---

## Conclusion

| System | Summary |
|---|---|
| **Chatbot** | Fast and natural, but unreliable for factual/numeric answers since it has no access to real data — prone to hallucination. |
| **Workflow** | Fast, deterministic, and fully reliable — but rigid, and unable to handle any question outside its fixed rule set. |
| **Agent** | Slower and less deterministic, but the most capable — able to combine tools and reasoning to correctly handle both structured and open-ended questions. |

The right choice depends on the use case: workflows for well-defined,
repetitive, high-stakes operations; agents for flexible, multi-step tasks;
and plain chatbots for open-ended conversational tasks that don't need
grounded, factual data.