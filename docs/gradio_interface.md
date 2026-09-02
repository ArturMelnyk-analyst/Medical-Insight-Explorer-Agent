# Gradio Interface

## Purpose

The Gradio interface provides the interactive front end for **Medical Insight Explorer Agent v1.2.0**.

Users can:

- ask supported healthcare claims questions
- switch between English and German
- select stakeholder personas
- run single-step and supported multi-step analytics
- review deterministic analytical results and insights
- inspect Plotly visualizations when available
- see whether one or multiple approved analytics tools were executed

---

## Interface Flow

The deployed application follows this user-facing flow:

```text
User question
        ↓
Gradio interface
        ↓
Language normalization
        ↓
Controlled analytics planning
        ↓
Approved analytics execution
        ↓
Response + analytical insight
        ↓
Primary Plotly visualization
        ↓
Gradio output
```

Detailed orchestration behavior is documented in [LangGraph Orchestration](langgraph_orchestration.md).

---

## Language Selection

The interface supports:

- **English**
- **Deutsch**

Changing the language updates the relevant user-facing content, including:

- persona descriptions
- recommended questions
- response presentation
- analytical step descriptions
- workflow status
- method and safety notes

German questions are normalized into the same language-independent analytical capabilities used for English questions.

---

## Stakeholder Personas

The interface provides three stakeholder perspectives:

- **Hospital Operations Analyst**
- **Healthcare Fraud Investigator**
- **Healthcare Policy Researcher**

Selecting a persona updates its description and recommended questions.

Persona examples include both single-step questions and supported multi-step comparisons.

Personas guide the user experience but do not change analytical calculations, tool permissions, or safety boundaries.

---

## Single-Step Analytics

Existing single-step questions remain supported.

Examples include:

```text
Show me the shape of all tables

Give me an inpatient summary

Give me an outpatient summary

What is the average beneficiary age?

Show top inpatient providers

Show top outpatient providers

Show inpatient claims by state

Show outpatient claims by state

What is the diabetes cost summary?

Show reimbursement distribution
```

A supported single-step request executes one approved analytics tool.

---

## Multi-Step Analytics

Version v1.2.0 adds controlled multi-step questions for selected comparisons.

Supported compound workflows include:

```text
Compare inpatient and outpatient provider activity

Compare inpatient and outpatient claims by state

Compare inpatient and outpatient claim summaries
```

Equivalent supported German questions use the same analytical workflows.

For multi-step requests, the interface presents the results from all executed analytical operations in one combined response.

---

## Workflow Indicator

The interface displays the analytical workflow status so users can distinguish between:

```text
Single-step
→ one approved analytics tool executed
```

and:

```text
Multi-step
→ multiple approved analytics tools executed
```

Unsupported or rejected requests execute no analytics tools.

The indicator exposes executed analytical operations, not private reasoning or chain-of-thought.

---

## Response Presentation

Single-step responses preserve the existing concise analytical format.

Supported multi-step responses can include:

- summary
- analytical workflow
- analytical steps
- analytical insight
- computed results from each executed tool
- method note
- safety note

The response area is sized to accommodate the longer multi-result format.

All numerical healthcare metrics originate from deterministic analytics functions.

---

## Visualization Behavior

Supported analytical routes can produce Plotly charts, including:

- provider rankings
- claims by state
- reimbursement distribution
- diabetes reimbursement comparison

Other analytical routes, such as table shapes and claim summaries, are primarily text-based.

### Multi-Step Visualization

Multi-step workflows intentionally retain **one primary visualization**.

```text
all executed results
→ textual response

primary analytical route
→ Plotly chart
```

Multiple simultaneous charts are outside the current v1.2.0 interface scope.

For visualization details, see [Visualization Tools](visualization_tools.md).

---

## Guided Questions

Recommended questions are presented as clickable interface examples.

They update according to the selected:

```text
language + stakeholder persona
```

This allows reviewers to explore supported functionality without needing to know the available analytical routes in advance.

The user can also enter a supported question manually.

---

## Data Source

The application can use full processed data locally from:

```text
data/processed/
```

and lightweight sample data from:

```text
data/sample/
```

The public Hugging Face deployment uses the lightweight sample-data path.

For details, see [Deployment Guide](deployment.md).

---

## Controlled Scope

The interface provides access to approved descriptive healthcare claims analytics.

It does not provide unrestricted execution of:

- Python
- SQL
- pandas operations
- arbitrary analytics-engine methods

Unsupported and causal medical requests use controlled handling rather than unrestricted analytical execution.

For complete boundaries, see [Limitations](limitations.md).

---

## Summary

The v1.2.0 interface combines:

```text
bilingual interaction
        +
stakeholder guidance
        +
single-step analytics
        +
bounded multi-step analytics
        +
workflow transparency
        +
deterministic results
        +
controlled visualization
```

Gradio provides the user-facing layer while analytical computation, planning, and execution remain separated into dedicated backend components.