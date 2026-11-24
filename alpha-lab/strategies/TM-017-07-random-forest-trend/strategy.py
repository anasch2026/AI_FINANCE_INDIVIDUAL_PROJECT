"""TM-017-07-random-forest-trend: time-series momentum with the rule replaced by a fitted random-forest forecast (build-plan.md).

Self-contained: the lab refuses a strategy that imports it, so the walk-forward code is here in full.
It is the same code in TM-017-06, -07 and -08 (only the card's `model` differs), identical to
lab/ml.py, which tests/test_ml.py checks on synthetic prices (no look-ahead, memory bound, a planted
trend found and a random walk not).
"""
import hashlib

import numpy as np
import pandas as pd

LOOKBACK = 252          # the oldest close a feature reads, in sessions back from the session before
FEATURES = ("r21", "r63", "r126", "r252", "r252x21", "vol63", "vol126", "ma200")
MIN_ROWS = 100          # the fewest asset-months a fit takes
MODELS = ("elastic-net", "random-forest", "gradient-boosting")
_FITS: dict = {}
_MAX_FITS = 20000


def decision_rows(index: pd.DatetimeIndex) -> np.ndarray:
    """Positions of the first session of each month, the first session of the index excluded (it has
    no close before it)."""
    first = np.r_[True, index.month[1:] != index.month[:-1]]
    first[0] = False
    return np.flatnonzero(first)


def features_at(closes: np.ndarray, p: int) -> np.ndarray:
    """The features of every asset at decision position p, from the closes p-1-LOOKBACK to p-1;
    NaN for an asset without a full window. Shape (assets, features)."""
    w = closes[p - 1 - LOOKBACK:p]                      # LOOKBACK + 1 closes, the last at p-1
    last = w[-1]
    r = lambda k: last / w[-1 - k] - 1.0                # return over the last k sessions
    logret = np.log(w[1:] / w[:-1])
    vol = lambda k: logret[-k:].std(axis=0, ddof=1) * np.sqrt(252)
    ma200 = last / w[-200:].mean(axis=0) - 1.0
    out = np.column_stack([r(21), r(63), r(126), r(252), w[-22] / w[0] - 1.0, vol(63), vol(126), ma200])
    out[np.isnan(w).any(axis=0)] = np.nan
    return out


def outcome(closes: np.ndarray, bill: np.ndarray, p: int, q: int) -> np.ndarray:
    """Each asset's return over the bill from the close p-1 to the close q-1."""
    cash = np.prod(1.0 + bill[p:q]) - 1.0
    return closes[q - 1] / closes[p - 1] - 1.0 - cash


def make(model: str):
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    from sklearn.linear_model import ElasticNetCV
    from sklearn.model_selection import TimeSeriesSplit
    if model == "elastic-net":
        # the penalty and the L1 share chosen by time-ordered cross-validation inside the window only
        return ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9], alphas=np.logspace(-4, 0, 20), cv=TimeSeriesSplit(3),
                            max_iter=10000)
    if model == "random-forest":
        return RandomForestRegressor(n_estimators=200, max_depth=3, min_samples_leaf=20, max_features=0.5,
                                     random_state=0, n_jobs=1)
    if model == "gradient-boosting":
        return GradientBoostingRegressor(n_estimators=150, learning_rate=0.03, max_depth=2, subsample=0.7,
                                         min_samples_leaf=20, random_state=0)
    raise ValueError(f"unknown model {model!r}: one of {', '.join(MODELS)}")


def fitted(model: str, X: np.ndarray, y: np.ndarray):
    """The model fitted on (X, y), standardised with the window's own means and deviations; cached on
    the exact bytes of the data."""
    key = hashlib.sha256(model.encode() + X.tobytes() + y.tobytes() + str(X.shape).encode()).hexdigest()
    if key not in _FITS:
        mean, std = X.mean(axis=0), X.std(axis=0)
        std[std == 0] = 1.0
        scale = y.std() or 1.0
        estimator = make(model).fit((X - mean) / std, y / scale)
        if len(_FITS) >= _MAX_FITS:
            _FITS.clear()
        _FITS[key] = (estimator, mean, std, scale)
    return _FITS[key]


def predict(fit, X: np.ndarray) -> np.ndarray:
    estimator, mean, std, scale = fit
    return estimator.predict((X - mean) / std) * scale


def forecasts(market, model: str, window: int, memory: int) -> pd.DataFrame:
    """The forecast of each asset's return over the bill for the month ahead, on each decision date
    whose fit has `window` months behind it; NaN elsewhere."""
    if model not in MODELS:
        raise ValueError(f"unknown model {model!r}: one of {', '.join(MODELS)}")
    index, columns = market.signal_prices.index, market.signal_prices.columns
    closes = market.signal_prices.to_numpy(dtype=float)
    bill = market.rf.reindex(index).fillna(0.0).to_numpy(dtype=float)
    rows = decision_rows(index)
    rows = rows[rows >= LOOKBACK + 1]                   # a decision needs a full window of closes
    feats = {p: features_at(closes, p) for p in rows}
    out = pd.DataFrame(np.nan, index=index, columns=columns)
    for k in range(window, len(rows)):
        i = rows[k]
        oldest = i - 1 - memory                         # the oldest close the fit may read
        X, y = [], []
        for j in range(k - window, k):                  # the last `window` months, each closed by i
            p, q = rows[j], rows[j + 1]
            if p - 1 - LOOKBACK < oldest:
                continue
            f, o = feats[p], outcome(closes, bill, p, q)
            keep = ~np.isnan(f).any(axis=1) & ~np.isnan(o)
            X.append(f[keep])
            y.append(o[keep])
        if not X:
            continue
        X, y = np.vstack(X), np.concatenate(y)
        if len(y) < MIN_ROWS:
            continue
        now = feats[i]
        known = ~np.isnan(now).any(axis=1)
        values = np.full(len(columns), np.nan)
        if known.any():
            values[known] = predict(fitted(model, X, y), now[known])
        out.iloc[i] = values
    return out


def _positions(market, model: str, window: int, memory: int) -> pd.DataFrame:
    """Targets: on each decision date with a forecast, each tradable asset whose forecast is above zero
    holds 1/N of the portfolio, N the universe's size; the rest stays in cash."""
    f = forecasts(market, model, window, memory)
    decided = f.notna().any(axis=1)
    held = (f > 0) & market.tradable.reindex_like(f).fillna(False).astype(bool)
    weights = held.astype(float) / f.shape[1]
    return weights.where(decided, axis=0)


MEMORY = 2400   # the card's memory: no fit reads a close older than this many sessions before the session before


def positions(market, model, window):
    # steps 1 to 5 of the build plan: decision dates, features, outcomes, rolling fit, targets
    return _positions(market, model=model, window=window, memory=MEMORY)
