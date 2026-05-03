
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
- `setup_research_workspace.py`
- `utils.py`


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

## Decision 7: Exclude Generated Outputs and Personal Research Files from Git

### Decision

Add `outputs/` and `thesis` to `.gitignore`.

### Reasoning

Generated reports may contain personal investment reasoning, risk notes, portfolio theses, and holding-level research notes. These files are useful locally but may contain sensitive or personal financial information.

### Benefits

- Protects personal financial data
- Keeps repository clean and safe 
- Avoids unnecessary generated-file commits
- Protects personal investment reasoning
- Separates reusable code from private research content
- Prevents accidental commits of personal thesis notes

### Tradeoffs

- Generated reports are not synced across computers
- Reports must be regenerated locally

### Future Option

Create sanitized thesis examples under an `examples/` or `templates/` folder for public demos.

Example:

```text
templates/
├── portfolio_thesis_template.md
├── risk_register_template.md
└── holding_thesis_template.md
```


## Decision 8: Create an Initial Research Workspace Setup Script

### Decision

Add `scripts/setup_research_workspace.py` to genreate a local research workspace from `data/holdings.csv`

The script creates:
- `thesis/portfolio_thesis.md`
- `thesis/risk_register.md`
- `thesis/holdings/TICKER.md` for each holding

### Reasoning

Users should be able to start with only a hodlings CSV and generate the folder structure needed for thesis tracking, risk review, and future NotebookLM or AI-assisted analysis.

This supports an onboarding workflow:

```text
holdings.csv
    ↓
fetch latest prices
    ↓
calculate portfolio weights
    ↓
generate thesis and risk templates

```

### Benefits

- Makes the project easier to initialize
- Creates repeatable structure for every holding
- Turns the project from simple reporting script into a research operating system
- Supports future use with NotebookLM, Notion, or AI APIs
- Reduces manual setup work

### Tradeoffs

- Create more files and folders
- Requires the user to understand which generated files are personal/local
- Thesis templates still require manual completion

### Future option

The setup script could later support command-line options such as:

```text
python scripts/setup_research_workspace.py --overwrite
python scripts/setup_research_workspace.py --ticker NVDA
python scripts/setup_research_workspace.py --template advanced
```

## Decision 9: Keep Thesis Generation Human in the Loop

### Decision

The setup script creates thesis templates with [User to complete] placeholders instead of automatically inventing investment theses.

### Reasoning

Investment thesis content is subjective and should reflect the user's actual reasoning. Automatically generating confident-sounding theses could create false conviction or misleading research notes.

The system should structure the user's thinking, not replace it.

### Benefits

- Keeps the workflow honest
- Avoids fake AI-generated conviction
- Encourages the user to document their own reasoning
- Makes the project more useful for decision discipline
- Reduces risk of treating generated text as financial advice

### Tradeoffs

- Requires manual work from the user
- The generated thesis files are incomplete at first
- The system becomes more useful only after the user fills in the templates

### Future Option

An AI assistant could later suggest draft thesis questions or summarize uploaded source material, but the user should still approve and edit the final thesis.

## Decision 10: Centralize Shared Utility Functions

### Decision

Move common formatting or reusable helper functions into a shared utility file instead of duplicating them across scripts.

The project currently seperates utilities by responsiblity:

```text
utils/
├── formatting.py
├── file_utils.py
└── markdown_utils.py
```

### Reasoning

As the project grows, multiple scripts need the same formatting, file-writing, and Markdown-generation behavior. Duplicating these helpers across scripts increases maintenance risk and makes bugs more likely.

Centralizing these helpers keeps the main workflow scripts focused on their actual responsibilities:

- fetch_prices.py handles price retrieval and enriched holdings data
- portfolio_summary.py handles allocation summaries
- generate_daily_reports.py handles daily report generation
- setup_research_workspace.py handles thesis and risk workspace creation
- utils/ handles generic reusable support functions

### Benefits

- Reduces repeated code
- Makes scripts easier to maintain
- Creates more consistent output formatting
- Makes future refactoring easier
- Makes future AI-assisted thesis generation easier to support

### Tradeoffs

- Adds another file/module to understand
- Requires scripts to import shared functions correctly
- Can create import errors if files are moved or run from the wrong directory


### Future Options

The project could later be reorganized into a package structure:

```text
src/
└── portfolio_research_engine/
    ├── data_loader.py
    ├── price_provider.py
    ├── portfolio_metrics.py
    ├── report_generator.py
    ├── thesis_generator.py
    └── utils/
        ├── formatting.py
        ├── file_utils.py
        └── markdown_utils.py

```

Future utility modules could include:

- `date_utils.py` for timestamp and date helpers
- `dataframe_utils.py` for column normalization and validation
- `prompt_utils.py` for future AI prompt templates

## Decision 11: Reuse Price Retrieval Logic Across Workflows

### Decision

Use `fetch_prices_for_holdings()` as the central price-enrichment function for multiple workflows, including portfolio summaries, daily reports, and research workspace setup.

### Reasoning

Multiple scripts need the same enriched holdings data:

- latest price
- previous close
- market value
- portfolio weight
- price status

Rather than duplicating price-fetching and allocation logic, the project should reuse one function.

### Benefits:

- One place to update price retrieval logic
- Easier future migration away from yfinance
- More consistent calculations across reports and thesis templates
- Reduces bugs caused by mismatched column names

### Tradeoffs:

- Downstream scripts depend on consistent output columns
- Changes to fetch_prices_for_holdings() can affect multiple workflows
- Requires clear documentation of expected returned columns

### Expected Output Columns

`fetch_prices_for_holdings()` should return an enriched DataFrame with:

///text
current_price
previous_close
currency
price_timestamp
price_status
market_value
portfolio_weight_percent

///

### Future Option

Create a formal data validation step to confirm required columns exist before downstream scripts run

## Decision 13: Use Safe File Creation for Research Notes

### Decision

Generated thesis and risk files should be created only if they do not already exist.

### Reasoning

Once a user fills out thesis notes manually, rerunning the setup script should not overwrite their work.

### Benefits

- Protects user-written research notes
- Makes the setup script safe to rerun
- Reduces risk of accidental data loss
- Supports iterative project usage

### Tradeoffs

- Existing files will not receive updated template changes automatically
- Useres may need a manual update process for old templates

### Future Option

Add optional overwrite or backup behavior:

```text
python scripts/setup_research_workspace.py --overwrite
python scripts/setup_research_workspace.py --backup-existing

```

