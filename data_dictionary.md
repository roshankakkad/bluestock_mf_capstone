# Data Dictionary - Bluestock Mutual Fund Analytics Capstone

## Source Files

| File | Description | Source Folder |
|---|---|---|
| 01_fund_master.csv | Master details of mutual fund schemes | data/raw |
| 02_nav_history.csv | Daily NAV history by AMFI code | data/raw |
| 03_aum_by_fund_house.csv | Fund-house level quarterly AUM | data/raw |
| 04_monthly_sip_inflows.csv | Monthly SIP inflows and SIP account metrics | data/raw |
| 05_category_inflows.csv | Monthly net inflow by mutual fund category | data/raw |
| 06_industry_folio_count.csv | Industry folio count by category | data/raw |
| 07_scheme_performance.csv | Scheme-level return and risk metrics | data/raw |
| 08_investor_transactions.csv | Investor transaction records | data/raw |
| 09_portfolio_holdings.csv | Scheme-level top portfolio holdings | data/raw |
| 10_benchmark_indices.csv | Daily benchmark index values | data/raw |

## Table: dim_fund

| Column | Type | Business Definition |
|---|---|---|
| amfi_code | TEXT | Unique AMFI scheme code used to join scheme-level datasets |
| fund_house | TEXT | Asset Management Company name |
| scheme_name | TEXT | Official scheme name |
| category | TEXT | Broad fund category such as Equity, Debt, or Hybrid |
| sub_category | TEXT | SEBI-style sub-category such as Large Cap, Liquid, ELSS |
| plan | TEXT | Direct or Regular plan |
| launch_date | DATE | Scheme launch date |
| benchmark | TEXT | Benchmark index assigned to the scheme |
| expense_ratio_pct | REAL | Annual expense ratio in percentage |
| exit_load_pct | REAL | Exit load percentage |
| min_sip_amount | REAL | Minimum SIP investment amount |
| min_lumpsum_amount | REAL | Minimum lumpsum investment amount |
| fund_manager | TEXT | Primary fund manager |
| risk_category | TEXT | Risk grade such as Low, Moderate, High, Very High |
| sebi_category_code | TEXT | Internal SEBI category code |

## Table: dim_date

| Column | Type | Business Definition |
|---|---|---|
| date_id | INTEGER | Date key in YYYYMMDD format |
| date | DATE | Calendar date |
| year | INTEGER | Calendar year |
| month | INTEGER | Calendar month number |
| month_name | TEXT | Month name |
| quarter | INTEGER | Calendar quarter |
| is_weekday | BOOLEAN | Indicates whether date is Monday-Friday |

## Table: fact_nav

| Column | Type | Business Definition |
|---|---|---|
| amfi_code | TEXT | Scheme code linked to dim_fund |
| date | DATE | NAV date |
| nav | REAL | Net Asset Value in rupees |
| daily_return_pct | REAL | Daily percentage return calculated from NAV movement |

## Table: fact_transactions

| Column | Type | Business Definition |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | DATE | Date of transaction |
| amfi_code | TEXT | Scheme code linked to dim_fund |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption |
| amount_inr | REAL | Transaction amount in Indian rupees |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| city_tier | TEXT | T30 or B30 city classification |
| age_group | TEXT | Investor age band |
| gender | TEXT | Investor gender category |
| annual_income_lakh | REAL | Annual income in Rs. lakh |
| payment_mode | TEXT | Mode of payment |
| kyc_status | TEXT | KYC status, Verified or Pending |

## Table: fact_performance

| Column | Type | Business Definition |
|---|---|---|
| amfi_code | TEXT | Scheme code linked to dim_fund |
| return_1yr_pct | REAL | One-year return percentage |
| return_3yr_pct | REAL | Three-year CAGR percentage |
| return_5yr_pct | REAL | Five-year CAGR percentage |
| benchmark_3yr_pct | REAL | Benchmark three-year CAGR percentage |
| alpha | REAL | Excess return over benchmark |
| beta | REAL | Market sensitivity measure |
| sharpe_ratio | REAL | Risk-adjusted return metric |
| sortino_ratio | REAL | Downside-risk-adjusted return metric |
| std_dev_ann_pct | REAL | Annualised standard deviation percentage |
| max_drawdown_pct | REAL | Maximum peak-to-trough fall percentage |
| aum_crore | REAL | Scheme AUM in crore |
| expense_ratio_pct | REAL | Annual expense ratio percentage |
| morningstar_rating | INTEGER | Rating from 1 to 5 |
| expense_ratio_anomaly | BOOLEAN | True if expense ratio falls outside 0.1%-2.5% range |
| negative_sharpe_flag | BOOLEAN | True if Sharpe ratio is negative |
| high_beta_flag | BOOLEAN | True if absolute beta is greater than 2 |

## Table: fact_aum

| Column | Type | Business Definition |
|---|---|---|
| date | DATE | AUM reporting date |
| fund_house | TEXT | Asset Management Company name |
| aum_lakh_crore | REAL | AUM in Rs. lakh crore |
| aum_crore | REAL | AUM in Rs. crore |
| num_schemes | INTEGER | Number of schemes managed by the fund house |

## Cleaning Notes

- Dates were parsed using Pandas `to_datetime()`.
- NAV records were sorted by `amfi_code` and `date`.
- NAV values were forward-filled after reindexing to daily calendar dates.
- Duplicate rows were removed.
- NAV and transaction amount values were validated to be greater than zero.
- Transaction types were standardised to SIP, Lumpsum, and Redemption.
- KYC status was checked against Verified and Pending.
- Scheme performance numeric columns were converted to numeric types.
- Expense ratio anomalies were flagged where values were outside 0.1% to 2.5%.
