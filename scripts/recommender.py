"""Recommend mutual funds based on risk appetite and Sharpe ratio.

This utility supports Day 6 advanced analytics by reading the cleaned performance
data when available and falling back to the raw scheme performance file.
"""

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "clean_scheme_performance.csv"
FALLBACK_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "07_scheme_performance.csv"


def load_performance_data():
    """Load cleaned performance data, or fall back to the raw performance file."""
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return pd.read_csv(FALLBACK_PATH)


def recommend_funds(risk_appetite="Moderate", top_n=3):
    """Return top funds by Sharpe ratio for a given risk appetite."""
    df = load_performance_data()
    risk_appetite = risk_appetite.strip().title()

    risk_col = "risk_grade" if "risk_grade" in df.columns else "risk_category"
    matches = df[df[risk_col].astype(str).str.title() == risk_appetite].copy()

    if matches.empty:
        print(f"No funds found for risk appetite: {risk_appetite}")
        print("Try Low, Moderate, High or Very High depending on available data.")
        return pd.DataFrame()

    cols = ["scheme_name", "fund_house", risk_col, "return_3yr_pct", "sharpe_ratio", "expense_ratio_pct"]
    result = matches.sort_values("sharpe_ratio", ascending=False)[cols].head(top_n)
    return result


if __name__ == "__main__":
    appetite = input("Enter risk appetite (Low / Moderate / High / Very High): ")
    print("\nTop recommended funds:\n")
    print(recommend_funds(appetite).to_string(index=False))
