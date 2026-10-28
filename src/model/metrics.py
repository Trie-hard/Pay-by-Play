from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def spearman_fairness(df: pd.DataFrame) -> float:
    sub = df[["pay_raw", "value_shrunk"]].dropna()
    if len(sub) < 3:
        return np.nan
    return float(stats.spearmanr(sub["pay_raw"], sub["value_shrunk"]).statistic)


def misallocation_index(df: pd.DataFrame) -> float:
    """
    Fraction of total payroll that would need to move so pay share matches value share.
    Uses non-negative value weights.
    """
    sub = df.dropna(subset=["pay_raw", "value_shrunk"]).copy()
    if sub.empty or sub["pay_raw"].sum() == 0:
        return np.nan
    v = sub["value_shrunk"].clip(lower=0)
    if v.sum() == 0:
        return np.nan
    target_share = v / v.sum()
    actual_share = sub["pay_raw"] / sub["pay_raw"].sum()
    return float(0.5 * np.abs(target_share - actual_share).sum())


def placebo_pay_shuffle(df: pd.DataFrame, rng: np.random.Generator | None = None) -> float:
    rng = rng or np.random.default_rng(0)
    shuffled = df.copy()
    for _, idx in shuffled.groupby(["league", "position"]).groups.items():
        pays = shuffled.loc[idx, "pay_raw"].to_numpy().copy()
        rng.shuffle(pays)
        shuffled.loc[idx, "pay_raw"] = pays
    return spearman_fairness(shuffled)
