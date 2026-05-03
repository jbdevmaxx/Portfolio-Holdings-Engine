import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime


# Finds the main project folder automatically
BASE_DIR = Path(__file__).resolve().parents[1]

# Input file
HOLDINGS_FILE = BASE_DIR / "data" / "holdings.csv"

# Output folder
OUTPUT_DIR = BASE_DIR / "outputs" / "prices"


def load_holdings() -> pd.DataFrame:
    """
    Load holdings.csv and normalize column names.
    Required column: ticker
    Optional columns: company, category, asset_type, shares, notes
    """
    if not HOLDINGS_FILE.exists():
        raise FileNotFoundError(f"Could not find holdings file: {HOLDINGS_FILE}")

    holdings = pd.read_csv(HOLDINGS_FILE)

    # Make column names consistent
    holdings.columns = holdings.columns.str.strip().str.lower()

    if "ticker" not in holdings.columns:
        raise ValueError("holdings.csv must contain a column named 'ticker'")

    # Clean ticker formatting
    holdings["ticker"] = holdings["ticker"].astype(str).str.upper().str.strip()

    return holdings


def get_latest_price(ticker: str) -> dict:
    """
    Get latest available price data for one ticker using yfinance.

    Uses:
    1. fast_info for quick latest price data
    2. history(period='5d') as fallback if fast_info fails or returns no price
    """
    ticker = ticker.upper().strip()

    result = {
        "ticker": ticker,
        "current_price": None,
        "previous_close": None,
        "currency": None,
        "price_timestamp": datetime.now().isoformat(timespec="seconds"),
        "price_status": "not_started",
    }

    try:
        stock = yf.Ticker(ticker)

        # Try fast_info first
        try:
            fast_info = stock.fast_info

            result["current_price"] = fast_info.get("last_price")
            result["previous_close"] = fast_info.get("previous_close")
            result["currency"] = fast_info.get("currency")

        except Exception as fast_info_error:
            result["price_status"] = f"fast_info_failed: {fast_info_error}"

        # Fallback if current price is missing
        if result["current_price"] is None:
            history = stock.history(period="5d")

            if not history.empty:
                latest_row = history.iloc[-1]
                result["current_price"] = float(latest_row["Close"])

                if len(history) >= 2:
                    result["previous_close"] = float(history.iloc[-2]["Close"])

        if result["current_price"] is not None:
            result["price_status"] = "success"
        else:
            result["price_status"] = "no_price_found"

    except Exception as e:
        result["price_status"] = f"error: {e}"

    return result


#fetches prices for all holdings in csv file and merges results back into original holdings dataframe
def fetch_prices_for_holdings(holdings: pd.DataFrame) -> pd.DataFrame:
    
    #Fetch latest prices for all tickers in holdings.csv.

    """

    Returns a DataFrame with:
    - current_price
    - previous_close
    - currency
    - price_status
    - market_value
    - portfolio_weight_percent

    """
    
    
    price_results = []

    for ticker in holdings["ticker"]:
        print(f"Fetching price for {ticker}...")
        price_data = get_latest_price(ticker)
        price_results.append(price_data)

    prices = pd.DataFrame(price_results)

    # Merge price data back into original holdings dataframe
    merged = holdings.merge(prices, on="ticker", how="left")

    # If shares exists, calculate market value
    if "shares" in merged.columns:
        merged["shares"] = pd.to_numeric(merged["shares"], errors="coerce").fillna(0)
        merged["current_price"] = pd.to_numeric(merged["current_price"], errors="coerce")
        merged["market_value"] = merged["shares"] * merged["current_price"]

        total_value = merged["market_value"].sum()

        if total_value > 0:
            merged["portfolio_weight_percent"] = (
                merged["market_value"] / total_value * 100
            ).round(2)
        else:
            merged["portfolio_weight_percent"] = 0

    return merged


def save_price_report(price_report: pd.DataFrame) -> Path:
    """
    Save price report to outputs/prices/prices_YYYY-MM-DD.csv
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"prices_{today}.csv"

    price_report.to_csv(output_file, index=False)

    return output_file


def main():
    holdings = load_holdings()
    price_report = fetch_prices_for_holdings(holdings)
    output_file = save_price_report(price_report)

    print("\nPrice retrieval complete.")
    print(f"Saved report to: {output_file}")

    columns_to_show = [
        col for col in [
            "ticker",
            "company",
            "shares",
            "current_price",
            "previous_close",
            "market_value",
            "portfolio_weight_percent",
            "currency",
            "price_status",
        ]
        if col in price_report.columns
    ]

    print("\nPreview:")
    print(price_report[columns_to_show])


if __name__ == "__main__":
    main()