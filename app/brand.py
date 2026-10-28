"""Pay-by-Play brand tokens (Brand System v1.2 — De Stijl Modernism)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# De Stijl primaries (light)
DS_RED = "#E60012"
DS_BLUE = "#0047AB"
DS_YELLOW = "#FFDD00"
DS_BLACK = "#0A0A0A"
DS_PAPER = "#FAFAF9"
DS_GRAY = "#71717A"
DS_WHITE = "#FFFFFF"

# Dark-mode calibrated tints
DARK_BG = "#121212"
DARK_SURFACE = "#1E1E22"
DARK_RED = "#FF3333"
DARK_BLUE = "#4D88FF"
DARK_YELLOW = "#FFDD00"
DARK_INK = "#F5F5F5"
DARK_GRAY = "#A1A1AA"

FONT_DISPLAY = "Archivo, Helvetica, Arial, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Courier New', monospace"

LOGO_MARK = ASSETS / "logo-mark.svg"
LOGO_ICON = ASSETS / "logo-icon.svg"
LOGO_ICON_DARK = ASSETS / "logo-icon-dark.svg"
LOGO_WORDMARK = ASSETS / "logo-wordmark.svg"
LOGO_MARK_PNG = ASSETS / "logo-mark-512.png"
LOGO_ICON_PNG = ASSETS / "logo-icon-128.png"
FAVICON = ASSETS / "favicon-64.png"
FAVICON_SMALL = ASSETS / "favicon-32.png"

BRAND_TAGLINE = "Does pay follow play, and does the pay structure change the answer?"
GAP_FORMULA = "gap = value_pct − pay_pct"


def colors(*, dark: bool) -> dict[str, str]:
    if dark:
        return {
            "ink": DARK_INK,
            "paper": DARK_BG,
            "rail": DARK_SURFACE,
            "red": DARK_RED,
            "blue": DARK_BLUE,
            "yellow": DARK_YELLOW,
            "gray": DARK_GRAY,
        }
    return {
        "ink": DS_BLACK,
        "paper": DS_PAPER,
        "rail": "#F0F0EE",
        "red": DS_RED,
        "blue": DS_BLUE,
        "yellow": DS_YELLOW,
        "gray": DS_GRAY,
    }
