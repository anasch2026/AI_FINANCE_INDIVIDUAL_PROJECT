# MR-001-01 — Build plan

Written after the isolated card commit. The strategy is self-contained and imports only numpy and pandas.

1. Read market.signal_prices, never today's closing return. Use shifted closes for the trailing lookback return; require a full nonmissing lagged price window.
2. Compute the compounded bill return with a bounded rolling product, shifted one session, over exactly the sessions between those closes. Avoid cumulative or expanding state.
3. A fund whose lagged return is strictly below that bill and that trades today receives one universe slot, one seventh in the card's universe. Every other fund receives zero. No fitted model or cross-sectional selection is introduced.
4. Emit complete target rows on the first session of each calendar month and NaNs between decisions. Initial insufficient history means cash. Month starts use only the index up to each decision, never the next month's date.
5. The largest neighbour uses 32 sessions back from the prior close, consistent with the fixed memory. Validate with the official --check and --try only; no strategy-return script or parameter selection precedes the one official run.
