# Bluestock Mutual Fund Analytics Capstone

End-to-end mutual fund analytics project completed for the Bluestock Fintech Data Analyst internship capstone. The project combines 10 mutual-fund datasets, live NAV history, ETL processing, SQLite warehousing, exploratory analysis, risk/performance metrics, advanced analytics, and a Power BI dashboard.

## Project Objectives

1. Ingest and profile all provided mutual fund datasets.
2. Fetch selected live NAV histories from mfapi.in.
3. Clean and standardize raw data for analytics.
4. Design a star-schema SQLite analytical database.
5. Perform EDA on NAV, AUM, SIP inflows, investor transactions, folios, and categories.
6. Calculate fund performance metrics including CAGR, Sharpe, Sortino, Alpha, Beta, tracking error, drawdown, VaR and CVaR.
7. Build dashboard pages for industry overview, fund performance, investor analytics, and SIP/market trends.
8. Deliver a professional report, presentation, clean scripts, and final release package.

## Repository Structure

```text
data/
  raw/                 Original datasets and live NAV CSV files
  processed/           Cleaned datasets and analytical outputs
  db/                  SQLite database: bluestock_mf.db
notebooks/             EDA, performance and advanced analytics notebooks
scripts/               Clean Python scripts and run_pipeline.py
sql/                   schema.sql and queries.sql
reports/               Final report, dashboard PDF, screenshots and charts
```

## Setup Instructions

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
```

## How to Run the ETL Pipeline

Run from the project root:

```bash
python scripts/run_pipeline.py
```

To also fetch fresh live NAV files from mfapi.in:

```bash
python scripts/run_pipeline.py --fetch-live-nav
```

The ETL creates cleaned CSV files in `data/processed/` and loads the SQLite database at `data/db/bluestock_mf.db`.

## How to Open the Dashboard

The submitted dashboard is available as a PDF export and screenshots:

- `reports/bluestock_mf_dashboard.pdf`
- `reports/dashboard_page1.png` - Industry Overview
- `reports/dashboard_page2.png` - Fund Performance
- `reports/dashboard_page3.png` - Investor Analytics
- `reports/dashboard_page4.png` - SIP & Market Trends

Open the dashboard PDF directly, or use the screenshots inside the final report and presentation.

## Dataset Descriptions

| Dataset | Description |
|---|---|
| 01_fund_master.csv | Fund metadata including scheme names, fund house, category, launch date and expenses |
| 02_nav_history.csv | Historical NAV values used for returns and trend analysis |
| 03_aum_by_fund_house.csv | AMC-wise AUM and scheme counts |
| 04_monthly_sip_inflows.csv | Monthly SIP inflow, account and index trend data |
| 05_category_inflows.csv | Monthly net inflows by mutual fund category |
| 06_industry_folio_count.csv | Industry folio growth over time |
| 07_scheme_performance.csv | Fund-level return, risk and rating metrics |
| 08_investor_transactions.csv | Investor transactions by state, age group, type and amount |
| 09_portfolio_holdings.csv | Portfolio holdings and sector allocations |
| 10_benchmark_indices.csv | Benchmark index history for comparison and beta calculations |

## Final Deliverables

- `Final_Report.pdf`
- `Bluestock_MF_Presentation.pptx`
- Cleaned Python scripts with docstrings
- `scripts/run_pipeline.py`
- SQLite database and processed datasets
- Dashboard PDF and screenshots
- Self-review checklist

## Git Release Commands

```bash
git add .
git commit -m "Final: Complete Bluestock MF Capstone"
git tag v1.0
git push
git push origin v1.0
```

## Notes

Dashboard publishing to Power BI Service or Tableau Public is optional. Add the published dashboard URL here after uploading it:

`Dashboard URL: Not published / optional`

## Final Deliverable Mapping

| ID | Deliverable | Location |
|---|---|---|
| D1 | ETL pipeline script | `scripts/etl_pipeline.py`, `scripts/run_pipeline.py` |
| D2 | SQLite database | `data/db/bluestock_mf.db`; schema in `sql/schema.sql` |
| D3 | EDA notebook | `notebooks/03_eda_analysis.ipynb` |
| D4 | Performance metrics | `notebooks/04_performance_analytics.ipynb`, CSVs in `data/processed/` |
| D5 | Interactive dashboard export | `dashboard/bluestock_mf_dashboard.pdf` + page screenshots |
| D6 | Advanced analytics | `notebooks/05_advanced_analytics.ipynb`, `scripts/recommender.py` |
| D7 | Final report + slides | `reports/Final_Report.pdf`, `reports/Presentation.pptx` |

## Bonus Challenge Files

- B1: `bonus/weekday_nav_cron.txt`
- B2: `bonus/streamlit_app.py`
- B3: `bonus/monte_carlo_nav.py`
- B4: `bonus/efficient_frontier.py`
- B5: `bonus/weekly_email_report.py`

## GitHub Submission Note

The SQLite database is included in this ZIP for evaluation, but `.gitignore` contains `*.db` and `*.sqlite` so database binaries are not pushed to GitHub. Share `sql/schema.sql` in the repository and submit the `.db` file separately if required.
