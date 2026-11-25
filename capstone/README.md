# Capstone research application and deliverables

Read manuscript.md or manuscript.docx for the full study, and presentation.pptx for the two-minute individual defence. The manuscript contains numbered tables and figures and uses first-person academic prose. Detailed provenance is kept in results-notes.md.

- results.csv: all completed strategies plus the retired, unrun 03–05 cards. Blank financial values mean not run, not zero.
- figures/: four published-output charts covering the reference, original ML models, both reversal follow-ups and the repaired weighting card; the gate chart also marks TM-017-09 unrun.
- diagnostics/: an in-sample-only forecast diagnostic, six charts, overall/year/fund metrics, coefficient histories, training importances, decision behaviour and source hashes. It computes no portfolio return.
- verdict-drafts/: gate-by-gate review documents for the original ML cards, both executed reversal cards and TM-017-10, plus an unrun-specification record for TM-017-09; no lab verdict.md is written.
- presentation.pptx: four slides for the two-minute defence, built by build_defence.py; defence-script.md holds the spoken script and timing.
- presentation-backup.pptx: fifteen backup slides for questions, built by build_presentation.py; presentation-outline.md is its text companion.
- costs-robustness.csv: published gross/net/doubled-cost Sharpe, annual costs, calendar blocks, DSR and profit concentration, transcribed by extract_costs.py from saved report cells; manuscript Table 3.
- defence-qa.md: nineteen concise preparation answers, including research-integrity questions.
- SUMMARY-FR.md: French handover, conclusions and pre-submission review priorities.
- STOPPED.md: preserved history of administrative and comparison limitations, with current status appended.
- source-hashes.json: hashes of the seven saved report notebooks.
- build_capstone.py, build_presentation.py and local_plotting.py: local artifact builders and repository-only cache/font setup. export_docx.py, extract_costs.py and build_defence.py need only the packages in ../requirements-docs.txt.

## Research record

TM-017-03 to -05 were retired without runs after a locking error. TM-017-06 to -08 each ran once. The diagnostic then used data truncated before assembly at 2022-12-31. The first follow-up, MR-001-01-monthly-liquidity-reversal, was locked alone before code and run once; it first failed gate 2. Anas then fixed two more rules before either new card ran. MR-001-02-stress-conditioned-reversal was locked alone, passed preflight and ran once; it also first failed gate 2. Each registry entry was committed alone before its report. TM-017-09-volatility-weighted-trend was locked alone and checked but skipped after its exact all-tradable inverse-volatility denominator was undefined in the official preflight. At that stage no substitute was drawn. Anas subsequently authorised only TM-017-10 to repair the unrun rule by excluding undefined-volatility funds from holdings and denominator. It ran once, passed economics and robustness, and first failed significance. No completed strategy was edited or rerun.

The follow-up designs did not use further holdout calculations. Four follow-up cards were specified overall; three have financial trials, while TM-017-09 still has no run, registered trial, financial metric or opened holdout. The skip is detailed in STOPPED.md and its verdict-draft document. Earlier holdout outputs were already known and remain explicitly disclosed; the follow-up is exploratory. The official paired comparison with TM-017-01 remains unavailable because its historical run commit is missing. Comparisons are descriptive, with different effective windows and recorded threshold versions.

## Rebuild documentation only

From the repository root, activate the existing environment, then rebuild saved-output charts, Word and PowerPoint:

```sh
source .venv/bin/activate
python -B capstone/build_capstone.py
python -B capstone/build_presentation.py
```

These commands do not execute a strategy or recompute market forecasts. The diagnostic itself has its own script and committed outputs; rebuilding the final documents does not rerun it. All caches and bundled fonts remain inside the repository. No installation, internet access or external rendering application is required by the builders.


## Six-model forecast extension

The diagnostic now compares OLS, Elastic Net, Random Forest, Gradient Boosting,
logistic regression and MLP, plus the rule proxy. Only the original three ML
cards have portfolio runs; the added models evaluate forecasts only. Original
numerical rows, coefficient histories and decision summaries are preserved.
Logistic R² is displayed as n/a; the classifier is judged by accuracy, AUC
and log-loss. Archived numerical metric files remain unchanged. Following-month permutation
importance uses ten repeats and a frozen model on each scored month, never
holdout data or a portfolio return. Fixed settings were committed before evaluation.

To reproduce that forecast-only extension, with the environment activated:

```sh
python -B capstone/diagnostics/diagnostics.py --extend
```

The two-decimal display uses metrics computed before rounding. New observations
are in extended-forecast-observations.csv; permutation and impurity summaries
are separate CSVs. The archived original observation and fit-history files remain
unchanged. Rebuilding Word or PowerPoint does not rerun any forecasts or strategy.
