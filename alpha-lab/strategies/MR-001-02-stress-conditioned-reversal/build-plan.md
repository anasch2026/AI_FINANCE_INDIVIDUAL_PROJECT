# MR-001-02 — Build plan

Written after the isolated card commit, implementing only Anas's fixed rule.

1. Compute SPY daily log returns and rolling sample volatility over the fixed 63 sessions, annualised by the lab's trading-session convention.
2. Compute the median of the previous 756 volatility observations with a separate lag, then lag the strict above-median comparison to the session before the decision. No current volatility enters its reference median.
3. Compute each fund's lookback return and the compounded bill over the same interval ending on the preceding session, using bounded rolling state.
4. In stress, allocate exactly one seventh per tradable fund below the bill. Outside stress, set every slot to zero. No extra signal, fit or filter.
5. Emit targets on the first session of each month, NaNs between decisions. The two stress windows are fixed constants and lookback is the only parameter. Validate chronology and the user-fixed 830-session memory with --check and --try before the single run.
