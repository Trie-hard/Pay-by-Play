"""Franchise home cities for map pins (approximate arena / market centers)."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import pydeck as pdk

from app.theme import map_palette

MAP_LAYER_ID = "franchise-markets"
MAP_GLOW_LAYER_ID = "franchise-markets-glow"
MAP_LABEL_LAYER_ID = "franchise-markets-labels"

# key matches the `team` column (PWHL, WNBA) or `team_id` (WPL)


@dataclass(frozen=True)
class TeamPin:
    key: str
    city: str
    franchise: str
    lat: float
    lon: float

    @property
    def label(self) -> str:
        return f"{self.city} · {self.franchise}"


PWHL_PINS: dict[str, TeamPin] = {
    "Boston": TeamPin("Boston", "Boston", "Fleet", 42.3601, -71.0589),
    "Minnesota": TeamPin("Minnesota", "Saint Paul", "Frost", 44.9537, -93.0900),
    "Montreal": TeamPin("Montreal", "Montréal", "Victoire", 45.5017, -73.5673),
    "New York": TeamPin("New York", "Newark", "Sirens", 40.7357, -74.1724),
    "Ottawa": TeamPin("Ottawa", "Ottawa", "Charge", 45.4215, -75.6972),
    "Seattle": TeamPin("Seattle", "Seattle", "Torrent", 47.6062, -122.3321),
    "Toronto": TeamPin("Toronto", "Toronto", "Sceptres", 43.6532, -79.3832),
    "Vancouver": TeamPin("Vancouver", "Vancouver", "Goldeneyes", 49.2827, -123.1207),
}

WNBA_PINS: dict[str, TeamPin] = {
    "ATL": TeamPin("ATL", "Atlanta", "Dream", 33.7573, -84.3963),
    "CHI": TeamPin("CHI", "Chicago", "Sky", 41.8781, -87.6298),
    "CON": TeamPin("CON", "Hartford", "Sun", 41.7658, -72.6734),
    "DAL": TeamPin("DAL", "Dallas", "Wings", 32.7767, -96.7970),
    "GS": TeamPin("GS", "San Francisco", "Valkyries", 37.7749, -122.4194),
    "IND": TeamPin("IND", "Indianapolis", "Fever", 39.7684, -86.1581),
    "LA": TeamPin("LA", "Los Angeles", "Sparks", 34.0522, -118.2437),
    "LV": TeamPin("LV", "Las Vegas", "Aces", 36.1699, -115.1398),
    "MIN": TeamPin("MIN", "Minneapolis", "Lynx", 44.9778, -93.2650),
    "NY": TeamPin("NY", "Brooklyn", "Liberty", 40.6782, -73.9442),
    "PHX": TeamPin("PHX", "Phoenix", "Mercury", 33.4484, -112.0740),
    "POR": TeamPin("POR", "Portland", "Fire", 45.5152, -122.6784),
    "SEA": TeamPin("SEA", "Seattle", "Storm", 47.6062, -122.3321),
    "TOR": TeamPin("TOR", "Toronto", "Tempo", 43.6532, -79.3832),
    "WSH": TeamPin("WSH", "Washington", "Mystics", 38.9072, -77.0369),
}

WPL_PINS: dict[str, TeamPin] = {
    "1461": TeamPin("1461", "Delhi", "Capitals", 28.6139, 77.2090),
    "1465": TeamPin("1465", "Ahmedabad", "Gujarat Giants", 23.0225, 72.5714),
    "1468": TeamPin("1468", "Mumbai", "Indians", 19.0760, 72.8777),
    "1472": TeamPin("1472", "Bengaluru", "Royal Challengers", 12.9716, 77.5946),
    "1479": TeamPin("1479", "Lucknow", "Warriorz", 26.8467, 80.9462),
}

LEAGUE_PIN_TABLE = {"PWHL": PWHL_PINS, "WNBA": WNBA_PINS, "WPL": WPL_PINS}


def team_keys_in_frame(league: str, df) -> list[str]:
    if league == "WPL" and "team_id" in df.columns:
        keys = df["team_id"].astype(str).dropna().unique().tolist()
    elif "team" in df.columns:
        keys = [k for k in df["team"].dropna().unique().tolist() if isinstance(k, str)]
    else:
        keys = []
    table = LEAGUE_PIN_TABLE.get(league, {})
    return [k for k in keys if k in table]


def pins_for_keys(league: str, keys: list[str]) -> list[TeamPin]:
    table = LEAGUE_PIN_TABLE.get(league, {})
    return [table[k] for k in keys if k in table]


def filter_by_team_key(league: str, df, team_key: str):
    if team_key == "All":
        return df
    if league == "WPL" and "team_id" in df.columns:
        return df[df["team_id"].astype(str) == team_key]
    if "team" in df.columns:
        return df[df["team"] == team_key]
    return df


def team_map_deck(league: str, pins: list[TeamPin], selected_key: str | None) -> pdk.Deck:
    """Clickable franchise map (PyDeck + Streamlit on_select)."""
    palette = map_palette()
    if league == "WPL":
        view = pdk.ViewState(latitude=22.0, longitude=79.0, zoom=4.35, pitch=0, bearing=0)
    else:
        view = pdk.ViewState(latitude=46.0, longitude=-98.0, zoom=3.45, pitch=0, bearing=0)

    if not pins:
        return pdk.Deck(layers=[], initial_view_state=view, map_style=palette["basemap"])

    rows = []
    for p in pins:
        selected = p.key == selected_key
        rows.append(
            {
                "lat": p.lat,
                "lon": p.lon,
                "label": p.label,
                "short": p.city,
                "key": p.key,
                "fill": palette["selected"] if selected else palette["pin"],
                "dim": palette["pin_dim"] if not selected else palette["selected"],
                "ring": palette["selected_ring"] if selected else palette["pin_ring"],
                "radius": 72000 if selected else 48000,
                "glow": 110000 if selected else 70000,
                "label_size": 15 if selected else 12,
            }
        )
    df = pd.DataFrame(rows)

    glow = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        id=MAP_GLOW_LAYER_ID,
        get_position=["lon", "lat"],
        get_fill_color="dim",
        get_radius="glow",
        pickable=False,
        stroked=False,
        opacity=0.35,
    )
    markers = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        id=MAP_LAYER_ID,
        get_position=["lon", "lat"],
        get_fill_color="fill",
        get_line_color="ring",
        get_radius="radius",
        line_width_min_pixels=2,
        stroked=True,
        pickable=True,
        auto_highlight=True,
        highlight_color=palette["highlight"],
    )
    labels = pdk.Layer(
        "TextLayer",
        data=df,
        id=MAP_LABEL_LAYER_ID,
        get_position=["lon", "lat"],
        get_text="short",
        get_size="label_size",
        get_color=palette["label"],
        get_text_anchor="'middle'",
        get_alignment_baseline="'bottom'",
        get_pixel_offset=[0, -14],
        pickable=False,
    )

    return pdk.Deck(
        layers=[glow, markers, labels],
        initial_view_state=view,
        map_style=palette["basemap"],
        tooltip={"text": "{label}"},
    )
