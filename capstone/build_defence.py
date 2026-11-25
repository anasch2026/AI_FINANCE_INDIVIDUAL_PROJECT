"""Build the two-minute defence deck from saved results only.

Four slides of about thirty seconds each, with speaker notes. Every number is
read from capstone/results.csv, capstone/costs-robustness.csv or
capstone/diagnostics/summary.json; the gate chart is the saved PNG used in the
manuscript. Needs only python-pptx and Pillow: no matplotlib, notebook,
strategy or market data. Run from the repository root:

    python -B capstone/build_defence.py

Outputs: capstone/presentation.pptx and capstone/defence-script.md.
The fifteen-slide backup deck for questions is built by build_presentation.py.
"""
from pathlib import Path
import csv
import json

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "capstone"
NAVY, BLUE, INK, GRAY, PALE, TEAL = "24364B", "627D8C", "25313C", "65727D", "EEF2F5", "007F73"

results = {r["model"]: r for r in csv.DictReader((OUT / "results.csv").open())
           if r["trial_status"] == "recorded"}
costs = {r["model"]: r for r in csv.DictReader((OUT / "costs-robustness.csv").open())}
forecasts = {m["model"]: m for m in
             json.loads((OUT / "diagnostics/summary.json").read_text())["overall"]}
rule, en, rf, gb = (results[k] for k in ("Plain rule", "Elastic Net", "Random Forest", "Gradient Boosting"))
best = results["Volatility-weighted trend"]
r2 = [forecasts[m]["r2_zero_pct"] for m in ("OLS", "Elastic Net", "Random Forest", "Gradient Boosting", "MLP")]

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
prs.core_properties.author = "Anas Chantah"
prs.core_properties.title = "Do machine-learning trend signals survive strict validation?"


def color(value):
    return RGBColor.from_string(value)


def text(slide, value, x, y, w, h, size=22, fill=INK, bold=False, align=None):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = 0
    for i, line in enumerate(value.split("\n")):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.text = line
        p.font.name, p.font.size, p.font.bold = "Calibri", Pt(size), bold
        p.font.color.rgb = color(fill)
        p.space_after = Pt(10)
        if align:
            p.alignment = align
    return box


def slide(title, notes, source):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = RGBColor(255, 255, 255)
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    band.fill.solid()
    band.fill.fore_color.rgb = color(NAVY)
    band.line.fill.background()
    text(s, title, 0.6, 0.4, 12.1, 0.9, size=30, fill=NAVY, bold=True)
    text(s, source, 0.6, 7.0, 11.4, 0.3, size=10, fill=GRAY)
    number = text(s, f"{len(prs.slides)} / 4", 12.0, 7.0, 0.7, 0.3, size=10, fill=GRAY)
    number.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
    s.notes_slide.notes_text_frame.text = notes
    return s


def table(s, headers, rows, x, y, w, h, size=18):
    t = s.shapes.add_table(len(rows) + 1, len(headers), Inches(x), Inches(y), Inches(w), Inches(h)).table
    for j, v in enumerate(headers):
        t.cell(0, j).text = v
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row):
            t.cell(i, j).text = v
    for i, row in enumerate(t.rows):
        for cell in row.cells:
            cell.fill.solid()
            cell.fill.fore_color.rgb = color(NAVY if i == 0 else (PALE if i % 2 else "FFFFFF"))
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.12)
            for p in cell.text_frame.paragraphs:
                p.font.name, p.font.size, p.font.bold = "Calibri", Pt(size), i == 0
                p.font.color.rgb = color("FFFFFF" if i == 0 else INK)
    return t


def picture(s, path, x, y, w):
    with Image.open(OUT / path) as im:
        ratio = im.width / im.height
    s.shapes.add_picture(str(OUT / path), Inches(x), Inches(y), width=Inches(w), height=Inches(w / ratio))


# Slide 1 — problem and answer.
s = slide("Do ML trend signals survive strict validation?",
          f"A trend rule on seven ETFs beats equal-weight holding, Sharpe {rule['sharpe']} against "
          f"{rule['benchmark_sharpe']}, but it beats only {rule['placebo_beaten_pct']} percent of shifted-timing "
          "placebos, so its edge may be luck. I asked whether machine learning can make that monthly "
          "entry decision reliably better after costs. The short answer is no.",
          "Sources: results.csv (TM-017-01 report). Prior work: Alpha Factory, co-founded with Sami Andaloussi. AI assistance disclosed in the manuscript.")
text(s, "Anas Chantah | AI for Finance | IE Business School", 0.85, 1.25, 11.5, 0.35, size=16, fill=GRAY)
text(s, "Business problem", 0.85, 1.7, 11.5, 0.5, size=20, fill=BLUE, bold=True)
text(s, f"Trend rule on 7 ETFs: Sharpe {rule['sharpe']} vs {rule['benchmark_sharpe']} passive, "
        f"alpha {rule['alpha_pct_pa']}%/yr\n…but only {rule['placebo_beaten_pct']}% of timing placebos beaten (90% needed)",
     0.85, 2.25, 11.6, 1.4, size=24)
text(s, "Question", 0.85, 3.85, 11.5, 0.5, size=20, fill=BLUE, bold=True)
text(s, "Can ML forecasts turn this entry decision into a validated, cost-adjusted edge?",
     0.85, 4.4, 11.6, 0.8, size=24)
text(s, "Answer: no tested strategy passes all seven gates.", 0.85, 5.5, 11.6, 0.7,
     size=26, fill=TEAL, bold=True)

# Slide 2 — what I built.
s = slide("ML replaces only the entry decision",
          "I kept the funds, the monthly schedule and the one-seventh allocation, and replaced only the "
          "decision to hold. Elastic Net, Random Forest and Gradient Boosting forecast next-month excess "
          "returns from eight lagged price features on a rolling sixty-month window. Every strategy then "
          "faces seven gates: hygiene, economic edge, significance, multiple testing, stability, "
          "robustness and a sealed 2023 to 2025 holdout.",
          "Sources: ML card.yaml and strategy.py; manuscript Table 1.")
steps = [("Data", "7 ETFs\nSPY, EFA, EEM,\nIEF, TLT, GLD, DBC\nDaily, 2005–2025"),
         ("Forecast", "Elastic Net\nRandom Forest\nGradient Boosting\n8 features\n60-month window"),
         ("Decision", "1/7 of portfolio\nper eligible fund\nif forecast > 0"),
         ("Validation", "7 gates:\nHygiene; economics\nPlacebos; DSR\nStability; robustness\n2023–2025 holdout")]
for i, (head, body) in enumerate(steps):
    x = 0.7 + i * 3.1
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(2.0), Inches(2.8), Inches(3.4))
    box.fill.solid()
    box.fill.fore_color.rgb = color(PALE)
    box.line.color.rgb = color(BLUE)
    text(s, head, x + 0.2, 2.2, 2.4, 0.5, size=22, fill=NAVY, bold=True)
    text(s, body, x + 0.2, 2.9, 2.45, 2.3, size=16)
text(s, "Timing controls: lagged features · labels used only once known · diagnostic cut at 2022",
     0.7, 5.8, 12.0, 0.6, size=16, fill=GRAY)

# Slide 3 — results.
s = slide("No ML strategy survives; costs are not the reason",
          f"All three ML strategies fail. Their Sharpe ratios are {en['sharpe']}, {rf['sharpe']} and "
          f"{gb['sharpe']}, with negative alphas, on their reported windows. Costs are not the reason: "
          "the gross Sharpe ratios are already too low. These cross-window comparisons are descriptive. Forecasts are worse than predicting zero for "
          "every return model. Elastic Net mostly collapses to a single average forecast, so it produces few distinct target changes.",
          "Sources: results.csv; costs-robustness.csv; diagnostics/summary.json. Unequal effective windows; comparison is descriptive.")
rows = [[name, results[name]["sharpe"], costs[name]["gross_sharpe"], results[name]["alpha_pct_pa"],
         results[name]["first_failed_gate"]]
        for name in ("Plain rule", "Elastic Net", "Random Forest", "Gradient Boosting")]
t = table(s, ["Strategy", "Net Sharpe", "Gross Sharpe", "Alpha (%/yr)", "First failed gate"],
          rows, 0.7, 1.6, 11.9, 2.9, size=20)
for j, width in enumerate((3.3, 2.0, 2.2, 2.2, 2.2)):
    t.columns[j].width = Inches(width)
t.rows[0].height = Inches(0.80)
for row in list(t.rows)[1:]:
    row.height = Inches(0.525)
for cell in t.rows[0].cells:
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.size = Pt(18)
        paragraph.space_after = Pt(0)
        paragraph.line_spacing = 1.0
text(s, f"All five return models: R² vs zero = {min(r2):.2f}% to {max(r2):.2f}%",
     0.7, 4.85, 12.0, 0.6, size=21, fill=NAVY, bold=True)
text(s, "Elastic Net: all slopes zero in 76.92% of refits → 17 clustered decisions",
     0.7, 5.55, 12.0, 0.6, size=21)

# Slide 4 — best follow-up and conclusion.
s = slide("Best follow-up still fails: do not deploy",
          f"My best economic follow-up weights trend positions by inverse volatility. Its Sharpe is "
          f"{best['sharpe']} and its alpha {best['alpha_pct_pa']} percent, but it beats only "
          f"{best['placebo_beaten_pct']} percent of placebos and its deflated Sharpe is "
          f"{costs['Volatility-weighted trend']['dsr']}, far below 0.90, so it is not a near-pass. "
          "This follow-up is exploratory: earlier holdouts were already seen. The lesson: a good backtest is not a validated strategy. I would not deploy any of them.",
          "Sources: results.csv and costs-robustness.csv (TM-017-10 report); manuscript Tables 1–3 and Section 4.")
cv = costs['Volatility-weighted trend']
t = table(s, ["Gate", "Requirement", "TM-017-10", "Result"], [
    ["2 Economic edge", "Net edge and doubled-cost resilience", f"{best['sharpe']} vs {best['benchmark_sharpe']}", "Pass"],
    ["3 Significance", "≥ 90% of placebos beaten", f"{best['placebo_beaten_pct']}%", "Fail"],
    ["4 Multiple testing", "Deflated Sharpe ≥ 0.90", cv['dsr'], "Fail"],
    ["6 Robustness", "Includes: one asset ≤ 30% of profit", f"{cv['largest_profit_asset']} {cv['largest_profit_share_pct']}%", "Pass"]],
    0.7, 1.55, 11.9, 3.0, size=19)
for j, width in enumerate((3.0, 4.6, 2.5, 1.8)):
    t.columns[j].width = Inches(width)
text(s, "Risks: 88 trials · holdout seen before follow-ups · 7 correlated funds · governance unassessed",
     0.7, 4.95, 11.9, 0.6, size=17, fill=GRAY)
text(s, "A good backtest is not a validated strategy: I would deploy none of them.", 0.7, 5.75, 11.9, 0.7,
     size=24, fill=TEAL, bold=True)

prs.save(OUT / "presentation.pptx")
spoken = sum(len(s.notes_slide.notes_text_frame.text.split()) for s in prs.slides)
script = ["# Two-minute defence script", "",
          f"Four slides, about thirty seconds each: {spoken} spoken words, roughly "
          f"{spoken / 140:.1f} minutes at 140 words per minute. "
          "Backup slides for questions: presentation-backup.pptx.", ""]
for i, current in enumerate(prs.slides, 1):
    title = next(sh.text for sh in current.shapes if sh.has_text_frame and sh.text)
    notes = current.notes_slide.notes_text_frame.text
    script += [f"## Slide {i} — {title}", "", notes, "", f"({len(notes.split())} words)", ""]
(OUT / "defence-script.md").write_text("\n".join(script).rstrip() + "\n")
print(f"Saved presentation.pptx with {len(prs.slides)} slides and defence-script.md.")
