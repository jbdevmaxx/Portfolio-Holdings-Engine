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