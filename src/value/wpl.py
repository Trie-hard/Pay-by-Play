from __future__ import annotations

import pandas as pd


def attach_wpl_values(stats: pd.DataFrame, definition: str = "A") -> pd.DataFrame:
    """Phase-adjusted runs added (placeholder until Cricsheet ingest lands)."""
    out = stats.copy()
    balls = out["balls"].clip(lower=1)
    raw = out["runs_added"] / balls * 100
    if definition == "B":
        raw = raw + 0.2 * out.get("wicket_value", 0)
    out["value_raw"] = raw
    return out
