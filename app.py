from pathlib import Path

import gradio as gr
import plotly.graph_objects as go

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.data_loader import HealthcareDataLoader
from agent.graph_workflow import HealthcareGraphWorkflow
from agent.response_generator import ResponseGenerator


PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample"


LANGUAGE_TEXT = {
    "English": {
        "examples_label": "☰ English examples",
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
        "examples_label": "☰ Deutsche Beispiele",
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
    Prefer full local processed data and fall back to sample data for demo deployment.
    """
    required_file = "train_beneficiary_clean.parquet"

    if (PROCESSED_DATA_DIR / required_file).exists():
        return PROCESSED_DATA_DIR

    if (SAMPLE_DATA_DIR / required_file).exists():
        return SAMPLE_DATA_DIR

    raise FileNotFoundError(
        "No healthcare Parquet data found. "
        "Place cleaned Parquet files in data/processed/ "
        "or sample Parquet files in data/sample/."
    )


def initialize_components() -> tuple[HealthcareAnalyticsEngine, ResponseGenerator]:
    """
    Load healthcare tables and initialize analytics, response, and graph components.
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

GRAPH_WORKFLOW = HealthcareGraphWorkflow(
    analytics_engine=ENGINE,
    response_generator=RESPONSE_GENERATOR,
)


def update_example_visibility(language: str) -> tuple[gr.update, gr.update]:
    """
    Show only the example prompts for the selected interface language.
    """
    if language == "Deutsch":
        return gr.update(visible=False), gr.update(visible=True)

    return gr.update(visible=True), gr.update(visible=False)


def create_empty_question_chart(language: str) -> go.Figure:
    """
    Return a simple placeholder chart when the user submits an empty question.
    """
    fig = go.Figure()

    fig.update_layout(
        title=(
            "Keine Frage eingegeben"
            if language == "Deutsch"
            else "No question entered"
        )
    )

    return fig


def respond(question: str, language: str) -> tuple[str, go.Figure]:
    """
    Submit a user question to the LangGraph workflow and return text + chart output.
    """
    if not question or not question.strip():
        if language == "Deutsch":
            return (
                "Bitte geben Sie eine Frage zur Healthcare-Analyse ein.",
                create_empty_question_chart(language),
            )

        return (
            "Please enter a healthcare analytics question.",
            create_empty_question_chart(language),
        )

    result = GRAPH_WORKFLOW.invoke(
        question=question,
        language=language,
    )

    text_response = result.get(
        "text_response",
        "No response generated.",
    )

    chart = result.get("chart")

    if chart is None:
        chart = go.Figure()
        chart.update_layout(title="No visualization generated")

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

    question_input = gr.Textbox(
        label="Ask a healthcare analytics question / Frage zur Healthcare-Analyse",
        placeholder="Example: Show top inpatient providers",
        lines=2,
    )

    with gr.Row():
        submit_button = gr.Button(
            "Run analysis / Analyse ausführen",
            variant="primary",
        )
        clear_button = gr.Button("Clear / Zurücksetzen")

    with gr.Column(visible=True) as english_examples_section:
        gr.Markdown(LANGUAGE_TEXT["English"]["examples_label"])
        gr.Examples(
            examples=LANGUAGE_TEXT["English"]["examples"],
            inputs=question_input,
        )

    with gr.Column(visible=False) as german_examples_section:
        gr.Markdown(LANGUAGE_TEXT["Deutsch"]["examples_label"])
        gr.Examples(
            examples=LANGUAGE_TEXT["Deutsch"]["examples"],
            inputs=question_input,
        )

    response_output = gr.Textbox(
        label="Agent response / Antwort des Agenten",
        lines=22,
    )

    chart_output = gr.Plot(
        label="Visualization output / Visualisierung",
    )

    gr.Markdown(
        """
        Supported languages: English | Deutsch  

        Deterministic analytics • Claims data only • No diagnosis
        """
    )

    language_input.change(
        fn=update_example_visibility,
        inputs=language_input,
        outputs=[
            english_examples_section,
            german_examples_section,
        ],
    )

    submit_button.click(
        fn=respond,
        inputs=[
            question_input,
            language_input,
        ],
        outputs=[
            response_output,
            chart_output,
        ],
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