# Official release manifest — September 2026

Canonical branch: `main`

## Release artifacts

- `submission/final_combined_paper_final.tex`
  - SHA-256: `7640da6da5839d06a8f8db509005425f06285ce60bfc2defd7bc8311c1b302d7`
- `Parity_families_signed_spectra_FINAL_OFFICIAL.pdf`
  - SHA-256: `4855ce5b45dc9b46fb0741db5f556dff7e248c68de41471cad853a4400438795`
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
