from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """
    Validate that required columns exist in a DataFrame.
    """
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required column(s): {missing_columns}")


def bar_chart_top_values(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> go.Figure:
    """
    Create a bar chart for ranked or grouped values.

    Example use cases:
    - Top providers by claim count
    - Claim counts by state
    - Average reimbursement by chronic condition
    """
    validate_columns(df, [x_col, y_col])

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={
            x_col: x_label or x_col,
            y_col: y_label or y_col,
        },
    )

    fig.update_layout(
        xaxis_title=x_label or x_col,
        yaxis_title=y_label or y_col,
        margin=dict(l=40, r=40, t=70, b=40),
    )

    return fig


def horizontal_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> go.Figure:
    """
    Create a horizontal bar chart.

    Useful when category labels are long, such as Provider IDs.
    """
    validate_columns(df, [x_col, y_col])

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        orientation="h",
        title=title,
        labels={
            x_col: x_label or x_col,
            y_col: y_label or y_col,
        },
    )

    fig.update_layout(
        xaxis_title=x_label or x_col,
        yaxis_title=y_label or y_col,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=40, r=40, t=70, b=40),
    )

    return fig


def histogram(
    df: pd.DataFrame,
    column: str,
    title: str,
    x_label: Optional[str] = None,
    nbins: int = 30,
) -> go.Figure:
    """
    Create a histogram for numeric distributions.

    Example use cases:
    - Distribution of inpatient reimbursement
    - Distribution of beneficiary age
    """
    validate_columns(df, [column])

    fig = px.histogram(
        df,
        x=column,
        nbins=nbins,
        title=title,
        labels={column: x_label or column},
    )

    fig.update_layout(
        xaxis_title=x_label or column,
        yaxis_title="Count",
        margin=dict(l=40, r=40, t=70, b=40),
    )

    return fig


def box_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> go.Figure:
    """
    Create a box plot for comparing distributions across groups.

    Example use cases:
    - Reimbursement by chronic condition
    - Claim amount distribution by state
    """
    validate_columns(df, [x_col, y_col])

    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={
            x_col: x_label or x_col,
            y_col: y_label or y_col,
        },
    )

    fig.update_layout(
        xaxis_title=x_label or x_col,
        yaxis_title=y_label or y_col,
        margin=dict(l=40, r=40, t=70, b=40),
    )

    return fig