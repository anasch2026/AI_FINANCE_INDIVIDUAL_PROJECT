# TM-017-10 — Volatility-weighted trend: verdict for review

**First failure: gate 3, significance**, threshold version 4. This new user-fixed card repairs only the missing-volatility membership of unrun TM-017-09, which remains unchanged and has no financial result. Earlier holdouts were already seen and disclosed. TM-017-10 ran once after its card-only lock and successful preflight.

## Gate by gate

1. Hygiene — PASS. The report has 203 clustered decisions over 16.90 years, no timing or same-day break on 100 dates, and no memory break on 50 memory-check dates. Memory is 400 sessions. Effective evaluation starts 2006-02-02.

2. Economic edge — PASS. Sharpe is 0.61 against benchmark 0.41; annual alpha is 2.16%. At doubled costs, Sharpe is 0.59 and alpha 2.08%. The recorded economic criterion is met without changing the prescribed rule.

3. Significance — FAIL. The base beats 89.80% of 1,000 shifted placebos, below 90.00%. Its PSR rounds to 1.00, but this does not offset the failed placebo requirement or imply certainty. The separately published blend rank is 88.60%.

4. Multiple testing — FAIL. DSR is 0.27 against 0.90 required, across 81 effective trials from 88 registered trials. The appraisal ratio is 0.46. The additional trial is retained in the accumulated search record.

5. Stability — FAIL. The blend passes gate 2 but fails gates 3 and 4. All five predefined blocks have positive alpha. Removing the best year, 2008, leaves annual alpha 0.92%; those favourable episode checks do not cancel the blend failures.

6. Robustness — PASS. Median neighbour retention is 96.54%, lowest nearby retention 86.51%, worst cluster removal (bonds) retention 68.97%, and one-day delay retention 99.39%. SPY supplies the largest profit share at 28.55%, below the cap. No neighbour leaves targets identical to the base.

7. Sealed holdout — PASS. Published holdout Sharpe is 0.79 and annual alpha -0.02%, above floors -0.11 and -1.51%. No variant is rewritten and no timing break occurs on 20 checked dates. Only saved lab figures are used; no additional holdout calculation is made.

## What was learned

The repaired sizing is executable and meets the recorded economic and robustness criteria. Its significance, multiple-testing and blend-stability requirements still fail. Passing gate 6 is a concrete result, but different historical threshold versions and the unavailable official paired comparison prevent a causal or statistical claim about improvement over TM-017-01. No homemade paired test is substituted.

The positive-alpha refutation condition is not met, but the required significance and later validation conditions are not cleared. The verdict remains gate 3. Being close to the placebo cutoff is not permission to lower it or try another setting. The holdout's slightly negative alpha and the failed DSR remain visible alongside the favourable in-sample economics. No new card, change or rerun follows this result. The diagnostic expansion evaluates forecasts only and is not an additional portfolio trial.

Sources: alpha-lab/strategies/TM-017-10-volatility-weighted-trend/report.ipynb, cells 4 and 10–24; its locked card.yaml, reasoning.md and strategy.py; STOPPED.md for the preserved TM-017-09 preflight history and unavailable paired comparison. All financial figures are the notebook's, rounded to two decimals.
