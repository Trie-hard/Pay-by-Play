from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ROOT
from src.match import normalize_name


def load_wnba_salaries(path: Path | None = None) -> pd.DataFrame:
    path = path or ROOT / "data" / "raw" / "wnba_salaries.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run: python scripts/fetch_data.py")
    df = pd.read_csv(path)
    df["league"] = "WNBA"
    df["name_key"] = df["name"].map(normalize_name)
    return df


def aggregate_wnba_box(box: pd.DataFrame) -> pd.DataFrame:
    if box.empty:
        return box
    g = box.groupby(["athlete_id", "athlete_display_name"], as_index=False).agg(
        games=("game_id", "nunique"),
        minutes=("minutes", "sum"),
        points=("points", "sum"),
        rebounds=("rebounds", "sum"),
        assists=("assists", "sum"),
        steals=("steals", "sum"),
        blocks=("blocks", "sum"),
        position=("athlete_position_abbreviation", "first"),
        team=("team_abbreviation", "last"),
    )
    g["name"] = g["athlete_display_name"]
    g["name_key"] = g["name"].map(normalize_name)
    return g


def build_wnba_player_season(
    salaries: pd.DataFrame,
    stats: pd.DataFrame,
    min_games: int = 15,
) -> pd.DataFrame:
    st = stats.copy()
    merged = salaries.merge(st, on="name_key", how="left", suffixes=("", "_stat"))
    merged["league"] = "WNBA"
    merged["season"] = 2026
    merged["athlete_id"] = merged.get("athlete_id", pd.NA)
    merged["games"] = pd.to_numeric(merged.get("games", 0), errors="coerce").fillna(0).astype(int)
    merged["exposure"] = merged["minutes"].fillna(0)
    merged["regular_flag"] = merged["games"] >= min_games
    merged["position"] = merged.get("position", "G").fillna("G")
    merged["rookie_flag"] = merged.get("signing_status", "").astype(str).str.contains("Rookie", case=False)
    merged["data_flags"] = ""
    merged.loc[merged["athlete_id"].isna(), "data_flags"] = "unmatched_athlete_id"
    merged.loc[merged["pay_raw"].isna(), "data_flags"] = merged.loc[merged["pay_raw"].isna(), "data_flags"].apply(
        lambda f: "missing_salary" if not f else f + ";missing_salary"
    )
    return merged
