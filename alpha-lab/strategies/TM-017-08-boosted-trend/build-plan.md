# TM-017-08-boosted-trend — Build plan

`strategy.py` holds the whole walk-forward code (the lab refuses a strategy that imports it); the same code, identical to `lab/ml.py`, is in TM-017-06 to TM-017-08, and the three cards differ by `model`. Function names below are those of `strategy.py`.

1. **Decision dates**: the first session of each month (`ml.decision_rows`), as TM-017-01.
2. **Features** of each decision date p, read from `market.signal_prices` between p-1-252 and p-1,
   with numpy on that window alone (`ml.features_at`), NaN for a fund without a full window.
3. **Outcomes** of each month: the close at q-1 over the close at p-1, less the bill compounded from
   p to q-1 (`ml.outcome`); a month enters a fit made at i only once q <= i.
4. **Fit** at each decision i from the `window` months before it, rows older than i-1-memory left out,
   at least 100 rows (`ml.forecasts`); standardised on the window, cached on the data's bytes so the
   battery's repeated calls refit nothing they have fitted.
5. **Targets**: a seventh (1/N of the market handed) per tradable fund whose forecast is above zero,
   the rest cash; NaN between decisions and before the first fit (`ml.positions`).

Checked before any run on real data, on synthetic prices: the targets of 8 random decision dates are
unchanged when the future is cut, and when the closes older than the memory are scrambled; a planted
trend gives a rank correlation of about +0.15 to +0.20 between forecasts and next-month returns, a
random walk about zero.
