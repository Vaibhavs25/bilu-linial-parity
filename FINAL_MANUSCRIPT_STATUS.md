# Final manuscript status — 19 September 2026

## Final integrated manuscript

**Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models**

Final local submission artifacts:
- final_combined_paper_final.tex
- final_combined_paper_final.pdf

SHA-256:
- Source: 7bf1fbebdb42cc66ef4016d36572191d1b8aec062cec55f93c128f1ed84b37f3
- PDF: b2eeffb1ddeaa5337b117ff74064c4863d76871439b53336f4e63f14f627f3c7

## Final audit fixes completed

1. Proposition 16 now uses the correct q <= r fresh-run encoding and explicitly handles pure-cycle supports.
2. Proposition 21/23 retain k = ceil((log n)^2), with an explicit constant check reducing C_rank s log s / R_0 to theta (j + Lambda).
3. Proposition 13 cites the equality case of Wielandt's theorem through C. D. Meyer (2000).
4. Proposition 25 explicitly derives the diagonal-unitary conjugacy from equal cycle holonomies.
5. Remark 30 explicitly states the constrained-family minimum.
6. The random-signing observation is explicitly empirical sampling evidence, not a concentration theorem.
7. The abstract distinguishes closed-walk parity counts from the later non-backtracking linearization.
8. The September 2026 Bilu--Linial literature, related work, and the author's prior arXiv:2607.17343 are explicitly positioned.
9. The Huang arXiv:2609.17551 date remains July 16, 2026.
10. The period-8 circulant result remains a theorem; global optimality remains a conjecture.

## Final build and visual verification

- 22 pages, US Letter.
- pdfTeX 1.40.26.
- Three-pass compilation with -halt-on-error completed successfully.
- Final pass: no LaTeX warnings, undefined references, overfull boxes, or underfull boxes.
- 38 unique labels; no duplicates; all 84 ref/eqref/pageref targets resolve.
- PDF metadata populated.
- Full rendered-page inspection completed with no visible clipping, overlap, broken glyphs, or malformed pages.

## Reproducibility freeze

The final-2026-09-19 branch freezes the audited code/data snapshot together with the exact final source under submission/final_combined_paper_final.tex and the SHA-256 manifest in submission/SHA256SUMS.txt.

The exact 22-page PDF is supplied in the release package and is identified by the PDF SHA-256 above. The available GitHub connector does not expose binary release-asset upload, so the repository does not claim to contain the PDF binary.

The corrected campaign.py implements the rank-matched random-affine control and non-uniformity disclaimer for the MCMC control. That corrected campaign protocol has not been rerun for this manuscript snapshot.
