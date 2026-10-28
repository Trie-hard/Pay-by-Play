from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.analytics import draft_vs_value_h1, mechanism_scorecard, write_analytics_bundle
from src.bootstrap import bootstrap_gap_intervals, bootstrap_wnba_gap_from_box
from src.config import ROOT, load_league_config
from src.ingest_pwhl import (
    aggregate_game_logs,
    build_pwhl_player_season,
    load_pwhl_game_logs,
    load_pwhl_salaries,
    load_pwhl_season_stats,
)
from src.ingest_wnba import aggregate_wnba_box, build_wnba_player_season, load_wnba_salaries
from src.model.gap import add_pay_and_value_percentiles, confident_bargain_mask
from src.model.metrics import misallocation_index, spearman_fairness
from src.model.shrink import empirical_bayes_shrink
from src.model.twolens import merge_two_lenses
from src.qa.checksums import reconcile_team_payroll
from src.robustness import run_robustness
from src.value.pwhl import attach_pwhl_values
from src.value.wnba import attach_wnba_values

PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
MANIFEST = ROOT / "data" / "manifest.json"


def _finalize(df: pd.DataFrame, league: str, min_games: int, lens: str, definition: str) -> pd.DataFrame:
    df = attach_pwhl_values(df, definition) if league == "PWHL" else attach_wnba_values(df, definition)
    df = empirical_bayes_shrink(df, "value_raw", ["league", "position"], exposure_col="games")
    df = add_pay_and_value_percentiles(df, league)
    df["value_definition"] = definition
    df["lens"] = lens
    return df


def run_pwhl_lens(
    stats_path: Path,
    lens: str,
    value_definition: str = "A",
    bootstrap_reps: int = 120,
) -> pd.DataFrame:
    cfg = load_league_config()["pwhl"]
    salaries = load_pwhl_salaries()
    checksum = reconcile_team_payroll(
        salaries,
        team="Boston",
        expected_total=cfg["checksum_teams"]["Boston"]["expected_total"],
        expected_contracts=cfg["checksum_teams"]["Boston"]["expected_contracts"],
    )
    if not checksum.ok:
        raise RuntimeError(f"PWHL checksum failed: {checksum.message}")

    season_stats = load_pwhl_season_stats(stats_path)
    if season_stats.empty and lens == "B":
        season_stats = aggregate_game_logs(load_pwhl_game_logs())
    df = build_pwhl_player_season(salaries, season_stats, min_games=cfg["regulars"]["min_games"])
    df = _finalize(df, "PWHL", cfg["regulars"]["min_games"], lens, value_definition)
    logs = load_pwhl_game_logs()
    if not logs.empty:
        df = bootstrap_gap_intervals(df, logs, n_boot=bootstrap_reps)
        df["confident_bargain"] = confident_bargain_mask(df, cfg["regulars"]["min_games"])
    return df


def run_wnba_lens(
    box_path: Path,
    lens: str,
    value_definition: str = "A",
    bootstrap_reps: int = 80,
) -> pd.DataFrame:
    cfg = load_league_config()["wnba"]
    salaries = load_wnba_salaries()
    box = pd.read_csv(box_path)
    stats = aggregate_wnba_box(box)
    df = build_wnba_player_season(salaries, stats, min_games=cfg["regulars"]["min_games"])
    df = df.dropna(subset=["pay_raw"])
    df = _finalize(df, "WNBA", cfg["regulars"]["min_games"], lens, value_definition)
    if not box.empty:
        df = bootstrap_wnba_gap_from_box(df, box, n_boot=bootstrap_reps)
        df["confident_bargain"] = confident_bargain_mask(df, cfg["regulars"]["min_games"])
    return df


def write_league_outputs(df: pd.DataFrame, league_key: str) -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    path = PROCESSED / f"player_season_{league_key}.parquet"
    df.to_parquet(path, index=False)
    summary = {
        "league": league_key.upper(),
        "within_league_fairness_spearman": spearman_fairness(df),
        "misallocation_index": misallocation_index(df),
        "confident_bargains": int(df["confident_bargain"].sum()),
        "n_players": len(df),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (PROCESSED / f"scoreboard_{league_key}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    pwhl_a = run_pwhl_lens(RAW / "pwhl_stats_2025-26.csv", lens="A")
    pwhl_b = run_pwhl_lens(RAW / "pwhl_stats_2026-27.csv", lens="B")
    pwhl_two = merge_two_lenses(pwhl_a, pwhl_b, on=["player_id"])
    write_league_outputs(pwhl_b, "pwhl")
    pwhl_two.to_parquet(PROCESSED / "pwhl_two_lens.parquet", index=False)

    wnba_a = run_wnba_lens(RAW / "wnba_player_box_2025.csv", lens="A")
    wnba_b = run_wnba_lens(RAW / "wnba_player_box_2026.csv", lens="B")
    wnba_two = merge_two_lenses(wnba_a, wnba_b, on=["athlete_id"])
    write_league_outputs(wnba_b, "wnba")
    wnba_two.to_parquet(PROCESSED / "wnba_two_lens.parquet", index=False)

    scorecard = mechanism_scorecard({"PWHL": pwhl_b, "WNBA": wnba_b})
    extras = {
        "pwhl_h1_draft_vs_value": draft_vs_value_h1(pwhl_b),
        "pwhl_checksum": "Boston 25 @ $1,436,173.50 (PWHLPA PDF)",
        "wnba_salary_source": "Her Hoop Stats cap hit 2026 (cite in definitions.md)",
    }
    write_analytics_bundle(PROCESSED, scorecard, extras)
    run_robustness()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["datasets"] = {
        "player_season_pwhl": {"path": "data/processed/player_season_pwhl.parquet"},
        "player_season_wnba": {"path": "data/processed/player_season_wnba.parquet"},
        "pwhl_two_lens": {"path": "data/processed/pwhl_two_lens.parquet"},
        "wnba_two_lens": {"path": "data/processed/wnba_two_lens.parquet"},
    }
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(
        f"PWHL n={len(pwhl_b)} fairness={spearman_fairness(pwhl_b):.3f} | "
        f"WNBA n={len(wnba_b)} fairness={spearman_fairness(wnba_b):.3f}"
    )


if __name__ == "__main__":
    main()
