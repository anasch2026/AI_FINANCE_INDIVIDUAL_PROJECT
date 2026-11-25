"""Build descriptive capstone artifacts from saved notebook outputs only.

No notebook execution, strategy import, returns calculation, paired test or network.
Run with the repository virtual environment activated, from the repository root.
All caches, fonts and temporary paths are explicitly inside the repository.
"""
from pathlib import Path
from html.parser import HTMLParser
from decimal import Decimal
import csv
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "capstone"
WORK = ROOT / ".build-cache"
WORK.mkdir(exist_ok=True)
for name in ("MPLCONFIGDIR", "XDG_CACHE_HOME", "TMPDIR"):
    p = WORK / name.lower()
    p.mkdir(exist_ok=True)
    os.environ[name] = str(p)
os.environ["MPLBACKEND"] = "Agg"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

IDS = ["TM-017-01-time-series-momentum", "TM-017-06-elastic-net-trend",
       "TM-017-07-random-forest-trend", "TM-017-08-boosted-trend", "MR-001-01-monthly-liquidity-reversal", "MR-001-02-stress-conditioned-reversal", "TM-017-10-volatility-weighted-trend"]
NAMES = ["Plain rule", "Elastic Net", "Random Forest", "Gradient Boosting", "Liquidity reversal", "Stress reversal", "Volatility-weighted trend"]
SHORT = ["01", "06", "07", "08", "MR1", "MR2", "10"]
SOURCES = [f"alpha-lab/strategies/{i}/report.ipynb" for i in IDS]


class Table(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.rows, self.row, self.value, self.capture = [], [], "", False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        if tag in ("th", "td"):
            self.value, self.capture = "", True

    def handle_data(self, data):
        if self.capture:
            self.value += data

    def handle_endtag(self, tag):
        if tag in ("th", "td"):
            self.row.append(self.value.strip())
            self.capture = False
        if tag == "tr" and self.row:
            self.rows.append(self.row)


def table(nb, cell):
    html = next(o["data"]["text/html"] for o in nb["cells"][cell]["outputs"]
                if "text/html" in o.get("data", {}))
    return Table("".join(html)).rows


def fields(nb, cell):
    rows = table(nb, cell)
    return dict(zip(rows[0][1:], rows[-1][1:]))


def number(s, percent=False):
    x = Decimal(s) * (100 if percent else 1)
    return f"{x:.2f}"


DATA = []
for ident, name, source in zip(IDS, NAMES, SOURCES):
    nb = json.loads((ROOT / source).read_text())
    vals = {g: fields(nb, c) for g, c in zip(range(1, 8), range(10, 24, 2))}
    gates = [r[1].replace("passes", "pass").replace("fails", "fail")
             for r in table(nb, 24)[2:]]
    assert len(gates) == 7
    md = " ".join("".join(o.get("data", {}).get("text/markdown", []))
                  for o in nb["cells"][4]["outputs"])
    start, end = re.search(r"evaluated from .*?, (\d{4}-\d{2}-\d{2}), to (\d{4}-\d{2}-\d{2})", md).groups()
    version_text = " ".join("".join(o.get("data", {}).get("text/markdown", []))
                            for o in nb["cells"][24]["outputs"])
    version = re.search(r"version (\d+)", version_text)[1]
    row = dict(card=ident, model=name, trial_status="recorded", first_failed_gate=gates.index("fail") + 1,
               **{f"gate_{i}": v for i, v in enumerate(gates, 1)},
               declared_in_sample="2005-01-01/2022-12-31", evaluated_start=start,
               evaluated_end=end, thresholds_version=version,
               sharpe=number(vals[2]["Sharpe"]), benchmark_sharpe=number(vals[2]["benchmark Sharpe"]),
               alpha_pct_pa=number(vals[2]["alpha"], True),
               placebo_beaten_pct=number(vals[3]["placebos beaten"], True),
               holdout_evaluated="yes", holdout_period="2023-01-01/2025-12-31",
               holdout_sharpe=number(vals[7]["holdout Sharpe"]),
               holdout_alpha_pct_pa=number(vals[7]["holdout alpha"], True),
               paired_comparison="unavailable", source_file=source,
               source_cells="4;10;12;14;16;18;20;22;24")
    DATA.append((row, vals))

with (OUT / "results.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(DATA[0][0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(r for r, _ in DATA)
    for ident, name in [("TM-017-03-elastic-net-trend", "Elastic Net"), ("TM-017-04-random-forest-trend", "Random Forest"), ("TM-017-05-boosted-trend", "Gradient Boosting")]:
        row = {k: "" for k in DATA[0][0]}
        row.update(card=ident, model=name, trial_status="retired_unrun", holdout_evaluated="no", source_file="capstone/STOPPED.md", paired_comparison="not_applicable")
        row.update({f"gate_{i}": "not_run" for i in range(1, 8)})
        writer.writerow(row)
    row = {k: "" for k in DATA[0][0]}
    row.update(card="TM-017-09-volatility-weighted-trend", model="Volatility-weighted trend", trial_status="skipped_preflight", holdout_evaluated="no", source_file="capstone/STOPPED.md", paired_comparison="not_applicable")
    row.update({f"gate_{i}": "not_run" for i in range(1, 8)})
    writer.writerow(row)

def result_table(french=False):
    head = ("| Strategy | First failed gate | IS Sharpe | Alpha (%/yr) | Placebos beaten (%) | Holdout Sharpe | Holdout alpha (%/yr) |\n"
            "|---|---|---:|---:|---:|---:|---:|\n")
    if french:
        head = ("| Carte | Premier gate échoué | Sharpe IS | Alpha (%/an) | Placebos battus (%) | Sharpe holdout | Alpha holdout (%/an) |\n"
                "|---|---|---:|---:|---:|---:|---:|\n")
    for (r, _), short in zip(DATA, SHORT):
        ident = "-".join(r['card'].split('-')[:3])
        head += f"| {ident} — {r['model']} | {r['first_failed_gate']} | {r['sharpe']} | {r['alpha_pct_pa']} | {r['placebo_beaten_pct']} | {r['holdout_sharpe']} | {r['holdout_alpha_pct_pa']} |\n"
    head += "| TM-017-09 — Volatility-weighted trend | Not run | — | — | — | — | — |\n"
    return head

SOURCE_COMMENT = "<!-- Sources: " + "; ".join(SOURCES) + "; cells 4, 12, 14, 22, 24. -->"
note = """# Results: scope, units and provenance

This is a descriptive side-by-side transcription, not a paired test. The official
comparison cannot authenticate the reference run because its run commit 9a00fbb is
absent from the squashed local history. No replacement test or common-window return
calculation is supplied. All cards declare 2005–2022, but their published effective
evaluation windows differ: the plain rule starts 2006-02-01, the ML cards 2011-02-02;
all end 2022-12-30. Threshold versions also differ: reference version 1, later cards version 4.

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

"""
(OUT / "results-notes.md").write_text(note + result_table() + "\n" + SOURCE_COMMENT + "\n")

(OUT / "results-notes.md").write_text(note.replace("all end 2022-12-30", "MR-001-01 starts 2005-03-02, MR-001-02 starts 2008-05-02 and TM-017-10 starts 2006-02-02; all recorded runs end 2022-12-30") + result_table() + "\n" + SOURCE_COMMENT + "\n" + """

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
but the published tables and chart show logistic R² as n/a. R² is not defined for a binary target; the logistic model is judged by accuracy, AUC and log-loss.
No probability-to-return conversion is invented. Its accuracy, AUC and log-loss
concern the sign. Rank IC uses probabilities against future
return ranks. The other R2 values retain their original return/proxy definitions.
Permutation importance is evaluated only on each following month's seven labels
inside the cutoff, with ten repeats and random_state=0. Its units are the increase
in next-month MSE in return basis points squared. Negative values mean shuffling
improves error; training impurity importance is a different quantity. The new
settings and evaluation protocol were committed before the diagnostic ran.
""")

with (OUT / "results-notes.md").open("a") as f:
    f.write('\n\n## Final local reconstruction and interpretation corrections\n\nThe final manuscript uses the official five-section structure and word limit. Trading-cost drag is not reported as turnover. Cross-window comparisons are descriptive; the same sizing rule does not establish a causal model effect. Regulatory readiness and runtime costs remain unassessed rather than asserted. The original reference entries and all numerical research outputs are unchanged.\n\nAll six manuscript figures can be reconstructed from the archived notebook/CSV inputs: financial figures by build_capstone.py, diagnostic figures by render_saved_figures.py. The latter imports no lab code or estimator and uses no raw market values. Any rounded coefficient/importance display comes from its saved CSV; accuracy statistics are preserved rather than re-estimated. See the root README for the distinction between document reconstruction and an independent experimental replication.\n')

# Use the active environment and repository-local caches, without a Mac-specific .venv path.
from local_plotting import configure
configure()
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FormatStrFormatter

plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.facecolor": "white"})
FIG = OUT / "figures"
FIG.mkdir(exist_ok=True)
labels = [f"{s}  {n}" for s, n in zip(SHORT, NAMES)]
colors = ["#4b5563", "#6b8193", "#6b8193", "#6b8193", "#8b7360", "#925c57", "#59715d"]
foot = "Descriptive: unequal effective windows, thresholds v1 / v4. TM-017-09 unrun (see STOPPED.md)."

def save(fig, name, cell_note, footer=foot):
    # Source comment for each chart: SOURCES, plus the zero-based cells below.
    source = "; ".join(SOURCES) + "; " + cell_note + "; TM-017-09 unrun status: capstone/STOPPED.md"
    fig.text(0.02, 0.015, footer, fontsize=8, color="#4b5563")
    fig.savefig(FIG / f"{name}.png", dpi=180, bbox_inches="tight",
                metadata={"Description": "Source: " + source})
    plt.close(fig)
    (FIG / f"{name}.sources.md").write_text(f"<!-- Source: {source}. -->\n\n{footer}\n")

# Chart 1 source: every source notebook cell 24, gate-result table.
fig, ax = plt.subplots(figsize=(11, 5.2))
grid = [[int(r[f"gate_{i}"] == "pass") for i in range(1, 8)] for r, _ in DATA]
grid.append([-1] * 7)
ax.imshow(grid, cmap=ListedColormap(["#e1e5e9", "#e7c4bf", "#bdd2c6"]), vmin=-1, vmax=1, aspect="auto")
for y, row in enumerate(grid):
    for x, v in enumerate(row):
        ax.text(x, y, "Not run" if v == -1 else ("Pass" if v else "Fail"), ha="center", va="center")
ax.set_xticks(range(7), [f"Gate {i}" for i in range(1, 8)])
ax.set_yticks(range(len(grid)), labels + ["09  Volatility-weighted (unrun)"])
ax.set_title("Published gate outcomes — verdict is the first failure", pad=15)
fig.tight_layout(rect=(0, 0.10, 1, 1))
save(fig, "01-gates", "cell 24")

def two_metrics(name, keys, titles, title, cells, benchmark=False, footer=foot):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, key, subtitle in zip(axes, keys, titles):
        values = [float(r[key]) for r, _ in DATA]
        bars = ax.bar(range(len(DATA)), values, color=colors, width=0.6)
        ax.axhline(0, color="#555555", linewidth=0.7)
        for b, v, (r, _) in zip(bars, values, DATA):
            ax.annotate(r[key], (b.get_x() + b.get_width()/2, v),
                        xytext=(0, 5 if v >= 0 else -14), textcoords="offset points",
                        ha="center", fontsize=10)
        if benchmark and key == "sharpe":
            bvals = [float(r["benchmark_sharpe"]) for r, _ in DATA]
            ax.scatter(range(len(DATA)), bvals, marker="_", s=500, linewidths=2,
                       color="#8b6253", label="Equal-weight hold (own window)")
            ax.legend(fontsize=8, loc="upper right")
        ax.set_xticks(range(len(DATA)), SHORT)
        ax.set_xlabel("01 rule · 06 EN · 07 RF · 08 GB · MR1 reversal · MR2 stress · 10 weighted", fontsize=8)
        ax.set_title(subtitle)
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        lo, hi = ax.get_ylim()
        ax.set_ylim(lo - (hi-lo)*0.12, hi + (hi-lo)*0.25)
        ax.grid(axis="y", alpha=0.15)
    fig.suptitle(title)
    fig.tight_layout(rect=(0, 0.10, 1, 0.94))
    save(fig, name, cells, footer)

# Chart 2 source: each report cell 12, base economic metrics, its own window.
two_metrics("02-in-sample", ["sharpe", "alpha_pct_pa"],
            ["Net excess-return Sharpe", "Alpha vs equal-weight hold (%/year)"],
            "Published in-sample performance — unequal effective windows", "cell 12", True)

# Chart 3 source: each report cell 14 (base rank), cell 24 (90% threshold).
fig, ax = plt.subplots(figsize=(10, 4.9))
values = [float(r["placebo_beaten_pct"]) for r, _ in DATA]
ax.barh(labels[::-1], values[::-1], color=colors[::-1])
for i, v in enumerate(values[::-1]):
    ax.text(v + 1, i, f"{v:.2f}%", va="center")
ax.axvline(90, color="#8b6253", linestyle="--", label="Required: 90.00%")
ax.set_xlim(0, 104)
ax.set_xlabel("Shifted placebos beaten (%) — not a p-value")
ax.set_title("Published base-strategy placebo ranks")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout(rect=(0, 0.12, 1, 1))
save(fig, "03-placebos", "cells 14 and 24")

# Chart 4 source: each report cell 22; no holdout inference is recomputed.
two_metrics("04-holdout", ["holdout_sharpe", "holdout_alpha_pct_pa"],
            ["Holdout net excess-return Sharpe", "Holdout alpha vs equal-weight hold (%/year)"],
            "Published holdout diagnostics: 2023–2025", "cell 22",
            footer="Recorded runs pass gate 7; earlier failures remain. TM-017-09 unrun; EN alpha slightly negative.")


from export_docx import export_docx  # Word export lives in its own module.


if __name__ == "__main__":
    if (OUT / "manuscript.md").exists():
        export_docx()
    manifest = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    (OUT / "source-hashes.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Built results.csv, results-notes.md, four sourced PNG charts; exported DOCX if manuscript exists.")
