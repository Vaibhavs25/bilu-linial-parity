# Parity families for signed spectra — final audit bundle

This repository contains the verification suite, executed drivers, CI gate, regenerated data, and the July 2026 standalone manuscripts as provenance.

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

The final cumulative local manuscript was rebuilt on 19 September 2026 after the referee audit.

Local final artifact hashes:
- LaTeX SHA-256: `c9d3856d1134ad6b0e95cc8f0a076c72d2d0a8a14e8aa7266d9d5a138810109b`
- PDF SHA-256: `3f7ab24cbb778b62e4d821ec107f6f0654494b2f23a3c852fa3f04164948a0d4`

The final manuscript is 20 pages. The local build uses pdfTeX 1.40.26 and completed in three passes with no LaTeX warnings. It has 37 labels and all internal references resolve.

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


## Final snapshot

Frozen repository branch: `final-2026-09-19`, based at commit `4ccb2fd508df1a70f76ef40615bfb57ade92b903`. The exact local integrated PDF/source are identified by the SHA-256 hashes above; the final binary PDF is supplied with the submission package.
