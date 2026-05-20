def normalize_question_for_routing(question: str, language: str) -> str:
    """
    Normalize supported German prompts into English-style routing phrases.

    This keeps deterministic routing stable while supporting bilingual UX.
    """
    if language != "Deutsch":
        return question

    question_lower = question.lower()

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