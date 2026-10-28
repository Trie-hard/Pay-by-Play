"""Theme helpers for charts and maps (Streamlit light / dark + De Stijl accents)."""

from __future__ import annotations

import streamlit as st

from app.brand import DS_BLACK, DS_BLUE, DS_GRAY, DS_RED, DS_YELLOW, FONT_DISPLAY

CARTO_LIGHT = "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json"
CARTO_DARK = "https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json"


def is_dark_theme() -> bool:
    theme_type = getattr(st.context.theme, "type", None)
    return theme_type == "dark"


def chart_qualitative() -> list[str]:
    if is_dark_theme():
        return ["#FF3333", "#6B9FFF", "#FFDD00", "#F5F5F5", "#9E9E9E", "#4FC3F7", "#CE93D8", "#A1887F"]
    return [DS_RED, DS_BLUE, DS_YELLOW, DS_BLACK, DS_GRAY, "#1565C0", "#6A1B9A", "#5D4037"]


def plotly_layout_overrides() -> dict:
    dark = is_dark_theme()
    grid = "rgba(245,245,245,0.15)" if dark else "rgba(10,10,10,0.12)"
    line = DS_BLACK if not dark else "#F5F5F5"
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_DISPLAY, size=13, color=line if not dark else "#F5F5F5"),
        "margin": dict(l=44, r=16, t=36, b=44),
        "xaxis": dict(
            gridcolor=grid,
            zerolinecolor=line,
            linecolor=line,
            linewidth=2,
            mirror=True,
        ),
        "yaxis": dict(
            gridcolor=grid,
            zerolinecolor=line,
            linecolor=line,
            linewidth=2,
            mirror=True,
        ),
    }


def ref_line_color() -> str:
    return "rgba(245,245,245,0.5)" if is_dark_theme() else DS_BLACK


def map_palette() -> dict:
    dark = is_dark_theme()
    if dark:
        return {
            "basemap": CARTO_DARK,
            "pin": [107, 159, 255, 220],
            "pin_dim": [158, 158, 158, 160],
            "pin_ring": [245, 245, 245, 200],
            "selected": [255, 51, 51, 240],
            "selected_ring": [255, 221, 0, 255],
            "highlight": [255, 221, 0, 200],
            "label": [245, 245, 245, 255],
        }
    return {
        "basemap": CARTO_LIGHT,
        "pin": [0, 71, 171, 230],
        "pin_dim": [128, 128, 128, 180],
        "pin_ring": [10, 10, 10, 255],
        "selected": [230, 0, 18, 240],
        "selected_ring": [255, 221, 0, 255],
        "highlight": [255, 221, 0, 220],
        "label": [10, 10, 10, 255],
    }
