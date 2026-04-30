import pandas as pd
from pathlib import Path
from datetime import datetime 
from fetch_prices import fetch_prices_for_holdings

# Finds the main project folder automatically
BASE_DIR = Path(__file__).resolve().parents[1]
HOLDINGS_FILE = BASE_DIR / "data" / "holdings.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "portfolio_summaries"

# Path to holdings CSV
HOLDINGS_FILE = BASE_DIR / "data" / "holdings.csv"

def load_holdings():
    """Load holdings from CSV file."""
    if not HOLDINGS_FILE.exists():
        raise FileNotFoundError(f"Could not find file: {HOLDINGS_FILE}")

    holdings = pd.read_csv(HOLDINGS_FILE)

    #cleans hodlings data to ensure consistency and correct data types
    holdings.columns = holdings.columns.str.strip().str.lower()

    required_columns = {"ticker", "company", "category", "shares"}
    missing_columns = required_columns - set(holdings.columns)

    if missing_columns:
        raise ValueError(f"holdings.csv is missing required columns: {missing_columns}")
    
    holdings["ticker"] = holdings["ticker"].astype(str).str.upper().str.strip()
    holdings["shares"] = pd.to_numeric(holdings["shares"], errors="coerce").fillna(0.0)

    return holdings

def print_holdings_percentages(holdings: pd.DataFrame) -> None:
    print("\nPercentage of each holding in the portfolio:")

    display_columns = [
        "ticker", 
        "company", 
        "shares", 
        "current_price",
        "market value",
        "portfolio_weight_percent"
    ]

    available_columns = [col for col in display_columns if col in holdings.columns]
    summary = holdings[available_columns].copy()

    if "current_price" in summary.columns:
        summary["current_price"] = summary["current_price"].map(lambda x: f"${x:,.2f}")

    if "market_value" in summary.columns:
        summary["market_value"] = summary["market_value"].map(lambda x: f"${x:.2f}")

    if "portfolio_weight_percent" in summary.columns:
        summary["portfolio_weight_percent"] = summary["portfolio_weight_percent"].map(lambda x: f"{x:.2f}%")

    print(summary.to_string(index=False))

def print_category_percentages(holdings: pd.DataFrame) -> None:
    if "category" not in holdings.columns or "market_value" not in holdings.columns:
        print("\nMissing category or market_value column.")
        return

    total_market_value = holdings["market_value"].sum()

    if total_market_value <= 0:
        print("\nTotal portfolio value is 0. Cannot calculate category percentages.")
        return

    category_summary = (
        holdings.groupby("category", dropna=False)["market_value"]
        .sum()
        .reset_index()
    )

    category_summary["category_percentage"] = (
        category_summary["market_value"] / total_market_value * 100
    )

    category_summary = category_summary.sort_values(
        by="category_percentage",
        ascending=False
    )

    print("\nPercentage of each category in the portfolio:")

    for _, row in category_summary.iterrows():
        print(
            f"- {row['category']}: "
            f"${row['market_value']:,.2f} "
            f"({row['category_percentage']:.2f}%)"
        )

def save_portfolio_summary(holdings: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"portfolio_summary_{today}.csv"

    holdings.to_csv(output_file, index=False)

    print(f"\nSaved portfolio summary to: {output_file}")



def main():
    holdings = load_holdings()
    print("\nPortfolio Holdings Loaded Successfully\n")

    #Use function from fetch_prices.py to get current prices and calculate market value and portfolio weight
    holdings = fetch_prices_for_holdings(holdings)

    print_holdings_percentages(holdings)
    print_category_percentages(holdings)
    save_portfolio_summary(holdings)

    



if __name__ == "__main__":
    main()