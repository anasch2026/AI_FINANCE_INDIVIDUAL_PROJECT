"""MR-001-01: a fixed monthly liquidity-reversal implication; see build-plan.md.

Written after the isolated card commit. No fitted coefficients, files, lab
imports, network, optimisation or post-result parameter selection.
"""
import numpy as np
import pandas as pd


def positions(market, lookback):
    prices = market.signal_prices
    # 1. Both endpoints and the full price window end on the prior session.
    past = prices.shift(1) / prices.shift(1 + lookback) - 1
    known = prices.shift(1).rolling(lookback + 1).count().eq(lookback + 1)
    # 2. Exactly that trailing interval, with bounded state and no current bar.
    bill = (1 + market.rf.fillna(0.0)).rolling(lookback).apply(np.prod, raw=True).shift(1) - 1
    # 3. Provide liquidity after relative selling pressure; unused slots are cash.
    buy = past.lt(bill, axis=0) & known & market.tradable
    weights = buy.astype(float) / prices.shape[1]
    # 4. A complete target row at each month start; hold between decisions.
    index = prices.index
    first = pd.Series(np.r_[True, index.month[1:] != index.month[:-1]], index=index)
    return weights.where(first, axis=0)
