\# Gradio Interface



\## Purpose



The Gradio interface provides an interactive front end for the Medical Insight Explorer Agent.



It allows users to ask natural-language healthcare analytics questions and receive:



\- grounded text responses

\- deterministic analytical results

\- optional Plotly visualizations



\## Architecture



```text

User question

&#x20;       ↓

Gradio interface

&#x20;       ↓

ResponseGenerator

&#x20;       ↓

QueryRouter

&#x20;       ↓

HealthcareAnalyticsEngine

&#x20;       ↓

Computed result

&#x20;       ↓

Text response + optional Plotly chart

```

\## Supported Questions



Current examples include:



Show me the shape of all tables

Give me an inpatient summary

Give me an outpatient summary

What is the average beneficiary age?

Show top inpatient providers

Show top outpatient providers

Show inpatient claims by state

What is the diabetes cost summary?

Show reimbursement distribution



\## Visualization Behavior



Some questions are best answered as text summaries, while others produce charts.



Text-only examples:



table shapes

inpatient summary

outpatient summary

beneficiary age summary



Chart examples:



top providers by claim count

claims by state

reimbursement distribution

diabetes reimbursement comparison



For text-only questions, the app displays a placeholder chart explaining that no visualization was generated.



\## Data Source



The app first looks for full local processed data under:



data/processed/



If full data is unavailable, it can fall back to:



data/sample/



\## Current Scope



This PR creates the first local interactive UI layer.



It does not yet include:



Hugging Face deployment

packaged sample data

advanced chart routing

live LLM API responses

