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