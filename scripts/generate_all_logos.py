"""Generate high-quality De Stijl SVGs and PNGs for Pay-by-Play."""

from __future__ import annotations

from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ASSETS = ROOT / "assets"
CONCEPTS = ASSETS / "concepts"

# De Stijl Palette
DS_RED = "#E60012"
DS_BLUE = "#0047AB"
DS_YELLOW = "#FFDD00"
DS_BLACK = "#0A0A0A"
DS_PAPER = "#FAFAF9"
DS_GRAY = "#71717A"
DS_WHITE = "#FFFFFF"

# Dark Theme Palette
DARK_BG = "#121212"
DARK_SURFACE = "#1E1E22"
DARK_RED = "#FF3333"
DARK_BLUE = "#4D88FF"
DARK_YELLOW = "#FFDD00"
DARK_INK = "#F5F5F5"
DARK_GRAY = "#A1A1AA"


def create_svg_icon() -> str:
    """Crisp, iconic De Stijl square app icon / favicon glyph."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%" role="img" aria-label="Pay-by-Play Icon">
  <defs>
    <clipPath id="squircle">
      <rect x="16" y="16" width="480" height="480" rx="64"/>
    </clipPath>
    <filter id="subtle-shadow" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.18"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect x="16" y="16" width="480" height="480" rx="64" fill="{DS_PAPER}"/>

  <!-- Clipped Mondrian Grid Canvas -->
  <g clip-path="url(#squircle)">
    <!-- Blue Block (Pay / Stability) -->
    <rect x="16" y="16" width="194" height="280" fill="{DS_BLUE}"/>

    <!-- Red Block (Play / Athletic Action) -->
    <rect x="210" y="16" width="286" height="314" fill="{DS_RED}"/>

    <!-- Play Symbol inside Red Block -->
    <!-- Centered optical play triangle (pointed right) -->
    <polygon points="315,100 315,246 430,173" fill="{DS_PAPER}" filter="url(#subtle-shadow)"/>
    <polygon points="315,100 315,246 430,173" fill="none" stroke="{DS_BLACK}" stroke-width="8" stroke-linejoin="round"/>

    <!-- Yellow Block (The Value Gap / Surplus / Bargain) -->
    <rect x="210" y="330" width="140" height="166" fill="{DS_YELLOW}"/>

    <!-- Deep Ink Block (Bottom-Right Anchor) -->
    <rect x="350" y="330" width="146" height="166" fill="{DS_BLACK}"/>

    <!-- Bottom-Left Light Block with Econometric Grid Accents -->
    <rect x="16" y="296" width="194" height="200" fill="{DS_PAPER}"/>
    <!-- Subtle horizontal bar lines evoking a salary ledger / data table -->
    <line x1="44" y1="345" x2="182" y2="345" stroke="{DS_BLACK}" stroke-width="6" stroke-linecap="round"/>
    <line x1="44" y1="385" x2="150" y2="385" stroke="{DS_BLACK}" stroke-width="6" stroke-linecap="round"/>
    <line x1="44" y1="425" x2="168" y2="425" stroke="{DS_BLACK}" stroke-width="6" stroke-linecap="round"/>

    <!-- Mondrian Master Structural Grid Lines (12px bold black lines) -->
    <!-- Main Vertical Spine -->
    <line x1="210" y1="16" x2="210" y2="496" stroke="{DS_BLACK}" stroke-width="12"/>
    <!-- Top-Left Horizontal Line -->
    <line x1="16" y1="296" x2="210" y2="296" stroke="{DS_BLACK}" stroke-width="12"/>
    <!-- Bottom-Right Horizontal Line -->
    <line x1="210" y1="330" x2="496" y2="330" stroke="{DS_BLACK}" stroke-width="12"/>
    <!-- Bottom-Right Sub-Vertical Line -->
    <line x1="350" y1="330" x2="350" y2="496" stroke="{DS_BLACK}" stroke-width="12"/>

    <!-- Sports Court / Rink Accent: Semi-circle crease cutting across the grid -->
    <path d="M 210,120 A 53 53 0 0 0 210,226" fill="none" stroke="{DS_PAPER}" stroke-width="6" stroke-dasharray="10 8"/>
  </g>

  <!-- Outer Structural Border -->
  <rect x="16" y="16" width="480" height="480" rx="64" fill="none" stroke="{DS_BLACK}" stroke-width="12"/>
</svg>"""


def create_svg_icon_dark() -> str:
    """Dark-mode variant of the app icon."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%" role="img" aria-label="Pay-by-Play Icon (Dark)">
  <defs>
    <clipPath id="squircle-dark">
      <rect x="16" y="16" width="480" height="480" rx="64"/>
    </clipPath>
  </defs>

  <rect x="16" y="16" width="480" height="480" rx="64" fill="{DARK_BG}"/>

  <g clip-path="url(#squircle-dark)">
    <!-- Blue Block -->
    <rect x="16" y="16" width="194" height="280" fill="{DARK_BLUE}"/>

    <!-- Red Block -->
    <rect x="210" y="16" width="286" height="314" fill="{DARK_RED}"/>

    <!-- Play Symbol -->
    <polygon points="315,100 315,246 430,173" fill="{DARK_INK}" stroke="{DARK_BG}" stroke-width="8" stroke-linejoin="round"/>

    <!-- Yellow Block -->
    <rect x="210" y="330" width="140" height="166" fill="{DARK_YELLOW}"/>

    <!-- Dark Surface Block -->
    <rect x="350" y="330" width="146" height="166" fill="{DARK_SURFACE}"/>

    <!-- Bottom-Left Charcoal Block -->
    <rect x="16" y="296" width="194" height="200" fill="#18181B"/>
    <line x1="44" y1="345" x2="182" y2="345" stroke="{DARK_INK}" stroke-width="6" stroke-linecap="round"/>
    <line x1="44" y1="385" x2="150" y2="385" stroke="{DARK_INK}" stroke-width="6" stroke-linecap="round"/>
    <line x1="44" y1="425" x2="168" y2="425" stroke="{DARK_INK}" stroke-width="6" stroke-linecap="round"/>

    <!-- Grid Lines -->
    <line x1="210" y1="16" x2="210" y2="496" stroke="{DARK_BG}" stroke-width="12"/>
    <line x1="16" y1="296" x2="210" y2="296" stroke="{DARK_BG}" stroke-width="12"/>
    <line x1="210" y1="330" x2="496" y2="330" stroke="{DARK_BG}" stroke-width="12"/>
    <line x1="350" y1="330" x2="350" y2="496" stroke="{DARK_BG}" stroke-width="12"/>

    <!-- Arc -->
    <path d="M 210,120 A 53 53 0 0 0 210,226" fill="none" stroke="{DARK_INK}" stroke-width="6" stroke-dasharray="10 8"/>
  </g>

  <rect x="16" y="16" width="480" height="480" rx="64" fill="none" stroke="{DARK_INK}" stroke-width="10"/>
</svg>"""


def create_svg_logo_mark() -> str:
    """The complete logo mark: icon badge + architectural typography."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%" role="img" aria-label="Pay-by-Play Logo">
  <defs>
    <clipPath id="top-panel">
      <rect x="36" y="36" width="440" height="300" rx="28"/>
    </clipPath>
    <filter id="glow-play" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Container Box -->
  <rect x="16" y="16" width="480" height="480" rx="48" fill="{DS_PAPER}"/>
  <rect x="16" y="16" width="480" height="480" rx="48" fill="none" stroke="{DS_BLACK}" stroke-width="10"/>

  <!-- Upper Visual Panel -->
  <g clip-path="url(#top-panel)">
    <!-- Base Paper Fill -->
    <rect x="36" y="36" width="440" height="300" fill="{DS_PAPER}"/>

    <!-- Blue Field (Pay) -->
    <rect x="36" y="36" width="180" height="210" fill="{DS_BLUE}"/>

    <!-- Red Field (Play) -->
    <rect x="216" y="36" width="260" height="210" fill="{DS_RED}"/>

    <!-- Yellow Accent Block -->
    <rect x="216" y="246" width="124" height="90" fill="{DS_YELLOW}"/>

    <!-- Ink Block -->
    <rect x="340" y="246" width="136" height="90" fill="{DS_BLACK}"/>

    <!-- Bottom Left Subtle Ledger Lines -->
    <line x1="60" y1="270" x2="190" y2="270" stroke="{DS_BLACK}" stroke-width="5" stroke-linecap="round"/>
    <line x1="60" y1="300" x2="155" y2="300" stroke="{DS_BLACK}" stroke-width="5" stroke-linecap="round"/>

    <!-- Central Play Arrow (Optically centered at x=346, y=141) -->
    <polygon points="305,95 305,187 385,141" fill="{DS_PAPER}" filter="url(#glow-play)"/>
    <polygon points="305,95 305,187 385,141" fill="none" stroke="{DS_BLACK}" stroke-width="6" stroke-linejoin="round"/>

    <!-- Hockey / Basketball Sports Arc Accent -->
    <path d="M 216,91 A 50 50 0 0 0 216,191" fill="none" stroke="{DS_PAPER}" stroke-width="5" stroke-dasharray="8 6"/>

    <!-- Grid Dividing Lines -->
    <line x1="216" y1="36" x2="216" y2="336" stroke="{DS_BLACK}" stroke-width="10"/>
    <line x1="36" y1="246" x2="476" y2="246" stroke="{DS_BLACK}" stroke-width="10"/>
    <line x1="340" y1="246" x2="340" y2="336" stroke="{DS_BLACK}" stroke-width="10"/>
  </g>
  <!-- Border around panel -->
  <rect x="36" y="36" width="440" height="300" rx="28" fill="none" stroke="{DS_BLACK}" stroke-width="8"/>

  <!-- Horizontal Divider Line -->
  <line x1="36" y1="362" x2="476" y2="362" stroke="{DS_BLACK}" stroke-width="6"/>

  <!-- Typography: PAY -BY- PLAY -->
  <text x="256" y="428" text-anchor="middle" font-family="'Archivo', 'Arial Black', Helvetica, sans-serif" font-size="40" font-weight="900" letter-spacing="0.04em">
    <tspan fill="{DS_BLACK}">PAY</tspan>
    <tspan fill="{DS_GRAY}" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="24" font-weight="700" letter-spacing="0.08em" dy="-3"> -BY- </tspan>
    <tspan fill="{DS_RED}" dy="3">PLAY</tspan>
  </text>

  <!-- Subtitle Tagline -->
  <text x="256" y="468" text-anchor="middle" font-family="'JetBrains Mono', 'Courier New', monospace" font-size="13" font-weight="700" fill="{DS_GRAY}" letter-spacing="0.26em">
    WOMEN'S PRO SPORTS ECONOMETRICS
  </text>
</svg>"""


def create_svg_wordmark() -> str:
    """Wide banner / horizontal wordmark (1280x512)."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 512" width="100%" height="100%" role="img" aria-label="Pay-by-Play Banner">
  <defs>
    <clipPath id="panel-wide">
      <rect x="0" y="0" width="380" height="380" rx="44"/>
    </clipPath>
    <filter id="shadow-wide" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.2"/>
    </filter>
  </defs>

  <!-- Clean Canvas -->
  <rect width="1280" height="512" fill="{DS_PAPER}"/>

  <!-- Left Icon Mark -->
  <g transform="translate(66, 66)">
    <!-- Container -->
    <rect width="380" height="380" rx="44" fill="{DS_PAPER}"/>

    <g clip-path="url(#panel-wide)">
      <!-- Blue Block -->
      <rect x="0" y="0" width="155" height="230" fill="{DS_BLUE}"/>

      <!-- Red Block -->
      <rect x="155" y="0" width="225" height="255" fill="{DS_RED}"/>

      <!-- Yellow Block -->
      <rect x="155" y="255" width="110" height="125" fill="{DS_YELLOW}"/>

      <!-- Black Block -->
      <rect x="265" y="255" width="115" height="125" fill="{DS_BLACK}"/>

      <!-- Bottom-Left Light Block with Ticks -->
      <rect x="0" y="230" width="155" height="150" fill="{DS_PAPER}"/>
      <line x1="28" y1="270" x2="130" y2="270" stroke="{DS_BLACK}" stroke-width="5" stroke-linecap="round"/>
      <line x1="28" y1="305" x2="105" y2="305" stroke="{DS_BLACK}" stroke-width="5" stroke-linecap="round"/>
      <line x1="28" y1="340" x2="120" y2="340" stroke="{DS_BLACK}" stroke-width="5" stroke-linecap="round"/>

      <!-- Play Symbol -->
      <polygon points="235,75 235,180 325,127" fill="{DS_PAPER}" filter="url(#shadow-wide)"/>
      <polygon points="235,75 235,180 325,127" fill="none" stroke="{DS_BLACK}" stroke-width="6" stroke-linejoin="round"/>

      <!-- Sports Arc -->
      <path d="M 155,70 A 57 57 0 0 0 155,185" fill="none" stroke="{DS_PAPER}" stroke-width="5" stroke-dasharray="8 6"/>

      <!-- Master Grid Lines -->
      <line x1="155" y1="0" x2="155" y2="380" stroke="{DS_BLACK}" stroke-width="10"/>
      <line x1="0" y1="230" x2="155" y2="230" stroke="{DS_BLACK}" stroke-width="10"/>
      <line x1="155" y1="255" x2="380" y2="255" stroke="{DS_BLACK}" stroke-width="10"/>
      <line x1="265" y1="255" x2="265" y2="380" stroke="{DS_BLACK}" stroke-width="10"/>
    </g>

    <!-- Outer Border -->
    <rect width="380" height="380" rx="44" fill="none" stroke="{DS_BLACK}" stroke-width="10"/>
  </g>

  <!-- Right Typography & Branding Block -->
  <g transform="translate(500, 110)">
    <!-- League Badge Pills -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="82" height="28" rx="6" fill="{DS_BLACK}"/>
      <text x="41" y="19" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="700" fill="{DS_WHITE}">PWHL</text>

      <rect x="94" y="0" width="82" height="28" rx="6" fill="{DS_RED}"/>
      <text x="135" y="19" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="700" fill="{DS_WHITE}">WNBA</text>

      <rect x="188" y="0" width="76" height="28" rx="6" fill="{DS_BLUE}"/>
      <text x="226" y="19" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="700" fill="{DS_WHITE}">WPL</text>

      <text x="280" y="20" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="600" fill="{DS_GRAY}">· CROSS-LEAGUE DECISION SUPPORT</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="98" font-family="'Archivo', 'Arial Black', Helvetica, sans-serif" font-size="64" font-weight="900" letter-spacing="-0.02em">
      <tspan fill="{DS_BLACK}">PAY</tspan>
      <tspan fill="{DS_GRAY}" font-family="'JetBrains Mono', monospace" font-size="38" font-weight="700" letter-spacing="0.06em" dy="-4"> -BY- </tspan>
      <tspan fill="{DS_RED}" dy="4">PLAY</tspan>
    </text>

    <!-- De Stijl Triple Color Rule -->
    <g transform="translate(0, 130)">
      <rect x="0" y="0" width="220" height="6" fill="{DS_BLUE}"/>
      <rect x="226" y="0" width="60" height="6" fill="{DS_YELLOW}"/>
      <rect x="292" y="0" width="380" height="6" fill="{DS_RED}"/>
    </g>

    <!-- Core Question Hook -->
    <text x="0" y="192" font-family="'Archivo', Helvetica, sans-serif" font-size="28" font-weight="700" fill="{DS_BLACK}">
      Does pay follow play?
    </text>

    <!-- Explanatory Subtitle -->
    <text x="0" y="235" font-family="Helvetica, Arial, sans-serif" font-size="20" font-weight="400" fill="{DS_GRAY}">
      Empirical Bayes value estimation · Two lenses on contract timing · Fairness metrics
    </text>

    <!-- Formula Tag -->
    <g transform="translate(0, 260)">
      <text x="0" y="24" font-family="'JetBrains Mono', monospace" font-size="15" font-weight="600" fill="{DS_BLACK}">
        gap = value_pct − pay_pct
      </text>
      <text x="260" y="24" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="{DS_GRAY}">
        (Within-league position percentiles)
      </text>
    </g>
  </g>
</svg>"""


def create_svg_emblem_lenses() -> str:
    """Concept B: Two Lenses Diamond / Stadium Emblem."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%" role="img" aria-label="Pay-by-Play Two Lenses Emblem">
  <defs>
    <clipPath id="circle-clip">
      <circle cx="256" cy="256" r="216"/>
    </clipPath>
    <filter id="emblem-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="512" height="512" rx="64" fill="{DS_PAPER}"/>

  <!-- Circle Badge -->
  <g clip-path="url(#circle-clip)">
    <!-- Upper-Left Hemisphere: Lens A / Pay (Blue) -->
    <polygon points="40,40 472,40 40,472" fill="{DS_BLUE}"/>

    <!-- Lower-Right Hemisphere: Lens B / Play (Red) -->
    <polygon points="472,40 472,472 40,472" fill="{DS_RED}"/>

    <!-- Sports Pitch Ring Lines -->
    <circle cx="256" cy="256" r="160" fill="none" stroke="{DS_PAPER}" stroke-width="4" stroke-opacity="0.4"/>
    <circle cx="256" cy="256" r="110" fill="none" stroke="{DS_PAPER}" stroke-width="4" stroke-opacity="0.6"/>

    <!-- Diagonal Black Separator Channel -->
    <line x1="30" y1="30" x2="482" y2="482" stroke="{DS_BLACK}" stroke-width="16"/>

    <!-- Central De Stijl Yellow Core (The Gap / Synthesis) -->
    <circle cx="256" cy="256" r="66" fill="{DS_YELLOW}" stroke="{DS_BLACK}" stroke-width="12" filter="url(#emblem-shadow)"/>

    <!-- Precisely Centered Play Triangle (cx=256, optical center adjusted) -->
    <!-- Triangle bounding box: x from 242 to 284 (width 42, center at 263, visual optical center aligns at 256) -->
    <polygon points="242,230 242,282 284,256" fill="{DS_PAPER}" stroke="{DS_BLACK}" stroke-width="6" stroke-linejoin="round"/>
  </g>

  <!-- Outer Ring Frames -->
  <circle cx="256" cy="256" r="216" fill="none" stroke="{DS_BLACK}" stroke-width="14"/>
  <circle cx="256" cy="256" r="228" fill="none" stroke="{DS_BLACK}" stroke-width="3"/>

  <!-- Compass / Coordinate Axis Notches (Modernist Econometrics) -->
  <line x1="256" y1="18" x2="256" y2="34" stroke="{DS_BLACK}" stroke-width="6"/>
  <line x1="256" y1="478" x2="256" y2="494" stroke="{DS_BLACK}" stroke-width="6"/>
  <line x1="18" y1="256" x2="34" y2="256" stroke="{DS_BLACK}" stroke-width="6"/>
  <line x1="478" y1="256" x2="494" y2="256" stroke="{DS_BLACK}" stroke-width="6"/>
</svg>"""


def export_svgs() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    CONCEPTS.mkdir(parents=True, exist_ok=True)

    files = {
        ASSETS / "logo-icon.svg": create_svg_icon(),
        ASSETS / "logo-icon-dark.svg": create_svg_icon_dark(),
        ASSETS / "logo-mark.svg": create_svg_logo_mark(),
        ASSETS / "logo-wordmark.svg": create_svg_wordmark(),
        CONCEPTS / "logo-emblem-lenses.svg": create_svg_emblem_lenses(),
    }

    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
        print(f"Wrote SVG: {path}")


def load_font(size: int, *, black: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        ("arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf")
        if black
        else ("arial.ttf", "Arial.ttf", "DejaVuSans.ttf")
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_all_pngs() -> None:
    """Render high-resolution PNGs at all key standard sizes using Pillow."""

    # Render sizes
    sizes = [
        (32, ASSETS / "favicon-32.png", True),
        (64, ASSETS / "favicon-64.png", True),
        (128, ASSETS / "logo-icon-128.png", True),
        (128, ASSETS / "logo-mark-128.png", False),
        (256, ASSETS / "logo-icon-256.png", True),
        (512, ASSETS / "logo-mark-512.png", False),
    ]

    for size, path, icon_only in sizes:
        img = Image.new("RGBA", (size, size), (250, 250, 249, 255))
        draw = ImageDraw.Draw(img)

        # Draw outer rounded border
        rx = max(4, size // 9)
        border_w = max(2, int(size * 0.024))
        draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=rx, fill=(250, 250, 249, 255), outline=(10, 10, 10, 255), width=border_w)

        if icon_only:
            # Full-tile Mondrian Icon
            m = max(2, int(size * 0.035))
            w = size - 2 * m
            h = size - 2 * m
            x0, y0 = m, m

            x_split = x0 + int(w * 0.40)
            y_left_split = y0 + int(h * 0.58)
            y_right_split = y0 + int(h * 0.65)
            x_sub_split = x_split + int((w - int(w * 0.40)) * 0.52)

            # Blue block (Top-Left)
            draw.rectangle([x0, y0, x_split, y_left_split], fill=(0, 71, 171, 255))

            # Red block (Top-Right)
            draw.rectangle([x_split, y0, x0 + w, y_right_split], fill=(230, 0, 18, 255))

            # Yellow block (Bottom-Right 1)
            draw.rectangle([x_split, y_right_split, x_sub_split, y0 + h], fill=(255, 221, 0, 255))

            # Black block (Bottom-Right 2)
            draw.rectangle([x_sub_split, y_right_split, x0 + w, y0 + h], fill=(10, 10, 10, 255))

            # Bottom-Left Paper with Lines
            draw.rectangle([x0, y_left_split, x_split, y0 + h], fill=(250, 250, 249, 255))
            line_w = max(1, int(size * 0.015))
            if size >= 64:
                draw.line([(x0 + int(w * 0.08), y_left_split + int(h * 0.12)), (x_split - int(w * 0.08), y_left_split + int(h * 0.12))], fill=(10, 10, 10, 255), width=line_w)
                draw.line([(x0 + int(w * 0.08), y_left_split + int(h * 0.22)), (x_split - int(w * 0.15), y_left_split + int(h * 0.22))], fill=(10, 10, 10, 255), width=line_w)

            # Play Arrow in Red Block
            rw = x0 + w - x_split
            rh = y_right_split - y0
            tri_h = int(rh * 0.50)
            tri_w = int(tri_h * 0.85)
            cx = x_split + rw // 2 + int(tri_w * 0.1)
            cy = y0 + rh // 2
            tri_pts = [
                (cx - tri_w // 2, cy - tri_h // 2),
                (cx - tri_w // 2, cy + tri_h // 2),
                (cx + tri_w // 2, cy),
            ]
            draw.polygon(tri_pts, fill=(250, 250, 249, 255), outline=(10, 10, 10, 255))

            # Mondrian Grid lines
            grid_w = max(2, int(size * 0.024))
            draw.line([(x_split, y0), (x_split, y0 + h)], fill=(10, 10, 10, 255), width=grid_w)
            draw.line([(x0, y_left_split), (x_split, y_left_split)], fill=(10, 10, 10, 255), width=grid_w)
            draw.line([(x_split, y_right_split), (x0 + w, y_right_split)], fill=(10, 10, 10, 255), width=grid_w)
            draw.line([(x_sub_split, y_right_split), (x_sub_split, y0 + h)], fill=(10, 10, 10, 255), width=grid_w)

            # Redraw outer border
            draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=rx, fill=None, outline=(10, 10, 10, 255), width=border_w)

        else:
            # Mark with Typography at Bottom
            top_h = int(size * 0.68)
            m = max(3, int(size * 0.06))
            w = size - 2 * m
            h = top_h - m

            x_split = m + int(w * 0.40)
            y_left_split = m + int(h * 0.65)
            y_right_split = m + int(h * 0.68)
            x_sub_split = x_split + int((w - int(w * 0.40)) * 0.52)

            # Blue block
            draw.rectangle([m, m, x_split, y_left_split], fill=(0, 71, 171, 255))
            # Red block
            draw.rectangle([x_split, m, m + w, y_right_split], fill=(230, 0, 18, 255))
            # Yellow block
            draw.rectangle([x_split, y_right_split, x_sub_split, m + h], fill=(255, 221, 0, 255))
            # Black block
            draw.rectangle([x_sub_split, y_right_split, m + w, m + h], fill=(10, 10, 10, 255))
            # Bottom-left paper
            draw.rectangle([m, y_left_split, x_split, m + h], fill=(250, 250, 249, 255))

            # Play Arrow
            rw = m + w - x_split
            rh = y_right_split - m
            tri_h = int(rh * 0.48)
            tri_w = int(tri_h * 0.85)
            cx = x_split + rw // 2 + int(tri_w * 0.1)
            cy = m + rh // 2
            tri_pts = [
                (cx - tri_w // 2, cy - tri_h // 2),
                (cx - tri_w // 2, cy + tri_h // 2),
                (cx + tri_w // 2, cy),
            ]
            draw.polygon(tri_pts, fill=(250, 250, 249, 255), outline=(10, 10, 10, 255))

            # Grid lines inside top panel
            grid_w = max(2, int(size * 0.02))
            draw.line([(x_split, m), (x_split, m + h)], fill=(10, 10, 10, 255), width=grid_w)
            draw.line([(m, y_left_split), (x_split, y_left_split)], fill=(10, 10, 10, 255), width=grid_w)
            draw.line([(x_split, y_right_split), (m + w, y_right_split)], fill=(10, 10, 10, 255), width=grid_w)
            draw.line([(x_sub_split, y_right_split), (x_sub_split, m + h)], fill=(10, 10, 10, 255), width=grid_w)
            draw.rectangle([m, m, m + w, m + h], fill=None, outline=(10, 10, 10, 255), width=grid_w)

            # Divider line above text
            draw.line([(m, int(size * 0.72)), (m + w, int(size * 0.72))], fill=(10, 10, 10, 255), width=grid_w)

            # Typography
            if size >= 128:
                font_title = load_font(max(10, int(size * 0.08)), black=True)
                font_by = load_font(max(7, int(size * 0.048)), black=True)
                t_pay = "PAY"
                t_by = " -BY- "
                t_play = "PLAY"
                bb_pay = draw.textbbox((0, 0), t_pay, font=font_title)
                bb_by = draw.textbbox((0, 0), t_by, font=font_by)
                bb_play = draw.textbbox((0, 0), t_play, font=font_title)
                w_pay = bb_pay[2] - bb_pay[0]
                w_by = bb_by[2] - bb_by[0]
                w_play = bb_play[2] - bb_play[0]
                total_tw = w_pay + w_by + w_play
                tx = (size - total_tw) // 2
                ty = int(size * 0.81)
                by_y_offset = (bb_pay[3] - bb_pay[1] - (bb_by[3] - bb_by[1])) // 2

                draw.text((tx, ty), t_pay, fill=(10, 10, 10, 255), font=font_title)
                draw.text((tx + w_pay, ty + by_y_offset), t_by, fill=(113, 113, 122, 255), font=font_by)
                draw.text((tx + w_pay + w_by, ty), t_play, fill=(230, 0, 18, 255), font=font_title)

                if size >= 256:
                    font_sub = load_font(max(8, int(size * 0.03)), black=False)
                    sub_text = "WOMEN'S PRO SPORTS ECONOMETRICS"
                    bb_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
                    sw = bb_sub[2] - bb_sub[0]
                    draw.text(((size - sw) // 2, int(size * 0.91)), sub_text, fill=(113, 113, 122, 255), font=font_sub)

        img.save(path, "PNG")
        print(f"Rendered PNG: {path} ({size}x{size})")

    # Wide banner 1280x512
    banner = Image.new("RGBA", (1280, 512), (250, 250, 249, 255))
    icon_src = ASSETS / "logo-icon-256.png"
    if not icon_src.exists():
        icon_src = ASSETS / "logo-icon-128.png"
    icon_512 = Image.open(icon_src)
    icon_scaled = icon_512.resize((380, 380), Image.Resampling.LANCZOS)
    banner.paste(icon_scaled, (66, 66), icon_scaled)

    draw_b = ImageDraw.Draw(banner)
    f_badge = load_font(14, black=True)
    f_title = load_font(64, black=True)
    f_hook = load_font(26, black=True)
    f_desc = load_font(18, black=False)
    f_code = load_font(15, black=True)

    # Badges
    bx = 500
    by = 70
    draw_b.rounded_rectangle([bx, by, bx + 70, by + 26], radius=5, fill=(10, 10, 10, 255))
    draw_b.text((bx + 14, by + 5), "PWHL", fill=(255, 255, 255, 255), font=f_badge)

    draw_b.rounded_rectangle([bx + 80, by, bx + 155, by + 26], radius=5, fill=(230, 0, 18, 255))
    draw_b.text((bx + 94, by + 5), "WNBA", fill=(255, 255, 255, 255), font=f_badge)

    draw_b.rounded_rectangle([bx + 165, by, bx + 235, by + 26], radius=5, fill=(0, 71, 171, 255))
    draw_b.text((bx + 182, by + 5), "WPL", fill=(255, 255, 255, 255), font=f_badge)

    draw_b.text((bx + 250, by + 5), "· CROSS-LEAGUE DECISION SUPPORT", fill=(113, 113, 122, 255), font=f_desc)

    # Title
    t_y = 120
    t_pay = "PAY"
    t_by = " -BY- "
    t_play = "PLAY"
    f_by = load_font(38, black=True)
    bb_pay = draw_b.textbbox((0, 0), t_pay, font=f_title)
    bb_by = draw_b.textbbox((0, 0), t_by, font=f_by)
    bb_play = draw_b.textbbox((0, 0), t_play, font=f_title)
    w_pay = bb_pay[2] - bb_pay[0]
    w_by = bb_by[2] - bb_by[0]
    w_play = bb_play[2] - bb_play[0]
    by_y_offset = (bb_pay[3] - bb_pay[1] - (bb_by[3] - bb_by[1])) // 2

    draw_b.text((bx, t_y), t_pay, fill=(10, 10, 10, 255), font=f_title)
    draw_b.text((bx + w_pay, t_y + by_y_offset), t_by, fill=(113, 113, 122, 255), font=f_by)
    draw_b.text((bx + w_pay + w_by, t_y), t_play, fill=(230, 0, 18, 255), font=f_title)

    # De Stijl rule bar
    ry = 215
    draw_b.rectangle([bx, ry, bx + 200, ry + 6], fill=(0, 71, 171, 255))
    draw_b.rectangle([bx + 206, ry, bx + 260, ry + 6], fill=(255, 221, 0, 255))
    draw_b.rectangle([bx + 266, ry, bx + 640, ry + 6], fill=(230, 0, 18, 255))

    # Hook
    draw_b.text((bx, 250), "Does pay follow play?", fill=(10, 10, 10, 255), font=f_hook)
    draw_b.text((bx, 295), "Empirical Bayes value estimation · Two lenses on contract timing · Fairness metrics", fill=(113, 113, 122, 255), font=f_desc)
    draw_b.text((bx, 340), "gap = value_pct − pay_pct  (Within-league position percentiles)", fill=(10, 10, 10, 255), font=f_code)

    banner.save(ASSETS / "logo-wordmark-1280.png", "PNG")
    print(f"Rendered Banner: {ASSETS / 'logo-wordmark-1280.png'}")


if __name__ == "__main__":
    export_svgs()
    render_all_pngs()
