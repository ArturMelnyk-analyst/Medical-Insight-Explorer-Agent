import plotly.graph_objects as go

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.visualization_tools import (
    bar_chart_top_values,
    histogram,
    horizontal_bar_chart,
)


def create_placeholder_chart(language: str) -> go.Figure:
    """
    Return placeholder chart for text-only questions.
    """
    fig = go.Figure()

    fig.update_layout(
        title=(
            "No visualization generated for this question"
            if language == "English"
            else "Keine Visualisierung für diese Frage erstellt"
        ),
        annotations=[
            {
                "text": (
                    "This query is best answered as a text summary."
                    if language == "English"
                    else "Diese Frage eignet sich besser für eine textbasierte Zusammenfassung."
                ),
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
            }
        ],
    )

    return fig


def build_chart_for_route(
    analytics_engine: HealthcareAnalyticsEngine,
    route: str,
    language: str,
) -> go.Figure:
    """
    Build Plotly chart from selected deterministic analytics route.
    """
    if route == "top_outpatient_providers":
        df = analytics_engine.top_providers_by_claim_count(
            claim_type="outpatient",
            top_n=10,
        )

        return horizontal_bar_chart(
            df=df,
            x_col="claim_count",
            y_col="Provider",
            title=(
                "Top 10 Outpatient Providers by Claim Count"
                if language == "English"
                else "Top 10 ambulante Provider nach Claim-Anzahl"
            ),
            x_label="Claim Count" if language == "English" else "Claim-Anzahl",
            y_label="Provider",
        )

    if route == "top_inpatient_providers":
        df = analytics_engine.top_providers_by_claim_count(
            claim_type="inpatient",
            top_n=10,
        )

        return horizontal_bar_chart(
            df=df,
            x_col="claim_count",
            y_col="Provider",
            title=(
                "Top 10 Inpatient Providers by Claim Count"
                if language == "English"
                else "Top 10 stationäre Provider nach Claim-Anzahl"
            ),
            x_label="Claim Count" if language == "English" else "Claim-Anzahl",
            y_label="Provider",
        )

    if route == "inpatient_claims_by_state":
        df = analytics_engine.claim_distribution_by_state(
            claim_type="inpatient",
        ).head(10)

        return bar_chart_top_values(
            df=df,
            x_col="State",
            y_col="claim_count",
            title=(
                "Top 10 States by Inpatient Claim Count"
                if language == "English"
                else "Top 10 Bundesstaaten nach stationärer Claim-Anzahl"
            ),
            x_label="State" if language == "English" else "Bundesstaat",
            y_label="Claim Count" if language == "English" else "Claim-Anzahl",
        )

    if route == "outpatient_claims_by_state":
        df = analytics_engine.claim_distribution_by_state(
            claim_type="outpatient",
        ).head(10)

        return bar_chart_top_values(
            df=df,
            x_col="State",
            y_col="claim_count",
            title=(
                "Top 10 States by Outpatient Claim Count"
                if language == "English"
                else "Top 10 Bundesstaaten nach ambulanter Claim-Anzahl"
            ),
            x_label="State" if language == "English" else "Bundesstaat",
            y_label="Claim Count" if language == "English" else "Claim-Anzahl",
        )

    if route == "diabetes_cost_summary":
        df = analytics_engine.average_inpatient_cost_by_chronic_condition(
            "ChronicCond_Diabetes"
        )

        return bar_chart_top_values(
            df=df,
            x_col="ChronicCond_Diabetes",
            y_col="mean",
            title=(
                "Average Inpatient Reimbursement by Diabetes Indicator"
                if language == "English"
                else "Durchschnittliche stationäre Erstattung nach Diabetes-Indikator"
            ),
            x_label=(
                "Diabetes Indicator"
                if language == "English"
                else "Diabetes-Indikator"
            ),
            y_label=(
                "Average Reimbursement"
                if language == "English"
                else "Durchschnittliche Erstattung"
            ),
        )

    if route == "reimbursement_distribution":
        inpatient = analytics_engine.tables["train_inpatient"]

        return histogram(
            df=inpatient,
            column="InscClaimAmtReimbursed",
            title=(
                "Distribution of Inpatient Claim Reimbursement"
                if language == "English"
                else "Verteilung der stationären Erstattungsbeträge"
            ),
            x_label=(
                "Inpatient Claim Amount Reimbursed"
                if language == "English"
                else "Stationärer Erstattungsbetrag"
            ),
            nbins=40,
        )

    return create_placeholder_chart(language)