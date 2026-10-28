from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from src.model.metrics import misallocation_index, spearman_fairness


def mechanism_scorecard(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for league, df in frames.items():
        rows.append(
            {
                "league": league,
                "within_league_fairness_spearman": spearman_fairness(df),
                "misallocation_index": misallocation_index(df),
                "n_players": len(df),
                "n_confident_bargains": int(df.get("confident_bargain", pd.Series(dtype=bool)).sum()),
            }
        )
    return pd.DataFrame(rows)


def draft_vs_value_h1(df: pd.DataFrame) -> dict:
    """H1: draft pick vs value for explaining pay."""
    sub = df.dropna(subset=["draft_pick", "pay_pct", "value_pct"]).copy()
    if len(sub) < 10:
        return {"n": len(sub), "note": "insufficient draft data"}
    draft = pd.to_numeric(sub["draft_pick"], errors="coerce")
    r_draft, _ = stats.spearmanr(draft, sub["pay_pct"])
    r_value, _ = stats.spearmanr(sub["value_pct"], sub["pay_pct"])
    return {
        "n": len(sub),
        "spearman_pay_draft": float(r_draft),
        "spearman_pay_value": float(r_value),
        "draft_dominates": abs(r_draft) > abs(r_value),
    }


def wnba_mechanical_raise_decomposition(
    salaries: pd.DataFrame,
    value_prior: pd.DataFrame,
) -> pd.DataFrame:
    """H2: mechanical vs performance-conditioned raise (proxy via prior value percentile)."""
    m = salaries.merge(value_prior, on="name", how="inner", suffixes=("", "_prior"))
    if "pay_raw_prior" not in m.columns and "pay_raw" in m.columns:
        m["raise_usd"] = m["pay_raw"]  # single-year snapshot; use prior pay if added later
    m["value_pct_prior"] = m.get("value_pct_prior", m.get("value_pct", np.nan))
    if m["value_pct_prior"].notna().sum() > 5:
        slope, intercept, _, _, _ = stats.linregress(m["value_pct_prior"], m["pay_raw"])
        m["pay_pred_performance"] = intercept + slope * m["value_pct_prior"]
        m["residual_pay"] = m["pay_raw"] - m["pay_pred_performance"]
    return m


def write_analytics_bundle(processed_dir: Path, scorecard: pd.DataFrame, extras: dict) -> None:
    processed_dir.mkdir(parents=True, exist_ok=True)
    scorecard.to_csv(processed_dir / "mechanism_scorecard.csv", index=False)
    (processed_dir / "analytics_summary.json").write_text(
        json.dumps(extras, indent=2, default=str),
        encoding="utf-8",
    )
