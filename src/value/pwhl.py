from __future__ import annotations

import pandas as pd

from src.model.normalize import zscore_within_cohort


def skater_value_per_game(stats: pd.DataFrame, definition: str = "A") -> pd.Series:
    """
    Definition A: per-game box composite (G, A, SOG, +/- penalties).
    B/C: reserved for on-ice share and weight sensitivity (falls back to A).
    """
    g = stats["games"].clip(lower=1)
    goals = stats["goals"] / g
    assists = stats["assists"] / g
    shots = stats["shots"] / g
    pen_net = (stats["penalties_drawn"] - stats["penalties_taken"]) / g

    if definition == "C":
        w = {"goals": 1.2, "assists": 0.9, "shots": 0.15, "pen_net": 0.25}
    else:
        w = {"goals": 1.0, "assists": 1.0, "shots": 0.2, "pen_net": 0.3}

    raw = (
        w["goals"] * goals
        + w["assists"] * assists
        + w["shots"] * shots
        + w["pen_net"] * pen_net
    )
    if definition == "B" and "on_ice_goal_share" in stats.columns:
        raw = raw + 0.5 * stats["on_ice_goal_share"].fillna(0)

    out = stats.copy()
    out["value_raw"] = raw
    out["value_raw"] = zscore_within_cohort(out, "value_raw", ["position"])
    return out["value_raw"]


def goalie_value_per_game(stats: pd.DataFrame) -> pd.Series:
    g = stats["games"].clip(lower=1)
    save_pct = stats.get("save_pct", pd.Series(0.9, index=stats.index))
    raw = save_pct - 0.9 + (stats.get("shutouts", 0) / g) * 0.1
    out = stats.copy()
    out["value_raw"] = raw
    return out["value_raw"]


def attach_pwhl_values(stats: pd.DataFrame, definition: str = "A") -> pd.DataFrame:
    out = stats.copy()
    is_goalie = out["position"].str.upper().eq("G")
    out.loc[~is_goalie, "value_raw"] = skater_value_per_game(out.loc[~is_goalie], definition)
    out.loc[is_goalie, "value_raw"] = goalie_value_per_game(out.loc[is_goalie])
    return out
