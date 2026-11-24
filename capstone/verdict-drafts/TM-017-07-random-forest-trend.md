# TM-017-07 — Random Forest: draft verdict

Draft for Anas's review; this is not the lab's verdict.md. The recorded verdict is **fails gate 2, economic edge**. All later gates were evaluated. Threshold version: 4.

<!-- Source for verdict, all gate labels and version: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cells 0 and 24. -->

## Gate by gate

1. Hygiene — PASS. The report counts 102 clustered decisions over 11.90 evaluated years. No look-ahead or same-day break occurs on 100 checked dates; no memory break occurs on 50 memory-check dates. Declared memory is 2,400 sessions, and data problems are reported as none.

<!-- Source: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cell 10. -->

2. Economic edge — FAIL. Sharpe is 0.08, below the required 0.40 and benchmark 0.39. Annual alpha is -2.07%. At doubled costs Sharpe is 0.06 and alpha -2.19%. The first failure is therefore economic, before significance or multiple-testing corrections.

<!-- Source: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cells 12 and 24. -->

3. Significance — FAIL. PSR is 0.62, below 0.95. The base beats 0.90% of 1,000 shifted placebos, below 90.00%. The blend's separately reported rank is 1.10%; the base rank is used in results.csv.

<!-- Source: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cells 14, 18 and 24. -->

4. Multiple testing — FAIL. DSR is below 0.01 against 0.90 required, with 84 registered trials and 77 effective trials. Appraisal ratio is -0.59. These counts cover the lab's accumulated registry, not just this capstone's models.

<!-- Source: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cells 16 and 24. -->

5. Stability — FAIL. The blend fails gates 2, 3 and 4. No calendar block has positive alpha out of five. Excluding the best year, 2014, leaves annual alpha -2.30%.

<!-- Source: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cells 18 and 24. -->

6. Robustness — FAIL. Removing bonds leaves Sharpe retention -35.51%, below the required 50.00%; SPY's P&L share is 151.00%, above 30.00%. A share above 100% is possible when other contributions offset the largest positive contribution. Neighbour median retention is 291.50%, with lowest nearby retention 177.80%; such ratios against a weak base do not establish a useful strategy. One-day delay retention is 147.00%.

<!-- Source: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cells 20 and 24. Ratios are converted to percentage units. -->

7. Sealed holdout — PASS. Over 2023–2025, Sharpe is 0.79 and annual alpha -0.15%, above floors -0.62 and -4.29%. No variant is rewritten and no timing break occurs on 20 checked dates. Negative alpha can pass this gate because the floor is an in-sample-derived lower bound.

<!-- Source: alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb, cells 22 and 24. -->

## Refutation clauses and what was learned

The negative alpha meets the card's no-alpha condition; the low placebo rank and concentration also weigh against the proposed implementation. The incremental-alpha clause against TM-017-01 is unassessed because its recorded run commit 9a00fbb is absent, so the official paired comparison is refused. No homemade test replaces it.

The theory lesson is that allowing nonlinear interactions in these price features does not produce a validated timing signal in this experiment. The market evidence is negative relative to passive exposure and depends on the bond cluster and SPY contribution. These observations do not reveal which feature interactions caused failure. The lab lesson is that passing timing checks is necessary but does not confer economic value; a holdout decay pass cannot rescue an economic failure. No strategy change or post-run repair is performed.

This replaces retired, unrun TM-017-04 after the locking error. Its effective IS window is 2011-02-02 to 2022-12-30. The reference begins 2006-02-01 and uses threshold version 1, while this run uses version 4. Side-by-side comparison is descriptive, not a common-window paired inference.

<!-- Sources: alpha-lab/strategies/TM-017-07-random-forest-trend/card.yaml and reasoning.md; its report.ipynb cells 4 and 24; alpha-lab/strategies/TM-017-01-time-series-momentum/report.ipynb cells 4 and 24; capstone/STOPPED.md. -->
