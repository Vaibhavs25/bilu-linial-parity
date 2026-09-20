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

`submission/final_combined_paper_final.pdf`

SHA-256:

`c4980d0d7445d562ee70c49c598c949de873a190f5ca7ada5045b444faf6bd8c`

The PDF is recorded by hash but is not committed through this connector workflow because the available GitHub file-write action accepts UTF-8 text rather than arbitrary binary files.

## Scientific status

The release distinguishes proved statements, conditioning consequences, exact finite calculations, conjectures, and exploratory computations. In particular, the period-8 global-minimality statement remains conjectural.
