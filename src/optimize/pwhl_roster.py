from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import pulp

POSITION_GROUP = {
    "G": "G",
    "D": "D",
    "LD": "D",
    "RD": "D",
    "F": "F",
    "C": "F",
    "LW": "F",
    "RW": "F",
}


@dataclass
class RosterResult:
    selected_ids: list[int]
    total_pay: float
    total_value: float
    avg_salary: float
    status: str
    message: str = ""


def _position_group(position: str) -> str:
    return POSITION_GROUP.get(str(position).upper(), "F")


def optimize_roster(
    pool: pd.DataFrame,
    roster_size: int,
    target_avg: float = 60099.99,
    band_pct: float = 0.10,
    min_by_position: dict[str, int] | None = None,
) -> RosterResult:
    """
    Maximize sum(value_shrunk) subject to roster size, position mins, and avg salary band.
    Uses disclosed base salaries only.
    """
    work = pool.dropna(subset=["player_id", "pay_raw", "value_shrunk"]).copy()
    work["player_id"] = work["player_id"].astype(int)
    work = work.drop_duplicates(subset=["player_id"])
    work["pos_group"] = work["position"].map(_position_group)

    if len(work) < roster_size:
        return RosterResult([], 0.0, 0.0, 0.0, "Infeasible", f"Pool has {len(work)} players, roster asks for {roster_size}.")

    counts = work["pos_group"].value_counts().to_dict()
    requested = min_by_position or {"F": 6, "D": 4, "G": 1}
    mins = {pos: min(requested.get(pos, 0), int(counts.get(pos, 0))) for pos in ("F", "D", "G")}
    if sum(mins.values()) > roster_size:
        return RosterResult([], 0.0, 0.0, 0.0, "Infeasible", "Position minimums exceed roster size.")

    low = (1 - band_pct) * target_avg * roster_size
    high = (1 + band_pct) * target_avg * roster_size
    value_of = dict(zip(work["player_id"], work["value_shrunk"].astype(float)))
    pay_of = dict(zip(work["player_id"], work["pay_raw"].astype(float)))
    ids = list(value_of)

    prob = pulp.LpProblem("pwhl_roster", pulp.LpMaximize)
    x = prob.add_variable_dicts("pick", ids, cat="Binary")

    prob += pulp.lpSum(x[i] * value_of[i] for i in ids)
    prob += pulp.lpSum(x[i] for i in ids) == roster_size
    prob += pulp.lpSum(x[i] * pay_of[i] for i in ids) >= low
    prob += pulp.lpSum(x[i] * pay_of[i] for i in ids) <= high

    for pos, mn in mins.items():
        pos_ids = work.loc[work["pos_group"] == pos, "player_id"].tolist()
        if mn > 0 and pos_ids:
            prob += pulp.lpSum(x[i] for i in pos_ids) >= mn

    stats = prob.solve(pulp.HiGHS(msg=False))
    status = stats.status.name
    if status != "Optimal":
        return RosterResult(
            [],
            0.0,
            0.0,
            0.0,
            status,
            f"No roster of {roster_size} fits the ±{band_pct:.0%} average-salary band around ${target_avg:,.0f} "
            f"with position minimums {mins}.",
        )

    chosen = [i for i in ids if (pulp.value(x[i]) or 0) >= 0.5]
    pay = sum(pay_of[i] for i in chosen)
    val = sum(value_of[i] for i in chosen)
    return RosterResult(chosen, pay, val, pay / roster_size, status, f"Position minimums applied: {mins}.")


def suggest_swaps(
    current: pd.DataFrame,
    pool: pd.DataFrame,
    result: RosterResult,
    max_swaps: int = 3,
) -> list[str]:
    if result.status != "Optimal":
        return [result.message]
    current_ids = set(current["player_id"].dropna().astype(int))
    optimal_ids = set(result.selected_ids)
    drops = list(current_ids - optimal_ids)[:max_swaps]
    adds = list(optimal_ids - current_ids)[:max_swaps]
    lines = []
    for d, a in zip(drops, adds):
        drow = pool.loc[pool["player_id"].astype(int) == d].iloc[0]
        arow = pool.loc[pool["player_id"].astype(int) == a].iloc[0]
        lines.append(
            f"Drop {drow['name']} (${drow['pay_raw']:,.0f}) → "
            f"add {arow['name']} (${arow['pay_raw']:,.0f}); "
            f"Δvalue {arow['value_shrunk'] - drow['value_shrunk']:.2f}"
        )
    if not lines:
        lines.append("Current list already matches the solved roster.")
    return lines
