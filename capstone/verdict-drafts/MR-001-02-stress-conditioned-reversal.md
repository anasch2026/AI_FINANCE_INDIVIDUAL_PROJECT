# MR-001-02 — Stress-conditioned reversal: verdict for review

The recorded verdict is **fails gate 2, economic edge**, threshold version 4. This is capstone follow-up number 2. Anas fixed the full rule before its run. The prior holdout results of TM-017-06/07/08 and MR-001-01 were already known and disclosed. No existing card was changed or rerun.

## Gate by gate

1. Hygiene — PASS. There are 92 clustered decisions over 14.66 evaluated years, with no timing or same-day break on 100 dates and no memory break on 50 memory-check dates. Memory is 830 sessions. Effective evaluation starts 2008-05-02 after the nested stress-history warm-up.

2. Economic edge — FAIL. Net Sharpe is 0.08 against benchmark 0.34, and annual alpha is -1.37%. At doubled costs, Sharpe is 0.06 and alpha -1.52%. Conditioning on the fixed stress proxy does not establish economic edge.

3. Significance — FAIL. PSR is 0.64 against 0.95 required. The base beats 33.70% of 1,000 shifted placebos against 90.00% required. The separately reported blend rank is 34.60% and is not substituted for the base.

4. Multiple testing — FAIL. DSR is below 0.01 against 0.90 required, with 80 effective trials from 87 registered trials. The appraisal ratio is -0.23. This additional base trial remains in the accumulated testing record.

5. Stability — FAIL. The blend fails gates 2, 3 and 4. Alpha is positive in two of five predefined blocks; removing the best year, 2015, leaves alpha -2.30%. The preflight found four eligible blocks after the first holding.

6. Robustness — FAIL. The lowest nearby Sharpe retention is -32.58%, the worst cluster removal (metals) retains 12.09%, and GLD accounts for 84.15% of profit. Those fail the lab's respective requirements. Neighbour median retention is 223.60% and one-day delay retention 169.80%, ratios against a weak base rather than evidence of a useful strategy.

7. Sealed holdout — PASS. Published holdout Sharpe is 0.78 and annual alpha 1.04%, above respective floors -0.62 and -4.63%. No variant is rewritten and no timing break occurs on 20 checked dates. These saved lab figures do not reverse the first failure.

## What was learned

The user-specified realised-volatility stress state does not rescue this reversal implementation under the recorded battery. Realised SPY volatility is a proxy rather than the VIX used in Nagel's discussion; failure does not refute every state-conditioned liquidity-provision strategy. The weak economic evidence, sensitivity to a nearby horizon and concentration in gold limit this implementation. Unequal effective windows prevent a paired claim that stress improves or worsens MR-001-01; no replacement paired test is computed.

The card was locked alone, its code committed afterwards, and its one run completed normally. The registry was committed alone before the report. The rule, windows, threshold and code remain unchanged after the result. The next requested rule was fixed by Anas before this run and cannot be changed in response to its outcome.

Sources for all financial figures and gate labels: alpha-lab/strategies/MR-001-02-stress-conditioned-reversal/report.ipynb, cells 4, 10, 12, 14, 16, 18, 20, 22 and 24. Preflight output: the official --try reported during preparation. Design: card.yaml and reasoning.md. Attribution: Nagel (2012), The Review of Financial Studies, 25(7), 2005–2039.
