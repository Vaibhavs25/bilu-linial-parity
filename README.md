# Parity families for signed spectra — final audit snapshot

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

The September 19, 2026 integrated manuscript is frozen with the final proof/presentation cleanup.

Exact local submission artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `13d6bff3f167e4b7878876f739e5aa52f9f4aa285ee2ba3617c1016ce8492ace`
- PDF: `6b72cdec9ad480ee836e0f5aef90d16ea820ecb5e367980891c436d50902b7c3`

The audited source is frozen at `submission/final_combined_paper_final.tex`. The generated PDF is supplied as the external binary submission artifact because the available GitHub connector does not expose binary release-asset upload.

## Verification

- `verify_all.py` — 18/18 PASS.
- `ci.sh` — verification/drivers gate.
- `campaign.py` — corrected exact-rank affine control and non-uniform MCMC wording.
- `variance_onset_v2.csv` — corrected variance artifact.
- `variance_onset_v1.csv` and `campaign.csv` are retained as provenance.

The corrected campaign protocol has not been rerun for this final manuscript snapshot, so no new campaign results are claimed.

## Final freeze

Branch: `final-2026-09-19`

The freeze commit contains the audited source, corrected code, preserved data, status record, and SHA-256 manifest. The PDF remains an external-but-hashed submission artifact.
