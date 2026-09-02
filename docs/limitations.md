# Limitations

## Purpose

Medical Insight Explorer Agent is a controlled portfolio system for descriptive healthcare claims analytics.

This document summarizes the main boundaries of the current **v1.2.0** release.

Detailed implementation information is documented separately in the architecture, orchestration, visualization, deployment, and response-layer documentation.

---

## Descriptive Claims Analytics Only

The project analyzes healthcare claims data.

It does not provide:

- medical diagnosis
- treatment recommendations
- patient-specific clinical advice
- clinical decision-making
- fraud determination
- causal medical conclusions

Analytical insights describe patterns in the available claims data and should not be interpreted as clinical or causal evidence.

---

## Bounded Analytical Scope

The application does not provide unrestricted natural-language access to the underlying dataframes.

Controller-facing analytics are limited to capabilities explicitly registered in:

```text
agent/tool_registry.py
```

The current registry exposes ten approved deterministic analytics tools.

Unsupported requests are handled through controlled fallback behavior rather than arbitrary dataframe analysis.

This means the system intentionally favors:

```text
predictable approved analytics
```

over:

```text
open-ended analytical freedom
```

For the complete capability architecture, see [Architecture](architecture.md).

---

## Limited Multi-Step Planning

Version v1.2.0 supports bounded multi-step analytics, but it is not a general-purpose autonomous analytics agent.

The planner currently supports explicit compound workflows for:

- inpatient vs outpatient provider activity
- inpatient vs outpatient claims by state
- inpatient vs outpatient claim summaries

Plans are limited to:

```text
MAX_ANALYTICS_STEPS = 3
```

The system does not:

- create arbitrary analytical plans
- generate arbitrary Python, SQL, or pandas operations
- dynamically invent new analytics tools
- continue investigating indefinitely from intermediate results

Additional compound workflows require explicit implementation.

For planning and execution details, see [LangGraph Orchestration](langgraph_orchestration.md).

---

## Deterministic Computation Boundary

Numerical healthcare results are produced by predefined pandas-based analytics functions.

The orchestration and explanation layers do not independently calculate arbitrary healthcare statistics.

The project therefore does not support:

- unrestricted dataframe manipulation
- arbitrary analytics-engine method selection
- arbitrary user-defined calculations
- dynamically generated SQL or Python analytics

This is an intentional safety and reproducibility constraint.

---

## Causal Questions

The system is designed for descriptive analytics rather than causal inference.

Causal healthcare requests are rejected before analytics execution when detected by the supported safety logic.

For example, the application may compare reimbursement distributions between groups, but it should not conclude that a medical condition **caused** the observed difference.

The current causal-safety logic is controlled and rule-based; it should not be interpreted as a complete natural-language medical-safety classifier.

---

## Multilingual Scope

The application supports English and German for its controlled analytical workflows.

Supported German questions are normalized into the same language-independent analytical capabilities used for English questions.

However, bilingual support is not equivalent to unrestricted natural-language understanding.

Questions outside the supported vocabulary, phrasing, or analytical scope may fall back even when a human could infer the intended analysis.

---

## Multi-Step Response Limitations

For supported compound questions, the textual response can synthesize results from all executed analytics tools.

However, multi-step synthesis remains bounded by the predefined analytical outputs.

It does not:

- perform hidden follow-up analysis
- introduce additional unexecuted calculations
- infer causal relationships
- expose private chain-of-thought

Only analytical operations that were actually executed are presented as workflow steps.

---

## Visualization Limitations

Charts are available only for supported analytical routes.

Some questions are intentionally text-only.

For multi-step workflows:

```text
all executed analytical results
→ included in the textual response

primary analytical route
→ one visualization
```

Multiple simultaneous charts are outside the scope of v1.2.0.

For chart behavior, see [Visualization Tools](visualization_tools.md).

---

## Dataset Limitations

The project is based on cleaned Medicare healthcare claims data from the upstream project pipeline.

The data should not be assumed to represent:

- every healthcare system
- every patient population
- current real-world claims behavior
- complete clinical context
- causal medical relationships

Claims data records administrative and reimbursement activity and should not be treated as a complete representation of patient health or clinical decision-making.

---

## Sample Deployment

The public Hugging Face deployment uses lightweight sample Parquet data rather than the complete local processed dataset.

As a result:

- public-demo values may differ from full local results
- the deployment demonstrates system behavior rather than full-dataset analytical coverage
- the public demo should not be treated as a production healthcare analytics environment

The core deterministic analytics and controlled orchestration architecture remain the same.

See [Deployment Guide](deployment.md) for runtime details.

---

## Diabetes Reimbursement Example

The diabetes reimbursement analysis is included as an example of controlled chronic-condition claims analytics.

In the current data, reimbursement distributions for beneficiaries with and without diabetes are highly similar.

The comparison should therefore be interpreted descriptively rather than as evidence that diabetes causes higher or lower reimbursement.

This example illustrates an important project-wide distinction:

```text
observed association
≠
causal conclusion
```

---

## Persona Limitations

The interface includes stakeholder personas for:

- hospital operations
- healthcare fraud investigation
- healthcare policy research

Personas guide descriptions and recommended questions.

They do not change:

- analytics calculations
- approved tool permissions
- planner limits
- safety boundaries

In particular, the Healthcare Fraud Investigator persona does not determine whether a provider or claim is fraudulent.

---

## LLM Boundary

The project preserves optional LLM explanation architecture, but numerical healthcare computation remains deterministic.

An LLM, when enabled in the appropriate response path, is intended to explain already-computed results rather than manipulate healthcare dataframes or create numerical results independently.

The project should therefore not be interpreted as an unrestricted LLM healthcare-data agent.

See [LLM Response Layer](llm_response_layer.md) for details.

---

## Production Limitations

Medical Insight Explorer Agent is a portfolio and demonstration project rather than a production clinical or enterprise healthcare platform.

The current architecture does not provide a complete production environment with features such as:

- enterprise authentication and authorization
- production database infrastructure
- comprehensive automated testing
- production monitoring and tracing
- clinical validation
- regulatory compliance infrastructure

These capabilities would require additional engineering and governance before production use.

---

## Summary

The project's limitations are largely intentional.

Medical Insight Explorer Agent prioritizes:

```text
deterministic computation
+
approved analytics
+
bounded orchestration
+
transparent analytical scope
```

over unrestricted autonomous analysis.

The system demonstrates controlled conversational healthcare claims analytics while deliberately limiting clinical, causal, and open-ended analytical behavior.