from __future__ import annotations

from pathlib import Path

import pandas as pd
from sportsdataverse.pwhl import load_pwhl_player_boxscores
from sportsdataverse.pwhl.pwhl_api import pwhl_teams

from src.config import ROOT


def _team_lookup() -> pd.DataFrame:
    teams = pwhl_teams(return_as_pandas=True)
    return teams[["team_id", "team_code", "team_name"]]


def season_stats_from_boxscores(season_year: int) -> pd.DataFrame:
    """Full-league season totals from ESPN/HockeyTech game logs (pwhl_stats is team-scoped)."""
    box = load_pwhl_player_boxscores(seasons=[season_year], return_as_pandas=True)
    if box.empty:
        return pd.DataFrame()
    teams = _team_lookup()
    box["team_id"] = pd.to_numeric(box["team_id"], errors="coerce").astype("Int64")
    teams["team_id"] = pd.to_numeric(teams["team_id"], errors="coerce").astype("Int64")
    box = box.merge(teams, on="team_id", how="left")
    box["goals"] = pd.to_numeric(box["goals"], errors="coerce").fillna(0)
    box["assists"] = pd.to_numeric(box["assists"], errors="coerce").fillna(0)
    box["shots"] = pd.to_numeric(box["shots"], errors="coerce").fillna(0)
    box["penalty_minutes"] = pd.to_numeric(box.get("penalty_minutes", 0), errors="coerce").fillna(0)

    def _mode_team(sub: pd.DataFrame) -> pd.Series:
        tc = sub["team_code"].mode()
        return tc.iloc[0] if len(tc) else sub["team_code"].iloc[0]

    agg = (
        box.groupby(["player_id", "first_name", "last_name", "position"], as_index=False)
        .agg(
            games=("game_id", "nunique"),
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            shots=("shots", "sum"),
            penalty_minutes=("penalty_minutes", "sum"),
        )
    )
    team_codes = box.groupby("player_id").apply(_mode_team).reset_index(name="team_code")
    agg = agg.merge(team_codes, on="player_id", how="left")
    agg["penalties_taken"] = agg["penalty_minutes"] / 2.0
    agg["penalties_drawn"] = 0
    agg["name"] = agg["first_name"] + " " + agg["last_name"]
    agg["season_year"] = season_year
    return agg


def fetch_pwhl_season_stats(dest_dir: Path | None = None) -> tuple[Path, Path]:
    dest_dir = dest_dir or ROOT / "data" / "raw"
    dest_dir.mkdir(parents=True, exist_ok=True)
    a = season_stats_from_boxscores(2025)
    b = season_stats_from_boxscores(2026)
    path_a = dest_dir / "pwhl_stats_2025-26.csv"
    path_b = dest_dir / "pwhl_stats_2026-27.csv"
    a.to_csv(path_a, index=False)
    b.to_csv(path_b, index=False)
    return path_a, path_b


def fetch_pwhl_game_logs(seasons: list[int] | None = None, dest_dir: Path | None = None) -> Path:
    seasons = seasons or [2025, 2026]
    dest_dir = dest_dir or ROOT / "data" / "raw"
    dest_dir.mkdir(parents=True, exist_ok=True)
    box = load_pwhl_player_boxscores(seasons=seasons, return_as_pandas=True)
    teams = _team_lookup()
    box["team_id"] = pd.to_numeric(box["team_id"], errors="coerce").astype("Int64")
    teams["team_id"] = pd.to_numeric(teams["team_id"], errors="coerce").astype("Int64")
    box = box.merge(teams, on="team_id", how="left")
    path = dest_dir / "pwhl_player_game_logs.csv"
    box.to_csv(path, index=False)
    return path
