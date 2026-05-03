# Portfolio Research Engine

A Python-based research workflow that reads portfolio holdings, retrieves current market prices, calculates allocation by holding and category, and generates daily Markdown portfolio reports for personal research.

## Current Features

- Reads portfolio holdings from CSV
- Updates share counts manually
- Retrieves latest available prices using `yfinance`
- Calculates market value per holding
- Calculates portfolio weight by holding
- Calculates allocation by category
- Generates daily Markdown portfolio reports
- Generates an initial research workspace from holdings data
- Creates a portfolio risk register template
- Creates starter thesis files for each holding
- Saves generated outputs separately from source holdings data

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