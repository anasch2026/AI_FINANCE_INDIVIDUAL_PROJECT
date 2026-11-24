# Individual defence — slide outline and speaker notes

Fifteen slides for an approximately ten-minute individual defence. The PowerPoint contains the same speaker notes.

## Slide 1 — Do ML trend signals survive strict validation?

Speaker notes:

The original ML cards do not survive validation. The diagnostic now compares six fixed learners, including OLS, logistic regression and a small network, without adding a strategy or portfolio trial. Both reversal follow-ups fail economics. TM-017-09 remains skipped, while its separately fixed repair, TM-017-10, passes economics and robustness but first fails significance. I preserve that qualified progress, the original failures, the unrun specification and prior holdout exposure. Forecast evaluation and investment validation are distinct conclusions.

Sources: Saved reports: TM-017-01/06/07/08/10; MR-001-01/02. TM-017-09 unrun. results-notes.md.

## Slide 2 — My contribution is the ML application and the research

Speaker notes:

Alpha Factory is prior work I co-founded with Sami Andaloussi. My course contribution is the ML layer, diagnostic, follow-ups, experiments and analysis under my name. Claude and OpenAI Codex assisted with coding and drafting. Four follow-up cards are specified overall, three with financial runs and one skipped. The repair was fixed before its run and changes only undefined-volatility membership; 09 had no result to tune against. The additional forecast estimators create no portfolio trial. Completed cards and earlier numbers remain unchanged.

Sources: Prior work attribution: github.com/Sami-Andaloussi/alpha-factory. Disclosure: manuscript.md.

## Slide 3 — The model changes the entry decision, not the allocation

Speaker notes:

The funds are SPY, EFA, EEM, IEF, TLT, GLD and DBC. Each forecast uses eight lagged price features: several return horizons, skip-month momentum, volatility and moving-average distance. I pool fund-months, refit on sixty completed months, and hold a seventh per fund if its forecast exceeds zero. Elastic Net regularises a linear relationship; the forest and boosting models allow nonlinear relationships. Their settings were fixed before the original runs. The declared in-sample period is 2005 to 2022, but the actual ML performance window begins in February 2011. I preserve that distinction.

Sources: ML card.yaml and strategy.py files; report.ipynb cell 4; diagnostics/summary.json.

## Slide 4 — The first failed gate defines the verdict

Speaker notes:

The battery tests hygiene, economics, significance, multiple testing, stability, robustness and holdout. The first failure determines rejection. Elastic Net fails evidence sufficiency; the ensembles and reversal cards fail economics. The plain rule and the repaired volatility-weighted rule first fail significance. The repaired rule also passes robustness, which is a favourable recorded result but not full validation. Different historical threshold versions and the missing paired comparison limit interpretation. Forecast-only OLS, logistic and MLP do not receive gate verdicts.

Sources: figures/01-gates.png; all report.ipynb files, cell 24; battery.py.

## Slide 5 — The original ML cards do not establish economic edge

Speaker notes:

These are net excess-return Sharpes and annual regression alphas against passive equal-weight holding, not against the trend rule. Elastic Net has only seventeen clustered decisions, so its first failure is hygiene, although its alpha is also negative. The two ensembles have enough decisions but fail economics immediately. Different effective evaluation windows prevent a clean ranking against the historical rule. In addition, lab.compare cannot authenticate the missing historical reference commit. I therefore present this table descriptively and make no paired estimate or statistical superiority claim.

Sources: TM-017-01/06/07/08 report.ipynb cells 12 and 24; results.csv.

## Slide 6 — Forecast accuracy is weak before portfolio construction

Speaker notes:

The diagnostic cuts raw inputs before market assembly and uses no holdout observation. It computes no portfolio return. The common scored sample contains 994 fund-months. Return R squared is negative for all five return regressors, and the tree ensembles have negative mean monthly rank information coefficients. Logistic R squared is displayed as n/a, as explained on the next slide. Elastic Net has only thirty-two valid IC months because many forecasts are constant across funds. Its IC average therefore needs special care. The rule is a sign signal, so its R squared uses a declared mechanical monthly scaling proxy; that number is contextual rather than a calibrated model comparison.

Sources: diagnostics/01-forecast-quality.png; forecast-metrics.csv; diagnostics.py.

## Slide 7 — Six models, same verdict

Speaker notes:

The shared scored sample and fixed protocol compare six learners and a rule proxy. OLS and MLP have negative return R squared, like the original regressors. Logistic regression predicts a probability of a positive return. R² is not defined for a binary target; the logistic model is judged by accuracy, AUC and log-loss. The classifier has weak accuracy, AUC and log-loss. The same forecast conclusion is weak evidence on this sample, not six failed trading cards. No new portfolio return, holdout evaluation or registry trial is produced by this extension.

Sources: diagnostics/forecast-metrics.csv; diagnostics.py; all figures before 2023.

## Slide 8 — Elastic Net mostly learns a pooled intercept

Speaker notes:

All Elastic Net slopes are zero in 76.92 percent of monthly fits. When this happens, every fund receives the same forecast from the pooled intercept. Positive forecasts account for 96.90 percent of its decision history and it holds an average of 6.78 funds. Refitting is frequent, but target signs rarely change. The reconstructed target history reproduces exactly the seventeen clustered decisions in the official report. This is an explanation grounded in the estimator and targets, rather than an assumption that timing checks failed. I did not lower the penalty or change the old card to obtain more decisions.

Sources: diagnostics/03-elastic-net-coefficients.png; summary.json; decision-behaviour.csv.

## Slide 9 — Only volatility helps out of sample

Speaker notes:

The adjacent training-importance rank correlations remain 0.82 and 0.79, but persistence is not predictive skill. Following-month permutation evaluates a frozen model on only that next month’s seven observations. Most tree features have negative mean permutation importance; vol63 is the only positive mean for each ensemble. The MLP has mixed signs and large refit dispersion. Positive training impurity importance can coexist with worse future prediction. The full comparison is in the manuscript. No feature subset or new model setting is selected from it.
Bars show each model’s mean next-month MSE increase in thousands of basis points squared; teal highlights vol63, the only positive mean for both tree models.

Sources: diagnostics/07-tree-permutation-importance.png; diagnostics/permutation-summary.csv; diagnostics/importance-stability.csv.

## Slide 10 — First follow-up: liquidity reversal after a decline

Speaker notes:

The diagnostic gives no reason to add model complexity. I instead test a distinct mechanism from the literature: providing liquidity after selling pressure may earn a rebound. The rule buys a fund after its trailing twenty-one-session return underperforms the bill. It uses the same monthly schedule and equal allocation slots, with no fitted coefficients. The horizon and zero boundary are economic conventions, not choices selected by a backtest. I locked the card alone, then wrote code and ran it once. Earlier holdout results had already been seen, so this remains an exploratory follow-up with that limitation disclosed.

Sources: MR-001-01 card.yaml and reasoning.md; bank/MR-001; Nagel (2012).

## Slide 11 — The new hypothesis also fails economic edge

Speaker notes:

The official run passes timing, memory and decision-count checks, with 205 clustered decisions. It then fails economics: Sharpe is 0.24 against the benchmark 0.45, and annual alpha is minus 1.07 percent. Its placebo-beaten fraction is 37.10 percent, far below the required ninety percent. Stability and concentration also fail. The holdout cannot cancel the first failure. I committed the registry alone, then the report, and kept the strategy unchanged. Anas later fixed two separate follow-up rules before either newly requested card ran.
Nagel (2012) finds little unconditional reversal profit in diversified industry portfolios and profitability mainly at high VIX; MR-001-01 uses diversified ETFs without volatility conditioning, so its failure is consistent with that evidence.

Sources: MR-001-01 report.ipynb cells 10–24; results.csv.

## Slide 12 — Follow-up 2: stress does not validate reversal

Speaker notes:

Anas fixed this stress condition before the run. SPY realised volatility over sixty-three sessions must exceed the median of its preceding 756 volatility observations. Current volatility is excluded from that reference median. Only then does the rule buy funds below the bill over the fixed base return horizon. It passes hygiene with 92 clustered decisions but fails economic edge and later significance, stability and robustness. GLD accounts for 84.15 percent of profit. The favourable holdout does not rescue it. This proxy is realised volatility, not Nagel’s VIX state. Its shorter effective window also prevents a paired claim against unconditional reversal. The added trial remains in gate four.

Sources: MR-001-02 card.yaml; report.ipynb cells 10–24; results.csv.

## Slide 13 — TM-017-10 repairs 09 but still stops at significance

Speaker notes:

TM-017-09 remains skipped at preflight and has no return result. Anas fixes a separate card, 10, changing only the undefined case: a fund without defined volatility is neither held nor included in the sum. The repaired rule passes hygiene, economics and robustness. SPY’s largest profit share is 28.55 percent. It first fails significance with 89.80 percent of placebos beaten against ninety percent required. DSR is 0.27 and the blend also fails stability. This is qualified economic and robustness progress, not full validation or a paired proof of improvement. No threshold or setting is changed after the result.
The permutation result for 63-session volatility and TM-017-10’s use of volatility for weighting rather than prediction are consistent but not causal: the card was specified before the extended diagnostic.

Sources: TM-017-10 report.ipynb cells 12–24; TM-017-09 remains skipped; STOPPED.md.

## Slide 14 — A positive holdout Sharpe is not value added

Speaker notes:

Elastic Net has holdout Sharpe 0.91 versus the rule’s 0.89, but its alpha rounds to slightly negative zero while the rule’s is 0.61 percent. Sharpe measures excess return relative to volatility. Alpha measures return beyond benchmark exposure. The apparent paradox disappears when I separate these questions. Gate seven is also a lower-tail decay diagnostic, so it does not require positive alpha. The new rule has positive holdout alpha but fails earlier. I report all these outcomes and compute no new holdout return or forecast outside the official runs.

Sources: figures/04-holdout.png; report.ipynb cell 22; battery.py, decide_holdout().

## Slide 15 — The contribution is a transparent negative research cycle

Speaker notes:

The original ML cards fail validation, and the fixed six-model diagnostic provides weak forecast evidence without adding trading trials. Both reversal cards fail economics. The repaired volatility-weighted rule passes economics and robustness but fails significance and multiple testing. Its positive result on individual criteria remains visible alongside rejection. Four follow-up specifications contain three financial trials and one skipped preflight. Earlier holdouts were seen; paired comparison remains unavailable and effective windows differ. I retain every result, display logistic R squared as n/a and do not use importance to tune another model.

Sources: manuscript.md; results-notes.md; STOPPED.md; full local experiment record.
