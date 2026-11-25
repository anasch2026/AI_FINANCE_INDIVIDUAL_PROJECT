# TM-017-06-elastic-net-trend — Elastic net trend: reasoning

## Why this theory now

TM-017-01 tested time-series momentum in its plainest form on seven funds and stopped at gate 3: a
Sharpe ratio of 0.50 against 0.41 for the funds held always, an alpha of 1.55% a year, but a rank of
81.7% among its placebos, short of 90%. The rule fixes everything by hand: one feature, the past
return, one threshold, the bill. This card asks whether a model fitted on the recent past, reading
several features of the same prices, times the same funds better: the question of the empirical
machine-learning literature in asset pricing (Gu, Kelly and Xiu, 2020), asked here of seven funds
and one decision a month. It is one of three cards, one per model of the course AI for Finance
(IE Business School, MiF): an elastic net (TM-017-06), a random forest (TM-017-07) and gradient
boosting (TM-017-08). The three are trials of the registry, and gate 4 counts them.

## From the mechanism to a signal

- **The model** is an elastic net, a linear model whose penalty shrinks the weights of the features and sets some to zero, the penalty and its L1 share chosen by time-ordered cross-validation inside the window. A linear forecast, the course's first model: the plain rule is one feature with a fixed weight and a fixed threshold, the elastic net weighs eight features and learns the weights, and its penalty is the course's answer to correlated features (the returns over overlapping lookbacks are).

- **The universe** is TM-017-01's seven funds, so that `lab.compare` can set this card's alpha
  against the rule's over the same sessions: the claim is that fitting adds to the rule, not that a
  model earns something on another universe.
- **The allocation** is the rule's: a seventh per fund held, cash otherwise, on the first session of
  each month. Only the decision to hold changes.
- **The features** are eight, all from the fund's own closes, read up to the session before: returns
  over 21, 63, 126 and 252 sessions (the horizons TM-017's sources name), the return from 252 to 21
  sessions back (the momentum of the academic construction, without the last month), volatility over
  63 and 126 sessions (trends pay differently in calm and in stress), and the distance of the close
  to its 200-session average (the moving-average form of trend). No other data: the theory is about
  an asset's own past.
- **The outcome** is the fund's return over the bill from the session before the decision to the
  session before the next: the excess return the rule's threshold compares with zero.
- **The fit** pools the funds: each row is one fund in one month, seven rows a month, about 420 in a
  window of 60 months. A model per fund would have 60 rows, too few. Features are standardised with
  the window's own means and deviations, the outcome scaled by its deviation.
- **The window** is 60 months, five years, rolling: long enough for a few hundred rows, short enough
  that the fit follows a form that shifts. A window that expands reads the whole history, which the
  lab's memory forbids; a rolling one is bounded. Its neighbours, 30 to 90 months, test the choice.
- **The memory** is 2,400 sessions: the longest window, 90 months of at most 23 sessions, plus the
  252 sessions the oldest feature reads, plus the session before; the code drops any row older.
- **The hyperparameters** are fixed here, before any run, at the course's conservative settings;
  none is tuned on the in-sample returns. An elastic net, a linear model whose penalty shrinks the weights of the features and sets some to zero, the penalty and its L1 share chosen by time-ordered cross-validation inside the window.

## Options rejected

- **A neural network**: a few hundred rows per fit are too few for it to beat the trees; the course
  puts it later, and Gu, Kelly and Xiu fit theirs on millions of stock-months.
- **A wider universe** (the 22 funds of the lab): more rows, but no paired comparison with
  TM-017-01, which is the question.
- **A forecast that ranks the funds** (hold the top third): it would test cross-sectional momentum,
  TM-001, not this theory.
- **Choosing among the three models in a walk-forward**: it would be a fourth trial, and it hides
  which model does what.

## What the lab has published about this period

TM-017-01's verdict, on the same seven funds and the same in-sample period: Sharpe ratio 0.50 against
0.41, alpha 1.55% a year, gate 3 failed at 81.7%, SPY carrying 33% of the profit (gate 6). TM-017-02's
verdict on one-month trend, on the same funds, stops at gate 2. Nothing was computed on the in-sample
returns for this card: the code was checked on synthetic prices only (a planted trend found, a
random walk not; no look-ahead; no target moved by closes older than the memory).

## Why this card replaces TM-017-03

TM-017-03 holds the same hypothesis, but its card was committed together with its reasoning, and the
lab refuses a card whose locking commit holds other files ("the card is committed alone"). It was
never run: no registry line, its holdout never opened (`lab.report` refused it before any gate). A
locking commit cannot be changed without rewriting history, so the hypothesis is carried, unchanged,
into this new card, committed alone; TM-017-03 to -05 are retired without a run.
