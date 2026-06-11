# LLM Response Layer

## Purpose

The LLM response layer converts user questions into grounded analytical responses.

This layer does not allow the LLM to freely manipulate healthcare dataframes. Instead, it routes supported questions to deterministic analytics functions and then explains the computed result.

## Design Principle

The project follows this pattern:

```text
User question
      ↓
Rule-based route selection
      ↓
Deterministic pandas analytics function
      ↓
Computed result
      ↓
Response formatter
      ↓
Analytical insight layer
      ↓
Optional LLM explanation support
```

The LLM is used for interpretation, not calculation.

## Analytical Insight Layer

The response layer now includes deterministic analytical insights for supported routes.

These insights explain computed results in cautious, non-causal language.

The insight layer does not create new statistics and does not provide diagnosis, treatment advice, or clinical recommendations.



## Components


| Component             | Purpose                                                       |

| --------------------- | ------------------------------------------------------------- |

| `QueryRouter`         | Maps natural-language questions to supported analytics routes |

| `ResponseGenerator`   | Runs the selected analytics function and generates a response |

| `prompt_templates.py` | Stores system and explanation prompts for optional LLM usage  |


## Supported Routes


| Route                        | Trigger Examples          | Analytics Function                                                    |

| ---------------------------- | ------------------------- | --------------------------------------------------------------------- |

| `table_shapes`               | "shape", "tables"         | `get_table_shapes()`                                                  |

| `inpatient_summary`          | "inpatient summary"       | `inpatient_claim_summary()`                                           |

| `outpatient_summary`         | "outpatient summary"      | `outpatient_claim_summary()`                                          |

| `age_summary`                | "age"                     | `beneficiary_age_summary()`                                           |

| `top_inpatient_providers`    | "top provider"            | `top_providers_by_claim_count("inpatient")`                           |

| `top_outpatient_providers`   | "top outpatient provider" | `top_providers_by_claim_count("outpatient")`                          |

| `inpatient_claims_by_state`  | "state"                   | `claim_distribution_by_state("inpatient")`                            |

| `outpatient_claims_by_state` | "outpatient state"        | `claim_distribution_by_state("outpatient")`                           |

| `diabetes_cost_summary`      | "diabetes", "diabetic"    | `average_inpatient_cost_by_chronic_condition("ChronicCond_Diabetes")` |

| `fallback`                   | unsupported questions     | Safe unsupported-query message                                        |


## Fallback Behavior

The response layer works without an API key.

When `use_llm=False`, the system returns deterministic fallback explanations based on computed results.

When `use_llm=True` and an API key is configured, the LLM receives:

- the user question

- selected route

- computed result

It does not receive direct dataframe access.

## Safety Boundaries

The response layer is designed for healthcare claims analytics only.

It does not:

- diagnose patients
- provide treatment recommendations
- make clinical decisions
- invent unsupported statistics
- claim causality without evidence

## Future Work

Later PRs will connect this response layer to:

- visualization routing
- Gradio interface
- Hugging Face deployment
- richer prompt templates
- expanded analytics tools

