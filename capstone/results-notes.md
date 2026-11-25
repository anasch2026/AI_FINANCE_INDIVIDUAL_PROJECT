# Results: scope, units and provenance

This is a descriptive side-by-side transcription, not a paired test. The official
comparison cannot authenticate the reference run because its run commit 9a00fbb is
absent from the squashed local history. No replacement test or common-window return
calculation is supplied. All cards declare 2005–2022, but their published effective
evaluation windows differ: the plain rule starts 2006-02-01, the ML cards 2011-02-02;
MR-001-01 starts 2005-03-02, MR-001-02 starts 2008-05-02 and TM-017-10 starts 2006-02-02; all recorded runs end 2022-12-30. Threshold versions also differ: reference version 1, later cards version 4.

Alpha is the lab's annual regression intercept against the same seven funds held
always in equal parts, using the report's own effective window. It is not alpha
against TM-017-01 and not a subtraction of total returns. Sharpe uses returns over
the Treasury bill, net of the lab's costs. Percent fields are percentage units, not
fractions. Numeric values are rounded to at most two decimals; pass/fail labels are
copied from the reports, never recomputed from rounded figures. The Elastic Net
holdout alpha rounds to -0.00%; its published sign is slightly negative.

Every gate was evaluated, including holdout, even after an earlier gate failed.
`first_failed_gate` is the verdict, not a claim that later gates were skipped.
Placebo percentage means the fraction of shifted placebos beaten, not a p-value.
Base ranks are used; the blend's separately reported ranks are not substituted.

CSV provenance columns identify each row's source file and zero-based notebook
cells. Cell 4 supplies dates; 10 hygiene; 12 economic metrics; 14 placebo ranks;
16 multiple testing; 18 stability; 20 robustness; 22 holdout; 24 gate statuses and
threshold version. The reference verdict corroborates its report:
`alpha-lab/strategies/TM-017-01-time-series-momentum/verdict.md`.

<!-- Each financial figure in results.csv comes from its row's source_file,
with the zero-based cell mapping immediately above. -->

| Strategy | First failed gate | IS Sharpe | Alpha (%/yr) | Placebos beaten (%) | Holdout Sharpe | Holdout alpha (%/yr) |
|---|---|---:|---:|---:|---:|---:|
| TM-017-01 — Plain rule | 3 | 0.50 | 1.55 | 81.70 | 0.89 | 0.61 |
| TM-017-06 — Elastic Net | 1 | 0.30 | -0.61 | 0.00 | 0.91 | -0.00 |
| TM-017-07 — Random Forest | 2 | 0.08 | -2.07 | 0.90 | 0.79 | -0.15 |
| TM-017-08 — Gradient Boosting | 2 | 0.09 | -1.90 | 1.80 | 0.71 | -0.54 |
| MR-001-01 — Liquidity reversal | 2 | 0.24 | -1.07 | 37.10 | 0.90 | 1.06 |
| MR-001-02 — Stress reversal | 2 | 0.08 | -1.37 | 33.70 | 0.78 | 1.04 |
| TM-017-10 — Volatility-weighted trend | 3 | 0.61 | 2.16 | 89.80 | 0.79 | -0.02 |
| TM-017-09 — Volatility-weighted trend | Not run | — | — | — | — | — |

<!-- Sources: alpha-lab/strategies/TM-017-01-time-series-momentum/report.ipynb; alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb; alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb; alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb; alpha-lab/strategies/MR-001-01-monthly-liquidity-reversal/report.ipynb; alpha-lab/strategies/MR-001-02-stress-conditioned-reversal/report.ipynb; alpha-lab/strategies/TM-017-10-volatility-weighted-trend/report.ipynb; cells 4, 12, 14, 22, 24. -->


## Final manuscript, tables and figure provenance

The CSV also preserves retired, unrun cards 03–05 with not_run gates and blank
financial metrics. They are not silently counted as completed trials. The new
MR-001-01 is one additional registered base trial, with no selected alternatives.
Its notebook has the same cell mapping as the original reports. The new theory's
status alone was updated, with the bank index and board regenerated as the runbook
requires; no existing strategy, model, threshold, template or data file changed.

Manuscript Table 1 (gates): alpha-lab/lab/battery.py, constants and decide_*;
alpha-lab/RUNBOOK.md. Historical reference thresholds are version 1; ML, MR and
TM-017-10 are version 4. These are lab definitions, not new chosen thresholds.
Table 2 (strategy results): each CSV row's source_file and cells 12, 14, 22, 24.
Table 3 (costs, calendar stability, DSR): costs-robustness.csv, transcribed by
extract_costs.py from each report's saved cells 12, 16, 18 and 20; nothing recomputed.
Table 4 (forecast diagnostic): diagnostics/forecast-metrics.csv and summary.json.
All model settings and feature horizons: the corresponding lab card.yaml and
strategy.py, make(), features_at(), forecasts(); no settings were inferred from
holdout performance. Snapshot dates: each report cell 4 and data/manifest.json.
Diagnostic behaviour, coefficients, warnings and importances: diagnostics.py,
fit-history.csv, decision-behaviour.csv and importance-stability.csv; cutoff
2022-12-31. The data reader is truncated before market assembly. The scored
period ends November 2022; refit and decision histories include December 2022.

Manuscript Figure 1: figures/01-gates.png, each report cell 24.
Figure 2: diagnostics/01-forecast-quality.png, diagnostics.py and forecast-metrics.csv.
Figure 3: diagnostics/03-elastic-net-coefficients.png, diagnostics.py and fit-history.csv.
Figure 4: diagnostics/06-permutation-importances.png, diagnostics.py,
permutation-summary.csv and impurity-summary.csv. The archived original training
importance chart remains diagnostics/04-feature-importances.png.
Figure 5: figures/02-in-sample.png, each report cell 12.
Figure 6: figures/04-holdout.png, each report cell 22.
The remaining published placebo and diagnostic charts have PNG source metadata
and are generated by the corresponding script. No new holdout return or forecast
is computed to draw saved-output figures.

Reference literature entries for Bailey and López de Prado; Gu, Kelly and Xiu;
Harvey, Liu and Zhu; and Moskowitz, Ooi and Pedersen are preserved verbatim from
the prior manuscript. The additional liquidity-reversal motivation is documented
in bank/MR-001-short-term-reversal-liquidity-provision.md (Nagel, 2012). No online
verification was performed in this local-only session.

The official paired-comparison refusal remains in STOPPED.md. It is not repaired
or replaced. Old holdout results were seen before the diagnostic and new design;
that prior exposure is disclosed. The new card was locked alone in commit
11e268a, then its code committed, then run once. Its registry was committed alone
in a31cfd5 and its report separately in aa76374. Source text was not changed after
the run. The added diagnostics are exploratory, not independent confirmation.

## Two further pre-fixed specifications

MR-001-02 is follow-up 2. Its isolated card commit is 85b0ff2, code commit
41dbd85, isolated registry commit 818bb2c and report commit 00408dc. All of
its numerical results and statuses use its report.ipynb cells 4 and 10–24.
The SPY volatility window 63, preceding-median window 756 and memory 830 were
fixed by Anas. The current volatility is excluded from its reference median.
The only parameter and neighbours are those in its locked card.yaml.

TM-017-09 is follow-up 3, locked alone in 547df95 before code 6d5ac29. It is
skipped_preflight, not a failed financial trial. The exact all-tradable
inverse-volatility denominator is undefined for tradable DBC at the official
preflight decision 2006-03-01 because a full 63-session volatility is absent.
The first DBC date 2006-02-06 is in the frozen data manifest and universe.py.
No substitute, shorter window, imputation, excluded fund or new start is used.
Its CSV metrics remain blank, its gates not_run and its holdout unopened.
The gate chart uses a distinct unrun row; performance charts exclude this
unmeasured specification rather than showing zero. Source: STOPPED.md and
.git/codex-logs/try-TM-017-09-volatility-weighted-trend.log.

Both rules were fixed by Anas in one instruction before either new card ran.
Earlier 06–08 and MR-001-01 holdouts were already known. At that stage three
follow-up cards were specified; two had financial trials and one was unrun
(TM-017-10 later brought the total to four). This phase
adds only one registered trial. Every additional registered trial increases the
multiple-testing burden; an unrun card does not add a fabricated trial. Original
metrics, diagnostic statistics and earlier reports are not recomputed or changed.

## TM-017-10 and the fixed forecast extension

TM-017-09 stays skipped at preflight and is repaired only by the separately
locked TM-017-10. Anas explicitly specified parent=null and the sole change:
undefined-volatility funds are not held and do not enter the denominator.
TM-017-10 card-only lock: b3dc647; code: 47b5dca; isolated registry: fe8c43e;
report: f308b34. Its notebook cells 4 and 10–24 supply every new performance
figure. Its first failed gate is 3. The exact original rule and code in 09 were
not edited. The repair adds one registered base trial; forecast evaluations
of OLS, logistic regression and MLP add no portfolio trial or gate result.

The six-model diagnostic table adds fixed OLS, logistic and MLP settings to
the original three learners and rule proxy. Original numerical metric rows,
decision histories and coefficient records remain unchanged. New classification
and permutation definitions are in diagnostics/diagnostics.md and diagnostics.py.
The archived binary-sign score is retained unchanged in the raw metric files,
but the published tables and chart show logistic R² as n/a. Return-unit R² is not applicable to logistic probabilities; the logistic model is judged by accuracy, AUC and log-loss.
No probability-to-return conversion is invented. Its accuracy, AUC and log-loss
concern the sign. Rank IC uses probabilities against future
return ranks. The other R2 values retain their original return/proxy definitions.
Permutation importance is evaluated only on each following month's seven labels
inside the cutoff, with ten repeats and random_state=0. Its units are the increase
in next-month MSE in return basis points squared. Negative values mean shuffling
improves error; training impurity importance is a different quantity. The new
settings and evaluation protocol were committed before the diagnostic ran.


## Final local reconstruction and interpretation corrections

The final manuscript uses the official five-section structure and word limit. Trading-cost drag is not reported as turnover. Cross-window comparisons are descriptive; the same sizing rule does not establish a causal model effect. Regulatory readiness and runtime costs remain unassessed rather than asserted. The original reference entries and all numerical research outputs are unchanged.

All six manuscript figures can be reconstructed from the archived notebook/CSV inputs: financial figures by build_capstone.py, diagnostic figures by render_saved_figures.py. The latter imports no lab code or estimator and uses no raw market values. Any rounded coefficient/importance display comes from its saved CSV; accuracy statistics are preserved rather than re-estimated. See the root README for the distinction between document reconstruction and an independent experimental replication.
