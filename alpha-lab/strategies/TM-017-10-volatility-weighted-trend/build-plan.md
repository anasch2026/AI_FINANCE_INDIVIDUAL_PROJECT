# TM-017-10 — Build plan

Written after the isolated card commit. Implement exactly Anas's missing-volatility repair.

1. Compute trailing fund returns and the compounded bill with bounded rolling history, both ending on the preceding session.
2. Compute annualised daily-log-return sample volatility over the fixed 63 sessions and lag it one session. Eligibility is tradability plus defined volatility; undefined-volatility funds are not held or included in the denominator.
3. Sum inverse volatilities over every eligible fund, including unheld funds. Do not normalise only over positive-trend holdings or impute missing volatility.
4. Give each eligible fund that beats the bill its inverse-volatility slot divided by the sum. Leave unheld slots in cash; with no holdings targets are zero. A truly undefined reciprocal/denominator raises an error rather than introducing a floor.
5. Emit complete targets on month starts and NaNs between. Lookback is the only parameter; memory 400 covers all prescribed neighbours and the volatility window. Use the official --check and --try before one official run, without another return calculation.
