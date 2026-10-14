## Description

This project aggregates development indicators for Jordan and three comparator countries (Egypt, Lebanon, Saudi Arabia) from three public data sources into a single, explorable dataset. It lets users look for trends across different years and compare how these indicators have evolved, surfacing patterns that would otherwise require manually cross-referencing multiple separate sources. It also includes an AI-powered Q&A feature that answers natural-language questions grounded in the actual filtered data shown on the dashboard. Rather than a generic chatbot, it retrieves real evidence before answering and is upfront when the data doesn’t support a question.

## Architecture

```mermaid
flowchart LR
    A[World Bank WDI] --> D[Python ETL Scripts]
    B[UNDP HDR] --> D
    C[Jordan DOS] --> D
    D --> E[(PostgreSQL)]
    E --> F[Streamlit Dashboard]
    F -->|filtered data + question| G[Gemini API]
    G -->|AI answer| F
```
## Tech Stack

- **Python** — ETL scripts and data processing (pandas)
- **PostgreSQL** — relational database storing the cleaned, merged indicator data
- **psycopg2** — Python-to-PostgreSQL connector
- **SQLAlchemy** — connection pooling and automatic reconnection (`pool_pre_ping`) on top of psycopg2, so the app recovers cleanly if the database connection goes stale (e.g. a hosted Postgres provider suspending an idle connection)
- **Streamlit** — interactive dashboard UI
- **Google Gemini API** (gemini-3.5-flash-lite) AI Q&A feature, grounded in the filtered dashboard data
- **Git/GitHub** — version control

## Setup & Running Locally

1. Clone the repo and install dependencies:
    - git clone https://github.com/alshalabiraghad/jordan-dev-data-explorer.git
    - cd jordan-dev-data-explorer
    - pip install -r requirements.txt

2. Set up a PostgreSQL database (two options):
   - **Option A — local Postgres**: create a database (e.g. `createdb jordan_dev_data`), then build your own connection string: `postgresql://postgres:your_password@localhost/jordan_dev_data`.
   - **Option B — hosted Postgres (e.g. Neon)**: create a free [Neon](https://neon.tech) project and copy its **pooled** connection string (the one with `-pooler` in the hostname).
   - Either way, run the schema against it: `psql "<your connection string>" -f schema.sql`

3. Create a `.env` file in the project root with:
    - DATABASE_URL=<your connection string from step 2>
    - GEMINI_API_KEY=your_gemini_api_key

4. Run the data processing scripts, then load the data into Postgres:
    - python explore_data.py
    - python explore_dos_data.py
    - python explore_hdr_data.py
    - python load_to_db.py

5. Launch the dashboard:
    - streamlit run app.py

## Data Sources & Methodology

This project aggregates development indicators for Jordan and three comparator countries (Egypt, Lebanon, Saudi Arabia) from three public sources:
- **World Bank World Development Indicators (WDI)**
- **UNDP Human Development Reports (HDR)**
- **Jordan Department of Statistics (DOS)**

Data cleaning steps, known gaps (missing years, staggered indicator coverage across sources, a UTF-8 BOM issue, etc.), and full methodology notes are documented in [`data_notes.md`](./data_notes.md).

## AI Q&A Feature & Responsible AI

The dashboard includes an AI-powered Q&A feature that answers natural-language questions grounded in the data currently filtered on the dashboard, rather than a general-purpose chatbot. It retrieves the filtered data as evidence before answering, and is upfront when the data doesn't support a question.

See [`RESPONSIBLE_AI.md`](./RESPONSIBLE_AI.md) for a full breakdown of how this feature was built with responsible AI practices in mind. Covering hallucination mitigation, bias, data quality, privacy, transparency, limitations, and appropriate use.

## Limitations

- **Country coverage**: the project covers only 4 countries (Jordan, Egypt, Lebanon, Saudi Arabia), chosen for relevance rather than statistical representativeness. Trends and comparisons are only valid relative to these specific countries, not the region or world more broadly.
- **Data source limitations**: the underlying data comes from self-reported national statistics (World Bank WDI, UNDP HDR, Jordan DOS), which can differ in measurement methodology across countries and carry some incentive for favorable reporting. Specific gaps (missing years, staggered indicator coverage, and data cleaning issues) are documented in [`data_notes.md`](./data_notes.md).
- **AI feature scope**: the AI Q&A feature only answers using the data currently filtered on the dashboard (one indicator, selected countries/years at a time), not the full dataset. It can't yet answer questions comparing multiple indicators to each other. It's also not fully reliable for arithmetic, and its instruction-following isn't a hard guarantee. Full details are in [`RESPONSIBLE_AI.md`](./RESPONSIBLE_AI.md).
- **Platform-specific dependency generation**: `requirements.txt` was generated via `pip freeze` on Windows, which can silently include Windows-only packages (e.g. `pywinpty`) that fail to build on Linux-based hosting. These are commented out for deployment. See the note in Setup & Running Locally if running locally on Windows and you want that functionality back.
- **No causal analysis**: the dashboard surfaces trends and comparisons, not causal relationships. A visible correlation between two indicators doesn't imply one causes the other.

## Future Work

- **Multi-indicator AI queries**: extend the AI Q&A feature to read across the whole dataset rather than only the currently filtered indicator, so users can ask questions comparing two or more indicators to each other (e.g. "how does youth unemployment relate to GDP growth in Jordan?"), not just questions about a single filtered indicator.
- **UI polish**: wide-layout page config, sidebar-based filters, and more stable chart colors across re-renders.
- **Configurable database connection**: move the hardcoded database name/user/host into environment variables so the project runs on any local Postgres setup without code changes.

## Screenshots

### Dashboard
![Dashboard view showing filtered indicator trends](./screenshots/dashboard.png)

### AI Q&A Feature
![AI Q&A feature answering a question grounded in filtered data](./screenshots/ai_qa.png)

