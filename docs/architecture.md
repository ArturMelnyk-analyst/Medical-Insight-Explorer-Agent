# Architecture — Medical Insight Explorer Agent

## Purpose

Medical Insight Explorer Agent is a controlled bilingual healthcare claims analytics system built on cleaned Medicare data.

The project connects an upstream data-engineering pipeline with deterministic analytics, bounded analytical planning, LangGraph orchestration, response synthesis, visualization, and a Gradio interface.

The architecture follows four principles:

```text
Compute deterministically.
Select only approved analytics.
Keep orchestration bounded.
Do not make unsupported healthcare claims.
```

All numerical healthcare results originate from predefined pandas-based analytics functions.

Natural-language components can select and explain approved analytics, but they do not receive unrestricted access to healthcare dataframes.

---

## System Overview

Medical Insight Explorer Agent is downstream from the companion **Healthcare-Data-Cleaning** repository.

The architecture combines two related paths:

- a **data path**, which supplies cleaned and validated healthcare data to the deterministic analytics engine
- a **controlled analytical path**, which determines which approved analytics operation should be executed for a supported user question

### Data Path

```text
Raw healthcare CSV files
        ↓
Healthcare-Data-Cleaning
        ↓
Cleaned + validated Parquet tables
        ↓
HealthcareDataLoader
        ↓
HealthcareAnalyticsEngine
```

The upstream **Healthcare-Data-Cleaning** repository owns raw-data preparation, cleaning, and validation.

Medical Insight Explorer Agent begins from the validated Parquet outputs and uses them as the input boundary for deterministic downstream analytics.

### Controlled Analytical Path

```text
User question
        ↓
Bilingual Gradio interface
        ↓
Language normalization
        ↓
Controlled Analytics Planner
        ↓
Approved Analytics Tool Registry
        ↓
HealthcareAnalyticsEngine
        ↓
Deterministic analytical results
        ↓
Insight + Response Synthesis
        ↓
Primary Visualization
        ↓
Gradio output
```

The planner selects bounded analytical workflows using approved symbolic tool names.

The tool registry constrains controller-facing execution to approved deterministic analytics capabilities.

`HealthcareAnalyticsEngine` performs the numerical pandas-based calculations, while LangGraph coordinates planning, sequential execution, result collection, response synthesis, and chart generation around this controlled flow.

Together, these paths form four primary architectural layers:

```text
DATA ENGINEERING
        ↓
DETERMINISTIC ANALYTICS
        ↓
CONTROLLED ORCHESTRATION
        ↓
PRESENTATION
```

The separation keeps data preparation, numerical computation, analytical control, and user-facing presentation as distinct responsibilities.

---

## Architecture Diagrams

Architecture diagrams are stored in:

```text
images/architecture/
```

Current diagrams:

```text
data_pipeline_architecture.png
agent_workflow_architecture.png
```

### Data Pipeline

The data-pipeline diagram represents:

```text
Raw CSV data
        ↓
Healthcare-Data-Cleaning
        ↓
Validated Parquet outputs
        ↓
HealthcareDataLoader
        ↓
HealthcareAnalyticsEngine
```

It documents data provenance and the boundary between upstream data preparation and downstream analytics.

### Agent Workflow

The agent-workflow diagram represents:

```text
User question
        ↓
Language normalization
        ↓
Controlled planner
        ↓
Approved tool registry
        ↓
Bounded deterministic execution
        ↓
Stored analytical results
        ↓
Insight + response synthesis
        ↓
Primary visualization
        ↓
Gradio output
```

Detailed graph execution mechanics are documented in
[LangGraph Orchestration](langgraph_orchestration.md).

---

## Main Components

| Component | File | Responsibility |
|---|---|---|
| Data loader | `agent/data_loader.py` | Loads cleaned Parquet tables |
| Analytics engine | `agent/analytics_engine.py` | Computes deterministic healthcare metrics |
| Tool registry | `agent/tool_registry.py` | Defines controller-approved analytics capabilities |
| Analytics planner | `agent/planner.py` | Creates bounded plans using approved tool names |
| Language utilities | `agent/language_utils.py` | Normalizes supported bilingual analytical questions |
| Graph workflow | `agent/graph_workflow.py` | Coordinates planning, execution, synthesis, and chart generation |
| Insight layer | `agent/insight_layer.py` | Adds cautious interpretation to computed results |
| Response formatter | `agent/response_formatter.py` | Formats single-step and multi-step bilingual responses |
| Response generator | `agent/response_generator.py` | Provides the standalone controlled response path |
| Chart router | `agent/chart_router.py` | Selects the primary visualization |
| Visualization tools | `agent/visualization_tools.py` | Generates Plotly visualizations |
| Persona layer | `agent/personas.py` | Provides stakeholder-guided analytical prompts |
| Prompt templates | `agent/prompt_templates.py` | Supports optional controlled LLM explanation |
| Gradio interface | `app.py` | Provides the interactive application |

Each component has a narrow responsibility so that numerical computation, orchestration, interpretation, and presentation remain separated.

---

## Data Architecture

The full local workflow consumes cleaned Parquet files under:

```text
data/processed/
```

These outputs are generated by the upstream **Healthcare-Data-Cleaning** project.

Full processed datasets are excluded from GitHub.

For lightweight public deployment, the application can use:

```text
data/sample/
```

The data layer is independent from:

- interface language
- stakeholder persona
- analytical planning
- response formatting
- visualization

This allows the same analytics architecture to operate over the configured local or sample dataset.

For detailed input expectations, see [Data Contract](data_contract.md).

---

## Deterministic Analytics Layer

The numerical analytics layer is implemented in:

```text
agent/analytics_engine.py
```

It contains predefined pandas-based calculations for areas such as:

- table structure
- inpatient and outpatient summaries
- beneficiary age
- provider activity
- claims by state
- chronic-condition reimbursement comparison
- reimbursement distribution

The central computation boundary is:

```text
HealthcareAnalyticsEngine
=
source of numerical truth
```

The orchestration and response layers do not invent healthcare statistics.

The analytics engine can contain reusable internal functionality that is not directly available to controller logic.

Approved controller-facing access is defined separately by the tool registry.

For calculation details, see [Analytics Engine](analytics_engine.md).

---

## Approved Analytics Capability Layer

Approved controller-facing analytics are defined in:

```text
agent/tool_registry.py
```

The registry contains ten approved capabilities:

```text
table_shapes
inpatient_summary
outpatient_summary
age_summary
top_inpatient_providers
top_outpatient_providers
inpatient_claims_by_state
outpatient_claims_by_state
diabetes_cost_summary
reimbursement_distribution
```

The registry maps symbolic tool names to controlled deterministic analytics behavior.

It provides a shared capability boundary for the project's execution paths and prevents orchestration code from selecting arbitrary analytics-engine methods.

Conceptually:

```text
Natural-language intent
        ↓
approved symbolic tool
        ↓
Tool Registry
        ↓
fixed deterministic behavior
        ↓
HealthcareAnalyticsEngine
```

Unknown or unregistered tools are not executed.

---

## Controlled Planning Layer

The planner is implemented in:

```text
agent/planner.py
```

Its role is to convert supported normalized questions into plans containing approved symbolic tool names.

Simple questions use one tool when one tool is sufficient.

Supported compound questions can use multiple tools.

Execution is bounded by:

```text
MAX_ANALYTICS_STEPS = 3
```

The current release includes controlled compound workflows for:

- inpatient vs outpatient provider activity
- inpatient vs outpatient claims by state
- inpatient vs outpatient claim summaries

The planner does not construct arbitrary Python, SQL, pandas expressions, or dataframe operations.

Detailed planning, graph state, execution-loop, and rejection behavior are documented in [LangGraph Orchestration](langgraph_orchestration.md).

---

## LangGraph Orchestration Layer

The deployed Gradio application uses:

```text
HealthcareGraphWorkflow
```

implemented in:

```text
agent/graph_workflow.py
```

LangGraph coordinates the analytical lifecycle:

```text
normalize
        ↓
plan
        ↓
execute approved tools
        ↓
store results
        ↓
synthesize response
        ↓
generate primary chart
```

For multi-step questions, approved tools execute sequentially and their deterministic results are retained for combined response generation.

The execution loop is bounded by the validated analytical plan.

LangGraph coordinates execution; it does not replace the analytics engine.

The detailed graph state and node behavior belong in [LangGraph Orchestration](langgraph_orchestration.md).

---

## Two Intentional Execution Paths

The project retains two controlled execution paths.

### LangGraph Application Path

`HealthcareGraphWorkflow` supports the deployed application's orchestration lifecycle, including bounded multi-step execution.

```text
question
    ↓
normalization
    ↓
planning
    ↓
approved analytics
    ↓
result synthesis
    ↓
visualization
```

### Standalone Response Path

`ResponseGenerator` remains a separate controlled response component.

It uses the same approved analytics registry and preserves the project's optional LLM explanation architecture after deterministic computation.

The two paths have different responsibilities but share the same controller-facing capability definition.

This avoids maintaining separate definitions of which analytics operations are approved.

---

## Multilingual Architecture

English and German interaction is separated from numerical computation.

```text
English ─────┐
             │
German ──────┤
             ↓
     normalization
             ↓
         planner
             ↓
     approved tools
             ↓
 deterministic analytics
             ↓
    localized response
```

Supported German analytical questions normalize into the same language-independent tool representation used by English questions.

Safety-relevant causal intent is preserved during normalization so that unsupported causal requests can be rejected before analytics execution.

The analytics engine therefore does not require separate English and German implementations.

Detailed multilingual planning behavior is documented in [LangGraph Orchestration](langgraph_orchestration.md).

---

## Analytical Interpretation and Response

Deterministic results move through two user-facing analytical components:

```text
agent/insight_layer.py
agent/response_formatter.py
```

The insight layer provides cautious interpretation of already-computed results.

The response formatter converts those results into readable English or German output.

For compound workflows:

```text
result 1 ──┐
           │
result 2 ──┼──→ combined analytical response
           │
result 3 ──┘
```

The response can describe the analytical operations that were actually executed without exposing private reasoning.

The interpretation layer does not independently query data or create unsupported healthcare statistics.

---

## Visualization Architecture

Visualization is separated from analytics computation.

```text
deterministic result
        ↓
Chart Router
        ↓
Visualization Tools
        ↓
Plotly figure
```

The chart router selects supported visualization behavior based on the primary analytical route.

Multi-step workflows currently retain **one primary visualization**, while the textual response includes all executed analytical results.

This avoids introducing a separate multi-chart dashboard architecture in v1.2.0.

Detailed chart behavior is documented in [Visualization Tools](visualization_tools.md).

---

## Persona and Interface Layer

The Gradio application is implemented in:

```text
app.py
```

The interface supports:

- English/German interaction
- stakeholder personas
- persona-guided prompts
- single-step questions
- supported multi-step questions
- analytical responses
- workflow execution status
- Plotly visualizations

Current personas are:

- Hospital Operations Analyst
- Healthcare Fraud Investigator
- Healthcare Policy Researcher

Personas guide exploration but do not modify:

```text
analytics formulas
tool permissions
planner limits
safety boundaries
```

The interface therefore remains a presentation layer over the controlled analytical architecture.

For usage details, see [User Guide](user_guide.md).

---

## Runtime Architecture

The project supports two primary runtime contexts.

### Local

```text
data/processed/
        ↓
full cleaned Parquet data
        ↓
same analytics/orchestration architecture
```

### Hugging Face

```text
data/sample/
        ↓
lightweight sample Parquet data
        ↓
same core analytics/orchestration architecture
```

The primary runtime difference is the configured dataset rather than the analytical control model.

Deployment-specific instructions belong in [Deployment Guide](deployment.md).

---

## Architectural Safety Boundaries

Safety is enforced through component boundaries rather than unrestricted model behavior.

```text
User question
        ↓
Language normalization
        ↓
Bounded planner
        ↓
Approved registry
        ↓
Deterministic analytics
        ↓
Cautious interpretation
```

The system does not provide:

- medical diagnosis
- treatment recommendations
- patient-specific clinical advice
- fraud determination
- causal medical conclusions

The orchestration layer does not permit arbitrary:

- Python execution
- SQL execution
- pandas expressions
- dataframe manipulation
- analytics-engine method selection
- unregistered tools
- open-ended analytical loops

Unsupported or causal requests can terminate without executing analytics tools.

Detailed scope restrictions are documented in [Limitations](limitations.md).

---

## Architectural Boundaries

The system can be summarized through six primary boundaries:

| Boundary | Responsibility |
|---|---|
| **Data** | Upstream cleaning is separated from downstream analytics |
| **Computation** | `HealthcareAnalyticsEngine` owns numerical results |
| **Capability** | `tool_registry.py` defines approved controller-facing analytics |
| **Planning** | `planner.py` selects bounded approved tool sequences |
| **Orchestration** | LangGraph coordinates execution and result flow |
| **Presentation** | Insight, formatting, visualization, and Gradio present results |

These boundaries are the core of the project's architecture.

---

## Current Architectural Constraints

The architecture is intentionally bounded:

- compound workflows are explicitly supported rather than open-ended
- plans are limited to three approved analytics executions
- multi-step workflows currently render one primary visualization
- healthcare analysis is descriptive rather than causal
- the public deployment uses lightweight sample data
- optional LLM explanation remains separate from deterministic computation

These are design constraints rather than hidden capabilities.

For the complete discussion, see [Limitations](limitations.md).

---

## Documentation Map

Detailed implementation information is intentionally separated from this architecture overview.

| Document | Responsibility |
|---|---|
| [LangGraph Orchestration](langgraph_orchestration.md) | Planner, graph state, bounded execution, and multi-result orchestration |
| [Analytics Engine](analytics_engine.md) | Deterministic analytical calculations |
| [LLM Response Layer](llm_response_layer.md) | Controlled response and optional LLM explanation architecture |
| [Visualization Tools](visualization_tools.md) | Plotly chart implementation |
| [Gradio Interface](gradio_interface.md) | User-interface implementation |
| [Data Contract](data_contract.md) | Data inputs and schema expectations |
| [User Guide](user_guide.md) | Application usage |
| [Limitations](limitations.md) | Scope, safety, and known limitations |
| [Deployment Guide](deployment.md) | Local and Hugging Face deployment |

---

## Architecture Summary

Medical Insight Explorer Agent uses a layered deterministic-first architecture:

```text
Validated healthcare data
        ↓
Deterministic analytics
        ↓
Approved capability registry
        ↓
Bounded analytical planning
        ↓
LangGraph orchestration
        ↓
Stored analytical results
        ↓
Interpretation + response synthesis
        ↓
Controlled visualization
        ↓
Bilingual Gradio interface
```

The responsibilities remain deliberately separated:

```text
Analytics engine → computes
Registry         → constrains
Planner          → selects
LangGraph        → coordinates
Insight layer    → interprets
Interface        → presents
```

This structure provides controlled multi-step analytical behavior without giving the orchestration layer unrestricted access to healthcare data or arbitrary computation.