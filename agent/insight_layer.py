def build_analytical_insight(route: str, language: str) -> str:
    """
    Return cautious deterministic analytical interpretation for supported routes.

    These insights are descriptive and non-causal.
    They do not provide diagnosis, treatment advice, or clinical recommendations.
    """
    if language == "Deutsch":
        insights = {
            "table_shapes": (
                "Diese Übersicht hilft zu prüfen, ob alle erwarteten Tabellen geladen wurden "
                "und ob die Datenbasis für weitere Analysen vollständig wirkt."
            ),
            "inpatient_summary": (
                "Diese Zusammenfassung gibt einen schnellen Überblick über stationäre Claims, "
                "Provider-Abdeckung und Erstattungsvolumen."
            ),
            "outpatient_summary": (
                "Diese Zusammenfassung hilft, ambulante Claims und Provider-Aktivität auf hoher Ebene zu verstehen."
            ),
            "age_summary": (
                "Die Altersübersicht unterstützt die Einordnung der Beneficiary-Population im Datensatz."
            ),
            "top_inpatient_providers": (
                "Eine starke Konzentration auf wenige Provider kann auf operative Schwerpunkte, "
                "Spezialisierung oder hohe Claim-Konzentration hinweisen."
            ),
            "top_outpatient_providers": (
                "Hohe ambulante Claim-Volumina können Provider-Konzentration oder Nutzungsschwerpunkte sichtbar machen."
            ),
            "inpatient_claims_by_state": (
                "Regionale Unterschiede können mit Bevölkerungsgröße, Provider-Dichte oder Nutzungsmustern zusammenhängen."
            ),
            "outpatient_claims_by_state": (
                "Ambulante regionale Muster können Hinweise auf unterschiedliche Nutzung oder Datenabdeckung geben."
            ),
            "diabetes_cost_summary": (
                "Die Erstattungsverteilungen für Beneficiaries mit und ohne Diabetes erscheinen in diesem Datensatz sehr ähnlich. "
                "Dies sollte als Verteilungsvergleich und nicht als kausale Aussage interpretiert werden."
            ),
            "reimbursement_distribution": (
                "Die Verteilung der Erstattungsbeträge kann Schiefe, typische Claim-Höhen und hohe Ausreißer sichtbar machen."
            ),
        }

        return insights.get(
            route,
            "Für diese Frage ist aktuell keine zusätzliche analytische Interpretation verfügbar.",
        )

    insights = {
        "table_shapes": (
            "This overview helps verify whether all expected relational tables loaded correctly "
            "before deeper analysis."
        ),
        "inpatient_summary": (
            "This summary provides a quick view of inpatient claim volume, provider coverage, "
            "and reimbursement scale."
        ),
        "outpatient_summary": (
            "This summary helps understand outpatient claim volume and provider activity at a high level."
        ),
        "age_summary": (
            "The age summary helps contextualize the beneficiary population represented in the dataset."
        ),
        "top_inpatient_providers": (
            "High concentration among a small number of providers may indicate operational hotspots, "
            "specialization patterns, or reimbursement concentration."
        ),
        "top_outpatient_providers": (
            "High outpatient claim volume can highlight provider concentration or utilization hotspots."
        ),
        "inpatient_claims_by_state": (
            "Regional differences may reflect population size, provider density, utilization patterns, "
            "or dataset coverage."
        ),
        "outpatient_claims_by_state": (
            "Outpatient regional patterns may highlight differences in utilization or data coverage."
        ),
        "diabetes_cost_summary": (
            "Reimbursement distributions for beneficiaries with and without diabetes appear highly similar "
            "in this dataset. This should be interpreted as a distribution comparison, not a causal finding."
        ),
        "reimbursement_distribution": (
            "The reimbursement distribution can reveal skew, typical claim amounts, and high-cost outliers."
        ),
    }

    return insights.get(
        route,
        "No additional analytical interpretation is available for this route yet.",
    )


def get_multi_step_workflow_name(
    tool_results: list[dict],
) -> str | None:
    """
    Identify a supported multi-step workflow from executed tool names.

    The executed tool sequence is used as the stable workflow identifier so
    English and German prompts that produce the same approved plan receive the
    same deterministic analytical interpretation.
    """
    tool_names = [
        item.get("tool")
        for item in tool_results
    ]

    if tool_names == [
        "top_inpatient_providers",
        "top_outpatient_providers",
    ]:
        return "provider_activity_comparison"

    if tool_names == [
        "inpatient_claims_by_state",
        "outpatient_claims_by_state",
    ]:
        return "claims_by_state_comparison"

    if tool_names == [
        "inpatient_summary",
        "outpatient_summary",
    ]:
        return "claim_summary_comparison"

    return None


def build_multi_step_analytical_insight(
    tool_results: list[dict],
    language: str,
) -> str:
    """
    Return cautious deterministic interpretation for supported multi-step workflows.

    This helper recognizes only approved compound workflows from the controlled
    analytics planner. It does not inspect DataFrame contents or calculate new
    statistics; it only maps executed approved tool sequences to predefined,
    descriptive, non-causal interpretation.
    """
    workflow_name = get_multi_step_workflow_name(
        tool_results
    )

    if language == "Deutsch":
        if workflow_name == "provider_activity_comparison":
            return (
                "Die stationären und ambulanten Rankings zeigen, bei welchen Providern "
                "sich die Claim-Aktivität innerhalb der jeweiligen Versorgungsbereiche "
                "konzentriert. Unterschiede zwischen den Rankings beschreiben nur "
                "Nutzungsmuster und sind kein Nachweis für Fraud, Provider-Qualität "
                "oder Kausalität."
            )

        if workflow_name == "claims_by_state_comparison":
            return (
                "Die stationären und ambulanten Bundesstaat-Rankings zeigen, wie sich "
                "das Claim-Volumen geografisch zwischen den beiden Versorgungsbereichen "
                "unterscheidet. Unterschiede können mit Nutzung, Bevölkerung, "
                "Provider-Verfügbarkeit oder Datenabdeckung zusammenhängen und sollten "
                "nicht kausal interpretiert werden."
            )

        if workflow_name == "claim_summary_comparison":
            return (
                "Die beiden Zusammenfassungen ermöglichen einen direkten Vergleich "
                "von stationärem und ambulantem Claim-Volumen, Beneficiary-Abdeckung, "
                "Provider-Abdeckung und Erstattungsumfang. Der Vergleich ist "
                "deskriptiv und basiert auf dem verfügbaren Claims-Datensatz."
            )

        return (
            "Mehrere genehmigte Analyse-Tools wurden ausgeführt. "
            "Die Ergebnisse sollten deskriptiv und nicht kausal interpretiert werden."
        )

    if workflow_name == "provider_activity_comparison":
        return (
            "The inpatient and outpatient rankings show where claim activity "
            "is concentrated within each care setting. Differences between the "
            "rankings describe utilization patterns only and should not be "
            "interpreted as evidence of fraud, provider quality, or causality."
        )

    if workflow_name == "claims_by_state_comparison":
        return (
            "The inpatient and outpatient state rankings show how claim volume "
            "varies geographically across the two care settings. Differences may "
            "reflect utilization, population, provider availability, or dataset "
            "coverage and should not be interpreted causally."
        )

    if workflow_name == "claim_summary_comparison":
        return (
            "The two summaries provide a side-by-side view of inpatient and "
            "outpatient claim volume, beneficiary coverage, provider coverage, "
            "and reimbursement scale. The comparison is descriptive and reflects "
            "the available claims dataset."
        )

    return (
        "Multiple approved analytics tools were executed. "
        "The results should be interpreted descriptively and not causally."
    )

