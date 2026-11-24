# TM-017-08 — Gradient Boosting: draft verdict

Draft for Anas's review; this is not the lab's verdict.md. The recorded verdict is **fails gate 2, economic edge**. All later gates were evaluated. Threshold version: 4.

<!-- Source for verdict, all gate labels and version: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cells 0 and 24. -->

## Gate by gate

1. Hygiene — PASS. The report counts 122 clustered decisions over 11.90 evaluated years. There are no look-ahead or same-day breaks on 100 checked dates, or memory breaks on 50 memory-check dates; memory is 2,400 sessions and no data problem is reported.

<!-- Source: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cell 10. -->

2. Economic edge — FAIL. Sharpe is 0.09, below required 0.40 and benchmark 0.39, with annual alpha -1.90%. At doubled costs, the report's gate summary gives Sharpe 0.07 and alpha -2.07%. These are unfavourable economic results independently of later selection adjustments.

<!-- Source: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cell 12 for base figures and cell 24 for the doubled-cost alpha as published in the gate summary. -->

3. Significance — FAIL. PSR is 0.65 against 0.95 required. The base strategy beats 1.80% of 1,000 shifted placebos, short of 90.00%. The blend's separately reported rank is 0.90%; the base rank is retained in the results table.

<!-- Source: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cells 14, 18 and 24. -->

4. Multiple testing — FAIL. DSR is below 0.01, against required 0.90, with 85 registered trials and 78 effective trials. Appraisal ratio is -0.57. Rounding does not imply that the DSR is exactly zero.

<!-- Source: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cells 16 and 24. -->

5. Stability — FAIL. The blend fails gates 2, 3 and 4; none of the five calendar blocks has positive alpha. Excluding the best year, 2020, leaves annual alpha -2.57%.

<!-- Source: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cells 18 and 24. -->

6. Robustness — FAIL. Removing the broad cluster leaves Sharpe retention -168.60%, below required 50.00%. SPY's P&L share is 117.50%, above 30.00%, reflecting offsetting contributions elsewhere. Neighbour median retention is 85.35%, lowest nearby retention 54.41%, and one-day delay retention 144.10%. Passing some sensitivity checks does not cancel cluster and concentration failures.

<!-- Source: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cells 20 and 24. Ratios are converted to percentage units. -->

7. Sealed holdout — PASS. Over 2023–2025, Sharpe is 0.71 and alpha -0.54% annually, above floors -0.65 and -4.27%. No variant is rewritten, and no timing break is found on 20 checked dates. This pass is a decay diagnostic, not validation of a positive benchmark-relative edge.

<!-- Source: alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb, cells 22 and 24. -->

## Refutation clauses and what was learned

The negative alpha meets the card's no-alpha condition. The low placebo rank and concentration provide further adverse evidence. The incremental-alpha clause against TM-017-01 remains unassessed: the historical run commit 9a00fbb cannot be authenticated locally and lab.compare refuses. No replacement paired calculation is made.

The theory lesson is that shallow, slowly fitted boosted trees on these own-price features do not validate the proposed timing improvement. The market evidence is negative against passive holding and sensitive to the broad cluster. The report does not establish whether nonlinear overfitting, insufficient information or changing regimes caused failure. The lab lesson is that conservative hyperparameters do not guarantee economic edge, and a later holdout pass cannot repair the first failed gate. No strategy change or post-run repair is performed.

This card replaces retired, unrun TM-017-05 after a locking error. Its effective IS window is 2011-02-02 to 2022-12-30, while the rule begins 2006-02-01. Recorded thresholds are version 4 here and version 1 for the rule; the comparison remains descriptive.

<!-- Sources: alpha-lab/strategies/TM-017-08-boosted-trend/card.yaml and reasoning.md; its report.ipynb cells 4 and 24; alpha-lab/strategies/TM-017-01-time-series-momentum/report.ipynb cells 4 and 24; capstone/STOPPED.md. -->
