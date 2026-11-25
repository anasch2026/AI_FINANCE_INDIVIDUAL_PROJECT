"""Export capstone/manuscript.md to capstone/manuscript.docx.

Needs only python-docx (no matplotlib, notebook, strategy or market data), so the
Word file can be rebuilt on any machine. Figures are embedded from the PNG files
the manuscript references. Run from the repository root:

    python -B capstone/export_docx.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "capstone"


def export_docx():
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = section.bottom_margin = Inches(0.75)
    section.left_margin = section.right_margin = Inches(0.75)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing = 1.08
    normal.paragraph_format.space_after = Pt(7)
    doc.core_properties.author = "Anas Chantah"
    doc.core_properties.title = "Do machine-learning trend signals survive strict validation?"
    header = section.header.paragraphs[0]
    header.text = "Anas Chantah | AI for Finance"
    header.runs[0].font.size = Pt(8)
    footer = section.footer.paragraphs[0]
    footer.alignment = 2
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    footer._p.append(field)
    lines = (OUT / "manuscript.md").read_text().splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("<!--"):
            comment = line
            while "-->" not in comment:
                index += 1
                comment += " " + lines[index].strip()
            text = comment.replace("<!--", "").replace("-->", "").strip()
            p = doc.add_paragraph(text)
            for run in p.runs:
                run.font.size = Pt(7)
                run.font.color.rgb = RGBColor.from_string("666666")
        elif line.startswith("!["):
            match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            doc.add_picture(str(OUT / match[2]), width=Inches(6.5))
            doc.paragraphs[-1].paragraph_format.keep_with_next = True
            doc.add_paragraph(match[1], style="Caption")
        elif line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [c.strip() for c in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                index += 1
            t = doc.add_table(rows=1, cols=len(rows[0]))
            t.style = "Light Shading Accent 1"
            repeat = OxmlElement('w:tblHeader')
            t.rows[0]._tr.get_or_add_trPr().append(repeat)
            for c, value in zip(t.rows[0].cells, rows[0]):
                c.text = value
            for row in rows[1:]:
                for c, value in zip(t.add_row().cells, row):
                    c.text = value
            for row in t.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        for run in p.runs:
                            run.font.size = Pt(9 if len(rows[0]) == 3 else 8)
            continue
        elif re.match(r'Table \d+\.', line):
            caption = doc.add_paragraph(line, style='Caption')
            caption.paragraph_format.keep_with_next = True
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            doc.add_heading(line[level:].strip(), level=min(level - 1, 3))
        elif line.startswith("- "):
            doc.add_paragraph(line[2:], style="List Bullet")
        else:
            block = [line]
            while index + 1 < len(lines) and lines[index + 1].strip() and not lines[index + 1].startswith(("#", "|", "<!--", "![", "- ")):
                index += 1
                block.append(lines[index].strip())
            doc.add_paragraph(" ".join(block))
        index += 1
    doc.save(OUT / "manuscript.docx")


if __name__ == "__main__":
    export_docx()
    print("Exported capstone/manuscript.docx from capstone/manuscript.md.")
