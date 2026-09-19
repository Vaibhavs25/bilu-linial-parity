# Final manuscript status — 19 September 2026

The final cumulative manuscript is:

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and periodic circulant counterexamples**

Local final artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `6a27d4834c7ba08aed7bd4fe5549b30bd86c00a94005966790bafba0d6a05cc6`
- PDF: `413de50fec0668424f4a89bbb6a4bfdb65e7419d9b41b2df35f04d4bcb767ce4`

## Necessary audit fixes included

1. The non-backtracking reachability lemma now has an explicit oriented-line-graph formulation and a cited strong-connectivity statement.
2. The window-path lemma makes the tree/unicyclic decomposition and winding count explicit.
3. The bicycle-free rank lemma uses connectedness, explicit short-cycle packing, and componentwise Moore-bound algebra.
4. The bicycle-free epsilon theorem uses the proved radius scale `R >= C (log log n)^2 / delta` and `k = ceil((log n)^2)`.
5. The adjacency transfer is presented through a standalone non-backtracking linearization statement; the dilute and bicycle-free proofs bound cyclic non-backtracking traces directly.
6. The averaged Ihara identity fixes the logarithm branch by `log det(I-u B_sigma)=0` at `u=0` and begins in `|u| < 1/(d-1)`.
7. Finite-moment wording no longer makes a finite-`k` Alon--Boppana or “sub-Kesten” claim.
8. The unsupported random-2-lift high-probability assertion has been removed from the theorem narrative.
9. Current 2026 literature uses Huang (arXiv:2609.17551), Lin--Zhou (arXiv:2609.15715), and Xu (arXiv:2609.15591); the withdrawn Xu--Zhang preprint is not used as a current result.
10. Experimental interval wording is descriptive; the deterministic row-reduction solution is reported separately from the random affine-tail population for dispersion statistics.

## Final local build check

- 21 pages, letter size.
- pdfTeX 1.40.26.
- Three-pass LaTeX compilation completed with `-halt-on-error`.
- No LaTeX warnings in the final build log.
- 37 labels; all references resolve.
- No duplicate labels.
- No stale `xuzhang`, `sub-Kesten`, or `Alon-Boppana-forced` wording remains.

The repository currently contains the verification suite and this release-status record. The exact hashes above identify the final local submission files; the older standalone manuscript files remain in the repository as provenance until those final artifacts are uploaded there.
