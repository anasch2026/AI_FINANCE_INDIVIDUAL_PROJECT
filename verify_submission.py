"""Audit report provenance and submission requirements; never run an experiment."""
from pathlib import Path
from html.parser import HTMLParser
from decimal import Decimal
import csv
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'capstone'


class Table(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.rows=[]; self.row=[]; self.value=''; self.capture=False; self.feed(html)
    def handle_starttag(self, tag, attrs):
        if tag=='tr': self.row=[]
        if tag in ('th','td'): self.value=''; self.capture=True
    def handle_data(self, data):
        if self.capture: self.value+=data
    def handle_endtag(self, tag):
        if tag in ('th','td'): self.row.append(self.value.strip()); self.capture=False
        if tag=='tr' and self.row: self.rows.append(self.row)


def fields(nb, cell):
    value=next(o['data']['text/html'] for o in nb['cells'][cell]['outputs'] if 'text/html' in o.get('data',{}))
    rows=Table(''.join(value)).rows
    return dict(zip(rows[0][1:],rows[-1][1:]))


def fmt(value, percent=False):
    return f'{Decimal(value)*(100 if percent else 1):.2f}'


def tables(text):
    result=[]; current=[]
    for line in text.splitlines()+['']:
        if line.startswith('|'):
            row=[c.strip() for c in line.strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',v) for v in row): current.append(row)
        elif current: result.append(current); current=[]
    return result


def manuscript_paragraphs(text):
    """Expected visible paragraphs, including captions but excluding table cells."""
    lines=text.splitlines(); result=[]; i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line or line.startswith('|'):
            i+=1; continue
        if line.startswith('#'):
            result.append(line.lstrip('#').strip())
        elif line.startswith('!['):
            result.append(re.match(r'!\[(.*?)\]\(',line)[1])
        elif line.startswith('- '):
            result.append(line[2:])
        else:
            block=[line]
            while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].startswith(('#','|','![','- ')):
                i+=1; block.append(lines[i].strip())
            result.append(' '.join(block))
        i+=1
    return result


def main():
    checks=[]
    def check(condition,message):
        if not condition: raise AssertionError(message)
        checks.append(message)
    manifest=json.loads((ROOT/'RESEARCH-INPUTS.sha256.json').read_text())
    for name,expected in manifest['files'].items():
        check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'Unchanged input: '+name)
    text=(OUT/'manuscript.md').read_text()
    abstract=text.split('## Abstract\n',1)[1].split('\n## 1 ',1)[0]
    body=text.split('## 1 Introduction and Business Problem\n',1)[1].split('\n## References',1)[0]
    body_lines=[l for l in body.splitlines() if l.strip() and not l.startswith(('|','![','#','Table '))]
    body_words=len(' '.join(body_lines).split())
    refs=text.split('## References\n',1)[1].split('\n## Annex',1)[0]
    check(len(abstract.split())<=250,'Abstract within 250 words')
    check(2000<=body_words<=3000,'Body within 2000–3000 words')
    check(body_words+len(refs.split())<=3000,'Within 3000 words also when references are counted')
    for heading in ['## Abstract','## 1 Introduction and Business Problem','## 2 Data and Methodology','## 3 Empirical Results','## 4 Conclusion and Implementation Risks']:
        check(heading in text,'Required section: '+heading)
    mt=tables(text); check(len(mt)==4,'Four manuscript tables')
    results=list(csv.DictReader((OUT/'results.csv').open()))
    recorded=[r for r in results if r['trial_status']=='recorded']
    check(len(recorded)==7 and len(results)==11,'Seven recorded strategies and four unrun identifiers retained')
    for r in recorded:
        nb=json.loads((ROOT/r['source_file']).read_text())
        e,p,h=fields(nb,12),fields(nb,14),fields(nb,22)
        expected=[fmt(e['Sharpe']),fmt(e['alpha'],True),fmt(p['placebos beaten'],True),fmt(h['holdout Sharpe']),fmt(h['holdout alpha'],True)]
        actual=[r[k] for k in ['sharpe','alpha_pct_pa','placebo_beaten_pct','holdout_sharpe','holdout_alpha_pct_pa']]
        check(expected==actual,'Published financial metrics: '+r['card'])
        raw=next(o['data']['text/html'] for o in nb['cells'][24]['outputs'] if 'text/html' in o.get('data',{}))
        gates=[a[1].replace('passes','pass').replace('fails','fail') for a in Table(''.join(raw)).rows[2:]]
        check(gates==[r[f'gate_{i}'] for i in range(1,8)],'Published gate labels: '+r['card'])
        ident='-'.join(r['card'].split('-')[:3]); row=next(a for a in mt[1][1:] if a[0].startswith(ident+' '))
        check(row[1:]==[r['first_failed_gate']]+expected,'Manuscript Table 2: '+ident)
    cost_rows=list(csv.DictReader((OUT/'costs-robustness.csv').open()))
    for r,row in zip(cost_rows,mt[2][1:]):
        nb=json.loads((ROOT/r['source_file']).read_text()); e,d,st,rb=[fields(nb,n) for n in [12,16,18,20]]
        dsr='<0.01' if Decimal(d['DSR'])<Decimal('0.005') else fmt(d['DSR'])
        expected=[fmt(e['gross Sharpe']),fmt(e['Sharpe']),fmt(e['Sharpe at 2x costs']),fmt(e['costs a year'],True),st['positive blocks'],fmt(st['alpha without the best year'],True),dsr]
        check(row[1:]==expected,'Manuscript Table 3: '+r['card'])
        check(r['largest_profit_share_pct']==fmt(rb['largest P&L share'],True),'Published concentration: '+r['card'])
    overall={r['model']:r for r in csv.DictReader((OUT/'diagnostics/forecast-metrics.csv').open()) if r['scope']=='overall'}
    for row in mt[3][1:]:
        model=row[0].rstrip('*'); r=overall[model]
        expected=['n/a' if model=='Logistic Regression' else r['r2_zero_pct'],r['rank_ic'],r['rank_ic_t_hac3'],r['valid_ic_months'],r['sign_hit_pct'],r['auc'] or '—',r['log_loss'] or '—']
        check(row[1:]==expected,'Manuscript Table 4: '+model)
    figures=re.findall(r'!\[([^\]]+)\]\(([^)]+)\)',text)
    check(len(figures)==6 and all((OUT/p).is_file() for _,p in figures),'Six manuscript figures present')
    for filename in ['manuscript.docx','presentation.pptx','presentation-backup.pptx']:
        with zipfile.ZipFile(OUT/filename) as z: check(z.testzip() is None,'Valid Office archive: '+filename)
    from docx import Document
    from pptx import Presentation
    doc=Document(OUT/'manuscript.docx')
    check(len(doc.tables)==4 and len(doc.inline_shapes)==6,'Word contains four tables and six figures')
    check([[[c.text for c in r.cells] for r in t.rows] for t in doc.tables]==mt,'Word tables exactly match manuscript')
    check([p.text for p in doc.paragraphs if p.text.strip()]==manuscript_paragraphs(text),'All Word prose and captions exactly match manuscript')
    embedded=[hashlib.sha256(doc.part.related_parts[sh._inline.graphic.graphicData.pic.blipFill.blip.embed].blob).hexdigest() for sh in doc.inline_shapes]
    check(embedded==[hashlib.sha256((OUT/p).read_bytes()).hexdigest() for _,p in figures],'All Word figures exactly match the cited saved PNGs')
    prs=Presentation(OUT/'presentation.pptx'); backup=Presentation(OUT/'presentation-backup.pptx')
    check(len(prs.slides)==4 and len(backup.slides)==15,'Four defence slides and fifteen backup slides')
    spoken=sum(len(s.notes_slide.notes_text_frame.text.split()) for s in prs.slides)
    check(spoken<=250 and all(s.notes_slide.notes_text_frame.text.strip() for s in prs.slides),'Concise spoken script and notes on all four slides')
    script=(OUT/'defence-script.md').read_text()
    check(all(s.notes_slide.notes_text_frame.text in script for s in prs.slides),'Spoken script matches all defence notes')
    by_model={r['model']:r for r in recorded}; by_cost={r['model']:r for r in cost_rows}
    slide_table=next(sh.table for sh in prs.slides[2].shapes if sh.has_table)
    expected=[[m,by_model[m]['sharpe'],by_cost[m]['gross_sharpe'],by_model[m]['alpha_pct_pa'],by_model[m]['first_failed_gate']] for m in ['Plain rule','Elastic Net','Random Forest','Gradient Boosting']]
    check([[c.text for c in row.cells] for row in list(slide_table.rows)[1:]]==expected,'Main defence financial table matches archived results')
    check(all('R² is not defined for a binary target' not in s.notes_slide.notes_text_frame.text for s in backup.slides),'Backup notes distinguish return forecasts from classification probabilities')
    check(all(sh.left>=0 and sh.top>=0 and sh.left+sh.width<=prs.slide_width+3 and sh.top+sh.height<=prs.slide_height+3 for s in prs.slides for sh in s.shapes),'Defence elements within slide bounds')
    report={'abstract_words':len(abstract.split()),'body_words_excluding_abstract_tables_captions_references_annexes':body_words,'body_with_references':body_words+len(refs.split()),'spoken_words':spoken,'assumed_delivery_words_per_minute':140,'estimated_minutes_at_assumed_rate':round(spoken/140,2),'manuscript_tables':4,'manuscript_figures':6,'defence_slides':4,'backup_slides':15,'research_input_files_verified':len(manifest['files']),'checks_passed':len(checks),'experiments_rerun':False,'new_financial_metrics_computed':False,'scope':'Saved-output reconstruction and consistency audit; not fresh-environment re-estimation or a guaranteed grade.','checks':checks}
    (OUT/'verification-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
