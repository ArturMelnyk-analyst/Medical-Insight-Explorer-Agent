# Analytics Engine



## Purpose



The analytics engine provides deterministic pandas-based calculations over cleaned Medicare healthcare claims data.



This layer computes deterministic healthcare metrics directly from cleaned relational datasets before any LLM-based interpretation is applied.



## Current Functions

The analytics engine exposes modular analytical helper functions used by the AI Agent for healthcare claim exploration, reimbursement analysis, provider monitoring, and beneficiary-level insights.

### Dataset Inspection

| Function | Purpose |
|---|---|
| `get_table_shapes()` | Returns row and column counts for all loaded tables |
| `available_beneficiary_columns()` | Lists beneficiary columns available for analytics |

---

### Claim Analytics

| Function | Purpose |
|---|---|
| `inpatient_claim_summary()` | Summarizes inpatient claim counts, beneficiaries, providers, and reimbursement |
| `outpatient_claim_summary()` | Summarizes outpatient claim counts, beneficiaries, providers, and reimbursement |
| `claim_distribution_by_state()` | Counts claims by beneficiary state |

---

### Reimbursement Analytics

| Function | Purpose |
|---|---|
| `average_inpatient_cost_by_chronic_condition()` | Calculates inpatient reimbursement by chronic-condition flag |
| `inpatient_reimbursement_by_diabetes_status()` | Returns inpatient reimbursement distributions segmented by diabetes status for comparative cost analysis |

---

### Provider & Beneficiary Analytics

| Function | Purpose |
|---|---|
| `top_providers_by_claim_count()` | Returns top providers by claim volume |
| `beneficiary_age_summary()` | Summarizes beneficiary age statistics |


## Design Principle



The LLM should not invent healthcare statistics.



The intended system flow is:



```text
User question
       ↓
Query routing
       ↓
Computed pandas result
       ↓
Analytical insight layer
       ↓
Formatted response
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

