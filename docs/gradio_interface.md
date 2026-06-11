# Gradio Interface


## Purpose

The Gradio interface provides an interactive front end for the Medical Insight Explorer Agent.

It allows users to ask natural-language healthcare analytics questions and receive:

- grounded text responses
- deterministic analytical results
- optional Plotly visualizations

## Architecture


```text
User question
      ↓
Gradio interface
      ↓
Stakeholder persona guidance
      ↓
LangGraph workflow
      ↓
HealthcareAnalyticsEngine
      ↓
Analytical insight layer
      ↓
Text response + optional Plotly chart
```

## Supported Questions

Current examples include:

```text
Show me the shape of all tables
Give me an inpatient summary
Give me an outpatient summary
What is the average beneficiary age?
Show top inpatient providers
Show top outpatient providers
Show inpatient claims by state
What is the diabetes cost summary?
Show reimbursement distribution
```

## Visualization Behavior

Some questions are best answered as text summaries, while others produce charts.

Text-only examples:

- table shapes
- inpatient summary
- outpatient summary
- beneficiary age summary


Chart examples:

- top providers by claim count
- claims by state
- reimbursement distribution
- diabetes reimbursement comparison

For text-only questions, the app displays a placeholder chart explaining that no visualization was generated.


## Bilingual Interface

The Gradio interface supports English and German user-facing text.

Current bilingual elements include:

- language selector
- example prompts
- response summaries
- method notes
- safety notes
- visualization placeholder messages

The backend analytics routes remain deterministic and language-independent. German prompts are normalized into supported deterministic analytics routes before computation.

This design keeps the analytics engine stable while improving usability for German-speaking reviewers.

## Stakeholder Persona Selector

The Gradio interface includes a stakeholder persona selector.

Selecting a persona updates:

- persona description
- clickable recommended questions
- guided analytics workflow

This improves reviewer usability by making the app purpose clear for different healthcare stakeholders.


## Data Source

The app first looks for full local processed data under:

```text
data/processed/
```

If full data is unavailable, it can fall back to:


```text
data/sample/
```

## Current Scope

This PR creates the first local interactive UI layer.

It does not yet include:

- Hugging Face deployment
- packaged sample data
- advanced chart routing
- live LLM API responses

