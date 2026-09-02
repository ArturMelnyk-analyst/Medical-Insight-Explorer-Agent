# Visualization Tools

## Purpose

The visualization layer converts deterministic healthcare analytics outputs into interactive Plotly figures.

Charts are created from already-computed analytical results rather than from unrestricted model-generated calculations.

This keeps visual outputs consistent with the deterministic analytics layer.

---

## Visualization Functions

The reusable visualization utilities include:

| Function | Purpose |
|---|---|
| `bar_chart_top_values()` | Vertical bar charts for ranked or grouped metrics |
| `horizontal_bar_chart()` | Horizontal bar charts for categories with long labels |
| `histogram()` | Numeric distribution visualization |
| `box_plot()` | Distribution comparison across groups |
| `validate_columns()` | Input validation before chart generation |

These utilities operate on analytical outputs rather than independently querying healthcare datasets.

---

## Visualization Flow

The application separates analytical computation from chart generation:

```text
Approved analytics tool
        ↓
Deterministic analytics result
        ↓
Chart routing
        ↓
Visualization utility
        ↓
Plotly figure
        ↓
Gradio interface
```

This separation prevents the visualization layer from becoming an independent analytics engine.

For the complete application flow, see [Architecture](architecture.md).

---

## Supported Visualizations

Current analytical routes with chart support include:

### Provider Activity

- top inpatient providers by claim count
- top outpatient providers by claim count

Provider rankings use bar-chart visualizations suited to comparing categorical counts.

### Claims by State

- inpatient claims by state
- outpatient claims by state

These charts provide geographic claim-count comparisons using deterministic aggregated results.

### Reimbursement Distribution

Inpatient reimbursement values can be displayed as a distribution to show the spread of reimbursement amounts rather than only a single summary statistic.

### Diabetes Reimbursement Comparison

The diabetes analysis uses a box plot to compare inpatient reimbursement distributions between:

```text
No Diabetes
Diabetes
```

This is more informative than a mean-only comparison because it preserves information about spread and distribution shape.

The visualization is descriptive and does not imply that diabetes causes differences in reimbursement.

---

## Text-Only Analytics

Not every supported analytical route requires a chart.

Examples of primarily text-based outputs include:

- table shapes
- inpatient claim summary
- outpatient claim summary
- beneficiary age summary

For these questions, the analytical response itself is the primary output.

---

## Multi-Step Visualization Behavior

Version v1.2.0 supports selected multi-step analytical workflows.

For these requests:

```text
all executed analytics
        ↓
included in the textual response

primary analytical route
        ↓
used for visualization
```

Multi-step workflows currently render **one primary visualization**, while the textual response includes **all executed analytical results**.

The application does not generate a separate chart for every tool executed within a multi-step plan.

This is an intentional v1.2.0 design boundary.

---

## Chart Routing

Chart selection is controlled by the application rather than freely generated from natural-language requests.

Only supported analytical routes with defined visualization behavior produce analytical charts.

The chart layer does not:

- execute arbitrary dataframe operations
- calculate new healthcare statistics independently
- select arbitrary analytics-engine methods
- generate unrestricted user-defined visualizations

This keeps visualization aligned with approved deterministic analytics.

---

## Gradio Integration

Plotly figures are rendered directly in the Gradio application.

The interface supports both English and German analytical workflows while using the same underlying visualization logic.

Persona selection may change the recommended questions shown to the user, but it does not change how analytical charts are calculated.

---

## Demo Assets

Representative visualization and application screenshots are stored under:

```text
images/demo/
```

Current analytical visualization assets include:

```text
top_10_inpatient_providers_by_claim_count.png
inpatient_reimbursement_distribution.png
```

Additional interface and portfolio screenshots are maintained separately from the visualization implementation.

---

## Local Notebook Rendering

When testing Plotly charts directly in Jupyter, browser rendering can be enabled with:

```python
import plotly.io as pio

pio.renderers.default = "browser"
```

This setting is useful for local notebook validation and is separate from Gradio's application rendering.

---

## Current Limitations

The visualization layer is intentionally bounded:

- charts exist only for supported analytical routes
- some analytics are text-only
- multi-step workflows use one primary chart
- multiple simultaneous charts are not currently generated
- arbitrary natural-language visualization requests are not supported

For broader project boundaries, see [Limitations](limitations.md).

---

## Summary

The visualization layer follows a simple principle:

```text
deterministic analytical result
        ↓
controlled chart selection
        ↓
Plotly visualization
```

It presents approved healthcare claims analytics visually without introducing a separate source of analytical computation.