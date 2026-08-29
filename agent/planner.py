from __future__ import annotations

from typing import TypedDict

from agent.tool_registry import ANALYTICS_TOOLS


MAX_ANALYTICS_STEPS = 3


class AnalyticsPlanStep(TypedDict):
    """
    One approved deterministic analytics step selected by the planner.
    """

    tool: str


class AnalyticsPlan(TypedDict):
    """
    A bounded analytics execution plan.
    """

    steps: list[AnalyticsPlanStep]
    is_supported: bool
    reason: str


class ControlledAnalyticsPlanner:
    """
    Build bounded plans using approved analytics tools only.
    """

    def __init__(self, router) -> None:
        self.router = router

    def plan(self, normalized_question: str) -> AnalyticsPlan:
        """
        Build a controlled analytics plan for one normalized user question.

        Multi-step patterns are checked before the existing router so compound
        questions are not accidentally reduced to a single matching route.
        """
        question_lower = normalized_question.lower()

        causal_terms = {
            "because",
            "cause",
            "caused",
            "causal",
            "weil",
            "verursacht",
            "ursache",
            "kausal",
        }

        if any(term in question_lower for term in causal_terms):
            return {
                "steps": [],
                "is_supported": False,
                "reason": (
                    "The current analytics workflow supports descriptive claims "
                    "analysis but not causal medical conclusions."
                ),
            }

        if (
            "compare" in question_lower
            and "inpatient" in question_lower
            and "outpatient" in question_lower
            and "provider" in question_lower
        ):
            return self._build_plan(
                steps=[
                    {"tool": "top_inpatient_providers"},
                    {"tool": "top_outpatient_providers"},
                ],
                reason=(
                    "Provider activity comparison requires both inpatient "
                    "and outpatient provider rankings."
                ),
            )

        if (
            "compare" in question_lower
            and "inpatient" in question_lower
            and "outpatient" in question_lower
            and "state" in question_lower
        ):
            return self._build_plan(
                steps=[
                    {"tool": "inpatient_claims_by_state"},
                    {"tool": "outpatient_claims_by_state"},
                ],
                reason=(
                    "State-level comparison requires both inpatient and "
                    "outpatient claim distributions."
                ),
            )

        if (
            "compare" in question_lower
            and "inpatient" in question_lower
            and "outpatient" in question_lower
            and (
                "summary" in question_lower
                or "summaries" in question_lower
            )
        ):
            return self._build_plan(
                steps=[
                    {"tool": "inpatient_summary"},
                    {"tool": "outpatient_summary"},
                ],
                reason=(
                    "Claim-summary comparison requires both inpatient "
                    "and outpatient summary tools."
                ),
            )

        single_route = self.router.route(normalized_question)

        if single_route == "fallback":
            return {
                "steps": [],
                "is_supported": False,
                "reason": (
                    "This question is not supported by the current analytics tools."
                ),
            }

        if single_route not in ANALYTICS_TOOLS:
            return {
                "steps": [],
                "is_supported": False,
                "reason": (
                    "The selected analytics route is not registered as an approved tool."
                ),
            }

        return self._build_plan(
            steps=[{"tool": single_route}],
            reason="A single approved analytics tool is sufficient for this question.",
        )

    def _build_plan(
        self,
        steps: list[AnalyticsPlanStep],
        reason: str,
    ) -> AnalyticsPlan:
        """
        Validate and return a bounded analytics plan.
        """
        if len(steps) == 0:
            return {
                "steps": [],
                "is_supported": False,
                "reason": "No approved analytics steps were selected.",
            }

        if len(steps) > MAX_ANALYTICS_STEPS:
            return {
                "steps": [],
                "is_supported": False,
                "reason": (
                    "This request requires more analytical steps than the "
                    "current controlled workflow allows."
                ),
            }

        for step in steps:
            tool_name = step["tool"]

            if tool_name not in ANALYTICS_TOOLS:
                return {
                    "steps": [],
                    "is_supported": False,
                    "reason": (
                        f"Planned analytics tool is not approved: {tool_name}"
                    ),
                }

        return {
            "steps": steps,
            "is_supported": True,
            "reason": reason,
        }
