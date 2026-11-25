# MR-001-01 — Liquidity reversal: verdict for review

The recorded verdict is **fails gate 2, economic edge**, under threshold version 4. This is a capstone verdict document, not a lab verdict.md. All later gates were evaluated.

## Gate by gate

1. Hygiene — PASS. The report has 205 clustered decisions over 17.83 evaluated years. It finds no look-ahead or same-day break on 100 checked dates and no memory break on 50 memory-check dates. Declared memory is 32 sessions; no data problem is reported.

2. Economic edge — FAIL. Sharpe is 0.24, below 0.40 and benchmark 0.45. Annual alpha is -1.07%. At doubled costs, Sharpe is 0.21 and alpha -1.36%. The failure concerns benchmark-relative economics before later testing adjustments.

3. Significance — FAIL. PSR is 0.87 against 0.95 required. The base beats 37.10% of 1,000 shifted placebos, below 90.00%. The blend's separate rank is 34.60%; it does not replace the base metric.

4. Multiple testing — FAIL. DSR is below 0.01 against 0.90 required, across 79 effective trials from 86 registered trials. Appraisal ratio is -0.20. The DSR is small, not exactly zero.

5. Stability — FAIL. The blend fails gates 2, 3 and 4. Alpha is positive in two of five calendar blocks, below three required. Removing the best year, 2015, leaves annual alpha -1.63%.

6. Robustness — FAIL. GLD carries 32.88% of P&L, above 30.00%. Other recorded checks retain 128.20% of base Sharpe at the neighbour median, 66.41% at the lowest nearby setting, 68.55% without the metals cluster and 122.70% with a one-day delay. Those tolerances do not cancel the concentration failure.

7. Sealed holdout — PASS. Published 2023–2025 Sharpe is 0.90 and annual alpha 1.06%, above respective floors -0.46 and -4.50%. No variant is rewritten and no timing break occurs on 20 checked dates. I use only this saved lab output; I compute no additional holdout statistic. The pass does not reverse the economic failure.

## Refutation and lessons

The card's nonpositive-alpha condition is met in-sample. Its placebo requirement and concentration condition also fail. The hypothesis does not validate on these funds under this implementation. Its positive holdout alpha is reported without changing the verdict.

The diagnostic motivated reducing estimation freedom after the original price-only learners produced negative R² and Elastic Net collapsed to a pooled intercept. It did not demonstrate reversal in advance. This new economic mechanism is a rule-based follow-up, not a successful revised ML specification or a causal identification of liquidity provision.

The lab record preserves a card-only lock before code, one run, an isolated registry commit and a separate report commit. The new design did not use further holdout calculations, but the earlier 06–08 holdout outputs were already known. The follow-up is exploratory and cannot claim a globally unseen calendar holdout.

I stop after this single additional card and keep the code unchanged. The side-by-side comparison remains descriptive: the reference's missing historical commit prevents the official paired comparison, and effective windows differ.

Source for every numerical gate statement: alpha-lab/strategies/MR-001-01-monthly-liquidity-reversal/report.ipynb, cells 10, 12, 14, 16, 18, 20, 22 and 24. Design rationale: its card.yaml and reasoning.md; diagnostic sources: capstone/diagnostics/summary.json and associated CSV files. Full table and figure provenance is in capstone/results-notes.md.
