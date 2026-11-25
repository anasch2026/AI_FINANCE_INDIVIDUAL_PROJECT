# Two-minute defence script

Four slides, about thirty seconds each: 240 spoken words, roughly 1.7 minutes at 140 words per minute. Backup slides for questions: presentation-backup.pptx.

## Slide 1 — Do ML trend signals survive strict validation?

A trend rule on seven ETFs beats equal-weight holding, Sharpe 0.50 against 0.41, but it beats only 81.70 percent of shifted-timing placebos, so its edge may be luck. I asked whether machine learning can make that monthly entry decision reliably better after costs. The short answer is no.

(48 words)

## Slide 2 — ML replaces only the entry decision

I kept the funds, the monthly schedule and the one-seventh allocation, and replaced only the decision to hold. Elastic Net, Random Forest and Gradient Boosting forecast next-month excess returns from eight lagged price features on a rolling sixty-month window. Every strategy then faces seven gates: hygiene, economic edge, significance, multiple testing, stability, robustness and a sealed 2023 to 2025 holdout.

(60 words)

## Slide 3 — No ML strategy survives; costs are not the reason

All three ML strategies fail. Their Sharpe ratios are 0.30, 0.08 and 0.09, with negative alphas, on their reported windows. Costs are not the reason: the gross Sharpe ratios are already too low. These cross-window comparisons are descriptive. Forecasts are worse than predicting zero for every return model. Elastic Net mostly collapses to a single average forecast, so it produces few distinct target changes.

(64 words)

## Slide 4 — Best follow-up still fails: do not deploy

My best economic follow-up weights trend positions by inverse volatility. Its Sharpe is 0.61 and its alpha 2.16 percent, but it beats only 89.80 percent of placebos and its deflated Sharpe is 0.27, far below 0.90, so it is not a near-pass. This follow-up is exploratory: earlier holdouts were already seen. The lesson: a good backtest is not a validated strategy. I would not deploy any of them.

(68 words)
