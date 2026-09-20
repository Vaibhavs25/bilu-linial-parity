# Official release manifest — September 2026

Canonical branch: `main`
Frozen release branch: `final-2026-09-20`

## Release artifacts

- `submission/final_combined_paper_final.tex`
  - SHA-256: `1f7fc908f8eb6569934333dea538192fb7f02fd9ecffca016156723932cd49bc`
- `submission/final_combined_paper_final.pdf`
  - SHA-256: `c4980d0d7445d562ee70c49c598c949de873a190f5ca7ada5045b444faf6bd8c`
  - 20 pages
  - external binary release artifact for this connector workflow
- `submission/verify_theorem26.py`
  - exact symbolic check of the $8\times8$ determinant identity and the $s=2$ factorization

## Verification commit

The pinned theorem-specific verification script is available at commit:

`b37002b020edd5d26065a0ee6ee7cff85cf7814c`

File:

`verify_theorem26.py`

## Release rule

The source under `submission/final_combined_paper_final.tex` is the canonical manuscript source. The recorded PDF hash must match the PDF produced from that source by the documented three-pass LaTeX build.

No new computational campaign results are claimed for this release.
