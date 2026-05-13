\# Analytics Engine



\## Purpose



The analytics engine provides deterministic pandas-based calculations over cleaned Medicare healthcare claims data.



This layer computes deterministic healthcare metrics directly from cleaned relational datasets before any LLM-based interpretation is applied.



\## Current Functions



| Function | Purpose |

|---|---|

| `get\_table\_shapes()` | Returns row and column counts for all loaded tables |

| `inpatient\_claim\_summary()` | Summarizes inpatient claim counts, beneficiaries, providers, and reimbursement |

| `outpatient\_claim\_summary()` | Summarizes outpatient claim counts, beneficiaries, providers, and reimbursement |

| `beneficiary\_age\_summary()` | Summarizes beneficiary age statistics |

| `top\_providers\_by\_claim\_count()` | Returns top providers by claim volume |

| `average\_inpatient\_cost\_by\_chronic\_condition()` | Calculates inpatient reimbursement by chronic-condition flag |

| `claim\_distribution\_by\_state()` | Counts claims by beneficiary state |

| `available\_beneficiary\_columns()` | Lists beneficiary columns available for analytics |



\## Design Principle



The LLM should not invent healthcare statistics.



The intended system flow is:



```text

User question

&#x20;       ↓

Query routing

&#x20;       ↓

Analytics engine function

&#x20;       ↓

Computed pandas result

&#x20;       ↓

LLM explanation

```



\## Scope



This module does not perform diagnosis, clinical decision-making, or medical recommendations. It is designed for claims analytics, utilization analysis, cost summaries, and portfolio demonstration.

