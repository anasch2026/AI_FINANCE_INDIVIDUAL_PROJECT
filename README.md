# AI for Finance — final capstone

Anas Chantah · Master in Finance, IE Business School · Type A application

**Financial objective:** assess whether learned monthly entry signals add validated, cost-adjusted value to a seven-ETF allocation relative to passive holding and a fixed trend rule. No tested strategy passes all seven validation gates.

## Open these deliverables

| Deliverable | File |
|---|---|
| Final manuscript | `capstone/manuscript.docx` |
| Manuscript source | `capstone/manuscript.md` |
| Main defence — four slides, maximum two minutes | `capstone/presentation.pptx` |
| Spoken text and slide notes | `capstone/defence-script.md` |
| Fifteen-slide backup for questions | `capstone/presentation-backup.pptx` |
| Twenty-four preparation questions | `capstone/defence-qa.md` |
| Numerical provenance | `capstone/results-notes.md` |
| Compliance and integrity audit | `capstone/verification-report.json` |
| Official requirements | `instructions/AI_for_Finance_Capstone_Guidelines.pdf` and `instructions/AI_for_Finance_Capstone_Rubric.pdf` |

The deadline is the official start time of Session 13, as stated in the official guidelines. The exact calendar time must be taken from the course submission task.

## One-command saved-output reconstruction

With the documented packages already available, run from this directory:

```sh
python -B reproduce.py
```

The command checks the input hashes, transcribes financial tables from the executed notebooks, redraws the manuscript figures from saved results and diagnostic CSVs, exports the Word, rebuilds both decks, and audits every numerical table against its sources. It performs **no download, installation, model fitting, forecasting, strategy execution, portfolio calculation or holdout reopening**.

`verify_submission.py` can also be run alone. Its JSON report gives the abstract and body word counts, slide counts, spoken word count, integrity checks and scope. The estimated speaking time assumes 140 words per minute; a personal timed rehearsal is still needed. The body is checked both excluding and including references, to avoid relying on an ambiguous count convention.

## Dependencies and portability

The document workflow was exercised with the existing Python 3.14 environment. `requirements-docs.txt` pins the document/figure libraries actually used; `alpha-lab/requirements.txt` preserves the experiment dependencies unchanged. `requirements.txt` references both. On an independently authorised clean machine, an assessor can create an environment and install these pinned dependencies before running the command above. No installation was performed during this finalisation.

The builders use the active Python environment and repository-local `.build-cache/` paths. They no longer require the absolute path or `.venv` location from Anas's Mac. A second build is checked in an isolated directory with the same installed environment; that is a portability check, not proof of a clean installation on another machine.

## Research inputs now supplied

The earlier cloud transfer deliberately contained only documentary inputs. This final local package additionally supplies:

- the complete tracked `alpha-lab/` source, tests, templates, bank and immutable trial registry;
- all locked cards and executed reports, including historical failures and unrun identifiers;
- both original frozen snapshot folders named in `alpha-lab/data/manifest.json`, copied as opaque files and verified against their original hashes;
- the original MIT licence and copyright attribution to Sami Andaloussi;
- `RESEARCH-INPUTS.sha256.json`, identifying the frozen inputs and both provenance commits.

The snapshots are archived inputs, not a fresh download. They are never parsed by the default reconstruction command; only their byte hashes are checked. No new holdout statistic is computed. The local package has not been uploaded or published automatically. The software licence is preserved and does not purport to define third-party data-use rights.

## Reproduction scope — distinguish two claims

**Verified here:** reconstructing the submitted tables, figures, Word and slides from the archived published outputs, and checking their provenance against the frozen source records. The full code and frozen inputs are supplied for inspection.

**Not performed here:** an independent re-estimation of all forecasts or a fresh run of the financial experiments. The original runner locks completed cards and opens each holdout once. The missing historical reference commit `9a00fbb` also still prevents the official paired comparison. Do not delete the registry, alter lock checks, rewrite Git history or claim that those limitations have been repaired.

`capstone/diagnostics/diagnostics.py` and the original lab remain research source, not part of the default build. Running them would be a new execution requiring separate authorisation. No script for re-downloading revised Yahoo prices is substituted for the frozen data vintage.

## Mapping reported evidence to code

| Report item | Source / reconstruction |
|---|---|
| Table 1 — validation criteria | Existing lab battery and RUNBOOK; text in manuscript |
| Table 2 — strategy outcomes | Saved notebook cells 12, 14, 22 and 24; `build_capstone.py` |
| Table 3 — costs, stability, DSR | Saved cells 12, 16, 18 and 20; `extract_costs.py` |
| Table 4 — forecast evaluation | Frozen `forecast-metrics.csv` and `summary.json`; no metric re-estimation |
| Figures 1, 5 and 6 | Saved notebook outputs; `build_capstone.py` |
| Figures 2, 3 and 4 | Saved diagnostic CSVs; `render_saved_figures.py` |
| Short defence | `build_defence.py` |
| Backup defence and importance chart | `build_presentation.py` |
| Word export | `export_docx.py` |

The coefficient/importance plots use the published, rounded CSV display records. The reported forecast accuracy statistics remain the original pre-rounding calculations; they are not recalculated from the rounded observations. Logistic return R² remains n/a.

## Attribution and individual accountability

Alpha Factory is pre-existing work co-founded with Sami Andaloussi and used as the evaluation tool. Anas's graded contribution is the ML layer, diagnostics, follow-up hypotheses, experiments and analysis. The manuscript retains the Claude/OpenAI Codex disclosure. Original research inputs are unchanged; final changes concern interpretation, packaging and document reconstruction. Anas remains responsible for understanding and defending the submission.
