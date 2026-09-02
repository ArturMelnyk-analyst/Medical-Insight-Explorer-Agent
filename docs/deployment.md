# Deployment Guide

## Purpose

This document describes how **Medical Insight Explorer Agent v1.2.0** is deployed locally and on Hugging Face Spaces.

The project supports two runtime contexts:

```text
Local development
→ full processed Parquet data when available

Hugging Face Spaces
→ lightweight sample Parquet data
```

Both use the same core application code and controlled analytics workflow.

---

## Live Demo

The public application is available on Hugging Face Spaces:

https://huggingface.co/spaces/Artur-Melnyk/Medical-Insight-Explorer-Agent

The Space runs the Gradio application using lightweight sample Parquet files.

---

## Deployment Model

GitHub and Hugging Face serve different purposes:

```text
GitHub repository
        ↓
engineering source of truth
        ↓
validated release
        ↓
Hugging Face Space
        ↓
public portfolio demo
```

The GitHub repository contains the complete project, documentation, development history, and supporting assets.

The Hugging Face repository contains the runtime files required for the public application.

Deployment commits remain separate from the GitHub development history.

---

## Data Strategy

The local application can use full cleaned Parquet data from:

```text
data/processed/
```

The public deployment uses lightweight sample data from:

```text
data/sample/
```

When full processed data is unavailable, the application can use the sample-data fallback.

```text
data/processed/
      │
      ├── available → full local data
      │
      └── unavailable
                ↓
          data/sample/
```

Public-demo results may therefore differ from results produced using the complete local dataset.

Full processed healthcare datasets are not included in the public deployment.

For data details, see [Data Contract](data_contract.md).

---

## Hugging Face Runtime Files

The Space should contain the files required to run the application:

```text
app.py
requirements.txt
runtime.txt

agent/
    __init__.py
    analytics_engine.py
    chart_router.py
    data_loader.py
    graph_workflow.py
    insight_layer.py
    language_utils.py
    personas.py
    planner.py
    prompt_templates.py
    response_formatter.py
    response_generator.py
    tool_registry.py
    visualization_tools.py

data/
    sample/

README.md
```

Development-only material does not need to be included unless it is intentionally used by the Space.

Examples:

```text
notebooks/
docs/
images/
demo/
scripts/
data/processed/
.venv/
```

The deployed runtime files should remain synchronized with the validated GitHub release.

---

## Local Validation Before Deployment

Before updating Hugging Face, run the release candidate locally:

```powershell
python app.py
```

Verify representative application behavior:

- English single-step analytics
- German single-step analytics
- English multi-step analytics
- German multi-step analytics
- supported chart rendering
- unsupported-request fallback
- causal-request rejection

For a multi-step request, confirm that all executed analytical results appear in the response while one primary visualization is retained.

A useful test prompt is:

```text
Compare inpatient and outpatient provider activity
```

German:

```text
Vergleiche stationäre und ambulante Provider
```

---

## Validate Sample-Data Fallback

The deployment path should also be tested without the full processed dataset.

From the repository root in PowerShell:

```powershell
Rename-Item data\processed processed_full_backup
python app.py
```

Confirm that the application starts successfully using:

```text
data/sample/
```

After testing, restore the directory:

```powershell
Rename-Item data\processed_full_backup processed
```

Do not deploy until the sample-data path works independently of `data/processed/`.

---

## Deploy to Hugging Face

After validating the release candidate, synchronize the required runtime files with the separate Hugging Face repository.

Typical workflow:

```powershell
cd <hugging-face-repository>

git status
git pull

# Synchronize the validated runtime files.

git status
git diff

git add .
git commit -m "deploy: update Medical Insight Explorer Agent to v1.2.0"
git push
```

Verify the actual local Hugging Face repository path and branch before running these commands.

After the push, wait for the Space to rebuild and confirm that it starts successfully.

---

## Post-Deployment Validation

Test the live Space after every release update.

Confirm:

- application startup
- English and German interaction
- persona controls and example prompts
- single-step analytics
- supported multi-step analytics
- multi-result response synthesis
- workflow status
- supported Plotly charts
- one-primary-chart behavior
- controlled fallback for unsupported and causal requests

Successful deployment logs alone are not sufficient; the live application should be tested interactively.

---

## Release Synchronization

GitHub and Hugging Face maintain separate repository histories but should represent the same validated application release.

```text
GitHub v1.2.0 source
        ↓
validated runtime files
        ↓
Hugging Face deployment
        ↓
live validation
```

After the final deployment is verified, public screenshots and demo assets can be refreshed to match the released interface.

---

## Deployment Constraints

The Hugging Face Space is a lightweight portfolio deployment rather than a production healthcare platform.

Important constraints include:

- sample data instead of the complete processed dataset
- descriptive healthcare claims analytics only
- approved deterministic analytics capabilities
- bounded multi-step orchestration
- no unrestricted Python, SQL, pandas, or dataframe execution

For detailed system boundaries, see [Limitations](limitations.md).

For architecture details, see:

- [Architecture](architecture.md)
- [LangGraph Orchestration](langgraph_orchestration.md)

---

## Summary

The deployment model keeps engineering and public-demo responsibilities separate:

```text
GitHub
→ complete engineering project

Hugging Face
→ lightweight public runtime
```

Local execution can use the full processed dataset, while Hugging Face uses sample Parquet data with the same core application architecture.