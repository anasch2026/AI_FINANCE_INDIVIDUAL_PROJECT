# AGENTS.md — Capstone "AI for Finance" (IE Business School, MiF) — briefing for the coding agent

Read this whole file, then `alpha-lab/RUNBOOK.md` and `alpha-lab/ML-CAPSTONE.md`, before doing anything.
Talk to the user in **French**, simply and briefly: he is not a developer. Explain any command before running it.

---

## 1. Who and what

- User: **Anas Chantah**, student of the Master in Finance (MiF), IE Business School, Madrid. Mac (Apple Silicon).
- Course: **AI for Finance**, Prof. **Josep Gisbert** (josep.gisbert@ie.edu), fall 2026.
- Project: the **individual capstone** (50% of the course grade). Anas builds an ML layer on top of
  **Alpha Factory**, a strategy-validation framework he co-founded with **Sami Andaloussi** before the course.
- Research question: **do ML signals survive strict out-of-sample validation where rule-based strategies fail?**

## 2. What the course asks (from Lecture 1 slides)

- Grading: Group presentation 20%, **Individual applied project (capstone) 50%**, Final exam 25%, Participation 5%.
- Capstone, choose one:
  1. **Build an ML-driven finance application** — "creating your novel finance application based on the course's topics" ← **chosen option**
  2. Replicate an empirical finance paper using ML methods, with an innovation.
- Capstone deliverables: a **manuscript** (written report) and an **individual presentation**.
  Sessions 14 and 15 of the course are the "Capstone defences".
- **GenAI policy: encouraged, with disclosure** (the use of AI agents must be declared in the manuscript).
- Academic integrity is part of participation expectations.
- The detailed rubric and guidelines are in a "Capstone Project" folder on Blackboard Ultra (not yet read
  by the agent; if the user provides them, they override anything here).
- Course topics covered so far: Lecture 2 linear & logistic models (OLS, Lasso, Ridge, Elastic Net, logit),
  Lecture 3 tree-based & ensemble methods (decision trees, Gini/entropy, Random Forest, boosting,
  subsampling, learning rate). Later: deep learning, LLMs, reinforcement learning, AI agents.

## 3. The professor's approval

Email sent by Anas (subject "AI for Finance – Capstone project proposal"), summarised: Alpha Factory was
co-founded before the course with Sami Andaloussi; early development was on Sami's machine and GitHub
account, so the repository history shows his name; the framework is used only as an evaluation tool,
cited as prior work; Anas's contribution is the ML layer (Elastic Net, Random Forest, gradient boosting,
walk-forward), the research question, and the experiments, results and analysis, done during the course
and committed under his own name. Framework link: https://github.com/Sami-Andaloussi/alpha-factory (alpha-lab).

**Professor's reply (11 Nov 2026), verbatim:**
> Hi Anas,
> Yes, this fits the novel finance application option. Please go ahead.
> Using Alpha Factory as an evaluation tool is fine, as long as you clearly cite it as prior work and commit
> all new ML code, experiments, and analysis under your own name. Only this new work will be graded.
> Curious to see if any ML signals survive the gates.
> Best,
> Josep

Consequences for you:
- **Every new commit must be authored by Anas Chantah** (git user already configured in this clone; check
  with `git config user.name` before committing; never change it).
- **Never rewrite history** (no amend, rebase, squash, filter-branch, author rewrite). The pre-course
  commits stay as they are, under Sami's name.
- **Do not modify existing lab files.** Only new files, plus what the lab itself regenerates (STATUS.md,
  registry lines, run outputs). The only pre-existing file edited so far is `alpha-lab/requirements.txt`
  (scikit-learn, joblib, threadpoolctl appended) — already committed.

## 4. Current state of this clone (`~/alpha-factory`)

- Local clone of github.com/Sami-Andaloussi/alpha-factory. **The git remote was removed on purpose: this
  copy is disconnected. Never add a remote, never push.** Nothing goes to GitHub.
- Python env: `~/alpha-factory/.venv` (Python 3.14, pinned requirements + scikit-learn 1.9.1).
  Activate with `cd ~/alpha-factory && source .venv/bin/activate && cd alpha-lab`, then use `python`.
  (Calling `../.venv/bin/python` instead prints harmless "Unexpected value in sys.prefix" warnings and
  breaks one notebook test: always activate.)
- Data: snapshot `2026-09-22` (21 files) + addition `2026-09-23` (5 files) in `alpha-lab/data/`,
  copied from Sami's machine. `python -m lab.data check` → both "hashes match", 5,283 sessions,
  2005-01-03 to 2025-12-31. The integrity findings it prints (large moves 2008/2020, CHF 2015, zero
  returns, volume outliers) are known and documented: not errors.
- Tests: full suite **514 passed** (after regenerating STATUS.md).
- Commits added by Anas, in this order (the lab's lock: cards before code):
  1. `card: TM-017-03-elastic-net-trend` (card.yaml + reasoning.md only)
  2. `card: TM-017-04-random-forest-trend`
  3. `card: TM-017-05-boosted-trend`
  4. `ML layer for TM-017-03 to TM-017-05` (lab/ml.py, tests/test_ml.py, requirements.txt, build-plan.md
     and strategy.py of the three cards, ML-CAPSTONE.md)
  5. `status: TM-017-03 to TM-017-05 added` (STATUS.md regenerated: 49 strategies, 4 not run yet)
- **None of the three ML cards has been run yet.**

## 5. The ML layer (what was built)

- `alpha-lab/lab/ml.py`, shared by the three cards; each `strategy.py` calls
  `ml.positions(market, model=..., window=..., memory=2400)`.
- Universe: the seven funds of TM-017-01 — **SPY, EFA, EEM, IEF, TLT, GLD, DBC** — so that `lab.compare`
  gives a paired comparison with the plain time-series momentum rule.
- Decision: first session of each month. Allocation identical to TM-017-01: 1/7 per fund held, cash otherwise.
  A fund is held when its **forecast of next month's return over the T-bill is > 0**.
- Features (8, from the fund's own closes up to the session before): returns over 21, 63, 126, 252
  sessions; 12-1 momentum (252 to 21 sessions back); annualised volatility over 63 and 126 sessions;
  close / 200-session average − 1.
- Target: the fund's return over the bill from the session before the decision to the session before the next.
- Fit: pooled across funds, **rolling window of 60 months** (`window` parameter, neighbours 30/45/75/90),
  refitted every month, standardised on the window only; memory 2,400 sessions (no read older).
- Models (hyperparameters fixed in advance, none tuned on real returns):
  - TM-017-03 **Elastic Net** — ElasticNetCV, l1_ratio {0.1, 0.5, 0.9}, alphas logspace(-4, 0, 20), TimeSeriesSplit(3) inside the window.
  - TM-017-04 **Random Forest** — 200 trees, depth 3, min 20 per leaf, max_features 0.5, random_state 0.
  - TM-017-05 **Gradient Boosting** — 150 trees, depth 2, learning rate 0.03, subsample 0.7, min 20 per leaf, random_state 0.
- Checked on synthetic prices only (tests/test_ml.py): no look-ahead, no read older than the memory,
  a planted trend found (rank IC ≈ +0.15 to +0.20), a random walk not.
- Benchmark rule TM-017-01 (already run, published verdict): Sharpe 0.50 vs 0.41 for equal-weight hold,
  alpha +1.55%/yr in-sample, **failed gate 3** (beats 81.7% of placebos, 90% needed), SPY 33% of profit.

## 6. Your task

1. For each card (03, 04, 05): `python -m lab.report --check strategies/<folder>`, then
   `python -m lab.report --try strategies/<folder>` (checks targets and timing, shows **no returns**,
   consumes nothing). Show the output. **If anything fails: STOP, explain in French, change nothing.**
2. Only if all three pass: run them for real, **one at a time, in order 03 → 04 → 05**:
   `nohup python -m lab.report strategies/<folder> > /tmp/run-<id>.log 2>&1 &`
   (logs in /tmp: a file left in the repo would block the next run, since the lab refuses anything uncommitted).
   Check the log every few minutes until the run has finished. Never start the next run before.
   After each run, RUNBOOK step 7: **commit `registry/trials.jsonl` at once, alone** (`registry: <id>`),
   then commit the run's other outputs (report notebook, STATUS.md) before the next run.
   If a run prints a refusal or an error, STOP and explain: never retry a card that has run.
3. Then `python -m lab.compare` of each card against `strategies/TM-017-01-time-series-momentum`.
4. Report, in French, a short table: for each card, the first gate failed (or "passes 1 to 7"), Sharpe,
   alpha vs benchmark, placebo rank (gate 3), and the difference with TM-017-01 from `lab.compare`.

## 7. Hard rules

- **A run is irreversible**: each card's holdout (2023–2025) opens once. Never re-run a card, never edit a
  card after its run, never "fix" anything to get a better result.
- Never edit `card.yaml`, `reasoning.md`, `bank/`, or any pre-existing lab file. Never touch Sami's work.
- Never amend, rebase, squash or rewrite commits. Never add a remote. Never push.
- **Do not write `verdict.md`**: the verdicts and the analysis are graded work; Anas writes them himself.
- No API keys, no network calls: everything runs locally.
- Ask the user before any action not listed in section 6.

## 8. What comes after (for context, not your task now)

- Manuscript (~10–15 pages): introduction (research question), literature (time-series momentum;
  ML in asset pricing, Gu, Kelly & Xiu 2020), data & method (the seven funds, features, walk-forward,
  three models, Alpha Factory's gates — cited as prior work), results (gate table per model, comparison
  with TM-017-01), discussion (why signals pass or fail; a negative result is a valid result),
  limitations, and disclosure (pre-existing framework; use of AI tools).
- Individual presentation (~10 slides) for sessions 14–15.
- Later, a separate GitHub repository under Anas's own name may be created to show the new work —
  only when the user asks.

## UPDATE (11 Nov 2026) — card ids changed
TM-017-03/04/05 were refused by the lab (their card was committed together with reasoning.md) and were
never run; they are retired. The same hypotheses are now TM-017-06-elastic-net-trend,
TM-017-07-random-forest-trend and TM-017-08-boosted-trend, each card committed alone. Everywhere this
file says 03, 04, 05, read 06, 07, 08.
