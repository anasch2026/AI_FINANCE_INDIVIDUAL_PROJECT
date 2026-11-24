"""User-fixed stress-conditioned liquidity reversal; see build-plan.md.

Written after the isolated card commit. Only lookback is a parameter.
"""
import numpy as np
import pandas as pd

VOL_WINDOW = 63
MEDIAN_WINDOW = 756


def positions(market, lookback):
    prices = market.signal_prices
    # 1–2. At decision t compare vol[t-1] with the median ending at t-2.
    spy_log = np.log(prices['SPY'] / prices['SPY'].shift(1))
    vol = spy_log.rolling(VOL_WINDOW).std(ddof=1) * np.sqrt(252)
    reference = vol.shift(1).rolling(MEDIAN_WINDOW).median()
    stress = vol.gt(reference).shift(1, fill_value=False)
    # 3. Both endpoints and the compounded bill end on the prior session.
    past = prices.shift(1) / prices.shift(lookback + 1) - 1
    bill = (1 + market.rf.fillna(0.0)).rolling(lookback).apply(np.prod, raw=True).shift(1) - 1
    # 4. Fixed slots: no redistribution from unheld funds and all cash otherwise.
    buy = past.lt(bill, axis=0) & market.tradable
    weights = buy.mul(stress, axis=0).astype(float) / 7
    # 5. Month starts use no future calendar observation.
    index = prices.index
    first = pd.Series(np.r_[True, index.month[1:] != index.month[:-1]], index=index)
    return weights.where(first, axis=0)
