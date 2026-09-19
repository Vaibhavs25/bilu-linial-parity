# Parity families for signed spectra — final audit bundle

This repository contains the verification suite, executed drivers, CI gate, regenerated data, and the July 2026 standalone manuscripts as provenance.

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

The final cumulative local manuscript was rebuilt on 19 September 2026 after the referee audit.

Local final artifact hashes:
- LaTeX SHA-256: `3cbf59e50004f6c95c6786a916a8526ae212f2f675e0adc9f5bb3b182b4f2ccc`
- PDF SHA-256: `fa77875ba58f2bd86a8534ceb92121f2d36d07412aa85d77d075bb3d3410bade`

The final manuscript is 22 pages. The local build uses pdfTeX 1.40.26 and completed in three passes with `-halt-on-error`; the final build logs contain no LaTeX errors or warnings. It has 38 unique labels and all internal references resolve.

The final necessary referee fixes are recorded in `FINAL_MANUSCRIPT_STATUS.md`.

The exact final PDF and LaTeX files are currently in the ChatGPT working environment; older repository manuscript files remain as provenance until those final artifacts are uploaded there.

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
- `campaign.csv` — historical matched-evaluation-budget experiment/provenance artifact.

The corrected `campaign.py` implements the rank-matched random-affine control and writes `campaign_v2.csv`; that corrected campaign protocol has not been rerun for this final manuscript snapshot, so no new campaign results are claimed.

## Historical audit record

The July 2026 audit/changelog files and standalone manuscripts remain in the repository as provenance. The September 2026 integrated revision is documented separately in `FINAL_MANUSCRIPT_STATUS.md`.

## Final snapshot

The frozen `final-2026-09-19` branch is maintained as the repository audit snapshot. The exact local integrated PDF/source are identified by the SHA-256 hashes above; the final binary PDF is supplied with the submission package.
