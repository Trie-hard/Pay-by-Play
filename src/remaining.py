from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from scipy import stats

from src.config import ROOT
from src.match import normalize_name
from src.model.gap import add_pay_and_value_percentiles, confident_bargain_mask
from src.model.metrics import misallocation_index, spearman_fairness
from src.model.shrink import empirical_bayes_shrink

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TEAM_IDS = ["1461", "1465", "1468", "1472", "1479"]


def _inr(token: str) -> float | None:
    token = token.replace(",", "").strip()
    m = re.search(r"([\d.]+)\s*(Cr|L)", token, re.I)
    if not m:
        return None
    amount = float(m.group(1))
    return amount * (1e7 if m.group(2).lower() == "cr" else 1e5)


def fetch_wpl_auction() -> pd.DataFrame:
    rows = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for team_id in TEAM_IDS:
        url = f"https://www.cricbuzz.com/cricket-series/wpl-2026/auction/teams/{team_id}"
        html = requests.get(url, timeout=40, headers=headers).text
        soup = BeautifulSoup(html, "lxml")
        cells = [c.get_text(" ", strip=True) for c in soup.find_all(id="table-cell")]
        for i in range(0, len(cells) - 1, 3):
            label, price = cells[i], cells[i + 1]
            pay = _inr(price)
            if pay is None:
                continue
            name = re.split(r"\s+(India|Australia|England|New Zealand|South Africa|West Indies|Ireland|Scotland)\b", label)[0]
            name = name.replace("• retained", "").strip()
            retained = "retained" in label.lower()
            rows.append(
                {
                    "name": name,
                    "pay_raw": pay,
                    "pay_currency": "INR",
                    "pay_type": "auction" if not retained else "retention",
                    "retained": retained,
                    "team_id": team_id,
                    "season": "2026",
                    "source_url": url,
                    "source_tier": "aggregator",
                }
            )
    df = pd.DataFrame(rows).drop_duplicates(subset=["name"])
    df.to_csv(RAW / "wpl_auction.csv", index=False)
    return df


def _phase(over: int) -> str:
    if over < 6:
        return "pp"
    if over < 15:
        return "middle"
    return "death"


def wpl_value_from_cricsheet(zip_path: Path | None = None) -> pd.DataFrame:
    zip_path = zip_path or RAW / "wpl_json.zip"
    bat_rows = []
    bowl_rows = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if not name.endswith(".json"):
                continue
            match = json.loads(zf.read(name))
            season = str(match["info"].get("season"))
            for inn in match.get("innings", []):
                for over in inn.get("overs", []):
                    phase = _phase(int(over["over"]))
                    for delivery in over.get("deliveries", []):
                        runs = delivery["runs"]["batter"]
                        bat_rows.append((season, delivery["batter"], phase, runs, 1))
                        wicket = 1 if delivery.get("wickets") else 0
                        bowl_rows.append((season, delivery["bowler"], phase, delivery["runs"]["total"], wicket))
    bat = pd.DataFrame(bat_rows, columns=["season", "name", "phase", "runs", "balls"])
    bowl = pd.DataFrame(bowl_rows, columns=["season", "name", "phase", "runs_conceded", "wickets"])
    phase_rr = bat.groupby("phase")["runs"].mean()
    bat["above"] = bat["runs"] - bat["phase"].map(phase_rr)
    wicket_value = {"pp": 22, "middle": 18, "death": 14}
    bowl["wicket_runs"] = bowl["wickets"] * bowl["phase"].map(wicket_value)
    bat_g = bat.groupby(["season", "name"], as_index=False).agg(balls=("balls", "sum"), runs_above=("above", "sum"), runs=("runs", "sum"))
    bowl_g = bowl.groupby(["season", "name"], as_index=False).agg(
        balls_bowled=("wickets", "size"), wickets=("wickets", "sum"), wicket_runs=("wicket_runs", "sum"), runs_conceded=("runs_conceded", "sum")
    )
    out = bat_g.merge(bowl_g, on=["season", "name"], how="outer")
    for col in ("balls", "runs_above", "runs", "balls_bowled", "wickets", "wicket_runs", "runs_conceded"):
        out[col] = out[col].fillna(0)
    out["value_raw"] = out["runs_above"] + out["wicket_runs"] - 0.15 * out["runs_conceded"]
    out["games"] = 1
    out["exposure"] = out["balls"] + out["balls_bowled"]
    out["position"] = np.where(out["wickets"] >= out["runs"] / 25, "BOWL", "BAT")
    out["league"] = "WPL"
    out["regular_flag"] = out["exposure"] >= 60
    return out


def score_wpl(auction: pd.DataFrame, values: pd.DataFrame, season: str) -> pd.DataFrame:
    val = values[values["season"] == season].copy()
    auction = auction.copy()
    auction["last"] = auction["name"].map(lambda n: normalize_name(n).split()[-1] if normalize_name(n) else "")
    val["last"] = val["name"].map(lambda n: normalize_name(n).split()[-1] if normalize_name(n) else "")
    unique_last = val["last"].value_counts()
    val = val[val["last"].map(unique_last) == 1]
    merged = auction.merge(val, on="last", how="inner", suffixes=("", "_cs"))
    merged["name"] = merged["name"]
    merged = empirical_bayes_shrink(merged, "value_raw", ["league", "position"], exposure_col="exposure")
    merged = add_pay_and_value_percentiles(merged, "WPL")
    merged["value_definition"] = "A"
    merged["lens"] = "B" if season == "2025/26" else "A"
    return merged


def parse_pwhl_draft(html_path: Path | None = None) -> pd.DataFrame:
    html_path = html_path or RAW / "pwhl_2025_draft.html"
    tables = pd.read_html(html_path)
    draft = tables[0]
    draft.columns = [str(c).strip() for c in draft.columns]
    pick_col = next(c for c in draft.columns if "pick" in c.lower())
    draft["draft_pick"] = draft[pick_col].astype(str).str.split("|").str[-1]
    draft["draft_pick"] = pd.to_numeric(draft["draft_pick"], errors="coerce")
    draft = draft.rename(columns={"Player": "name", "player": "name"})
    draft["name_key"] = draft["name"].map(normalize_name)
    draft.to_csv(RAW / "pwhl_2025_draft.csv", index=False)
    return draft


def h1_draft(pwhl: pd.DataFrame, draft: pd.DataFrame) -> dict:
    sal = pwhl.drop(columns=["draft_pick"], errors="ignore").copy()
    sal["name_key"] = sal["name"].map(normalize_name)
    m = sal.merge(draft[["name_key", "draft_pick"]], on="name_key", how="inner")
    m = m.dropna(subset=["draft_pick", "pay_raw", "value_pct"])
    if len(m) < 8:
        return {"n": int(len(m)), "note": "too few drafted players matched to the salary guide"}
    r_pick, p_pick = stats.spearmanr(m["draft_pick"], m["pay_raw"])
    r_val, p_val = stats.spearmanr(m["value_pct"], m["pay_raw"])
    return {
        "n": int(len(m)),
        "spearman_pay_vs_draft_pick": float(r_pick),
        "p_draft": float(p_pick),
        "spearman_pay_vs_value": float(r_val),
        "p_value": float(p_val),
        "production_beats_draft_slot": bool(abs(r_val) > abs(r_pick)),
    }


def h2_raises(pay_2025: pd.DataFrame, pay_2026: pd.DataFrame, two_lens: pd.DataFrame) -> dict:
    a = pay_2025.rename(columns={"pay_raw": "pay_2025"})
    b = pay_2026.rename(columns={"pay_raw": "pay_2026"})
    a["name_key"] = a["name"].map(normalize_name)
    b["name_key"] = b["name"].map(normalize_name)
    m = a[["name_key", "name", "pay_2025"]].merge(b[["name_key", "pay_2026"]], on="name_key", how="inner")
    prior = two_lens.drop_duplicates("athlete_id") if "athlete_id" in two_lens.columns else two_lens
    prior = prior.copy()
    prior["name_key"] = prior["name"].map(normalize_name)
    m = m.merge(prior[["name_key", "value_pct_lens_a"]], on="name_key", how="inner")
    m = m.dropna(subset=["pay_2025", "pay_2026", "value_pct_lens_a"])
    m["raise_usd"] = m["pay_2026"] - m["pay_2025"]
    slope, intercept, r, p, _ = stats.linregress(m["value_pct_lens_a"], m["raise_usd"])
    m["raise_hat"] = intercept + slope * m["value_pct_lens_a"]
    ss_tot = float(((m["raise_usd"] - m["raise_usd"].mean()) ** 2).sum())
    ss_res = float(((m["raise_usd"] - m["raise_hat"]) ** 2).sum())
    return {
        "n": int(len(m)),
        "mean_raise_usd": float(m["raise_usd"].mean()),
        "median_raise_usd": float(m["raise_usd"].median()),
        "r_squared_raise_on_prior_value": float(r**2),
        "slope_usd_per_value_pct": float(slope),
        "p_value": float(p),
        "share_of_raise_variance_not_linear_in_prior_value": float(ss_res / ss_tot) if ss_tot else None,
        "source": "Her Hoop Stats 2025 and 2026 cap hits, matched by player name",
    }
