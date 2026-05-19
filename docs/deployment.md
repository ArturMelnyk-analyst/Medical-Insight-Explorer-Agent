# Deployment Guide

## Purpose

This document explains how the Medical Insight Explorer Agent can be deployed as a lightweight Hugging Face Spaces demo.

The deployed version uses sample Parquet files instead of full processed healthcare datasets.

## Live Demo

The deployed Hugging Face Spaces demo is available here:

```text
https://huggingface.co/spaces/Artur-Melnyk/Medical-Insight-Explorer-Agent
```

## Deployment Strategy

The project uses two repositories:

```text
GitHub repository
       ↓
source-of-truth engineering repository
       ↓
Hugging Face Space
       ↓
lightweight deployed demo repository
```

The GitHub repository contains the full project structure, documentation, development history, and reproducibility instructions.

The Hugging Face Space contains only the files required to run the demo app.


## Data Strategy

Full processed healthcare datasets are not committed to GitHub or Hugging Face.

The deployed app uses small sample Parquet files under:

```text
data/sample/
```
The local development app can still use full processed files under:

```text
data/processed/
```

The app automatically tries:

```text
data/processed/
```
first.


If full processed data is unavailable, it falls back to:

```text
data/sample/
```

## Required Files for Hugging Face Space

The Hugging Face Space should include:

```text
app.py
requirements.txt
runtime.txt
agent/
data/sample/
README.md
```

The Space does not need:

```text
notebooks/
docs/
data/processed/
data/raw/
.venv/
```

## Hugging Face Space Setup

Create a new Hugging Face Space with:

```text
SDK: Gradio
Visibility: Public
Python runtime: defined in runtime.txt
```

Then upload or push the minimal deployment files.


## Local Validation Before Deployment

Before deploying, test sample-data fallback locally:

```bash
ren data\processed processed_full_backup
python app.py
ren data\processed_full_backup processed
```

The app should run using:

```text
data/sample/
```

## Data Governance

The deployed version is a portfolio demo.

It does not include full healthcare datasets.

It uses small sampled Parquet files for demonstration only.

The app remains limited to healthcare claims analytics and does not provide diagnosis, treatment recommendations, or clinical advice.

## Future Improvements

Possible deployment improvements include:

- Hugging Face README polish
- embedded Space iframe in portfolio site
- demo GIF
- smaller optimized sample files
- LangGraph workflow after deployment stability

