def normalize_question_for_routing(question: str, language: str) -> str:
    """
    Normalize supported German prompts into English-style routing phrases.

    This keeps deterministic routing stable while supporting bilingual UX.
    """
    if language != "Deutsch":
        return question

    question_lower = question.lower()

    # Preserve German causal wording so the planner can reject causal questions
    # before broad one-step normalization removes the causal signal.
    german_causal_terms = {
        "weil",
        "verursacht",
        "ursache",
        "kausal",
    }

    if any(term in question_lower for term in german_causal_terms):
        return question

    comparison_requested = (
        "vergleiche" in question_lower
        or "vergleich" in question_lower
    )

    # Compound comparison routes must be checked before broad single-route rules.
    if (
        comparison_requested
        and (
            "stationär" in question_lower
            or "stationären" in question_lower
            or "stationärer" in question_lower
        )
        and (
            "ambulant" in question_lower
            or "ambulanten" in question_lower
            or "ambulanter" in question_lower
        )
        and "provider" in question_lower
    ):
        return "Compare inpatient and outpatient provider activity"

    if (
        comparison_requested
        and (
            "stationär" in question_lower
            or "stationäre" in question_lower
            or "stationären" in question_lower
        )
        and (
            "ambulant" in question_lower
            or "ambulante" in question_lower
            or "ambulanten" in question_lower
        )
        and (
            "bundesstaat" in question_lower
            or "bundesstaaten" in question_lower
        )
    ):
        return "Compare inpatient and outpatient claims by state"

    if (
        comparison_requested
        and (
            "stationär" in question_lower
            or "stationäre" in question_lower
            or "stationären" in question_lower
        )
        and (
            "ambulant" in question_lower
            or "ambulante" in question_lower
            or "ambulanten" in question_lower
        )
        and (
            "zusammenfassung" in question_lower
            or "zusammenfassungen" in question_lower
        )
    ):
        return "Compare inpatient and outpatient claim summaries"

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
