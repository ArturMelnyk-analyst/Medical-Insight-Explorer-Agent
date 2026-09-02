# User Guide — Medical Insight Explorer Agent

## Purpose

This guide explains how to use **Medical Insight Explorer Agent v1.2.0**.

The application supports controlled English and German healthcare claims analytics through:

- single-step analytical questions
- supported multi-step comparisons
- deterministic analytical results
- cautious analytical insights
- controlled Plotly visualizations
- stakeholder-guided example questions

The application analyzes healthcare claims data only. It does not provide clinical advice or unrestricted data analysis.

---

## Start the App

From the project root:

```powershell
python app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://127.0.0.1:7860
```

The public demo is also available on Hugging Face Spaces:

https://huggingface.co/spaces/Artur-Melnyk/Medical-Insight-Explorer-Agent

For installation and deployment details, see [Deployment Guide](deployment.md).

---

## Using the Interface

A typical workflow is:

```text
1. Select language
        ↓
2. Select stakeholder persona
        ↓
3. Choose an example question
   or enter a supported question
        ↓
4. Run the analysis
        ↓
5. Review workflow status
        ↓
6. Read the analytical response
        ↓
7. Review the chart when available
```

---

## Language Selection

The interface supports:

- **English**
- **Deutsch**

Changing the language updates the user-facing experience, including supported example questions and response presentation.

English and German questions use the same underlying deterministic analytics.

---

## Stakeholder Personas

The interface includes three stakeholder perspectives:

- **Hospital Operations Analyst**
- **Healthcare Fraud Investigator**
- **Healthcare Policy Researcher**

Selecting a persona updates its description and recommended analytical questions.

Personas help users explore relevant use cases. They do not change the underlying calculations, analytical permissions, or safety boundaries.

The Healthcare Fraud Investigator persona supports descriptive claims analysis; it does not determine whether fraud occurred.

---

## Single-Step Questions

Single-step questions use one approved analytics capability.

Examples include:

```text
Show me the shape of all tables

Give me an inpatient summary

Give me an outpatient summary

What is the average beneficiary age?

Show top inpatient providers

Show top outpatient providers

Show inpatient claims by state

Show outpatient claims by state

What is the diabetes cost summary?

Show reimbursement distribution
```

A supported single-step question produces one deterministic analytical result and, where appropriate, a visualization.

The workflow indicator identifies it as a single-step analysis.

---

## Multi-Step Questions

Version v1.2.0 also supports selected compound questions that require more than one approved analytical operation.

Current supported comparisons include:

### Provider Activity

```text
Compare inpatient and outpatient provider activity
```

This executes the approved inpatient and outpatient provider analyses and combines both results into one response.

### Claims by State

```text
Compare inpatient and outpatient claims by state
```

This compares the approved inpatient and outpatient state-level analyses.

### Claim Summaries

```text
Compare inpatient and outpatient claim summaries
```

This combines the inpatient and outpatient summary results.

Multi-step execution is intentionally bounded. The application does not create unrestricted analytical plans from arbitrary requests.

---

## German Questions

Supported German questions use the same analytical capabilities as their English equivalents.

Examples of single-step questions include:

```text
Zeige die Form aller Tabellen

Gib mir eine Zusammenfassung der stationären Claims

Gib mir eine Zusammenfassung der ambulanten Claims

Wie hoch ist das durchschnittliche Alter der Beneficiaries?

Zeige die wichtigsten stationären Provider

Zeige die wichtigsten ambulanten Provider

Zeige stationäre Claims nach Bundesstaat

Zeige ambulante Claims nach Bundesstaat

Wie sieht die Kostenzusammenfassung für Diabetes aus?

Zeige die Verteilung der Erstattungsbeträge
```

Supported compound questions are also available in German through the application's language-normalization layer.

The persona example buttons provide recommended questions in the selected language.

---

## Understanding Workflow Status

The interface shows whether the request used one or multiple approved analytics tools.

Conceptually:

```text
Single-step
→ one approved analytics tool executed
```

```text
Multi-step
→ multiple approved analytics tools executed
```

Unsupported or rejected requests execute no analytics tools.

The workflow indicator describes executed analytical operations without exposing private internal reasoning.

---

## Reading the Response

### Single-Step Responses

A typical single-step response includes:

1. **Summary** — what was analyzed
2. **Analytical insight** — cautious interpretation
3. **Computed result** — deterministic analytical output
4. **Method note** — context about how the result was produced
5. **Safety note** — reminder of the analytical scope

### Multi-Step Responses

Supported compound questions can additionally show:

1. **Summary**
2. **Analytical workflow**
3. **Analytical steps**
4. **Analytical insight**
5. **Computed results from each executed analysis**
6. **Method note**
7. **Safety note**

All reported numerical results come from the deterministic analytics layer.

---

## Visualizations

Charts are available for selected analytical routes, including:

- provider rankings
- claims by state
- reimbursement distribution
- diabetes reimbursement comparison

Other questions, such as table shapes, claim summaries, and beneficiary age statistics, are primarily text-based.

### Multi-Step Visualization

For a multi-step question:

```text
all executed analytical results
→ included in the text response

primary analytical result
→ represented by one chart
```

Multi-step workflows currently display **one primary visualization**, not one chart for every executed analytical tool.

This is intentional behavior in v1.2.0.

---

## Unsupported Questions

The application supports controlled healthcare claims analytics rather than unrestricted natural-language data exploration.

If a question cannot be mapped to an approved analytical capability, the application returns a controlled fallback instead of attempting arbitrary dataframe operations.

For example, the application does not dynamically execute user-requested:

```text
Python
SQL
pandas code
arbitrary dataframe operations
```

Try one of the persona-guided questions when exploring the available analytical capabilities.

---

## Clinical and Causal Questions

The application should not be used for:

- diagnosis
- treatment recommendations
- patient-specific clinical advice
- fraud determination
- causal medical conclusions

For example, a descriptive question such as:

```text
What is the diabetes cost summary?
```

is within the analytical scope.

A causal question such as:

```text
Does diabetes cause higher inpatient reimbursement?
```

is outside the supported scope and should not execute healthcare analytics.

For complete boundaries, see [Limitations](limitations.md).

---

## Recommended Demo Flow

A concise way to demonstrate v1.2.0 is:

1. Select **English**
2. Select **Hospital Operations Analyst**
3. Run `Show top inpatient providers`
4. Review the single-step status, response, and chart
5. Run `Compare inpatient and outpatient provider activity`
6. Review the multi-step status and combined results
7. Confirm that one primary chart is displayed
8. Switch to **Deutsch**
9. Select a German persona-guided question
10. Run a supported German single-step or multi-step analysis

This demonstrates the progression from:

```text
single-step analytics
        ↓
bounded multi-step analytics
        ↓
bilingual interaction
```

without requiring technical knowledge of the underlying implementation.

---

## Data

The local application can use cleaned Parquet files under:

```text
data/processed/
```

The public Hugging Face demo uses lightweight sample data under:

```text
data/sample/
```

Public-demo results may therefore differ from results produced using the complete local dataset.

For details, see:

- [Data Contract](data_contract.md)
- [Deployment Guide](deployment.md)

---

## Troubleshooting

### App Does Not Start

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

Then run:

```powershell
python app.py
```

### Data Cannot Be Loaded

Confirm that the expected Parquet data exists under:

```text
data/processed/
```

or that the configured sample data is available under:

```text
data/sample/
```

### Chart Does Not Render

Restart the application:

```text
CTRL + C
```

then:

```powershell
python app.py
```

If the selected analytical route is text-only, the absence of an analytical chart may be expected.

---

## Additional Documentation

For technical details, see:

- [Architecture](architecture.md)
- [LangGraph Orchestration](langgraph_orchestration.md)
- [Analytics Engine](analytics_engine.md)
- [Visualization Tools](visualization_tools.md)
- [Deployment Guide](deployment.md)
- [Limitations](limitations.md)

---

## Summary

Medical Insight Explorer Agent supports controlled interaction with deterministic healthcare claims analytics.

Users can:

```text
select a stakeholder perspective
        ↓
ask a supported question
        ↓
run one or multiple approved analytics tools
        ↓
review deterministic results
        ↓
read cautious analytical insight
        ↓
inspect a controlled visualization
```

Version v1.2.0 extends the original single-step experience with bounded multi-step comparisons while preserving deterministic computation, bilingual interaction, and explicit analytical limits.