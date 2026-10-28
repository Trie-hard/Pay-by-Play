# Pay-by-Play glossary

| Term | Meaning |
|------|---------|
| **pay_raw** | Disclosed compensation in local currency (base salary or auction price). Bonuses and benefits are excluded unless noted. |
| **pay_pct** | Within-league, within-position percentile rank of pay (0–100). |
| **value_raw** | Sport-specific production composite before shrinkage. |
| **value_shrunk** | Empirical Bayes estimate shrunk toward position mean: μ + B·(V_obs − μ). |
| **gap** | value_pct − pay_pct. Positive ⇒ underpaid relative to peers at the same position. |
| **Lens A (pay rationality)** | Current pay vs prior-season value. |
| **Lens B (return on pay)** | Current pay vs current-season value. |
| **Lens gap** | Difference between Lens B and Lens A gaps — how much teams guessed on breakouts/slumps. |
| **Within-league fairness** | Spearman correlation between pay rank and value rank inside one league (not cross-currency). |
| **Misallocation index** | Share of payroll that would need to move so pay shares match value shares. |
| **Replacement level** | 20th percentile of regulars at position. |
| **Confident bargain** | Bootstrap 80% CI for gap strictly above zero, enough games, no blocking data_flags. |
