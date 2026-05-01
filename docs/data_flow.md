# Portfolio Research Engine — Data Flow

## Purpose

This document explains how data moves through the Portfolio Research Engine from the source holdings file to the generated daily Markdown report.

The goal is to make the system easy to understand, debug, and extend.

## High-Level Data Flow

```text
holdings.csv
    ↓
load_holdings()
    ↓
holdings DataFrame
    ↓
fetch_prices_for_holdings()
    ↓
enriched holdings DataFrame
    ↓
generate_daily_report()
    ↓
daily_report_YYYY-MM-DD.md