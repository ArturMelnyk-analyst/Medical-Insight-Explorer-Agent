from __future__ import annotations

from typing import Any, Optional, TypedDict

import pandas as pd
import plotly.graph_objects as go
from langgraph.graph import END, START, StateGraph

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.response_generator import ResponseGenerator
from agent.visualization_tools import (
    bar_chart_top_values,
    histogram,
    horizontal_bar_chart,
)


class HealthcareGraphState(TypedDict, total=False):
    """
    Shared state passed between LangGraph workflow nodes.
    """

    question: str
    language: str
    normalized_question: str
    route: str
    computed_result: Any
    text_response: str
    chart: Optional[go.Figure]


class HealthcareGraphWorkflow:
    """
    LangGraph orchestration layer for the Medical Insight Explorer Agent.

    This class does not replace deterministic analytics.
    It makes the existing safe workflow explicit:

    question -> normalize -> route -> compute -> respond -> visualize
    """

    def __init__(
        self,
        analytics_engine: HealthcareAnalyticsEngine,
        response_generator: ResponseGenerator,
    ) -> None:
        self.analytics_engine = analytics_engine
        self.response_generator = response_generator
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(HealthcareGraphState)

        workflow.add_node("normalize_question", self._normalize_question)
        workflow.add_node("route_question", self._route_question)
        workflow.add_node("run_analytics", self._run_analytics)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("generate_chart", self._generate_chart)

        workflow.add_edge(START, "normalize_question")
        workflow.add_edge("normalize_question", "route_question")
        workflow.add_edge("route_question", "run_analytics")
        workflow.add_edge("run_analytics", "generate_response")
        workflow.add_edge("generate_response", "generate_chart")
        workflow.add_edge("generate_chart", END)

        return workflow.compile()

    def invoke(self, question: str, language: str = "English") -> HealthcareGraphState:
        initial_state: HealthcareGraphState = {
            "question": question,
            "language": language,
        }

        return self.graph.invoke(initial_state)

    def _normalize_question(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        question = state.get("question", "")
        language = state.get("language", "English")

        normalized_question = self._normalize_german_question(
            question=question,
            language=language,
        )

        return {
            "normalized_question": normalized_question,
        }

    def _route_question(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        normalized_question = state.get("normalized_question", "")

        route = self.response_generator.router.route(normalized_question)

        return {
            "route": route,
        }

    def _run_analytics(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        route = state.get("route", "fallback")

        computed_result = self._execute_route(route)

        return {
            "computed_result": computed_result,
        }

    def _generate_response(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        question = state.get("normalized_question", "")
        language = state.get("language", "English")
        route = state.get("route", "fallback")
        computed_result = state.get("computed_result")

        text_response = self._format_response(
            question=question,
            language=language,
            route=route,
            computed_result=computed_result,
        )

        return {
            "text_response": text_response,
        }

    def _generate_chart(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        question = state.get("normalized_question", "")
        language = state.get("language", "English")

        chart = self._build_chart(
            question=question,
            language=language,
        )

        return {
            "chart": chart,
        }

    def _execute_route(self, route: str) -> Any:
        if route == "table_shapes":
            return self.analytics_engine.get_table_shapes()

        if route == "inpatient_summary":
            return self.analytics_engine.inpatient_claim_summary()

        if route == "outpatient_summary":
            return self.analytics_engine.outpatient_claim_summary()

        if route == "age_summary":
            return self.analytics_engine.beneficiary_age_summary()

        if route == "top_inpatient_providers":
            return self.analytics_engine.top_providers_by_claim_count(
                claim_type="inpatient",
                top_n=10,
            )

        if route == "top_outpatient_providers":
            return self.analytics_engine.top_providers_by_claim_count(
                claim_type="outpatient",
                top_n=10,
            )

        if route == "inpatient_claims_by_state":
            return self.analytics_engine.claim_distribution_by_state(
                claim_type="inpatient",
            ).head(10)

        if route == "outpatient_claims_by_state":
            return self.analytics_engine.claim_distribution_by_state(
                claim_type="outpatient",
            ).head(10)

        if route == "diabetes_cost_summary":
            return self.analytics_engine.average_inpatient_cost_by_chronic_condition(
                "ChronicCond_Diabetes"
            )

        return {
            "message": (
                "This question is not supported by the current analytics routes."
            )
        }

    def _format_response(
        self,
        question: str,
        language: str,
        route: str,
        computed_result: Any,
    ) -> str:
        formatted_result = self._format_computed_result(computed_result)

        if language == "Deutsch":
            summary = self._build_german_summary(route, computed_result)

            return (
                f"Zusammenfassung:\n"
                f"{summary}\n\n"
                f"Berechnetes Ergebnis:\n"
                f"{formatted_result}\n\n"
                f"Methodischer Hinweis:\n"
                f"Diese Antwort basiert auf deterministischen pandas-Berechnungen "
                f"über bereinigte Healthcare-Claims-Daten.\n\n"
                f"Dies ist Claims-Analytik und keine Diagnose, "
                f"Behandlungsberatung oder klinische Empfehlung."
            )

        summary = self._build_english_summary(route, computed_result)

        return (
            f"Summary:\n"
            f"{summary}\n\n"
            f"Computed result:\n"
            f"{formatted_result}\n\n"
            f"Method note:\n"
            f"This answer is based on deterministic pandas computations "
            f"over cleaned healthcare claims data.\n\n"
            f"This is claims analytics only and does not provide diagnosis, "
            f"treatment advice, or clinical recommendations."
        )

    def _format_computed_result(self, computed_result: Any) -> str:
        if isinstance(computed_result, pd.DataFrame):
            return computed_result.to_string(index=False)

        if isinstance(computed_result, list):
            return pd.DataFrame(computed_result).to_string(index=False)

        if isinstance(computed_result, dict):
            return "\n".join(
                f"{key}: {value}" for key, value in computed_result.items()
            )

        return str(computed_result)

    def _build_english_summary(
        self,
        route: str,
        computed_result: Any,
    ) -> str:
        if route == "table_shapes":
            return "All loaded tables were summarized by row and column count."

        if route == "inpatient_summary" and isinstance(computed_result, dict):
            return (
                f"The inpatient claims table contains "
                f"{computed_result.get('total_claims')} claims for "
                f"{computed_result.get('unique_beneficiaries')} unique beneficiaries."
            )

        if route == "outpatient_summary" and isinstance(computed_result, dict):
            return (
                f"The outpatient claims table contains "
                f"{computed_result.get('total_claims')} claims for "
                f"{computed_result.get('unique_beneficiaries')} unique beneficiaries."
            )

        if route == "age_summary" and isinstance(computed_result, dict):
            mean_age = computed_result.get("mean_age")
            if isinstance(mean_age, (int, float)):
                return f"The average beneficiary age is approximately {mean_age:.2f} years."

        if route == "top_inpatient_providers":
            return "Provider activity was ranked using inpatient claim volume."

        if route == "top_outpatient_providers":
            return "Provider activity was ranked using outpatient claim volume."

        if route in {"inpatient_claims_by_state", "outpatient_claims_by_state"}:
            return "Claims were grouped by state and ranked by claim count."

        if route == "diabetes_cost_summary":
            return "Inpatient reimbursement amounts were grouped by diabetes indicator."

        return "The selected analytics route was executed using deterministic computation."

    def _build_german_summary(
        self,
        route: str,
        computed_result: Any,
    ) -> str:
        if route == "table_shapes":
            return "Alle geladenen Tabellen wurden nach Zeilen- und Spaltenanzahl zusammengefasst."

        if route == "inpatient_summary" and isinstance(computed_result, dict):
            return (
                f"Die stationären Claims umfassen "
                f"{computed_result.get('total_claims')} Claims für "
                f"{computed_result.get('unique_beneficiaries')} eindeutige Beneficiaries."
            )

        if route == "outpatient_summary" and isinstance(computed_result, dict):
            return (
                f"Die ambulanten Claims umfassen "
                f"{computed_result.get('total_claims')} Claims für "
                f"{computed_result.get('unique_beneficiaries')} eindeutige Beneficiaries."
            )

        if route == "age_summary" and isinstance(computed_result, dict):
            mean_age = computed_result.get("mean_age")
            if isinstance(mean_age, (int, float)):
                return f"Das durchschnittliche Beneficiary-Alter beträgt ungefähr {mean_age:.2f} Jahre."

        if route == "top_inpatient_providers":
            return "Die Provider-Aktivität wurde anhand des stationären Claim-Volumens bewertet."

        if route == "top_outpatient_providers":
            return "Die Provider-Aktivität wurde anhand des ambulanten Claim-Volumens bewertet."

        if route in {"inpatient_claims_by_state", "outpatient_claims_by_state"}:
            return "Die Claims wurden nach Bundesstaat gruppiert und nach Claim-Anzahl sortiert."

        if route == "diabetes_cost_summary":
            return "Die stationären Erstattungsbeträge wurden nach Diabetes-Indikator gruppiert."

        return "Die ausgewählte Analyse-Route wurde mit deterministischer Berechnung ausgeführt."

    def _build_chart(
        self,
        question: str,
        language: str,
    ) -> go.Figure:
        q = question.lower() if question else ""

        if "outpatient" in q and "provider" in q:
            df = self.analytics_engine.top_providers_by_claim_count(
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

        if "provider" in q:
            df = self.analytics_engine.top_providers_by_claim_count(
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

        if "state" in q:
            df = self.analytics_engine.claim_distribution_by_state(
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

        if "diabetes" in q:
            df = self.analytics_engine.average_inpatient_cost_by_chronic_condition(
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

        if "reimbursement" in q or "cost" in q or "claim amount" in q:
            inpatient = self.analytics_engine.tables["train_inpatient"]

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

    def _normalize_german_question(
        self,
        question: str,
        language: str,
    ) -> str:
        if language != "Deutsch":
            return question

        question_lower = question.lower()

        if "form aller tabellen" in question_lower or "tabellen" in question_lower:
            return "Show me the shape of all tables"

        if "stationären claims" in question_lower and "zusammenfassung" in question_lower:
            return "Give me an inpatient summary"

        if "ambulanten claims" in question_lower and "zusammenfassung" in question_lower:
            return "Give me an outpatient summary"

        if "alter" in question_lower:
            return "What is the average beneficiary age?"

        if "stationären provider" in question_lower or "stationäre provider" in question_lower:
            return "Show top inpatient providers"

        if "ambulanten provider" in question_lower or "ambulante provider" in question_lower:
            return "Show top outpatient providers"

        if "bundesstaat" in question_lower or "claims nach" in question_lower:
            return "Show inpatient claims by state"

        if "diabetes" in question_lower:
            return "What is the diabetes cost summary?"

        if "erstattungsbeträge" in question_lower or "erstattung" in question_lower:
            return "Show reimbursement distribution"

        return question