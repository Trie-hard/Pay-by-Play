from __future__ import annotations

import numpy as np
import pandas as pd

from src.value.pwhl import skater_value_per_game


def _game_value_row(row: pd.Series) -> float:
    pos = str(row.get("position", "F")).upper()
    if pos == "G":
        return float(row.get("save_pct", 0.9) or 0.9)
    one = pd.DataFrame(
        [
            {
                "games": 1,
                "goals": row.get("goals", 0) or 0,
                "assists": row.get("assists", 0) or 0,
                "shots": row.get("shots", 0) or 0,
                "penalties_drawn": 0,
                "penalties_taken": (row.get("penalty_minutes", 0) or 0) / 2,
                "position": pos,
            }
        ]
    )
    return float(skater_value_per_game(one, "A").iloc[0])


def _gap_bootstrap_from_values(
    boot_values: np.ndarray,
    pay_pct: float,
    peer_vals: np.ndarray,
    pos_loc: int,
    n_boot: int,
    rng: np.random.Generator,
    ci: float,
) -> tuple[float, float]:
    n_g = len(boot_values)
    draws = rng.choice(boot_values, size=(n_boot, n_g), replace=True)
    boot_means = draws.mean(axis=1)
    peers = np.delete(peer_vals, pos_loc)
    # Percentile among the position cohort, with this player's value replaced.
    below = (peers[None, :] < boot_means[:, None]).sum(axis=1)
    equal = (peers[None, :] == boot_means[:, None]).sum(axis=1)
    value_pct = (below + 0.5 * equal + 0.5) / (len(peers) + 1) * 100
    gaps = value_pct - pay_pct
    alpha = (1 - ci) / 2
    return float(np.quantile(gaps, alpha)), float(np.quantile(gaps, 1 - alpha))


def bootstrap_gap_intervals(
    player_season: pd.DataFrame,
    game_logs: pd.DataFrame,
    n_boot: int = 120,
    ci: float = 0.80,
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    out = player_season.copy()
    logs = game_logs.dropna(subset=["player_id"]).copy()
    logs["player_id"] = logs["player_id"].astype(int)

    ci_low = np.full(len(out), np.nan)
    ci_high = np.full(len(out), np.nan)
    peer_cache: dict[str, np.ndarray] = {}

    for i, (idx, row) in enumerate(out.iterrows()):
        pid = row.get("player_id")
        if pd.isna(pid) or pd.isna(row.get("pay_pct")):
            continue
        g = logs.loc[logs["player_id"] == int(pid)]
        if len(g) < 3:
            continue
        game_vals = g.apply(_game_value_row, axis=1).to_numpy()
        pos = str(row["position"])
        if pos not in peer_cache:
            peer_cache[pos] = out.loc[out["position"] == pos, "value_shrunk"].astype(float).to_numpy()
        peer_vals = peer_cache[pos]
        pos_loc = list(out.loc[out["position"] == pos].index).index(idx)
        lo, hi = _gap_bootstrap_from_values(
            game_vals, float(row["pay_pct"]), peer_vals, pos_loc, n_boot, rng, ci
        )
        ci_low[i] = lo
        ci_high[i] = hi

    out["ci_low"] = ci_low
    out["ci_high"] = ci_high
    return out


def bootstrap_wnba_gap_from_box(
    player_season: pd.DataFrame,
    box: pd.DataFrame,
    n_boot: int = 80,
    ci: float = 0.80,
    seed: int = 42,
) -> pd.DataFrame:
    from src.value.wnba import attach_wnba_values

    rng = np.random.default_rng(seed)
    out = player_season.copy()
    box = box.dropna(subset=["athlete_id"]).copy()
    ci_low = np.full(len(out), np.nan)
    ci_high = np.full(len(out), np.nan)
    peer_cache: dict[str, np.ndarray] = {}

    # Precompute per-game value contributions
    game_vals_by_athlete: dict[int, np.ndarray] = {}
    for aid, g in box.groupby("athlete_id"):
        vals = []
        for _, row in g.iterrows():
            tmp = attach_wnba_values(
                pd.DataFrame(
                    [
                        {
                            "minutes": max(row["minutes"], 0.1),
                            "points": row["points"],
                            "rebounds": row["rebounds"],
                            "assists": row["assists"],
                            "steals": row["steals"],
                            "blocks": row["blocks"],
                            "position": row.get("athlete_position_abbreviation", "G"),
                        }
                    ]
                ),
                "A",
            )
            vals.append(float(tmp["value_raw"].iloc[0]))
        game_vals_by_athlete[int(aid)] = np.array(vals)

    for i, (idx, row) in enumerate(out.iterrows()):
        aid = row.get("athlete_id")
        if pd.isna(aid) or pd.isna(row.get("pay_pct")):
            continue
        game_vals = game_vals_by_athlete.get(int(aid))
        if game_vals is None or len(game_vals) < 5:
            continue
        pos = str(row["position"])
        if pos not in peer_cache:
            peer_cache[pos] = out.loc[out["position"] == pos, "value_shrunk"].astype(float).to_numpy()
        peer_vals = peer_cache[pos]
        pos_loc = list(out.loc[out["position"] == pos].index).index(idx)
        lo, hi = _gap_bootstrap_from_values(
            game_vals, float(row["pay_pct"]), peer_vals, pos_loc, n_boot, rng, ci
        )
        ci_low[i] = lo
        ci_high[i] = hi

    out["ci_low"] = ci_low
    out["ci_high"] = ci_high
    return out
