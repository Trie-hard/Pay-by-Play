# Pay-by-Play — Brand Identity & Specification Document

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
| **The Gap** | `#FFDD00` (Canary Yellow) | The surplus metric ($gap = value\_pct - pay\_pct$), highlighting confident bargains and raise cases. |
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
