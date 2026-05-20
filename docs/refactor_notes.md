\# Refactor Notes



\## Purpose



This document explains the response and chart helper refactor completed after LangGraph orchestration was added.



\## Why This Refactor Was Needed



After LangGraph integration, some helper logic existed in more than one place.



Duplicated logic increases maintenance risk because future changes could update one path but not another.



This refactor separates responsibilities more clearly.



\## Updated Module Responsibilities



| Module | Responsibility |

|---|---|

| `app.py` | Gradio UI layout and event handling |

| `agent/graph\_workflow.py` | LangGraph state workflow and orchestration |

| `agent/language\_utils.py` | Language normalization helpers |

| `agent/response\_formatter.py` | English/German response formatting |

| `agent/chart\_router.py` | Route-based Plotly chart generation |



\## Design Principle



The app should remain thin.



The graph should orchestrate.



Helper modules should format, normalize, or visualize.



Deterministic analytics remain in `HealthcareAnalyticsEngine`.



\## Result



The project now has a cleaner separation between:



\- UI logic

\- orchestration logic

\- response formatting

\- chart routing

\- deterministic analytics



This makes the project easier to maintain and extend.

