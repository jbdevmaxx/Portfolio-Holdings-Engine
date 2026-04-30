# Portfolio Research Engine

A Python-based research workflow that reads portfolio holdings, retrieves current market prices, calculates allocation by holding and category, and generates portfolio summary outputs.

## Current Features

- Reads portfolio holdings from CSV
- Updates share counts manually
- Retrieves latest available prices using yfinance
- Calculates market value per holding
- Calculates portfolio weight by holding
- Calculates allocation by category
- Saves generated summaries separately from source holdings data

## Project Structure

```text
Portfolio-Research-Engine/
├── data/
│   └── holdings.csv
├── scripts/
│   ├── update_holdings.py
│   ├── fetch_prices.py
│   └── portfolio_summary.py
├── outputs/
├── requirements.txt
├── .gitignore
└── README.md