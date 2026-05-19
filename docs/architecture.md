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
Visualization tools
       ↓
ResponseGenerator
       ↓
LangGraph workflow
       ↓
Gradio interface
```


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
- computing healthcare analytics
- generating visualizations
- explaining computed results
- exposing the workflow through a Gradio interface



## Main Components



| Component           | File                           | Responsibility                                          |
|---|---|---|
| Data loader         | `agent/data_loader.py`         | Loads required cleaned Parquet tables                   |
| Analytics engine    | `agent/analytics_engine.py`    | Computes deterministic healthcare metrics               |
| Visualization tools | `agent/visualization_tools.py` | Generates Plotly charts                                 |
| Response layer      | `agent/response_generator.py`  | Routes questions and formats grounded responses         |
| Graph workflow      | `agent/graph_workflow.py`      | Coordinates LangGraph execution workflow                |
| Prompt templates    | `agent/prompt_templates.py`    | Defines safe explanation prompts for optional LLM usage |
| Gradio app          | `app.py`                       | Provides bilingual interactive user interface           |




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
- claim distribution by state
- reimbursement summaries by chronic-condition indicator



The key point is that numbers are computed by code, not invented by an LLM.





## Visualization Layer



The visualization tools convert analytics results into Plotly charts.



Supported visual types include:



- vertical bar charts
- horizontal bar charts
- histograms
- box plots
- placeholder charts for text-only analytical questions





## Response Layer



The response layer uses rule-based routing coordinated through LangGraph orchestration.



The workflow is:


```text
User question
       ↓
Normalize question if needed
       ↓
Select supported analytics route
       ↓
Run deterministic pandas function
       ↓
Format computed result
       ↓
Return text response and optional chart
```


The LLM does not directly manipulate dataframes.


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

It coordinates the existing safe computation and response-generation pipeline.



## Bilingual UI Layer



The Gradio interface supports:



- English examples
- German examples
- English/German summaries
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
- richer chart routing
- expanded analytics tools
- automated test suite
- optional database-backed query layer

