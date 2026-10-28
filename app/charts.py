"""Plotly figure builders for the Streamlit app."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.theme import DS_BLUE, DS_RED, DS_YELLOW, chart_qualitative, is_dark_theme, plotly_layout_overrides, ref_line_color

CHART_HEIGHT = 460


def _palette() -> list[str]:
    return chart_qualitative()


def _marker_line_color() -> str:
    return "rgba(26,35,50,0.35)" if not is_dark_theme() else "rgba(255,255,255,0.45)"


def style_fig(fig: go.Figure, *, height: int = CHART_HEIGHT) -> go.Figure:
    overrides = plotly_layout_overrides()
    dark = is_dark_theme()
    fig.update_layout(
        paper_bgcolor=overrides["paper_bgcolor"],
        plot_bgcolor=overrides["plot_bgcolor"],
        font=overrides["font"],
        margin=dict(l=52, r=24, t=48, b=52),
        height=height,
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#0A0A0A" if not dark else "#161616",
            bordercolor="#0A0A0A" if not dark else "#F5F5F5",
            font=dict(size=12, color="#FFFFFF" if not dark else "#F5F5F5", family="Archivo, Helvetica, Arial, sans-serif"),
        ),
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        title=dict(font=dict(size=15), x=0, xanchor="left"),
    )
    fig.update_xaxes(
        **overrides["xaxis"],
        title_font=dict(size=13),
        tickfont=dict(size=11),
        showgrid=True,
        zeroline=False,
    )
    fig.update_yaxes(
        **overrides["yaxis"],
        title_font=dict(size=13),
        tickfont=dict(size=11),
        showgrid=True,
        zeroline=False,
    )
    return fig


def _add_quadrant_tints(fig: go.Figure) -> None:
    """Subtle upper-left (bargain) and lower-right (overpaid) washes."""
    bargain = "rgba(0,71,171,0.12)" if not is_dark_theme() else "rgba(107,159,255,0.15)"
    over = "rgba(230,0,18,0.10)" if not is_dark_theme() else "rgba(255,51,51,0.12)"
    fig.add_shape(type="rect", x0=0, x1=50, y0=50, y1=100, fillcolor=bargain, line_width=0, layer="below")
    fig.add_shape(type="rect", x0=50, x1=100, y0=0, y1=50, fillcolor=over, line_width=0, layer="below")


def pay_value_scatter(df, title: str | None = None) -> go.Figure:
    plot_df = df.dropna(subset=["pay_pct", "value_pct"]).copy()
    if plot_df.empty:
        fig = go.Figure()
        fig.update_layout(title=title or "Pay vs value")
        return style_fig(fig)

    if "confident_bargain" in plot_df.columns:
        plot_df["_marker_size"] = plot_df["confident_bargain"].map(lambda b: 14 if b else 10)
    else:
        plot_df["_marker_size"] = 10

    scatter_kwargs = dict(
        x="pay_pct",
        y="value_pct",
        size="_marker_size",
        size_max=16,
        hover_name="name" if "name" in plot_df.columns else None,
        color_discrete_sequence=_palette(),
        labels={"pay_pct": "Pay percentile", "value_pct": "Value percentile", "position": "Position"},
        title=title,
    )
    if "position" in plot_df.columns:
        scatter_kwargs["color"] = "position"
    if "gap" in plot_df.columns:
        scatter_kwargs["custom_data"] = ["gap"]

    fig = px.scatter(plot_df, **scatter_kwargs)

    if "gap" in plot_df.columns:
        fig.update_traces(
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Pay %{x:.0f} · Value %{y:.0f}<br>"
                "Gap %{customdata[0]:+.0f}"
                "<extra></extra>"
            )
        )
    else:
        fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Pay %{x:.0f} · Value %{y:.0f}<extra></extra>")

    ref = ref_line_color()
    _add_quadrant_tints(fig)
    fig.add_hline(y=50, line_dash="dot", line_width=1, line_color=ref)
    fig.add_vline(x=50, line_dash="dot", line_width=1, line_color=ref)

    # 45-degree Fair-Pay Equator (y = x)
    fig.add_shape(
        type="line",
        x0=0, y0=0, x1=100, y1=100,
        line=dict(color=ref, width=1.5, dash="dash"),
        layer="below",
    )
    fig.add_annotation(
        x=82, y=87,
        text="Pay = Value (1:1)",
        showarrow=False,
        font=dict(size=10, color=ref, family="Archivo, Helvetica, Arial, sans-serif"),
        textangle=45,
        opacity=0.7,
    )

    accent_blue = DS_BLUE if not is_dark_theme() else "#6B9FFF"
    accent_red = DS_RED if not is_dark_theme() else "#FF3333"
    fig.add_annotation(
        x=8, y=94,
        text="▲ Paid below value (Surplus)",
        showarrow=False,
        font=dict(size=10, color=accent_blue, family="Archivo, Helvetica, Arial, sans-serif"),
        bgcolor="rgba(0,71,171,0.08)" if not is_dark_theme() else "rgba(107,159,255,0.12)",
        bordercolor=accent_blue,
        borderwidth=1,
        borderpad=4,
        opacity=0.95,
    )
    fig.add_annotation(
        x=92, y=6,
        text="▼ Paid above value (Deficit)",
        showarrow=False,
        font=dict(size=10, color=accent_red, family="Archivo, Helvetica, Arial, sans-serif"),
        bgcolor="rgba(230,0,18,0.06)" if not is_dark_theme() else "rgba(255,51,51,0.1)",
        bordercolor=accent_red,
        borderwidth=1,
        borderpad=4,
        opacity=0.95,
        xanchor="right",
    )

    fig.update_traces(marker=dict(opacity=0.88, line=dict(width=1.1, color=_marker_line_color())))

    fig.update_xaxes(range=[-2, 102], dtick=20)
    fig.update_yaxes(range=[-2, 102], dtick=20)
    return style_fig(fig)


def lens_delta_histogram(tl) -> go.Figure:
    series = tl["lens_delta"].dropna()
    primary = DS_RED if not is_dark_theme() else "#FF3333"
    fig = px.histogram(
        tl,
        x="lens_delta",
        nbins=28,
        color_discrete_sequence=[primary],
        labels={"lens_delta": "Lens B − lens A (gap points)", "count": "Players"},
        title="Two-lens gap shift",
    )
    fig.update_traces(
        marker=dict(line=dict(width=0.6, color=_marker_line_color()), opacity=0.9),
    )
    fig.add_vline(x=0, line_width=1.5, line_dash="solid", line_color=ref_line_color())
    if len(series) > 0:
        mean = float(series.mean())
        fig.add_vline(
            x=mean,
            line_width=1.5,
            line_dash="dash",
            line_color=DS_YELLOW if not is_dark_theme() else "#FFDD00",
            annotation_text=f"mean {mean:+.0f}",
            annotation_position="top",
            annotation_font_size=11,
        )
    fig.update_layout(bargap=0.08, xaxis_title="Lens B − lens A (gap points)")
    return style_fig(fig, height=400)


def dedupe_players(df: pd.DataFrame) -> pd.DataFrame:
    ordered = df.sort_values("gap", ascending=False)
    if "player_id" in ordered.columns:
        return ordered.drop_duplicates(subset=["player_id"], keep="first")
    if "athlete_id" in ordered.columns:
        return ordered.drop_duplicates(subset=["athlete_id"], keep="first")
    keys = ["name"]
    if "team" in ordered.columns:
        keys.append("team")
    elif "team_id" in ordered.columns:
        keys.append("team_id")
    return ordered.drop_duplicates(subset=keys, keep="first")


def raise_radar_chart(df: pd.DataFrame, *, max_players: int = 18) -> go.Figure:
    """Dumbbell chart: pay percentile → value percentile per player."""
    plot = dedupe_players(df.dropna(subset=["pay_pct", "value_pct", "gap"]))
    if plot.empty:
        fig = go.Figure()
        fig.update_layout(title="No players to show")
        return style_fig(fig, height=220)

    plot = plot.head(max_players).copy()
    for col in ("ci_low", "ci_high"):
        if col not in plot.columns:
            plot[col] = float("nan")
    has_ci = plot["ci_low"].notna().any() and plot["ci_high"].notna().any()

    def _row_label(r) -> str:
        name = str(r["name"])
        pos = str(r.get("position", "") or "")
        if len(name) > 22:
            name = name[:21] + "…"
        return f"{name} · {pos}" if pos else name

    plot["_label"] = plot.apply(_row_label, axis=1)
    plot = plot.sort_values("gap", ascending=True)

    dark = is_dark_theme()
    pay_color = DS_BLUE if not dark else "#6B9FFF"
    val_color = DS_RED if not dark else "#FF3333"
    link_color = "rgba(255,221,0,0.92)" if not dark else "rgba(255,221,0,0.85)"

    fig = go.Figure()
    for _, row in plot.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["pay_pct"], row["value_pct"]],
                y=[row["_label"], row["_label"]],
                mode="lines",
                line=dict(color=link_color, width=5),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    if has_ci:
        custom = plot[["gap", "value_pct", "ci_low", "ci_high"]].to_numpy()
        pay_hover = (
            "<b>%{y}</b><br>Pay %{x:.0f}th percentile<br>"
            "Gap +%{customdata[0]:.1f} (80% CI %{customdata[2]:.1f}–%{customdata[3]:.1f})"
            "<extra></extra>"
        )
    else:
        custom = plot[["gap", "value_pct"]].to_numpy()
        pay_hover = (
            "<b>%{y}</b><br>Pay %{x:.0f}th percentile<br>Gap +%{customdata[0]:.1f}<extra></extra>"
        )
    fig.add_trace(
        go.Scatter(
            x=plot["pay_pct"],
            y=plot["_label"],
            mode="markers",
            name="Pay rank",
            marker=dict(size=12, color=pay_color, line=dict(width=1.5, color=_marker_line_color())),
            customdata=custom,
            hovertemplate=pay_hover,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=plot["value_pct"],
            y=plot["_label"],
            mode="markers",
            name="Value rank",
            marker=dict(size=12, color=val_color, symbol="square", line=dict(width=1.5, color=_marker_line_color())),
            customdata=custom,
            hovertemplate=(
                "<b>%{y}</b><br>Value %{x:.0f}th percentile<br>"
                "Gap +%{customdata[0]:.1f}"
                "<extra></extra>"
            ),
        )
    )

    ref = ref_line_color()
    fig.add_vline(x=50, line_width=1, line_dash="dot", line_color=ref)
    row_h = 38
    height = min(720, max(300, row_h * len(plot) + 120))
    fig = style_fig(fig, height=height)
    fig.update_layout(
        title=dict(text="Pay rank → value rank", x=0, xanchor="left", y=0.98, yanchor="top"),
        xaxis_title="Percentile within position",
        yaxis_title="",
        margin=dict(l=4, r=20, t=44, b=72),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            x=0.5,
            xanchor="center",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(range=[-2, 102], dtick=20, title_standoff=10)
    fig.update_yaxes(automargin=True, tickfont=dict(size=11))
    return fig
