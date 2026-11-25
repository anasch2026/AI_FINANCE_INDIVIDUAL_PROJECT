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
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
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
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = 1.08
    normal.paragraph_format.space_after = Pt(7)
    for name, size in [('Title', 24), ('Heading 1', 14), ('Heading 2', 12), ('Heading 3', 11), ('Caption', 9)]:
        style = doc.styles[name]
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.font.size = Pt(size)
        if style.paragraph_format.element.pPr is not None:
            for border in list(style.paragraph_format.element.pPr.findall(qn('w:pBdr'))):
                border.getparent().remove(border)
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
    annex = False
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
            t.style = "Table Grid"
            t.autofit = False
            if len(rows[0]) == 3:
                widths = [1.10, 1.75, 3.92]
            elif len(rows[0]) == 7:
                widths = [1.85, 0.60, 0.65, 0.82, 0.95, 0.87, 1.03]
            elif rows[0][0] == 'Strategy':
                widths = [1.60, 0.65, 0.65, 0.75, 0.75, 0.80, 0.95, 0.62]
            else:
                widths = [1.50, 0.83, 0.60, 0.60, 0.65, 0.85, 0.70, 1.04]
            for column, width in zip(t.columns, widths):
                column.width = Inches(width)
            repeat = OxmlElement('w:tblHeader')
            t.rows[0]._tr.get_or_add_trPr().append(repeat)
            for c, value in zip(t.rows[0].cells, rows[0]):
                c.text = value
            for row in rows[1:]:
                for c, value in zip(t.add_row().cells, row):
                    c.text = value
            for ri, row in enumerate(t.rows):
                row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
                for ci, cell in enumerate(row.cells):
                    cell.width = Inches(widths[ci])
                    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    properties = cell._tc.get_or_add_tcPr()
                    shading = OxmlElement('w:shd')
                    shading.set(qn('w:fill'), '24364B' if ri == 0 else ('F0F3F5' if ri % 2 else 'FFFFFF'))
                    properties.append(shading)
                    borders = OxmlElement('w:tcBorders')
                    for edge in ('top', 'left', 'bottom', 'right'):
                        border = OxmlElement('w:' + edge)
                        for k, value in [('val', 'single'), ('sz', '4'), ('color', 'D9D9D9')]:
                            border.set(qn('w:' + k), value)
                        borders.append(border)
                    properties.append(borders)
                    padding = OxmlElement('w:tcMar')
                    for edge in ('top', 'left', 'bottom', 'right'):
                        margin = OxmlElement('w:' + edge)
                        margin.set(qn('w:w'), '65')
                        margin.set(qn('w:type'), 'dxa')
                        padding.append(margin)
                    properties.append(padding)
                    for p in cell.paragraphs:
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.line_spacing = 1.0
                        if ci > 0 and len(rows[0]) > 3:
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        for run in p.runs:
                            run.font.size = Pt(9)
                            run.font.bold = ri == 0
                            run.font.color.rgb = RGBColor.from_string('FFFFFF' if ri == 0 else '000000')
            spacer = doc.add_paragraph()
            spacer.paragraph_format.space_after = Pt(2)
            spacer.paragraph_format.space_before = Pt(0)
            spacer.paragraph_format.line_spacing = Pt(2)
            continue
        elif re.match(r'Table \d+\.', line):
            caption = doc.add_paragraph(line, style='Caption')
            caption.paragraph_format.keep_with_next = True
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            annex = annex or line.startswith('## Annex')
            doc.add_heading(line[level:].strip(), level=min(level - 1, 3))
        elif line.startswith("- "):
            doc.add_paragraph(line[2:], style="List Bullet")
        else:
            block = [line]
            while index + 1 < len(lines) and lines[index + 1].strip() and not lines[index + 1].startswith(("#", "|", "<!--", "![", "- ")):
                index += 1
                block.append(lines[index].strip())
            p = doc.add_paragraph(" ".join(block))
            if annex:
                p.paragraph_format.keep_together = True
        index += 1
    doc.save(OUT / "manuscript.docx")


if __name__ == "__main__":
    export_docx()
    print("Exported capstone/manuscript.docx from capstone/manuscript.md.")
