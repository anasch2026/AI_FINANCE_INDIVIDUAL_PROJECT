"""Transcribe published cost, stability, multiple-testing and concentration metrics.

Reads only the saved outputs of each executed report notebook (cells 12, 16,
18 and 20). It executes no notebook, imports no strategy, computes no return and
needs only the Python standard library. Values are rounded for display with
Decimal, exactly as build_capstone.py rounds results.csv.

Run from the repository root:  python -B capstone/extract_costs.py
Output: capstone/costs-robustness.csv
"""
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "capstone" / "costs-robustness.csv"
CARDS = [
    ("TM-017-01-time-series-momentum", "Plain rule"),
    ("TM-017-06-elastic-net-trend", "Elastic Net"),
    ("TM-017-07-random-forest-trend", "Random Forest"),
    ("TM-017-08-boosted-trend", "Gradient Boosting"),
    ("MR-001-01-monthly-liquidity-reversal", "Liquidity reversal"),
    ("MR-001-02-stress-conditioned-reversal", "Stress reversal"),
    ("TM-017-10-volatility-weighted-trend", "Volatility-weighted trend"),
]


class Table(HTMLParser):
    """Collect the cells of an HTML table rendered by pandas."""

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


def fields(notebook, cell):
    """Return the last row of the cell's table as {column: published text}."""
    html = next(o["data"]["text/html"] for o in notebook["cells"][cell]["outputs"]
                if "text/html" in o.get("data", {}))
    rows = Table("".join(html)).rows
    return dict(zip(rows[0][1:], rows[-1][1:]))


def fmt(text, percent=False):
    value = Decimal(text) * (100 if percent else 1)
    return f"{value:.2f}"


def dsr(text):
    return "<0.01" if Decimal(text) < Decimal("0.005") else fmt(text)


rows = []
for card, model in CARDS:
    source = f"alpha-lab/strategies/{card}/report.ipynb"
    nb = json.loads((ROOT / source).read_text())
    economics, selection, stability = fields(nb, 12), fields(nb, 16), fields(nb, 18)
    robustness = fields(nb, 20)
    rows.append(dict(
        card=card, model=model,
        gross_sharpe=fmt(economics["gross Sharpe"]),
        net_sharpe=fmt(economics["Sharpe"]),
        sharpe_2x_costs=fmt(economics["Sharpe at 2x costs"]),
        alpha_2x_costs_pct_pa=fmt(economics["alpha at 2x costs"], True),
        costs_pct_pa=fmt(economics["costs a year"], True),
        positive_alpha_blocks_of_5=stability["positive blocks"],
        best_year=stability["best year"],
        alpha_without_best_year_pct_pa=fmt(stability["alpha without the best year"], True),
        trials=selection["trials"], effective_trials=selection["effective trials"],
        dsr=dsr(selection["DSR"]),
        largest_profit_share_pct=fmt(robustness["largest P&L share"], True),
        largest_profit_asset=robustness["asset with the largest share"],
        source_file=source, source_cells="12;16;18;20"))

with OUT.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {OUT.relative_to(ROOT)} with {len(rows)} published rows.")
