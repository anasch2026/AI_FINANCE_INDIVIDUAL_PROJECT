# TM-017-09 — Volatility-weighted trend, capstone follow-up 3

## User-fixed design and integrity disclosure

Anas Chantah fixed this complete rule before any run of this card, in the same instruction that fixed MR-001-02. This is capstone follow-up number 3, after MR-001-01 and MR-001-02. The holdout results of TM-017-06/07/08 and MR-001-01 had already been seen when the instruction was given; MR-001-02 subsequently ran first, as required, without changing this specification. This prior exposure is disclosed rather than called an unseen independent holdout. No raw 2023–2025 data is inspected outside the lab's own run, and no return is computed outside its official commands. No tuning, additional feature or substitute rule is allowed.

## Mechanism and prior published evidence

The selected theory is TM-017. Moskowitz, Ooi and Pedersen (2012), Time Series Momentum, motivates both trend following and volatility-scaled positions. The related TM-047 bank file distinguishes volatility-based sizing from the forecast mechanism. The user's hypothesis retains TM-017-01's entry rule and changes only sizing: inverse-volatility slots should reduce the capital assigned to more volatile funds. It does not guarantee equal portfolio risk or smaller realised profit concentration, since correlations and returns also matter.

TM-017-01's published Sharpe is 0.50, annual alpha 1.55%, placebo-beaten fraction 81.70%, and its first failure is gate 3; it also fails gate 6 because SPY contributes more than the allowed share of profit (report.ipynb cells 12, 14, 20 and 24). This published evidence motivates the requested sizing hypothesis. I do not compute a common-window performance contrast or a power estimate before locking the card. The official comparison with TM-017-01 remains unavailable because its historical run commit is missing.

## Exact allocation and sole parameter

On the first session of each month, a tradable fund is held if its trailing 252-session return, ending at the preceding session, exceeds the bill compounded over the same interval. Compute annualised sample volatility of daily log returns over the last 63 sessions, also ending at the preceding session. The slot for a held fund is its inverse volatility divided by the sum of inverse volatilities of ALL tradable funds, including those not held. Unheld slots remain cash. The sum must not be restricted to positive-trend funds or to funds selected by some new condition.

Lookback=252 is the sole parameter, with neighbours 189/315 and 126/378. Volatility window 63 is fixed in code. Memory is the user-fixed 400 sessions. There is one base variant, no volatility floor, imputation, new starting date, stress filter, leverage or optimisation.

## Exactness issue to check before a run

The frozen manifest and lab universe identify DBC's first price/tradable session as 2006-02-06. Thus at early subsequent monthly decisions a tradable denominator member can lack the required full 63 daily log returns, even though other funds have enough history for the trend signal. The user's formula then has an undefined term. Omitting that term from a pandas sum, defining it as zero, shortening its volatility window, assigning an imputed volatility, delaying all other holdings or imposing a new universe start would change the rule.

The implementation will evaluate the specified formula where it is defined and raise a clear feasibility error if a held-target decision requires an undefined denominator. This is an error check, not an alternative trading condition or fallback allocation. The official --try must establish whether the issue occurs. If it does, Anas's explicit instruction is to record the reason and skip the card, not invent a substitute. No real run or trial is authorised for an unimplementable specification, and the locked card must not be edited to repair it.

## Prediction and reporting

The qualitative prediction is positive benchmark-relative alpha with better control of volatile capital weights. No numerical size was fixed by the user and none is invented. The existing lab gates judge any admissible run. If the preflight cannot define the exact rule, the result is unrun/skipped rather than a financial failure, no holdout is opened, no registry line is fabricated and no metric is reported as zero. Every earlier trial and retired card remains visible.
