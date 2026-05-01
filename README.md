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

Generated files in `outputs/` are not committed to GitHub.

## Roadmap

- [x] Read holdings from CSV
- [x] Update share counts manually
- [x] Retrieve latest available prices
- [x] Calculate market value and portfolio allocation
- [x] Generate daily Markdown portfolio reports
- [ ] Add news retrieval by ticker
- [ ] Add earnings calendar tracking
- [ ] Add thesis/risk notes per holding
- [ ] Generate NotebookLM-ready research packets
- [ ] Add Notion export
- [ ] Add tests

## Disclaimer

This project is for personal research, education, and workflow automation only. It does not provide financial advice, investment recommendations, or trading signals.