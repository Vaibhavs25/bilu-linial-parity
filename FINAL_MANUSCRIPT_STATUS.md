# Final manuscript status — 19 September 2026

The final cumulative manuscript is:

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

Final local artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `7975fff4e4a6b7c1f8aba2528bfab1b6ffa374bd5fbc8f6f9dc30dfd49fe5ca8`
- PDF: `99fb331b5c2d863a59d205e3a82ed3827f9a44352cd237c46697be3cec0d1108`
- Final ZIP: `608e157ceb8625c7f5686e215becf395cd57c3c9d1d2a9db9da8466e72ada461`

## Final referee-audit changes completed

1. Proposition 16 now treats pure-cycle supports explicitly: on a cycle the two non-backtracking orientations are forced once the starting directed edge is fixed, so a stale segment has at most (2s) possibilities. This is absorbed by the displayed polynomial factor and does not invoke the reachability lemma.
2. Propositions 21–23 retain (k=lceil(log n)^2ceil) and (ell=2k). The rank estimate is checked uniformly for every (1le jleell), and the required (R_0ge C_{m rank}log(eell)/(2	heta)) is explicitly implied by the preceding radius scale after one enlargement of the absolute constant.
3. Proposition 13 cites the equality case of Wielandt's theorem via Horn–Johnson, *Matrix Analysis*, 2nd ed., Thm. 8.3.11.
4. The holonomy-to-diagonal-unitary step is isolated as a short lemma and proved directly.
5. The constrained-family minimum is explicitly separated from the unrestricted global minimum; the period-8 global-optimality assertion remains a conjecture.
6. The random-signing statement is explicitly empirical (“in our sampled instances”); no concentration theorem is claimed.
7. The abstract now describes Proposition 7 as a closed-walk identity and states the non-backtracking conversion separately through the linearization.
8. The arXiv date on reference [16] remains July 16, 2026.
9. The experimental repository code removes the misleading MCMC uniformity wording; the corrected campaign protocol uses an exactly rank-matched random-affine control and records the retained constraint rank. That corrected campaign was not rerun for this snapshot.

## Final build verification

- 22 pages, letter size.
- pdfTeX 1.40.26.
- Three-pass compilation with `-halt-on-error`.
- No LaTeX errors or warnings on the final pass.
- 38 unique labels; no duplicate labels; all source references resolve.
- PDF metadata populated.
- Full 22-page rendering checked; no visible clipping, overlap, broken glyphs, or malformed pages.

## Reproducibility freeze

The repository branch `final-2026-09-19` is the frozen code/data audit snapshot. It contains the corrected experimental code and preserved data artifacts. The exact generated PDF and source are supplied separately in the release package and identified by the hashes above. The repository does not claim that the historical campaign CSV was produced by the corrected campaign protocol.
