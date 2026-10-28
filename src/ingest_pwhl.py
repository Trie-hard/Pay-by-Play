from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ROOT
from src.match import attach_player_ids, normalize_name, pwhl_team_code


def load_pwhl_salaries(path: Path | None = None) -> pd.DataFrame:
    path = path or ROOT / "data" / "raw" / "pwhl_salaries.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run: python scripts/fetch_data.py")
    df = pd.read_csv(path)
    df["league"] = "PWHL"
    df["pay_currency"] = df.get("pay_currency", "USD")
    df["pay_type"] = "salary"
    return df


def load_pwhl_season_stats(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_pwhl_game_logs(path: Path | None = None) -> pd.DataFrame:
    path = path or ROOT / "data" / "raw" / "pwhl_player_game_logs.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def aggregate_game_logs(box: pd.DataFrame) -> pd.DataFrame:
    if box.empty:
        return box
    g = box.groupby("player_id", as_index=False).agg(
        games=("game_id", "nunique"),
        goals=("goals", "sum"),
        assists=("assists", "sum"),
        shots=("shots", "sum"),
        penalty_minutes=("penalty_minutes", "sum"),
        position=("position", "first"),
        first_name=("first_name", "first"),
        last_name=("last_name", "last"),
        team_code=("team_id", "first"),
    )
    g["penalties_taken"] = g["penalty_minutes"].fillna(0) / 2.0
    g["penalties_drawn"] = 0
    return g


def build_pwhl_player_season(
    salaries: pd.DataFrame,
    season_stats: pd.DataFrame,
    min_games: int = 10,
) -> pd.DataFrame:
    linked = attach_player_ids(salaries, season_stats)
    stats = season_stats.copy()
    if "player_id" not in stats.columns:
        raise ValueError("season_stats must include player_id from HockeyTech")
    stats = stats.sort_values("games", ascending=False).drop_duplicates(subset=["player_id"], keep="first")
    merged = linked.drop_duplicates(subset=["name", "team"], keep="first").merge(
        stats,
        on="player_id",
        how="left",
        suffixes=("", "_stat"),
    )
    merged["league"] = "PWHL"
    merged["season"] = salaries["season"].iloc[0] if "season" in salaries.columns else "2025-26"
    gp = merged.get("games", merged.get("games_played", 0))
    merged["games"] = pd.to_numeric(gp, errors="coerce").fillna(0).astype(int)
    merged["exposure"] = merged["games"]
    merged["regular_flag"] = merged["games"] >= min_games
    pos = merged.get("position", merged.get("position_group", "F"))
    merged["position"] = pos.fillna("F").astype(str).str.upper()
    if "rookie" in merged.columns:
        merged["rookie_flag"] = merged["rookie"].fillna(False)
    else:
        merged["rookie_flag"] = False
    merged["draft_pick"] = pd.NA
    merged["age"] = merged.get("age", pd.NA)
    if "data_flags" not in merged.columns:
        merged["data_flags"] = ""
    merged["data_flags"] = merged["data_flags"].fillna("").astype(str)
    merged.loc[merged["games"] == 0, "data_flags"] = merged.loc[merged["games"] == 0, "data_flags"].apply(
        lambda f: "missing_stats" if not f else f + ";missing_stats"
    )
    merged["name_key"] = merged["name"].map(normalize_name)
    merged["team_code"] = merged["team"].map(pwhl_team_code)
    return merged
