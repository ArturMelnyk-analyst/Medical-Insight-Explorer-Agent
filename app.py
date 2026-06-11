from pathlib import Path

import gradio as gr
import plotly.graph_objects as go

from agent.analytics_engine import HealthcareAnalyticsEngine
from agent.data_loader import HealthcareDataLoader
from agent.graph_workflow import HealthcareGraphWorkflow
from agent.personas import (
    get_persona_choices,
    get_persona_description,
    get_persona_examples,
)
from agent.response_generator import ResponseGenerator


PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample"


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


def get_examples_title(language: str) -> str:
    """
    Return persona-specific examples section title.
    """
    if language == "Deutsch":
        return "### Empfohlene Fragen für diese Persona"

    return "### Recommended questions for this persona"


def get_default_persona(language: str) -> str:
    """
    Return first persona for selected language.
    """
    return get_persona_choices(language)[0]


def get_three_persona_examples(language: str, persona: str) -> list[str]:
    """
    Return exactly three persona examples for clickable buttons.

    If fewer than three examples ever exist, pad with empty strings.
    """
    examples = get_persona_examples(
        language=language,
        persona=persona,
    )

    examples = examples[:3]

    while len(examples) < 3:
        examples.append("")

    return examples


def update_language_context(
    language: str,
) -> tuple[gr.update, str, str, gr.update, gr.update, gr.update]:
    """
    Update persona choices, description, title, and clickable example buttons
    when language changes.
    """
    persona_choices = get_persona_choices(language)
    default_persona = persona_choices[0]
    examples = get_three_persona_examples(language, default_persona)

    return (
        gr.update(
            choices=persona_choices,
            value=default_persona,
        ),
        get_persona_description(
            language=language,
            persona=default_persona,
        ),
        get_examples_title(language),
        gr.update(value=examples[0], visible=bool(examples[0])),
        gr.update(value=examples[1], visible=bool(examples[1])),
        gr.update(value=examples[2], visible=bool(examples[2])),
    )


def update_persona_context(
    language: str,
    persona: str,
) -> tuple[str, str, gr.update, gr.update, gr.update]:
    """
    Update persona description, title, and clickable example buttons
    when persona changes.
    """
    examples = get_three_persona_examples(language, persona)

    return (
        get_persona_description(
            language=language,
            persona=persona,
        ),
        get_examples_title(language),
        gr.update(value=examples[0], visible=bool(examples[0])),
        gr.update(value=examples[1], visible=bool(examples[1])),
        gr.update(value=examples[2], visible=bool(examples[2])),
    )


def use_example(example_text: str) -> str:
    """
    Put clicked persona example into the question textbox.
    """
    return example_text


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
        chart.update_layout(
            title=(
                "Keine Visualisierung erstellt"
                if language == "Deutsch"
                else "No visualization generated"
            )
        )

    return text_response, chart


DEFAULT_LANGUAGE = "English"
DEFAULT_PERSONA = get_default_persona(DEFAULT_LANGUAGE)
DEFAULT_EXAMPLES = get_three_persona_examples(DEFAULT_LANGUAGE, DEFAULT_PERSONA)


with gr.Blocks(title="Medical Insight Explorer Agent") as demo:
    gr.Markdown(
        """
        # Medical Insight Explorer Agent

        Conversational analytics over cleaned Medicare healthcare claims data.  
        Konversationelle Analyse bereinigter Medicare-Healthcare-Claims-Daten.

        Deterministic analytics first. Persona-guided questions. Grounded explanations and optional visual outputs.
        """
    )

    language_input = gr.Dropdown(
        choices=["English", "Deutsch"],
        value=DEFAULT_LANGUAGE,
        label="Language / Sprache",
    )

    persona_input = gr.Dropdown(
        choices=get_persona_choices(DEFAULT_LANGUAGE),
        value=DEFAULT_PERSONA,
        label="Stakeholder persona / Stakeholder-Persona",
    )

    persona_description = gr.Markdown(
        get_persona_description(
            language=DEFAULT_LANGUAGE,
            persona=DEFAULT_PERSONA,
        )
    )

    persona_examples_title = gr.Markdown(
        get_examples_title(DEFAULT_LANGUAGE)
    )

    with gr.Row():
        persona_example_1 = gr.Button(
            value=DEFAULT_EXAMPLES[0],
            visible=bool(DEFAULT_EXAMPLES[0]),
        )
        persona_example_2 = gr.Button(
            value=DEFAULT_EXAMPLES[1],
            visible=bool(DEFAULT_EXAMPLES[1]),
        )
        persona_example_3 = gr.Button(
            value=DEFAULT_EXAMPLES[2],
            visible=bool(DEFAULT_EXAMPLES[2]),
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

    response_output = gr.Textbox(
        label="Agent response / Antwort des Agenten",
        lines=24,
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
        fn=update_language_context,
        inputs=language_input,
        outputs=[
            persona_input,
            persona_description,
            persona_examples_title,
            persona_example_1,
            persona_example_2,
            persona_example_3,
        ],
    )

    persona_input.change(
        fn=update_persona_context,
        inputs=[
            language_input,
            persona_input,
        ],
        outputs=[
            persona_description,
            persona_examples_title,
            persona_example_1,
            persona_example_2,
            persona_example_3,
        ],
    )

    persona_example_1.click(
        fn=use_example,
        inputs=persona_example_1,
        outputs=question_input,
    )

    persona_example_2.click(
        fn=use_example,
        inputs=persona_example_2,
        outputs=question_input,
    )

    persona_example_3.click(
        fn=use_example,
        inputs=persona_example_3,
        outputs=question_input,
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