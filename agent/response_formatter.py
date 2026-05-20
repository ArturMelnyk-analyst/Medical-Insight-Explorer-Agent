from typing import Any

import pandas as pd


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
        return "Inpatient reimbursement amounts were grouped by diabetes indicator."

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
        return "Die stationären Erstattungsbeträge wurden nach Diabetes-Indikator gruppiert."

    if route == "reimbursement_distribution":
        return (
            "Die Verteilung der stationären Erstattungsbeträge wurde aus nicht fehlenden "
            "Claim-Erstattungswerten berechnet."
        )

    return "Die ausgewählte Analyse-Route wurde mit deterministischer Berechnung ausgeführt."


def format_response(
    route: str,
    computed_result: Any,
    language: str,
) -> str:
    """
    Format final user-facing response in English or German.
    """
    formatted_result = format_computed_result(
        computed_result=computed_result,
        route=route,
        language=language,
    )

    if language == "Deutsch":
        summary = build_german_summary(route, computed_result)

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

    summary = build_english_summary(route, computed_result)

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