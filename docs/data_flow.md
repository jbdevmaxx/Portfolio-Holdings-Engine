# Portfolio Research Engine — Data Flow

## Purpose

This document explains how data moves through the Portfolio Research Engine from the source holdings file to the generated daily Markdown report.

The goal is to make the system easy to understand, debug, and extend.

## High-Level Data Flow

```text
holdings.csv
    ↓
load_holdings()
    ↓
holdings DataFrame
    ↓
fetch_prices_for_holdings()
    ↓
enriched holdings DataFrame
    ↓
generate_daily_report()
    ↓
daily_report_YYYY-MM-DD.md
```

## Daily Report Data Flow

```text
data/holdings.csv
    ↓
load_holdings()
    ↓
holdings DataFrame
    ↓
fetch_prices_for_holdings()
    ↓
enriched holdings DataFrame
    ↓
calculate market value and portfolio weight
    ↓
generate_daily_report()
    ↓
outputs/daily_reports/daily_report_YYYY-MM-DD.md
```

## Research Workspace Data Flow

```text
data/holdings.csv
    ↓
load_holdings()
    ↓
holdings DataFrame
    ↓
fetch_prices_for_holdings()
    ↓
enriched holdings DataFrame
    ↓
setup_research_workspace.py
    ↓
thesis/portfolio_thesis.md
thesis/risk_register.md
thesis/holdings/TICKER.md
```

## Input Data

The primary source file for holdings data is:

data/holdings.csv

Required columns:
 - ticker
 - company
 - category
 - asset_type
 - shares


The holdings CSV is the manually maintained by user as the soruce of truth.  It should contain user-controlled portfolio data, not generated price data (i.e shares amounts rather than shares market value)

## Enrihed Data Columns

After `fetch_prices_for_holdings()` runs, the hodlings DataFrame is enriched with market data and allocation metrics

Expected added columns:
- current price
- previous_close
- currency
- price_timestamp
- price_status
- market-value
- portfolio weight percent

These columns are genrated by the script and should not be manually maintined in `holdings.csv`

## Generated Outputs

Generated reports are saved locally in:

```text
outputs/daily_reports/
outputs/prices/
outputs/portfolio_summaries/
```

Generated research workspace files are saved locally in:

```text
thesis/
thesis/holdings/
```
These folders are ignored by GIT because they may contain personal portfolio values, daily reports, or investment reasoning

## Data Ownership Rules

- `data/holdings.csv` is manually maintained
- Price data is retrieved dynamically through `fetch_prices.py`
- Allocation metrics are calcualted from `shares x current price`
- Daily reports are generated outputs
- Thesis and risk-register files are personal research notes
- Generated files should not overwrite the orginal holdings CSV

## Design Intent

The data flow is designed so that each layer has a clear responsibility

```text
data/holdings.csv
    = source of static values(ticker, company, category, asset_type, shares) from user

scripts/fetch_prices.py
    = add current market data prices

scripts/portfolio_summary.py
    = allocation calculations and terminal summaries

scripts/generate_daily_reports.py
    = daily Markdown report creation

scripts/setup_research_workspace.py
    = initial thesis and risk workspace generation

outputs/
    = generated reports and snapshots

thesis/
    = personal research notes and holding-level thesis files


```













