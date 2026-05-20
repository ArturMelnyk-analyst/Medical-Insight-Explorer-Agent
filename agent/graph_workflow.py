from __future__ import annotations

from typing import Any, Optional, TypedDict

import plotly.graph_objects as go
from langgraph.graph import END, START, StateGraph

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.chart_router import build_chart_for_route
from agent.language_utils import normalize_question_for_routing
from agent.response_formatter import format_response
from agent.response_generator import ResponseGenerator


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

    This class coordinates the safe deterministic workflow:

    question -> normalize -> route -> compute -> respond -> visualize

    It does not replace the analytics engine and does not allow an LLM
    to directly manipulate healthcare dataframes.
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

    def invoke(
        self,
        question: str,
        language: str = "English",
    ) -> HealthcareGraphState:
        """
        Run the full graph workflow for one user question.
        """
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

        normalized_question = normalize_question_for_routing(
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
        language = state.get("language", "English")
        route = state.get("route", "fallback")
        computed_result = state.get("computed_result")

        text_response = format_response(
            route=route,
            computed_result=computed_result,
            language=language,
        )

        return {
            "text_response": text_response,
        }

    def _generate_chart(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        language = state.get("language", "English")
        route = state.get("route", "fallback")

        chart = build_chart_for_route(
            analytics_engine=self.analytics_engine,
            route=route,
            language=language,
        )

        return {
            "chart": chart,
        }

    def _execute_route(self, route: str) -> Any:
        """
        Execute deterministic analytics based on selected route.
        """
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

        if route == "reimbursement_distribution":
            inpatient = self.analytics_engine.tables["train_inpatient"]

            return inpatient[["InscClaimAmtReimbursed"]].dropna()

        return {
            "message": (
                "This question is not supported by the current analytics routes."
            )
        }