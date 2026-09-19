# Parity families for signed spectra — final audit snapshot

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

The September 19, 2026 integrated manuscript is frozen with the audited proof and presentation revisions.

Exact local submission artifacts:
- final_combined_paper_final.tex
- final_combined_paper_final.pdf

SHA-256:
- Source: 7bf1fbebdb42cc66ef4016d36572191d1b8aec062cec55f93c128f1ed84b37f3
- PDF: b2eeffb1ddeaa5337b117ff74064c4863d76871439b53336f4e63f14f627f3c7

The manuscript is 22 pages, US Letter. The local build used pdfTeX 1.40.26, three passes with -halt-on-error, and the final pass has no warnings or undefined references. The source contains 38 unique labels and all cross-references resolve.

The exact audited source is also committed at:
submission/final_combined_paper_final.tex

The exact binary PDF cannot be attached through the available GitHub connector; it is supplied in the release package and pinned by the PDF hash above.

## Verification

- verify_all.py — 18/18 PASS.
- ci.sh — verification/drivers gate.
- campaign.py — corrected rank-matched affine control and MCMC wording.
- variance_onset_v2.csv — corrected variance artifact.
- variance_onset_v1.csv and campaign.csv are retained as provenance.

The corrected campaign protocol has not been rerun for this final manuscript snapshot, so no new campaign results are claimed.

## Final freeze

Branch: final-2026-09-19

The branch freeze commit contains the audited repository code/data, final status record, exact source, and SHA-256 manifest. The PDF remains an external-but-hashed submission artifact because binary release-asset upload is not exposed by the connector.
