# Final manuscript status — 19 September 2026

The final cumulative manuscript is:

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

Final local artifacts:
- `final_combined_paper_final.tex`
- `final_combined_paper_final.pdf`

SHA-256:
- Source: `7975fff4e4a6b7c1f8aba2528bfab1b6ffa374bd5fbc8f6f9dc30dfd49fe5ca8`
- PDF: `99fb331b5c2d863a59d205e3a82ed3827f9a44352cd237c46697be3cec0d1108`
- Final package: `8fe8f1b1c5aa07196b5ee6eccfed122bd91d8677071d6528d870b0865c08c993`

## Final referee-audit changes completed

1. Proposition 16 explicitly handles pure-cycle supports; the pure-cycle case is bounded directly and does not invoke the reachability lemma.
2. Propositions 21–23 retain `k=ceil((log n)^2)` and `ell=2k`; the rank estimate is checked uniformly for every `1 <= j <= ell`, with the constant requirement made explicit.
3. Proposition 13 cites the equality case of Wielandt's theorem through Horn–Johnson, *Matrix Analysis*, 2nd ed., Thm. 8.3.11.
4. Proposition 25 isolates and proves the holonomy-to-diagonal-unitary gauge lemma.
5. The constrained-family minimum is distinguished explicitly from the unrestricted minimum; period-8 global optimality remains conjectural.
6. The random-signing statement is empirical and explicitly tied to the sampled instances.
7. The abstract distinguishes Proposition 7's closed-walk identity from the later non-backtracking linearization.
8. Reference [16]'s July 16, 2026 date is retained.
9. The corrected repository campaign code uses an exact-rank affine control and makes no uniform-MCMC claim; it has not been rerun for this release.

## Final build verification

- 22 pages, letter size.
- pdfTeX 1.40.26.
- Three-pass compilation with `-halt-on-error`.
- No LaTeX errors or warnings on the final pass.
- 38 unique labels; no duplicate labels; all source references resolve.
- PDF metadata populated.
- Full rendered-page inspection completed with no visible clipping, overlap, broken glyphs, or malformed pages.

## Reproducibility freeze

The branch `final-2026-09-19` freezes the corrected source, code, data, status, and manifest in one commit. The generated PDF is the external binary artifact identified by its SHA-256 above.
