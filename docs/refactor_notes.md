# Refactor Notes



## Purpose



This document explains the response and chart helper refactor completed after LangGraph orchestration was added.



## Why This Refactor Was Needed



After LangGraph integration, some helper logic existed in more than one place.



Duplicated logic increases maintenance risk because future changes could update one path but not another.



This refactor separates responsibilities more clearly.



## Updated Module Responsibilities



| Module | Responsibility |

|---|---|

| `app.py` | Gradio UI layout and event handling |

| `agent/graph_workflow.py` | LangGraph state workflow and orchestration |

| `agent/language_utils.py` | Language normalization helpers |

| `agent/response_formatter.py` | English/German response formatting |

| `agent/chart_router.py` | Route-based Plotly chart generation |

| `agent/personas.py` | Defines stakeholder personas and recommended questions |

| `agent/insight_layer.py` | Provides cautious analytical interpretation for supported routes |


This update extends the helper-module separation by keeping persona guidance and analytical interpretation outside `app.py`.



## Design Principle



The app should remain thin.



The graph should orchestrate.



Helper modules should format, normalize, or visualize.



Deterministic analytics remain in `HealthcareAnalyticsEngine`.



## Result



The project now has a cleaner separation between:



- UI logic

- orchestration logic

- response formatting

- chart routing

- visualization tools

- deterministic analytics

- persona guidance

- analytical insight generation



This makes the project easier to maintain and extend.

