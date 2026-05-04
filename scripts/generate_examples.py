from pathlib import Path

from portfolio_summary import load_holdings
from fetch_prices import fetch_prices_for_holdings
from generate_daily_reports import generate_daily_report
from setup_research_workspace import (
    build_holding_thesis_content,
    build_portfolio_thesis_content,
    build_risk_register_content
)

from utils.file_utils import ensure_directory, write_text_file

BASE_DIR = Path(__file__).resolve().parents[1]

EXAMPLES_DIR = BASE_DIR / "examples"
SAMPLE_HOLDINGS_FILE = EXAMPLES_DIR / "sample_holdings.csv"

SAMPLE_DAILY_REPORT_FILE = EXAMPLES_DIR / "sample_daily_report.md"
SAMPLE_PORTFOLIO_THESIS_FILE = EXAMPLES_DIR / "sample_portfolio_thesis.md"
SAMPLE_RISK_REGISTER_FILE = EXAMPLES_DIR / "sample_risk_register.md"
SAMPLE_HOLDING_THESIS_FILE = EXAMPLES_DIR / "sample_holding_thesis_NVDA.md"

def get_sample_holding_row(holdings, ticker: str):
    # Return one row from the sample holdings DataFrame for a given ticker

    ticker = ticker.upper().strip()

    match = holdings["ticker"].astype(str).str.upper().str.strip() == ticker

    if not match.any():
        raise ValueError(f"Ticker {ticker} not found in sample holdings")
    
    return holdings.loc[match].iloc[0]

def generate_example_files() -> None:
    # Generates demo-safe example files from examples/sample_holdings.csv

    ensure_directory(EXAMPLES_DIR)

    print("\nLoading sample holdings...")
    holdings = load_holdings(SAMPLE_HOLDINGS_FILE)

    print("Fetching prices for sample holdings...")
    holdings = fetch_prices_for_holdings(holdings)

    print("Generating sample daily report...")
    daily_report = generate_daily_report(holdings)
    write_text_file(SAMPLE_DAILY_REPORT_FILE, daily_report)

    print("Generating sample portfolio thesis...")
    portfolio_thesis = build_portfolio_thesis_content(holdings)
    write_text_file(SAMPLE_PORTFOLIO_THESIS_FILE, portfolio_thesis)

    print("GEnerating sample NVDA holding thesis...")
    nvda_row = get_sample_holding_row(holdings, "NVDA")
    nvda_thesis = build_holding_thesis_content(nvda_row)
    write_text_file(SAMPLE_HOLDING_THESIS_FILE, nvda_thesis)

    print("\nExample files generated succesfully:")
    print(SAMPLE_DAILY_REPORT_FILE)
    print(SAMPLE_PORTFOLIO_THESIS_FILE)
    print(SAMPLE_RISK_REGISTER_FILE)
    print(SAMPLE_HOLDING_THESIS_FILE)

def main():
    generate_example_files()

if __name__ == "__main__":
    main()