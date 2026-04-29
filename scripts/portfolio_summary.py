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

def obtain_prices(holdings: pd.DataFrame) -> pd.DataFrame:
    # Placeholder function to obtain current prices for each holding
    # This will need to be implemented using a web scraper or API to get real-time prices
    holdings["price"] = 0.0  # Replace with actual price retrieval logic
    return holdings

def main():
    holdings = load_holdings()
    print("\nPortfolio Holdings Loaded Successfully\n")

    # Print Current SUmmary of holdings
    print(holdings)

    # Print percentage of each holding in the portfolio
    total_shares = holdings["shares"].sum()
    holdings["percentage"] = (holdings["shares"] / total_shares) * 100
    print("\nPercentage of each holding in the portfolio:")
    print(holdings[["ticker", "company", "shares", "percentage"]])  

    #Need to finish web scraper to obtain prices of each holding to calculate total value of each holding and percentage of total portfolio value

    #Print percentage of each sector in the category in the portfolio   





if __name__ == "__main__":
    main()