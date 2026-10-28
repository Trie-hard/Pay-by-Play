"""Minimal page chrome — single hero block."""

from __future__ import annotations

import pandas as pd

from app.brand import BRAND_TAGLINE, GAP_FORMULA


def top_chrome_html(
    pwhl: pd.DataFrame,
    wnba: pd.DataFrame,
    wpl: pd.DataFrame,
) -> str:
    n_wnba = len(wnba) if not wnba.empty else 0
    n_wpl = len(wpl) if not wpl.empty else 0
    total = len(pwhl) + n_wnba + n_wpl
    league_bits = []
    if len(pwhl):
        league_bits.append(f"PWHL {len(pwhl)}")
    if n_wnba:
        league_bits.append(f"WNBA {n_wnba}")
    if n_wpl:
        league_bits.append(f"WPL {n_wpl}")
    roster_line = " · ".join(league_bits) if league_bits else "—"

    return f"""
    <div class="dstijl-hero">
      <div class="dstijl-hero-grid" aria-hidden="true">
        <span></span><span></span><span></span><span></span>
      </div>
      <h1 class="dstijl-title">
        <span class="dstijl-pay">PAY</span><span class="dstijl-by">-BY-</span><span class="dstijl-play">PLAY</span>
      </h1>
      <p class="lede">{BRAND_TAGLINE}</p>
      <p class="dstijl-meta">{total} players · {roster_line}</p>
    </div>
    """


def home_tab_html() -> str:
    return f"""
    <section class="dstijl-home">
      <p class="dstijl-home-hook">
        Does pay follow play—and does the pay <em>structure</em> change the answer?
      </p>

      <div class="dstijl-home-split">
        <div class="dstijl-home-prose">
          <h2 class="dstijl-home-h">What Pay-by-Play is</h2>
          <p>
            A decision-support layer for women&rsquo;s pro leagues where compensation is public enough
            to analyze honestly. We line up <strong>disclosed pay</strong> with <strong>on-field production</strong>
            inside each league and position—PWHL salary bands, WNBA cap tiers, WPL auction prices.
          </p>
          <p>
            This is not a cross-currency &ldquo;who earns the most worldwide&rdquo; table. Dollar amounts
            stay in context; ranks and gaps do the work.
          </p>
        </div>
        <aside class="dstijl-home-aside">
          <span class="dstijl-home-aside-label">Core metric</span>
          <p class="dstijl-home-formula">{GAP_FORMULA}</p>
          <p class="dstijl-home-aside-body">
            Both ranks are percentiles within the same league and position.
            A <strong>positive gap</strong> means production outruns the paycheck—your raise case
            (within-league position percentiles).
          </p>
        </aside>
      </div>

      <h2 class="dstijl-home-h">How players are scored</h2>
      <ol class="dstijl-home-steps">
        <li class="dstijl-home-step dstijl-home-step--red">
          <span class="dstijl-home-step-n">1</span>
          <span><strong>Ingest</strong> published pay and game-level stats with league-specific rules.</span>
        </li>
        <li class="dstijl-home-step dstijl-home-step--blue">
          <span class="dstijl-home-step-n">2</span>
          <span><strong>Shrink</strong> raw value with empirical Bayes toward position means—stabilize small samples.</span>
        </li>
        <li class="dstijl-home-step dstijl-home-step--yellow">
          <span class="dstijl-home-step-n">3</span>
          <span><strong>Rank</strong> pay and value; bootstrap gaps where data allow <em>confident bargains</em>.</span>
        </li>
        <li class="dstijl-home-step dstijl-home-step--ink">
          <span class="dstijl-home-step-n">4</span>
          <span><strong>Explore</strong> fairness ρ, maps, raise radar, two lenses, and PWHL roster math.</span>
        </li>
      </ol>

      <h2 class="dstijl-home-h">Two lenses on timing</h2>
      <div class="dstijl-home-lenses">
        <div class="dstijl-home-lens">
          <span class="dstijl-home-lens-tag">Lens A</span>
          <p><strong>Pay rationality</strong> — current pay vs <em>prior-season</em> value (did last year earn this contract?).</p>
        </div>
        <div class="dstijl-home-lens">
          <span class="dstijl-home-lens-tag">Lens B</span>
          <p><strong>Return on pay</strong> — current pay vs <em>current-season</em> value (are you delivering now?).</p>
        </div>
      </div>
      <p class="dstijl-home-note">
        The difference between lenses shows how much teams are betting on breakouts and slumps—not just last year&rsquo;s box score.
      </p>

      <h2 class="dstijl-home-h">Where to go in the app</h2>
      <div class="dstijl-home-tour">
        <div class="dstijl-home-tile">
          <span class="dstijl-home-tile-tab">Scoreboard</span>
          <p>League-level fairness ρ, bargain counts, and hypothesis checks (draft, raises).</p>
        </div>
        <div class="dstijl-home-tile">
          <span class="dstijl-home-tile-tab">Explorer</span>
          <p>Click a city on the map; scatter pay vs value for that market.</p>
        </div>
        <div class="dstijl-home-tile">
          <span class="dstijl-home-tile-tab">Raise radar</span>
          <p>Dumbbell view of who is most underpaid relative to production.</p>
        </div>
        <div class="dstijl-home-tile">
          <span class="dstijl-home-tile-tab">Two lenses</span>
          <p>Histogram of lens deltas—who gained or lost on the timing bet.</p>
        </div>
        <div class="dstijl-home-tile">
          <span class="dstijl-home-tile-tab">Roster lab</span>
          <p>PWHL-only: pick a team and solve a roster under the salary band.</p>
        </div>
        <div class="dstijl-home-tile">
          <span class="dstijl-home-tile-tab">Methods</span>
          <p>Glossary, data sources, and why NWSL is out of scope for scoring.</p>
        </div>
      </div>

      <div class="dstijl-home-leagues" aria-label="Leagues covered">
        <div class="dstijl-home-league dstijl-home-league--pwhl"><strong>PWHL</strong><span>Salary guide · core</span></div>
        <div class="dstijl-home-league dstijl-home-league--wnba"><strong>WNBA</strong><span>Cap tiers · live</span></div>
        <div class="dstijl-home-league dstijl-home-league--wpl"><strong>WPL</strong><span>Auction · stretch</span></div>
        <div class="dstijl-home-league dstijl-home-league--nwsl"><strong>NWSL</strong><span>Methods only — sparse public pay</span></div>
      </div>
    </section>
    """
