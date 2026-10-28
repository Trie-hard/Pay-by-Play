from __future__ import annotations

import numpy as np
import pandas as pd


def estimate_tau_sigma(
    values: pd.Series,
    group: pd.Series,
) -> tuple[float, float]:
    """
    Variance decomposition among regulars: τ² = between-group, σ² = within-group residual.
    Falls back to global estimates when groups are tiny.
    """
    v = values.astype(float)
    g = group.astype(str)
    overall_var = v.var(ddof=0)
    if np.isnan(overall_var) or overall_var == 0:
        return 0.0, 1.0

    group_means = v.groupby(g).transform("mean")
    between = group_means.groupby(g).first().var(ddof=0)
    within = (v - group_means).var(ddof=0)
    tau2 = float(between) if not np.isnan(between) else 0.0
    sigma2 = float(within) if not np.isnan(within) and within > 0 else float(overall_var)
    return tau2, sigma2


def empirical_bayes_shrink(
    df: pd.DataFrame,
    value_col: str,
    group_cols: list[str],
    exposure_col: str = "games",
    out_col: str = "value_shrunk",
) -> pd.DataFrame:
    """V_shrunk = μ + B * (V_obs - μ), B = τ² / (τ² + σ²/n)."""
    out = df.copy()
    group_key = out[group_cols].astype(str).agg("|".join, axis=1)
    mu = out.groupby(group_key)[value_col].transform("mean")
    tau2, sigma2 = estimate_tau_sigma(out.loc[out["regular_flag"], value_col], group_key.loc[out["regular_flag"]])
    if out["regular_flag"].sum() < 5:
        tau2, sigma2 = _fallback_tau_sigma(out[value_col])

    n = out[exposure_col].clip(lower=1).astype(float)
    B = tau2 / (tau2 + sigma2 / n)
    out[out_col] = mu + B * (out[value_col] - mu)
    return out


def _fallback_tau_sigma(values: pd.Series) -> tuple[float, float]:
    overall_var = values.var(ddof=0)
    if np.isnan(overall_var) or overall_var == 0:
        return 0.0, 1.0
    return overall_var * 0.5, overall_var * 0.5


def game_bootstrap_gap_ci(
    game_level: pd.DataFrame,
    player_id: str,
    value_fn,
    n_boot: int = 1000,
    ci: float = 0.80,
    rng: np.random.Generator | None = None,
) -> tuple[float, float]:
    """
    Resample games with replacement; value_fn maps game subset -> scalar value.
    Returns (ci_low, ci_high) for the player value (not gap — gap applied downstream).
    """
    rng = rng or np.random.default_rng(42)
    games = game_level.loc[game_level["player_id"] == player_id]
    if games.empty:
        return np.nan, np.nan
    idx = games.index.to_numpy()
    estimates = []
    for _ in range(n_boot):
        sample_idx = rng.choice(idx, size=len(idx), replace=True)
        estimates.append(value_fn(games.loc[sample_idx]))
    alpha = (1 - ci) / 2
    return float(np.quantile(estimates, alpha)), float(np.quantile(estimates, 1 - alpha))
