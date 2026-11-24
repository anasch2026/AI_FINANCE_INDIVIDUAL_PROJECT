"""Forecast diagnostics only. No portfolio return, backtest, or holdout computation.

Run from the repository root with the repository virtual environment activated.
The lab loader is used with a process-local read adapter truncating every raw
frame BEFORE assemble(), so even ancillary market construction excludes holdout.
Original strategy sources are compiled and executed, never edited. A fitted()
observer records returned estimators without changing fitting or forecasts.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'capstone'))
from local_plotting import configure
configure()
sys.path.insert(0, str(ROOT / 'alpha-lab'))
import hashlib
import json
import types
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from sklearn.exceptions import ConvergenceWarning
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neural_network import MLPRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score, log_loss
from lab import data, stats

OUT = ROOT / 'capstone/diagnostics'
END = pd.Timestamp('2022-12-31')
FUNDS = ['SPY', 'EFA', 'EEM', 'IEF', 'TLT', 'GLD', 'DBC']
LOGISTIC_R2_NOTE = 'R² is not defined for a binary target; the logistic model is judged by accuracy, AUC and log-loss.'

CARDS = [('Elastic Net', 'TM-017-06-elastic-net-trend', 'elastic-net'), ('Random Forest', 'TM-017-07-random-forest-trend', 'random-forest'), ('Gradient Boosting', 'TM-017-08-boosted-trend', 'gradient-boosting')]


def raw_inside(path):
    frame = pd.read_csv(path, index_col='Date', parse_dates=['Date'])
    return frame.loc[:END].copy()


def load_inside():
    original = data.read
    data.read = raw_inside
    try:
        full = data.load(start='2005-01-01', end=str(END.date()))
    finally:
        data.read = original
    market = data.Market(full.prices[FUNDS], full.tradable[FUNDS], full.rf, full.signal_prices[FUNDS])
    assert market.prices.index.max() <= END and market.rf.index.max() <= END
    return market


def rankcorr(x, y):
    x, y = np.asarray(x), np.asarray(y)
    if len(x) < 3 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return np.nan
    return float(pd.Series(x).rank().corr(pd.Series(y).rank()))


def mean_t(values):
    """Mean and Newey-West t statistic, predeclared lag 3, no significance claim."""
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return np.nan, np.nan, 0
    mean = float(x.mean())
    if len(x) < 4:
        return mean, np.nan, len(x)
    z = x - mean
    v = float(z @ z / len(x))
    for lag in range(1, min(3, len(x)-1)+1):
        v += 2 * (1-lag/4) * float(z[lag:] @ z[:-lag] / len(x))
    return mean, mean / np.sqrt(v/len(x)) if v > 0 else np.nan, len(x)


def metrics(frame, scope, group):
    y, p = frame.actual.to_numpy(), frame.forecast.to_numpy()
    r2 = 1 - np.sum((y-p)**2)/np.sum(y*y) if np.sum(y*y) > 0 else np.nan
    monthly = [rankcorr(g.forecast, g.actual) for _, g in frame.groupby('date')]
    ic, t, n = mean_t(monthly)
    if scope == 'fund':
        ic, t, n = rankcorr(p, y), np.nan, len(frame)
    return dict(model=frame.model.iloc[0], scope=scope, group=str(group), observations=len(frame),
                months=frame.date.nunique(), r2_zero_pct=100*r2, rank_ic=ic,
                rank_ic_t_hac3=t, valid_ic_months=n if scope != 'fund' else 0,
                sign_hit_pct=100*np.mean((p>0)==(y>0)), positive_forecasts_pct=100*np.mean(p>0))


def clean(value):
    if isinstance(value, dict): return {k: clean(v) for k,v in value.items()}
    if isinstance(value, list): return [clean(v) for v in value]
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (float, np.floating)): return round(float(value), 2) if np.isfinite(value) else None
    return value


def fmt(value):
    return 'N/A' if value is None or not np.isfinite(value) else f'{value:.2f}'


def run():
    market = load_inside()
    observations, fitted_rows, decisions, hashes = [], [], [], {}
    all_forecasts = {}
    for name, ident, model in CARDS:
        path = ROOT / 'alpha-lab/strategies' / ident / 'strategy.py'
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        module = types.ModuleType('diagnostic_' + model.replace('-', '_'))
        module.__file__ = str(path)
        exec(compile(path.read_text(), str(path), 'exec'), module.__dict__)
        fits = []
        original = module.fitted
        def observe(*args, _original=original, **kwargs):
            result = _original(*args, **kwargs)
            fits.append(result)
            return result
        module.fitted = observe
        print('FORECAST', name, 'on truncated market ending', market.prices.index.max(), flush=True)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', ConvergenceWarning)
            forecasts = module.forecasts(market, model=model, window=60, memory=2400)
        forecasts = forecasts.dropna(how='all')
        assert forecasts.index.max() <= END and len(fits) == len(forecasts)
        all_forecasts[name] = forecasts
        for date, fit in zip(forecasts.index, fits):
            estimator, mean, std, scale = fit
            row = dict(model=name, date=str(date.date()), n_train=int(estimator.n_features_in_))
            if model == 'elastic-net':
                row['all_coefficients_zero'] = int(np.all(estimator.coef_ == 0))
                row['intercept_bps'] = estimator.intercept_ * scale * 10000
                row.update({f: c*scale*10000 for f,c in zip(module.FEATURES, estimator.coef_)})
            else:
                row.update(dict(zip(module.FEATURES, estimator.feature_importances_)))
            fitted_rows.append(row)
        rows = module.decision_rows(market.prices.index)
        next_rows = dict(zip(rows[:-1], rows[1:]))
        for date, values in forecasts.iterrows():
            p = market.prices.index.get_loc(date)
            # Only exact original labels with their next decision inside the cutoff.
            if p not in next_rows: continue
            q = next_rows[p]
            assert market.prices.index[q] <= END
            target = module.outcome(market.signal_prices.to_numpy(), market.rf.to_numpy(), p, q)
            for fund, forecast, actual in zip(FUNDS, values, target):
                if np.isfinite(forecast) and np.isfinite(actual):
                    observations.append(dict(model=name, date=date, fund=fund, forecast=forecast, actual=actual))
        positive = forecasts.gt(0)
        changes = positive.ne(positive.shift()).iloc[1:]
        targets = pd.DataFrame(np.nan, index=market.prices.index, columns=FUNDS)
        targets.loc[forecasts.index] = positive.astype(float)/len(FUNDS)
        start = targets.fillna(0).sum(axis=1).gt(0).idxmax()
        clusters = stats.decision_clusters(targets.loc[start:])
        decisions.append(dict(model=name, refits=len(forecasts), positive_pct=positive.to_numpy().mean()*100,
                              changed_sign_pct=changes.to_numpy().mean()*100,
                              average_funds_held=positive.sum(axis=1).mean(), clustered_decisions=clusters,
                              convergence_warnings=sum(isinstance(w.message, ConvergenceWarning) for w in caught)))
        print('DONE',name,'refits',len(forecasts),'clustered decisions',clusters, flush=True)
    obs = pd.DataFrame(observations)
    # Contextual rule: sign is exactly trailing 252-session return over bill.
    # R² needs return units, so use excess/12 as a declared mechanical monthly proxy.
    # It is not a fitted forecast and not the rule's portfolio return.
    template = obs[obs.model == 'Elastic Net']
    prices, bill = market.signal_prices, market.rf
    for date, g in template.groupby('date'):
        p = prices.index.get_loc(date)
        excess = prices.iloc[p-1]/prices.iloc[p-1-252]-1 - (np.prod(1+bill.iloc[p-252:p])-1)
        for row in g.itertuples():
            observations.append(dict(model='Plain rule proxy', date=date, fund=row.fund, forecast=excess[row.fund]/12, actual=row.actual))
    obs = pd.DataFrame(observations)
    assert obs.date.max() <= END
    common = set.intersection(*(set(g.set_index(['date','fund']).index) for _,g in obs.groupby('model')))
    obs = obs[obs.set_index(['date','fund']).index.isin(common)].copy()
    metric_rows = []
    for name,g in obs.groupby('model',sort=False):
        metric_rows.append(metrics(g,'overall','all'))
        for year,h in g.groupby(g.date.dt.year): metric_rows.append(metrics(h,'year',year))
        for fund,h in g.groupby('fund'): metric_rows.append(metrics(h,'fund',fund))
    met = pd.DataFrame(metric_rows)
    fitdf = pd.DataFrame(fitted_rows)
    features = list(module.FEATURES)
    stability = []
    for name,g in fitdf.groupby('model',sort=False):
        a = g[features].to_numpy()
        corr = [rankcorr(a[i-1],a[i]) for i in range(1,len(a))]
        stability.append(dict(model=name, adjacent_rank_correlation=float(np.nanmean(corr)) if np.isfinite(corr).any() else np.nan,
                              top_feature_unchanged_pct=100*np.mean(np.argmax(a[1:],axis=1)==np.argmax(a[:-1],axis=1)),
                              zero_coefficient_refits_pct=100*g.all_coefficients_zero.mean() if name=='Elastic Net' else np.nan))
    decisiondf = pd.DataFrame(decisions)
    assert decisiondf.clustered_decisions.tolist() == [17,102,122]
    met.to_csv(OUT/'forecast-metrics.csv',index=False,float_format='%.2f')
    exported = obs.copy()
    exported['forecast_bps'] = exported.pop('forecast')*10000
    exported['actual_bps'] = exported.pop('actual')*10000
    exported.to_csv(OUT/'forecast-observations.csv',index=False,float_format='%.2f')
    fitdf.rename(columns={'n_train':'feature_count'}).to_csv(OUT/'fit-history.csv',index=False,float_format='%.2f')
    decisiondf.to_csv(OUT/'decision-behaviour.csv',index=False,float_format='%.2f')
    pd.DataFrame(stability).to_csv(OUT/'importance-stability.csv',index=False,float_format='%.2f')
    overall = met[met.scope=='overall'].to_dict('records')
    summary = dict(cutoff=str(END.date()),scored_first=str(obs.date.min().date()),scored_last=str(obs.date.max().date()),
                   overall=overall, decisions=decisions, stability=stability,
                   source_hashes=hashes, monthly_ic_t='Newey-West, fixed lag 3; descriptive post-run diagnostic',
                   plain_rule_proxy='252-session excess return / 12; sign exact, R2 scale is a mechanical convention')
    (OUT/'summary.json').write_text(json.dumps(clean(summary),indent=2,allow_nan=False)+'\n')
    charts(met,fitdf,all_forecasts,features)
    report(met,decisiondf,pd.DataFrame(stability),summary)
    print(met[met.scope=='overall'].to_string(index=False),flush=True)
    print('IN-SAMPLE DIAGNOSTIC COMPLETE; no portfolio returns computed.',flush=True)


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


def charts(met,fits,forecasts,features):
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):
        fig.tight_layout(rect=(0,0.06,1,1))
        fig.text(0.02,0.01,'Source: diagnostics.py; frozen data truncated before assembly; no portfolio returns.',fontsize=8)
        fig.savefig(OUT/(name+'.png'),dpi=180,bbox_inches='tight',metadata={'Description':'Source: capstone/diagnostics/diagnostics.py; in-sample only, cutoff 2022-12-31.'})
        plt.close(fig)
    quality_chart(met)
    fig,ax=plt.subplots(figsize=(9,3.6))
    for name,g in met[met.scope=='year'].groupby('model',sort=False):ax.plot(g.group.astype(int),g.r2_zero_pct,label=name,marker='.',lw=1)
    ax.axhline(0,color='gray',lw=0.7);ax.set_ylabel('R² vs zero (%)');ax.set_title('Forecast accuracy by year; rule uses a mechanical monthly proxy');ax.legend(fontsize=8,ncol=2)
    save(fig,'02-yearly-accuracy')
    en=fits[fits.model=='Elastic Net']
    fig,ax=plt.subplots(figsize=(10,3.8));a=en[features].to_numpy().T
    image=ax.imshow(a,aspect='auto',cmap='RdBu_r',vmin=-max(1,np.abs(a).max()),vmax=max(1,np.abs(a).max()))
    ax.set_yticks(range(len(features)),features);ticks=np.linspace(0,len(en)-1,6,dtype=int);ax.set_xticks(ticks,en.date.iloc[ticks].str[:7],rotation=20)
    ax.set_title('Elastic Net coefficients: return basis points per feature standard deviation');fig.colorbar(image,ax=ax,label='Basis points')
    save(fig,'03-elastic-net-coefficients')
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,name in zip(axes,['Random Forest','Gradient Boosting']):
        g=fits[fits.model==name][features]
        ax.barh(features[::-1],g.mean()[::-1],xerr=g.std()[::-1],color='#647c8c',ecolor='#888888',capsize=2)
        ax.set_title(name);ax.set_xlabel('Mean impurity importance ± refit SD')
    save(fig,'04-feature-importances')
    fig,ax=plt.subplots(figsize=(10,3.8))
    for name,frame in forecasts.items():ax.plot(frame.index,frame.gt(0).sum(axis=1),label=name,lw=1)
    ax.set_ylim(-0.2,7.8);ax.set_ylabel('Funds with positive forecast');ax.set_title('Monthly target decisions — no portfolio-return calculation');ax.legend(fontsize=8,ncol=3)
    save(fig,'05-decision-behaviour')


def report(met,decisions,stability,summary):
    lines=['# Forecast diagnostic — in-sample only','',
           'I execute each unchanged ML strategy source and call its original forecasts() with the original settings. A passive observer records the fitted estimators. I use the lab market loader with a process-local raw-reader adapter that truncates every input frame before market assembly. No holdout observation enters features, fitting, labels or plots; no strategy return is computed.',
           '',f"Scored monthly decisions run from {summary['scored_first']} through {summary['scored_last']}. December 2022 forecasts are included in fit and behaviour histories but not scored: their next decision is outside the truncated market. All models and the rule proxy use identical scored fund-months.",
           '', '## Definitions and limits','',
           'For regression forecasts, R² vs zero = 1 − sum((actual − forecast)²) / sum(actual²), reported as a percentage. Sign hit rate compares positive forecasts with positive next-month excess returns. Monthly IC is Spearman rank correlation across the funds; constant forecasts have undefined IC and are excluded, not assigned zero. The IC t statistic uses Newey–West variance with a fixed lag of three valid IC observations after undefined months are omitted; for Elastic Net these need not be adjacent calendar months. These are post-run exploratory diagnostics, not a new gate or an independent confirmation.',
           '', 'The plain rule supplies a sign, not a calibrated monthly forecast. For the requested R² context I report a transparent mechanical proxy: trailing 252-session return over the bill divided by twelve. Its sign matches the rule exactly; its R² depends on that fixed scale and must not be interpreted as the rule’s forecast accuracy under an estimated model. Its rank IC uses the continuous signal, not tied binary holdings.',
           '', 'Per-fund rank correlation is a time-series Spearman correlation across that fund’s months; monthly cross-sectional IC and its t statistic are not defined for a single fund. Per-year IC averages the monthly cross-sectional correlations inside that year. Small yearly samples and serial dependence limit inference. I do not select models, years or funds using these diagnostics.',
           '', '## Overall forecast quality','',
           '| Model | R² vs zero (%) | Monthly rank IC | IC t (HAC) | Valid IC months | Sign hit (%) | AUC | Log-loss | Observations |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    order=['OLS','Elastic Net','Random Forest','Gradient Boosting','Logistic Regression','MLP','Plain rule proxy']
    overall=met[met.scope=='overall'].set_index('model')
    for name in order:
        if name not in overall.index: continue
        r=overall.loc[name]
        label=name+'*' if name=='Logistic Regression' else name
        lines.append(f'| {label} | {"n/a" if name=="Logistic Regression" else fmt(r.r2_zero_pct)} | {fmt(r.rank_ic)} | {fmt(r.rank_ic_t_hac3)} | {int(r.valid_ic_months)} | {fmt(r.sign_hit_pct)} | {fmt(r.get("auc",np.nan))} | {fmt(r.get("log_loss",np.nan))} | {int(r.observations)} |')
    if 'Logistic Regression' in overall.index:
        lines+=['','*'+LOGISTIC_R2_NOTE+' IC uses probabilities against subsequent return ranks.']
    lines+=['','## Decision behaviour','','| Model | Refits | Positive forecasts (%) | Adjacent sign changes (%) | Average funds held | Clustered decisions |','|---|---:|---:|---:|---:|---:|']
    for r in decisions.itertuples():lines.append(f'| {r.model} | {r.refits} | {fmt(r.positive_pct)} | {fmt(r.changed_sign_pct)} | {fmt(r.average_funds_held)} | {r.clustered_decisions} |')
    lines+=['','## What the models learned','','| Model | All-zero coefficient refits (%) | Adjacent importance-rank correlation | Same top feature (%) |','|---|---:|---:|---:|']
    for r in stability.itertuples():lines.append(f'| {r.model} | {fmt(r.zero_coefficient_refits_pct)} | {fmt(r.adjacent_rank_correlation)} | {fmt(r.top_feature_unchanged_pct) if r.model!="Elastic Net" else "N/A"} |')
    lines+=['', 'Elastic Net coefficients are reported in basis points of forecast return per one training-window standard deviation of the feature. When every slope is zero, the forecast is only the fitted intercept: every fund then receives the same prediction. Changes in that pooled intercept’s sign can change the whole allocation together. The recomputed target histories reproduce the report’s clustered decision counts exactly. The diagnostic separates the number of refits from actual changes in target holdings.',
            '', 'Tree importances are impurity-based training diagnostics, not causal effects or out-of-sample predictive contributions. Means and standard deviations across refits and adjacent rank correlations describe their stability; correlated features can share or exchange importance.',
            '', '## By year and by fund','', 'The complete overall/year/fund table is forecast-metrics.csv. The fit-level records are fit-history.csv; decision-behaviour.csv and importance-stability.csv record the summaries. forecast-observations.csv stores individual forecasts and targets in basis points rounded to two decimals; metrics are computed before this display rounding.', '']
    for scope in ['year','fund']:
        lines += [f'### {scope.title()} breakdown','', '| Model | Group | R² vs zero (%) | Rank IC | IC t | Sign hit (%) |','|---|---|---:|---:|---:|---:|']
        for r in met[met.scope==scope].itertuples():lines.append(f'| {r.model+"*" if r.model=="Logistic Regression" else r.model} | {r.group} | {"n/a" if r.model=="Logistic Regression" else fmt(r.r2_zero_pct)} | {fmt(r.rank_ic)} | {fmt(r.rank_ic_t_hac3)} | {fmt(r.sign_hit_pct)} |')
        if 'Logistic Regression' in set(met.loc[met.scope==scope,'model']):lines+=['','*'+LOGISTIC_R2_NOTE]
        lines.append('')
    for name,caption in [('01-forecast-quality','Overall forecast quality'),('02-yearly-accuracy','Yearly forecast accuracy'),('03-elastic-net-coefficients','Elastic Net coefficient histories'),('04-feature-importances','Impurity importances and their refit dispersion'),('05-decision-behaviour','Decision behaviour')]:lines+= [f'![{caption}]({name}.png)','']
    lines+= ['## Provenance','', 'Source: diagnostics.py; the frozen data/manifest.json and its hash-verified snapshots; unchanged strategy.py in TM-017-06, TM-017-07 and TM-017-08. Source hashes, dates and scoring definitions are recorded in summary.json. No portfolio engine or lab.report run is invoked. The published holdout results of these completed cards were already seen before this diagnostic; no new holdout calculation is made.']
    (OUT/'diagnostics.md').write_text('\n'.join(lines)+'\n')


class BasisPointForecast(RegressorMixin, BaseEstimator):
    """Read-only adapter: score the fitted regressor in return basis points."""
    def __init__(self, fitted, predictor):
        self.fitted=fitted
        self.predictor=predictor
        self.n_features_in_=len(fitted[1])

    def fit(self, X, y=None):
        raise RuntimeError('Permutation evaluation must never refit the model')

    def predict(self, X):
        return self.predictor(self.fitted, np.asarray(X))*10000


def extended_metrics(frame, scope, group):
    if frame.model.iloc[0]!='Logistic Regression':
        row=metrics(frame,scope,group)
        row.update(r2_target='excess_return',auc=np.nan,log_loss=np.nan)
        return row
    actual=frame.actual.to_numpy();p=frame.forecast.to_numpy();sign=(actual>0).astype(int)
    # The classifier has no return forecast: its R² is a Brier/zero SIGN target score.
    r2=1-np.sum((sign-p)**2)/np.sum(sign**2) if np.sum(sign**2)>0 else np.nan
    ic,t,n=mean_t([rankcorr(g.forecast,g.actual) for _,g in frame.groupby('date')])
    if scope=='fund':ic,t,n=rankcorr(p,actual),np.nan,0
    return dict(model='Logistic Regression',scope=scope,group=str(group),observations=len(frame),months=frame.date.nunique(),
                r2_zero_pct=100*r2,rank_ic=ic,rank_ic_t_hac3=t,valid_ic_months=n,
                sign_hit_pct=100*np.mean((p>0.5)==(sign>0)),positive_forecasts_pct=100*np.mean(p>0.5),
                r2_target='binary_sign',auc=roc_auc_score(sign,p) if len(np.unique(sign))==2 else np.nan,
                log_loss=log_loss(sign,p,labels=[0,1]))


def extend_diagnostic():
    """Fixed forecast extension; preserve all published legacy numerical rows."""
    if not (OUT/'forecast-metrics.csv').exists():run()
    legacy_names=['Elastic Net','Random Forest','Gradient Boosting','Plain rule proxy']
    old_metrics=pd.read_csv(OUT/'forecast-metrics.csv',dtype={'group':str})
    old_metrics=old_metrics[old_metrics.model.isin(legacy_names)].copy()
    old_metrics['r2_target']=np.where(old_metrics.model.eq('Plain rule proxy'),'mechanical_return_proxy','excess_return')
    old_metrics['auc']=np.nan;old_metrics['log_loss']=np.nan
    old_summary=json.loads((OUT/'summary.json').read_text())
    legacy_overall=[r for r in old_summary['overall'] if r['model'] in legacy_names]
    legacy_obs=pd.read_csv(OUT/'forecast-observations.csv',parse_dates=['date'])
    common=set(legacy_obs[legacy_obs.model=='Elastic Net'].set_index(['date','fund']).index)
    market=load_inside();closes=market.signal_prices.to_numpy();bill=market.rf.to_numpy()
    assert market.prices.index.max()<=END
    observations=[];perm_rows=[];impurity_rows=[];fit_info=[]
    jobs=[('OLS','ols'),('Logistic Regression','logistic'),('MLP','mlp'),('Random Forest','random-forest'),('Gradient Boosting','gradient-boosting')]
    source=ROOT/'alpha-lab/strategies/TM-017-06-elastic-net-trend/strategy.py'
    for name,model in jobs:
        path=source
        if model=='random-forest':path=ROOT/'alpha-lab/strategies/TM-017-07-random-forest-trend/strategy.py'
        if model=='gradient-boosting':path=ROOT/'alpha-lab/strategies/TM-017-08-boosted-trend/strategy.py'
        module=types.ModuleType('extension_'+model.replace('-','_'));module.__file__=str(path)
        exec(compile(path.read_text(),str(path),'exec'),module.__dict__)
        module.MODELS=(*module.MODELS,'ols','logistic','mlp')
        original_make=module.make
        def make(which,_original=original_make):
            if which=='ols':return LinearRegression()
            if which=='logistic':return LogisticRegression(penalty='l2',C=1.0,max_iter=1000)
            if which=='mlp':return MLPRegressor(hidden_layer_sizes=(16,8),alpha=1e-3,early_stopping=True,max_iter=500,random_state=0)
            return _original(which)
        module.make=make
        if model=='logistic':
            def fit_log(which,X,y,_make=make):
                mean,std=X.mean(axis=0),X.std(axis=0);std[std==0]=1.0
                estimator=_make(which).fit((X-mean)/std,(y>0).astype(int))
                return estimator,mean,std,1.0
            module.fitted=fit_log
            def probability(fit,X):
                estimator,mean,std,_=fit
                return estimator.predict_proba((X-mean)/std)[:,1]
            module.predict=probability
        fits=[];original_fitted=module.fitted
        def observe(*args,_original=original_fitted,**kwargs):
            result=_original(*args,**kwargs);fits.append(result);return result
        module.fitted=observe
        print('EXTENSION',name,'fixed settings; market cutoff',market.prices.index.max(),flush=True)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            forecasts=module.forecasts(market,model=model,window=60,memory=2400).dropna(how='all')
        assert len(fits)==len(forecasts)==143 and forecasts.index.max()<=END
        fit_info.append(dict(model=name,refits=len(fits),convergence_warnings=sum(isinstance(w.message,ConvergenceWarning) for w in caught)))
        positions=module.decision_rows(market.prices.index);next_rows=dict(zip(positions[:-1],positions[1:]))
        for date,fit in zip(forecasts.index,fits):
            estimator=fit[0]
            if model in ('random-forest','gradient-boosting'):
                impurity_rows.extend(dict(model=name,date=str(date.date()),feature=f,importance=v) for f,v in zip(module.FEATURES,estimator.feature_importances_))
            p=market.prices.index.get_loc(date)
            if p not in next_rows:continue
            q=next_rows[p];assert market.prices.index[q]<=END
            X=module.features_at(closes,p);y=module.outcome(closes,bill,p,q)
            keep=np.isfinite(X).all(axis=1)&np.isfinite(y)
            assert all((date,f) in common for f,k in zip(FUNDS,keep) if k)
            if model in ('ols','logistic','mlp'):
                for fund,prediction,actual,k in zip(FUNDS,forecasts.loc[date],y,keep):
                    if k:observations.append(dict(model=name,date=date,fund=fund,forecast=prediction,actual=actual))
            if model in ('random-forest','gradient-boosting','mlp'):
                scored=BasisPointForecast(fit,module.predict)
                importance=permutation_importance(scored,X[keep],y[keep]*10000,scoring='neg_mean_squared_error',n_repeats=10,random_state=0,n_jobs=1)
                perm_rows.extend(dict(model=name,date=str(date.date()),feature=f,importance_bps2=v,repeat_sd_bps2=sd) for f,v,sd in zip(module.FEATURES,importance.importances_mean,importance.importances_std))
        print('DONE',name,'refits',len(fits),'next-month permutation' if model in ('random-forest','gradient-boosting','mlp') else 'forecast evaluation only',flush=True)
    new_obs=pd.DataFrame(observations);new_rows=[]
    assert new_obs.groupby('model').size().eq(994).all() and new_obs.date.max()<=END
    for name,g in new_obs.groupby('model',sort=False):
        assert set(g.set_index(['date','fund']).index)==common
        new_rows.append(extended_metrics(g,'overall','all'))
        for year,h in g.groupby(g.date.dt.year):new_rows.append(extended_metrics(h,'year',year))
        for fund,h in g.groupby('fund'):new_rows.append(extended_metrics(h,'fund',fund))
    combined=pd.concat([old_metrics,pd.DataFrame(new_rows)],ignore_index=True)
    combined.to_csv(OUT/'forecast-metrics.csv',index=False,float_format='%.2f')
    export=new_obs[['model','date','fund']].copy();is_log=new_obs.model.eq('Logistic Regression')
    export['forecast_return_bps']=np.where(is_log,np.nan,new_obs.forecast*10000)
    export['probability_pct']=np.where(is_log,new_obs.forecast*100,np.nan)
    export['actual_return_bps']=new_obs.actual*10000;export['actual_sign']=(new_obs.actual>0).astype(int)
    export.to_csv(OUT/'extended-forecast-observations.csv',index=False,float_format='%.2f')
    perm=pd.DataFrame(perm_rows);perm.to_csv(OUT/'permutation-importances.csv',index=False,float_format='%.2f')
    summary=perm.groupby(['model','feature'],sort=False).agg(mean_bps2=('importance_bps2','mean'),refit_sd_bps2=('importance_bps2','std'),months=('date','count')).reset_index()
    summary.to_csv(OUT/'permutation-summary.csv',index=False,float_format='%.2f')
    impurity=pd.DataFrame(impurity_rows).groupby(['model','feature'],sort=False).importance.agg(['mean','std']).reset_index()
    impurity.to_csv(OUT/'impurity-summary.csv',index=False,float_format='%.2f')
    old_summary['overall']=legacy_overall+[clean(r) for r in new_rows if r['scope']=='overall']
    old_summary['extension']=dict(forecast_only=True,cutoff=str(END.date()),settings={
        'OLS':'LinearRegression defaults; original rolling standardisation and target scaling',
        'Logistic Regression':'L2, C=1.0, max_iter=1000; sign target; threshold 0.5',
        'MLP':'hidden_layer_sizes=(16,8), alpha=10^-3, early_stopping=True, max_iter=500, random_state=0',
        'permutation':'n_repeats=10, random_state=0; negative next-month MSE in return basis points squared'},
        fit_info=fit_info,logistic_r2='binary-sign R2 versus all-zero sign forecast; not a return R2',
        permutation_summary=clean(summary.to_dict('records')))
    (OUT/'summary.json').write_text(json.dumps(old_summary,indent=2,allow_nan=False)+'\n')
    report(combined,pd.read_csv(OUT/'decision-behaviour.csv'),pd.read_csv(OUT/'importance-stability.csv'),old_summary)
    extra='''
## Fixed forecast extension and classification scale

OLS uses LinearRegression. Logistic regression uses L2, C=1.00 and max_iter=1000,
predicting the sign with a fixed probability boundary of 0.50. The MLP uses hidden
layers (16, 8), alpha=10^-3, early stopping, max_iter=500 and random_state=0.
All reuse the original eight features, completed labels, pooled 60-month window,
monthly dates, training-only scaling and bounded history. No setting is selected
from these results. The additional estimators produce forecasts only: no positions,
portfolio return, strategy card, gate verdict or registry entry is created.

The classifier's R² is displayed as n/a. Its rank IC uses probabilities
against subsequent excess-return ranks; accuracy, AUC and log-loss evaluate signs.
No probability-to-return calibration is invented. Regression and rule-proxy R²
definitions, all original metric rows and original decision histories are retained.

Permutation importance is the increase in following-month MSE when a feature is
permuted, in return basis points squared, with ten repeats and random_state=0.
The estimator and training scaler are frozen before that month's seven outcomes
are scored. Each date uses only the next completed month inside the cutoff; there
are 142 scored refits. The mean is across monthly importance estimates, with
refit dispersion shown separately. Negative importance means shuffling improved
that month's error. These small, correlated cross-sections do not identify causes.
Training impurity importances use the original 143 refits, including unscored
December 2022. The MLP has no tree impurity importance.

The MLP's early-stopping validation is internal to historical training data, not
the next evaluation month, but it is not a separate chronological inner split.
Convergence warnings are recorded in summary.json without changing settings.

![Impurity next to next-month permutation importance](06-permutation-importances.png)

Provenance: diagnostics.py, forecast-metrics.csv, extended-forecast-observations.csv,
permutation-importances.csv, permutation-summary.csv and impurity-summary.csv.
Original forecast-observations.csv, fit-history.csv, decision-behaviour.csv and
importance-stability.csv remain unchanged. New metrics are computed before
two-decimal display rounding. No holdout or portfolio return is evaluated.
'''
    with (OUT/'diagnostics.md').open('a') as f:f.write(extra)
    append_permutation_table(summary)
    extended_charts(combined,summary,impurity)
    print(combined[combined.scope=='overall'].to_string(index=False,float_format=lambda x:f'{x:.2f}'),flush=True)
    print('EXTENSION COMPLETE: six models plus rule proxy; no portfolio trial.',flush=True)


def append_permutation_table(summary):
    lines=['','## Following-month permutation summary','',
           '| Model | Feature | Mean MSE increase (bp²) | Refit SD (bp²) | Months |',
           '|---|---|---:|---:|---:|']
    for row in summary.itertuples():lines.append(f'| {row.model} | {row.feature} | {fmt(row.mean_bps2)} | {fmt(row.refit_sd_bps2)} | {int(row.months)} |')
    lines+=['','For both tree ensembles, vol63 is the only feature with positive mean permutation importance; most training-important features have negative following-month importance. The MLP has mixed signs and its largest positive mean is ma200. Refit dispersion is large relative to these means. Positive importance for one input does not validate the complete model, whose return R² remains negative. Source: permutation-summary.csv; every feature and month is retained.','']
    with (OUT/'diagnostics.md').open('a') as f:f.write('\n'.join(lines))


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


if __name__=='__main__':
    if sys.argv[1:]==['--refresh-quality']:
        # Redraw committed metrics only: no market load, forecasts or refitting.
        quality_chart(pd.read_csv(OUT/'forecast-metrics.csv'))
    else:
        extend_diagnostic()
