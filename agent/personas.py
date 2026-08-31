PERSONAS = {
    "English": {
        "Hospital Operations Analyst": {
            "description": (
                "Explore provider utilization, claim volume, and reimbursement patterns."
            ),
            "examples": [
                "Compare inpatient and outpatient provider activity",
                "Show inpatient claims by state",
                "Show reimbursement distribution",
            ],
        },
        "Healthcare Fraud Investigator": {
            "description": (
                "Review provider concentration, unusual claim volume, and reimbursement patterns."
            ),
            "examples": [
                "Compare inpatient and outpatient provider activity",
                "Show reimbursement distribution",
                "What is the diabetes cost summary?",
            ],
        },
        "Healthcare Policy Researcher": {
            "description": (
                "Analyze population-level utilization, beneficiary characteristics, and regional trends."
            ),
            "examples": [
                "What is the average beneficiary age?",
                "Compare inpatient and outpatient claims by state",
                "Show outpatient claims by state",
            ],
        },
    },
    "Deutsch": {
        "Analyst für Krankenhausbetrieb": {
            "description": (
                "Untersucht Provider-Auslastung, Claim-Volumen und Erstattungsmuster."
            ),
            "examples": [
                "Vergleiche stationäre und ambulante Provider",
                "Zeige stationäre Claims nach Bundesstaat",
                "Zeige die Verteilung der Erstattungsbeträge",
            ],
        },
        "Prüfer für Healthcare-Fraud": {
            "description": (
                "Analysiert Provider-Konzentration, ungewöhnliches Claim-Volumen und Erstattungsmuster."
            ),
            "examples": [
                "Vergleiche stationäre und ambulante Provider",
                "Zeige die Verteilung der Erstattungsbeträge",
                "Wie sieht die Kostenzusammenfassung für Diabetes aus?",
            ],
        },
        "Healthcare-Policy-Researcher": {
            "description": (
                "Analysiert populationsbezogene Nutzung, Beneficiary-Merkmale und regionale Trends."
            ),
            "examples": [
                "Wie hoch ist das durchschnittliche Alter der Beneficiaries?",
                "Vergleiche stationäre und ambulante Claims nach Bundesstaaten",
                "Zeige ambulante Claims nach Bundesstaat",
            ],
        },
    },
}


def get_persona_choices(language: str) -> list[str]:
    return list(PERSONAS[language].keys())


def get_persona_description(language: str, persona: str) -> str:
    return PERSONAS[language][persona]["description"]


def get_persona_examples(language: str, persona: str) -> list[str]:
    return PERSONAS[language][persona]["examples"]
