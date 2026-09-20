# Final manuscript status — September 2026

## Canonical release

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

The canonical public manuscript is the **20-page audited revision** represented by:

- `submission/final_combined_paper_final.tex`

Official local PDF:

- `Parity_families_signed_spectra_FINAL_OFFICIAL.pdf`

SHA-256:
- Source: `7640da6da5839d06a8f8db509005425f06285ce60bfc2defd7bc8311c1b302d7`
- PDF: `4855ce5b45dc9b46fb0741db5f556dff7e248c68de41471cad853a4400438795`

## Final substantive scope

The final revision incorporates the referee-driven changes that matter to the mathematical framing:

1. The bounded-rank counting proposition is explicitly finite-scale and is not presented as an asymptotic fixed-rank regime at the $(\log n)^2$ scale.
2. The bicycle-free existence statement is an explicit conditioning consequence of the Mohanty--O'Donnell--Paredes random-signing theorem.
3. The fixed-graph totally-even slice is distinguished from the doubling lower benchmark.
4. The non-backtracking spectral calculation for dense trapping uses the sharp Ihara--Bass input.
5. The holonomy argument explicitly addresses the integer cycle lattice.
6. The constrained quadrilateral-family minimum is separated from the unrestricted signing minimum.
7. Period-8 global optimality remains a conjecture; the gauge-fixed periodic scans are explicitly supporting evidence only.
8. The $8\times8$ determinant and $s=2$ factorization in Theorem 26 are covered by an exact SymPy verification script pinned to a repository commit.
9. Computational observations are labeled as exact checks or exploratory evidence rather than replacements for proof.

## Build verification

- 20 pages, letter size.
- Three consecutive `pdflatex -halt-on-error` passes.
- No final-pass LaTeX errors or warnings.
- Rendered-page inspection completed.
- PDF comparison against the uploaded 20-page revision changes only page 17, where the pinned verification-script URL was added.

## Repository status

The `main` branch is the canonical public branch. The canonical manuscript source is committed under `submission/final_combined_paper_final.tex`.

The PDF remains an external binary artifact in this connector workflow; its SHA-256 is recorded above and in `submission/SHA256SUMS.txt`.
