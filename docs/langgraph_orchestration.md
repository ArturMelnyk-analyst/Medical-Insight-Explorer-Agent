# LangGraph Orchestration

## Purpose

This document describes the controlled LangGraph orchestration used by **Medical Insight Explorer Agent v1.2.0**.

LangGraph coordinates the analytical workflow around deterministic healthcare analytics.

Its responsibility is to manage:

- language-aware question normalization
- bounded analytical planning
- approved-tool execution
- multi-step graph state
- deterministic result collection
- response synthesis
- primary chart generation

The central orchestration boundary is:

```text
LangGraph coordinates.
The planner selects.
The registry constrains.
The analytics engine computes.
```

LangGraph does not receive unrestricted dataframe access and does not replace the deterministic analytics engine.

For the complete system architecture, see [Architecture](architecture.md).

---

## Orchestration Overview

The original workflow followed a single-route sequence:

```text
Question
   ↓
Normalize
   ↓
Route
   ↓
Run analytics
   ↓
Generate response
   ↓
Generate chart
```

Version **v1.2.0** extends this into bounded multi-step orchestration:

```text
User question
        ↓
normalize_question
        ↓
plan_analytics
        ↓
validate approved plan
        ↓
execute analytical step
        ↓
store deterministic result
        ↓
advance execution state
        ↓
more planned tools?
     /            \
   yes             no
    ↓               ↓
execute next    generate_response
approved tool        ↓
                  generate_chart
                       ↓
                    output
```

The execution cycle is bounded by a validated plan.

It is not an open-ended autonomous agent loop.

---

## Main Components

The orchestration path uses the following modules:

| Component | File | Role |
|---|---|---|
| Graph workflow | `agent/graph_workflow.py` | Coordinates graph state and execution |
| Planner | `agent/planner.py` | Creates bounded analytical plans |
| Tool registry | `agent/tool_registry.py` | Validates and executes approved analytics |
| Language utilities | `agent/language_utils.py` | Normalizes supported English/German questions |
| Analytics engine | `agent/analytics_engine.py` | Performs deterministic calculations |
| Insight layer | `agent/insight_layer.py` | Interprets computed results cautiously |
| Response formatter | `agent/response_formatter.py` | Formats single-step and multi-step responses |
| Chart router | `agent/chart_router.py` | Selects the primary visualization |

The Gradio application invokes the workflow from:

```text
app.py
```

---

## Planning

The planner is implemented in:

```text
agent/planner.py
```

It converts a supported normalized question into a list of approved symbolic analytics tools.

The planner follows two rules:

```text
Use one tool when one tool is sufficient.

Use multiple tools only for explicitly supported
compound analytical questions.
```

For example:

```text
Show top inpatient providers
        ↓
[
    "top_inpatient_providers"
]
```

while:

```text
Compare inpatient and outpatient provider activity
        ↓
[
    "top_inpatient_providers",
    "top_outpatient_providers"
]
```

The planner does not generate Python, SQL, pandas expressions, or arbitrary dataframe operations.

---

## Execution Bound

The planner is constrained by:

```text
MAX_ANALYTICS_STEPS = 3
```

Therefore:

```text
0 tools → unsupported or rejected request
1 tool  → single-step workflow
2 tools → supported compound workflow
3 tools → maximum permitted plan
>3      → rejected
```

This bound prevents unrestricted iterative analytics.

The graph executes only the validated plan; intermediate results do not cause it to invent additional analytical steps.

---

## Supported Compound Workflows

Version v1.2.0 supports three explicit multi-step analytical patterns.

| Question | Plan |
|---|---|
| Compare inpatient and outpatient provider activity | `top_inpatient_providers` → `top_outpatient_providers` |
| Compare inpatient and outpatient claims by state | `inpatient_claims_by_state` → `outpatient_claims_by_state` |
| Compare inpatient and outpatient claim summaries | `inpatient_summary` → `outpatient_summary` |

Equivalent supported German questions normalize into the same language-independent plans.

Additional compound workflows require explicit implementation rather than automatic generation.

---

## Registry Boundary

Every planned tool must be approved by:

```text
agent/tool_registry.py
```

The orchestration flow is therefore:

```text
Planner
   ↓
symbolic tool name
   ↓
Registry validation
   ↓
approved?
  /      \
yes       no
 ↓         ↓
execute   reject
 ↓
deterministic analytics
```

The registry is the controller-facing capability boundary.

It prevents LangGraph from dynamically selecting arbitrary methods from `HealthcareAnalyticsEngine`.

Approved execution follows:

```text
approved tool name
        ↓
registry entry
        ↓
fixed analytics-engine method
        ↓
controlled parameters
        ↓
deterministic result
```

The complete registry and analytics architecture are documented in [Architecture](architecture.md) and [Analytics Engine](analytics_engine.md).

---

## Graph State

LangGraph uses shared state to carry the analytical workflow between nodes.

The multi-step implementation adds four important execution concepts:

```text
analysis_plan
current_step
tool_results
steps_completed
```

### `analysis_plan`

Stores the approved tools selected for the request.

Example:

```python
[
    "top_inpatient_providers",
    "top_outpatient_providers",
]
```

It contains symbolic tool names rather than executable instructions.

### `current_step`

Tracks the current position in the plan.

```text
0 → first analytical tool
1 → second analytical tool
2 → third analytical tool
```

### `tool_results`

Stores deterministic outputs from completed analytical steps.

Conceptually:

```text
tool_results
├── top_inpatient_providers
│       └── deterministic result
│
└── top_outpatient_providers
        └── deterministic result
```

Retaining these outputs allows the response layer to synthesize all executed results after the plan completes.

### `steps_completed`

Tracks how many approved analytical operations have executed.

It supports both execution control and user-visible workflow status.

---

## Primary-Result Compatibility

The graph also preserves the existing primary route/result concept used by downstream single-step and chart behavior.

Conceptually:

```text
analysis_plan
    ↓
primary tool
    ↓
route
    ↓
computed_result
```

while:

```text
tool_results
=
all executed analytical results
```

This distinction allows v1.2.0 to add multi-result orchestration without replacing the established chart architecture.

For a multi-step workflow:

```text
all tool results
        ↓
text synthesis

primary result
        ↓
chart routing
```

This is why compound workflows can include all analytical results in text while rendering one primary visualization.

---

## Sequential Execution

A multi-step plan executes one approved tool at a time.

For example:

```text
analysis_plan =
[
    top_inpatient_providers,
    top_outpatient_providers
]
```

The graph progresses as follows:

```text
current_step = 0
        ↓
execute top_inpatient_providers
        ↓
store result
        ↓
steps_completed = 1
        ↓
advance current_step
        ↓
execute top_outpatient_providers
        ↓
store result
        ↓
steps_completed = 2
        ↓
plan complete
        ↓
response synthesis
```

The graph does not dynamically expand the plan based on intermediate analytical results.

Execution ends when the validated plan is complete.

---

## Single-Step Compatibility

Existing supported questions continue to work as one-tool plans.

```text
single-step question
        ↓
normalization
        ↓
one approved tool
        ↓
deterministic result
        ↓
existing response behavior
        ↓
existing chart behavior
```

The planner can reuse the existing controlled routing logic for these questions.

Multi-step orchestration therefore extends rather than replaces the original single-step workflow.

---

## Multilingual Planning

Language normalization occurs before planning.

```text
English ─────┐
             │
German ──────┤
             ↓
     normalization
             ↓
         planner
             ↓
 language-independent
    analytical plan
```

For example, supported English and German provider-comparison questions can resolve to the same plan:

```python
[
    "top_inpatient_providers",
    "top_outpatient_providers",
]
```

The analytics engine remains language-independent.

Language affects question normalization and response presentation, not numerical formulas.

---

## Causal Safety Before Planning

The normalization layer preserves safety-relevant causal intent so it can be evaluated before compound analytical matching.

The ordering is:

```text
Question
        ↓
normalize while preserving causal intent
        ↓
causal safety evaluation
        ↓
       causal?
      /       \
    yes        no
     ↓          ↓
reject       continue
analytics    planning
     ↓
zero-tool plan
```

This prevents a causal healthcare question from being simplified into an apparently safe descriptive comparison.

For example, a question asking whether one condition **causes** higher reimbursement should not be transformed into an ordinary reimbursement comparison.

Detailed healthcare scope and safety limitations are documented in [Limitations](limitations.md).

---

## Unsupported Requests

The planner can return no approved analytical steps.

```text
unsupported request
        ↓
planner
        ↓
zero approved tools
        ↓
no analytics execution
        ↓
controlled fallback response
```

This is preferable to forcing an unsupported question into the nearest available analytics route.

The same zero-tool behavior can be used for requests rejected by safety controls.

---

## Multi-Result Handoff

After execution completes, stored results are passed into the response stage.

```text
tool_results
    │
    ├── result 1
    ├── result 2
    └── result 3
          ↓
response generation
          ↓
combined analytical output
```

The response formatter can therefore include every analytical result actually produced by the plan.

For multi-step workflows, the response can present:

```text
Summary
Analytical workflow
Analytical steps
Analytical insight
Computed results
Method note
Safety note
```

Only executed analytical operations are reported.

The workflow does not expose private chain-of-thought.

---

## Insight and Response Nodes

After deterministic execution, the workflow uses:

```text
agent/insight_layer.py
agent/response_formatter.py
```

The insight layer interprets already-computed results.

The response formatter converts the analytical outputs into readable English or German.

Neither component receives authority to create arbitrary new healthcare calculations.

Conceptually:

```text
deterministic tool results
        ↓
analytical insight
        ↓
response formatting
        ↓
user-facing text
```

This preserves the separation between computation and explanation.

---

## Chart Node

Chart generation remains controlled through:

```text
agent/chart_router.py
```

The chart node uses the primary route/result to select a supported Plotly visualization.

For multi-step workflows:

```text
tool_results
        ↓
all results → textual response

primary route/result
        ↓
chart router
        ↓
one primary chart
```

This is an intentional compatibility design for v1.2.0.

The graph does not dynamically generate arbitrary chart specifications from unrestricted natural-language instructions.

Detailed visualization behavior is documented in [Visualization Tools](visualization_tools.md).

---

## Workflow Visibility

Execution metadata can be surfaced by the Gradio interface.

Examples:

```text
Single-step · 1 approved tool executed
```

```text
Multi-step · 2 approved tools executed
```

A rejected or unsupported request can expose a zero-tool state.

This gives the user visibility into the analytical workflow without revealing hidden reasoning.

---

## Relationship to `ResponseGenerator`

The project intentionally retains a separate:

```text
agent/response_generator.py
```

execution path.

The distinction is:

```text
HealthcareGraphWorkflow
        ↓
LangGraph orchestration
bounded multi-step execution
multi-result state
deployed application workflow
```

versus:

```text
ResponseGenerator
        ↓
standalone controlled response path
registry-backed deterministic execution
optional LLM explanation architecture
```

Both paths share the approved tool registry.

The registry centralizes controller-facing capabilities without requiring the two execution paths to be collapsed into one implementation.

The optional LLM architecture is documented separately in [LLM Response Layer](llm_response_layer.md).

---

## Execution Safety

LangGraph operates inside explicit execution boundaries.

It cannot use the planner to perform unrestricted:

```text
Python
SQL
pandas
dataframe manipulation
analytics-engine method selection
unregistered tool execution
open-ended tool loops
```

The effective execution model is:

```text
supported question
        ↓
bounded symbolic plan
        ↓
registry validation
        ↓
predefined deterministic calculation
```

This keeps natural-language flexibility separate from numerical authority.

---

## Failure Behavior

The workflow fails in a controlled manner when execution boundaries are violated.

| Condition | Behavior |
|---|---|
| Unknown tool | Registry rejects execution |
| Unsupported question | Zero-tool plan / controlled fallback |
| Causal request | Analytics execution rejected |
| Plan exceeds maximum | Plan rejected |
| Empty plan | No analytics executed |
| Valid plan | Approved tools execute sequentially |

The workflow does not substitute arbitrary code when an approved analytical path is unavailable.

---

## Validation

The orchestration was validated across the main v1.2.0 behavior categories:

- single-step English/German execution
- supported multi-step English/German planning
- provider, state, and summary comparisons
- registry validation and unknown-tool rejection
- zero-tool unsupported behavior
- causal-request rejection
- maximum-step enforcement
- multi-result retention and synthesis
- workflow-status reporting
- one-primary-chart compatibility
- local LangGraph/Gradio execution

The planner regression suite passed all **9 configured English/German cases** during implementation.

Detailed release-level validation can be maintained separately from this architectural description.

---

## Current Constraints

The LangGraph implementation is intentionally bounded:

- only explicitly supported compound patterns produce multi-step plans
- plans contain no more than three approved analytics tools
- intermediate results do not trigger autonomous replanning
- arbitrary dataframe analytics cannot be generated
- causal healthcare inference is outside scope
- multi-step workflows currently retain one primary chart

For broader project limitations, see [Limitations](limitations.md).

---

## Orchestration Summary

The v1.2.0 LangGraph workflow can be summarized as:

```text
User question
        ↓
language-aware normalization
        ↓
bounded analytical planner
        ↓
0–3 approved symbolic tools
        ↓
registry validation
        ↓
sequential deterministic execution
        ↓
stored multi-tool results
        ↓
response + insight synthesis
        ↓
primary chart routing
        ↓
Gradio output
```

The key responsibilities remain deliberately separated:

```text
Planner          → selects
Registry         → constrains
Analytics engine → computes
LangGraph        → coordinates
Response layer   → presents
```

This provides meaningful multi-step orchestration without turning the application into an unrestricted autonomous healthcare-data agent.