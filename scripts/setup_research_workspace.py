import pandas as pd
from pathlib import Path
from datetime import datetime


from portfolio_summary import load_holdings
from fetch_prices import fetch_prices_for_holdings

from utils.formatting import format_currency, format_percent


#setting up file paths to write to Thesis folder
BASE_DIR = Path(__file__).resolve().parents[1]

THESIS_DIR = BASE_DIR / "thesis"
HOLDINGS_THESIS_DIR = THESIS_DIR / "holdings"

PORTFOLIO_THESIS_FILE = THESIS_DIR/ "portfolio_thesis.md"
RISK_REGISTER_FILE = THESIS_DIR / "risk_register.md"

def create_directory_structure() -> None:
    # Ceates thesis folders if they do not exist
    THESIS_DIR.mkdir(parents = True, exist_ok=True)
    HOLDINGS_THESIS_DIR.mkdir(parents = True, exist_ok=True)

def safe_write_file(file_path: Path, content: str) -> None:
    # Safely writes content to a file if it does not exist, o
    if file_path.exists():
        print(f"Skipped existing file: {file_path}")
        return
    
    file_path.write_text(content, encoding="utf-8")
    print(f"Created file: {file_path}")

def build_category_summary(holdings: pd.DataFrame) -> pd.DataFrame:
    # Creates category allocation summary based on market value
    
    if "market_value" not in holdings.columns:
        raise ValueError("Missing requied column: market_value")
    
    total_market_value = holdings["market_value"].sum()

    #creates summary table by categroy from holdings file
    category_summary = (
        holdings.groupby("category",dropna=False)["market_value"]
        .sum()
        .reset_index()
    )

    if total_market_value > 0:
        category_summary["portfolio_weight_percent"] = (
            category_summary["market_value"] / total_market_value * 100
        )
    else:
        category_summary["portfolio_weight_percent"] = 0
    
    return category_summary.sort_values(
        by="portfolio_weight_percent", 
        ascending=False
    )

def build_portfolio_thesis_content(holdings: pd.DataFrame) -> str:
    #Builds starter content for portfolio_thesis.md
    today = datetime.now().strftime("%Y-%m-%d")
    total_market_value = holdings["market_value"].sum()

    category_summary = build_category_summary(holdings)

    # creates top 10 holdings table
    top_holdings = holdings.sort_values(
        by="portfolio_weight_percent",
        ascending=False
    ).head(10)

    category_lines = []
    for _, row in category_summary.iterrows():
        category_lines.append(
            f"- {row['category']}: "
            f"{format_currency(row['market_value'])} "
            f"({format_percent(row['portfolio_weight_percent'])})"
        )

    top_holdings_lines = []
    for _, row in top_holdings.iterrows():
        top_holdings_lines.append(
            f"- {row['ticker']} ({row['company']}): "
            f"{format_currency(row['market_value'])} "
            f"({format_percent(row['portfolio_weight_percent'])})"
        )

    content = f"""# Portfolio Thesis - {today}

## Purpose

Describe the overall purpose of this portfolio.

Examples:
- Long-term wealth building
- Core ETF compounding
- Selective high-conviction growth exposure
- AI / semiconductor exposure
- Defense / aerospace exposure
- Speculative upside exposure

## Current Portfolio Snapshot

Total estimated market value: **{format_currency(total_market_value)}**

## Largest Holdings


{chr(10).join(top_holdings_lines)}

## Category Allocation

{chr(10).join(category_lines)}

## Portfolio Strategy

### Core Holdings

Purpose:
- [User to complete]

Current core holdings:
- [User to complete]

### Growth Holdings

Purpose:
- [User to complete]

Current growth holdings:
- [User to complete]

### Speculative Holdings

Purpose:
- [User to complete]

Current speculative holdings:
- [User to complete]

### Defensive / Stabilizing Holdings

Purpose:
- [User to complete]

Current defensive holdings:
- [User to complete]

## Portfolio Principles

- Avoid adding to a position without a written thesis.
- Review largest holdings more frequently than smaller holdings.
- Separate price movement from thesis-changing information.
- Track concentration risks across categories.
- Compare individual holdings against ETF alternatives.

## Review Cadence

Daily:
- Review major allocation changes and price movement.

Weekly:
- Review concentration risks and research priorities.

Quarterly:
- Review earnings, filings, and thesis validity.

Annually:
- Review whether the portfolio still matches the intended strategy.

## Open Questions

- Which positions have the strongest written thesis?
- Which positions are oversized relative to conviction?
- Which positions are too small to matter?
- Which categories are most concentrated?
- Which risks apply across multiple holdings?
"""

    return content

def build_risk_register_content(holdings: pd.DataFrame) -> str:
    #Builds risk register template content based on current holdings

    today = datetime.now().strftime("%Y-%m-%d")
    category_summary = build_category_summary(holdings)

    category_risk_sections = []

    for _, row in category_summary.iterrows():
        category = row["category"]
        category_holdings = holdings[holdings["category"] == category]

        affected_holdings = [
            f" -{holding_row['ticker']} ({holding_row['company']})"
            for _, holding_row in category_holdings.iterrows()
        ]
    
        section = f"""### {category}, Risk

Affected Holdings:
{chr(10).join(affected_holdings)}

Current allocation:
- {format_currency(row['market_value'])} 
- {format_percent(row['portfolio_weight_percent'])}

Risk description:
- [User to complete]

What could cause this risk to increase?
- [User to complete]

What could reduce this risk?
- [User to complete]

Sources to monitor:
- Earnings transcripts
- Company Filings
- Investor presenations
- Sector news
"""
        category_risk_sections.append(section)

    content = f"""# Portfolio Risk Register - {today}

This file tracks portfolio-level risks that may affect multiple holdings.

## How to Use This File

For each risk theme:
1. Identify affected holdings.
2. Describe why the risk matters.
3. Define what evidence would increase or reduce the risk.
4. List sources to monitor.

---

{chr(10).join(category_risk_sections)}

## Cross-Portfolio Risks

### Concentration Risk

Description:
- [User to complete]

Holdings to monitor:
- [User to complete]

### Valuation Risk

Description:
- [User to complete]

Holdings to monitor:
- [User to complete]

### Macro / Interest Rate Risk

Description:
- [User to complete]

Holdings to monitor:
- [User to complete]

### Liquidity / Position Sizing Risk

Description:
- [User to complete]

Holdings to monitor:
- [User to complete]
"""

    return content

def build_holding_thesis_content(holding_row: pd.Series) -> str:
    # Builds srarter thesis conetent for inddividual holdings based on ticker and company name
    today = datetime.now().strftime("%Y-%m-%d")

    ticker = holding_row.get("ticker", "").upper()
    company = holding_row.get("company", "").upper()
    category = holding_row.get("category", "").upper()
    asset_type = holding_row.get("asset_type", "").upper()
    shares = holding_row.get("shares", 0)
    current_price = holding_row.get("current_price", 0)
    market_value = holding_row.get("market_value", 0)
    portfolio_weight = holding_row.get("portfolio_weight_percent", 0)

    content = f"""{ticker} Thesis

Generated {today}

## Company / Asset

Ticker: {ticker}
Company: {company}
Category: {category}
Asset Type: {asset_type}

## Current Position Snapshot

Shares: {shares}
Current Price: {format_currency(current_price)}
Market Value: {format_currency(market_value)}
Portfolio Weight: {format_percent(portfolio_weight)}

## Position Role

Role in portfolio:
- [Core / Growth / Speculative / Defensive / ETF / Thematic]

Conviction level:
- [High / Medium / Low]

Intended holding period:
- [Short-term / Medium-term / Long-term]

## Why I Own It

Primary reasons:
- [User to complete]
- [User to complete]
- [User to complete]

What I believe needs to be true:
- [User to complete]
- [User to complete]
- [User to complete]

## Bull Case

What could go right:
- [User to complete]
- [User to complete]

Key catalysts:
- [User to complete]
- [User to complete]

## Bear Case

What could go wrong:
- [User to complete]
- [User to complete]

What would weaken the thesis:
- [User to complete]
- [User to complete]

## Key Risks

Business risks:
- [User to complete]

Valuation risks:
- [User to complete]

Competitive risks:
- [User to complete]

Macro risks:
- [User to complete]

Portfolio-specific risks:
- [User to complete]

## What Would Make Me Add

- [User to complete]
- [User to complete]

## What Would Make Me Reduce or Exit

- [User to complete]
- [User to complete]

## What I Need to Research Next

- [User to complete]
- [User to complete]

## Last Reviewed

Date:
Notes:
"""

    return content


def create_portfolio_thesis_file(holdings: pd.DataFrame) -> None:
    # Creates portfolio_thesis.md file if it does not already exist

    content = build_portfolio_thesis_content(holdings)
    safe_write_file(PORTFOLIO_THESIS_FILE, content)


def create_risk_register_file(holdings: pd.DataFrame) -> None:
    # Creates risk_register.md file if it does not already exist

    content = build_risk_register_content(holdings)
    safe_write_file(RISK_REGISTER_FILE, content)

def create_holdings_thesis_files(holdings: pd.DataFrame) -> None:
    # Create one thesis file per holding in holdings.csv if it does not already exist
    for _, row in holdings.iterrows():
        ticker = str(row["ticker"]).upper().strip()
        file_path = HOLDINGS_THESIS_DIR / f"{ticker}.md"
        content = build_holding_thesis_content(row)
        safe_write_file(file_path, content)


def main():
    print("\nLoading Holdings...")
    holdings = load_holdings()

    print("\nFetching Current Prices...")
    holdings = fetch_prices_for_holdings(holdings)

    #Debug function:
    print("\nColumns after fetch_prices_for_holdings():")
    print(holdings.columns.tolist())

    print("\nPreview:")
    print(holdings.head())
    
    #Debuf funciton end

    print("Creating Thesis Workspace...")
    create_directory_structure()

    print("Creating portfolio thesis file...")
    create_portfolio_thesis_file(holdings)

    print("Creating risk register file...:")
    create_risk_register_file(holdings)

    print("create indivdiual holding thesis files...")
    create_holdings_thesis_files(holdings)

    print("\nResearch workspace setup complete:")









if __name__ == "__main__":
    main()