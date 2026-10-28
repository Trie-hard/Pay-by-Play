from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sportsdataverse.wnba import load_wnba_player_boxscore

from src.fetch.pwhl_hockeytech import fetch_pwhl_game_logs, fetch_pwhl_season_stats
from src.fetch.pwhlpa_salaries import fetch_pwhlpa_salaries
from src.fetch.wnba_herhoop import fetch_wnba_salaries


def ensure_hhs_snapshot() -> None:
    """Seed Her Hoop Stats pipe table if live fetch is blocked."""
    dest = ROOT / "data" / "raw" / "hhs_wnba_salary_2026_snapshot.md"
    if dest.exists():
        return
    # Bundled copy path (optional); user can replace with fresh save from browser.
    candidate = ROOT / "data" / "reference" / "hhs_wnba_salary_2026_snapshot.md"
    if candidate.exists():
        shutil.copy(candidate, dest)


def main() -> None:
    print("Fetching PWHLPA salary PDF…")
    fetch_pwhlpa_salaries()
    print("Fetching PWHL HockeyTech season + game logs…")
    fetch_pwhl_season_stats()
    fetch_pwhl_game_logs()
    ensure_hhs_snapshot()
    print("Fetching WNBA salaries (Her Hoop Stats)…")
    fetch_wnba_salaries()
    print("Fetching WNBA ESPN box scores (2025, 2026)…")
    raw = ROOT / "data" / "raw"
    for season in (2025, 2026):
        box = load_wnba_player_boxscore(seasons=[season], return_as_pandas=True)
        box.to_csv(raw / f"wnba_player_box_{season}.csv", index=False)
        print(f"  WNBA {season}: {len(box)} game rows")
    print("Done.")


if __name__ == "__main__":
    main()
