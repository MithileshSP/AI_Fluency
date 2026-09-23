# Day 2 Task --- Explanation and Observations

## 1. Task Overview

This is the **Day 2 Task** continuation of the Personal Project Tracker
scenario developed for Day 1.

Day 1 compared:

-   a plain chatbot,
-   a rule-based workflow,
-   and a tool-using AI agent.

Day 2 keeps the same private-data scenario but changes the question
being studied. Instead of comparing system architectures, this task
compares three reasoning/acting approaches:

1.  **Direct Prompting**
2.  **Chain-of-Thought Prompting**
3.  **ReAct Agent**

This follows the Day 2 Task requirement to choose a scenario containing
both questions that require careful reasoning and at least one question
that requires external/private information through a tool.

------------------------------------------------------------------------

## 2. Scenario --- Personal Project Tracker

The scenario represents a small private project tracker. The information
below is private project data used by the programs.

  ---------------------------------------------------------------------------------------
  Project        Status          Estimated   Completed   Remaining        Days Priority
                                       Hrs         Hrs         Hrs   Remaining 
  -------------- ------------- ----------- ----------- ----------- ----------- ----------
  AI Fluency     In Progress            30          12          18           7 HIGH
  Training                                                                     

  Smart Farming  In Progress            45          25          20          18 MEDIUM
  Assistant                                                                    

  COE Portal     Maintenance            20          16           4          30 LOW
  Improvements                                                                 
  ---------------------------------------------------------------------------------------

The important point is that the private tracker data is stored in the
project's local code/tool layer. The ReAct agent can retrieve it through
tools, while Direct Prompting and Chain-of-Thought do not automatically
have access to it.

------------------------------------------------------------------------

## 3. Why Day 2 Continues Day 1

The two tasks form a logical progression.

### Day 1

The question was:

> How do different system architectures handle private project data?

The comparison was:

``` text
Chatbot
Workflow
Agent
```

### Day 2

The question becomes:

> How do different reasoning strategies handle the same type of problem,
> and when is tool access required?

The comparison is:

``` text
Direct Prompting
Chain-of-Thought
ReAct
```

Using the same scenario makes the comparison easier to understand
because the private data and project context remain constant.

------------------------------------------------------------------------

# 4. Questions Used in This Task

The questions were designed specifically for the Personal Project
Tracker.

## Question 1 --- Pure multi-step reasoning

``` text
I have 18 hours remaining on a project and 7 days left.
If I work for 2 hours per day for the first 5 days,
how many hours will remain for the final 2 days?
```

Correct calculation:

``` text
Initial remaining work = 18 hours

Work during first 5 days:
2 × 5 = 10 hours

Remaining:
18 - 10 = 8 hours
```

**Correct answer: 8 hours.**

This question does not require private-data retrieval because all
numbers are included in the question.

------------------------------------------------------------------------

## Question 2 --- Multi-step proportional reasoning

``` text
I have three projects requiring 18, 20, and 4 hours respectively.
If I can spend 6 hours today and want to divide my time
proportionally according to the remaining workload,
how many hours should I allocate to each project?
```

Total remaining work:

``` text
18 + 20 + 4 = 42 hours
```

Six hours are distributed proportionally.

### AI Fluency Training

``` text
18 / 42 × 6
= 2.5714 hours
```

### Smart Farming Assistant

``` text
20 / 42 × 6
= 2.8571 hours
```

### COE Portal Improvements

``` text
4 / 42 × 6
= 0.5714 hours
```

Rounded to two decimal places:

  Project                         Allocation
  ------------------------- ----------------
  AI Fluency Training             2.57 hours
  Smart Farming Assistant         2.86 hours
  COE Portal Improvements         0.57 hours
  **Total**                   **6.00 hours**

This question tests multi-step reasoning without requiring a tool.

------------------------------------------------------------------------

## Question 3 --- Private-data tool question

``` text
Which project should I prioritize today based on my private
project tracker? Consider remaining work, days remaining,
and priority.
```

This question is intentionally different.

The question does **not** provide the project information.

The system therefore needs access to the private tracker to answer it
reliably.

The relevant data is:

``` text
AI Fluency Training
18 hours remaining
7 days remaining
HIGH priority

Smart Farming Assistant
20 hours remaining
18 days remaining
MEDIUM priority

COE Portal Improvements
4 hours remaining
30 days remaining
LOW priority
```

The agent can retrieve these values using the project tools from Day 1
and then reason over the observations.

------------------------------------------------------------------------

# 5. Approach 1 --- Direct Prompting

Direct prompting sends the question directly to the LLM without a
visible reasoning instruction and without tool access.

Conceptually:

``` text
User question
     ↓
LLM
     ↓
Answer
```

For Questions 1 and 2, the model has all the necessary information
inside the prompt, so it can attempt the calculations.

For Question 3, the model does not have the private project tracker
values in the question. Therefore, direct prompting cannot reliably
retrieve the actual private data.

### Strength

It is simple, fast, and suitable for straightforward questions where the
required information is already available.

### Limitation in this scenario

It cannot access the private project tracker.

------------------------------------------------------------------------

# 6. Approach 2 --- Chain-of-Thought

Chain-of-Thought prompting explicitly asks the model to work through a
problem step by step before giving a final answer.

Conceptually:

``` text
User question
     ↓
Step-by-step reasoning
     ↓
Final answer
```

For Questions 1 and 2, this can help because both require multiple
calculations.

However, CoT does not create access to the private project tracker.

For Question 3, asking the model to reason step by step does not provide
the missing project data. The model would still lack the information
required to make a data-grounded answer.

### Strength

Useful for multi-step arithmetic and logical reasoning when the required
information is already available.

### Limitation in this scenario

It can reason about known information but cannot retrieve missing
private data without a tool.

------------------------------------------------------------------------

# 7. Approach 3 --- ReAct Agent

The ReAct agent combines reasoning with tools.

Its conceptual loop is:

``` text
Thought
   ↓
Action
   ↓
Observation
   ↓
Thought
   ↓
Action
   ↓
Observation
   ↓
Final Answer
```

For Question 3, the agent can call the tools from the Day 1 project.

A possible trace is:

  -----------------------------------------------------------------------------------------------
  Step                    Action                                          Observation
  ----------------------- ----------------------------------------------- -----------------------
  1                       `list_projects()`                               Three project names

  2                       `get_project_info("AI Fluency Training")`       18 hrs remaining, 7
                                                                          days, HIGH

  3                       `get_project_info("Smart Farming Assistant")`   20 hrs remaining, 18
                                                                          days, MEDIUM

  4                       `get_project_info("COE Portal Improvements")`   4 hrs remaining, 30
                                                                          days, LOW

  5                       Reason over observations                        Compare workload,
                                                                          deadline and priority

  6                       Final answer                                    State which project
                                                                          should be prioritized
                                                                          and why
  -----------------------------------------------------------------------------------------------

The exact order and number of calls must be taken from the actual
terminal output when the agent is run. The table above is a
planned/illustrative trace, not an actual experimental result.

------------------------------------------------------------------------

# 8. Direct vs CoT vs ReAct Comparison

The Day 2 Task requires comparison using reasoning depth, tool usage,
multi-step reliability, transparency, speed/cost, and repeated-run
consistency.

  --------------------------------------------------------------------------
  Basis             Direct Prompting    Chain-of-Thought   ReAct Agent
  ----------------- ------------------- ------------------ -----------------
  Reasoning depth   Limited visible     Explicit           Iterative
                    reasoning           step-by-step       reasoning with
                                        reasoning          observations

  Tool usage        None                None               Yes

  Reliability on    Depends on model    Can improve for    Can combine
  multi-step                            multi-step         reasoning with
  questions                             calculations       retrieved data

  Transparency      Final answer only   Reasoning steps    Tool calls and
                                        are requested in   observations can
                                        the prompt         be traced

  Speed / cost      Usually lowest      More tokens, so    Can be highest
                                        usually higher     because of
                                                           multiple
                                                           model/tool cycles

  Consistency       Depends on          Can vary when      Tool sequence and
                    temperature/model   sampling is        final wording can
                                        enabled            vary

  Private-data      No                  No                 Yes, through
  access                                                   tools
  --------------------------------------------------------------------------

These are the conceptual expectations. The final report should also
record the actual behavior observed from the programs.

------------------------------------------------------------------------

# 9. Self-Consistency Experiment

The Day 2 Task requires one Chain-of-Thought question to be run several
times at a non-zero temperature.

For this project, Question 2 is suitable because it requires multiple
calculations but does not require private-data retrieval.

Current experiment:

``` text
RUNS = 5
TEMPERATURE = 0.8
```

The program records the final answer from each run and selects the most
common answer.

### Observation table

Fill this table from the actual terminal output:

  Run   Answer
  ----- -------------------
  1     **Record actual**
  2     **Record actual**
  3     **Record actual**
  4     **Record actual**
  5     **Record actual**

Then record:

  Observation                        Result
  ---------------------------------- -------------------
  Majority answer                    **Record actual**
  Majority count                     **Record actual**
  Was the majority answer correct?   **Y/N**
  Result at temperature = 0          **Record actual**

At a non-zero temperature, the model may produce different wording or
reasoning paths. At temperature 0, repeated outputs are expected to
become much more deterministic.

------------------------------------------------------------------------

# 10. Expected Experimental Observations

The following are expectations to compare against actual execution; they
should not be presented as measured results until the programs have been
run.

### Direct Prompting

For Questions 1 and 2, the model has all required numerical information
in the question.

For Question 3, the model lacks the private project data unless that
information has somehow been supplied separately. Therefore, a reliable
answer requires another information source.

### Chain-of-Thought

For Questions 1 and 2, explicit intermediate calculations can make the
reasoning easier to follow and can reduce arithmetic mistakes.

For Question 3, CoT alone does not solve the missing-data problem.

### ReAct

For Question 3, the agent can retrieve the private project information
through the tools inherited from Day 1 and then reason over those
observations.

The main trade-off is that the ReAct approach can require multiple model
calls and tool calls, making it more complex and potentially slower.

------------------------------------------------------------------------

# 11. Suitability Analysis

There is no single approach that is appropriate for every question in
this scenario.

For a simple question such as:

``` text
What is 18 - (2 × 5)?
```

direct prompting is sufficient.

For a multi-step calculation such as the proportional allocation
question, Chain-of-Thought can be useful because it encourages the model
to work through the intermediate calculations.

For a question requiring the private project tracker:

``` text
Which project should I prioritize today based on my private tracker?
```

tool access becomes important. ReAct is appropriate because it can
retrieve the relevant private information and then reason over it.

Therefore, the important distinction is not simply that one approach is
universally better. The appropriate method depends on whether the
problem requires only a response, structured reasoning, or reasoning
combined with external/private information.

------------------------------------------------------------------------

# 12. General Conclusion

Direct prompting is suitable for simple questions where the required
information is already available and the task does not need substantial
reasoning or external data.

Chain-of-Thought is useful when a problem contains multiple reasoning
steps and all of the necessary information is already available to the
model. It can make intermediate calculations explicit and can help
reduce certain reasoning errors, although it increases the amount of
generated text and does not provide external information.

ReAct is useful when reasoning must be combined with external
information or actions. In the Personal Project Tracker scenario, the
ReAct agent can call project-information tools, observe the returned
private data, and continue reasoning before producing its answer.

The Day 2 Task therefore extends the Day 1 experiment: Day 1 showed why
an agent needs tools to work with private data, while Day 2 shows how
different reasoning strategies behave once the problem is considered
from the perspective of reasoning and acting.

------------------------------------------------------------------------

# 13. Commands Used

From the repository root:

``` bash
source .venv/bin/activate
```

Run Direct Prompting vs CoT:

``` bash
python Day_2_Task/cot_compare.py
```

Run Self-Consistency:

``` bash
python Day_2_Task/self_consistency.py
```

Run ReAct:

``` bash
python Day_2_Task/react_trace.py
```

------------------------------------------------------------------------

# 14. Final Observation Checklist

Before submitting, replace every **"Record actual"** field with
observations from your own terminal runs.

Check that the repository contains:

``` text
Day_2_Task/
├── cot_compare.py
├── self_consistency.py
├── react_trace.py
├── explanation.md
└── screenshots/
    ├── cot_compare.png
    ├── self_consistency.png
    └── react_trace.png
```

The screenshots should show the programs actually running on the
Personal Project Tracker scenario.

The analysis should distinguish clearly between:

-   expected behavior,
-   actual observed output,
-   and conclusions drawn from the experiment.
