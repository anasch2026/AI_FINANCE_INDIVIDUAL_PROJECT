"""Create the fifteen-slide backup deck for questions from saved results only."""
from pathlib import Path
import csv
import json
from local_plotting import configure
ROOT = configure()
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

OUT = ROOT / 'capstone'
rows = [r for r in csv.DictReader((OUT/'results.csv').open()) if r['trial_status']=='recorded']
r = {row['model']:row for row in rows}
diagnostic = json.loads((OUT/'diagnostics/summary.json').read_text())
prs = Presentation()
prs.slide_width,prs.slide_height = Inches(13.33),Inches(7.5)
prs.core_properties.author='Anas Chantah'
prs.core_properties.title='Do machine-learning trend signals survive strict validation?'
NAVY='24364B';BLUE='627D8C';INK='25313C';GRAY='65727D';PALE='EEF2F5'


def text(slide,value,x,y,w,h,size=22,color=INK,bold=False):
    box=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=box.text_frame;tf.word_wrap=True
    tf.margin_left=tf.margin_right=0
    for i,line in enumerate(value.split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.text=line;p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color)
        p.space_after=Pt(12)
    return box


def slide(title,source,notes):
    s=prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor(255,255,255)
    band=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,prs.slide_width,Inches(0.12))
    band.fill.solid();band.fill.fore_color.rgb=RGBColor.from_string(NAVY);band.line.fill.background()
    text(s,title,0.6,0.4,12.1,0.85,size=28,color=NAVY,bold=True)
    text(s,source,0.6,7.0,11.7,0.25,size=9,color=GRAY)
    num=text(s,str(len(prs.slides)),12.1,7.0,0.6,0.25,size=10,color=GRAY)
    num.text_frame.paragraphs[0].alignment=PP_ALIGN.RIGHT
    s.notes_slide.notes_text_frame.text=notes+'\n\nSources: '+source
    return s


def bullets(s,items,y=1.65,size=24):
    for i,item in enumerate(items):
        text(s,item,0.85,y+i*1.05,11.6,0.95,size=size)


def chart(s,path,y=1.75,height=4.85):
    p=OUT/path
    with Image.open(p) as im: ratio=im.width/im.height
    w=min(12.0,height*ratio);h=w/ratio
    s.shapes.add_picture(str(p),Inches((13.33-w)/2),Inches(y),width=Inches(w),height=Inches(h))



def tree_importance_chart():
    """Display saved mean importances only; never load market data or fit models."""
    source = OUT / 'diagnostics/permutation-summary.csv'
    means = {(row['model'], row['feature']): float(row['mean_bps2'])
             for row in csv.DictReader(source.open())}
    features = ['r21', 'r63', 'r126', 'r252', 'r252x21', 'vol63', 'vol126', 'ma200']
    labels = ['21-session return', '63-session return', '126-session return',
              '252-session return', '12–1 momentum', '63-session volatility (vol63)',
              '126-session volatility', 'Distance from 200-session average']
    fig, ax = plt.subplots(figsize=(14, 6.4))
    gray, teal = '#74838E', '#007F73'
    for model, offset, hatch in [('Random Forest', -0.17, None),
                                  ('Gradient Boosting', 0.17, '///')]:
        # Rescaling is a unit conversion, not a new estimate: bp² / 1,000.
        values = [means[(model, feature)] / 1000 for feature in features]
        ax.barh([i + offset for i in range(len(features))], values, height=0.29,
                color=[teal if f == 'vol63' else gray for f in features],
                hatch=hatch, edgecolor='white', linewidth=0.5, zorder=3)
    ax.set_yticks(range(len(features)), labels, fontsize=17)
    ax.invert_yaxis()
    for label, feature in zip(ax.get_yticklabels(), features):
        if feature == 'vol63':
            label.set_color(teal)
            label.set_fontweight('bold')
    ax.axvline(0, color='#394651', linewidth=1.1, zorder=2)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.tick_params(axis='x', labelsize=17, length=0, pad=8)
    ax.tick_params(axis='y', length=0, pad=14)
    ax.set_xlabel('Mean next-month MSE increase (thousand bp²)', fontsize=18, labelpad=12)
    ax.grid(axis='x', color='#E5E9EC', linewidth=0.8, zorder=0)
    ax.margins(x=0.10, y=0.06)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(handles=[Patch(facecolor=gray, label='Random Forest'),
                       Patch(facecolor=gray, edgecolor='white', hatch='///', label='Gradient Boosting'),
                       Patch(facecolor=teal, label='vol63 highlighted')],
              loc='lower left', bbox_to_anchor=(0, 1.03), ncol=3,
              frameon=False, fontsize=15, handlelength=1.8, columnspacing=1.5)
    fig.subplots_adjust(left=0.34, right=0.985, top=0.86, bottom=0.16)
    path = Path('diagnostics/07-tree-permutation-importance.png')
    fig.savefig(OUT / path, dpi=200, bbox_inches='tight',
                metadata={'Description': 'Source: capstone/diagnostics/permutation-summary.csv; '
                          'mean_bps2 for Random Forest and Gradient Boosting; '
                          'display unit: thousand basis points squared. No refit or new metric.'})
    plt.close(fig)
    return path


def table(s,headers,values,y=2.0,height=3.4):
    shape=s.shapes.add_table(len(values)+1,len(headers),Inches(0.7),Inches(y),Inches(11.9),Inches(height))
    t=shape.table
    for j,v in enumerate(headers):t.cell(0,j).text=v
    for i,row in enumerate(values,1):
        for j,v in enumerate(row):t.cell(i,j).text=str(v)
    for i,row in enumerate(t.rows):
        for cell in row.cells:
            cell.fill.solid();cell.fill.fore_color.rgb=RGBColor.from_string(NAVY if i==0 else (PALE if i%2 else 'FFFFFF'))
            cell.vertical_anchor=MSO_ANCHOR.MIDDLE
            cell.margin_left=Inches(0.12)
            for p in cell.text_frame.paragraphs:
                p.font.name='Aptos';p.font.size=Pt(18);p.font.bold=i==0;p.font.color.rgb=RGBColor.from_string('FFFFFF' if i==0 else INK)
    return t


s=slide('Do ML trend signals survive strict validation?',
        'Saved reports: TM-017-01/06/07/08/10; MR-001-01/02. TM-017-09 unrun. results-notes.md.',
        'The original ML cards do not survive validation. The diagnostic now compares six fixed learners, including OLS, logistic regression and a small network, without adding a strategy or portfolio trial. Both reversal follow-ups fail economics. TM-017-09 remains skipped, while its separately fixed repair, TM-017-10, passes economics and robustness but fails significance and multiple testing. Forecast evaluation and investment validation are distinct conclusions.')
text(s,'A complete research cycle',0.85,1.75,11.5,0.7,size=33,color=BLUE,bold=True)
bullets(s,['Hypothesis → test → failure → diagnosis → new hypotheses → results',
           'No tested strategy passes all seven gates.',
           'Anas Chantah | Master in Finance | IE Business School'],y=3.0,size=23)

s=slide('My contribution is the ML application and the research',
        'Prior work attribution: github.com/Sami-Andaloussi/alpha-factory. Disclosure: manuscript.md.',
        'Alpha Factory is prior work I co-founded with Sami Andaloussi. My course contribution is the ML layer, diagnostic, follow-ups, experiments and analysis under my name. Claude and OpenAI Codex assisted with coding and drafting. Four follow-up cards are specified overall, three with financial runs and one skipped. The repair was fixed before its run and changes only undefined-volatility membership; 09 had no result to tune against. Completed cards and earlier numbers remain unchanged.')
bullets(s,['Prior work: Alpha Factory, co-founded with Sami Andaloussi.',
           'New work: forecasts, diagnostic, hypothesis, experiments and analysis.',
           'AI assistance disclosed: Claude and OpenAI Codex.',
           'Four follow-ups specified; three run, one skipped; no post-result tuning.'],size=22)

s=slide('The model changes the entry decision, not the allocation',
        'ML card.yaml and strategy.py files; report.ipynb cell 4; diagnostics/summary.json.',
        'The funds are SPY, EFA, EEM, IEF, TLT, GLD and DBC. Each forecast uses eight lagged price features: several return horizons, skip-month momentum, volatility and moving-average distance. I pool fund-months, refit on sixty completed months, and hold a seventh per fund if its forecast exceeds zero. Elastic Net regularises a linear relationship; the forest and boosting models allow nonlinear relationships. Their settings were fixed before the original runs. The declared in-sample period is 2005 to 2022, but the actual ML performance window begins in February 2011.')
bullets(s,['Seven funds; eight lagged price features.',
           'Rolling 60-month estimation; monthly refitting.',
           'Positive next-month excess-return forecast → hold one seventh.',
           'Declared IS: 2005–2022 | holdout: 2023–2025.'],size=22)

s=slide('The first failed gate defines the verdict',
        'figures/01-gates.png; all report.ipynb files, cell 24; battery.py.',
        'The battery tests hygiene, economics, significance, multiple testing, stability, robustness and holdout. The first failure determines rejection. Elastic Net fails evidence sufficiency; the ensembles and reversal cards fail economics. The plain rule and the repaired volatility-weighted rule first fail significance. The repaired rule also passes robustness, which is a favourable recorded result but not full validation. Different historical threshold versions and the missing paired comparison limit interpretation. Forecast-only OLS, logistic and MLP do not receive gate verdicts.')
chart(s,Path('figures/01-gates.png'))

s=slide('The original ML cards do not establish economic edge',
        'TM-017-01/06/07/08 report.ipynb cells 12 and 24; results.csv.',
        'These are net excess-return Sharpes and annual regression alphas against passive equal-weight holding, not against the trend rule. Elastic Net has only seventeen clustered decisions, so its first failure is hygiene, although its alpha is also negative. The two ensembles have enough decisions but fail economics immediately. Different effective evaluation windows prevent a clean ranking against the historical rule. In addition, lab.compare cannot authenticate the missing historical reference commit. I therefore present this table descriptively and make no paired estimate or statistical superiority claim.')
values=[]
for name in ['Plain rule','Elastic Net','Random Forest','Gradient Boosting']:
    row=r[name];values.append([name,row['sharpe'],row['alpha_pct_pa'],row['first_failed_gate']])
table(s,['Strategy','IS Sharpe','Alpha (%/year)','First failed gate'],values)
text(s,'Alpha is against passive holding. Effective evaluation windows differ.',0.85,6.05,11.5,0.6,size=18,color=GRAY)

s=slide('Forecast accuracy is weak before portfolio construction',
        'diagnostics/01-forecast-quality.png; forecast-metrics.csv; diagnostics.py.',
        'The diagnostic cuts raw inputs before market assembly and uses no holdout observation or portfolio return. The common scored sample contains 994 fund-months. Return R squared is negative for all five return regressors, and the tree ensembles have negative mean monthly rank information coefficients. Logistic R squared is displayed as n/a, as explained on the next slide. Elastic Net has only thirty-two valid IC months because many forecasts are constant across funds, so its IC average needs care. The rule is a sign signal, so its R squared uses a declared mechanical monthly scaling proxy; that number is contextual rather than a calibrated model comparison.')
chart(s,Path('diagnostics/01-forecast-quality.png'))

s=slide('Six models, same verdict',
        'diagnostics/forecast-metrics.csv; diagnostics.py; all figures before 2023.',
        'The shared scored sample and fixed protocol compare six learners and a rule proxy. OLS and MLP have negative return R squared, like the original regressors. Logistic regression predicts the probability of a positive return. R² is not defined for a binary target, so I judge the classifier by accuracy, AUC and log-loss, and all three are weak. The common conclusion is weak forecast evidence on this sample, not six failed trading cards. No new portfolio return, holdout evaluation or registry trial is produced by this extension.')
metric_rows=[]
for name in ['OLS','Elastic Net','Random Forest','Gradient Boosting','Logistic Regression','MLP','Plain rule proxy']:
    m=next(v for v in diagnostic['overall'] if v['model']==name)
    label={'Logistic Regression':'Logistic*','Gradient Boosting':'Boosting','Plain rule proxy':'Rule proxy'}.get(name,name)
    metric_rows.append([label,'n/a' if name=='Logistic Regression' else f"{m['r2_zero_pct']:.2f}",f"{m['rank_ic']:.2f}",f"{m['rank_ic_t_hac3']:.2f}",f"{m['sign_hit_pct']:.2f}",f"{m['auc']:.2f}" if m.get('auc') is not None else '—',f"{m['log_loss']:.2f}" if m.get('log_loss') is not None else '—'])
t=table(s,['Model','R² (%)','Rank IC','IC t','Hit (%)','AUC','Log-loss'],metric_rows,y=1.5,height=4.9)
for row in t.rows:
    for cell in row.cells:
        for paragraph in cell.text_frame.paragraphs:paragraph.font.size=Pt(16)
text(s,'*Return R² is n/a for logistic probabilities; accuracy, AUC and log-loss evaluate the classifier.',0.8,6.5,11.8,0.4,size=15,color=GRAY)

s=slide('Elastic Net mostly learns a pooled intercept',
        'diagnostics/03-elastic-net-coefficients.png; summary.json; decision-behaviour.csv.',
        'All Elastic Net slopes are zero in 76.92 percent of monthly fits. When this happens, every fund receives the same forecast from the pooled intercept. Positive forecasts account for 96.90 percent of its decision history and it holds an average of 6.78 funds. Refitting is frequent, but target signs rarely change. The reconstructed target history reproduces exactly the seventeen clustered decisions in the official report. I did not lower the penalty or change the old card to obtain more decisions.')
text(s,'76.92% zero-slope refits | 96.90% positive forecasts | 17 clustered decisions',0.8,1.35,11.8,0.55,size=19,color=BLUE,bold=True)
chart(s,Path('diagnostics/03-elastic-net-coefficients.png'),y=2.0,height=4.55)

s=slide('Only volatility has positive tree importance',
        'diagnostics/07-tree-permutation-importance.png; diagnostics/permutation-summary.csv; diagnostics/importance-stability.csv.',
        'The adjacent training-importance rank correlations remain 0.82 and 0.79, but persistence is not predictive skill. Following-month permutation evaluates a frozen model on only that next month’s seven observations. Most tree features have negative mean permutation importance; vol63 is the only positive mean for each ensemble. The MLP has mixed signs and large refit dispersion. Positive training impurity importance can coexist with worse future prediction. These are noisy descriptive means from the pre-2023 sample, not the holdout, and neither causal effects nor significance tests. No feature subset or new model setting is selected from it.\nBars are in thousands of basis points squared; teal marks vol63.')
chart(s,tree_importance_chart(),y=1.35,height=5.40)

s=slide('First follow-up: liquidity reversal after a decline',
        'MR-001-01 card.yaml and reasoning.md; bank/MR-001; Nagel (2012).',
        'The diagnostic gives no reason to add model complexity. I instead test a distinct mechanism from the literature: providing liquidity after selling pressure may earn a rebound. The rule buys a fund after its trailing twenty-one-session return underperforms the bill. It uses the same monthly schedule and equal allocation slots, with no fitted coefficients. The horizon and zero boundary are economic conventions, not choices selected by a backtest. I locked the card alone, then wrote code and ran it once. Earlier holdout results had already been seen, so this remains an exploratory follow-up with that limitation disclosed.')
bullets(s,['MR-001-01: a distinct economic hypothesis, not a repaired ML card.',
           'Trailing 21-session return below the bill → buy that fund.',
           'One base variant; prescribed neighbours; bounded memory.',
           'Card locked before code; one run; prior holdout exposure disclosed.'],size=21)

s=slide('Follow-up 1 also fails economic edge',
        'MR-001-01 report.ipynb cells 10–24; results.csv.',
        'The official run passes timing, memory and decision-count checks, with 205 clustered decisions. It then fails economics: Sharpe is 0.24 against the benchmark 0.45, and annual alpha is minus 1.07 percent. Its placebo-beaten fraction is 37.10 percent, far below the required ninety percent. Stability and concentration also fail. The holdout cannot cancel the first failure, and the strategy stays unchanged. I then fixed two further rules before either of their cards ran.'
        '\nNagel (2012) finds little unconditional reversal profit in diversified industry portfolios and profitability mainly at high VIX; MR-001-01 uses diversified ETFs without volatility conditioning, so its failure is consistent with that evidence.')
row=r['Liquidity reversal']
table(s,['Recorded metric','Outcome'],[
    ['First failed gate','2 — Economic edge'],['IS Sharpe / benchmark',row['sharpe']+' / '+row['benchmark_sharpe']],
    ['Annual alpha',row['alpha_pct_pa']+'%'],['Shifted placebos beaten',row['placebo_beaten_pct']+'%']],height=3.8)

s=slide('Follow-up 2: stress does not validate reversal',
        'MR-001-02 card.yaml; report.ipynb cells 10–24; results.csv.',
        'I fixed this stress condition before the run. SPY realised volatility over sixty-three sessions must exceed the median of its preceding 756 volatility observations. Only then does the rule buy funds below the bill over the fixed base return horizon. It passes hygiene with 92 clustered decisions but fails economic edge and later significance, stability and robustness. GLD accounts for 84.15 percent of profit. The favourable holdout does not rescue it. This proxy is realised volatility, not Nagel’s VIX state. Its shorter effective window also prevents a paired claim against unconditional reversal. The added trial remains in gate four.')
row=r['Stress reversal']
table(s,['Recorded metric','Outcome'],[
    ['First failed gate','2 — Economic edge'],['IS Sharpe / benchmark',row['sharpe']+' / '+row['benchmark_sharpe']],
    ['Annual alpha',row['alpha_pct_pa']+'%'],['Shifted placebos beaten',row['placebo_beaten_pct']+'%']],height=3.8)

s=slide('TM-017-10 repairs 09 but fails gates 3 and 4',
        'TM-017-10 report.ipynb cells 12–24; TM-017-09 remains skipped; STOPPED.md.',
        'TM-017-09 remains skipped at preflight and has no return result. I then fixed a separate card, 10, changing only the undefined case: a fund without defined volatility is neither held nor included in the sum. The repaired rule passes hygiene, economics and robustness; SPY’s largest profit share is 28.55 percent. It first fails significance with 89.80 percent of placebos beaten against ninety percent required. Its DSR of 0.27 is far below the 0.90 required, so gate four also fails, and the blend fails stability. It is not a near-pass and not a paired proof of improvement. No threshold or setting is changed after the result.\nIts use of volatility is consistent with the permutation result, but not causally linked: the card was specified before the extended diagnostic.')
row=r['Volatility-weighted trend']
table(s,['Recorded metric','Outcome'],[
    ['First failed gate','3 — Significance'],['IS Sharpe / annual alpha',row['sharpe']+' / '+row['alpha_pct_pa']+'%'],
    ['Shifted placebos beaten',row['placebo_beaten_pct']+'%'],['Robustness / DSR','Gate 6 passes / 0.27 (needs 0.90)']],height=3.8)

s=slide('A positive holdout Sharpe is not value added',
        'figures/04-holdout.png; report.ipynb cell 22; battery.py, decide_holdout().',
        'Elastic Net has holdout Sharpe 0.91 versus the rule’s 0.89, but its alpha rounds to slightly negative zero while the rule’s is 0.61 percent. Sharpe measures excess return relative to volatility. Alpha measures return beyond benchmark exposure. The apparent paradox disappears when I separate these questions. Gate seven is also a lower-tail decay diagnostic, so it does not require positive alpha. Both reversal rules have positive holdout alpha but fail earlier gates, while TM-017-10’s holdout alpha is slightly negative. I report all these outcomes and compute no new holdout return or forecast outside the official runs.')
chart(s,Path('figures/04-holdout.png'))

s=slide('The contribution is a transparent negative research cycle',
        'manuscript.md; results-notes.md; STOPPED.md; full local experiment record.',
        'The original ML cards fail validation, and the fixed six-model diagnostic provides weak forecast evidence without adding trading trials. Both reversal cards fail economics. The repaired volatility-weighted rule passes economics and robustness but fails significance and multiple testing. Its positive result on individual criteria remains visible alongside rejection. Four follow-up specifications contain three financial trials and one skipped preflight. Earlier holdouts were seen; paired comparison remains unavailable and effective windows differ. I retain every result, display logistic R squared as n/a and do not use importance to tune another model.')
bullets(s,['Weak forecast evidence across six fixed learners; no new ML strategy.',
           'TM-017-10 clears economics and robustness, but fails gates 3 and 4.',
           'Four follow-ups: three financial trials; 09 remains skipped.',
           'Prior exposure and accumulated trials limit confirmation.'],size=21)

prs.save(OUT/'presentation-backup.pptx')
outline=['# Individual defence — slide outline and speaker notes', '', 'Backup deck for questions: fifteen slides with the same speaker notes as presentation-backup.pptx. The two-minute defence itself is presentation.pptx (build_defence.py, defence-script.md).', '']
for index,current in enumerate(prs.slides,1):
    texts=[shape.text for shape in current.shapes if shape.has_text_frame and shape.text]
    outline.extend([f'## Slide {index} — {texts[0]}', '', 'Speaker notes:', '', current.notes_slide.notes_text_frame.text, ''])
(OUT/'presentation-outline.md').write_text('\n'.join(outline).rstrip()+'\n')
print('Saved presentation-backup.pptx with',len(prs.slides),'slides and speaker notes.')
