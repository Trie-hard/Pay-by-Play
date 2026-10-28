from __future__ import annotations

import numpy as np
import pandas as pd


def percentile_within_cohort(
    df: pd.DataFrame,
    value_col: str,
    group_cols: list[str],
    out_col: str,
) -> pd.Series:
    """Rank-based percentile (0–100) within group_cols."""

    def _pct(s: pd.Series) -> pd.Series:
        if len(s) <= 1:
            return pd.Series(50.0, index=s.index)
        ranks = s.rank(method="average", na_option="keep")
        return (ranks - 1) / (ranks.notna().sum() - 1) * 100

    return df.groupby(group_cols, dropna=False)[value_col].transform(_pct)


def zscore_within_cohort(
    df: pd.DataFrame,
    value_col: str,
    group_cols: list[str],
) -> pd.Series:
    def _z(s: pd.Series) -> pd.Series:
        m, sd = s.mean(), s.std(ddof=0)
        if sd == 0 or np.isnan(sd):
            return pd.Series(0.0, index=s.index)
        return (s - m) / sd

    return df.groupby(group_cols, dropna=False)[value_col].transform(_z)
