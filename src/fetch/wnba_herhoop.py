from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import requests

from src.config import ROOT

HHS_URL = "https://herhoopstats.com/salary-cap-sheet/wnba/players/salary_2026/stats_2025/"
CITE = "Her Hoop Stats WNBA Salary Cap Database"


def _parse_player_cell(cell: str) -> str:
    """'A'ja Wilson A Wilson' -> \"A'ja Wilson\"."""
    cell = cell.strip()
    if not cell:
        return cell
    parts = cell.split()
    if len(parts) >= 3 and parts[-2][0].isupper() and len(parts[-2]) <= 2:
        return " ".join(parts[:-2])
    return cell


def _parse_salary(val: str) -> float | None:
    val = (val or "").strip()
    if not val or val == "|":
        return None
    cleaned = re.sub(r"[^0-9.]", "", val)
    return float(cleaned) if cleaned else None


def parse_hhs_markdown_table(text: str) -> pd.DataFrame:
    """Parse pipe table (from saved page or WebFetch export)."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if cols[0] == "Player" or cols[0].startswith("---"):
            continue
        if len(cols) < 4:
            continue
        name = _parse_player_cell(cols[0])
        pay = _parse_salary(cols[1])
        rows.append(
            {
                "name": name,
                "pay_raw": pay,
                "signing_status": cols[2],
                "games_2025": _to_int(cols[3]),
                "minutes_2025": _to_float(cols[5]) if len(cols) > 5 else None,
                "points_2025": _to_float(cols[6]) if len(cols) > 6 else None,
                "rebounds_2025": _to_float(cols[20]) if len(cols) > 20 else None,
                "assists_2025": _to_float(cols[21]) if len(cols) > 21 else None,
                "steals_2025": _to_float(cols[23]) if len(cols) > 23 else None,
                "blocks_2025": _to_float(cols[24]) if len(cols) > 24 else None,
            }
        )
    df = pd.DataFrame(rows)
    df = df.dropna(subset=["name"])
    df["season"] = 2026
    df["pay_currency"] = "USD"
    df["pay_type"] = "salary"
    df["source_url"] = HHS_URL
    df["source_tier"] = "aggregator"
    df["source_note"] = CITE
    return df


def _to_int(s: str) -> int | None:
    try:
        return int(re.sub(r"[^0-9]", "", s))
    except (TypeError, ValueError):
        return None


def _to_float(s: str) -> float | None:
    try:
        return float(s.replace("%", ""))
    except (TypeError, ValueError):
        return None


def fetch_wnba_salaries(dest_dir: Path | None = None) -> Path:
    dest_dir = dest_dir or ROOT / "data" / "raw"
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / "wnba_salaries.csv"
    cache_html = dest_dir / "hhs_wnba_salary_2026.html"
    cache_md = dest_dir / "hhs_wnba_salary_2026_snapshot.md"

    text = ""
    try:
        r = requests.get(
            HHS_URL,
            timeout=60,
            headers={"User-Agent": "PayByPlay/0.1 (research; +https://github.com)"},
        )
        if r.status_code == 200 and len(r.text) > 5000:
            text = r.text
            cache_html.write_text(text, encoding="utf-8")
    except requests.RequestException:
        pass

    if not text and cache_html.exists():
        text = cache_html.read_text(encoding="utf-8")
    if not text and cache_md.exists():
        df = parse_hhs_markdown_table(cache_md.read_text(encoding="utf-8"))
        df.to_csv(out, index=False)
        return out

    if text and "<table" in text:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(text, "lxml")
        table = soup.find("table")
        if table:
            md_lines = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
                md_lines.append("| " + " | ".join(cells) + " |")
            df = parse_hhs_markdown_table("\n".join(md_lines))
            df.to_csv(out, index=False)
            return out

    if cache_md.exists():
        df = parse_hhs_markdown_table(cache_md.read_text(encoding="utf-8"))
    else:
        raise FileNotFoundError(
            f"Could not download {HHS_URL}. Save the page to {cache_html} "
            f"or a pipe table to {cache_md}."
        )
    df.to_csv(out, index=False)
    return out
