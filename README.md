# Parity families for signed spectra — final audit bundle

Two companion manuscripts, an aux-verified verification suite, executed drivers, a CI gate, and regenerated data. This repository also preserves the July 2026 standalone manuscripts as provenance.

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and periodic circulant counterexamples**

The final cumulative local manuscript was rebuilt on 19 September 2026 after the referee audit.

Local final artifact hashes:
- LaTeX SHA-256: `9d35d3a6e65debe90bfbe074d1d961a71a56e11460832e98fc957dd694b0cce7`
- PDF SHA-256: `f9a8a743406870168b86a702e9fa286a70a6462b3bbaf8725a632b862494933a`

The final manuscript is 21 pages. The local build uses pdfTeX 1.40.26 and completed in three passes with no LaTeX warnings. It has 37 labels and all internal references resolve.

The necessary referee fixes included:
- strengthened non-backtracking reachability and window-counting arguments;
- an explicit connected short-cycle packing proof for the bicycle-free rank lemma;
- corrected bicycle-free theorem scale (R\ge C(\log\log n)^2/\delta) and (k=\Theta((\log n)^2));
- a standalone non-backtracking linearization statement with the dilute theorem bounded directly by cyclic non-backtracking counts;
- the analytic branch convention for the averaged Ihara logarithm;
- removal of finite-(k) “sub-Kesten” and “Alon--Boppana-forced” wording;
- removal of the unsupported random-2-lift high-probability theorem claim;
- current 2026 literature corrections;
- descriptive wording for the reported experimental confidence intervals and separation of the deterministic particular solution from the random affine-tail dispersion population.

The exact final PDF and LaTeX files are currently in the ChatGPT working environment; the older repository manuscript files have not been silently relabeled as the final integrated manuscript.

## Verification and CI

- `verify_all.py` — **18/18 PASS**.
- `ci.sh` — runs the verification suite and all drivers and fails on any reported failure or traceback.

## Drivers

- `run_qg.py` — exhaustive q_G checks with Sturm-exact verdicts.
- `run_plan2.py` — parity-family and fair local-search comparison.
- `run_atlas.py` — regenerated exact-girth atlas.
- `trace_rates.py`, `gadgets.py`, `prism_L.py` — reproducible checks supporting the reported Section 7/8 numerical claims.

## Data

- `variance_onset_v2.csv` — current corrected variance artifact.
- `variance_onset_v1.csv` — preserved provenance artifact from the pre-fix run.
- `campaign.csv` — matched-evaluation-budget experiment.

## Historical audit record

The earlier July 2026 audit/changelog files remain in the repository for provenance. The present README describes the later September 2026 integrated revision; it supersedes the earlier “still open before submission” wording in the historical notes.
