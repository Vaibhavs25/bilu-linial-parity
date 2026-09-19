# Parity families for signed spectra — final audit snapshot

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

The September 19, 2026 integrated manuscript is frozen with the audited proof and presentation revisions.

Exact local submission artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `7975fff4e4a6b7c1f8aba2528bfab1b6ffa374bd5fbc8f6f9dc30dfd49fe5ca8`
- PDF: `99fb331b5c2d863a59d205e3a82ed3827f9a44352cd237c46697be3cec0d1108`

The audited source is committed at `submission/final_combined_paper_final.tex`. The generated PDF is supplied as the external binary submission artifact because the available GitHub connector does not expose binary release-asset upload.

## Verification

- `verify_all.py` — 18/18 PASS.
- `ci.sh` — verification/drivers gate.
- `campaign.py` — corrected exact-rank affine control and non-uniform MCMC wording.
- `variance_onset_v2.csv` — corrected variance artifact.
- `variance_onset_v1.csv` and `campaign.csv` are retained as provenance.

The corrected campaign protocol has not been rerun for this final manuscript snapshot, so no new campaign results are claimed.

## Final freeze

Branch: `final-2026-09-19`

The freeze commit contains the audited source, corrected code, preserved data, release status, and SHA-256 manifest. The PDF remains an external-but-hashed submission artifact.
