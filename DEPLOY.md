# Deploy Pay-by-Play

The app is a **Streamlit** dashboard (`app/streamlit_app.py`). The recommended host is **Streamlit Community Cloud** (free tier, connects to GitHub).

## Streamlit Community Cloud

1. Push this repo to GitHub (see README).
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub (**Trie-hard** account).
3. **New app** → pick repository **Trie-hard/Pay-by-Play** (or your fork).
4. Set:
   - **Main file path:** `app/streamlit_app.py`
   - **Branch:** `main`
   - **Python:** 3.12 (or 3.10+)
5. Deploy. First boot may take a few minutes while dependencies install from `requirements.txt`.

The repo includes **processed parquet/JSON** under `data/processed/` so the live app works without running the full fetch pipeline on Cloud. To refresh data locally:

```powershell
python scripts/fetch_data.py
python -m src.pipeline
```

Then commit updated files under `data/processed/` (and `data/raw/` if needed) and redeploy.

## Secrets

No secrets are required for the public read-only dashboard. If you add authenticated data sources later, use **Streamlit Cloud → App settings → Secrets** (same shape as `.streamlit/secrets.toml`). Do not commit secrets.

## Other hosts

- **Railway / Render / Fly.io:** run `streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0` from the repo root.
- **Cursor Origin:** not used for this project; the canonical remote is GitHub under **Trie-hard**.

## Contributors

Commits should use **your** Git identity (`git config user.name` / `user.email` on your machine). Do not add `Co-authored-by` trailers for AI tools if you want GitHub’s contributor graph to list only humans.
