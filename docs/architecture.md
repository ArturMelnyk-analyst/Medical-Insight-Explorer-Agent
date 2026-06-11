# Architecture — Medical Insight Explorer Agent



## Purpose



The Medical Insight Explorer Agent is designed as a controlled conversational analytics system for cleaned Medicare healthcare claims data.



The project connects an upstream healthcare data-cleaning pipeline with a downstream analytics and AI-assisted interface.



The main architectural principle is:



```text
Deterministic computation first.

LLM-style explanation second.

No unsupported medical diagnosis.
```



## System Flow

```text
Raw Kaggle CSV files
      ↓
Healthcare-Data-Cleaning repository
      ↓
Cleaned validated Parquet tables
      ↓
Medical Insight Explorer Agent
      ↓
HealthcareDataLoader
      ↓
HealthcareAnalyticsEngine
      ↓
Stakeholder persona context
      ↓
LangGraph workflow
      ↓
Analytical insight layer
      ↓
Response formatter
      ↓
Chart router
      ↓
Bilingual Gradio / Hugging Face interface
```

## Architecture Diagrams

Architecture diagrams are stored under:

```text
images/architecture/
```

Current diagrams include:

```text
images/architecture/data_pipeline_architecture.png
images/architecture/agent_workflow_architecture.png
```

The data pipeline diagram shows the upstream cleaning project, cleaned Parquet outputs, data loading, and deterministic analytics engine.

The agent workflow diagram shows the LangGraph routing flow, deterministic analytics tools, response generation, optional Plotly chart output, and bilingual Gradio/Hugging Face interface.


## Repository Relationship



This project is intentionally connected to the upstream repository:


```text
Healthcare-Data-Cleaning
```


The upstream project is responsible for:



- raw CSV loading
- cleaning
- validation
- feature engineering
- relationship checks
- Parquet export



This repository starts from the cleaned Parquet outputs and focuses on:



- loading validated relational tables
- computing deterministic healthcare analytics
- generating Plotly visualizations
- providing persona-guided analytical workflows
- adding cautious analytical interpretation
- explaining computed results
- exposing the workflow through a bilingual Gradio interface
- deploying a lightweight sample-data demo on Hugging Face Spaces



## Main Components



| Component           | File                           | Responsibility                                                        |
| ------------------- | ------------------------------ | --------------------------------------------------------------------- |
| Data loader         | `agent/data_loader.py`         | Loads required cleaned Parquet tables                                 |
| Analytics engine    | `agent/analytics_engine.py`    | Computes deterministic healthcare metrics                             |
| Visualization tools | `agent/visualization_tools.py` | Generates reusable Plotly chart types                                 |
| Chart router        | `agent/chart_router.py`        | Builds route-specific Plotly visualizations                           |
| Language utilities  | `agent/language_utils.py`      | Normalizes supported bilingual prompts                                |
| Persona layer       | `agent/personas.py`            | Defines stakeholder personas, descriptions, and recommended questions |
| Insight layer       | `agent/insight_layer.py`       | Adds cautious deterministic analytical interpretation                 |
| Response formatter  | `agent/response_formatter.py`  | Formats summaries, insights, computed results, and safety notes       |
| Response layer      | `agent/response_generator.py`  | Provides controlled routing and optional LLM explanation support      |
| Graph workflow      | `agent/graph_workflow.py`      | Coordinates LangGraph execution workflow                              |
| Prompt templates    | `agent/prompt_templates.py`    | Defines safe explanation prompts for optional LLM usage               |
| Gradio app          | `app.py`                       | Provides bilingual interactive user interface                         |




## Data Layer



The project expects cleaned Parquet files under:


```text
data/processed/
```


These full datasets are excluded from GitHub.



The expected tables are:



- train_beneficiary_clean.parquet
- test_beneficiary_clean.parquet
- train_inpatient_clean.parquet
- test_inpatient_clean.parquet
- train_outpatient_clean.parquet
- test_outpatient_clean.parquet
- train_labels_clean.parquet
- test_labels_clean.parquet



The app can also fall back to:


```text
data/sample/
```


for future lightweight demo deployment.




## Analytics Layer



The analytics engine computes controlled metrics using pandas.

Examples include:

- table shape summaries
- inpatient and outpatient claim summaries
- beneficiary age statistics
- top providers by claim count
- distribution by state
- reimbursement distribution analysis
- reimbursement comparison by chronic-condition indicator

The key point is that numbers are computed by code, not invented by an LLM.



## Persona Layer

The persona layer defines stakeholder-oriented demo workflows.

Current personas include:

- Hospital Operations Analyst
- Healthcare Fraud Investigator
- Healthcare Policy Researcher

Each persona provides:

- a short use-case description
- recommended analytical questions
- bilingual English/German support

This layer makes the app purpose clearer for reviewers by connecting supported analytics routes to realistic healthcare stakeholder needs.


## Insight Layer

The insight layer adds deterministic analytical interpretation after computation.

It does not create new statistics and does not make clinical claims.

The goal is to explain why a computed result may matter in a cautious, non-causal, claims-analytics context.

Example insight types include:

- provider concentration interpretation
- regional utilization interpretation
- reimbursement distribution interpretation
- cautious chronic-condition comparison interpretation



## Visualization Layer

The visualization tools convert analytics results into Plotly charts.

Supported visual types include:

- vertical bar charts
- horizontal bar charts
- histograms
- box plots
- placeholder charts for text-only analytical questions

Chart selection remains route-based and controlled.




## Response Layer



The response layer uses rule-based routing coordinated through LangGraph orchestration.



The workflow is:


```text
User question
       ↓
Stakeholder persona context
       ↓
Normalize question if needed
       ↓
Select supported analytics route
       ↓
Run deterministic pandas function
       ↓
Generate analytical insight
       ↓
Format computed result
       ↓
Return text response and optional chart
```


The LLM does not directly manipulate dataframes.

The current deployed configuration uses deterministic fallback responses.


## LangGraph Orchestration Layer


The LangGraph orchestration layer makes the workflow explicit as a graph.

It organizes the following steps:

```text
normalize_question
       ↓
route_question
       ↓
run_analytics
       ↓
generate_response
       ↓
generate_chart
```

The graph does not replace deterministic analytics.

It coordinates the existing safe computation, response-generation and visualization pipeline.



## Bilingual UI Layer



The Gradio interface supports:

- English personas
- German personas
- persona-specific recommended questions
- clickable persona-specific example questions
- English/German summaries
- English/German analytical insights
- German-safe analytics wording
- translated method notes
- translated safety notes
- translated chart titles

German questions are normalized into supported analytics routes before computation.





## Safety and Scope



The system is designed for claims analytics, not clinical decision-making.



It does not:



- diagnose patients
- recommend treatment
- predict individual medical outcomes
- provide clinical advice
- claim causal relationships without evidence





## Future Architecture Improvements



Possible future improvements include:



- LangSmith tracing
- conditional graph routing
- expanded multilingual support
- expanded analytics tools
- automated test suite
- optional database-backed query layer

