from __future__ import annotations

from typing import Any, Optional, TypedDict

import plotly.graph_objects as go
from langgraph.graph import END, START, StateGraph

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.chart_router import build_chart_for_route
from agent.language_utils import normalize_question_for_routing
from agent.planner import (
    MAX_ANALYTICS_STEPS,
    ControlledAnalyticsPlanner,
)
from agent.response_formatter import format_response
from agent.response_generator import ResponseGenerator
from agent.tool_registry import execute_tool


class HealthcareGraphState(TypedDict, total=False):
    """
    Shared state passed between LangGraph workflow nodes.
    """

    question: str
    language: str
    normalized_question: str
    analysis_plan: list[dict[str, str]]
    current_step: int
    tool_results: list[dict[str, Any]]
    steps_completed: int
    plan_supported: bool
    plan_reason: str
    route: str
    computed_result: Any
    text_response: str
    chart: Optional[go.Figure]


class HealthcareGraphWorkflow:
    """
    LangGraph orchestration layer for the Medical Insight Explorer Agent.

    This class coordinates a bounded deterministic workflow:

    question -> normalize -> plan -> execute -> prepare -> respond -> visualize

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
        self.planner = ControlledAnalyticsPlanner(
            router=self.response_generator.router,
        )
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(HealthcareGraphState)

        workflow.add_node("normalize_question", self._normalize_question)
        workflow.add_node("plan_analysis", self._plan_analysis)
        workflow.add_node("execute_next_tool", self._execute_next_tool)
        workflow.add_node("prepare_primary_result", self._prepare_primary_result)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("generate_chart", self._generate_chart)

        workflow.add_edge(START, "normalize_question")
        workflow.add_edge("normalize_question", "plan_analysis")

        workflow.add_conditional_edges(
            "plan_analysis",
            self._route_after_plan,
            {
                "execute": "execute_next_tool",
                "unsupported": "prepare_primary_result",
            },
        )

        workflow.add_conditional_edges(
            "execute_next_tool",
            self._route_after_execution,
            {
                "continue": "execute_next_tool",
                "done": "prepare_primary_result",
            },
        )

        workflow.add_edge("prepare_primary_result", "generate_response")
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

    def _plan_analysis(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        normalized_question = state.get(
            "normalized_question",
            "",
        )

        plan = self.planner.plan(
            normalized_question
        )

        return {
            "analysis_plan": plan["steps"],
            "current_step": 0,
            "tool_results": [],
            "steps_completed": 0,
            "plan_supported": plan["is_supported"],
            "plan_reason": plan["reason"],
        }

    def _route_after_plan(
        self,
        state: HealthcareGraphState,
    ) -> str:
        if not state.get("plan_supported", False):
            return "unsupported"

        return "execute"

    def _execute_next_tool(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        analysis_plan = state.get(
            "analysis_plan",
            [],
        )

        current_step = state.get(
            "current_step",
            0,
        )

        tool_results = list(
            state.get("tool_results", [])
        )

        if current_step >= len(analysis_plan):
            return {}

        step = analysis_plan[current_step]
        tool_name = step["tool"]

        result = execute_tool(
            analytics_engine=self.analytics_engine,
            tool_name=tool_name,
        )

        tool_results.append(
            {
                "tool": tool_name,
                "result": result,
            }
        )

        return {
            "tool_results": tool_results,
            "current_step": current_step + 1,
            "steps_completed": state.get(
                "steps_completed",
                0,
            ) + 1,
        }

    def _route_after_execution(
        self,
        state: HealthcareGraphState,
    ) -> str:
        analysis_plan = state.get(
            "analysis_plan",
            [],
        )

        current_step = state.get(
            "current_step",
            0,
        )

        steps_completed = state.get(
            "steps_completed",
            0,
        )

        if steps_completed >= MAX_ANALYTICS_STEPS:
            return "done"

        if current_step < len(analysis_plan):
            return "continue"

        return "done"

    def _prepare_primary_result(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        if not state.get(
            "plan_supported",
            False,
        ):
            return {
                "route": "fallback",
                "computed_result": {
                    "message": state.get(
                        "plan_reason",
                        "This question is not supported.",
                    )
                },
            }

        tool_results = state.get(
            "tool_results",
            [],
        )

        if not tool_results:
            return {
                "route": "fallback",
                "computed_result": {
                    "message": (
                        "No approved analytics result was produced."
                    )
                },
            }

        primary_result = tool_results[0]

        return {
            "route": primary_result["tool"],
            "computed_result": primary_result["result"],
        }

    def _generate_response(
        self,
        state: HealthcareGraphState,
    ) -> HealthcareGraphState:
        language = state.get("language", "English")
        route = state.get("route", "fallback")
        computed_result = state.get("computed_result")

        tool_results = state.get(
            "tool_results",
            [],
        )

        steps_completed = state.get(
            "steps_completed",
            0,
        )

        text_response = format_response(
            route=route,
            computed_result=computed_result,
            language=language,
            tool_results=tool_results,
            steps_completed=steps_completed,
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
