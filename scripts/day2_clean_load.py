"""Clean raw datasets, create analytical tables, and load the SQLite warehouse.

The script keeps the project logic from Day 2 unchanged: it cleans raw CSVs,
writes processed CSV files, builds dim_date, and loads tables into data/db/bluestock_mf.db.
"""

from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
try:
    from sqlalchemy import create_engine, text
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("data/db")
SQL_DIR = Path("sql")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "fund_master": "01_fund_master.csv",
    "nav_history": "02_nav_history.csv",
    "aum": "03_aum_by_fund_house.csv",
    "sip": "04_monthly_sip_inflows.csv",
    "category_inflows": "05_category_inflows.csv",
    "folio": "06_industry_folio_count.csv",
    "performance": "07_scheme_performance.csv",
    "transactions": "08_investor_transactions.csv",
    "portfolio": "09_portfolio_holdings.csv",
    "benchmark": "10_benchmark_indices.csv",
}


def read_csv(name):
    """Read a configured raw CSV file by logical dataset name."""
    return pd.read_csv(RAW_DIR / FILES[name])


def clean_fund_master():
    """Clean fund master records and standardize data types."""
    df = read_csv("fund_master")
    df = df.drop_duplicates().copy()
    df["amfi_code"] = df["amfi_code"].astype(str)
    df["launch_date"] = pd.to_datetime(df["launch_date"], errors="coerce")
    numeric_cols = ["expense_ratio_pct", "exit_load_pct", "min_sip_amount", "min_lumpsum_amount"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_nav_history():
    """Clean NAV history, fill daily gaps, and compute daily returns."""
    df = read_csv("nav_history")
    df = df.drop_duplicates().copy()
    df["amfi_code"] = df["amfi_code"].astype(str)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df = df.dropna(subset=["amfi_code", "date", "nav"])
    df = df[df["nav"] > 0]
    df = df.sort_values(["amfi_code", "date"])

    filled_frames = []
    for code, group in df.groupby("amfi_code"):
        group = group.set_index("date").sort_index()
        full_dates = pd.date_range(group.index.min(), group.index.max(), freq="D")
        group = group.reindex(full_dates)
        group["amfi_code"] = code
        group["nav"] = group["nav"].ffill()
        group.index.name = "date"
        filled_frames.append(group.reset_index())

    df = pd.concat(filled_frames, ignore_index=True)
    df["daily_return_pct"] = df.groupby("amfi_code")["nav"].pct_change() * 100
    df["daily_return_pct"] = df["daily_return_pct"].fillna(0)
    return df[["amfi_code", "date", "nav", "daily_return_pct"]]


def clean_transactions():
    """Clean investor transaction records and standardize categories."""
    df = read_csv("transactions")
    df = df.drop_duplicates().copy()
    df["amfi_code"] = df["amfi_code"].astype(str)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")

    mapping = {
        "sip": "SIP", "SIP": "SIP",
        "lumpsum": "Lumpsum", "LumpSum": "Lumpsum", "LUMPSUM": "Lumpsum",
        "redemption": "Redemption", "REDEMPTION": "Redemption"
    }
    df["transaction_type"] = df["transaction_type"].map(lambda x: mapping.get(str(x).strip(), str(x).strip()))
    valid_types = ["SIP", "Lumpsum", "Redemption"]
    df = df[df["transaction_type"].isin(valid_types)]
    df = df[df["amount_inr"] > 0]
    df = df.dropna(subset=["transaction_date", "amount_inr", "amfi_code"])

    valid_kyc = ["Verified", "Pending"]
    df["kyc_status"] = df["kyc_status"].astype(str).str.strip().str.title()
    df = df[df["kyc_status"].isin(valid_kyc)]
    return df


def clean_performance():
    """Clean scheme performance metrics and add quality flags."""
    df = read_csv("performance")
    df = df.drop_duplicates().copy()
    df["amfi_code"] = df["amfi_code"].astype(str)
    numeric_cols = [
        "return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct",
        "alpha", "beta", "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct",
        "max_drawdown_pct", "aum_crore", "expense_ratio_pct", "morningstar_rating"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["expense_ratio_anomaly"] = ~df["expense_ratio_pct"].between(0.1, 2.5)
    df["negative_sharpe_flag"] = df["sharpe_ratio"] < 0
    df["high_beta_flag"] = df["beta"].abs() > 2
    return df


def clean_other_files():
    """Clean supporting industry, portfolio, SIP, folio and benchmark files."""
    cleaned = {}

    aum = read_csv("aum").drop_duplicates().copy()
    aum["date"] = pd.to_datetime(aum["date"], errors="coerce")
    for col in ["aum_lakh_crore", "aum_crore", "num_schemes"]:
        aum[col] = pd.to_numeric(aum[col], errors="coerce")
    cleaned["03_aum_by_fund_house_clean.csv"] = aum

    sip = read_csv("sip").drop_duplicates().copy()
    sip["month"] = pd.to_datetime(sip["month"], errors="coerce")
    for col in sip.columns.drop("month"):
        sip[col] = pd.to_numeric(sip[col], errors="coerce")
    cleaned["04_monthly_sip_inflows_clean.csv"] = sip

    cat = read_csv("category_inflows").drop_duplicates().copy()
    cat["month"] = pd.to_datetime(cat["month"], errors="coerce")
    cat["net_inflow_crore"] = pd.to_numeric(cat["net_inflow_crore"], errors="coerce")
    cleaned["05_category_inflows_clean.csv"] = cat

    folio = read_csv("folio").drop_duplicates().copy()
    folio["month"] = pd.to_datetime(folio["month"], errors="coerce")
    for col in folio.columns.drop("month"):
        folio[col] = pd.to_numeric(folio[col], errors="coerce")
    cleaned["06_industry_folio_count_clean.csv"] = folio

    port = read_csv("portfolio").drop_duplicates().copy()
    port["amfi_code"] = port["amfi_code"].astype(str)
    port["portfolio_date"] = pd.to_datetime(port["portfolio_date"], errors="coerce")
    for col in ["weight_pct", "market_value_cr", "current_price_inr"]:
        port[col] = pd.to_numeric(port[col], errors="coerce")
    cleaned["09_portfolio_holdings_clean.csv"] = port

    bench = read_csv("benchmark").drop_duplicates().copy()
    bench["date"] = pd.to_datetime(bench["date"], errors="coerce")
    bench["close_value"] = pd.to_numeric(bench["close_value"], errors="coerce")
    bench = bench.dropna(subset=["date", "index_name", "close_value"])
    cleaned["10_benchmark_indices_clean.csv"] = bench

    return cleaned


def create_dim_date(*dataframes):
    """Create a reusable date dimension from date-bearing fact tables."""
    date_values = []
    for df, col in dataframes:
        date_values.extend(pd.to_datetime(df[col], errors="coerce").dropna().tolist())
    dim = pd.DataFrame({"date": sorted(pd.Series(date_values).drop_duplicates())})
    dim["date_id"] = dim["date"].dt.strftime("%Y%m%d").astype(int)
    dim["year"] = dim["date"].dt.year
    dim["month"] = dim["date"].dt.month
    dim["month_name"] = dim["date"].dt.month_name()
    dim["quarter"] = dim["date"].dt.quarter
    dim["is_weekday"] = dim["date"].dt.weekday < 5
    return dim[["date_id", "date", "year", "month", "month_name", "quarter", "is_weekday"]]


def save_cleaned_files(tables):
    """Save cleaned tables to the processed data folder."""
    for filename, df in tables.items():
        df.to_csv(PROCESSED_DIR / filename, index=False)
        print(f"Saved {filename}: {df.shape[0]} rows")


def load_to_sqlite(tables):
    """Load cleaned analytical tables into the SQLite database."""
    db_path = DB_DIR / "bluestock_mf.db"

    table_map = {
        "01_fund_master_clean.csv": "dim_fund",
        "dim_date.csv": "dim_date",
        "02_nav_history_clean.csv": "fact_nav",
        "08_investor_transactions_clean.csv": "fact_transactions",
        "07_scheme_performance_clean.csv": "fact_performance",
        "03_aum_by_fund_house_clean.csv": "fact_aum",
        "04_monthly_sip_inflows_clean.csv": "fact_sip_industry",
        "05_category_inflows_clean.csv": "fact_category_inflows",
        "06_industry_folio_count_clean.csv": "fact_folio",
        "09_portfolio_holdings_clean.csv": "fact_portfolio",
        "10_benchmark_indices_clean.csv": "fact_benchmark_indices",
    }

    if HAS_SQLALCHEMY:
        engine = create_engine(f"sqlite:///{db_path}")
        for csv_name, table_name in table_map.items():
            df = tables[csv_name]
            df.to_sql(table_name, engine, if_exists="replace", index=False)

        with engine.connect() as conn:
            print("\nSQLite row count verification")
            for table_name in table_map.values():
                count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                print(f"{table_name}: {count} rows")
    else:
        conn = sqlite3.connect(db_path)
        for csv_name, table_name in table_map.items():
            df = tables[csv_name]
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        print("\nSQLite row count verification")
        for table_name in table_map.values():
            count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"{table_name}: {count} rows")
        conn.close()

    print(f"\nDatabase created at: {db_path}")


def main():
    """Execute the complete Day 2 cleaning and database loading workflow."""
    fund = clean_fund_master()
    nav = clean_nav_history()
    tx = clean_transactions()
    perf = clean_performance()
    others = clean_other_files()

    dim_date = create_dim_date(
        (nav, "date"),
        (tx, "transaction_date"),
        (others["03_aum_by_fund_house_clean.csv"], "date"),
        (others["10_benchmark_indices_clean.csv"], "date"),
    )

    tables = {
        "01_fund_master_clean.csv": fund,
        "02_nav_history_clean.csv": nav,
        "07_scheme_performance_clean.csv": perf,
        "08_investor_transactions_clean.csv": tx,
        "dim_date.csv": dim_date,
    }
    tables.update(others)

    save_cleaned_files(tables)
    load_to_sqlite(tables)

    print("\nData quality notes")
    print("NAV minimum value:", nav["nav"].min())
    print("Transaction types:", sorted(tx["transaction_type"].unique()))
    print("KYC statuses:", sorted(tx["kyc_status"].unique()))
    print("Expense ratio anomalies:", int(perf["expense_ratio_anomaly"].sum()))
    print("Negative Sharpe funds:", int(perf["negative_sharpe_flag"].sum()))


if __name__ == "__main__":
    main()
