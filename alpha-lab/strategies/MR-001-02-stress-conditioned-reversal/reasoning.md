# MR-001-02 — Stress-conditioned reversal, capstone follow-up 2

## Pre-specification and research history

Anas Chantah fixed this rule, its universe, sole parameter, neighbours, fixed windows and memory in his instruction before any run of this card. I do not select or optimise them. This is capstone follow-up number 2, after MR-001-01. The original ML cards TM-017-06/07/08 and MR-001-01 have run, and their holdout results were already seen before this design was recorded. They remain disclosed. No new return, volatility diagnostic or performance estimate is computed outside the lab's own run; --try checks targets and timing without showing portfolio returns. No raw 2023–2025 data is examined outside that run.

The shared calendar holdout is not globally unseen again. This is an exploratory, explicitly pre-specified follow-up, not an independent discovery on untouched historical years. Anas also fixed the next requested rule in the same instruction before this card runs; this result cannot alter that rule.

## Mechanism and prior evidence

Nagel, S. (2012). Evaporating Liquidity. The Review of Financial Studies, 25(7), 2005–2039, motivates high returns to liquidity provision mainly in high-volatility periods. The bank's MR-001 describes short-term reversal as compensation for bearing inventory, adverse-selection and funding risk after selling pressure. MR-001-01 applied an unconditional long-only implication and failed gate 2, with published in-sample Sharpe 0.24, annual alpha -1.07% and 37.10% of shifted placebos beaten (its report.ipynb, cells 12, 14 and 24).

This new rule conditions the same reversal direction on stress. It uses realised SPY volatility, not the VIX in the paper; I do not claim that the proxy identifies the paper's exact state or causally isolates liquidity demand. Liquid diversified funds can lack a reversal premium even during this state. Related MR-011 conditions reversals on volume; this card uses no volume. MR-002's behavioural reversal and FP-002's inventory pressure are related mechanisms, not added signals here.

## Exact user-fixed rule

On the first session of each month, all signal closes end on the preceding session. Compute SPY daily log returns and their annualised rolling 63-session sample standard deviation, using the lab's annualisation convention. Compare the latest available volatility with the median of its preceding 756 observations, excluding the latest volatility from that reference history. Stress requires a strict excess over the median. Full fixed-window history is needed to establish stress; before it exists the condition cannot trigger a holding.

In stress, each tradable fund with a trailing 21-session return below the compounded bill over the same trailing interval receives exactly 1/7. All remaining slots stay in cash. Outside stress the complete target is all cash. There is no ranking, fit, leverage, extra filter or reallocation of unused slots. Decisions remain monthly.

The only parameter is lookback=21, with neighbours 16/26 at 25% and 10/32 at 50%. The volatility window 63 and historical-median window 756 are fixed code constants, not parameters or alternative trials. Memory is the user-fixed 830 sessions; it covers the nested volatility/median window plus the lag and every return neighbour. The code uses bounded rolling windows, not expanding or cumulative signal state.

## Prediction, scope and rejection

The economic prediction is positive benchmark-relative value from reversal in stress. The user specified no numerical performance magnitude, so none is invented; validation uses the lab's existing gates. The benchmark remains the same funds held always in equal parts. No paired difference against MR-001-01 or TM-017-01 is computed outside the official tool, and the known missing reference commit still prevents the latter comparison.

The complete card is committed alone before build-plan.md or strategy.py is written. It has one base variant and one official run, with its registry entry committed alone immediately afterwards. Any gate failure is reported without changing the card, fixed windows, code, threshold or parameter. The diagnostic and prior results do not justify an undisclosed power calculation or an extra attempt; none is made.
