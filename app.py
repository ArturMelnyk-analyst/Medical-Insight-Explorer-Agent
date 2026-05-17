from pathlib import Path
from typing import Any

import gradio as gr
import pandas as pd
import plotly.graph_objects as go

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.data_loader import HealthcareDataLoader
from agent.response_generator import ResponseGenerator
from agent.visualization_tools import (
    bar_chart_top_values,
    histogram,
    horizontal_bar_chart,
)


PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample"


LANGUAGE_TEXT = {
    "English": {
        "title": "Medical Insight Explorer Agent",
        "subtitle": "Conversational analytics over cleaned Medicare healthcare claims data.",
        "method_note": (
            "This app uses deterministic pandas-based analytics functions first, "
            "then returns grounded explanations and optional visual outputs."
        ),
        "question_label": "Ask a healthcare analytics question",
        "question_placeholder": "Example: Show top inpatient providers",
        "run_button": "Run analysis",
        "clear_button": "Clear",
        "response_label": "Agent response",
        "chart_label": "Visualization output",
        "no_visual_title": "No visualization generated for this question",
        "no_visual_text": "This query is best answered as a text summary.",
        "empty_question": "Please enter a healthcare analytics question.",
        "route_label": "Selected analysis route",
        "summary_label": "Summary",
        "details_label": "Computed result",
        "method_label": "Method note",
        "method_footer": (
            "This answer is based on deterministic pandas computations over cleaned healthcare claims data."
        ),
        "safety_footer": (
            "This is claims analytics only and does not provide diagnosis, treatment advice, or clinical recommendations."
        ),
        "examples": [
            "Show me the shape of all tables",
            "Give me an inpatient summary",
            "Give me an outpatient summary",
            "What is the average beneficiary age?",
            "Show top inpatient providers",
            "Show top outpatient providers",
            "Show inpatient claims by state",
            "What is the diabetes cost summary?",
            "Show reimbursement distribution",
        ],
    },
    "Deutsch": {
        "title": "Medical Insight Explorer Agent",
        "subtitle": "Konversationelle Analyse bereinigter Medicare-Healthcare-Claims-Daten.",
        "method_note": (
            "Diese App verwendet zuerst deterministische pandas-basierte Analysefunktionen "
            "und gibt anschließend erklärende, datenbasierte Antworten sowie optionale Visualisierungen zurück."
        ),
        "question_label": "Frage zur Healthcare-Analyse",
        "question_placeholder": "Beispiel: Zeige die wichtigsten stationären Provider",
        "run_button": "Analyse ausführen",
        "clear_button": "Zurücksetzen",
        "response_label": "Antwort des Agenten",
        "chart_label": "Visualisierung",
        "no_visual_title": "Keine Visualisierung für diese Frage erstellt",
        "no_visual_text": "Diese Frage eignet sich besser für eine textbasierte Zusammenfassung.",
        "empty_question": "Bitte geben Sie eine Frage zur Healthcare-Analyse ein.",
        "route_label": "Ausgewählte Analyse-Route",
        "summary_label": "Zusammenfassung",
        "details_label": "Berechnetes Ergebnis",
        "method_label": "Methodischer Hinweis",
        "method_footer": (
            "Diese Antwort basiert auf deterministischen pandas-Berechnungen über bereinigte Healthcare-Claims-Daten."
        ),
        "safety_footer": (
            "Dies ist Claims-Analytik und keine Diagnose, Behandlungsberatung oder klinische Empfehlung."
        ),
        "examples": [
            "Zeige die Form aller Tabellen",
            "Gib mir eine Zusammenfassung der stationären Claims",
            "Gib mir eine Zusammenfassung der ambulanten Claims",
            "Wie hoch ist das durchschnittliche Alter der Beneficiaries?",
            "Zeige die wichtigsten stationären Provider",
            "Zeige die wichtigsten ambulanten Provider",
            "Zeige stationäre Claims nach Bundesstaat",
            "Wie sieht die Kostenzusammenfassung für Diabetes aus?",
            "Zeige die Verteilung der Erstattungsbeträge",
        ],
    },
}


def resolve_data_dir() -> Path:
    """
    Prefer full local processed data.
    Fall back to sample data for lightweight demo environments.
    """
    required_file = "train_beneficiary_clean.parquet"

    if (PROCESSED_DATA_DIR / required_file).exists():
        return PROCESSED_DATA_DIR

    if (SAMPLE_DATA_DIR / required_file).exists():
        return SAMPLE_DATA_DIR

    raise FileNotFoundError(
        "No healthcare Parquet data found. "
        "Place cleaned Parquet files in data/processed/ or sample Parquet files in data/sample/."
    )


def initialize_components() -> tuple[HealthcareAnalyticsEngine, ResponseGenerator]:
    """
    Load healthcare tables and initialize analytics + response components.
    """
    data_dir = resolve_data_dir()

    loader = HealthcareDataLoader(data_dir=str(data_dir))
    tables = loader.load_tables()

    engine = HealthcareAnalyticsEngine(tables)
    response_generator = ResponseGenerator(
        analytics_engine=engine,
        use_llm=False,
    )

    return engine, response_generator


ENGINE, RESPONSE_GENERATOR = initialize_components()


def normalize_question_for_routing(question: str, language: str) -> str:
    """
    Convert supported German UI examples into English-style routing phrases.

    This keeps the backend router simple while allowing German-facing UX.
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


def format_computed_result(result: Any) -> str:
    """
    Convert computed result objects into readable text for the UI.
    """
    if isinstance(result, pd.DataFrame):
        return result.to_string(index=False)

    if isinstance(result, list):
        return pd.DataFrame(result).to_string(index=False)

    if isinstance(result, dict):
        return "\n".join(f"{key}: {value}" for key, value in result.items())

    return str(result)


def build_human_summary(route: str, computed_result: Any, language: str) -> str:
    """
    Create cleaner human-readable summaries for the UI instead of showing raw dictionaries only.
    """
    is_german = language == "Deutsch"

    if route == "top_inpatient_providers" and isinstance(computed_result, list):
        top_provider = computed_result[0]["Provider"]
        top_count = computed_result[0]["claim_count"]

        return (
            f"Die Provider-Aktivität wurde anhand des stationären Claim-Volumens bewertet. "
            f"Der führende Provider ist {top_provider} mit {top_count} Claims. "
            f"Eine höhere Claim-Anzahl kann auf ein größeres Patientenaufkommen oder ein breiteres Leistungsangebot hinweisen."
        )

        return (
    	    f"Provider activity was ranked using inpatient claim volume. "
            f"The leading provider is {top_provider} with {top_count} claims. "
            f"Higher claim counts may indicate larger patient throughput or broader service coverage."
	)

    if route == "top_outpatient_providers" and isinstance(computed_result, list):
        top_provider = computed_result[0]["Provider"]
        top_count = computed_result[0]["claim_count"]

        if is_german:
            return (
                f"Die wichtigsten ambulanten Provider wurden nach Claim-Anzahl identifiziert. "
                f"Der führende Provider ist {top_provider} mit {top_count} Claims."
            )

        return (
            f"The top outpatient providers were identified by claim count. "
            f"The leading provider is {top_provider} with {top_count} claims."
        )

    if route == "age_summary" and isinstance(computed_result, dict):
        mean_age = computed_result.get("mean_age")

        if isinstance(mean_age, (int, float)):
            if is_german:
                return f"Das durchschnittliche Beneficiary-Alter beträgt ungefähr {mean_age:.2f} Jahre."

            return f"The average beneficiary age is approximately {mean_age:.2f} years."

    if route == "inpatient_summary" and isinstance(computed_result, dict):
        total_claims = computed_result.get("total_claims")
        unique_beneficiaries = computed_result.get("unique_beneficiaries")

        if is_german:
            return (
                f"Die stationären Claims umfassen {total_claims} Claims "
                f"für {unique_beneficiaries} eindeutige Beneficiaries."
            )

        return (
            f"The inpatient claims table contains {total_claims} claims "
            f"for {unique_beneficiaries} unique beneficiaries."
        )

    if route == "outpatient_summary" and isinstance(computed_result, dict):
        total_claims = computed_result.get("total_claims")
        unique_beneficiaries = computed_result.get("unique_beneficiaries")

        if is_german:
            return (
                f"Die ambulanten Claims umfassen {total_claims} Claims "
                f"für {unique_beneficiaries} eindeutige Beneficiaries."
            )

        return (
            f"The outpatient claims table contains {total_claims} claims "
            f"for {unique_beneficiaries} unique beneficiaries."
        )

    if route == "table_shapes":
        if is_german:
            return "Alle geladenen Tabellen wurden mit Zeilen- und Spaltenanzahl zusammengefasst."

        return "All loaded tables were summarized by row and column count."

    if route == "diabetes_cost_summary":
        if is_german:
            return "Die stationären Erstattungsbeträge wurden nach Diabetes-Indikator gruppiert."

        return "Inpatient reimbursement amounts were grouped by diabetes indicator."

    if route in {"inpatient_claims_by_state", "outpatient_claims_by_state"}:
        if is_german:
            return "Die Claims wurden nach Bundesstaat gruppiert und nach Claim-Anzahl sortiert."

        return "Claims were grouped by state and ranked by claim count."

    if route == "fallback":
        if is_german:
            return "Diese Frage wird von den aktuellen Analyse-Routen noch nicht unterstützt."

        return "This question is not supported by the current analytics routes."

    if is_german:
        return "Das Ergebnis wurde erfolgreich mit der deterministischen Analyse-Engine berechnet."

    return "The result was successfully computed using the deterministic analytics engine."


def answer_question(question: str, language: str) -> str:
    """
    Main text-response function used by Gradio.
    """
    text = LANGUAGE_TEXT[language]

    if not question or not question.strip():
        return text["empty_question"]

    routed_question = normalize_question_for_routing(question, language)
    response = RESPONSE_GENERATOR.answer_question(routed_question)

    route = response["route"]
    computed_result = response["computed_result"]
    formatted_result = format_computed_result(computed_result)

    return (
    	f"{text['summary_label']}:\n"
    	f"{build_human_summary(route, computed_result, language)}\n\n"
    	f"{text['details_label']}:\n{formatted_result}\n\n"
    	f"{text['method_label']}:\n{text['method_footer']}\n\n"
    	f"{text['safety_footer']}"
    )


def generate_chart(question: str, language: str) -> go.Figure:
    """
    Generate a chart based on simple keyword routing.

    This is intentionally controlled and deterministic.
    """
    text = LANGUAGE_TEXT[language]
    routed_question = normalize_question_for_routing(question, language)
    q = routed_question.lower() if routed_question else ""

    if "outpatient" in q and "provider" in q:
        df = ENGINE.top_providers_by_claim_count(
            claim_type="outpatient",
            top_n=10,
        )

        title = (
            "Top 10 Outpatient Providers by Claim Count"
            if language == "English"
            else "Top 10 ambulante Provider nach Claim-Anzahl"
        )

        return horizontal_bar_chart(
            df=df,
            x_col="claim_count",
            y_col="Provider",
            title=title,
            x_label="Claim Count" if language == "English" else "Claim-Anzahl",
            y_label="Provider",
        )

    if "provider" in q:
        df = ENGINE.top_providers_by_claim_count(
            claim_type="inpatient",
            top_n=10,
        )

        title = (
            "Top 10 Inpatient Providers by Claim Count"
            if language == "English"
            else "Top 10 stationäre Provider nach Claim-Anzahl"
        )

        return horizontal_bar_chart(
            df=df,
            x_col="claim_count",
            y_col="Provider",
            title=title,
            x_label="Claim Count" if language == "English" else "Claim-Anzahl",
            y_label="Provider",
        )

    if "state" in q:
        df = ENGINE.claim_distribution_by_state(
            claim_type="inpatient",
        ).head(10)

        title = (
            "Top 10 States by Inpatient Claim Count"
            if language == "English"
            else "Top 10 Bundesstaaten nach stationärer Claim-Anzahl"
        )

        return bar_chart_top_values(
            df=df,
            x_col="State",
            y_col="claim_count",
            title=title,
            x_label="State" if language == "English" else "Bundesstaat",
            y_label="Claim Count" if language == "English" else "Claim-Anzahl",
        )

    if "diabetes" in q:
        df = ENGINE.average_inpatient_cost_by_chronic_condition(
            "ChronicCond_Diabetes"
        )

        title = (
            "Average Inpatient Reimbursement by Diabetes Indicator"
            if language == "English"
            else "Durchschnittliche stationäre Erstattung nach Diabetes-Indikator"
        )

        return bar_chart_top_values(
            df=df,
            x_col="ChronicCond_Diabetes",
            y_col="mean",
            title=title,
            x_label="Diabetes Indicator" if language == "English" else "Diabetes-Indikator",
            y_label="Average Reimbursement" if language == "English" else "Durchschnittliche Erstattung",
        )

    if "reimbursement" in q or "cost" in q or "claim amount" in q:
        inpatient = ENGINE.tables["train_inpatient"]

        title = (
            "Distribution of Inpatient Claim Reimbursement"
            if language == "English"
            else "Verteilung der stationären Erstattungsbeträge"
        )

        return histogram(
            df=inpatient,
            column="InscClaimAmtReimbursed",
            title=title,
            x_label=(
                "Inpatient Claim Amount Reimbursed"
                if language == "English"
                else "Stationärer Erstattungsbetrag"
            ),
            nbins=40,
        )

    fig = go.Figure()

    fig.update_layout(
        title=text["no_visual_title"],
        annotations=[
            {
                "text": text["no_visual_text"],
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
            }
        ],
    )

    return fig


def respond(question: str, language: str) -> tuple[str, go.Figure]:
    """
    Return text response and optional chart.
    """
    text_response = answer_question(question, language)
    chart = generate_chart(question, language)

    return text_response, chart


with gr.Blocks(title="Medical Insight Explorer Agent") as demo:
    gr.Markdown(
        """
        # Medical Insight Explorer Agent

        Conversational analytics over cleaned Medicare healthcare claims data.  
        Konversationelle Analyse bereinigter Medicare-Healthcare-Claims-Daten.

        Deterministic analytics first. Grounded explanations and optional visual outputs.
        """
    )

    language_input = gr.Dropdown(
        choices=["English", "Deutsch"],
        value="English",
        label="Language / Sprache",
    )

    with gr.Row():
        question_input = gr.Textbox(
            label="Ask a healthcare analytics question / Frage zur Healthcare-Analyse",
            placeholder="Example: Show top inpatient providers",
            lines=2,
        )

    with gr.Row():
        submit_button = gr.Button("Run analysis / Analyse ausführen", variant="primary")
        clear_button = gr.Button("Clear / Zurücksetzen")

    gr.Examples(
        examples=LANGUAGE_TEXT["English"]["examples"],
        inputs=question_input,
        label="English examples",
    )

    gr.Examples(
        examples=LANGUAGE_TEXT["Deutsch"]["examples"],
        inputs=question_input,
        label="Deutsche Beispiele",
    )

    with gr.Row():
        response_output = gr.Textbox(
            label="Agent response / Antwort des Agenten",
            lines=22,
        )

    with gr.Row():
        chart_output = gr.Plot(
            label="Visualization output / Visualisierung",
        )
	
    gr.Markdown(
        """
        Supported languages: English | Deutsch
 
        Deterministic analytics • Claims data only • No diagnosis
        """
    )

    submit_button.click(
        fn=respond,
        inputs=[question_input, language_input],
        outputs=[response_output, chart_output],
    )

    clear_button.click(
        fn=lambda: ("", "", None),
        inputs=[],
        outputs=[
            question_input,
            response_output,
            chart_output,
        ],
    )


if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        share=False,
    )