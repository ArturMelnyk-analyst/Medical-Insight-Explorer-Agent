# Refactor Notes

## Purpose

This document summarizes the helper-module refactor introduced to improve separation of responsibilities across the Medical Insight Explorer Agent.

The refactor keeps UI, orchestration, planning, analytics execution, response formatting, visualization, persona guidance, and analytical interpretation in clearly defined components.

---

## Why This Refactor Was Needed

After LangGraph orchestration was introduced, some helper logic existed in more than one place.

Duplicated responsibilities increase maintenance risk because future changes can update one execution path without updating another.

The refactor reduces this duplication and keeps each module focused on a specific responsibility.

---

## Updated Module Responsibilities

| Module | Responsibility |
|---|---|
| `app.py` | Gradio UI layout and event handling |
| `agent/graph_workflow.py` | LangGraph state workflow and orchestration |
| `agent/planner.py` | Builds bounded single-step and multi-step analytics plans |
| `agent/tool_registry.py` | Defines and executes approved deterministic analytics capabilities |
| `agent/language_utils.py` | Language normalization helpers |
| `agent/response_formatter.py` | English/German response formatting |
| `agent/chart_router.py` | Route-based Plotly chart generation |
| `agent/personas.py` | Defines stakeholder personas and recommended questions |
| `agent/insight_layer.py` | Provides cautious analytical interpretation for supported routes |
| `agent/analytics_engine.py` | Performs deterministic pandas-based healthcare analytics |

Persona guidance, analytical interpretation, planning, and approved tool execution remain separated from the Gradio application layer.

---

## Design Principle

The app should remain thin.

The graph should orchestrate.

The planner should select bounded analytical workflows.

The registry should constrain executable analytics capabilities.

Helper modules should format, normalize, interpret, or visualize.

Deterministic calculations should remain in `HealthcareAnalyticsEngine`.

Conceptually:

```text
Gradio UI
    ↓
LangGraph orchestration
    ↓
Controlled planning
    ↓
Approved tool registry
    ↓
Deterministic analytics
    ↓
Formatting / insight / visualization
```

---

## Separation of Responsibilities

The project maintains clear boundaries between:

- UI logic
- orchestration logic
- bounded analytics planning
- approved tool execution
- response formatting
- language normalization
- chart routing
- visualization tools
- deterministic analytics
- persona guidance
- analytical insight generation

This separation allows orchestration and presentation behavior to evolve without moving healthcare calculations outside the deterministic analytics layer.

---

## Result

The refactored structure provides a clearer separation between application concerns and analytical computation.

The v1.2.0 architecture builds on this separation by adding bounded planning and a shared approved analytics registry while preserving the same core principle:

```text
Orchestration coordinates.
Planning selects.
The registry constrains.
The analytics engine computes.
```

Detailed system architecture is documented in [Architecture](architecture.md), while LangGraph planning and execution behavior is documented in [LangGraph Orchestration](langgraph_orchestration.md).