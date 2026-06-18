"""B4 - Markowitz Efficient Frontier for selected funds."""
import numpy as np
import pandas as pd


def random_portfolios(returns: pd.DataFrame, n: int = 5000) -> pd.DataFrame:
    mean_returns = returns.mean() * 252
    cov = returns.cov() * 252
    rows = []
    for _ in range(n):
        w = np.random.random(len(returns.columns))
        w = w / w.sum()
        ret = float(np.dot(w, mean_returns))
        vol = float(np.sqrt(np.dot(w.T, np.dot(cov, w))))
        sharpe = ret / vol if vol else np.nan
        rows.append({"return": ret, "risk": vol, "sharpe": sharpe, **dict(zip(returns.columns, w))})
    return pd.DataFrame(rows)
