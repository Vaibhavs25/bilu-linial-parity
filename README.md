# Parity families for signed spectra — final audit bundle

This repository contains the verification suite, executed drivers, CI gate, regenerated data, and the July 2026 standalone manuscripts as provenance.

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and periodic circulant counterexamples**

The final cumulative local manuscript was rebuilt on 19 September 2026 after the referee audit.

Local final artifact hashes:
- LaTeX SHA-256: `6a27d4834c7ba08aed7bd4fe5549b30bd86c00a94005966790bafba0d6a05cc6`
- PDF SHA-256: `413de50fec0668424f4a89bbb6a4bfdb65e7419d9b41b2df35f04d4bcb767ce4`

The final manuscript is 21 pages. The local build uses pdfTeX 1.40.26 and completed in three passes with no LaTeX warnings. It has 37 labels and all internal references resolve.

The final necessary referee fixes are recorded in `FINAL_MANUSCRIPT_STATUS.md`.

The exact final PDF and LaTeX files are currently in the ChatGPT working environment; the older repository manuscript files remain as provenance until those final artifacts are uploaded there.

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

The July 2026 audit/changelog files and standalone manuscripts remain in the repository as provenance. The September 2026 integrated revision is documented separately in `FINAL_MANUSCRIPT_STATUS.md`.
