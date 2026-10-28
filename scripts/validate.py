from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
from scipy import stats

from src.config import load_league_config
from src.ingest_pwhl import load_pwhl_salaries
from src.model.metrics import placebo_pay_shuffle, spearman_fairness
from src.qa.checksums import reconcile_team_payroll


def check_checksum() -> bool:
    cfg = load_league_config()["pwhl"]["checksum_teams"]["Boston"]
    salaries = load_pwhl_salaries()
    r = reconcile_team_payroll(
        salaries,
        "Boston",
        cfg["expected_total"],
        cfg["expected_contracts"],
    )
    print(r.message)
    return r.ok


def check_processed() -> bool:
    pwhl = pd.read_parquet(ROOT / "data/processed/player_season_pwhl.parquet")
    wnba = pd.read_parquet(ROOT / "data/processed/player_season_wnba.parquet")
    ok = len(pwhl) >= 150 and pwhl["pay_raw"].notna().mean() > 0.95
    print(f"processed PWHL rows={len(pwhl)} WNBA rows={len(wnba)}")
    return ok and len(wnba) > 50


def check_placebo() -> bool:
    df = pd.read_parquet(ROOT / "data/processed/player_season_pwhl.parquet")
    real = spearman_fairness(df)
    fakes = [abs(placebo_pay_shuffle(df, np.random.default_rng(i))) for i in range(20)]
    mean_fake = float(np.mean(fakes))
    print(f"placebo: real={real:.3f} mean|shuffled|={mean_fake:.3f}")
    return mean_fake < max(0.15, abs(real) * 0.9)


def main() -> int:
    ok = all([check_checksum(), check_processed(), check_placebo()])
    print("validate:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
