"""Anas's fixed repair of unrun TM-017-09; see build-plan.md.

Only undefined-volatility membership changes. No volatility floor or imputation.
"""
import numpy as np
import pandas as pd

VOL_WINDOW = 63


def positions(market, lookback):
    prices = market.signal_prices
    past = prices.shift(1) / prices.shift(lookback + 1) - 1
    bill = (1 + market.rf.fillna(0.0)).rolling(lookback).apply(np.prod, raw=True).shift(1) - 1
    logs = np.log(prices / prices.shift(1))
    vol = logs.rolling(VOL_WINDOW).std(ddof=1).shift(1) * np.sqrt(252)
    # The sole repair: missing volatility excludes a fund from both sets.
    eligible = market.tradable & np.isfinite(vol)
    held = past.gt(bill, axis=0) & eligible
    inverse = (1 / vol).where(eligible, 0.0)
    denominator = inverse.sum(axis=1, skipna=False)
    index = prices.index
    first = pd.Series(np.r_[True, index.month[1:] != index.month[:-1]], index=index)
    invalid = first & held.any(axis=1) & (~np.isfinite(denominator) | denominator.le(0))
    if invalid.any():
        when = invalid.index[invalid][0]
        raise ValueError(f'undefined inverse-volatility allocation on {when.date()}; '
                         'the fixed rule supplies no volatility floor or alternate allocation')
    weights = inverse.div(denominator, axis=0).where(held, 0.0)
    return weights.where(first, axis=0)
