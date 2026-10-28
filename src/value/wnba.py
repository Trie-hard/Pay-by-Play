from __future__ import annotations

import pandas as pd

from src.model.normalize import zscore_within_cohort


def attach_wnba_values(stats: pd.DataFrame, definition: str = "A") -> pd.DataFrame:
    """Per-minute box composite; definition B adds optional impact column."""
    out = stats.copy()
    minutes = out["minutes"].clip(lower=1)
    pts = out["points"] / minutes
    reb = out["rebounds"] / minutes
    ast = out["assists"] / minutes
    stl = out["steals"] / minutes
    blk = out["blocks"] / minutes
    raw = pts + 0.7 * reb + 0.7 * ast + 1.0 * stl + 1.0 * blk
    if definition == "B" and "impact_rating" in out.columns:
        raw = raw + 0.3 * out["impact_rating"].fillna(0)
    if definition == "C":
        raw = raw * (minutes / minutes.median())
    out["value_raw"] = raw
    out["value_raw"] = zscore_within_cohort(out, "value_raw", ["position"])
    return out
