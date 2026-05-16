from pathlib import Path
from typing import Any, Dict

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


def answer_question(question: str) -> str:
    """
    Main text-response function used by Gradio.
    """
    if not question or not question.strip():
        return "Please enter a healthcare analytics question."

    response = RESPONSE_GENERATOR.answer_question(question)

    explanation = response["explanation"]
    route = response["route"]
    computed_result = response["computed_result"]

    formatted_result = format_computed_result(computed_result)

    return (
        f"Route selected: {route}\n\n"
        f"Explanation:\n{explanation}\n\n"
        f"Computed result:\n{formatted_result}"
    )


def generate_chart(question: str) -> go.Figure:
    """
    Generate a chart based on simple keyword routing.

    This is intentionally controlled and deterministic.
    """
    q = question.lower() if question else ""

    if "outpatient" in q and "provider" in q:
        df = ENGINE.top_providers_by_claim_count(
            claim_type="outpatient",
            top_n=10,
        )

        return horizontal_bar_chart(
            df=df,
            x_col="claim_count",
            y_col="Provider",
            title="Top 10 Outpatient Providers by Claim Count",
            x_label="Claim Count",
            y_label="Provider",
        )

    if "provider" in q:
        df = ENGINE.top_providers_by_claim_count(
            claim_type="inpatient",
            top_n=10,
        )

        return horizontal_bar_chart(
            df=df,
            x_col="claim_count",
            y_col="Provider",
            title="Top 10 Inpatient Providers by Claim Count",
            x_label="Claim Count",
            y_label="Provider",
        )

    if "state" in q:
        df = ENGINE.claim_distribution_by_state(
            claim_type="inpatient",
        ).head(10)

        return bar_chart_top_values(
            df=df,
            x_col="State",
            y_col="claim_count",
            title="Top 10 States by Inpatient Claim Count",
            x_label="State",
            y_label="Claim Count",
        )

    if "reimbursement" in q or "cost" in q or "claim amount" in q:
        inpatient = ENGINE.tables["train_inpatient"]

        return histogram(
            df=inpatient,
            column="InscClaimAmtReimbursed",
            title="Distribution of Inpatient Claim Reimbursement",
            x_label="Inpatient Claim Amount Reimbursed",
            nbins=40,
        )

    fig = go.Figure()

    fig.update_layout(
        title="No visualization generated for this question",
        annotations=[
            {
                "text": "This query is best answered as a text summary.",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
            }
        ],
    )

    return fig


def respond(question: str) -> tuple[str, go.Figure]:
    """
    Return text response and optional chart.
    """
    text_response = answer_question(question)
    chart = generate_chart(question)

    return text_response, chart


EXAMPLE_QUESTIONS = [
    "Show me the shape of all tables",
    "Give me an inpatient summary",
    "Give me an outpatient summary",
    "What is the average beneficiary age?",
    "Show top inpatient providers",
    "Show top outpatient providers",
    "Show inpatient claims by state",
    "What is the diabetes cost summary?",
    "Show reimbursement distribution",
]


with gr.Blocks(title="Medical Insight Explorer Agent") as demo:
    gr.Markdown(
        """
        # Medical Insight Explorer Agent

        Conversational analytics over cleaned Medicare healthcare claims data.

        This app uses deterministic pandas-based analytics functions first, then returns grounded explanations and optional visual outputs.
        """
    )

    with gr.Row():
        question_input = gr.Textbox(
            label="Ask a healthcare analytics question",
            placeholder="Example: Show top inpatient providers",
            lines=2,
        )

    with gr.Row():
        submit_button = gr.Button("Run analysis", variant="primary")
        clear_button = gr.Button("Clear")

    gr.Examples(
        examples=EXAMPLE_QUESTIONS,
        inputs=question_input,
    )

    with gr.Row():
        response_output = gr.Textbox(
            label="Agent response",
            lines=16,
        )

    with gr.Row():
        chart_output = gr.Plot(
            label="Visualization output",
        )

    submit_button.click(
        fn=respond,
        inputs=question_input,
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
        share=False
    )