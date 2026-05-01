
# Portfolio Research Engine — Technical Decisions

## Purpose

This document records key technical decisions made during development. The goal is to explain not only what the system does, but why certain design choices were made.

This is useful for long-term maintainability and for explaining the project as an architecture case study.

## Decision 1: Use CSV as the Initial Source of Truth

### Decision

Use `data/holdings.csv` as the manually maintained source of truth for portfolio holdings.

### Reasoning

A CSV is simple, transparent, and easy to edit manually. It avoids the complexity of brokerage API integration during the early MVP stage.

### Benefits

- Easy to inspect
- Easy to edit in Excel or VS Code
- Simple to load with pandas
- Works across Mac and Windows
- Avoids brokerage authentication complexity

### Tradeoffs

- Manual updates are required
- No automatic syncing with brokerage accounts
- Potential for user input errors

### Future Option

A future version could connect to a brokerage API or portfolio aggregation service.

---

## Decision 2: Keep Source Data Separate from Generated Outputs

### Decision

Keep `data/holdings.csv` separate from files generated in `outputs/`.

### Reasoning

The holdings file represents user-maintained source data. Generated reports are temporary or historical outputs created by scripts.

### Benefits

- Prevents scripts from accidentally overwriting the source of truth
- Keeps Git history cleaner
- Makes generated files easier to ignore
- Reduces risk of committing personal financial information

### Tradeoffs

- Requires multiple folders
- Users need to understand which files are inputs and which are outputs

---

## Decision 3: Use `yfinance` for Initial Price Retrieval

### Decision

Use `yfinance` as the initial price retrieval provider.

### Reasoning

`yfinance` is easy to install, easy to use, and sufficient for a personal MVP.

### Benefits

- Free
- Simple Python interface
- Fast to prototype
- Works well for basic personal research

### Tradeoffs

- Not a production-grade commercial data provider
- May have reliability limitations
- May not be appropriate for a consumer-facing paid product
- Data availability and behavior may change over time

### Future Option

If the project becomes consumer-facing or commercial, the price provider should be replaced with a more formal financial data API such as:

- Finnhub
- Financial Modeling Prep
- Tiingo
- Polygon/Massive

---

## Decision 4: Generate Markdown Reports

### Decision

Generate daily reports as Markdown files.

### Reasoning

Markdown is lightweight, readable, easy to store, and compatible with many tools.

### Benefits

- Human-readable
- Easy to upload into NotebookLM
- Easy to paste into Notion or documentation
- Easy to version if sanitized
- Simple to generate from Python

### Tradeoffs

- Not interactive
- Requires manual upload to NotebookLM for now
- Not a full dashboard experience

### Future Option

Future outputs could include:

- HTML reports
- PDF reports
- Notion pages
- Email summaries
- Web dashboard

---

## Decision 5: Use NotebookLM as a Manual Research Workspace

### Decision

Use NotebookLM manually rather than automating NotebookLM integration at the current stage.

### Reasoning

NotebookLM is useful for source-grounded analysis, but consumer NotebookLM automation is not the most reliable first integration target.

### Benefits

- Keeps workflow simple
- Allows manual review of generated reports
- Helps validate report quality before automation
- Avoids fragile unofficial browser automation

### Tradeoffs

- Manual upload required
- Not fully automated
- Daily workflow requires user involvement

### Future Option

For automation, a model API such as Gemini, Claude, or OpenAI may be more appropriate than trying to automate consumer NotebookLM directly.

---

## Decision 6: Use Modular Python Scripts

### Decision

Separate functionality across multiple scripts:

- `update_holdings.py`
- `fetch_prices.py`
- `portfolio_summary.py`
- `generate_daily_reports.py`

### Reasoning

Each script should have a focused responsibility.

### Benefits

- Easier to debug
- Easier to reuse functions
- Easier to replace components later
- Better project structure
- More aligned with real software engineering practices

### Tradeoffs

- Slightly more complexity than one large script
- Requires understanding imports between files

### Future Option

The project could later be refactored into a proper Python package under a `src/` directory.

---

## Decision 7: Exclude Generated Outputs from Git

### Decision

Add `outputs/` to `.gitignore`.

### Reasoning

Generated reports may contain personal portfolio information and should not be committed to the repository.

### Benefits

- Protects personal financial data
- Keeps repository clean
- Avoids unnecessary generated-file commits

### Tradeoffs

- Generated reports are not synced across computers
- Reports must be regenerated locally

### Future Option

Create sanitized sample outputs under an `examples/` folder for public demos or portfolio review.


