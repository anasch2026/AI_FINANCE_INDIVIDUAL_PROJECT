# TM-017-09 — Volatility-weighted trend: unrun specification

**No financial verdict: skipped before a real run.** This is the third specified capstone follow-up. Anas fixed the rule before either newly requested card ran. Its isolated card commit precedes its code. The official --check passes, but --try exits with code 1:

```text
refused: undefined inverse-volatility denominator on 2006-03-01: tradable fund(s) without a defined full 63-session volatility: DBC; the fixed rule supplies no exclusion, imputation or fallback
```

DBC becomes tradable on 2006-02-06 in both the frozen manifest and the lab universe. At the monthly decision identified by the official preflight, it lacks the full fixed volatility history while other trend holdings require a denominator. The rule explicitly includes every tradable fund, held or not. Dropping DBC, using a shorter volatility estimate, imputing a value or making the whole portfolio cash would change the prescribed allocation. No such substitute is used.

## Gates and interpretation

Gates 1–7 are all **not run**, not failures or zeros. No Sharpe, alpha, placebo rank or holdout metric exists for this card. It adds no registered return trial. A check of the official opening record confirms the holdout is unopened and the registry has no line for this identifier. The in-sample preflight is not a backtest.

Consequently, this card provides no financial evidence about whether volatility weighting improves the plain trend rule or reduces SPY's profit share. It identifies a missing-data convention that would have to be specified in a separate authorised hypothesis. The current locked card and code remain unchanged, and no substitute or extra card is drawn.

Prior holdout outcomes of TM-017-06/07/08 and MR-001-01 were already known; MR-001-02 was also completed before this code was tried, without altering the user-fixed rule. This exposure remains disclosed. No raw holdout data is examined for this preflight or used to repair the specification.

Sources: .git/codex-logs/try-TM-017-09-volatility-weighted-trend.log; alpha-lab/data/manifest.json, DBC.csv first date; alpha-lab/lab/universe.py, DBC first_session; this card's card.yaml, reasoning.md and strategy.py; official registry.opened() inspection. The specification's literature motivation is Moskowitz, Ooi and Pedersen (2012); an unexecuted implementation cannot validate or refute that evidence.

Later authorised repair: Anas specified TM-017-10 in a separate request, excluding undefined-volatility funds from both holdings and denominator. That new card ran once and first failed gate 3. TM-017-09 itself remains unchanged, unrun and without a financial result.
