# Day 2 Lab --- Explanation and Observations

## 1. Lab Overview

This document records the work for the **Day 2 Lab Manual: "Tracing
ReAct on Paper, and Comparing Answers With and Without
Chain-of-Thought."**

The lab covers two related ideas from Unit 1:

1.  **Chain-of-Thought (CoT) prompting** --- asking the model to work
    through a problem step by step.
2.  **ReAct** --- combining reasoning with tool calls using a Thought →
    Action → Observation cycle.

The official lab manual asks us to trace a ReAct run on paper, compare
that trace with a real agent trace, compare answers with and without
Chain-of-Thought, and apply self-consistency by running a reasoning
question several times.

### Repository structure used for this project

The lab manual originally describes placing the three new programs
inside the existing Day 1 folder so that they can reuse `config.py`,
`tools.py`, and `agent.py` without creating another virtual environment.

For this repository, the files are organized separately under `Day_2/`,
while the ReAct program imports the existing Day 1 implementation from
`Day_1_Task/`. The project uses the single root `.venv` rather than
creating a new environment for Day 2.

``` text
Python_AI/
├── .venv/
├── .env
├── requirements.txt
├── Day_1_Task/
│   ├── config.py
│   ├── tools.py
│   ├── agent.py
│   └── ...
└── Day_2/
    ├── cot_compare.py
    ├── self_consistency.py
    ├── react_trace.py
    └── explanation.md
```

------------------------------------------------------------------------

## 2. Part A --- ReAct Paper Trace

### Problem given by the lab manual

The original Day 2 lab uses the same course-fee data from Day 1:

-   CS101 = Rs. 12,000
-   AI202 = Rs. 18,000
-   DS303 = Rs. 15,000

The question is:

> Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three
> courses with a 25% scholarship? And by how much?

The known correct calculation is:

``` text
Option 1:
(12,000 + 18,000) × 0.90
= 30,000 × 0.90
= Rs. 27,000

Option 2:
(12,000 + 18,000 + 15,000) × 0.75
= 45,000 × 0.75
= Rs. 33,750

Difference:
33,750 - 27,000
= Rs. 6,750
```

Therefore, the first option is cheaper by **Rs. 6,750**.

### Tools available to the agent

The lab specifies two tools:

-   `get_course_fee(course_code)`
-   `calculator(expression)`

The important rule is that the agent should not assume the private fee
values. It must obtain them through the fee lookup tool and use the
calculator for arithmetic.

### Paper trace

A valid trace can be represented as follows:

  ------------------------------------------------------------------------------------------------------
  Step              Type              Content                                          Purpose
  ----------------- ----------------- ------------------------------------------------ -----------------
  1                 Thought           I need the prices of all three courses before    Identify missing
                                      comparing the two options.                       information

  2                 Action            `get_course_fee("CS101")`                        Retrieve CS101
                                                                                       fee

  3                 Observation       `12000`                                          Store retrieved
                                                                                       fee

  4                 Thought           I need the AI202 fee.                            Continue
                                                                                       gathering
                                                                                       required data

  5                 Action            `get_course_fee("AI202")`                        Retrieve AI202
                                                                                       fee

  6                 Observation       `18000`                                          Store retrieved
                                                                                       fee

  7                 Thought           I need the DS303 fee because the second option   Continue
                                      includes all three courses.                      gathering data

  8                 Action            `get_course_fee("DS303")`                        Retrieve DS303
                                                                                       fee

  9                 Observation       `15000`                                          Store retrieved
                                                                                       fee

  10                Thought           Now calculate the discounted cost of the first   Begin calculation
                                      option.                                          

  11                Action            `calculator("(12000 + 18000) * 0.9")`            Calculate option
                                                                                       1

  12                Observation       `27000`                                          Option 1 result

  13                Thought           Now calculate the discounted cost of the second  Continue
                                      option.                                          comparison

  14                Action            `calculator("(12000 + 18000 + 15000) * 0.75")`   Calculate option
                                                                                       2

  15                Observation       `33750`                                          Option 2 result

  16                Thought           Compare the two totals and calculate the         Determine cheaper
                                      difference.                                      option

  17                Action            `calculator("33750 - 27000")`                    Calculate
                                                                                       difference

  18                Observation       `6750`                                           Difference

  19                Final Answer      The first option is cheaper by Rs. 6,750.        Complete the task
  ------------------------------------------------------------------------------------------------------

The exact real agent trace does not have to use the same number or order
of steps. The lab specifically asks for a comparison between the paper
trace and the machine-generated trace.

### Questions below the paper trace

**How many tool calls are needed?**

A complete trace normally needs three fee lookups and multiple
calculator calls. The exact number can vary depending on how the agent
performs the arithmetic.

**How many LLM calls would that be in real life?**

In the implementation used here, each reasoning cycle corresponds to an
LLM call. The exact number depends on whether multiple tools are
requested in one response and whether another reasoning step is required
afterward.

**Could any two actions happen in parallel?**

Yes. The three independent fee lookups do not depend on one another, so
a tool-calling implementation could request them in parallel. The
calculator calls cannot begin until their required fee observations are
available.

------------------------------------------------------------------------

## 3. Part B --- Real ReAct Agent Trace

The program `react_trace.py` runs the real agent and prints the tool
calls and observations.

The purpose is not to force the machine to reproduce the paper trace
exactly. Instead, the purpose is to compare:

-   which tools were called,
-   the order of the calls,
-   the number of reasoning steps,
-   whether independent calls were performed together,
-   and whether the final answer is correct.

### Actual observation record

Fill the following table from the terminal output produced by:

``` bash
python Day_2/react_trace.py
```

  Item                                        Paper trace               Actual agent
  ------------------------------- ----------------------- --------------------------
  Number of fee lookups                                 3   **Record actual result**
  Number of calculator calls                            3   **Record actual result**
  Total steps                       **Record your trace**   **Record actual result**
  Any tools called in parallel?                   **Y/N**                    **Y/N**
  Final answer                                  Rs. 6,750   **Record actual answer**
  Correct?                                              Y                    **Y/N**

If the agent reaches the wrong answer, the important observation is the
first incorrect or missing tool result. That identifies where the
reasoning process broke.

------------------------------------------------------------------------

## 4. Part C --- Direct Prompting vs Chain-of-Thought

The lab uses three reasoning-only questions. These questions contain all
the information required to solve them, so no tools are necessary.

### Question 1 --- Instalments

> A student takes three courses costing Rs. 12,000, Rs. 18,000 and Rs.
> 15,000. She gets a 15% scholarship on the total and pays the rest in 4
> equal instalments. How much is each instalment?

Correct calculation:

``` text
Total = 12,000 + 18,000 + 15,000
      = 45,000

Scholarship = 15% of 45,000
            = 6,750

Payable = 45,000 - 6,750
        = 38,250

Each instalment = 38,250 / 4
                = Rs. 9,562.50
```

### Question 2 --- Lab sittings

> A lab has 18 computers. In the morning each computer is shared by 2
> students, and in the afternoon by 3 students. How many student
> sittings happen in one day?

Correct calculation:

``` text
Morning = 18 × 2 = 36
Afternoon = 18 × 3 = 54
Total = 36 + 54 = 90
```

Correct answer: **90 student sittings**.

### Question 3 --- Ordering

> Ravi is taller than Kumar. Kumar is taller than Arun. Priya is shorter
> than Arun. Who is the tallest and who is the shortest?

The ordering is:

``` text
Ravi > Kumar > Arun > Priya
```

Correct answer:

-   Tallest: **Ravi**
-   Shortest: **Priya**

------------------------------------------------------------------------

## 5. Direct Prompting

The direct prompt asks the model to provide only the final answer
without explanation.

Conceptually:

``` text
User question
     ↓
LLM
     ↓
Final answer
```

There is no visible reasoning trace and no tool call.

This approach is appropriate for simple questions where the answer is
straightforward and the model already has all required information.

### Observation table

Record the results from `cot_compare.py`:

  ------------------------------------------------------------------------
  Question           Without CoT       With CoT correct? Which reply was
                     correct?                            longer?
  ------------------ ----------------- ----------------- -----------------
  Q1 --- Instalments **Record actual** **Record actual** **Record actual**

  Q2 --- Lab         **Record actual** **Record actual** **Record actual**
  sittings                                               

  Q3 ---             **Record actual** **Record actual** **Record actual**
  Tallest/shortest                                       
  ------------------------------------------------------------------------

The official manual provides an example where the direct response to Q1
can incorrectly give Rs. 11,250 by missing the scholarship, while the
CoT response reaches Rs. 9,562.50. This is a sample result, not an
observation that should automatically be copied into our experiment.

------------------------------------------------------------------------

## 6. Chain-of-Thought Prompting

The CoT prompt explicitly asks the model to solve the problem step by
step and end with:

``` text
Final Answer: <answer>
```

Conceptually:

``` text
User question
     ↓
LLM
     ↓
Step 1
     ↓
Step 2
     ↓
...
     ↓
Final Answer
```

The important limitation is that CoT does **not** provide new
information. If the question requires private data that is not in the
prompt, asking the model to reason step by step does not give it access
to that data.

For example:

``` text
"What is the private fee for AI202?"
```

A CoT prompt can make the model explain its reasoning, but it cannot
retrieve the actual private fee unless a tool or another data source is
connected.

------------------------------------------------------------------------

## 7. Part D --- Self-Consistency

The `self_consistency.py` program runs the same CoT problem five times
using a non-zero temperature.

Current configuration:

``` text
RUNS = 5
TEMPERATURE = 0.8
```

The purpose is to allow different reasoning paths and then choose the
answer that appears most often.

### Observation table

  Item                           Actual observation
  ------------------------------ --------------------------------
  Answers seen across 5 runs     **Record actual five answers**
  Majority answer                **Record actual**
  Majority count                 **Record actual**
  Was majority answer correct?   **Y/N**
  Result when temperature = 0    **Record actual**

The lab manual uses five runs because five is an odd number, which
avoids a simple tie, and uses temperature 0.8 so that repeated runs have
an opportunity to differ.

At temperature 0, repeated answers are expected to become much more
similar, so voting provides little additional value.

------------------------------------------------------------------------

## 8. Discussion Questions

### 1. Does a different order of steps make the paper trace or agent trace wrong?

No. Different tool-call orders can still be valid if all required
information is obtained and the final result is correct. The order
becomes a problem only when a later action depends on information that
has not yet been obtained.

### 2. If the model already had the ability to solve a problem, why did it improve when asked to think step by step?

A direct prompt does not explicitly allocate output space or structure
for intermediate calculations. A CoT prompt encourages the model to
externalize intermediate steps, which can reduce mistakes on multi-step
problems. This does not guarantee correctness.

### 3. Why can Chain-of-Thought not answer a private fee question correctly?

The missing component is **external information access**. CoT changes
the reasoning process but does not add a tool. The ReAct pattern
supplies the missing capability by allowing the agent to call a tool and
observe its result.

### 4. Why does self-consistency use non-zero temperature while Day 1 tool calling used temperature 0?

Self-consistency needs variation between reasoning attempts so that
different possible paths can be sampled. Tool-calling experiments often
use temperature 0 to make behavior more deterministic and easier to
reproduce and debug.

### 5. How would Plan-and-Execute handle the fee comparison?

Plan-and-Execute would first create a plan for the task and then execute
the planned actions. The exact number of LLM calls depends on the
implementation. Unlike the reactive loop, the plan is created before
execution rather than being rebuilt after every observation.

### 6. What are the three row types in a ReAct trace?

-   **Thought:** identifies what the agent needs to do next.
-   **Action:** specifies a tool call.
-   **Observation:** contains the result returned by the tool.

### 7. Why can a Thought not change the outside world?

A Thought is only a reasoning step. External state changes or
information retrieval happen through an Action/tool call.

### 8. What is the difference between Chain-of-Thought and ReAct?

Chain-of-Thought focuses on step-by-step reasoning. ReAct combines
reasoning with actions and observations, allowing the system to obtain
external information or perform operations during the reasoning loop.

### 9. Why does self-consistency need temperature above 0?

With temperature 0, repeated calls are intended to be highly
deterministic. Self-consistency needs multiple different candidate
reasoning paths so that a majority can be selected.

### 10. Why is voting performed on the final answer?

The reasoning text can differ in wording even when the answer is the
same. Comparing the final answer makes the voting process simpler and
focuses it on the actual result.

### 11. What does two tool calls under the same step number mean?

It means the model requested multiple tool calls in the same
response/reasoning step. Independent calls may be executed together or
handled as a batch by the program.

### 12. Give one advantage and one disadvantage of CoT.

**Advantage:** it can improve structured multi-step reasoning.

**Disadvantage:** it produces more tokens and therefore can increase
response time/cost, while still lacking access to facts that are not in
the prompt.

------------------------------------------------------------------------

## 9. Overall Result

The Day 2 lab demonstrates three important distinctions.

First, a ReAct agent can combine reasoning with external tools. Second,
Chain-of-Thought can improve the handling of multi-step reasoning
problems when all required information is already available. Third,
self-consistency can use multiple sampled reasoning attempts to reduce
dependence on a single reasoning path.

The final observations in this document should be updated with the
actual terminal results after running the three programs. The sample
outputs from the lab manual should not be presented as personal
experimental results.

------------------------------------------------------------------------

## 10. Commands Used

From the repository root:

``` bash
source .venv/bin/activate
```

Run the ReAct comparison:

``` bash
python Day_2/react_trace.py
```

Run the direct vs CoT comparison:

``` bash
python Day_2/cot_compare.py
```

Run self-consistency:

``` bash
python Day_2/self_consistency.py
```

------------------------------------------------------------------------

## 11. Key Learning

The main lesson from this lab is that **reasoning and information access
are different capabilities**.

Chain-of-Thought can help a model reason through information that it
already has, but it cannot retrieve private information by itself. ReAct
extends the process by allowing the model to decide when a tool is
needed, call the tool, observe its result, and continue reasoning.

The experiment also shows why actual traces matter. A theoretical ReAct
trace describes what should happen, while the terminal trace reveals
what the model actually did. Differences in tool order, number of calls,
or final output are useful observations rather than something to hide.
