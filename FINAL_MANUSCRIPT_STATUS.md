# Final manuscript status — 19 September 2026

The final cumulative manuscript is:

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and periodic circulant counterexamples**

Local final artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `9d35d3a6e65debe90bfbe074d1d961a71a56e11460832e98fc957dd694b0cce7`
- PDF: `f9a8a743406870168b86a702e9fa286a70a6462b3bbaf8725a632b862494933a`

## Necessary audit fixes included

1. The non-backtracking reachability lemma now has an explicit oriented-line-graph formulation and a cited strong-connectivity statement.
2. The window-path lemma makes the tree/unicyclic decomposition and winding count explicit.
3. The bicycle-free rank lemma uses connectedness, an explicit short-cycle packing argument, and componentwise Moore-bound algebra.
4. The bicycle-free epsilon theorem uses the proved radius scale `R >= C (log log n)^2 / delta` and `k = ceil((log n)^2)`.
5. The adjacency transfer is presented through a standalone non-backtracking linearization statement; the dilute epsilon proof bounds cyclic non-backtracking traces directly.
6. The averaged Ihara identity fixes the logarithm branch by `log det(I-u B_sigma)=0` at `u=0` and begins in `|u| < 1/(d-1)`.
7. The finite-moment wording no longer makes a finite-`k` Alon--Boppana or “sub-Kesten” claim.
8. The unsupported random-2-lift high-probability assertion has been removed from the theorem narrative.
9. The current literature uses Huang (arXiv:2609.17551), Lin--Zhou (arXiv:2609.15715), and Xu (arXiv:2609.15591); the withdrawn Xu--Zhang preprint is not used as a current result.
10. Experimental confidence-interval language is explicitly descriptive, and the deterministic row-reduction solution is reported separately from the random affine-tail population for dispersion statistics.

## Final local build check

- 21 pages, letter size.
- pdfTeX 1.40.26.
- Three-pass LaTeX compilation completed with `-halt-on-error`.
- No LaTeX warnings in the final build log.
- 37 labels; all references resolve.
- No duplicate labels.
- No stale `xuzhang`, `sub-Kesten`, or `Alon-Boppana-forced` wording remains.

The GitHub repository currently contains the verification suite and this release-status record. The exact final source/PDF hashes above identify the local submission files; the older standalone manuscript files remain in the repository as provenance until those final artifacts are uploaded there.
