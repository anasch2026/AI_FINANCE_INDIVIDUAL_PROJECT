# TM-017-06 — Elastic Net: draft verdict

Draft for Anas's review; this is not the lab's verdict.md. The recorded verdict is **fails gate 1, hygiene**. All later gates were nevertheless evaluated. Threshold version: 4.

<!-- Source for verdict, all gate labels and version: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 0 and 24. -->

## Gate by gate

1. Hygiene — FAIL. The report counts 17 clustered decisions, below 30, over 11.90 evaluated years. There are no look-ahead or same-day breaks on 100 checked dates, and no memory breaks on 50 memory-check dates, with declared memory 2,400 sessions. This is an evidence-count failure, not a detected timing violation.

<!-- Source: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 10 and 24. -->

2. Economic edge — FAIL. Net Sharpe is 0.30 versus benchmark 0.39, with annual alpha -0.61%. At doubled costs, Sharpe is 0.30 and alpha -0.64%. Rounding the doubled-cost Sharpe to the displayed threshold does not change the lab's recorded failure; the economic and alpha conditions also fail.

<!-- Source: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 12 and 24. -->

3. Significance — FAIL. PSR is 0.87 against the required 0.95. The base strategy beats 0.00% of 1,000 shifted placebos, below the required 90.00%. This fraction is not a p-value.

<!-- Source: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 14 and 24. -->

4. Multiple testing — FAIL. The published DSR is below 0.01, against 0.90 required, with 83 registered trials and 76 effective trials. Appraisal ratio is -0.21. The tiny DSR should not be read as exactly zero after rounding.

<!-- Source: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 16 and 24. -->

5. Stability — FAIL. The blend fails gates 2, 3 and 4. Alpha is positive in one of five blocks, below three required. Without the best year, 2019, annual alpha is -0.80%. There is only one base variant; its blend is not an independently chosen successful model.

<!-- Source: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 6, 18 and 24. -->

6. Robustness — FAIL. SPY accounts for 46.87% of P&L, above 30.00%. Neighbour median Sharpe retention is 103.70%, the lowest nearby retention is 89.79%, removing the broad cluster retains 55.16%, and one-day delay retains 96.37%. These other tolerances do not offset the concentration failure.

<!-- Source: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 20 and 24. Percentages are the report's ratios converted to percentage units. -->

7. Sealed holdout — PASS. Over 2023–2025, Sharpe is 0.91 and alpha rounds to -0.00% annually, slightly negative before rounding. Their respective floors are -0.52 and -2.45%. No variant is rewritten and no timing break is reported on 20 checked dates. This is a pass against the lab's decay floors, not evidence that the earlier failures disappear.

<!-- Source: alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb, cells 22 and 24. -->

## Refutation clauses and what was learned

The reported negative in-sample alpha meets the card's no-alpha condition. The unfavourable placebo rank and SPY concentration provide additional adverse evidence. The incremental-alpha clause against TM-017-01 remains unassessed: lab.compare cannot verify the reference run because commit 9a00fbb is absent. No subtraction of headline alphas or homemade paired test replaces that measure.

The theory-level lesson is limited: this regularised price-only specification does not validate the proposed timing mechanism. The market evidence is insufficiently distinct and concentrated in SPY; persistent forecasts are a possible interpretation of the low decision count, not a proved explanation. The lab lesson is to distinguish information hygiene from evidence sufficiency and to preserve the first failure despite a later holdout pass. No post-run change or new bug repair is made; the manuscript separately records inner-cross-validation and target-timing limitations from code inspection.

This card carries the hypothesis of retired, unrun TM-017-03 after an administrative locking error. Its published effective IS window is 2011-02-02 to 2022-12-30; the reference starts 2006-02-01, and threshold versions differ. The comparison is descriptive only.

<!-- Sources: alpha-lab/strategies/TM-017-06-elastic-net-trend/card.yaml and reasoning.md; its report.ipynb cells 4 and 24; alpha-lab/strategies/TM-017-01-time-series-momentum/report.ipynb cells 4 and 24; capstone/STOPPED.md. -->
