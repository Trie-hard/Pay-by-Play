from __future__ import annotations

import re
import unicodedata

import pandas as pd

PWHL_TEAM_TO_CODE = {
    "boston": "BOS",
    "minnesota": "MIN",
    "montreal": "MTL",
    "montréal": "MTL",
    "new york": "NY",
    "ottawa": "OTT",
    "seattle": "SEA",
    "toronto": "TOR",
    "vancouver": "VAN",
}


def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    n = unicodedata.normalize("NFKD", name)
    n = "".join(c for c in n if not unicodedata.combining(c))
    n = re.sub(r"[^a-zA-Z' \-]", "", n)
    return re.sub(r"\s+", " ", n).strip().lower()


def pwhl_team_code(team: str) -> str:
    return PWHL_TEAM_TO_CODE.get(str(team).strip().lower(), str(team).upper()[:3])


def attach_player_ids(
    salaries: pd.DataFrame,
    stats: pd.DataFrame,
) -> pd.DataFrame:
    """Match PWHLPA names to HockeyTech player_id via name + team."""
    st = stats.copy()
    st["name_key"] = st.apply(
        lambda r: normalize_name(f"{r.get('first_name', '')} {r.get('last_name', '')}"),
        axis=1,
    )
    if "name" in st.columns:
        st["name_key_alt"] = st["name"].map(normalize_name)
    st["team_code"] = st.get("team_code", st.get("team_name", "")).astype(str).str.upper()

    sal = salaries.copy()
    sal["name_key"] = sal["name"].map(normalize_name)
    sal["team_code"] = sal["team"].map(pwhl_team_code)

    lookup = st.drop_duplicates(subset=["name_key", "team_code"])[["name_key", "team_code", "player_id"]]
    merged = sal.merge(lookup, on=["name_key", "team_code"], how="left")

    if "name_key_alt" in st.columns:
        missing = merged["player_id"].isna()
        alt_lookup = st.drop_duplicates(subset=["name_key_alt"])[["name_key_alt", "player_id"]]
        alt = merged.loc[missing, ["name_key"]].merge(
            alt_lookup,
            left_on="name_key",
            right_on="name_key_alt",
            how="left",
        )
        merged.loc[missing, "player_id"] = alt["player_id"].values

    missing = merged["player_id"].isna()
    if missing.any():
        name_only = st.drop_duplicates(subset=["name_key"])[["name_key", "player_id"]]
        name_only = name_only[name_only["name_key"].duplicated(keep=False) == False]  # noqa: E712
        uniq = name_only.set_index("name_key")["player_id"]
        for idx in merged.index[missing]:
            nk = merged.at[idx, "name_key"]
            if nk in uniq.index:
                merged.at[idx, "player_id"] = uniq[nk]

    merged["data_flags"] = merged["player_id"].isna().map(lambda x: "unmatched_player_id" if x else "")
    return merged
