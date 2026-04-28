import pandas as pd
from pathlib import Path

# Finds the main project folder automatically
BASE_DIR = Path(__file__).resolve().parents[1]

# Path to holdings CSV
HOLDINGS_FILE = BASE_DIR / "data" / "holdings.csv"


def load_holdings():
    """Load holdings from CSV file."""
    if not HOLDINGS_FILE.exists():
        raise FileNotFoundError(f"Could not find file: {HOLDINGS_FILE}")

    holdings = pd.read_csv(HOLDINGS_FILE)
    return holdings


def main():
    holdings = load_holdings()

    print("\nPortfolio Holdings Loaded Successfully\n")
    print(holdings)

    print("\nTickers:")
    tickers = holdings["ticker"].tolist()
    print(tickers)
    company = holdings["company"].tolist()
    print(company)

    print(f"\nTotal holdings: {len(holdings)}")


if __name__ == "__main__":
    main()