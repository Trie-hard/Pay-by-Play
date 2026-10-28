from __future__ import annotations

import pandas as pd


def negotiation_line(row: pd.Series) -> str:
    name = row["name"]
    gap = row["gap"]
    ci_lo, ci_hi = row.get("ci_low", gap), row.get("ci_high", gap)
    pay_pct = row.get("pay_pct", 0)
    val_pct = row.get("value_pct", 0)
    return (
        f"{name} ranks at the {pay_pct:.0f}th pay percentile but the "
        f"{val_pct:.0f}th value percentile among {row['position']}s "
        f"(gap +{gap:.1f}; 80% CI {ci_lo:.1f} to {ci_hi:.1f}) — strong case for a raise."
    )
