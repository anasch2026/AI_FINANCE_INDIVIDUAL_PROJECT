# MR-001-01 — A constrained liquidity-reversal hypothesis

## Why this card exists

The completed in-sample forecast diagnostic shows R² against zero of -2.36%, -6.23% and -13.08% for Elastic Net, Random Forest and Gradient Boosting. Elastic Net has all-zero slopes in 76.92% of 143 refits, positive forecasts in 96.90% of its decisions and only 17 clustered changes. The nonlinear fits do not restore positive aggregate forecast R². These findings motivate reducing estimation freedom and testing a distinct mechanism. They do not demonstrate that reversal works, and I have computed no return of the proposed strategy, no parameter search and no power estimate on its in-sample returns.

Sources: capstone/diagnostics/summary.json, forecast-metrics.csv, fit-history.csv and decision-behaviour.csv. The diagnostic uses only raw market inputs truncated before assembly at 2022-12-31. Its scored decisions end in November 2022; December forecasts enter behaviour only.

## Economic mechanism and sources

MR-001 describes short-term reversals as compensation for providing liquidity after selling pressure, rather than intermediate-horizon trend continuation. Grossman and Miller (1988), Liquidity and Market Structure, Journal of Finance, motivate costly immediacy; Nagel (2012), Evaporating Liquidity, Review of Financial Studies, connects reversal returns with liquidity provision. These are documented in bank/MR-001-short-term-reversal-liquidity-provision.md. I read its related MR-002 (behavioural overreaction), MR-007 (microstructure versus information), MR-010 (temporary price pressure), MR-011 (volume-conditioned reversal) and FP-002 (dealer inventory pressure). This card does not identify order flow or dealer inventory. It tests a coarse long-only implication: buying after a recent fall over the bill may capture a rebound that rewards absorbing selling pressure.

The seven liquid broad funds are an extrapolation from much of the stock-level literature. Their liquidity may eliminate the effect; persistent fundamental declines may overwhelm it. Failure is therefore a useful outcome, and passing would not identify liquidity provision causally. I do not claim a published expected Sharpe for this exact implementation.

## Fixed design and rejected alternatives

- Same seven funds as the completed ML study: SPY, EFA, EEM, IEF, TLT, GLD, DBC. No new data or universe selection from performance.
- Decision on the first session of each month; a fund whose trailing 21-session return is below the compounded bill return over the same trailing interval receives one seventh of the portfolio. Missing history leaves its share in cash. No shorting, leverage, ranking, fitted intercept or estimated coefficients.
- Twenty-one sessions is the conventional approximate monthly horizon already used in the ML feature set, not a horizon selected by a new return test. The zero threshold is the economic dividing line between underperforming and outperforming cash.
- One numeric parameter, lookback, with base 21 and prescribed neighbours 16/26 and 10/32. Memory is 32 sessions, covering the longest lag measured back from the session before a target and monthly holding intervals. These are robustness probes, not selectable variants.
- One base variant only. I deliberately draw one new card, not a sequence of attempts after each result. This is a rule-based mechanism test, not a repaired Elastic Net or a claim that ML now works.
- I reject extra volatility filters, nonlinear fits, a fitted holding threshold, shorter rebalance intervals and selection of the best diagnostic year/fund. Each would add another degree of freedom or change the claim without prior evidence of its incremental value.

The Sharpe prediction at or above 0.40 is a judgment tied to the lab's minimum economic requirement, not an empirical estimate or a literature figure. Positive alpha against passive holding is the economic claim. The published evidence does not justify a statistical power calculation for this strategy, so none is supplied.

## Prior information and holdout disclosure

I have seen TM-017-01's published results and the completed 06–08 reports, including their 2023–2025 holdout diagnostics. In particular, their holdout gate outcomes and metrics were already in the manuscript before this hypothesis. I do not use those holdout outcomes to choose the reversal direction, horizon, allocation, universe, thresholds or any other setting. This new design responds only to the diagnostic of pre-2023 forecasts and to the independent liquidity-reversal literature. No new holdout feature, forecast, return or statistic is computed outside the lab's own run. This disclosure does not make the calendar holdout globally unseen again: the test is an exploratory follow-up with prior partial knowledge, not a pristine independent confirmation.

The in-sample diagnostic exposed fund-month outcomes as well as the old forecasts. It did not compute this strategy's returns or a contrast approximating its graded alpha. The strategy is therefore not selected by its in-sample backtest, but its follow-up nature must remain explicit in the final analysis. All known original cards, failures and retired identifiers remain reported.

## Comparison and refutation

The benchmark is always holding the same seven funds in equal parts, not TM-017-01. The official paired comparison with TM-017-01 is unavailable because its historical run commit is absent; no substitute test will be written. Side-by-side published figures remain descriptive and may cover different effective windows.

The card fails validation at its first failed gate, irrespective of later diagnostics. Nonpositive alpha, insufficient placebo evidence, unstable episode results or concentrated contributions would count against this implementation. A negative result will be recorded without adjusting the card or rerunning it. No conclusion about a general absence of liquidity-related reversals follows from this restricted ETF test.
