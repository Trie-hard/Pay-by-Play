from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.brand import FAVICON, FAVICON_SMALL, LOGO_ICON, colors
from app.chrome import home_tab_html, top_chrome_html
from app.charts import dedupe_players, lens_delta_histogram, pay_value_scatter, raise_radar_chart
from app.team_geo import MAP_LAYER_ID, filter_by_team_key, pins_for_keys, team_keys_in_frame, team_map_deck
from src.config import ROOT as PROJECT_ROOT
from src.optimize.pwhl_roster import optimize_roster, suggest_swaps

PROCESSED = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_table(name: str) -> pd.DataFrame:
    return pd.read_parquet(PROCESSED / name)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def inject_css() -> None:
    dark = getattr(st.context.theme, "type", None) == "dark"
    c = colors(dark=dark)
    ink = c["ink"]
    paper = c["paper"]
    rail_bg = c["rail"]
    red = c["red"]
    blue = c["blue"]
    yellow = c["yellow"]
    gray = c["gray"]
    rail_grid = f"{ink}0A" if dark else f"{ink}07"
    st.markdown(
        f"""
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
          :root {{
            --pbp-content-max: 1100px;
            --pbp-rail-w: max(0px, calc((100vw - var(--pbp-content-max)) / 2));
            font-variant-numeric: tabular-nums lining-nums;
          }}
          * {{
            font-variant-numeric: tabular-nums lining-nums;
          }}
          .block-container {{
            max-width: var(--pbp-content-max);
            padding-top: 2.75rem;
            padding-bottom: 1.5rem;
          }}
          [data-testid="stAppViewContainer"] .main .block-container {{
            padding-top: 2.75rem;
          }}
          [data-testid="stAppViewContainer"],
          [data-testid="stAppViewContainer"] .main {{
            position: relative;
            z-index: 1;
          }}
          div[data-testid="stMarkdownContainer"],
          div[data-testid="stMarkdown"] {{
            overflow: visible !important;
          }}
          [data-testid="stLogo"] img {{
            border: 3px solid {ink};
            border-radius: 0;
            background: {paper};
          }}
          .stApp {{
            background: {paper};
            position: relative;
            min-height: 100vh;
          }}
          @media (min-width: 1120px) {{
            .stApp::before,
            .stApp::after {{
              content: "";
              position: fixed;
              top: 0;
              bottom: 0;
              width: var(--pbp-rail-w);
              z-index: 0;
              pointer-events: none;
              background-color: {rail_bg};
              background-repeat: no-repeat;
            }}
            .stApp::before {{
              left: 0;
              border-right: 2px solid {ink};
              background-image:
                linear-gradient({rail_grid} 1px, transparent 1px),
                linear-gradient(90deg, {rail_grid} 1px, transparent 1px),
                linear-gradient({red}, {red}),
                linear-gradient({blue}, {blue}),
                linear-gradient({yellow}, {yellow}),
                linear-gradient({ink}, {ink}),
                linear-gradient({paper}, {paper});
              background-size:
                22px 22px,
                22px 22px,
                min(68%, 220px) min(26vh, 240px),
                min(14%, 48px) min(42vh, 380px),
                min(52%, 180px) min(11vh, 100px),
                100% 3px,
                min(28%, 72px) min(28%, 72px);
              background-position:
                0 0,
                0 0,
                14% 9vh,
                78% 16vh,
                22% calc(100% - 20vh),
                0 calc(50% - 1.5px),
                8% calc(100% - 11vh);
            }}
            .stApp::after {{
              right: 0;
              border-left: 2px solid {ink};
              background-image:
                linear-gradient({rail_grid} 1px, transparent 1px),
                linear-gradient(90deg, {rail_grid} 1px, transparent 1px),
                linear-gradient({blue}, {blue}),
                linear-gradient({red}, {red}),
                linear-gradient({yellow}, {yellow}),
                linear-gradient({ink}, {ink}),
                linear-gradient({ink}, {ink});
              background-size:
                22px 22px,
                22px 22px,
                min(75%, 260px) min(18vh, 170px),
                min(40%, 120px) 3px,
                min(36%, 100px) min(36%, 100px),
                3px min(55vh, 480px),
                min(60%, 200px) 3px;
              background-position:
                0 0,
                0 0,
                18% 7vh,
                12% 38vh,
                62% 52vh,
                24% 24vh,
                10% calc(100% - 14vh);
            }}
          }}
          h2 {{
            font-family: Archivo, Helvetica, Arial, sans-serif !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 1.02rem !important;
            border-bottom: 2px solid {ink};
            padding-bottom: 0.3rem;
            margin-top: 1.25rem !important;
            margin-bottom: 0.65rem !important;
          }}
          h3 {{
            font-family: Archivo, Helvetica, Arial, sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.86rem !important;
            margin-top: 1rem !important;
            margin-bottom: 0.45rem !important;
            opacity: 0.92;
          }}
          h4 {{
            font-family: Archivo, Helvetica, Arial, sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 0.78rem !important;
            margin-top: 0.85rem !important;
            margin-bottom: 0.35rem !important;
            opacity: 0.85;
          }}
          .dstijl-hero {{
            border: 2px solid {ink};
            padding: 1.35rem 1.25rem 1.15rem;
            margin: 0 0 1rem;
            background: {paper};
            position: relative;
            overflow: visible;
          }}
          .dstijl-hero-grid {{
            position: absolute;
            top: 0;
            right: 0;
            width: 64px;
            height: 64px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            border-left: 2px solid {ink};
            border-bottom: 2px solid {ink};
          }}
          .dstijl-hero-grid span:nth-child(1) {{ background: #E60012; }}
          .dstijl-hero-grid span:nth-child(2) {{ background: #0047AB; }}
          .dstijl-hero-grid span:nth-child(3) {{ background: #FFDD00; }}
          .dstijl-hero-grid span:nth-child(4) {{ background: {paper}; }}
          .dstijl-title {{
            font-family: Archivo, Helvetica, Arial, sans-serif;
            font-size: clamp(1.55rem, 3.5vw, 2.1rem);
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0 0 0.5rem;
            line-height: 1.15;
            color: {ink};
            padding-right: 72px;
          }}
          .dstijl-meta {{
            margin: 0.65rem 0 0;
            font-family: Archivo, Helvetica, Arial, sans-serif;
            font-size: 0.8rem;
            line-height: 1.45;
            color: {ink};
            opacity: 0.72;
            max-width: 42rem;
          }}
          .dstijl-pay {{ color: {ink}; }}
          .dstijl-by {{
            color: {gray};
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-weight: 700;
            letter-spacing: 0.08em;
          }}
          .dstijl-play {{ color: {red}; }}
          .lede {{
            color: {ink};
            font-family: Archivo, Helvetica, Arial, sans-serif;
            font-size: 0.95rem;
            line-height: 1.5;
            max-width: 46rem;
            margin: 0;
            opacity: 0.88;
          }}
          .stTabs {{
            border: 2px solid {ink};
            background: {paper};
            margin-top: 0.25rem;
          }}
          .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            background: {paper};
            border-bottom: 3px solid {ink};
            flex-wrap: nowrap;
            padding: 0;
            width: 100%;
          }}
          .stTabs [data-baseweb="tab-border"],
          .stTabs [data-baseweb="tab-highlight"] {{
            display: none !important;
          }}
          .stTabs button[data-baseweb="tab"] {{
            flex: 1 1 0;
            min-width: 0;
            min-height: 2.85rem;
            margin: 0 !important;
            padding: 0.7rem 1rem !important;
            background: {paper} !important;
            border: none !important;
            border-right: 3px solid {ink} !important;
            border-radius: 0 !important;
            color: {ink} !important;
            font-family: Archivo, Helvetica, Arial, sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.7rem !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            line-height: 1.2;
            white-space: nowrap;
            justify-content: center;
            transition: background 0.15s ease, color 0.15s ease;
          }}
          .stTabs button[data-baseweb="tab"]:last-child {{
            border-right: none !important;
          }}
          .stTabs button[data-baseweb="tab"]:hover:not([aria-selected="true"]) {{
            background: var(--st-secondary-background-color) !important;
          }}
          .stTabs button[data-baseweb="tab"][aria-selected="true"] {{
            color: #FFFFFF !important;
            background: #E60012 !important;
            box-shadow: inset 0 -4px 0 {ink};
          }}
          .stTabs button[data-baseweb="tab"][aria-selected="true"]:hover {{
            background: #CC0010 !important;
          }}
          .stTabs [data-baseweb="tab-panel"] {{
            padding: 1rem 0.25rem 0.5rem;
            border-top: none;
          }}
          @media (max-width: 900px) {{
            .stTabs [data-baseweb="tab-list"] {{ flex-wrap: wrap; }}
            .stTabs button[data-baseweb="tab"] {{
              flex: 1 1 45%;
              border-bottom: 3px solid {ink} !important;
            }}
            .stTabs button[data-baseweb="tab"]:nth-child(2n) {{
              border-right: none !important;
            }}
          }}
          .score-row {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 0;
            border: 3px solid {ink};
            margin-bottom: 1.25rem;
            background: {paper};
          }}
          @media (max-width: 720px) {{ .score-row {{ grid-template-columns: 1fr; }} }}
          .score-cell {{
            padding: 0.85rem 1rem 0.95rem;
            border-right: 3px solid {ink};
            min-height: 6.8rem;
            background: {paper};
            color: {ink};
            position: relative;
            transition: background 0.15s ease;
          }}
          .score-cell:last-child {{ border-right: none; }}
          @media (max-width: 720px) {{
            .score-cell {{ border-right: none; border-bottom: 3px solid {ink}; }}
            .score-cell:last-child {{ border-bottom: none; }}
          }}
          .score-cell:hover {{
            background: var(--st-secondary-background-color);
          }}
          .score-cell--blue {{ border-top: 6px solid #0047AB; }}
          .score-cell--yellow {{ border-top: 6px solid #FFDD00; }}
          .score-cell--red {{ border-top: 6px solid #E60012; }}
          .score-league {{
            font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em;
            font-weight: 800;
            opacity: 0.82;
          }}
          .score-num {{
            font-size: 2.25rem; font-weight: 800;
            font-family: Archivo, Helvetica, Arial, sans-serif;
            line-height: 1.05;
            margin: 0.25rem 0 0.15rem;
            letter-spacing: -0.02em;
          }}
          .score-meta {{ font-size: 0.78rem; font-weight: 600; opacity: 0.78; }}
          .dstijl-callout {{
            border: 2px solid {ink};
            border-left: 8px solid #0047AB;
            padding: 0.55rem 0.75rem;
            margin: 0.45rem 0 0.65rem;
            background: var(--st-secondary-background-color);
            font-size: 0.92rem;
          }}
          .dstijl-home {{
            font-family: Archivo, Helvetica, Arial, sans-serif;
            color: {ink};
            padding: 0.15rem 0 0.5rem;
          }}
          .dstijl-home-hook {{
            font-size: clamp(1.15rem, 2.5vw, 1.45rem);
            font-weight: 700;
            line-height: 1.35;
            margin: 0 0 1.35rem;
            padding: 0 0 0.85rem;
            border-bottom: 3px solid {ink};
            max-width: 40rem;
          }}
          .dstijl-home-hook em {{ font-style: normal; color: #E60012; }}
          .dstijl-home-h {{
            font-size: 0.72rem !important;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin: 1.35rem 0 0.65rem !important;
            font-weight: 800 !important;
          }}
          .dstijl-home-split {{
            display: grid;
            grid-template-columns: 1.2fr 0.9fr;
            gap: 1rem;
            align-items: start;
          }}
          @media (max-width: 780px) {{
            .dstijl-home-split {{ grid-template-columns: 1fr; }}
          }}
          .dstijl-home-prose p {{
            margin: 0 0 0.75rem;
            font-size: 0.94rem;
            line-height: 1.55;
            opacity: 0.92;
            max-width: 36rem;
          }}
          .dstijl-home-aside {{
            border: 2px solid {ink};
            border-top: 5px solid #0047AB;
            padding: 1rem 1.05rem 1.05rem;
            background: var(--st-secondary-background-color);
          }}
          .dstijl-home-aside-label {{
            display: block;
            font-size: 0.62rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-weight: 800;
            margin-bottom: 0.4rem;
            opacity: 0.8;
          }}
          .dstijl-home-formula {{
            font-family: 'JetBrains Mono', ui-monospace, Menlo, Consolas, monospace;
            font-size: 0.92rem;
            font-weight: 700;
            margin: 0 0 0.5rem;
            letter-spacing: -0.01em;
            padding: 0.3rem 0.55rem;
            background: {paper};
            border: 1.5px solid {ink};
            display: inline-block;
          }}
          .dstijl-home-aside-body {{
            margin: 0;
            font-size: 0.86rem;
            line-height: 1.5;
            opacity: 0.9;
          }}
          .dstijl-home-steps {{
            list-style: none;
            margin: 0;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0;
            border: 2px solid {ink};
          }}
          @media (max-width: 900px) {{
            .dstijl-home-steps {{ grid-template-columns: 1fr 1fr; }}
          }}
          @media (max-width: 520px) {{
            .dstijl-home-steps {{ grid-template-columns: 1fr; }}
          }}
          .dstijl-home-step {{
            padding: 0.85rem 0.75rem;
            border-right: 2px solid {ink};
            border-bottom: 2px solid {ink};
            font-size: 0.82rem;
            line-height: 1.45;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            min-height: 5.5rem;
            background: {paper};
            transition: background 0.15s ease;
          }}
          .dstijl-home-step:hover {{
            background: var(--st-secondary-background-color);
          }}
          .dstijl-home-step:nth-child(4) {{ border-right: none; }}
          @media (max-width: 900px) {{
            .dstijl-home-step:nth-child(2) {{ border-right: none; }}
            .dstijl-home-step:nth-child(4) {{ border-right: none; }}
          }}
          @media (max-width: 520px) {{
            .dstijl-home-step {{ border-right: none !important; min-height: 0; }}
          }}
          .dstijl-home-step--red {{ border-top: 4px solid #E60012; }}
          .dstijl-home-step--blue {{ border-top: 4px solid #0047AB; }}
          .dstijl-home-step--yellow {{ border-top: 4px solid #FFDD00; }}
          .dstijl-home-step--ink {{ border-top: 4px solid {ink}; }}
          .dstijl-home-step-n {{
            font-size: 1.25rem;
            font-weight: 800;
            line-height: 1;
            opacity: 0.35;
          }}
          .dstijl-home-lenses {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
            border: 2px solid {ink};
          }}
          @media (max-width: 640px) {{
            .dstijl-home-lenses {{ grid-template-columns: 1fr; }}
          }}
          .dstijl-home-lens {{
            padding: 0.9rem 1rem;
            border-right: 2px solid {ink};
            font-size: 0.88rem;
            line-height: 1.5;
          }}
          .dstijl-home-lens:last-child {{ border-right: none; }}
          @media (max-width: 640px) {{
            .dstijl-home-lens {{ border-right: none; border-bottom: 2px solid {ink}; }}
            .dstijl-home-lens:last-child {{ border-bottom: none; }}
          }}
          .dstijl-home-lens p {{ margin: 0.35rem 0 0; opacity: 0.92; }}
          .dstijl-home-lens-tag {{
            font-size: 0.62rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #0047AB;
          }}
          .dstijl-home-note {{
            margin: 0.65rem 0 0;
            font-size: 0.84rem;
            line-height: 1.5;
            opacity: 0.78;
            max-width: 44rem;
          }}
          .dstijl-home-tour {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0;
            border: 2px solid {ink};
          }}
          @media (max-width: 820px) {{
            .dstijl-home-tour {{ grid-template-columns: 1fr 1fr; }}
          }}
          @media (max-width: 520px) {{
            .dstijl-home-tour {{ grid-template-columns: 1fr; }}
          }}
          .dstijl-home-tile {{
            padding: 0.85rem 0.9rem;
            border-right: 2px solid {ink};
            border-bottom: 2px solid {ink};
            background: {paper};
            transition: background 0.15s ease;
          }}
          .dstijl-home-tile:hover {{
            background: var(--st-secondary-background-color);
          }}
          .dstijl-home-tile:nth-child(3n) {{ border-right: none; }}
          .dstijl-home-tile:nth-last-child(-n+3) {{ border-bottom: none; }}
          @media (max-width: 820px) {{
            .dstijl-home-tile:nth-child(3n) {{ border-right: 2px solid {ink}; }}
            .dstijl-home-tile:nth-child(2n) {{ border-right: none; }}
            .dstijl-home-tile:nth-last-child(-n+3) {{ border-bottom: 2px solid {ink}; }}
            .dstijl-home-tile:nth-last-child(-n+2) {{ border-bottom: none; }}
          }}
          @media (max-width: 520px) {{
            .dstijl-home-tile {{ border-right: none !important; }}
            .dstijl-home-tile:not(:last-child) {{ border-bottom: 2px solid {ink} !important; }}
            .dstijl-home-tile:last-child {{ border-bottom: none !important; }}
          }}
          .dstijl-home-tile-tab {{
            display: inline-block;
            font-size: 0.65rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 0.15rem 0.35rem;
            border: 2px solid {ink};
            margin-bottom: 0.45rem;
            background: {paper};
          }}
          .dstijl-home-tile p {{
            margin: 0;
            font-size: 0.82rem;
            line-height: 1.45;
            opacity: 0.88;
          }}
          .dstijl-home-leagues {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            margin-top: 1.35rem;
            border: 2px solid {ink};
          }}
          @media (max-width: 720px) {{
            .dstijl-home-leagues {{ grid-template-columns: 1fr 1fr; }}
          }}
          .dstijl-home-league {{
            padding: 0.7rem 0.75rem;
            border-right: 2px solid {ink};
            font-size: 0.8rem;
            line-height: 1.4;
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
            background: {paper};
            transition: background 0.15s ease;
          }}
          .dstijl-home-league:hover {{
            background: var(--st-secondary-background-color);
          }}
          .dstijl-home-league:last-child {{ border-right: none; }}
          @media (max-width: 720px) {{
            .dstijl-home-league:nth-child(2) {{ border-right: none; }}
            .dstijl-home-league:nth-child(1),
            .dstijl-home-league:nth-child(2) {{ border-bottom: 2px solid {ink}; }}
          }}
          .dstijl-home-league strong {{
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
          }}
          .dstijl-home-league span {{ opacity: 0.75; font-size: 0.78rem; }}
          .dstijl-home-league--pwhl {{ border-top: 4px solid #0047AB; }}
          .dstijl-home-league--wnba {{ border-top: 4px solid #FFDD00; }}
          .dstijl-home-league--wpl {{ border-top: 4px solid #E60012; }}
          .dstijl-home-league--nwsl {{ border-top: 4px solid {ink}; opacity: 0.85; }}
          div[data-testid="stDeckGlJsonChart"],
          div[data-testid="stPlotlyChart"] {{
            border: 3px solid {ink};
            border-radius: 0;
            overflow: hidden;
          }}
          div[data-testid="stMetric"] {{ border-radius: 0; }}

          /* Native Streamlit Widget De Stijl Harmonization */
          div[data-testid="stButton"] button {{
            border: 2px solid {ink} !important;
            border-radius: 0 !important;
            box-shadow: 3px 3px 0px {ink} !important;
            font-family: Archivo, Helvetica, Arial, sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            background: {paper} !important;
            color: {ink} !important;
            padding: 0.55rem 1.25rem !important;
            transition: transform 0.08s ease, box-shadow 0.08s ease, background 0.12s ease !important;
          }}
          div[data-testid="stButton"] button:hover {{
            background: #FFDD00 !important;
            color: #0A0A0A !important;
            border-color: {ink} !important;
          }}
          div[data-testid="stButton"] button:active {{
            transform: translate(2px, 2px) !important;
            box-shadow: 1px 1px 0px {ink} !important;
          }}
          div[data-baseweb="select"] > div {{
            border-radius: 0 !important;
            border: 2px solid {ink} !important;
            background: {paper} !important;
            box-shadow: none !important;
          }}
          div[data-baseweb="input"] {{
            border-radius: 0 !important;
            border: 2px solid {ink} !important;
          }}
          div[data-baseweb="input"] input {{
            border-radius: 0 !important;
            font-family: Archivo, Helvetica, Arial, sans-serif !important;
          }}
          div[data-testid="stExpander"] {{
            border: 2px solid {ink} !important;
            border-radius: 0 !important;
            background: {paper} !important;
            margin-top: 0.75rem;
          }}
          div[data-testid="stExpander"] summary {{
            border-radius: 0 !important;
            font-family: Archivo, Helvetica, Arial, sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.75rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
          }}
          div[data-testid="stDataFrame"] {{
            border: 2px solid {ink} !important;
            border-radius: 0 !important;
          }}
          .dstijl-active-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.65rem;
            font-size: 0.72rem;
            font-family: Archivo, Helvetica, Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            background: var(--st-secondary-background-color);
            border: 1.5px solid {ink};
            border-left: 5px solid #E60012;
            margin: 0.35rem 0 0.2rem;
          }}
          .dstijl-active-pill span {{
            opacity: 0.7;
            font-weight: 600;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _sorted_pins(league: str, df: pd.DataFrame) -> list:
    keys = team_keys_in_frame(league, df)
    return sorted(pins_for_keys(league, keys), key=lambda p: p.city)


def _apply_map_selection(event, state_key: str, map_key: str) -> None:
    if not event or not event.selection.objects:
        return
    objs = event.selection.objects.get(MAP_LAYER_ID, [])
    if not objs:
        return
    team_key = str(objs[0].get("key", ""))
    if not team_key:
        return
    sig_key = f"{map_key}__sig"
    if team_key == st.session_state.get(sig_key):
        return
    st.session_state[sig_key] = team_key
    st.session_state[state_key] = team_key


def market_picker(
    league: str,
    df: pd.DataFrame,
    state_key: str,
    map_key: str,
    *,
    allow_all: bool = True,
) -> str:
    """Map click or dropdown; both write to session_state[state_key]."""
    league_key = f"{state_key}__league"
    if st.session_state.get(league_key) != league:
        st.session_state[state_key] = "All" if allow_all else _sorted_pins(league, df)[0].key
        st.session_state[league_key] = league
        st.session_state.pop(f"{map_key}__sig", None)

    pins = _sorted_pins(league, df)
    if not pins:
        return "All"

    options = (["All"] if allow_all else []) + [p.key for p in pins]
    labels = {k: lab for k, lab in zip(options, (["All markets"] if allow_all else []) + [p.label for p in pins])}
    st.session_state.setdefault(state_key, options[0])
    if st.session_state[state_key] not in options:
        st.session_state[state_key] = options[0]

    selected = st.session_state[state_key]
    highlight = None if selected == "All" else selected
    deck = team_map_deck(league, pins, highlight)
    event = st.pydeck_chart(
        deck,
        width="stretch",
        height=340,
        key=map_key,
        on_select="rerun",
        selection_mode="single-object",
    )
    _apply_map_selection(event, state_key, map_key)

    st.selectbox(
        "Market (city)",
        options,
        format_func=lambda k: labels[k],
        key=state_key,
        help="Click a dot on the map or pick from the list.",
    )
    if st.session_state[state_key] == "All":
        st.session_state.pop(f"{map_key}__sig", None)
    else:
        cur_label = labels.get(st.session_state[state_key], st.session_state[state_key])
        st.markdown(
            f'<div class="dstijl-active-pill"><span>Active market:</span> <strong>{cur_label}</strong></div>',
            unsafe_allow_html=True,
        )
    st.caption("Click a dot on the map (single click) to filter. Use the list to reset to all markets.")
    return st.session_state[state_key]


FAVICON_PATH = FAVICON if FAVICON.exists() else FAVICON_SMALL
st.set_page_config(
    page_title="Pay-by-Play",
    page_icon=str(FAVICON_PATH) if FAVICON_PATH.exists() else "🏒",
    layout="wide",
    initial_sidebar_state="collapsed",
)
if LOGO_ICON.exists():
    st.logo(str(LOGO_ICON), size="large")
inject_css()

if not (PROCESSED / "player_season_pwhl.parquet").exists():
    st.error("No processed data. Run fetch_data.py, then python -m src.pipeline.")
    st.stop()

pwhl = load_table("player_season_pwhl.parquet")
wnba = load_table("player_season_wnba.parquet") if (PROCESSED / "player_season_wnba.parquet").exists() else pd.DataFrame()
wpl = load_table("player_season_wpl.parquet") if (PROCESSED / "player_season_wpl.parquet").exists() else pd.DataFrame()
hyp = load_json(PROCESSED / "hypotheses.json")
robust_tbl = (
    pd.read_csv(PROCESSED / "value_definition_robustness.csv")
    if (PROCESSED / "value_definition_robustness.csv").exists()
    else pd.DataFrame()
)
pwhl_board = load_json(PROCESSED / "scoreboard_pwhl.json")
wnba_board = load_json(PROCESSED / "scoreboard_wnba.json")

leagues: dict[str, pd.DataFrame] = {"PWHL": pwhl}
if not wnba.empty:
    leagues["WNBA"] = wnba
if not wpl.empty:
    leagues["WPL"] = wpl

st.markdown(
    top_chrome_html(pwhl, wnba, wpl),
    unsafe_allow_html=True,
)

tab_home, tab_score, tab_explorer, tab_radar, tab_lens, tab_roster, tab_methods = st.tabs(
    ["Home", "Scoreboard", "Explorer", "Raise radar", "Two lenses", "Roster lab", "Methods"]
)

with tab_home:
    st.markdown(home_tab_html(), unsafe_allow_html=True)

with tab_score:
    pwhl_bargains = (
        int(pwhl["confident_bargain"].sum())
        if "confident_bargain" in pwhl.columns
        else pwhl_board.get("confident_bargains")
    )
    wnba_bargains = (
        int(wnba["confident_bargain"].sum())
        if not wnba.empty and "confident_bargain" in wnba.columns
        else wnba_board.get("confident_bargains")
    )
    wpl_fair = (hyp.get("wpl") or {}).get("spearman_fairness_2025_26")
    wpl_n = (hyp.get("wpl") or {}).get("matched_2025_26")
    cards = [
        ("PWHL", "Salary band", pwhl_board.get("within_league_fairness_spearman"), pwhl_bargains, len(pwhl)),
        ("WNBA", "Tiered cap", wnba_board.get("within_league_fairness_spearman"), wnba_bargains, len(wnba) if not wnba.empty else 0),
        ("WPL", "Auction", wpl_fair, None, wpl_n),
    ]
    tones = ("score-cell--blue", "score-cell--yellow", "score-cell--red")
    cells = []
    for i, (name, mech, fair, bargains, n) in enumerate(cards):
        fair_s = f"{fair:.2f}" if fair is not None else "—"
        if bargains is not None:
            meta = f"{int(bargains)} confident bargains · n = {n}"
        else:
            meta = f"Auction vs phase value · n = {n}"
        cells.append(
            f'<div class="score-cell {tones[i]}">'
            f'<div class="score-league">{name} · {mech}</div>'
            f'<div class="score-num">{fair_s}</div><div class="score-meta">{meta}</div></div>'
        )
    st.markdown(f'<div class="score-row">{"".join(cells)}</div>', unsafe_allow_html=True)

    h1 = hyp.get("h1_pwhl_draft") or {}
    h2 = hyp.get("h2_wnba_raise") or {}
    if h1:
        st.markdown(
            f'<div class="dstijl-callout"><strong>PWHL draft</strong> — Among {h1.get("n")} drafted players, '
            f"pay vs draft pick ρ = {h1.get('spearman_pay_vs_draft_pick', 0):.2f}; "
            f"pay vs value ρ = {h1.get('spearman_pay_vs_value', 0):.2f}.</div>",
            unsafe_allow_html=True,
        )
    if h2:
        st.markdown(
            f'<div class="dstijl-callout"><strong>WNBA raises</strong> — Mean raise '
            f"${h2.get('mean_raise_usd', 0):,.0f} (n = {h2.get('n')}). "
            f"Prior-season value explains {100 * h2.get('r_squared_raise_on_prior_value', 0):.0f}% of raise variation.</div>",
            unsafe_allow_html=True,
        )
    if not robust_tbl.empty:
        st.markdown("#### Value definition check")
        show = robust_tbl.copy()
        show["spearman_fairness"] = show["spearman_fairness"].map(lambda x: f"{x:.2f}")
        show["misallocation_index"] = show["misallocation_index"].map(lambda x: f"{x:.0%}")
        st.dataframe(show, hide_index=True, width="stretch")

with tab_explorer:
    league = st.selectbox("League", list(leagues), key="explorer_league")
    df = leagues[league]
    market = market_picker(league, df, "explorer_market", "explorer_map")
    subset = filter_by_team_key(league, df, market)
    pins = _sorted_pins(league, df)
    if market == "All":
        st.markdown(f"**All markets** · {len(subset)} players")
    else:
        pin = next((p for p in pins if p.key == market), None)
        st.markdown(f"**{pin.label if pin else market}** · {len(subset)} players")
    st.plotly_chart(pay_value_scatter(subset), width="stretch", theme="streamlit")
    st.caption(
        "Shaded corners mark bargain (upper left) and overpaid (lower right) zones. "
        "Larger dots = confident bargain (80% CI above zero). Percentiles are within position."
    )

with tab_radar:
    league = st.selectbox("League", list(leagues), key="radar_league")
    df = leagues[league]
    market = market_picker(league, df, "radar_market", "radar_map")
    subset = filter_by_team_key(league, df, market)
    if "confident_bargain" in subset.columns:
        bargains = subset[subset["confident_bargain"]]
    else:
        bargains = subset.head(0)
    has_bargain_flag = "confident_bargain" in subset.columns and subset["confident_bargain"].any()
    has_ci = "ci_low" in subset.columns and subset["ci_low"].notna().any()
    if has_bargain_flag:
        st.markdown(
            f"**{len(bargains)}** players with gap 80% CI entirely above zero (of **{len(subset)}** in view)."
        )
    else:
        st.markdown(
            f"**Top raise cases** in view (of **{len(subset)}** players). "
            "Bootstrap CIs are not computed for this league yet."
        )
    view = bargains if not bargains.empty else subset.sort_values("gap", ascending=False)
    if view.empty:
        st.info("No players in this market.")
    else:
        st.plotly_chart(raise_radar_chart(view), width="stretch", theme="streamlit")
        st.caption(
            "Blue dot = pay percentile, red dot = value percentile, yellow connector = gap. "
            "One row per player (highest gap kept if duplicates)."
        )
        detail = dedupe_players(view)
        cols = [c for c in ["name", "team", "position", "pay_pct", "value_pct", "gap", "ci_low", "ci_high"] if c in detail.columns]
        show = detail[cols].head(18).copy()
        for c in ("pay_pct", "value_pct", "gap", "ci_low", "ci_high"):
            if c in show.columns:
                show[c] = show[c].map(lambda x: f"{x:.1f}")
        with st.expander("Table view"):
            st.dataframe(show, hide_index=True, width="stretch")

with tab_lens:
    choice = st.selectbox(
        "League",
        [k for k in ("PWHL", "WNBA") if (PROCESSED / f"{k.lower()}_two_lens.parquet").exists()],
    )
    tl = pd.read_parquet(PROCESSED / f"{choice.lower()}_two_lens.parquet")
    if "lens_delta" in tl.columns:
        st.plotly_chart(lens_delta_histogram(tl), width="stretch", theme="streamlit")
        cols = [c for c in ["name", "gap_lens_a", "gap_lens_b", "lens_delta", "pay_pct"] if c in tl.columns]
        st.dataframe(tl.sort_values("lens_delta", ascending=False)[cols].head(25), hide_index=True, width="stretch")

with tab_roster:
    st.markdown("#### PWHL roster under the salary band")
    st.caption("Base salary only. Forwards = C/LW/RW; defense = LD/RD.")
    pool = pwhl[pwhl["regular_flag"]].copy()
    teams = sorted(pool["team"].unique())
    left, right = st.columns([1, 2])
    with left:
        def _pwhl_label(t: str) -> str:
            pin = pins_for_keys("PWHL", [t])
            return pin[0].label if pin else t

        st.session_state.setdefault("roster_team", teams[0])
        if st.session_state.get("roster_team") not in teams:
            st.session_state["roster_team"] = teams[0]
        roster_pins = _sorted_pins("PWHL", pool)
        roster_deck = team_map_deck("PWHL", roster_pins, st.session_state["roster_team"])
        roster_event = st.pydeck_chart(
            roster_deck,
            width="stretch",
            height=320,
            key="roster_map",
            on_select="rerun",
            selection_mode="single-object",
        )
        _apply_map_selection(roster_event, "roster_team", "roster_map")
        team = st.selectbox("Market (city)", teams, format_func=_pwhl_label, key="roster_team")
        st.caption("Click a city on the map to switch teams.")
        sub = pool[pool["team"] == team]
        roster_cap = int(len(sub))
        n = st.number_input("Roster size", min(12, roster_cap), roster_cap, min(20, roster_cap))
        go = st.button("Solve roster")
    with right:
        if go:
            res = optimize_roster(sub, roster_size=int(n))
            if res.status == "Optimal":
                st.write(f"**Average salary** ${res.avg_salary:,.0f} · payroll ${res.total_pay:,.0f}")
                st.caption(res.message)
                picked = sub[sub["player_id"].astype(int).isin(res.selected_ids)]
                st.dataframe(
                    picked[["name", "position", "pay_raw", "value_shrunk", "gap"]],
                    hide_index=True,
                    width="stretch",
                )
                for line in suggest_swaps(sub.head(int(n)), sub, res):
                    st.markdown(f"- {line}")
            else:
                st.warning(f"{res.status}. {res.message}")
        else:
            st.caption("Pick a market and solve. Result targets ±10% of the $60,100 team average.")

with tab_methods:
    st.markdown((PROJECT_ROOT / "definitions.md").read_text(encoding="utf-8"))
    st.markdown("#### NWSL")
    st.markdown(
        "The NWSL is not scored. Public salaries cover only a handful of players, so a league-wide "
        "correlation would not be meaningful. PWHL published base salaries are the transparency contrast."
    )
    st.caption(
        "Pay: PWHLPA guide, Her Hoop Stats cap hits, Cricbuzz WPL auction. "
        "Performance: HockeyTech, ESPN, Cricsheet."
    )
