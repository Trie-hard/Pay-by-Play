"""Draft slots, WNBA raise split, WPL auction + Cricsheet, and 1,000-draw intervals."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.bootstrap import bootstrap_gap_intervals, bootstrap_wnba_gap_from_box
from src.config import load_league_config
from src.fetch.wnba_herhoop import parse_hhs_markdown_table
from src.ingest_pwhl import load_pwhl_game_logs
from src.model.gap import confident_bargain_mask
from src.model.metrics import spearman_fairness
from src.remaining import fetch_wpl_auction, h1_draft, h2_raises, parse_pwhl_draft, score_wpl, wpl_value_from_cricsheet

PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"


def refresh_intervals() -> None:
    cfg = load_league_config()
    pwhl = pd.read_parquet(PROCESSED / "player_season_pwhl.parquet")
    logs = load_pwhl_game_logs()
    pwhl = bootstrap_gap_intervals(pwhl, logs, n_boot=1000)
    pwhl["confident_bargain"] = confident_bargain_mask(pwhl, cfg["pwhl"]["regulars"]["min_games"])
    pwhl.to_parquet(PROCESSED / "player_season_pwhl.parquet", index=False)

    wnba = pd.read_parquet(PROCESSED / "player_season_wnba.parquet")
    box = pd.read_csv(RAW / "wnba_player_box_2026.csv")
    wnba = bootstrap_wnba_gap_from_box(wnba, box, n_boot=1000)
    wnba["confident_bargain"] = confident_bargain_mask(wnba, cfg["wnba"]["regulars"]["min_games"])
    wnba.to_parquet(PROCESSED / "player_season_wnba.parquet", index=False)
    print(
        f"intervals x1000  PWHL bargains={int(pwhl['confident_bargain'].sum())} "
        f"WNBA bargains={int(wnba['confident_bargain'].sum())}"
    )


def main() -> None:
    snapshot = Path(r"C:\Users\niksh\.cursor\projects\d-Pay-By-Play\agent-tools\f8f58864-2239-4263-b98a-818f31e2e19b.txt")
    dest = ROOT / "data" / "reference" / "hhs_wnba_salary_2025_snapshot.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if snapshot.exists():
        shutil.copy(snapshot, dest)
    pay_2025 = parse_hhs_markdown_table(dest.read_text(encoding="utf-8"))
    pay_2025["season"] = 2025
    pay_2025.to_csv(RAW / "wnba_salaries_2025.csv", index=False)

    draft = parse_pwhl_draft()
    pwhl = pd.read_parquet(PROCESSED / "player_season_pwhl.parquet")
    h1 = h1_draft(pwhl, draft)

    pay_2026 = pd.read_csv(RAW / "wnba_salaries.csv")
    two = pd.read_parquet(PROCESSED / "wnba_two_lens.parquet")
    h2 = h2_raises(pay_2025, pay_2026, two)

    auction = fetch_wpl_auction()
    values = wpl_value_from_cricsheet()
    wpl_b = score_wpl(auction, values, "2025/26")
    wpl_a = score_wpl(auction, values, "2024/25")
    wpl_b.to_parquet(PROCESSED / "player_season_wpl.parquet", index=False)
    wpl_summary = {
        "auction_rows": int(len(auction)),
        "matched_2025_26": int(len(wpl_b)),
        "matched_2024_25": int(len(wpl_a)),
        "spearman_fairness_2025_26": spearman_fairness(wpl_b) if len(wpl_b) > 5 else None,
        "source_pay": "Cricbuzz WPL 2026 auction team pages (sold and retained prices, INR)",
        "source_value": "Cricsheet wpl_json.zip phase runs above baseline plus phase-valued wickets",
    }

    report = {"h1_pwhl_draft": h1, "h2_wnba_raise": h2, "wpl": wpl_summary}
    (PROCESSED / "hypotheses.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2))
    refresh_intervals()


if __name__ == "__main__":
    main()
