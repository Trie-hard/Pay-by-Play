from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ROOT


def load_wpl_auction(path: Path | None = None) -> pd.DataFrame:
    path = path or ROOT / "data" / "raw" / "wpl_auction.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["league"] = "WPL"
    df["pay_currency"] = "INR"
    df["pay_type"] = "auction"
    return df
