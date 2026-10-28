<p align="center">
  <img src="assets/logo-wordmark.svg" alt="Pay-by-Play" width="680"/>
</p>

# Pay-by-Play

**Does pay follow play, and does the pay structure change the answer?**

Cross-league econometrics and a Streamlit decision-support app for PWHL (core), WNBA (next), and WPL (stretch). See [definitions.md](definitions.md), [Brand Identity (PDF)](docs/Pay_By_Play_Brand_Identity.pdf), and [brand guidelines](docs/BRAND_GUIDELINES.md).

## Definition of Done (v1.1)

| League | Pay season | Value (Lens A / B) | Min regulars | Checksum / gate |
|--------|------------|--------------------|--------------|-----------------|
| PWHL | 2026-27 | 2025-26 / 2026-27 | 10 games | Boston team total $1,436,173.50 · 25 contracts |
| WNBA | 2026 | 2025 / 2026 | 15 games | wehoop loader verified before Spotrac |
| WPL | 2026 auction | 2025 / 2026 | 60 balls | Manual auction CSV + Cricsheet (stretch) |

**Value definitions (pre-registered):** see `config/leagues.yaml` keys `value_definitions` A/B/C per league.

**Empirical Bayes:** τ² and σ² estimated via position-level variance decomposition among regulars; `value_raw` z-scored within position before shrinkage.

## Quick start

Requires **Python 3.10+** (3.12 recommended). On this machine:

```powershell
cd D:\Pay_By_Play
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\fetch_data.py
python -m src.pipeline
python scripts\validate.py
streamlit run app\streamlit_app.py
```

Or: `make install pipeline validate app` (set `PYTHON` in the Makefile if needed).

**Brand assets:** regenerate logos and PNGs from the v1.2 spec with `python scripts/export_logo_png.py`.

**Deploy:** see [DEPLOY.md](DEPLOY.md) (Streamlit Community Cloud + GitHub **Trie-hard**).

## Data sources (production)

| League | Pay | Performance |
|--------|-----|-------------|
| PWHL | [PWHLPA salary guide PDF](https://www.pwhlpa.com/salary-guide) (parsed to CSV) | HockeyTech game logs via `sportsdataverse.pwhl` |
| WNBA | [Her Hoop Stats](https://herhoopstats.com/salary-cap-sheet/wnba/players/salary_2026/stats_2025/) 2026 cap hit (cached snapshot if live fetch blocked) | ESPN box scores via `sportsdataverse.wnba` |

```bash
python scripts/fetch_data.py   # refresh raw data
python -m src.pipeline         # analytics + bootstrap CIs + two-lens tables
```

## Repository layout

```
config/leagues.yaml
data/raw/          # salaries, stats (sample PWHL included)
data/processed/    # parquet + scoreboard JSON
src/ingest_*.py
src/value/
src/model/
src/optimize/pwhl_roster.py
src/pipeline.py
app/streamlit_app.py
scripts/validate.py
notebooks/validation.ipynb
```

## Limits

- Disclosed base salary only (PWHL); gaps are a lower bound when bonuses or benefits are omitted.
- Fairness and misallocation are **within-league** rank metrics — not dollar parity across leagues.
- Frame findings as who deserves a raise, not overpaid leaderboards.

## License

AQX Bowl / academic use — add license as needed.
