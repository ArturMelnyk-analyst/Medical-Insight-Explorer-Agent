from typing import Any

import pandas as pd

from agent.insight_layer import (
    build_analytical_insight,
    build_multi_step_analytical_insight,
    get_multi_step_workflow_name,
)


def format_computed_result(
    computed_result: Any,
    route: str | None = None,
    language: str = "English",
) -> str:
    """
    Convert computed result objects into readable text for the UI.

    Histogram-style outputs should not print every raw value into the response box.
    For those routes, the chart is the main output and the text should remain concise.
    """
    if route == "reimbursement_distribution":
        if language == "Deutsch":
            return (
                "Die Verteilung der Erstattungsbeträge wurde aus nicht fehlenden "
                "`InscClaimAmtReimbursed`-Werten berechnet. Die visuelle Verteilung "
                "ist im Histogramm unten dargestellt."
            )

        return (
            "Reimbursement distribution was computed from non-missing "
            "`InscClaimAmtReimbursed` values. See the histogram below for the visual distribution."
        )

    if isinstance(computed_result, pd.DataFrame):
        return computed_result.to_string(index=False)

    if isinstance(computed_result, list):
        return pd.DataFrame(computed_result).to_string(index=False)

    if isinstance(computed_result, dict):
        return "\n".join(
            f"{key}: {value}" for key, value in computed_result.items()
        )

    return str(computed_result)


def build_english_summary(route: str, computed_result: Any) -> str:
    """
    Build English human-readable summary from deterministic results.
    """
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
        return (
            "Inpatient reimbursement values were grouped by diabetes status. "
            "The visualization compares the reimbursement distributions for "
            "beneficiaries with and without diabetes."
        )

    if route == "reimbursement_distribution":
        return (
            "The inpatient reimbursement distribution was calculated from non-missing "
            "claim reimbursement values."
        )

    return "The selected analytics route was executed using deterministic computation."


def build_german_summary(route: str, computed_result: Any) -> str:
    """
    Build German human-readable summary from deterministic results.
    """
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
        return (
            "Die stationären Erstattungsbeträge wurden nach Diabetes-Status gruppiert. "
            "Die Visualisierung vergleicht die Erstattungsverteilungen für Begünstigte "
            "mit und ohne Diabetes."
        )

    if route == "reimbursement_distribution":
        return (
            "Die Verteilung der stationären Erstattungsbeträge wurde aus nicht fehlenden "
            "Claim-Erstattungswerten berechnet."
        )

    return "Die ausgewählte Analyse-Route wurde mit deterministischer Berechnung ausgeführt."

def describe_analytics_step(
    tool_name: str,
    language: str,
) -> str:
    """
    Return a user-facing description of one executed approved analytics tool.

    Internal registry identifiers are intentionally translated into readable
    descriptions so the response exposes executed analytical operations without
    exposing implementation-oriented tool names.
    """
    if language == "Deutsch":
        descriptions = {
            "top_inpatient_providers": (
                "Stationäre Provider wurden nach Claim-Anzahl gerankt."
            ),
            "top_outpatient_providers": (
                "Ambulante Provider wurden nach Claim-Anzahl gerankt."
            ),
            "inpatient_claims_by_state": (
                "Stationäre Claims wurden nach Bundesstaat gruppiert und gerankt."
            ),
            "outpatient_claims_by_state": (
                "Ambulante Claims wurden nach Bundesstaat gruppiert und gerankt."
            ),
            "inpatient_summary": (
                "Die genehmigte Zusammenfassung der stationären Claims wurde berechnet."
            ),
            "outpatient_summary": (
                "Die genehmigte Zusammenfassung der ambulanten Claims wurde berechnet."
            ),
        }

        return descriptions.get(
            tool_name,
            "Ein genehmigter Analyseschritt wurde ausgeführt.",
        )

    descriptions = {
        "top_inpatient_providers": (
            "Ranked inpatient providers by claim count."
        ),
        "top_outpatient_providers": (
            "Ranked outpatient providers by claim count."
        ),
        "inpatient_claims_by_state": (
            "Grouped and ranked inpatient claims by beneficiary state."
        ),
        "outpatient_claims_by_state": (
            "Grouped and ranked outpatient claims by beneficiary state."
        ),
        "inpatient_summary": (
            "Calculated the approved inpatient claim summary."
        ),
        "outpatient_summary": (
            "Calculated the approved outpatient claim summary."
        ),
    }

    return descriptions.get(
        tool_name,
        "Executed an approved analytics step.",
    )


def get_result_title(
    tool_name: str,
    language: str,
) -> str:
    """
    Return a human-readable title for one computed multi-step result.
    """
    if language == "Deutsch":
        titles = {
            "top_inpatient_providers": "Top stationäre Provider",
            "top_outpatient_providers": "Top ambulante Provider",
            "inpatient_claims_by_state": "Stationäre Claims nach Bundesstaat",
            "outpatient_claims_by_state": "Ambulante Claims nach Bundesstaat",
            "inpatient_summary": "Zusammenfassung stationärer Claims",
            "outpatient_summary": "Zusammenfassung ambulanter Claims",
        }

        return titles.get(
            tool_name,
            "Analyseergebnis",
        )

    titles = {
        "top_inpatient_providers": "Top inpatient providers",
        "top_outpatient_providers": "Top outpatient providers",
        "inpatient_claims_by_state": "Inpatient claims by state",
        "outpatient_claims_by_state": "Outpatient claims by state",
        "inpatient_summary": "Inpatient claim summary",
        "outpatient_summary": "Outpatient claim summary",
    }

    return titles.get(
        tool_name,
        "Analytics result",
    )


def format_multi_step_results(
    tool_results: list[dict[str, Any]],
    language: str,
) -> str:
    """
    Format each already-computed multi-step result using existing result formatting.

    This helper performs presentation only. It does not calculate, aggregate,
    join, or otherwise alter deterministic analytics results.
    """
    sections: list[str] = []

    for item in tool_results:
        tool_name = item["tool"]
        result = item["result"]

        title = get_result_title(
            tool_name=tool_name,
            language=language,
        )

        formatted = format_computed_result(
            computed_result=result,
            route=tool_name,
            language=language,
        )

        sections.append(
            f"{title}:\n{formatted}"
        )

    return "\n\n".join(sections)


def build_multi_step_summary(
    tool_results: list[dict[str, Any]],
    language: str,
) -> str:
    """
    Return a deterministic summary for an approved multi-step workflow.
    """
    workflow_name = get_multi_step_workflow_name(
        tool_results
    )

    if language == "Deutsch":
        if workflow_name == "provider_activity_comparison":
            return (
                "Die Aktivität stationärer und ambulanter Provider wurde mit zwei "
                "genehmigten deterministischen Analyse-Tools verglichen."
            )

        if workflow_name == "claims_by_state_comparison":
            return (
                "Die stationären und ambulanten Claim-Verteilungen nach Bundesstaat "
                "wurden mit zwei genehmigten deterministischen Analyse-Tools verglichen."
            )

        if workflow_name == "claim_summary_comparison":
            return (
                "Die Zusammenfassungen stationärer und ambulanter Claims wurden mit "
                "zwei genehmigten deterministischen Analyse-Tools direkt verglichen."
            )

        return (
            "Mehrere genehmigte deterministische Analyseergebnisse wurden kombiniert."
        )

    if workflow_name == "provider_activity_comparison":
        return (
            "Inpatient and outpatient provider activity were compared using two "
            "approved deterministic analytics tools."
        )

    if workflow_name == "claims_by_state_comparison":
        return (
            "Inpatient and outpatient claim distributions by state were compared "
            "using two approved deterministic analytics tools."
        )

    if workflow_name == "claim_summary_comparison":
        return (
            "Inpatient and outpatient claim summaries were compared side by side "
            "using two approved deterministic analytics tools."
        )

    return (
        "Multiple approved deterministic analytics results were combined."
    )


def format_analytical_steps(
    tool_results: list[dict[str, Any]],
    language: str,
) -> str:
    """
    Format the executed analytical operations as a numbered user-facing list.
    """
    steps: list[str] = []

    for index, item in enumerate(
        tool_results,
        start=1,
    ):
        description = describe_analytics_step(
            tool_name=item["tool"],
            language=language,
        )

        steps.append(
            f"{index}. {description}"
        )

    return "\n".join(steps)


def build_workflow_summary(
    steps_completed: int,
    language: str,
) -> str:
    """
    Return a concise label describing bounded analytics execution.
    """
    if language == "Deutsch":
        if steps_completed <= 0:
            return "Keine genehmigten Analyse-Tools ausgeführt."

        if steps_completed == 1:
            return "Einzelschritt-Analyse — 1 genehmigtes Tool ausgeführt."

        return (
            f"Mehrschritt-Analyse — {steps_completed} genehmigte Tools ausgeführt."
        )

    if steps_completed <= 0:
        return "No approved analytics tools executed."

    if steps_completed == 1:
        return "Single-step analysis — 1 approved tool executed."

    tool_word = "tool" if steps_completed == 1 else "tools"

    return (
        f"Multi-step analysis — {steps_completed} approved {tool_word} executed."
    )


def format_response(
    route: str,
    computed_result: Any,
    language: str,
    tool_results: list[dict[str, Any]] | None = None,
    steps_completed: int = 0,
) -> str:
    """
    Format final user-facing response in English or German.

    Existing single-step output remains unchanged. Multi-step output is enabled
    only when more than one executed result object is available.
    """
    tool_results = tool_results or []

    is_multi_step = (
        len(tool_results) > 1
    )

    if is_multi_step:
        summary = build_multi_step_summary(
            tool_results=tool_results,
            language=language,
        )

        workflow = build_workflow_summary(
            steps_completed=steps_completed,
            language=language,
        )

        steps = format_analytical_steps(
            tool_results=tool_results,
            language=language,
        )

        insight = build_multi_step_analytical_insight(
            tool_results=tool_results,
            language=language,
        )

        formatted_results = format_multi_step_results(
            tool_results=tool_results,
            language=language,
        )

        if language == "Deutsch":
            return (
                f"Zusammenfassung:\n"
                f"{summary}\n\n"
                f"Analytischer Workflow:\n"
                f"{workflow}\n\n"
                f"Analyseschritte:\n"
                f"{steps}\n\n"
                f"Analytische Einordnung:\n"
                f"{insight}\n\n"
                f"Berechnete Ergebnisse:\n"
                f"{formatted_results}\n\n"
                f"Methodischer Hinweis:\n"
                f"Diese Antwort kombiniert deterministische pandas-Berechnungen "
                f"aus genehmigten Healthcare-Analyse-Tools.\n\n"
                f"Sicherheitshinweis:\n"
                f"Dies ist Claims-Analytik und keine Diagnose, Behandlungsberatung, "
                f"Fraud-Feststellung oder klinische Empfehlung."
            )

        return (
            f"Summary:\n"
            f"{summary}\n\n"
            f"Analytical workflow:\n"
            f"{workflow}\n\n"
            f"Analytical steps:\n"
            f"{steps}\n\n"
            f"Analytical insight:\n"
            f"{insight}\n\n"
            f"Computed results:\n"
            f"{formatted_results}\n\n"
            f"Method note:\n"
            f"This response combines deterministic pandas computations "
            f"from approved healthcare analytics tools.\n\n"
            f"Safety note:\n"
            f"This is claims analytics only and does not provide diagnosis, "
            f"treatment advice, fraud determination, or clinical recommendations."
        )

    # Existing single-step behavior is intentionally preserved below.
    formatted_result = format_computed_result(
        computed_result=computed_result,
        route=route,
        language=language,
    )

    insight = build_analytical_insight(
        route=route,
        language=language,
    )

    if language == "Deutsch":
        summary = build_german_summary(route, computed_result)

        return (
            f"Zusammenfassung:\n"
            f"{summary}\n\n"
            f"Analytische Einordnung:\n"
            f"{insight}\n\n"
            f"Berechnetes Ergebnis:\n"
            f"{formatted_result}\n\n"
            f"Methodischer Hinweis:\n"
            f"Diese Antwort basiert auf deterministischen pandas-Berechnungen "
            f"über bereinigte Healthcare-Claims-Daten.\n\n"
            f"Dies ist Claims-Analytik und keine Diagnose, "
            f"Behandlungsberatung oder klinische Empfehlung."
        )

    summary = build_english_summary(route, computed_result)

    return (
        f"Summary:\n"
        f"{summary}\n\n"
        f"Analytical insight:\n"
        f"{insight}\n\n"
        f"Computed result:\n"
        f"{formatted_result}\n\n"
        f"Method note:\n"
        f"This answer is based on deterministic pandas computations "
        f"over cleaned healthcare claims data.\n\n"
        f"This is claims analytics only and does not provide diagnosis, "
        f"treatment advice, or clinical recommendations."
    )

