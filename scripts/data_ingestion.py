"""Profile raw Bluestock mutual fund CSV files.

This script reads every CSV file from data/raw and generates a compact data-quality
summary for each file. It is intended for Day 1 ingestion validation and does not
change any source data.
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
REPORT_PATH = Path("reports/data_ingestion_summary.csv")


def profile_csv(file_path: Path) -> dict:
    """Return row count, column count, duplicate count and missing-value count."""
    df = pd.read_csv(file_path)
    return {
        "file_name": file_path.name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
    }


def profile_raw_data(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Build a profiling table for all CSV files available in the raw data folder."""
    csv_files = sorted(raw_dir.glob("*.csv"))
    summaries = [profile_csv(file_path) for file_path in csv_files]
    return pd.DataFrame(summaries)


def main() -> None:
    """Run the ingestion profiling step and save the summary report."""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = profile_raw_data()
    summary.to_csv(REPORT_PATH, index=False)
    print(f"Data ingestion summary saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()
