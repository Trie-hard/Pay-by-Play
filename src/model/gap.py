from __future__ import annotations

import pandas as pd

from src.model.normalize import percentile_within_cohort


def add_pay_and_value_percentiles(
    df: pd.DataFrame,
    league: str,
) -> pd.DataFrame:
    out = df.copy()
    cohort = ["league", "position"]
    out["pay_pct"] = percentile_within_cohort(out, "pay_raw", cohort, "pay_pct")
    out["value_pct"] = percentile_within_cohort(out, "value_shrunk", cohort, "value_pct")
    out["gap"] = out["value_pct"] - out["pay_pct"]
    return out


def confident_bargain_mask(
    df: pd.DataFrame,
    min_games: int,
) -> pd.Series:
    flags_ok = df["data_flags"].fillna("").eq("")
    ci_ok = (df["ci_low"] > 0) & (df["gap"] > 0)
    games_ok = df["games"] >= min_games
    return flags_ok & ci_ok & games_ok
