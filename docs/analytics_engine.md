# Analytics Engine

## Purpose

The analytics engine provides deterministic pandas-based calculations over cleaned Medicare healthcare claims data.

It is responsible for computing healthcare claims metrics before response formatting, analytical interpretation, or visualization.

The engine is intentionally separate from natural-language planning and orchestration.

---

## Current Functions

### Dataset Inspection

| Function | Purpose |
|---|---|
| `get_table_shapes()` | Returns row and column counts for loaded tables |
| `available_beneficiary_columns()` | Lists beneficiary columns available for analytics |

### Claim Analytics

| Function | Purpose |
|---|---|
| `inpatient_claim_summary()` | Summarizes inpatient claims, beneficiaries, providers, and reimbursement |
| `outpatient_claim_summary()` | Summarizes outpatient claims, beneficiaries, providers, and reimbursement |
| `claim_distribution_by_state()` | Counts claims by beneficiary state |

### Provider & Beneficiary Analytics

| Function | Purpose |
|---|---|
| `top_providers_by_claim_count()` | Returns top providers by claim volume |
| `beneficiary_age_summary()` | Summarizes beneficiary age statistics |

### Reimbursement Analytics

| Function | Purpose |
|---|---|
| `average_inpatient_cost_by_chronic_condition()` | Calculates inpatient reimbursement by chronic-condition flag |
| `inpatient_reimbursement_by_diabetes_status()` | Returns inpatient reimbursement distributions segmented by diabetes status |
| `inpatient_reimbursement_distribution()` | Returns inpatient reimbursement values for distribution analysis |

---

## Approved Analytics Boundary

The analytics engine contains deterministic analytical methods, but controller-facing execution is restricted through:

```text
agent/tool_registry.py
```

The registry exposes only approved analytical capabilities to the application workflow.

This creates the boundary:

```text
User question
        ↓
Controlled planning / routing
        ↓
Approved analytics tool registry
        ↓
HealthcareAnalyticsEngine
        ↓
Deterministic pandas result
```

The analytics engine itself does not decide which tool should be executed.

For registry and orchestration details, see:

- [Architecture](architecture.md)
- [LangGraph Orchestration](langgraph_orchestration.md)

---

## Design Principle

The central analytical rule is:

```text
natural-language request
        ↓
approved deterministic calculation
        ↓
computed result
        ↓
interpretation and presentation
```

Healthcare statistics are calculated by predefined pandas functions rather than generated from natural-language reasoning.

This keeps numerical outputs reproducible and separates computation from explanation.

---

## Relationship to Multi-Step Analytics

Version v1.2.0 supports bounded multi-step questions, but this does not change the responsibility of the analytics engine.

For a supported compound question, the orchestration layer may execute multiple approved tools sequentially:

```text
approved tool 1 → deterministic result 1
approved tool 2 → deterministic result 2
                    ↓
             response synthesis
```

Each individual result is still produced independently by the deterministic analytics engine.

The engine does not create plans, execute autonomous loops, or synthesize multi-step responses.

---

## Scope

The analytics engine is designed for descriptive healthcare claims analysis, including:

- claims summaries
- provider activity
- beneficiary statistics
- geographic claim distributions
- reimbursement analysis

It does not perform:

- diagnosis
- treatment recommendations
- clinical decision-making
- fraud determination
- causal medical inference
- arbitrary Python, SQL, or dataframe execution

For complete project boundaries, see [Limitations](limitations.md).

---

## Summary

The analytics engine remains the deterministic computational foundation of the project:

```text
approved analytical request
        ↓
predefined pandas calculation
        ↓
deterministic healthcare claims result
```

Planning, multilingual normalization, response synthesis, and visualization are handled by separate application layers.