# Portfolio Research Engine — Architecture

## Overview

Portfolio Research Engine is a Python-based workflow that reads a user's portfolio holdings, retrieves current market prices, calculates portfolio allocation, and generates daily Markdown reports for personal investment research.

The system is currently designed as a local-first workflow. It uses a manually maintained holdings CSV as the source of truth, retrieves market data through a price provider, enriches the holdings data with current prices and allocation metrics, and outputs Markdown reports that can be reviewed manually or uploaded into NotebookLM for AI-assisted analysis.

## Problem Statement

Retail investors often have portfolio data, research notes, news, and investment theses scattered across multiple tools. This makes it difficult to answer basic portfolio management questions consistently:

- Which holdings have the largest impact on the portfolio?
- Which categories or sectors dominate portfolio exposure?
- Which holdings deserve research attention first?
- What information is missing before making a decision?
- How can daily research be structured into a repeatable process?

This project addresses that problem by creating a repeatable research workflow that turns raw portfolio holdings into structured analysis-ready reports.

## Current Architecture

```text
data/holdings.csv
    ↓
scripts/fetch_prices.py
    ↓
current price data + market value calculations
    ↓
scripts/portfolio_summary.py
    ↓
holding-level and category-level allocation summaries
    ↓
scripts/generate_daily_reports.py
    ↓
outputs/daily_reports/daily_report_YYYY-MM-DD.md
    ↓
manual upload to NotebookLM
    ↓
AI-assisted research review
```

## Research Workspace Setup Architecture

In addition to daily report generation, the project includes an initial setup workflow that creates a local research workspace from the user's holdings data.

This setup workflow is intended to be run when a user first creates or updates their portfolio research system.

```text
data/holdings.csv
    ↓
scripts/setup_research_workspace.py
    ↓
scripts/fetch_prices.py
    ↓
current price data + market value + portfolio weight
    ↓
thesis/portfolio_thesis.md
thesis/risk_register.md
thesis/holdings/TICKER.md
```

## Local Data Boundaries

The project separates source files, generated outputs, and personal research notes.

```text
data/
    Manually maintained portfolio input

scripts/
    Reusable Python workflows

outputs/
    Generated reports and price snapshots

thesis/
    Personal research notes and thesis templates

docs/
    Project architecture and technical documentation
```

## Current Scripts

### `scripts/fetch_prices.py`

Retrieves latest available price data and enriches holdings with:

- `current_price`
- `previous_close`
- `market_value`
- `portfolio_weight_percent`
- `price_status`

### `scripts/portfolio_summary.py`

Uses enriched holdings data to print portfolio allocation summaries by holding and category.

### `scripts/generate_daily_reports.py`

Generates a daily Markdown portfolio report saved locally in `outputs/daily_reports/`.

### `scripts/setup_research_workspace.py`

Creates an initial research workspace with:

- portfolio-level thesis template
- portfolio risk register template
- individual holding thesis templates

## Design Principles

- Keep `holdings.csv` as the manually maintained source of truth.
- Keep generated reports separate from source data.
- Keep personal thesis notes local and out of Git.
- Reuse price retrieval functions instead of duplicating logic across scripts.
- Use Markdown as the primary output format for compatibility with NotebookLM, Notion, GitHub documentation, and future AI API analysis.
- Keep thesis generation human-in-the-loop by using placeholders rather than automatically inventing investment reasoning.