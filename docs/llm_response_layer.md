\# LLM Response Layer



\## Purpose



The LLM response layer converts user questions into grounded analytical responses.



This layer does not allow the LLM to freely manipulate healthcare dataframes. Instead, it routes supported questions to deterministic analytics functions and then explains the computed result.



\## Design Principle



The project follows this pattern:



```text

User question

&#x20;       ↓

Rule-based query router

&#x20;       ↓

Deterministic pandas analytics function

&#x20;       ↓

Computed result

&#x20;       ↓

Optional LLM explanation

```



The LLM is used for interpretation, not calculation.



\##Components



| Component             | Purpose                                                       |

| --------------------- | ------------------------------------------------------------- |

| `QueryRouter`         | Maps natural-language questions to supported analytics routes |

| `ResponseGenerator`   | Runs the selected analytics function and generates a response |

| `prompt\_templates.py` | Stores system and explanation prompts for optional LLM usage  |



| Route                        | Trigger Examples          | Analytics Function                                                    |

| ---------------------------- | ------------------------- | --------------------------------------------------------------------- |

| `table\_shapes`               | "shape", "tables"         | `get\_table\_shapes()`                                                  |

| `inpatient\_summary`          | "inpatient summary"       | `inpatient\_claim\_summary()`                                           |

| `outpatient\_summary`         | "outpatient summary"      | `outpatient\_claim\_summary()`                                          |

| `age\_summary`                | "age"                     | `beneficiary\_age\_summary()`                                           |

| `top\_inpatient\_providers`    | "top provider"            | `top\_providers\_by\_claim\_count("inpatient")`                           |

| `top\_outpatient\_providers`   | "top outpatient provider" | `top\_providers\_by\_claim\_count("outpatient")`                          |

| `inpatient\_claims\_by\_state`  | "state"                   | `claim\_distribution\_by\_state("inpatient")`                            |

| `outpatient\_claims\_by\_state` | "outpatient state"        | `claim\_distribution\_by\_state("outpatient")`                           |

| `diabetes\_cost\_summary`      | "diabetes", "diabetic"    | `average\_inpatient\_cost\_by\_chronic\_condition("ChronicCond\_Diabetes")` |

| `fallback`                   | unsupported questions     | Safe unsupported-query message                                        |



\##Fallback Behavior



The response layer works without an API key.



When use\_llm=False, the system returns deterministic fallback explanations based on computed results.



When use\_llm=True and an API key is configured, the LLM receives:



the user question

selected route

computed result



It does not receive direct dataframe access.



\##Safety Boundaries



The response layer is designed for healthcare claims analytics only.



It does not:



diagnose patients

provide treatment recommendations

make clinical decisions

invent unsupported statistics

claim causality without evidence



\##Future Work



Later PRs will connect this response layer to:



visualization routing

Gradio interface

Hugging Face deployment

richer prompt templates

expanded analytics tools

