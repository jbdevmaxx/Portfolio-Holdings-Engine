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

def save_holdings(holdings: pd.DataFrame) -> None:
    """Save holdings back to CSV."""
    holdings.to_csv(HOLDINGS_FILE, index=False)

def update_shares(inputticker: str, inputshares: float) -> None:

    # Load CSV into pandas DataFrame
    holdings = pd.read_csv(HOLDINGS_FILE)
    
    #Ensures ticker is uppercase for consistency
    ticker = inputticker.upper()

    #IF Shares does not exist yet, creates it
    if "shares" not in holdings.columns:
        holdings["shares"] = 0.0

    #Search for ticker in hodlings DataFrame
    match = holdings["ticker"].str.upper() == ticker

    #IF ticker doesnt exist, stop and show message
    if not match.any():
        raise ValueError(f"Ticker{ticker} was not found in holdins.csv file")
    
    #update shares and upload to csv file
    holdings.loc[match, "shares"] = inputshares
    holdings.to_csv(HOLDINGS_FILE, index=False)

    print(f"Updated {ticker} shares to {inputshares})")

def add_new_shares(inputticker: str, inputshares: float) -> None:
    # Load CSV into pandas DataFrame
    holdings = load_holdings();

    #Ensure ticker is uppercase for consistency
    ticker = inputticker.upper().strip()

    match = holdings["ticker"].str.upper() == ticker

    #IF Shares does not exist yet, creates it
    if not match.any():
        raise ValueError(f"Ticker{ticker} was not found in holdins.csv file")

    #Search for ticker in hodlings DataFrame
    existing_shares = float(holdings.loc[match, "shares"].iloc[0])

    #update shares and upload to csv file
    new_total = inputshares + existing_shares

    holdings.loc[match, "shares"] = new_total
    save_holdings(holdings)

    print(f"Added {inputshares} shares to {ticker} (Total: {inputshares + existing_shares})")


def main():

    #Select whether to add to exisitng shares or update new share
    changeVal = int(input("Enter 1 to update share amounts: \nEnter 2 to enter newly purchased shares"))

    if changeVal ==1:
        ticker = input("Enter tickers: ")
        shares = float(input("Enter number of shares: "))
        update_shares (ticker, shares)
    elif changeVal == 2:
        ticker = input("Enter newly purchased ticker: ")
        shares = float(input("Enter number of newly bought shares:"))
        add_new_shares(ticker, shares)
        

    
        

    
    

if __name__ == "__main__":
    main()