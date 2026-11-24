# TM-017-10 — Repair of the unrun volatility-weighted specification

## Fixed rule and prior history

TM-017-09 was skipped at preflight before any real run: its all-tradable denominator required a full 63-session volatility for DBC on 2006-03-01, which did not exist. No return result of that card exists, no registry trial was recorded, and its holdout was not opened. This card repairs only that undefined case. Its parent field is null, as explicitly fixed by Anas. TM-017-09 and every existing card remain unchanged.

Anas fixed this complete repair before any run of TM-017-10: a tradable fund without defined 63-session volatility is neither held nor included in the denominator. Everything else is unchanged: the same seven funds, monthly decisions, lagged closes, entry over the bill, base 252-session lookback, prescribed neighbours, fixed 63-session volatility window and 400-session memory. No numerical performance size, extra filter, fitted coefficient, new start date, floor or tuning is introduced.

Earlier holdouts were already seen, including TM-017-06/07/08 and MR-001-01/02. The repair was specified after those publications, but not selected using a financial result from TM-017-09 because that result does not exist. This is a further exploratory follow-up, not a globally untouched calendar holdout. No raw 2023–2025 data is examined outside the lab's official run, and no strategy return is computed outside it.

## Mechanism and existing evidence

The theory is TM-017. Moskowitz, Ooi and Pedersen (2012), Time Series Momentum, Journal of Financial Economics, 104(2), 228–250, motivates trend following with volatility-scaled positions. TM-047's related bank discussion distinguishes sizing from the economic trend signal. The published plain rule has Sharpe 0.50, annual alpha 1.55%, beats 81.70% of shifted placebos and first fails gate 3. It also fails concentration at gate 6 (its report.ipynb, cells 12, 14, 20 and 24). Inverse-volatility capital slots can reduce allocation to volatile instruments, but do not guarantee equal risk or dispersed realised profit.

## Exact construction

On the first session of each month, all signal closes end on the preceding session. Compute each fund's trailing lookback return and the compounded bill over that same interval. A fund must beat the bill, be tradable and have a defined full 63-session daily-log-return volatility to be held. Volatility uses the lab's annualised sample-standard-deviation convention.

The denominator sums inverse volatilities over ALL tradable funds with defined volatility, including those that do not pass the trend condition. Each held fund gets its own inverse volatility divided by that sum. Slots of unheld funds remain cash. Missing volatility is excluded exactly as prescribed; it is not imputed. A mathematically undefined reciprocal or denominator is an error rather than permission for a new fallback or floor.

Lookback is the only parameter: base 252, neighbours 189/315 and 126/378. The volatility window 63 is fixed code, and memory is 400. These choices come from Anas's instruction, not return calculations. One base variant runs once. Before it, the official --check and --try validate the specification and targets without displaying portfolio returns. The card is committed alone before build-plan.md and strategy.py are written; the registry is committed alone immediately after the one run, followed by report outputs.

## Interpretation and stopping rule

The qualitative hypothesis is positive benchmark-relative value with volatility-aware sizing. No quantitative magnitude is invented. A failed gate is a result and cannot justify changing this card, code or rule afterwards. No further card is authorised. The paired comparison with TM-017-01 remains unavailable because its historical run commit is absent; no homemade paired return test replaces it. The separate expansion of forecast diagnostics is not a trading strategy or a registered portfolio trial.
