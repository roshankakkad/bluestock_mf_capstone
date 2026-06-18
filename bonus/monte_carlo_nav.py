"""B3 - Monte Carlo simulation for 5-year NAV growth uncertainty bands."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def simulate_nav(nav_series: pd.Series, years: int = 5, paths: int = 1000, trading_days: int = 252) -> pd.DataFrame:
    returns = nav_series.pct_change().dropna()
    mu, sigma = returns.mean(), returns.std()
    start = float(nav_series.dropna().iloc[-1])
    shocks = np.random.normal(mu, sigma, size=(years * trading_days, paths))
    simulated = start * np.cumprod(1 + shocks, axis=0)
    return pd.DataFrame({
        "day": range(1, years * trading_days + 1),
        "p05": np.percentile(simulated, 5, axis=1),
        "p50": np.percentile(simulated, 50, axis=1),
        "p95": np.percentile(simulated, 95, axis=1),
    })
