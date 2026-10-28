"""Export Pay-by-Play logos (SVGs and PNGs). Run from repo root."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_all_logos import export_svgs, render_all_pngs

def main() -> None:
    export_svgs()
    render_all_pngs()
    print("Successfully exported all Pay-by-Play SVGs and PNGs to assets/")

if __name__ == "__main__":
    main()
