"""Exact user-fixed inverse-volatility trend rule; no missing-value substitute.

The feasibility error preserves the prescribed all-tradable denominator rather
than silently changing its definition. See reasoning.md and build-plan.md.
"""
import numpy as np
import pandas as pd

VOL_WINDOW = 63


def positions(market, lookback):
    prices = market.signal_prices
    past = prices.shift(1) / prices.shift(lookback + 1) - 1
    bill = (1 + market.rf.fillna(0.0)).rolling(lookback).apply(np.prod, raw=True).shift(1) - 1
    held = past.gt(bill, axis=0) & market.tradable
    logs = np.log(prices / prices.shift(1))
    vol = logs.rolling(VOL_WINDOW).std(ddof=1).shift(1) * np.sqrt(252)
    # Every tradable fund enters, including one whose volatility is undefined.
    inverse = (1 / vol).where(market.tradable, 0.0)
    denominator = inverse.sum(axis=1, skipna=False)
    index = prices.index
    first = pd.Series(np.r_[True, index.month[1:] != index.month[:-1]], index=index)
    invalid = first & held.any(axis=1) & (~np.isfinite(denominator) | denominator.le(0))
    if invalid.any():
        when = invalid.index[invalid][0]
        bad = market.tradable.loc[when] & (~np.isfinite(vol.loc[when]) | vol.loc[when].le(0))
        names = ', '.join(vol.columns[bad])
        raise ValueError(f'undefined inverse-volatility denominator on {when.date()}: '
                         f'tradable fund(s) without a defined full 63-session volatility: {names}; '
                         'the fixed rule supplies no exclusion, imputation or fallback')
    weights = inverse.div(denominator, axis=0).where(held, 0.0)
    return weights.where(first, axis=0)
