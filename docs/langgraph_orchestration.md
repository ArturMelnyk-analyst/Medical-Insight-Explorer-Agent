# LangGraph Orchestration



## Purpose



This document explains the LangGraph orchestration layer added to the Medical Insight Explorer Agent.



The goal is to make the existing deterministic analytics workflow explicit as a graph.



This PR does not change the core analytics logic. It wraps the existing safe pipeline with a structured graph workflow.



## Why LangGraph



The project previously used a simple direct routing pattern:



```text

User question
      ↓
Rule-based router
      ↓
Deterministic analytics function
      ↓
Text response
      ↓
Optional chart

```



The LangGraph layer makes this workflow more explicit and easier to extend.



## Graph Flow



```text

User question
      ↓
normalize_question
      ↓
route_question
      ↓
run_analytics
      ↓
generate_response
      ↓
generate_chart
      ↓
final output

```


## Persona Context

Persona selection currently guides the UI and recommended questions.

The LangGraph workflow still routes based on the submitted question and selected language.


## Main File



The orchestration logic is implemented in:



```text

agent/graph_workflow.py

```



## Graph State



The graph passes a shared state object through each node.



The state includes:



- original question

- selected language

- normalized question

- selected analytics route

- computed result

- formatted response with analytical insight

- optional Plotly chart



## Graph Nodes



| Node | Responsibility |

|---|---|

| `normalize_question` | Normalizes German prompts into supported analytics questions |

| `route_question` | Selects a supported analytics route |

| `run_analytics` | Executes deterministic pandas-based analytics |

| `generate_response` | Formats the computed result into English or German text |

| `generate_chart` | Creates an optional Plotly figure |



## Design Principle



The graph does not allow an LLM to manipulate healthcare dataframes.



The computation remains deterministic.



The graph only organizes the workflow.



## Safety Boundaries



This workflow remains limited to healthcare claims analytics.



It does not provide:



- diagnosis

- treatment recommendations

- clinical decision-making

- patient-level medical advice

- unsupported causal claims



## Local Validation



Example English test:



```bash

python -c "from agent.data_loader import HealthcareDataLoader; from agent.analytics_engine import HealthcareAnalyticsEngine; from agent.response_generator import ResponseGenerator; from agent.graph_workflow import HealthcareGraphWorkflow; tables=HealthcareDataLoader().load_tables(); engine=HealthcareAnalyticsEngine(tables); rg=ResponseGenerator(engine, use_llm=False); graph=HealthcareGraphWorkflow(engine, rg); result=graph.invoke('Show top inpatient providers', 'English'); print(result['route']); print(result['text_response'][:300])"

```



Example German test:



```bash

python -c "from agent.data_loader import HealthcareDataLoader; from agent.analytics_engine import HealthcareAnalyticsEngine; from agent.response_generator import ResponseGenerator; from agent.graph_workflow import HealthcareGraphWorkflow; tables=HealthcareDataLoader().load_tables(); engine=HealthcareAnalyticsEngine(tables); rg=ResponseGenerator(engine, use_llm=False); graph=HealthcareGraphWorkflow(engine, rg); result=graph.invoke('Zeige die wichtigsten stationären Provider', 'Deutsch'); print(result['route']); print(result['text_response'][:300])"

```



## Future Improvements



Future improvements may include:



- conditional graph edges

- richer route validation

- graph-level logging

- LangSmith tracing

- expanded analytical routes

- optional LLM explanation node

