# Official release snapshot

This directory contains the canonical submission source and the files needed to reproduce the theorem-specific symbolic check.

## Canonical manuscript

`final_combined_paper_final.tex`

This is the final 20-page audited manuscript source on the `main` branch.

## Verification

Run:

```bash
python3 submission/verify_theorem26.py
```

The script recomputes the $8\times8$ Bloch-block determinant symbolically and checks the factorization at $s=2$ using exact SymPy arithmetic.

The pinned repository script is also retained at the repository root as `verify_theorem26.py`.

## PDF artifact

The corresponding official PDF is:

`Parity_families_signed_spectra_FINAL_OFFICIAL.pdf`

SHA-256:

`4855ce5b45dc9b46fb0741db5f556dff7e248c68de41471cad853a4400438795`

The PDF is recorded by hash but is not committed through this connector workflow because the available GitHub file-write action accepts UTF-8 text rather than arbitrary binary files.

## Scientific status

The release distinguishes proved statements, conditioning consequences, exact finite calculations, conjectures, and exploratory computations. In particular, the period-8 global-minimality statement remains conjectural.
