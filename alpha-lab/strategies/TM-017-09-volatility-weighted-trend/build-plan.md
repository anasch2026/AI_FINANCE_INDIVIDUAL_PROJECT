# TM-017-09 — Exact volatility-weighted trend

Written after the isolated card commit. No undefined volatility is replaced or silently omitted.

1. Compute the user's trailing fund return and compounded bill, both ending on the preceding session. Only lookback is a parameter.
2. Compute annualised daily-log-return sample volatility over exactly 63 sessions, also lagged one session. This is a fixed window.
3. Sum inverse volatility over every tradable fund, including unheld funds. Untradable funds contribute nothing; an undefined volatility of a tradable fund must not disappear through a skip-NaN sum.
4. At a monthly decision with holdings, raise a clear feasibility error if this exact denominator is undefined. This does not supply an alternative allocation; it exposes a missing rule so that --try can refuse and the user-mandated skip can be followed.
5. Where defined, give each positive-trend tradable fund its inverse-volatility slot divided by that complete denominator; leave unheld slots in cash. Targets are monthly and state is bounded by the fixed 400-session memory. No floor, imputation, shortened volatility history, new start date or extra trading filter is introduced.
