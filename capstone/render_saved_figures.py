"""Render published diagnostic figures from archived CSVs only.

No lab/strategy imports, market loading, fitting, prediction or portfolio engine.
The plotting functions preserve the original chart definitions. Display precision
comes from the committed diagnostic CSVs; no performance metric is recomputed.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from local_plotting import configure
ROOT = configure()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
OUT = ROOT / 'capstone/diagnostics'
LOGISTIC_R2_NOTE = 'Return R² is n/a for the logistic probability forecast; use accuracy, AUC and log-loss.'

def fmt(value):
    return 'N/A' if value is None or not np.isfinite(value) else f'{value:.2f}'

def quality_chart(met):
    overall=met[met.scope=='overall']
    order=['OLS','Elastic Net','Random Forest','Gradient Boosting','Logistic Regression','MLP','Plain rule proxy']
    overall=overall.set_index('model').reindex([n for n in order if n in set(overall.model)]).reset_index()
    short={'OLS':'OLS','Elastic Net':'EN','Random Forest':'RF','Gradient Boosting':'GB','Logistic Regression':'Logit*','MLP':'MLP','Plain rule proxy':'Rule'}
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,key,title in zip(axes,['r2_zero_pct','rank_ic'],['Forecast R² vs zero (%)','Mean monthly cross-sectional rank IC']):
        values=overall[key].to_numpy(dtype=float).copy()
        if key=='r2_zero_pct':values[overall.model.eq('Logistic Regression').to_numpy()]=np.nan
        ax.bar(range(len(values)),values,color='#647c8c')
        ax.set_xticks(range(len(values)),[short[n] for n in overall.model]);ax.set_title(title);ax.axhline(0,color='gray',lw=0.7)
        for i,v in enumerate(values):ax.annotate('n/a' if key=='r2_zero_pct' and overall.model.iloc[i]=='Logistic Regression' else fmt(v),(i,0 if not np.isfinite(v) else v),xytext=(0,-14 if not np.isfinite(v) else 5 if v>=0 else -14),textcoords='offset points',ha='center')
        ax.margins(y=0.25)
        if key=='rank_ic':
            ax.yaxis.set_major_locator(MultipleLocator(0.05))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    fig.tight_layout(rect=(0,0.06,1,1))
    fig.text(0.02,0.01,'Source: diagnostics.py; no portfolio test.\n*'+LOGISTIC_R2_NOTE,fontsize=7)
    fig.savefig(OUT/'01-forecast-quality.png',dpi=180,bbox_inches='tight',metadata={'Description':'Source: capstone/diagnostics/diagnostics.py and forecast-metrics.csv; in-sample only, cutoff 2022-12-31.'})
    plt.close(fig)

def extended_charts(met,permutation,impurity):
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    quality_chart(met)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    yearly=met[met.scope=='year']
    for name,g in yearly[yearly.model!='Logistic Regression'].groupby('model',sort=False):axes[0].plot(g.group.astype(int),g.r2_zero_pct,label=name,lw=1,marker='.')
    axes[0].axhline(0,color='gray',lw=0.7);axes[0].set_title('Return/proxy R² vs zero (%)');axes[0].legend(fontsize=7,ncol=2)
    log=yearly[yearly.model=='Logistic Regression']
    axes[1].plot(log.group.astype(int),log.sign_hit_pct,label='Sign accuracy (%)',marker='.')
    axes[1].plot(log.group.astype(int),log.auc*100,label='AUC × 100',marker='.')
    axes[1].set_title('Logistic classification by year');axes[1].legend(fontsize=8)
    fig.tight_layout(rect=(0,0.07,1,1));fig.text(0.02,0.01,'Source: diagnostics.py / forecast-metrics.csv; before 2023 only; no portfolio test.',fontsize=8)
    fig.savefig(OUT/'02-yearly-accuracy.png',dpi=180,bbox_inches='tight',metadata={'Description':'Source: diagnostics.py and forecast-metrics.csv; in-sample only.'});plt.close(fig)
    features=['r21','r63','r126','r252','r252x21','vol63','vol126','ma200']
    fig,axes=plt.subplots(2,3,figsize=(13,8))
    for column,name in enumerate(['Random Forest','Gradient Boosting','MLP']):
        top,bottom=axes[0,column],axes[1,column]
        if name!='MLP':
            imp=impurity[impurity.model==name].set_index('feature').reindex(features)
            top.barh(features[::-1],imp['mean'][::-1],xerr=imp['std'][::-1],color='#647c8c',ecolor='#aaaaaa')
            top.set_xlabel('Training impurity mean ± refit SD')
        else:
            top.text(0.5,0.5,'No tree impurity importance',ha='center',va='center',transform=top.transAxes);top.set_axis_off()
        top.set_title(name)
        p=permutation[permutation.model==name].set_index('feature').reindex(features)
        bottom.barh(features[::-1],p.mean_bps2[::-1],xerr=p.refit_sd_bps2[::-1],color='#8b7360',ecolor='#aaaaaa')
        bottom.axvline(0,color='#555555',lw=0.8);bottom.set_xlabel('Next-month MSE increase (bp²) ± refit SD')
        bottom.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    fig.tight_layout(rect=(0,0.05,1,1));fig.text(0.02,0.01,'Source: diagnostics.py; fixed following-month permutations (10 repeats); 142 scored months; no portfolio return.',fontsize=8)
    fig.savefig(OUT/'06-permutation-importances.png',dpi=180,bbox_inches='tight',metadata={'Description':'Source: diagnostics.py, permutation-summary.csv and impurity-summary.csv; no holdout evaluation.'});plt.close(fig)

def coefficients_chart():
    """Draw coefficient histories already saved in return basis points."""
    fits = pd.read_csv(OUT / 'fit-history.csv')
    en = fits[fits.model == 'Elastic Net']
    features = ['r21','r63','r126','r252','r252x21','vol63','vol126','ma200']
    values = en[features].to_numpy().T
    limit = max(1, np.abs(values).max())
    fig, ax = plt.subplots(figsize=(10, 3.8))
    plot = ax.imshow(values, aspect='auto', cmap='RdBu_r', vmin=-limit, vmax=limit)
    ax.set_yticks(range(len(features)), features)
    ticks = np.linspace(0, len(en)-1, 6, dtype=int)
    ax.set_xticks(ticks, en.date.iloc[ticks].str[:7], rotation=20)
    ax.set_title('Elastic Net coefficients: return basis points per feature standard deviation')
    fig.colorbar(plot, ax=ax, label='Basis points')
    fig.tight_layout(rect=(0,0.06,1,1))
    fig.text(0.02,0.01,'Source: archived fit-history.csv; rounded coefficients; no model refitted.',fontsize=8)
    fig.savefig(OUT/'03-elastic-net-coefficients.png',dpi=180,bbox_inches='tight',
                metadata={'Description':'Source: capstone/diagnostics/fit-history.csv; display from archived coefficients only.'})
    plt.close(fig)


def main():
    metrics = pd.read_csv(OUT/'forecast-metrics.csv',dtype={'group':str})
    permutation = pd.read_csv(OUT/'permutation-summary.csv')
    impurity = pd.read_csv(OUT/'impurity-summary.csv')
    extended_charts(metrics, permutation, impurity)
    coefficients_chart()
    print('Rebuilt diagnostic figures from archived CSVs; no data loading or estimation.')


if __name__ == '__main__':
    main()
