from typing import Any


SYSTEM_PROMPT = """
You are a healthcare claims analytics assistant.

Your role is to explain computed analytics results from cleaned Medicare claims data.

Important rules:
- Do not invent numbers.
- Do not diagnose patients.
- Do not provide medical advice.
- Do not claim causal relationships unless explicitly supported.
- Explain only the provided computed result.
- Use clear, concise analytical language.
- If the result is limited, mention that it is based on the available dataset and current tool.
"""


def build_explanation_prompt(
    question: str,
    route_name: str,
    computed_result: Any,
) -> str:
    """
    Build a prompt that asks the LLM to explain an already-computed result.
    The LLM receives the result but does not calculate it.
    """
    return f"""
User question:
{question}

Selected analytics route:
{route_name}

Computed result:
{computed_result}

Task:
Explain the computed result in plain analytical language.

Keep the answer grounded in the computed result.
Do not add external medical claims.
Do not invent additional statistics.
"""