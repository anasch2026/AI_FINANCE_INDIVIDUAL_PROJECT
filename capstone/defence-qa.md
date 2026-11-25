# Defence questions and answers

## 1. What is your answer to the research question?

None of the three ML implementations survives the battery. Elastic Net first fails gate 1 and both ensembles fail gate 2; the reference fails gate 3. None of the follow-ups passes all seven gates either: both reversal rules fail gate 2, and TM-017-10 fails gates 3 and 4. This is a negative result for these implementations, not for every use of ML in finance.

## 2. What did you contribute beyond the existing framework?

I built the ML layer, carried out the diagnostic, designed the follow-up hypothesis, ran the experiments and analysed the evidence. Alpha Factory predates the course and is cited as prior work I co-founded with Sami Andaloussi. The new work is committed under my name.

## 3. Why did you use these model families?

Elastic Net constrains a linear model with overlapping features. Random Forest and Gradient Boosting permit nonlinear relationships through different ensemble methods. Their candidate settings were fixed before the original runs. Elastic Net selects its penalty and L1/L2 share by inner time-series cross-validation; I did not select settings after seeing favourable portfolio returns.

## 4. What did the diagnostic find?

R² against zero is -2.36%, -6.23% and -13.08% for Elastic Net, Random Forest and Gradient Boosting, and -6.77% and -15.73% for the added OLS and MLP; logistic R² is n/a. Elastic Net usually removes all slopes and predicts positive returns, while the ensembles' more active decisions do not restore forecast accuracy. The complete yearly and fund-level results remain available, including unfavourable periods.

## 5. Why does Elastic Net have only 17 decisions despite monthly refits?

All slopes are zero in 76.92% of its fits; then each fund receives the pooled intercept. Positive forecasts account for 96.90% of the decision history. Repeatedly issuing nearly the same holdings does not create many changed-target episodes, and the reconstructed count matches the report's 17 exactly.

## 6. Can you compare the rule's R² directly with the models'?

Only with a qualification. The rule supplies an entry sign, not a monthly return estimate. I use its trailing excess return divided by twelve as an explicit mechanical proxy for R²; its sign is exact, but its squared-error result depends on that scale. I do not call it a calibrated rule forecast or a portfolio return.

## 7. How did you protect the holdout during diagnosis?

I cut each raw input frame at 2022-12-31 before the lab assembled the market. All features, fits, targets and diagnostic charts use that truncated data. I score only labels whose next monthly decision is inside the cutoff, and compute no portfolio return. New holdout calculations occur only inside the official lab run.

## 8. What does alpha mean, and why is positive Sharpe insufficient?

Alpha is the annual regression intercept against passive equal-weight holding of the same funds. Sharpe measures excess return relative to volatility. Elastic Net's holdout Sharpe is 0.91 versus the rule's 0.89, yet its alpha is approximately zero; earning market-related returns is different from adding value beyond passive exposure.

## 9. Why are stable tree importances not evidence of useful forecasts?

Impurity importances describe how features helped the training fit. Their adjacent rank correlations are 0.82 and 0.79, but both ensembles still have negative forecast R². Correlated features can substitute for one another, and importance is neither a causal effect nor an out-of-sample performance contribution.

## 10. Why draw a new card rather than repair the failed model?

Changing a completed card after observing its result would turn the same experiment into an undisclosed search. I instead state a distinct liquidity-reversal hypothesis, lock it before code and retain the failed ML records. The diagnostic motivates less estimation freedom; it does not prove that the new rule works.

## 11. Did seeing the old holdout compromise the new hypothesis?

It limits the strength of confirmation, and I disclose it. The earlier 06–08 holdout outputs were already seen, so I cannot make that calendar period globally unseen again. I used only the pre-2023 diagnostic and literature for the new design and made no additional holdout calculations outside the lab, but I call the follow-up exploratory.

## 12. Why did you stop after the new rule failed?

I retained the first follow-up’s failure without changing its rule. I then fixed two further specifications before either new card ran: stress reversal was executed once and failed gate 2; the weighting card 09 was skipped when its denominator was undefined. I subsequently fixed a separate card, 10, repairing only that undefined case. It ran once and failed gate 3. No completed card was changed, and 09 stays unrun.

## 13. Why reject MR-001-01 despite its positive holdout alpha?

Its first failure is economic edge: in-sample Sharpe 0.24 and annual alpha -1.07%, with only 37.10% of placebos beaten. Its published holdout alpha is 1.06%, but a later diagnostic pass does not cancel earlier failures. The rule remains rejected under its locked evaluation procedure.

## 14. What are your most important limitations?

The official paired comparison cannot authenticate missing reference commit 9a00fbb, and effective windows differ. The universe is small and correlated. Elastic Net scales before inner CV and may split a month across folds; it also raises convergence warnings. Cards 03–05 were retired unrun after a locking error, not hidden financial failures. Prior holdout exposure further limits the follow-up.

## 15. How did you use AI, and what are you responsible for?

Claude and OpenAI Codex assisted with coding and drafting, including the diagnostic, documents and slides. I disclose their use under the course policy and remain responsible for understanding and checking the implementation, references, numbers and conclusions. I must be able to explain every submitted claim without relying on generated prose.

## 16. Did conditioning reversal on stress fix the first result?

No. The fixed SPY-volatility rule passes hygiene but fails gate 2 with Sharpe 0.08, annual alpha -1.37% and 33.70% of placebos beaten. Its positive holdout alpha does not reverse that failure. It uses realised volatility rather than VIX, and unequal effective windows prevent a paired claim about the conditioning effect. Its registered trial increases the multiple-testing burden.

## 17. Why was TM-017-09 skipped, and what does TM-017-10 change?

The exact denominator includes all tradable funds. At the 2006-03-01 preflight decision DBC lacks a full 63-session volatility, so that denominator is undefined. I had ruled out in advance any exclusion, imputation or substitute rule and required a skip if exact implementation was impossible. Card 09 remains locked but unrun, with no registry trial or holdout opening. I later specified the eligible-volatility convention in new card 10; it passes economics and robustness but first fails significance, and its DSR of 0.27 against 0.90 required means it is not a near-pass. The two records must remain distinct.

## 18. Why add logistic regression rather than another return model?

It asks directly whether the return sign can be discriminated, instead of predicting its magnitude. I use fixed L2 regularisation, C=1.00 and max_iter=1000. Its accuracy is 48.69%, AUC 0.45 and log-loss 0.71. R² is displayed as n/a; I judge the classifier by accuracy, AUC and log-loss. No probability-to-return conversion or trading strategy is added.

## 19. Why use following-month permutation importance?

Impurity importance describes training splits, while permutation asks whether an input helps a frozen model predict the next month. I use ten fixed repeats and random_state=0 on only that month's observations before 2023, with no refit. Negative importance means shuffling improved error. Correlated inputs and small cross-sections make it noisy; I report all features and do not use the findings to tune another model.

## 20. Could transaction costs explain the ML failures?

No. The published annual cost drag is 0.04% to 0.30% (Table 3). The ML strategies' gross Sharpe ratios, before any cost, are 0.31, 0.09 and 0.12 against a benchmark of 0.39, so they lack an edge before trading. The ensembles have greater annual cost drag than the rule (0.13% and 0.19% against 0.08%), without positive net alpha; cost drag is not a direct turnover statistic.

## 21. Explain the deflated Sharpe ratio in one breath.

It is a model-based significance measure for benchmark-hedged returns against an expected-by-luck Sharpe hurdle, allowing for non-normal returns. This lab groups near-clone trials for the effective count, so registered and effective trials are not identical. TM-017-10's DSR of 0.27 means that, after 88 trials, its result is far from the 0.90 the battery requires. This is a model-based, selection-adjusted statistic, not a posterior probability that the strategy will be profitable.

## 22. What exactly are the shifted placebos?

Each placebo shifts the strategy's own weight history in time by a different offset, wrapping around the sample, so it keeps the same pattern of holdings but loses the timing. If the timing has value, the real strategy should beat at least 90% of 1,000 such placebos. TM-017-10 beats 89.80%, so roughly one placebo in ten does as well as the real timing; the plain rule beats 81.70%.

## 23. Why do you report no maximum drawdown or turnover?

The lab's saved reports do not publish them, and I did not compute new performance statistics outside the official runs. Annual cost drag describes the cost burden; it is not a published turnover measurement. I state this limitation in Section 4 rather than adding unlocked calculations after seeing the results.

## 24. What would you need before deploying any of these strategies?

A strategy that passes all seven gates first, then untouched data such as live paper trading, because the 2023–2025 holdout has already been seen. Production would require a jurisdiction- and activity-specific compliance assessment, documented model governance, independent validation and order controls; I have not established regulatory readiness. Monitoring would have to detect failures such as Elastic Net collapsing to a constant forecast.

Sources: original and new report.ipynb files identified in results.csv; diagnostic tables and summary.json; unchanged strategy.py files for implementation details; new card.yaml and reasoning.md; capstone/results-notes.md for the full mapping and STOPPED.md for the comparison refusal. No additional performance test is introduced in these answers.
