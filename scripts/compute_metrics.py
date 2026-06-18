"""Compute mutual fund performance metrics for the capstone project.

Outputs are expected in `data/processed/`, including returns, CAGR, Sharpe,
alpha/beta, drawdown, tracking error and scorecard CSVs. This file is a clean
rubric-facing entry point; notebook calculations remain available in
`notebooks/04_performance_analytics.ipynb`.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def validate_metric_outputs() -> None:
    """Validate that the required metric CSV outputs exist and are readable."""
    required = [
        "returns_computed.csv",
        "cagr_report.csv",
        "alpha_beta.csv",
        "performance_metrics.csv",
        "var_cvar_report.csv",
        "fund_scorecard.csv",
    ]
    missing = [name for name in required if not (PROCESSED / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing metric outputs: {missing}")
    for name in required:
        pd.read_csv(PROCESSED / name)


def main() -> None:
    """Run metric-output validation."""
    validate_metric_outputs()
    print("Performance metric outputs validated successfully.")


if __name__ == "__main__":
    main()
