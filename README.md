# Do machine-learning trend signals survive strict validation?

AI for Finance — individual capstone (Type A), Anas Chantah, Master in Finance, IE Business School.

Machine-learning forecasts (Elastic Net, Random Forest, Gradient Boosting, plus OLS, logistic
regression and an MLP as diagnostics) replace the monthly entry decision of a time-series momentum
rule on seven ETFs. Every strategy faces a seven-gate validation battery: costs, shifted-timing
placebos, a deflated Sharpe ratio for multiple testing, stability, robustness and a sealed 2023–2025
holdout. **No tested strategy passes all seven gates.**

| Deliverable | File |
|---|---|
| Manuscript (source / Word) | `capstone/manuscript.md`, `capstone/manuscript.docx` |
| Two-minute defence (4 slides, speaker notes) | `capstone/presentation.pptx`, `capstone/defence-script.md` |
| Backup slides for questions (15 slides) | `capstone/presentation-backup.pptx`, `capstone/presentation-outline.md` |
| Question preparation | `capstone/defence-qa.md` |
| All strategy results | `capstone/results.csv`, `capstone/costs-robustness.csv` |
| Forecast diagnostic | `capstone/diagnostics/` (report, CSV metrics, figures) |
| Provenance of every table and figure | `capstone/results-notes.md` |
| Strategy cards, code and executed reports | `alpha-lab/strategies/<card>/` |

## Reproducing the manuscript from the saved results

Every table and figure in the manuscript is generated from the executed report notebooks in
`alpha-lab/strategies/*/report.ipynb` and the diagnostic outputs in `capstone/diagnostics/`. These
steps read saved outputs only; they run no strategy and need no market data. From the repository root:

```sh
python -m pip install -r requirements-docs.txt
python -B capstone/extract_costs.py        # Table 3: costs, calendar blocks, DSR (cells 12, 16, 18, 20)
python -B capstone/build_capstone.py       # results.csv, Table 2, Figures 1, 5, 6 and manuscript.docx
python -B capstone/export_docx.py          # manuscript.docx alone (python-docx only)
python -B capstone/build_defence.py        # two-minute presentation.pptx and defence-script.md
python -B capstone/build_presentation.py   # fifteen-slide backup deck and its outline
```

`build_capstone.py` and `build_presentation.py` also draw charts with matplotlib and expect it in a
repository-local `.venv` (see `capstone/local_plotting.py`); `extract_costs.py`, `export_docx.py`
and `build_defence.py` run with the packages in `requirements-docs.txt` alone.

## Reproducing the experiments

The strategies were executed by Alpha Factory, a pre-existing validation framework co-founded with
Sami Andaloussi before the course (https://github.com/Sami-Andaloussi/alpha-factory), on a frozen
Yahoo Finance snapshot identified by hash in `alpha-lab/data/manifest.json`. Each card in
`alpha-lab/strategies/` contains its locked hypothesis (`card.yaml`), reasoning, build plan,
strategy code (`strategy.py`) and the executed report (`report.ipynb`) with its saved outputs.

This repository does not yet contain the framework's runner (`alpha-lab/lab/`), its tests, the
pinned experiment environment or the market data, so the backtests and the forecast diagnostic
(`capstone/diagnostics/diagnostics.py`) cannot be re-executed from this repository alone. With the
framework, the data snapshot and its environment, a card is run with
`python -m lab.report strategies/<card>` from `alpha-lab/`, as described in `alpha-lab/RUNBOOK.md`.
Each card's holdout is opened once, so re-running a recorded card is refused by design.

## Use of generative AI

Claude and OpenAI Codex were used for coding and drafting, as disclosed in the manuscript (Annex A).
The author reviewed and takes responsibility for all content.
