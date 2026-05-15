import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.prompt_templates import SYSTEM_PROMPT, build_explanation_prompt


class QueryRouter:
    """
    Simple rule-based router for mapping user questions to controlled analytics functions.

    This router intentionally avoids giving the LLM direct access to dataframes.
    """

    def route(self, question: str) -> str:
        question_lower = question.lower()

        if "shape" in question_lower or "tables" in question_lower:
            return "table_shapes"

        if "inpatient" in question_lower and "summary" in question_lower:
            return "inpatient_summary"

        if "outpatient" in question_lower and "summary" in question_lower:
            return "outpatient_summary"

        if "age" in question_lower:
            return "age_summary"

        if "top" in question_lower and "provider" in question_lower and "outpatient" in question_lower:
            return "top_outpatient_providers"

        if "top" in question_lower and "provider" in question_lower:
            return "top_inpatient_providers"

        if "state" in question_lower and "outpatient" in question_lower:
            return "outpatient_claims_by_state"

        if "state" in question_lower:
            return "inpatient_claims_by_state"

        if "diabetes" in question_lower or "diabetic" in question_lower:
            return "diabetes_cost_summary"

        return "fallback"


class ResponseGenerator:
    """
    Generates grounded responses by combining:
    - rule-based routing
    - deterministic analytics functions
    - optional LLM explanation

    The LLM never receives direct dataframe access.
    """

    def __init__(
        self,
        analytics_engine: HealthcareAnalyticsEngine,
        use_llm: bool = False,
    ) -> None:
        self.analytics_engine = analytics_engine
        self.router = QueryRouter()
        self.use_llm = use_llm

        load_dotenv()

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Route a question, compute a result, and return a grounded explanation.
        """
        route_name = self.router.route(question)
        computed_result = self._run_route(route_name)

        explanation = self._generate_explanation(
            question=question,
            route_name=route_name,
            computed_result=computed_result,
        )

        return {
            "question": question,
            "route": route_name,
            "computed_result": computed_result,
            "explanation": explanation,
        }

    def _run_route(self, route_name: str) -> Any:
        """
        Execute a controlled analytics route.
        """
        if route_name == "table_shapes":
            return self.analytics_engine.get_table_shapes().to_dict(orient="records")

        if route_name == "inpatient_summary":
            return self.analytics_engine.inpatient_claim_summary()

        if route_name == "outpatient_summary":
            return self.analytics_engine.outpatient_claim_summary()

        if route_name == "age_summary":
            return self.analytics_engine.beneficiary_age_summary()

        if route_name == "top_inpatient_providers":
            return self.analytics_engine.top_providers_by_claim_count(
                claim_type="inpatient",
                top_n=10,
            ).to_dict(orient="records")

        if route_name == "top_outpatient_providers":
            return self.analytics_engine.top_providers_by_claim_count(
                claim_type="outpatient",
                top_n=10,
            ).to_dict(orient="records")

        if route_name == "inpatient_claims_by_state":
            return self.analytics_engine.claim_distribution_by_state(
                claim_type="inpatient",
            ).head(10).to_dict(orient="records")

        if route_name == "outpatient_claims_by_state":
            return self.analytics_engine.claim_distribution_by_state(
                claim_type="outpatient",
            ).head(10).to_dict(orient="records")

        if route_name == "diabetes_cost_summary":
            return self.analytics_engine.average_inpatient_cost_by_chronic_condition(
                "ChronicCond_Diabetes"
            ).to_dict(orient="records")

        return {
            "message": (
                "This question is not supported by the current analytics routes. "
                "Try asking about table shapes, inpatient summary, outpatient summary, "
                "age statistics, top providers, state claim counts, or diabetes cost summary."
            )
        }

    def _generate_explanation(
        self,
        question: str,
        route_name: str,
        computed_result: Any,
    ) -> str:
        """
        Generate explanation using either:
        - deterministic fallback text
        - optional OpenAI call if enabled and configured
        """
        if self.use_llm and self.openai_api_key:
            return self._generate_llm_explanation(
                question=question,
                route_name=route_name,
                computed_result=computed_result,
            )

        return self._generate_fallback_explanation(
            route_name=route_name,
            computed_result=computed_result,
        )

    def _generate_fallback_explanation(
        self,
        route_name: str,
        computed_result: Any,
    ) -> str:
        """
        Deterministic explanation used when no LLM API key is configured.
        """
        if route_name == "fallback":
            return computed_result["message"]

        return (
            f"Route selected: {route_name}. "
            "The result was computed using deterministic pandas-based analytics. "
            f"Computed output: {computed_result}"
        )

    def _generate_llm_explanation(
        self,
        question: str,
        route_name: str,
        computed_result: Any,
    ) -> str:
        """
        Optional OpenAI-based explanation layer.
        """
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.openai_api_key)

            user_prompt = build_explanation_prompt(
                question=question,
                route_name=route_name,
                computed_result=computed_result,
            )

            response = client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )

            return response.choices[0].message.content

        except Exception as error:
            return (
                "LLM explanation was unavailable, so a deterministic fallback was used. "
                f"Route selected: {route_name}. "
                f"Computed output: {computed_result}. "
                f"LLM error: {error}"
            )