from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ChecksumResult:
    team: str
    expected_total: float
    actual_total: float
    expected_contracts: int | None
    actual_contracts: int
    ok: bool
    message: str


def reconcile_team_payroll(
    salaries: pd.DataFrame,
    team: str,
    expected_total: float,
    expected_contracts: int | None = None,
    team_col: str = "team",
    pay_col: str = "pay_raw",
    tolerance: float = 0.01,
) -> ChecksumResult:
    subset = salaries.loc[salaries[team_col] == team]
    actual_total = float(subset[pay_col].sum())
    actual_contracts = len(subset)
    total_ok = abs(actual_total - expected_total) <= tolerance
    count_ok = True
    if expected_contracts is not None:
        count_ok = actual_contracts == expected_contracts
    ok = total_ok and count_ok
    msg = (
        f"{team}: total {actual_total:,.2f} vs expected {expected_total:,.2f}; "
        f"contracts {actual_contracts}"
        + (f" vs expected {expected_contracts}" if expected_contracts else "")
    )
    return ChecksumResult(team, expected_total, actual_total, expected_contracts, actual_contracts, ok, msg)
