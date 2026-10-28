"""Build the interactive logo showcase HTML artifact."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_all_logos import (
    create_svg_icon,
    create_svg_icon_dark,
    create_svg_logo_mark,
    create_svg_wordmark,
    create_svg_emblem_lenses,
)

brain_dir = Path(r"C:\Users\niksh\.gemini\antigravity\brain\9b4f118f-afd8-468f-b00a-67b10efef7a9")
svg_icon = create_svg_icon()
svg_icon_dark = create_svg_icon_dark()
svg_mark = create_svg_logo_mark()
svg_wordmark = create_svg_wordmark()
svg_emblem = create_svg_emblem_lenses()

html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pay-by-Play Brand Identity &amp; Logo System</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .de-stijl-grid {{
      background-image: linear-gradient(to right, rgba(0,0,0,0.06) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(0,0,0,0.06) 1px, transparent 1px);
      background-size: 24px 24px;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen p-4 md:p-8">

  <!-- Header -->
  <header class="max-w-6xl mx-auto mb-8 border-b border-zinc-800 pb-6 flex flex-wrap items-center justify-between gap-4">
    <div>
      <div class="flex items-center gap-3 mb-2">
        <span class="px-2 py-0.5 text-xs font-mono font-bold bg-[#E60012] text-white rounded">v1.2</span>
        <span class="px-2 py-0.5 text-xs font-mono bg-[#0047AB] text-white rounded">DE STIJL MODERNISM</span>
        <span class="px-2 py-0.5 text-xs font-mono bg-[#FFDD00] text-black font-semibold rounded">PRODUCTION READY</span>
      </div>
      <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight">
        Pay-by-Play <span class="text-zinc-400 text-2xl font-normal">· Brand System</span>
      </h1>
      <p class="text-sm text-zinc-400 mt-1">
        Cross-league econometrics &amp; decision support for women's pro sports (PWHL, WNBA, WPL).
      </p>
    </div>

    <!-- Mode Selector -->
    <div class="flex items-center gap-2 bg-zinc-900 border border-zinc-800 p-1.5 rounded-lg text-xs font-mono">
      <button onclick="setPreviewBg('light')" id="btn-light" class="px-3 py-1.5 rounded font-bold transition hover:bg-zinc-800">Paper Light</button>
      <button onclick="setPreviewBg('dark')" id="btn-dark" class="px-3 py-1.5 rounded font-bold bg-[#E60012] text-white transition">Slate Dark</button>
      <button onclick="setPreviewBg('grid')" id="btn-grid" class="px-3 py-1.5 rounded font-bold transition hover:bg-zinc-800">Mondrian Grid</button>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-6xl mx-auto space-y-12">

    <!-- Section 1: Hero Showcase -->
    <section>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold flex items-center gap-2">
          <span class="w-3 h-3 bg-[#E60012] inline-block"></span>
          Primary Identity &amp; App Icon
        </h2>
        <span class="text-xs font-mono text-zinc-400">assets/logo-icon.svg · assets/logo-mark.svg</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Card 1: App Icon (Square) -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 flex flex-col items-center justify-between shadow-lg">
          <div class="w-full flex justify-between items-center mb-4 text-xs font-mono text-zinc-400">
            <span>APP ICON / FAVICON</span>
            <span>512 × 512</span>
          </div>
          <div id="preview-box-1" class="p-6 rounded-2xl transition duration-200 bg-[#FAFAF9] flex items-center justify-center w-56 h-56 shadow-md">
            <div class="w-44 h-44 drop-shadow-sm">
              {svg_icon}
            </div>
          </div>
          <div class="w-full mt-6 flex gap-2">
            <button onclick="copySvg('icon')" class="w-full py-2 px-3 text-xs font-mono font-bold bg-zinc-950 hover:bg-[#0047AB] hover:text-white border border-zinc-800 rounded-lg transition">
              📋 Copy SVG
            </button>
          </div>
        </div>

        <!-- Card 2: Primary Logo Mark (with Typography) -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 flex flex-col items-center justify-between shadow-lg">
          <div class="w-full flex justify-between items-center mb-4 text-xs font-mono text-zinc-400">
            <span>COMPLETE LOGO MARK</span>
            <span>512 × 512</span>
          </div>
          <div id="preview-box-2" class="p-6 rounded-2xl transition duration-200 bg-[#FAFAF9] flex items-center justify-center w-56 h-56 shadow-md">
            <div class="w-44 h-44 drop-shadow-sm">
              {svg_mark}
            </div>
          </div>
          <div class="w-full mt-6 flex gap-2">
            <button onclick="copySvg('mark')" class="w-full py-2 px-3 text-xs font-mono font-bold bg-zinc-950 hover:bg-[#E60012] hover:text-white border border-zinc-800 rounded-lg transition">
              📋 Copy SVG
            </button>
          </div>
        </div>

        <!-- Card 3: Two Lenses Stadium Emblem -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 flex flex-col items-center justify-between shadow-lg">
          <div class="w-full flex justify-between items-center mb-4 text-xs font-mono text-zinc-400">
            <span>TWO LENSES EMBLEM</span>
            <span>512 × 512</span>
          </div>
          <div id="preview-box-3" class="p-6 rounded-2xl transition duration-200 bg-[#FAFAF9] flex items-center justify-center w-56 h-56 shadow-md">
            <div class="w-44 h-44 drop-shadow-sm">
              {svg_emblem}
            </div>
          </div>
          <div class="w-full mt-6 flex gap-2">
            <button onclick="copySvg('emblem')" class="w-full py-2 px-3 text-xs font-mono font-bold bg-zinc-950 hover:bg-[#FFDD00] hover:text-black border border-zinc-800 rounded-lg transition">
              📋 Copy SVG
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 2: Wide Header Banner & Social Card -->
    <section>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold flex items-center gap-2">
          <span class="w-3 h-3 bg-[#0047AB] inline-block"></span>
          Full Banner &amp; Wordmark Lockup
        </h2>
        <span class="text-xs font-mono text-zinc-400">assets/logo-wordmark.svg · 1280 × 512</span>
      </div>

      <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-lg">
        <div id="preview-box-banner" class="p-4 rounded-xl transition duration-200 bg-[#FAFAF9] overflow-hidden flex items-center justify-center">
          <div class="w-full max-w-4xl">
            {svg_wordmark}
          </div>
        </div>
        <div class="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
          <span class="text-zinc-400">Perfect for GitHub README, OpenGraph cards, Streamlit home banner &amp; presentation decks.</span>
          <button onclick="copySvg('wordmark')" class="py-1.5 px-4 font-bold bg-zinc-950 hover:bg-[#0047AB] hover:text-white border border-zinc-800 rounded-lg transition">
            📋 Copy Banner SVG
          </button>
        </div>
      </div>
    </section>

    <!-- Section 3: In-Context Applications Mockups -->
    <section>
      <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
        <span class="w-3 h-3 bg-[#FFDD00] inline-block"></span>
        Live Context Mockups
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Mockup A: Browser Tab & Streamlit Top Bar -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div class="text-xs font-mono text-zinc-400">STREAMLIT TAB &amp; APP HEADER</div>
          <div class="bg-zinc-950 border border-zinc-800 rounded-xl overflow-hidden shadow-md">
            <!-- Browser chrome -->
            <div class="bg-zinc-900 px-4 py-2 flex items-center gap-2 border-b border-zinc-800">
              <div class="flex gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-red-500 inline-block"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-yellow-500 inline-block"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-green-500 inline-block"></span>
              </div>
              <!-- Tab -->
              <div class="ml-4 bg-zinc-950 px-3 py-1 rounded-t flex items-center gap-2 text-xs font-semibold text-white">
                <div class="w-4 h-4">{svg_icon}</div>
                <span>Pay-by-Play</span>
              </div>
            </div>
            <!-- Streamlit Hero snippet -->
            <div class="p-6 bg-[#0A0A0A] text-white flex items-center gap-4">
              <div class="w-12 h-12 flex-shrink-0">{svg_icon}</div>
              <div>
                <h3 class="text-lg font-black tracking-wider">
                  <span class="text-[#F5F5F5]">PAY</span><span class="text-[#71717A]">-BY-</span><span class="text-[#FF3333]">PLAY</span>
                </h3>
                <p class="text-xs text-zinc-400">Does pay follow play—and does pay structure change the answer?</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Mockup B: Multi-Size Scalability Test -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div class="text-xs font-mono text-zinc-400">SCALABILITY &amp; LEGIBILITY TEST</div>
          <div class="bg-zinc-950 border border-zinc-800 rounded-xl p-6 flex items-end justify-around gap-4 min-h-[140px]">
            <!-- 16px -->
            <div class="text-center space-y-1">
              <div class="w-4 h-4 mx-auto rounded-sm overflow-hidden">{svg_icon}</div>
              <span class="text-[10px] font-mono text-zinc-400">16px</span>
            </div>
            <!-- 24px -->
            <div class="text-center space-y-1">
              <div class="w-6 h-6 mx-auto rounded-sm overflow-hidden">{svg_icon}</div>
              <span class="text-[10px] font-mono text-zinc-400">24px</span>
            </div>
            <!-- 32px -->
            <div class="text-center space-y-1">
              <div class="w-8 h-8 mx-auto rounded overflow-hidden">{svg_icon}</div>
              <span class="text-[10px] font-mono text-zinc-400">32px (Favicon)</span>
            </div>
            <!-- 48px -->
            <div class="text-center space-y-1">
              <div class="w-12 h-12 mx-auto rounded-md overflow-hidden">{svg_icon}</div>
              <span class="text-[10px] font-mono text-zinc-400">48px (Dock)</span>
            </div>
            <!-- 64px -->
            <div class="text-center space-y-1">
              <div class="w-16 h-16 mx-auto rounded-lg overflow-hidden">{svg_icon}</div>
              <span class="text-[10px] font-mono text-zinc-400">64px (Avatar)</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 4: Brand Architecture & Palette Tokens -->
    <section>
      <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
        <span class="w-3 h-3 bg-white inline-block"></span>
        Design System Color Tokens
      </h2>

      <div class="grid grid-cols-2 md:grid-cols-5 gap-4 font-mono text-xs">
        <!-- Blue -->
        <div onclick="navigator.clipboard.writeText('#0047AB'); alert('Copied #0047AB');" class="cursor-pointer bg-[#0047AB] text-white p-4 rounded-xl flex flex-col justify-between h-28 shadow transition transform hover:-translate-y-1">
          <span class="font-bold">De Stijl Blue</span>
          <div>
            <div class="font-bold">#0047AB</div>
            <div class="text-[10px] opacity-80">Pay / Contract Stability</div>
          </div>
        </div>

        <!-- Red -->
        <div onclick="navigator.clipboard.writeText('#E60012'); alert('Copied #E60012');" class="cursor-pointer bg-[#E60012] text-white p-4 rounded-xl flex flex-col justify-between h-28 shadow transition transform hover:-translate-y-1">
          <span class="font-bold">De Stijl Red</span>
          <div>
            <div class="font-bold">#E60012</div>
            <div class="text-[10px] opacity-80">Play / On-Field Action</div>
          </div>
        </div>

        <!-- Yellow -->
        <div onclick="navigator.clipboard.writeText('#FFDD00'); alert('Copied #FFDD00');" class="cursor-pointer bg-[#FFDD00] text-black p-4 rounded-xl flex flex-col justify-between h-28 shadow transition transform hover:-translate-y-1">
          <span class="font-bold">Canary Yellow</span>
          <div>
            <div class="font-bold">#FFDD00</div>
            <div class="text-[10px] opacity-80">Surplus / Value Gap</div>
          </div>
        </div>

        <!-- Ink -->
        <div onclick="navigator.clipboard.writeText('#0A0A0A'); alert('Copied #0A0A0A');" class="cursor-pointer bg-[#0A0A0A] text-white border border-zinc-700 p-4 rounded-xl flex flex-col justify-between h-28 shadow transition transform hover:-translate-y-1">
          <span class="font-bold">Structural Ink</span>
          <div>
            <div class="font-bold">#0A0A0A</div>
            <div class="text-[10px] opacity-80">Architectural Grids</div>
          </div>
        </div>

        <!-- Paper -->
        <div onclick="navigator.clipboard.writeText('#FAFAF9'); alert('Copied #FAFAF9');" class="cursor-pointer bg-[#FAFAF9] text-zinc-900 p-4 rounded-xl flex flex-col justify-between h-28 shadow transition transform hover:-translate-y-1">
          <span class="font-bold">Paper White</span>
          <div>
            <div class="font-bold">#FAFAF9</div>
            <div class="text-[10px] opacity-80">Clean Negative Space</div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Script for interactivity -->
  <script>
    const svgs = {{
      icon: `{svg_icon.replace("`", "\\`")}`,
      mark: `{svg_mark.replace("`", "\\`")}`,
      wordmark: `{svg_wordmark.replace("`", "\\`")}`,
      emblem: `{svg_emblem.replace("`", "\\`")}`
    }};

    function copySvg(key) {{
      if (svgs[key]) {{
        navigator.clipboard.writeText(svgs[key]).then(() => {{
          alert('SVG code copied to clipboard!');
        }});
      }}
    }}

    function setPreviewBg(mode) {{
      const boxes = ['preview-box-1', 'preview-box-2', 'preview-box-3', 'preview-box-banner'];
      const btns = ['btn-light', 'btn-dark', 'btn-grid'];

      btns.forEach(b => document.getElementById(b).classList.remove('bg-[#E60012]', 'text-white'));
      document.getElementById('btn-' + mode).classList.add('bg-[#E60012]', 'text-white');

      boxes.forEach(id => {{
        const el = document.getElementById(id);
        el.className = el.className.replace(/bg-\\[.*?\\]|bg-zinc-950|de-stijl-grid/g, '');
        if (mode === 'light') {{
          el.classList.add('bg-[#FAFAF9]');
        }} else if (mode === 'dark') {{
          el.classList.add('bg-zinc-950');
        }} else if (mode === 'grid') {{
          el.classList.add('bg-[#FAFAF9]', 'de-stijl-grid');
        }}
      }});
    }}
  </script>
</body>
</html>"""

out_path = brain_dir / "logo_showcase.html"
out_path.write_text(html, encoding="utf-8")
print(f"Wrote showcase HTML: {out_path}")
