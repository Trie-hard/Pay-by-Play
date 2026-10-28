"""Build shareable brand identity document (HTML, PDF, Markdown)."""

from __future__ import annotations

import base64
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_all_logos import (
    create_svg_icon,
    create_svg_icon_dark,
    create_svg_logo_mark,
    create_svg_wordmark,
    create_svg_emblem_lenses,
    DS_RED,
    DS_BLUE,
    DS_YELLOW,
    DS_BLACK,
    DS_PAPER,
    DS_GRAY,
    DS_WHITE,
)

DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"
CONCEPTS = ASSETS / "concepts"


def get_base64_image(path: Path) -> str:
    """Encode an image as base64 data URI."""
    if not path.exists():
        return ""
    suffix = path.suffix.lower().lstrip(".")
    mime = "image/jpeg" if suffix in ["jpg", "jpeg"] else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_html_document() -> str:
    svg_icon = create_svg_icon()
    svg_icon_dark = create_svg_icon_dark()
    svg_mark = create_svg_logo_mark()
    svg_wordmark = create_svg_wordmark()
    svg_emblem = create_svg_emblem_lenses()

    img_ai_1 = get_base64_image(CONCEPTS / "pay_by_play_logo_1793193390141.jpg")
    img_ai_2 = get_base64_image(CONCEPTS / "pay_by_play_logo_v2_1793193409499.jpg")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pay-by-Play — Brand Identity &amp; Logo System</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=JetBrains+Mono:wght@500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --ds-red: {DS_RED};
      --ds-blue: {DS_BLUE};
      --ds-yellow: {DS_YELLOW};
      --ds-black: {DS_BLACK};
      --ds-paper: {DS_PAPER};
      --ds-gray: {DS_GRAY};
      --ds-white: {DS_WHITE};
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: #0F1117;
      color: #F1F5F9;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      padding: 2rem 1rem;
    }}

    .doc-container {{
      max-width: 1040px;
      margin: 0 auto;
      background: #18181B;
      border: 1px solid #27272A;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }}

    /* Action Bar (hidden in print) */
    .action-bar {{
      background: #121214;
      border-bottom: 1px solid #27272A;
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .action-btn {{
      background: #E60012;
      color: white;
      border: none;
      border-radius: 8px;
      padding: 0.6rem 1.2rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }}
    .action-btn:hover {{
      background: #FF3333;
      transform: translateY(-1px);
    }}

    .secondary-btn {{
      background: #27272A;
      color: #E4E4E7;
      border: 1px solid #3F3F46;
    }}
    .secondary-btn:hover {{
      background: #3F3F46;
      color: white;
    }}

    /* Cover / Hero */
    .cover-header {{
      background: #FAFAF9;
      color: #0A0A0A;
      padding: 4rem 3rem 3.5rem;
      position: relative;
      border-bottom: 8px solid #0A0A0A;
    }}

    .de-stijl-stripe {{
      display: flex;
      height: 8px;
      width: 100%;
      position: absolute;
      top: 0;
      left: 0;
    }}
    .stripe-blue {{ flex: 2; background: #0047AB; }}
    .stripe-yellow {{ flex: 1; background: #FFDD00; }}
    .stripe-red {{ flex: 3; background: #E60012; }}

    .badge-pills {{
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
    }}

    .pill {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.3rem 0.75rem;
      border-radius: 4px;
      letter-spacing: 0.05em;
    }}
    .pill-black {{ background: #0A0A0A; color: #FAFAF9; }}
    .pill-red {{ background: #E60012; color: #FFFFFF; }}
    .pill-blue {{ background: #0047AB; color: #FFFFFF; }}
    .pill-yellow {{ background: #FFDD00; color: #0A0A0A; }}

    .hero-title {{
      font-family: 'Archivo', sans-serif;
      font-size: 3.4rem;
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -0.03em;
      margin-bottom: 1rem;
    }}
    .hero-title span.pay {{ color: #0A0A0A; }}
    .hero-title span.by {{ color: #71717A; font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 700; }}
    .hero-title span.play {{ color: #E60012; }}

    .hero-tagline {{
      font-size: 1.35rem;
      font-weight: 700;
      color: #18181B;
      margin-bottom: 0.5rem;
    }}
    .hero-subtitle {{
      font-size: 1rem;
      color: #71717A;
      max-width: 720px;
    }}

    /* Section Styles */
    .doc-section {{
      padding: 3rem;
      border-bottom: 1px solid #27272A;
    }}
    .doc-section:last-child {{
      border-bottom: none;
    }}

    .section-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: #E60012;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .section-label::before {{
      content: "";
      width: 8px;
      height: 8px;
      background: #E60012;
      display: inline-block;
    }}

    .section-title {{
      font-family: 'Archivo', sans-serif;
      font-size: 1.85rem;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 1rem;
    }}

    .section-lead {{
      font-size: 1.05rem;
      color: #A1A1AA;
      margin-bottom: 2rem;
      max-width: 840px;
    }}

    /* Grid Layouts */
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 1.75rem;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.5rem;
    }}
    .grid-5 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 1rem;
    }}

    /* Cards */
    .asset-card {{
      background: #1F1F23;
      border: 1px solid #2E2E33;
      border-radius: 14px;
      padding: 1.5rem;
      display: flex;
      flex-col;
      flex-direction: column;
      justify-content: space-between;
    }}
    .asset-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #A1A1AA;
    }}

    .asset-preview {{
      background: #FAFAF9;
      border-radius: 12px;
      padding: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 220px;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }}
    .asset-preview.dark-preview {{
      background: #0A0A0A;
    }}

    .asset-card-footer {{
      margin-top: 1.25rem;
      font-size: 0.85rem;
      color: #D4D4D8;
    }}
    .asset-card-footer strong {{
      color: white;
      display: block;
      margin-bottom: 0.2rem;
    }}

    /* Color Chips */
    .color-chip {{
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid #2E2E33;
      background: #1F1F23;
    }}
    .color-swatch {{
      height: 90px;
      width: 100%;
    }}
    .color-info {{
      padding: 1rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
    }}
    .color-name {{
      font-weight: 700;
      color: white;
      font-size: 0.9rem;
      margin-bottom: 0.25rem;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .color-hex {{
      color: #FFDD00;
      font-weight: 700;
    }}
    .color-role {{
      font-size: 0.72rem;
      color: #A1A1AA;
      margin-top: 0.25rem;
    }}

    /* Rules Table */
    .rules-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
      font-size: 0.9rem;
    }}
    .rules-table th, .rules-table td {{
      padding: 1rem 1.25rem;
      text-align: left;
      border-bottom: 1px solid #2E2E33;
    }}
    .rules-table th {{
      background: #121214;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #A1A1AA;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .rules-table tr:hover td {{
      background: #1C1C20;
    }}
    .badge-do {{
      color: #22C55E;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }}
    .badge-dont {{
      color: #EF4444;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Typography Showcase */
    .type-specimen {{
      background: #1F1F23;
      border: 1px solid #2E2E33;
      border-radius: 14px;
      padding: 2rem;
      margin-bottom: 1.5rem;
    }}
    .type-specimen-header {{
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid #2E2E33;
      padding-bottom: 0.75rem;
      margin-bottom: 1.25rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #A1A1AA;
    }}

    /* Print Styles */
    @media print {{
      body {{
        background: white !important;
        color: black !important;
        padding: 0 !important;
      }}
      .action-bar {{
        display: none !important;
      }}
      .doc-container {{
        box-shadow: none !important;
        border: none !important;
        background: white !important;
        max-width: 100% !important;
      }}
      .doc-section {{
        background: white !important;
        color: black !important;
        border-bottom: 1px solid #E4E4E7 !important;
        padding: 2rem 1.5rem !important;
      }}
      .section-title {{
        color: black !important;
      }}
      .section-lead {{
        color: #52525B !important;
      }}
      .asset-card, .type-specimen, .color-chip {{
        background: #F4F4F5 !important;
        border: 1px solid #D4D4D8 !important;
        color: black !important;
      }}
      .asset-card-footer strong, .color-name {{
        color: black !important;
      }}
      .asset-card-footer, .color-role {{
        color: #52525B !important;
      }}
      .rules-table th {{
        background: #E4E4E7 !important;
        color: black !important;
      }}
      .rules-table td {{
        border-bottom: 1px solid #E4E4E7 !important;
        color: black !important;
      }}
      .page-break {{
        page-break-after: always;
        break-after: page;
      }}
      * {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
    }}
  </style>
</head>
<body>

  <div class="doc-container">

    <!-- Action Bar -->
    <div class="action-bar">
      <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #A1A1AA;">
        <strong>Pay-by-Play</strong> · Official Brand Specification Document
      </div>
      <div style="display: flex; gap: 0.75rem;">
        <button class="action-btn secondary-btn" onclick="window.scrollTo({{ top: document.body.scrollHeight, behavior: 'smooth' }})">
          📦 Asset Matrix
        </button>
        <button class="action-btn" onclick="window.print()">
          🖨️ Print / Save as PDF
        </button>
      </div>
    </div>

    <!-- Cover Page -->
    <header class="cover-header">
      <div class="de-stijl-stripe">
        <div class="stripe-blue"></div>
        <div class="stripe-yellow"></div>
        <div class="stripe-red"></div>
      </div>

      <div class="badge-pills">
        <span class="pill pill-black">BRAND SYSTEM v1.2</span>
        <span class="pill pill-red">DE STIJL MODERNISM</span>
        <span class="pill pill-blue">WOMEN'S PRO SPORTS</span>
        <span class="pill pill-yellow">PRODUCTION READY</span>
      </div>

      <h1 class="hero-title">
        <span class="pay">PAY</span><span class="by"> -BY- </span><span class="play">PLAY</span>
      </h1>
      <p class="hero-tagline">Does pay follow play, and does the pay structure change the answer?</p>
      <p class="hero-subtitle">
        A cross-league econometrics and decision-support layer for women's professional sports leagues
        (PWHL hockey, WNBA basketball, and WPL cricket).
      </p>
    </header>

    <!-- Section 1: Executive Summary & Philosophy -->
    <section class="doc-section">
      <div class="section-label">01 / Foundation</div>
      <h2 class="section-title">Brand Purpose &amp; Modernist Geometry</h2>
      <p class="section-lead">
        <strong>Pay-by-Play</strong> exists at the intersection of labor econometrics and athletic performance.
        The visual identity is anchored in the principles of <strong>De Stijl</strong> (The Style) — pioneered by
        Piet Mondrian and Gerrit Rietveld — which uses asymmetric rectilinear grids, pure primary colors,
        and bold structural framing to convey mathematical honesty and structural integrity.
      </p>

      <div class="grid-3">
        <div class="asset-card">
          <div class="asset-card-header">
            <span>METRIC MAPPING</span>
            <span>01</span>
          </div>
          <div>
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚖️</div>
            <h3 style="color: white; margin-bottom: 0.5rem; font-size: 1.1rem;">Pay vs. Play</h3>
            <p style="font-size: 0.85rem; color: #A1A1AA;">
              <strong>Pay</strong> (Blue) represents the financial baseline, disclosed salary bands, and cap constraints.
              <strong>Play</strong> (Red) represents on-field box score production and game-level value.
            </p>
          </div>
        </div>

        <div class="asset-card">
          <div class="asset-card-header">
            <span>THE VALUE GAP</span>
            <span>02</span>
          </div>
          <div>
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📐</div>
            <h3 style="color: white; margin-bottom: 0.5rem; font-size: 1.1rem;">The Surplus Signal</h3>
            <p style="font-size: 0.85rem; color: #A1A1AA;">
              <strong>Canary Yellow</strong> is reserved for the gap metric (value_pct − pay_pct).
              It signals surplus value, confident bargains, and players whose production outruns their paycheck.
            </p>
          </div>
        </div>

        <div class="asset-card">
          <div class="asset-card-header">
            <span>ATHLETIC GRID</span>
            <span>03</span>
          </div>
          <div>
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏒</div>
            <h3 style="color: white; margin-bottom: 0.5rem; font-size: 1.1rem;">Pitch &amp; Court Lines</h3>
            <p style="font-size: 0.85rem; color: #A1A1AA;">
              Structural ink lines echo both financial data tables and sports playing surfaces:
              the hockey goal crease, the basketball key, and the cricket batting crease.
            </p>
          </div>
        </div>
      </div>
    </section>

    <div class="page-break"></div>

    <!-- Section 2: Logo Suite -->
    <section class="doc-section">
      <div class="section-label">02 / Logo System</div>
      <h2 class="section-title">The Complete Logo Suite</h2>
      <p class="section-lead">
        The brand assets are engineered as infinitely scalable vector SVGs and pixel-perfect high-DPI PNGs
        for cross-platform deployment across web apps, documentation, mobile shortcuts, and print decks.
      </p>

      <div class="grid-2" style="margin-bottom: 2rem;">
        <!-- Complete Logo Mark -->
        <div class="asset-card">
          <div class="asset-card-header">
            <span>COMPLETE LOGO MARK</span>
            <span>assets/logo-mark.svg</span>
          </div>
          <div class="asset-preview">
            <div style="width: 220px; height: 220px;">
              {svg_mark}
            </div>
          </div>
          <div class="asset-card-footer">
            <strong>Complete Logo Mark</strong>
            Features the primary De Stijl graphic tile, the central forward play glyph (▶),
            and the signature <code>PAY -BY- PLAY</code> typographic lockup.
          </div>
        </div>

        <!-- Square App Icon -->
        <div class="asset-card">
          <div class="asset-card-header">
            <span>SQUARE APP ICON</span>
            <span>assets/logo-icon.svg</span>
          </div>
          <div class="asset-preview">
            <div style="width: 220px; height: 220px;">
              {svg_icon}
            </div>
          </div>
          <div class="asset-card-footer">
            <strong>App Icon &amp; Favicon</strong>
            Optimized for standalone recognition from 16×16px favicons up to 512×512px app launcher tiles.
          </div>
        </div>
      </div>

      <!-- Wide Banner -->
      <div class="asset-card" style="margin-bottom: 2rem;">
        <div class="asset-card-header">
          <span>WIDE BANNER &amp; WORDMARK</span>
          <span>assets/logo-wordmark.svg · 1280 × 512</span>
        </div>
        <div class="asset-preview" style="padding: 1.5rem 2rem;">
          <div style="width: 100%; max-width: 800px;">
            {svg_wordmark}
          </div>
        </div>
        <div class="asset-card-footer">
          <strong>Header Wordmark Banner</strong>
          Engineered for GitHub READMEs, Streamlit landing screens, presentation deck covers, and social cards.
        </div>
      </div>

      <div class="grid-2">
        <!-- Two Lenses Emblem -->
        <div class="asset-card">
          <div class="asset-card-header">
            <span>CONCEPT B: TWO LENSES EMBLEM</span>
            <span>assets/concepts/logo-emblem-lenses.svg</span>
          </div>
          <div class="asset-preview">
            <div style="width: 220px; height: 220px;">
              {svg_emblem}
            </div>
          </div>
          <div class="asset-card-footer">
            <strong>Two Lenses Stadium Emblem</strong>
            Circular stadium crest directly visualizing Lens A (Pay Rationality) and Lens B (Return on Pay)
            split across a 45° dynamic boundary with coordinate grid notches.
          </div>
        </div>

        <!-- Dark Mode Icon -->
        <div class="asset-card">
          <div class="asset-card-header">
            <span>DARK MODE OPTIMIZED ICON</span>
            <span>assets/logo-icon-dark.svg</span>
          </div>
          <div class="asset-preview dark-preview">
            <div style="width: 220px; height: 220px;">
              {svg_icon_dark}
            </div>
          </div>
          <div class="asset-card-footer">
            <strong>Dark Theme Icon</strong>
            Calibrated with higher-vibrancy tints (#FF3333 and #4D88FF) on a slate #121212 ground.
          </div>
        </div>
      </div>
    </section>

    <div class="page-break"></div>

    <!-- Section 3: Color Palette -->
    <section class="doc-section">
      <div class="section-label">03 / Palette</div>
      <h2 class="section-title">Color System &amp; Tokens</h2>
      <p class="section-lead">
        The palette strictly adheres to authentic De Stijl primaries: high-saturation Red, Cobalt Blue,
        Canary Yellow, structural Ink Black, and warm Paper White.
      </p>

      <div class="grid-5" style="margin-bottom: 2rem;">
        <!-- Blue -->
        <div class="color-chip">
          <div class="color-swatch" style="background: {DS_BLUE};"></div>
          <div class="color-info">
            <div class="color-name">De Stijl Blue</div>
            <div class="color-hex">{DS_BLUE}</div>
            <div class="color-role">RGB 0, 71, 171<br>Pay / Salary Base</div>
          </div>
        </div>

        <!-- Red -->
        <div class="color-chip">
          <div class="color-swatch" style="background: {DS_RED};"></div>
          <div class="color-info">
            <div class="color-name">De Stijl Red</div>
            <div class="color-hex">{DS_RED}</div>
            <div class="color-role">RGB 230, 0, 18<br>Play / Production</div>
          </div>
        </div>

        <!-- Yellow -->
        <div class="color-chip">
          <div class="color-swatch" style="background: {DS_YELLOW};"></div>
          <div class="color-info">
            <div class="color-name">Canary Yellow</div>
            <div class="color-hex">{DS_YELLOW}</div>
            <div class="color-role">RGB 255, 221, 0<br>The Value Gap</div>
          </div>
        </div>

        <!-- Ink -->
        <div class="color-chip">
          <div class="color-swatch" style="background: {DS_BLACK}; border-bottom: 1px solid #333;"></div>
          <div class="color-info">
            <div class="color-name">Structural Ink</div>
            <div class="color-hex">{DS_BLACK}</div>
            <div class="color-role">RGB 10, 10, 10<br>Grids &amp; Framing</div>
          </div>
        </div>

        <!-- Paper -->
        <div class="color-chip">
          <div class="color-swatch" style="background: {DS_PAPER};"></div>
          <div class="color-info">
            <div class="color-name">Paper White</div>
            <div class="color-hex">{DS_PAPER}</div>
            <div class="color-role">RGB 250, 250, 249<br>Canvas Ground</div>
          </div>
        </div>
      </div>

      <div class="asset-card">
        <h4 style="color: white; margin-bottom: 0.5rem; font-size: 1rem;">Palette Hierarchy &amp; Distribution Rule</h4>
        <p style="font-size: 0.85rem; color: #A1A1AA; line-height: 1.6;">
          In any application, maintain the <strong>40-30-15-10-5</strong> balance:
          <strong>40% Paper White</strong> (open breathing room),
          <strong>30% Structural Ink</strong> (data lines, text, framing),
          <strong>15% De Stijl Red</strong> (action callouts, highlights),
          <strong>10% De Stijl Blue</strong> (foundational anchors, payroll bars), and
          <strong>5% Canary Yellow</strong> (focal points, value gap badges, bargains).
        </p>
      </div>
    </section>

    <!-- Section 4: Typography -->
    <section class="doc-section">
      <div class="section-label">04 / Typography</div>
      <h2 class="section-title">Type Hierarchy &amp; Font Stack</h2>
      <p class="section-lead">
        Typography mirrors the dual nature of the product: aggressive athletic sans-serif headers
        paired with monospaced precision for statistical percentiles and formulas.
      </p>

      <!-- Archivo Specimen -->
      <div class="type-specimen">
        <div class="type-specimen-header">
          <span>PRIMARY DISPLAY · ARCHIVO (WEIGHT 900 / 800)</span>
          <span>HEADINGS &amp; LOGO WORDMARKS</span>
        </div>
        <div style="font-family: 'Archivo', sans-serif; font-size: 2.5rem; font-weight: 900; color: white; letter-spacing: -0.02em; margin-bottom: 0.5rem;">
          PAY -BY- PLAY
        </div>
        <div style="font-family: 'Archivo', sans-serif; font-size: 1.3rem; font-weight: 800; color: #A1A1AA; margin-bottom: 0.5rem;">
          DOES PAY FOLLOW PLAY IN WOMEN&rsquo;S PRO LEAGUES?
        </div>
        <div style="font-family: 'Archivo', sans-serif; font-size: 0.95rem; font-weight: 600; color: #71717A;">
          ABCDEFGHIJKLMNOPQRSTUVWXYZ · 0123456789 · $ % &amp; / ( )
        </div>
      </div>

      <!-- JetBrains Mono Specimen -->
      <div class="type-specimen">
        <div class="type-specimen-header">
          <span>DATA &amp; FORMULA FONT · JETBRAINS MONO (WEIGHT 500 / 700)</span>
          <span>METRICS, CODE &amp; -BY- CONNECTOR</span>
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 700; color: #FFDD00; margin-bottom: 0.5rem;">
          gap = value_pct - pay_pct
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; color: #E4E4E7; margin-bottom: 0.5rem;">
          PWHL $1,436,173.50 · WNBA 2026 CAP HIT · WPL AUCTION
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #71717A;">
          abcdefghijklmnopqrstuvwxyz 0123456789 {{ [ ] }} == &gt;= &lt;=
        </div>
      </div>
    </section>

    <div class="page-break"></div>

    <!-- Section 5: Brand Rules & Misuse -->
    <section class="doc-section">
      <div class="section-label">05 / Governance</div>
      <h2 class="section-title">Brand Rules: Do&rsquo;s and Don&rsquo;ts</h2>
      <p class="section-lead">
        To maintain visual recognition and authoritative econometric presentation, adhere to these guidelines.
      </p>

      <table class="rules-table">
        <thead>
          <tr>
            <th style="width: 15%;">Status</th>
            <th style="width: 42%;">Guideline</th>
            <th style="width: 43%;">Rationale</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="badge-do">✓ DO</span></td>
            <td>Always include the <strong>-BY-</strong> connector in the complete mark.</td>
            <td>Reinforces the trademark name and the relationship between compensation and athletic output.</td>
          </tr>
          <tr>
            <td><span class="badge-do">✓ DO</span></td>
            <td>Maintain the 1:1 square aspect ratio on app icons.</td>
            <td>Preserves the balanced Mondrian rectilinear cell distribution.</td>
          </tr>
          <tr>
            <td><span class="badge-do">✓ DO</span></td>
            <td>Keep the Play triangle pointing directly forward (to the right).</td>
            <td>Represents forward kinetic progress and playback of sports action.</td>
          </tr>
          <tr>
            <td><span class="badge-dont">✗ DON'T</span></td>
            <td>Never replace primary colors with gradients or pastels.</td>
            <td>De Stijl requires pure, unadulterated primary colors and stark black structural lines.</td>
          </tr>
          <tr>
            <td><span class="badge-dont">✗ DON'T</span></td>
            <td>Never remove the outer structural black border.</td>
            <td>The outer border contains the geometry and prevents bleeding on light surfaces.</td>
          </tr>
          <tr>
            <td><span class="badge-dont">✗ DON'T</span></td>
            <td>Never rotate or skew the logo mark or typography.</td>
            <td>All lines must remain purely orthogonal (horizontal and vertical).</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Section 6: Asset Inventory -->
    <section class="doc-section">
      <div class="section-label">06 / Asset Matrix</div>
      <h2 class="section-title">Production Asset Inventory</h2>
      <p class="section-lead">
        Summary of all generated files in the <code>assets/</code> directory ready for deployment.
      </p>

      <table class="rules-table">
        <thead>
          <tr>
            <th>Filename</th>
            <th>Type</th>
            <th>Dimensions</th>
            <th>Primary Usage</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>assets/logo-mark.svg</code></td>
            <td>Vector SVG</td>
            <td>512 × 512</td>
            <td>Primary complete logo mark with <code>PAY -BY- PLAY</code> lockup.</td>
          </tr>
          <tr>
            <td><code>assets/logo-icon.svg</code></td>
            <td>Vector SVG</td>
            <td>512 × 512</td>
            <td>Standalone app icon &amp; favicon glyph.</td>
          </tr>
          <tr>
            <td><code>assets/logo-icon-dark.svg</code></td>
            <td>Vector SVG</td>
            <td>512 × 512</td>
            <td>Dark-mode calibrated app icon.</td>
          </tr>
          <tr>
            <td><code>assets/logo-wordmark.svg</code></td>
            <td>Vector SVG</td>
            <td>1280 × 512</td>
            <td>Horizontal banner for GitHub README, headers, and slides.</td>
          </tr>
          <tr>
            <td><code>assets/concepts/logo-emblem-lenses.svg</code></td>
            <td>Vector SVG</td>
            <td>512 × 512</td>
            <td>Two Lenses circular stadium/rink crest.</td>
          </tr>
          <tr>
            <td><code>assets/favicon-32.png</code></td>
            <td>Raster PNG</td>
            <td>32 × 32</td>
            <td>Browser tab favicon (configured in Streamlit).</td>
          </tr>
          <tr>
            <td><code>assets/favicon-64.png</code></td>
            <td>Raster PNG</td>
            <td>64 × 64</td>
            <td>Retina browser favicon.</td>
          </tr>
          <tr>
            <td><code>assets/logo-icon-128.png</code></td>
            <td>Raster PNG</td>
            <td>128 × 128</td>
            <td>App dock icon &amp; profile avatar.</td>
          </tr>
          <tr>
            <td><code>assets/logo-icon-256.png</code></td>
            <td>Raster PNG</td>
            <td>256 × 256</td>
            <td>Desktop application launcher icon.</td>
          </tr>
          <tr>
            <td><code>assets/logo-mark-512.png</code></td>
            <td>Raster PNG</td>
            <td>512 × 512</td>
            <td>High-resolution complete mark with <code>PAY -BY- PLAY</code>.</td>
          </tr>
          <tr>
            <td><code>assets/logo-wordmark-1280.png</code></td>
            <td>Raster PNG</td>
            <td>1280 × 512</td>
            <td>Retina banner image for social cards and documentation.</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Footer -->
    <footer style="background: #121214; padding: 2rem 3rem; border-top: 1px solid #27272A; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #71717A;">
      <div>
        © 2026 <strong>Pay-by-Play</strong> · Cross-League Econometrics
      </div>
      <div>
        Specification v1.2 · Prepared for Stakeholders &amp; Contributors
      </div>
    </footer>

  </div>

</body>
</html>"""


def build_markdown_document() -> str:
    return """# Pay-by-Play — Brand Identity & Specification Document

> **"Does pay follow play, and does the pay structure change the answer?"**  
> *Cross-league econometrics and decision-support for women's pro sports (PWHL, WNBA, WPL).*

---

## 1. Executive Summary

**Pay-by-Play** provides econometric evaluation and decision support for women's professional sports leagues where compensation data is publicly disclosed. 

The brand identity marries **high-rigor sports analytics** with **Dutch De Stijl / Bauhaus Modernism** (pioneered by Piet Mondrian and Gerrit Rietveld). It uses pure primary colors, asymmetric rectilinear grids, and bold structural ink lines to convey mathematical honesty.

---

## 2. Core Visual Rationale

| Element | Color / Asset | Meaning & Domain Role |
| :--- | :--- | :--- |
| **PAY** | `#0047AB` (De Stijl Blue) & `#0A0A0A` (Ink) | Contracted compensation, base salary guides, and payroll stability. |
| **-BY-** | `#71717A` (Muted Gray / Mono) | Relational connector matching the `.dstijl-by` token in the Streamlit app. |
| **PLAY** | `#E60012` (De Stijl Red) | On-field production, box score output, and athletic momentum. |
| **The Gap** | `#FFDD00` (Canary Yellow) | The surplus metric ($gap = value\\_pct - pay\\_pct$), highlighting confident bargains and raise cases. |
| **Play Arrow** | Optical Center (▶) | Forward athletic motion and playback of sports action. |
| **Sports Arcs** | Dashed Crease Curves | Hockey goal creases, basketball free-throw keys, and cricket batting creases. |

---

## 3. The Logo Suite

All logo assets are located in the [`assets/`](../assets/) directory:

- **Complete Logo Mark**: [`assets/logo-mark.svg`](../assets/logo-mark.svg)  
  Features the primary De Stijl graphic tile, the central forward play arrow (▶), and the signature `PAY -BY- PLAY` lockup.
- **Square App Icon & Favicon**: [`assets/logo-icon.svg`](../assets/logo-icon.svg)  
  Optimized for high-contrast visibility at 16px, 32px, 64px, 128px, and 256px.
- **Dark Mode Icon**: [`assets/logo-icon-dark.svg`](../assets/logo-icon-dark.svg)  
  Calibrated with higher-vibrancy tints on a slate ground.
- **Header Wordmark Banner**: [`assets/logo-wordmark.svg`](../assets/logo-wordmark.svg)  
  1280×512 retina banner for GitHub README, web headers, and presentation slide covers.
- **Concept B Stadium Emblem**: [`assets/concepts/logo-emblem-lenses.svg`](../assets/concepts/logo-emblem-lenses.svg)  
  Circular crest representing Lens A (pay rationality) and Lens B (return on pay).

---

## 4. Color Palette Specifications

| Name | Role | Hex Code | RGB | HSL |
| :--- | :--- | :--- | :--- | :--- |
| **De Stijl Red** | Play / Action Callout | `#E60012` | `230, 0, 18` | `355°, 100%, 45%` |
| **De Stijl Blue** | Pay / Stability Anchor | `#0047AB` | `0, 71, 171` | `215°, 100%, 34%` |
| **Canary Yellow** | The Value Gap / Bargains | `#FFDD00` | `255, 221, 0` | `52°, 100%, 50%` |
| **Structural Ink** | Grids & Frame Lines | `#0A0A0A` | `10, 10, 10` | `0°, 0%, 4%` |
| **Paper White** | Canvas Ground | `#FAFAF9` | `250, 250, 249` | `60°, 9%, 98%` |

---

## 5. Typography Hierarchy

- **Display Headers**: `Archivo` (Weight 900 / Black) — bold, athletic, high-impact sans-serif.
- **Data & Metrics**: `JetBrains Mono` (Weight 500 / 700) — tabular numbers, formula tags, and `-BY-`.
- **UI & Prose**: `Helvetica` / `Plus Jakarta Sans` / System Sans-serif — clean, neutral readability.

---

## 6. Brand Governance (Do's and Don'ts)

- **DO** always use the full `PAY -BY- PLAY` lockup in complete marks.
- **DO** maintain the 1:1 aspect ratio on app icons.
- **DO** keep the play arrow pointing directly forward (to the right).
- **DON'T** replace primary colors with pastels, gradients, or non-modernist tints.
- **DON'T** omit the outer structural black line.
- **DON'T** rotate, skew, or stretch the geometry.
"""


def compile_pdf(html_path: Path, pdf_path: Path) -> bool:
    """Compile HTML to PDF using Chrome or Edge headless."""
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    browser = next((c for c in candidates if c.exists()), None)
    if not browser:
        print("No headless browser found to compile PDF.")
        return False

    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        str(html_path),
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if pdf_path.exists() and pdf_path.stat().st_size > 1000:
            print(f"Compiled PDF successfully: {pdf_path} ({pdf_path.stat().st_size} bytes)")
            return True
        else:
            print("PDF generation failed or file empty:", res.stderr)
            return False
    except Exception as e:
        print("Error compiling PDF:", e)
        return False


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)

    html_file = DOCS / "Pay_By_Play_Brand_Identity.html"
    md_file = DOCS / "BRAND_GUIDELINES.md"
    pdf_file = DOCS / "Pay_By_Play_Brand_Identity.pdf"

    html_content = build_html_document()
    html_file.write_text(html_content, encoding="utf-8")
    print(f"Wrote HTML document: {html_file}")

    md_content = build_markdown_document()
    md_file.write_text(md_content, encoding="utf-8")
    print(f"Wrote Markdown document: {md_file}")

    compile_pdf(html_file, pdf_file)


if __name__ == "__main__":
    main()
