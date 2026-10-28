from __future__ import annotations

import pandas as pd


def merge_two_lenses(
    lens_a: pd.DataFrame,
    lens_b: pd.DataFrame,
    on: list[str] | None = None,
) -> pd.DataFrame:
    on = on or ["league", "season", "player_id"]
    """Attach Lens B gap and lens_delta = gap_B - gap_A."""
    a = lens_a.rename(columns={"gap": "gap_lens_a", "value_pct": "value_pct_lens_a"})
    b = lens_b.rename(columns={"gap": "gap_lens_b", "value_pct": "value_pct_lens_b"})
    merged = a.merge(
        b[on + ["gap_lens_b", "value_pct_lens_b", "value_shrunk"]],
        on=on,
        how="inner",
        suffixes=("", "_b"),
    )
    merged["lens_delta"] = merged["gap_lens_b"] - merged["gap_lens_a"]
    return merged
