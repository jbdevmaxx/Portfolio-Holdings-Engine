import pandas as pd
from pathlib import Path
from datetime import datetime

from portfolio_summary import load_holdings, print_category_percentages
from fetch_prices import fetch_prices_for_holdings

from utils.formatting import format_currency, format_percent

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs" / "daily_reports"


def build_top_holdings_table(holdings: pd.DataFrame, top_n: int = 10) -> str:
    # BUilds a markdown table showing top holdings by portfolio weight

    required_columns = {
        "ticker",
        "company",
        "shares",
        "current_price",
        "market_value",
        "portfolio_weight_percent"
    }

    missing_columns = required_columns - set(holdings.columns)
    
    if missing_columns:
        return f"Missing columns for top holdings table: {missing_columns}"

    top_holdings = holdings.sort_values(by="portfolio_weight_percent", ascending=False).head(top_n)

    lines = []
    lines.append("| Ticker | Company | Shares | Current Price | Market Value | Portfolio Weight % |")
    lines.append("|--------|---------|--------|---------------|--------------|--------------------|")

    for _, row in top_holdings.iterrows():
        lines.append(
            f"| {row['ticker']} "
            f"| {row['company']} "
            f"| {row['shares']:.4g} "
            f"| {format_currency(row['current_price'])} "
            f"| {format_currency(row['market_value'])} "
            f"| {format_percent(row['portfolio_weight_percent'])} |"
        )

    return "\n".join(lines)

def build_category_allocation_table(holdings: pd.DataFrame) -> str:
    # Builds a markdown table showing category allocation percentages

    required_columns = {"category", "market_value"}

    missing_columns = required_columns - set(holdings.columns)
    if missing_columns:
        return f"Missing columns for category allocation table: {missing_columns}"

    total_market_value = holdings["market_value"].sum()

    if total_market_value <= 0:
        return "Total market value is 0. Cannot calculate category allocation."

    category_summary = (
        holdings.groupby("category", dropna=False)["market_value"].sum().reset_index()
    )

    category_summary["portfolio_weight_percent"] = (
        category_summary["market_value"] / total_market_value * 100
    )

    category_summary = category_summary.sort_values(
        by="portfolio_weight_percent",
        ascending=False
    )

    lines = []
    lines.append("| Category | Market Value | Portfolio Weight % |")
    lines.append("|----------|--------------|--------------------|")

    for _, row in category_summary.iterrows():
        category = row["category"] if pd.notna(row["category"]) else "Uncategorized"
        lines.append(
            f"| {category} "
            f"| {format_currency(row['market_value'])} "
            f"| {format_percent(row['portfolio_weight_percent'])} |"
        )       

    return "\n".join(lines)

def build_full_holdings_table(holdings: pd.DataFrame) -> str:
    #Build a Markdown table showing all holdings.

    required_columns = {
        "ticker",
        "company",
        "shares",
        "current_price",
        "market_value",
        "portfolio_weight_percent"
    }

    missing_columns = required_columns - set(holdings.columns)
    if missing_columns:
        return f"Missing columns for full holdings table: {missing_columns}"

    sorted_holdings = holdings.sort_values(
        by="portfolio_weight_percent",
        ascending=False
    )

    lines = []
    lines.append("| Ticker | Company | Category | Shares | Price | Market Value | Weight |")
    lines.append("|---|---|---|---:|---:|---:|---:|")

    for _, row in sorted_holdings.iterrows():
        lines.append(
            f"| {row['ticker']}"
            f"| {row['company']}"
            f"| {row['category']}"
            f"| {row['shares']:.4g}"
            f"| {format_currency(row['current_price'])}"
            f"| {format_currency(row['market_value'])}"
            f"| {format_percent(row['portfolio_weight_percent'])} |"
        )
        

    return "\n".join(lines)

def generate_daily_report(holdings: pd.DataFrame) -> str:

    # Generates the full mMarkdown daily portfolio report as a string

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_market_value = holdings["market_value"].sum() 

    top_holdings_table = build_top_holdings_table(holdings)
    category_allocation_table = build_category_allocation_table(holdings)
    full_holdings_table = build_full_holdings_table(holdings)

    report = f"""# Daily Portfolio Report - {today}


Generated: {timestamp}

## Portfolio Overview

Total Portfolio Value: **{format_currency(total_market_value)}**

This report uses the latest available price data retrieved through the project's price retrieval function.

---

## Top Holdings by Portfolio Weight

{top_holdings_table}

---

## Category Allocation

{category_allocation_table}

---

## Full Holdings Table

{full_holdings_table}

---

## NotebookLM Questions

Use these questions when uploading this report into NotebookLM:

1. Which holdings represent the largest concentration risk?
2. Which categories dominate the portfolio?
3. Which holdings should be prioritized for news and earnings review?
4. Are there any positions that appear too small to materially affect the portfolio?
5. Which holdings should have thesis notes reviewed next?
6. What portfolio risks are visible based only on allocation?

---

## Notes

This report is for personal research and workflow automation only. It is not financial advice.
"""

    return report

def save_daily_report(report: str) -> Path:
    # Save the markdown report to outputs/daily reports

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"daily_report_{today}.md"

    output_file.write_text(report, encoding="utf-8")

    return output_file




def main():
    print("\nLoaading holdings...")
    holdings = load_holdings()

    print("Fetching current prices and calculating market values...")
    holdings = fetch_prices_for_holdings(holdings)

    print("\nGenerating daily Markdown report...")
    report = generate_daily_report(holdings)

    output_file = save_daily_report(report)

    print(f"\nDaily report generated and saved to: {output_file}")
    print(output_file)


if __name__ == "__main__":
    main()