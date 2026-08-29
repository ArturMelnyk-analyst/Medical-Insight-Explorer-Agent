from __future__ import annotations

from typing import Any, Dict, TypedDict

import pandas as pd

from agent.analytics_engine import HealthcareAnalyticsEngine


class AnalyticsToolSpec(TypedDict, total=False):
    """
    Metadata describing one approved deterministic analytics capability.
    """

    name: str
    description: str
    category: str
    method_name: str
    returns: str
    supports_chart: bool
    fixed_kwargs: Dict[str, Any]
    row_limit: int


class UnknownAnalyticsToolError(ValueError):
    """
    Raised when an unregistered analytics tool is requested.
    """


ANALYTICS_TOOLS: Dict[str, AnalyticsToolSpec] = {
    "table_shapes": {
        "name": "table_shapes",
        "description": (
            "Summarize loaded healthcare tables by row and column count."
        ),
        "category": "data_validation",
        "method_name": "get_table_shapes",
        "returns": "pandas.DataFrame",
        "supports_chart": False,
        "fixed_kwargs": {},
    },

    "inpatient_summary": {
        "name": "inpatient_summary",
        "description": (
            "Summarize inpatient claim volume, beneficiaries, providers, "
            "and reimbursement."
        ),
        "category": "claims_summary",
        "method_name": "inpatient_claim_summary",
        "returns": "dict",
        "supports_chart": False,
        "fixed_kwargs": {},
    },

    "outpatient_summary": {
        "name": "outpatient_summary",
        "description": (
            "Summarize outpatient claim volume, beneficiaries, providers, "
            "and reimbursement."
        ),
        "category": "claims_summary",
        "method_name": "outpatient_claim_summary",
        "returns": "dict",
        "supports_chart": False,
        "fixed_kwargs": {},
    },

    "age_summary": {
        "name": "age_summary",
        "description": (
            "Summarize beneficiary age characteristics."
        ),
        "category": "beneficiary_demographics",
        "method_name": "beneficiary_age_summary",
        "returns": "dict",
        "supports_chart": False,
        "fixed_kwargs": {},
    },

    "top_inpatient_providers": {
        "name": "top_inpatient_providers",
        "description": (
            "Rank the top inpatient providers by claim count."
        ),
        "category": "provider_utilization",
        "method_name": "top_providers_by_claim_count",
        "returns": "pandas.DataFrame",
        "supports_chart": True,
        "fixed_kwargs": {
            "claim_type": "inpatient",
            "top_n": 10,
        },
    },

    "top_outpatient_providers": {
        "name": "top_outpatient_providers",
        "description": (
            "Rank the top outpatient providers by claim count."
        ),
        "category": "provider_utilization",
        "method_name": "top_providers_by_claim_count",
        "returns": "pandas.DataFrame",
        "supports_chart": True,
        "fixed_kwargs": {
            "claim_type": "outpatient",
            "top_n": 10,
        },
    },

    "inpatient_claims_by_state": {
        "name": "inpatient_claims_by_state",
        "description": (
            "Rank states by inpatient claim count."
        ),
        "category": "geographic_analysis",
        "method_name": "claim_distribution_by_state",
        "returns": "pandas.DataFrame",
        "supports_chart": True,
        "fixed_kwargs": {
            "claim_type": "inpatient",
        },
        "row_limit": 10,
    },

    "outpatient_claims_by_state": {
        "name": "outpatient_claims_by_state",
        "description": (
            "Rank states by outpatient claim count."
        ),
        "category": "geographic_analysis",
        "method_name": "claim_distribution_by_state",
        "returns": "pandas.DataFrame",
        "supports_chart": True,
        "fixed_kwargs": {
            "claim_type": "outpatient",
        },
        "row_limit": 10,
    },

    "diabetes_cost_summary": {
        "name": "diabetes_cost_summary",
        "description": (
            "Compare inpatient reimbursement statistics by diabetes status."
        ),
        "category": "chronic_condition_analysis",
        "method_name": "average_inpatient_cost_by_chronic_condition",
        "returns": "pandas.DataFrame",
        "supports_chart": True,
        "fixed_kwargs": {
            "condition_col": "ChronicCond_Diabetes",
        },
    },

    "reimbursement_distribution": {
        "name": "reimbursement_distribution",
        "description": (
            "Return non-missing inpatient reimbursement values "
            "for distribution analysis."
        ),
        "category": "reimbursement_analysis",
        "method_name": "inpatient_reimbursement_distribution",
        "returns": "pandas.DataFrame",
        "supports_chart": True,
        "fixed_kwargs": {},
    },
}


def list_tools() -> list[str]:
    """
    Return the names of all approved analytics tools.
    """
    return list(ANALYTICS_TOOLS.keys())


def get_tool(tool_name: str) -> AnalyticsToolSpec:
    """
    Return metadata for one approved analytics tool.

    Raises:
        UnknownAnalyticsToolError:
            If the requested tool is not registered.
    """
    if tool_name not in ANALYTICS_TOOLS:
        raise UnknownAnalyticsToolError(
            f"Analytics tool is not approved: {tool_name}"
        )

    return ANALYTICS_TOOLS[tool_name]


def execute_tool(
    analytics_engine: HealthcareAnalyticsEngine,
    tool_name: str,
) -> Any:
    """
    Execute one explicitly approved deterministic analytics tool.
    """
    tool = get_tool(tool_name)

    method_name = tool["method_name"]

    method = getattr(
        analytics_engine,
        method_name,
        None,
    )

    if method is None or not callable(method):
        raise RuntimeError(
            f"Registered analytics method is unavailable: {method_name}"
        )

    fixed_kwargs = tool.get("fixed_kwargs", {})

    result = method(**fixed_kwargs)

    row_limit = tool.get("row_limit")

    if row_limit is not None:
        if not isinstance(result, pd.DataFrame):
            raise TypeError(
                f"Tool '{tool_name}' expected a DataFrame before row limiting."
            )

        result = (
            result
            .head(row_limit)
            .reset_index(drop=True)
        )

    return result
