\# LangGraph Orchestration



\## Purpose



This document explains the LangGraph orchestration layer added to the Medical Insight Explorer Agent.



The goal is to make the existing deterministic analytics workflow explicit as a graph.



This PR does not change the core analytics logic. It wraps the existing safe pipeline with a structured graph workflow.



\## Why LangGraph



The project previously used a simple direct routing pattern:



```text

User question

&#x20;      ↓

Rule-based router

&#x20;      ↓

Deterministic analytics function

&#x20;      ↓

Text response

&#x20;      ↓

Optional chart

```



The LangGraph layer makes this workflow more explicit and easier to extend.



\## Graph Flow



```text

User question

&#x20;      ↓

normalize\_question

&#x20;      ↓

route\_question

&#x20;      ↓

run\_analytics

&#x20;      ↓

generate\_response

&#x20;      ↓

generate\_chart

&#x20;      ↓

final output

```



\## Main File



The orchestration logic is implemented in:



```text

agent/graph\_workflow.py

```



\## Graph State



The graph passes a shared state object through each node.



The state includes:



\- original question

\- selected language

\- normalized question

\- selected analytics route

\- computed result

\- formatted text response

\- optional Plotly chart



\## Graph Nodes



| Node | Responsibility |

|---|---|

| `normalize\_question` | Normalizes German prompts into supported analytics questions |

| `route\_question` | Selects a supported analytics route |

| `run\_analytics` | Executes deterministic pandas-based analytics |

| `generate\_response` | Formats the computed result into English or German text |

| `generate\_chart` | Creates an optional Plotly figure |



\## Design Principle



The graph does not allow an LLM to manipulate healthcare dataframes.



The computation remains deterministic.



The graph only organizes the workflow.



\## Safety Boundaries



This workflow remains limited to healthcare claims analytics.



It does not provide:



\- diagnosis

\- treatment recommendations

\- clinical decision-making

\- patient-level medical advice

\- unsupported causal claims



\## Local Validation



Example English test:



```bash

python -c "from agent.data\_loader import HealthcareDataLoader; from agent.analytics\_engine import HealthcareAnalyticsEngine; from agent.response\_generator import ResponseGenerator; from agent.graph\_workflow import HealthcareGraphWorkflow; tables=HealthcareDataLoader().load\_tables(); engine=HealthcareAnalyticsEngine(tables); rg=ResponseGenerator(engine, use\_llm=False); graph=HealthcareGraphWorkflow(engine, rg); result=graph.invoke('Show top inpatient providers', 'English'); print(result\['route']); print(result\['text\_response']\[:300])"

```



Example German test:



```bash

python -c "from agent.data\_loader import HealthcareDataLoader; from agent.analytics\_engine import HealthcareAnalyticsEngine; from agent.response\_generator import ResponseGenerator; from agent.graph\_workflow import HealthcareGraphWorkflow; tables=HealthcareDataLoader().load\_tables(); engine=HealthcareAnalyticsEngine(tables); rg=ResponseGenerator(engine, use\_llm=False); graph=HealthcareGraphWorkflow(engine, rg); result=graph.invoke('Zeige die wichtigsten stationären Provider', 'Deutsch'); print(result\['route']); print(result\['text\_response']\[:300])"

```



\## Future Improvements



Future improvements may include:



\- conditional graph edges

\- richer route validation

\- graph-level logging

\- LangSmith tracing

\- expanded analytical routes

\- optional LLM explanation node

