# Final manuscript status — 19 September 2026

The final cumulative manuscript is:

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

Final local artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `13d6bff3f167e4b7878876f739e5aa52f9f4aa285ee2ba3617c1016ce8492ace`
- PDF: `6b72cdec9ad480ee836e0f5aef90d16ea820ecb5e367980891c436d50902b7c3`

## Final cleanup completed

1. Proposition 16: removed the stochastic-search observation from the deterministic Lemma 20 proof and retained an explicit pure-cycle treatment in Proposition 16.
2. Propositions 21–23: retained (k=lceil(log n)^2ceil), (ell=2k), and the displayed (R_0,	heta) constant check; the estimate is uniform in (1le jleell).
3. Proposition 13: Wielandt equality case is cited to Horn–Johnson, *Matrix Analysis*, 2nd ed., Chapter 8.
4. Proposition 25: equal holonomy implies diagonal-unitary conjugacy via an explicit lemma and proof.
5. Abstract and Remark 31: wording distinguishes closed-walk identities from later non-backtracking linearization, separates constrained-family minima from the unrestricted minimum, and labels random-signing observations as empirical.
6. Remark 18: numerical theta/tree-burst measurements are explicitly introduced as computational observations.
7. Remaining small circulant cases (n=26,28,30): the statement is now explicitly framed as a heuristic-search observation tied to the accompanying repository, not as an exhaustive computation or certified optimality result.
8. Reference [16]: the July 16, 2026 date is retained.

## Final build verification

- 22 pages, letter size.
- pdfTeX 1.40.26.
- Three-pass compilation with `-halt-on-error`.
- Final pass: no LaTeX errors or warnings.
- 38 unique labels; no duplicate labels; all source references resolve.
- PDF metadata populated.
- Full 22-page rendering checked; no visible clipping, overlap, broken glyphs, or malformed pages.
- PDF preflight: openable, unencrypted, 22 letter-size pages.

## Reproducibility freeze

Branch `final-2026-09-19` freezes the audited source, corrected code, preserved data, status record, and SHA-256 manifest. The generated PDF is the external binary release artifact identified by the PDF hash above. The corrected campaign protocol has not been rerun for this release; `campaign.csv` remains provenance.
