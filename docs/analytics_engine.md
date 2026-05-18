# Analytics Engine



## Purpose



The analytics engine provides deterministic pandas-based calculations over cleaned Medicare healthcare claims data.



This layer computes deterministic healthcare metrics directly from cleaned relational datasets before any LLM-based interpretation is applied.



## Current Functions


| Function | Purpose |

|---|---|

| `get_table_shapes()` | Returns row and column counts for all loaded tables |

| `inpatient_claim_summary()` | Summarizes inpatient claim counts, beneficiaries, providers, and reimbursement |

| `outpatient_claim_summary()` | Summarizes outpatient claim counts, beneficiaries, providers, and reimbursement |

| `beneficiary_age_summary()` | Summarizes beneficiary age statistics |

| `top_providers_by_claim_count()` | Returns top providers by claim volume |

| `average_inpatient_cost_by_chronic_condition()` | Calculates inpatient reimbursement by chronic-condition flag |

| `claim_distribution_by_state()` | Counts claims by beneficiary state |

| `available_beneficiary_columns()` | Lists beneficiary columns available for analytics |


## Design Principle



The LLM should not invent healthcare statistics.



The intended system flow is:



```text
User question
       ↓
Query routing
       ↓
Analytics engine function
      ↓
Computed pandas result
      ↓
LLM explanation
```


## Scope

This module does not perform:

- diagnosis
- clinical decision-making
- medical recommendations

It is designed for:

- claims analytics
- utilization analysis
- reimbursement summaries
- portfolio demonstration

