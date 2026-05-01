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
│   └── generate_daily_reports.py
├── outputs/
│   ├── daily_reports/
│   ├── prices/
│   └── portfolio_summaries/
├── requirements.txt
├── .gitignore
└── README.md

## Current Workflow

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

Setup!

1. Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

2. Install Dependencies

pip install -r requirements.txt

Usage:

1. Update holdings or share counts:

python scripts/update_holdings.py

2. Generate portfolio summary in the terminal:

python scripts/portfolio_summary.py

3. Generate a daily Markdown report:

python scripts/generate_daily_reports.py

4. Markdown report is saved locally in:

outputs/daily_reports/

Generated reports are intentionally ignored by Git because they may contain personal portfolio information.

Data Notes

data/holdings.csv is the manually maintained source of truth for portfolio holdings.

Generated files in outputs/ are not committed to GitHub.

Roadmap
 Read holdings from CSV (Done)
 Update share counts manually (Done)
 Retrieve latest available prices (Done)
 Calculate market value and portfolio allocation (Done)
 Generate daily Markdown portfolio reports (Done)
 Add news retrieval by ticker
 Add earnings calendar tracking
 Add thesis/risk notes per holding
 Generate NotebookLM-ready research packets
 Add Notion export
 Add tests


Disclaimer

This project is for personal research, education, and workflow automation only. It does not provide financial advice, investment recommendations, or trading signals.