from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from scipy import stats

from src.config import ROOT
from src.model.gap import add_pay_and_value_percentiles
from src.model.metrics import misallocation_index, spearman_fairness
from src.model.shrink import empirical_bayes_shrink
from src.value.pwhl import attach_pwhl_values
from src.value.wnba import attach_wnba_values

PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"


LABELS = {
    ("PWHL", "A"): "box_per_game",
    ("PWHL", "B"): "box_plus_mean_plus_minus",
    ("PWHL", "C"): "position_weight_sensitivity",
    ("WNBA", "A"): "per_minute_box",
    ("WNBA", "B"): "box_plus_mean_plus_minus",
    ("WNBA", "C"): "minutes_weighted",
}


def _score_row(league: str, definition: str, df: pd.DataFrame) -> dict:
    return {
        "league": league,
        "value_definition": definition,
        "definition_label": LABELS[(league, definition)],
        "n": int(df["value_shrunk"].notna().sum()),
        "spearman_fairness": spearman_fairness(df),
        "misallocation_index": misallocation_index(df),
    }


def _rescore(df: pd.DataFrame, league: str, definition: str) -> pd.DataFrame:
    out = df.copy()
    if league == "PWHL":
        out = attach_pwhl_values(out, definition)
    else:
        out = attach_wnba_values(out, definition)
    out = empirical_bayes_shrink(out, "value_raw", ["league", "position"], exposure_col="games")
    out = add_pay_and_value_percentiles(out, league)
    return out


def pwhl_plus_minus(logs: pd.DataFrame) -> pd.Series:
    logs = logs.copy()
    logs["plus_minus"] = pd.to_numeric(logs["plus_minus"], errors="coerce")
    return logs.groupby("player_id")["plus_minus"].mean()


def value_definition_table(pwhl: pd.DataFrame, wnba: pd.DataFrame, logs: pd.DataFrame) -> pd.DataFrame:
    pwhl = pwhl.copy()
    pm = pwhl_plus_minus(logs)
    pwhl["on_ice_goal_share"] = pwhl["player_id"].map(pm)
    # Definition B uses on-ice plus/minus as the available on-ice signal (not full goal share).
    if "plus_minus" in pd.read_csv(RAW / "wnba_player_box_2026.csv", nrows=0).columns:
        box = pd.read_csv(RAW / "wnba_player_box_2026.csv", usecols=["athlete_id", "plus_minus"])
        impact = box.groupby("athlete_id")["plus_minus"].mean()
        wnba = wnba.copy()
        wnba["impact_rating"] = wnba["athlete_id"].map(impact)

    rows = []
    for definition in ("A", "B", "C"):
        rows.append(_score_row("PWHL", definition, _rescore(pwhl, "PWHL", definition)))
        rows.append(_score_row("WNBA", definition, _rescore(wnba, "WNBA", definition)))
    return pd.DataFrame(rows)


def year_over_year(two_lens: pd.DataFrame, id_col: str, league: str) -> dict:
    sub = two_lens.dropna(subset=["value_pct_lens_a", "value_pct_lens_b"]).copy()
    if id_col in sub.columns:
        sub = sub.drop_duplicates(subset=[id_col])
    if len(sub) < 10:
        return {"league": league, "n": len(sub), "spearman": None}
    r, p = stats.spearmanr(sub["value_pct_lens_a"], sub["value_pct_lens_b"])
    return {"league": league, "n": int(len(sub)), "spearman_value_pct": float(r), "p_value": float(p), "id": id_col}


def split_half_pwhl(logs: pd.DataFrame) -> dict:
    logs = logs.copy()
    logs["game_id"] = pd.to_numeric(logs["game_id"], errors="coerce")
    logs["goals"] = pd.to_numeric(logs["goals"], errors="coerce").fillna(0)
    odd = logs[logs["game_id"] % 2 == 1].groupby("player_id")["goals"].mean()
    even = logs[logs["game_id"] % 2 == 0].groupby("player_id")["goals"].mean()
    joined = pd.concat([odd, even], axis=1, keys=["odd", "even"]).dropna()
    joined = joined[(joined["odd"] + joined["even"]) > 0]
    if len(joined) < 20:
        return {"n": int(len(joined)), "spearman": None}
    r, p = stats.spearmanr(joined["odd"], joined["even"])
    return {"metric": "goals_per_game_odd_vs_even_game_id", "n": int(len(joined)), "spearman": float(r), "p_value": float(p)}


def h2_pay_on_prior_value(two_lens: pd.DataFrame) -> dict:
    """How much 2026 WNBA cap hit is linear in 2025 value percentile (Lens A)."""
    sub = two_lens.dropna(subset=["pay_raw", "value_pct_lens_a"]).copy()
    if "athlete_id" in sub.columns:
        sub = sub.drop_duplicates(subset=["athlete_id"])
    if len(sub) < 15:
        return {"n": int(len(sub))}
    slope, intercept, r, p, se = stats.linregress(sub["value_pct_lens_a"], sub["pay_raw"])
    sub["pay_hat"] = intercept + slope * sub["value_pct_lens_a"]
    sub["residual_pay"] = sub["pay_raw"] - sub["pay_hat"]
    ss_tot = float(((sub["pay_raw"] - sub["pay_raw"].mean()) ** 2).sum())
    ss_res = float((sub["residual_pay"] ** 2).sum())
    return {
        "n": int(len(sub)),
        "r_squared": float(r**2),
        "slope_usd_per_value_pct": float(slope),
        "intercept_usd": float(intercept),
        "p_value": float(p),
        "residual_sd_usd": float(sub["residual_pay"].std()),
        "share_unexplained": float(ss_res / ss_tot) if ss_tot else None,
    }


def run_robustness() -> dict:
    pwhl = pd.read_parquet(PROCESSED / "player_season_pwhl.parquet")
    wnba = pd.read_parquet(PROCESSED / "player_season_wnba.parquet")
    logs = pd.read_csv(RAW / "pwhl_player_game_logs.csv")
    pwhl_two = pd.read_parquet(PROCESSED / "pwhl_two_lens.parquet")
    wnba_two = pd.read_parquet(PROCESSED / "wnba_two_lens.parquet")

    defs = value_definition_table(pwhl, wnba, logs)
    defs.to_csv(PROCESSED / "value_definition_robustness.csv", index=False)

    report = {
        "value_definitions": defs.to_dict(orient="records"),
        "yoy_value": [
            year_over_year(pwhl_two, "player_id", "PWHL"),
            year_over_year(wnba_two, "athlete_id", "WNBA"),
        ],
        "pwhl_split_half": split_half_pwhl(logs),
        "wnba_h2_pay_vs_prior_value": h2_pay_on_prior_value(wnba_two),
    }
    (PROCESSED / "robustness.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    report = run_robustness()
    print(json.dumps(report["wnba_h2_pay_vs_prior_value"], indent=2))
    print(pd.read_csv(PROCESSED / "value_definition_robustness.csv").to_string(index=False))


if __name__ == "__main__":
    main()
