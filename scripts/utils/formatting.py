import pandas as pd

def format_currency(value: float) -> str:
    """Format a number as USD currency."""
    if pd.isna(value):
        return "$0.00"
    return f"${value:,.2f}"


def format_percent(value: float) -> str:
    if pd.isna(value):
        return "0.0%"
    return f"{value:.2f}%"