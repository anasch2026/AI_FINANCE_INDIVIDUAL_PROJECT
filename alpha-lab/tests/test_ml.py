"""The walk-forward forecasts of lab/ml.py (TM-017-03 to -05), on synthetic prices: no look-ahead, no
read older than the memory, a planted trend found and a random walk not, the lab's conventions kept."""
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from lab import ml

MEMORY = 2400


def market(seed: int, beta: float, k: int = 7):
    """21 years of daily closes; with beta > 0, a slow persistent drift that past returns reveal."""
    rng = np.random.default_rng(seed)
    days = pd.bdate_range("2005-01-03", "2025-12-31")
    n = len(days)
    u, shocks = np.zeros((n, k)), rng.normal(size=(n, k))
    for t in range(1, n):
        u[t] = 0.998 * u[t - 1] + np.sqrt(1 - 0.998 ** 2) * shocks[t]
    returns = rng.normal(0.0002, 0.01, (n, k)) + beta * 0.001 * u
    prices = pd.DataFrame(100 * np.cumprod(1 + returns, axis=0), index=days, columns=[f"A{j}" for j in range(k)])
    prices.iloc[:300, -1] = np.nan                      # one fund starts late
    return SimpleNamespace(prices=prices, signal_prices=prices.copy(), tradable=prices.notna(),
                           rf=pd.Series(0.02 / 252, index=days))


def asof(m, day):
    cut = slice(None, day)
    return SimpleNamespace(prices=m.prices.loc[cut], signal_prices=m.signal_prices.loc[cut],
                           tradable=m.tradable.loc[cut], rf=m.rf.loc[cut])


def same(a, b):
    return np.allclose(a.fillna(-1).to_numpy(), b.fillna(-1).to_numpy(), atol=1e-12)


@pytest.mark.parametrize("model", ml.MODELS)
def test_conventions_look_ahead_and_memory(model):
    m = market(1, beta=1.0)
    pos = ml.positions(m, model=model, window=60, memory=MEMORY)
    held = pos.dropna(how="all")
    assert (held >= 0).all().all() and (held.sum(axis=1) <= 1 + 1e-12).all()
    assert held.index[0] > m.prices.index[60 * 20]       # no target before a full window of months
    assert (held.index.month != np.r_[0, held.index.month[:-1]]).all()   # monthly
    rng = np.random.default_rng(0)
    for day in rng.choice(held.index, 6, replace=False):
        assert same(ml.positions(asof(m, day), model, 60, MEMORY).loc[[day]], pos.loc[[day]])
        i = m.prices.index.get_loc(day)
        cut = i - MEMORY - 1
        if cut > 0:
            seen = asof(m, day)
            moved = seen.signal_prices.copy()
            moved.iloc[:cut] = moved.iloc[:cut].to_numpy() * rng.uniform(0.5, 1.5, moved.iloc[:cut].shape)
            seen.signal_prices, seen.prices = moved, moved
            assert same(ml.positions(seen, model, 60, MEMORY).loc[[day]], pos.loc[[day]])


@pytest.mark.parametrize("model", ml.MODELS)
def test_a_planted_trend_is_found_and_noise_is_not(model):
    def skill(m):
        f = ml.forecasts(m, model, 60, MEMORY).dropna(how="all")
        ahead = m.signal_prices.pct_change(21, fill_method=None).shift(-21).reindex(f.index)
        return f.corrwith(ahead, axis=1, method="spearman").mean()
    assert skill(market(1, beta=1.0)) > 0.1
    assert abs(skill(market(2, beta=0.0))) < 0.08


def test_an_unknown_model_is_refused():
    with pytest.raises(ValueError):
        ml.positions(market(0, 0.0), model="neural-net", window=60, memory=MEMORY)
