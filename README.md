# ThesisOps (Formerly Portfolio Research Engine)

ThesisOps is a Python-based research workflow automation project that turns structured portfolio holdings data into organized, analysis-ready research outputs.

The project reads holdings from a CSV file, retrieves latest available market prices, calculates portfolio allocation, generates Markdown reports, and creates thesis/risk templates for human-in-the-loop investment research. The goal is not to create a stock-picking tool, but to build a repeatable research system that helps users document why they own each position, identify concentration risk, and prepare source material for AI-assisted review.

ThesisOps is designed as a local-first workflow and can be used as a foundation for future integrations with NotebookLM, Notion, AI APIs, dashboards, or other research automation tools.

## Current Features

- Reads portfolio holdings from a manually maintained CSV file
- Supports configurable holdings input for personal workflows, demos, and future tests
- Retrieves latest available price data using `yfinance`
- Calculates market value per holding
- Calculates portfolio weight by holding
- Calculates category-level allocation
- Generates daily Markdown portfolio reports
- Creates an initial research workspace from holdings data
- Generates a portfolio-level thesis template
- Generates a portfolio risk register template
- Generates individual holding thesis templates
- Uses shared utility modules for formatting, file writing, and Markdown helpers
- Keeps generated reports separate from source holdings data
- Includes sanitized sample holdings and example outputs for public demo use
- Documents architecture, data flow, and technical decisions
- Designed for future human-approved AI thesis suggestion workflows

## What This Project Demonstrates

- Python scripting and modular workflow design
- CSV data ingestion and validation
- External data retrieval through a price provider
- Portfolio allocation and concentration analysis
- Markdown report generation
- Local-first data privacy design
- Reusable utility functions
- Architecture and data-flow documentation
- Human-in-the-loop AI workflow planning
- Demo-safe sample data for public presentation

## Project Structure

```text
Portfolio-Research-Engine/
├── data/
│   └── holdings.csv
├── scripts/
│   ├── update_holdings.py
│   ├── fetch_prices.py
│   ├── portfolio_summary.py
│   ├── generate_daily_reports.py
│   └── setup_research_workspace.py
├── docs/
│   ├── architecture.md
│   ├── data_flow.md
│   └── technical_decisions.md
├── outputs/
│   ├── daily_reports/
│   ├── prices/
│   └── portfolio_summaries/
├── thesis/
│   ├── portfolio_thesis.md
│   ├── risk_register.md
│   └── holdings/
├── requirements.txt
├── .gitignore
└── README.md
```

## Current Workflow

```text
data/holdings.csv
    ↓
scripts/fetch_prices.py
    ↓
latest price data + market values
    ↓
scripts/portfolio_summary.py
    ↓
portfolio allocation by holding and category
    ↓
scripts/generate_daily_reports.py
    ↓
outputs/daily_reports/daily_report_YYYY-MM-DD.md
```

### Research Workspace Setup Flow

```text
data/holdings.csv
    ↓
scripts/setup_research_workspace.py
    ↓
latest price data + market values
    ↓
thesis/portfolio_thesis.md
thesis/risk_register.md
thesis/holdings/TICKER.md


## Setup

### 1. Create and activate a virtual environment

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage



### Update holdings or share counts

```bash
python scripts/update_holdings.py
```

### Generate initial research_workspace

```bash
python scripts/setup_research_workspace.py

### Generate portfolio summary in the terminal

```bash
python scripts/portfolio_summary.py
```

### Generate a daily Markdown report

```bash
python scripts/generate_daily_reports.py
```

The Markdown report is saved locally in:

```text
outputs/daily_reports/
```

Generated reports are intentionally ignored by Git because they may contain personal portfolio information.

## Data Notes

`data/holdings.csv` is the manually maintained source of truth for portfolio holdings.

Generated files in `outputs/` and personal research files in `thesis/` are not committed to GitHub.

The `thesis/` folder is generated locally and may contain personal investment reasoning, risk notes, and holding-level thesis details.

## Roadmap

- [x] Read holdings from CSV
- [x] Update share counts manually
- [x] Retrieve latest available prices
- [x] Calculate market value and portfolio allocation
- [x] Generate daily Markdown portfolio reports
- [x] Generate starter thesis/risk templates
- [ ] Fill out thesis/risk notes per holding
- [ ] Add news retrieval by ticker
- [ ] Add earnings calendar tracking
- [ ] Generate NotebookLM-ready research packets
- [ ] Add Notion export
- [ ] Add tests

## Disclaimer

This project is for personal research, education, and workflow automation only. It does not provide financial advice, investment recommendations, or trading signals.
