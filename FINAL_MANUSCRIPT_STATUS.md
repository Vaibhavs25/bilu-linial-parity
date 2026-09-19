# Final manuscript status — 19 September 2026

The final cumulative manuscript is:

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

Final local artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `c9d3856d1134ad6b0e95cc8f0a076c72d2d0a8a14e8aa7266d9d5a138810109b`
- PDF: `3f7ab24cbb778b62e4d821ec107f6f0654494b2f23a3c852fa3f04164948a0d4`

## Necessary referee fixes completed

1. Proposition 16: the stale-segment closure count uses a legitimate sum over all possible closure lengths (t,ldots,t+4s); the fixed-(delta) asymptotic claim was replaced by the correct limsup statement, with matching Kesten rate only when (delta	o0) (and fixed (r_0)).
2. Proposition 22: the confined-walk bound is stated uniformly for every (1le jleell), with one common prefactor.
3. Lemmas 15, 19, and 20: the non-backtracking reachability, window encoding, and bicycle-free rank arguments were made explicit enough to support their use in the subsequent counting chain.
4. Proposition 21: the proof uses (k=lceil(log n)^2ceil) and the proved bicycle-free scale (Rge C(loglog n)^2/delta), with the parameter bookkeeping written explicitly.
5. The averaged Ihara identity fixes the logarithm branch by (logdet(I-uB_sigma)=0) at (u=0) and starts the Euler-product argument in (|u|<(d-1)^{-1}); the larger Ramanujan-disk statement is stated only for the untwisted determinant term.
6. Finite-moment language has been corrected to the finite tree-moment benchmark; the phrase “Alon--Boppana-forced profile” is absent.
7. The unsupported probabilistic random-(2)-lift claim has been removed from the theorem narrative.
8. The experimental section no longer makes a causal “parity rather than conditioning” claim. The repository campaign ablation now matches the exact rank/codimension of the retained parity subsystem and records that rank. Planted inconsistent systems are named retained/greedy-consistent parity subsystems; the graph control is named MCMC-conditioned rather than uniformly conditioned; no claim of identical (C_4) distributions is made.
9. The MOP reference uses the published SIAM J. Comput. version; current Huang, Lin--Zhou, and Xu preprints are cited; the withdrawn Xu--Zhang preprint is not cited as a current result.
10. The period-(8) theorem uses a rational interval certificate for (r_*), and the theorem title identifies constrained-family global optimality.
11. PDF title/author/subject/keywords metadata are populated and hyperlinks are hidden for the final submission copy.

## Final local build check

- 20 pages, letter size.
- pdfTeX 1.40.26.
- Three-pass compilation with `-halt-on-error` completed successfully.
- No LaTeX errors or warnings in the final build log.
- 37 labels; no duplicate labels; all internal references resolve.
- No stale withdrawn-reference, “sub-Kesten”, or “Alon--Boppana-forced” wording remains.

## Reproducibility

The repository contains the verification suite, drivers, corrected `campaign.py`, and data artifacts. The corrected campaign commit is separate from the historical campaign data; the older campaign artifact is retained as provenance and is not used for causal attribution in the final paper.

The exact final PDF and source hashes above identify the submission files. An immutable archive/release (e.g. Zenodo DOI) should be created externally when the submission snapshot is deposited; the available GitHub connector does not expose release-asset upload for the generated local PDF.
