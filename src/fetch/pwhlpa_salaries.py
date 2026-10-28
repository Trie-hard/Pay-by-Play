from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pdfplumber
import requests

from src.config import ROOT

PDF_URL = (
    "https://cdn.prod.website-files.com/65038094882d837d666bf1bb/"
    "69efbccd65fdec269086fc2c_PlayerSalaries_2025-2026.pdf"
)
GUIDE_PAGE = "https://www.pwhlpa.com/salary-guide"


def _parse_pay(raw: str) -> float:
    return float(re.sub(r"[^0-9.]", "", raw))


def parse_salary_pdf(path: Path) -> list[dict]:
    rows: list[dict] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                if not table:
                    continue
                start = 1 if table[0] and table[0][0] == "First Name" else 0
                for r in table[start:]:
                    if len(r) < 4 or not r[0] or r[0] == "First Name":
                        continue
                    rows.append(
                        {
                            "first_name": r[0].strip(),
                            "last_name": r[1].strip(),
                            "name": f"{r[0].strip()} {r[1].strip()}",
                            "team": r[2].strip(),
                            "pay_raw": _parse_pay(r[3]),
                            "season": "2025-26",
                            "pay_as_of_date": "2026-04-12",
                            "source_url": GUIDE_PAGE,
                            "source_tier": "primary",
                        }
                    )
    return rows


def fetch_pwhlpa_salaries(
    dest_dir: Path | None = None,
    force: bool = False,
) -> Path:
    dest_dir = dest_dir or ROOT / "data" / "raw"
    dest_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = dest_dir / "pwhlpa_salary_guide_2025-26.pdf"
    csv_path = dest_dir / "pwhl_salaries.csv"

    if force or not pdf_path.exists():
        pdf_path.write_bytes(requests.get(PDF_URL, timeout=120).content)

    import pandas as pd

    rows = parse_salary_pdf(pdf_path)
    df = pd.DataFrame(rows)
    df["pay_currency"] = "USD"
    df.to_csv(csv_path, index=False)
    return csv_path
