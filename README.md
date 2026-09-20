# Parity families and signed spectra

## Official release

**Manuscript:** *Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models*  
**Author:** Vaibhav Suvagiya  
**Institution:** Sardar Vallabhbhai National Institute of Technology, Surat  
**Release status:** Official audited manuscript snapshot — September 2026

The canonical manuscript source is:

- `submission/final_combined_paper_final.tex`

The official compiled PDF corresponding to this source is the 20-page artifact:

- `Parity_families_signed_spectra_FINAL_OFFICIAL.pdf` — distributed as an external binary artifact in this release workflow.

### SHA-256

- Source: `7640da6da5839d06a8f8db509005425f06285ce60bfc2defd7bc8311c1b302d7`
- PDF: `4855ce5b45dc9b46fb0741db5f556dff7e248c68de41471cad853a4400438795`

The PDF hash is recorded even though the available GitHub connector cannot upload binary release assets. When the PDF is manually attached to GitHub, verify it against the recorded hash.

## Reproducibility

Exact symbolic verification of the load-bearing $8\times8$ Bloch determinant and the $s=2$ factorization:

```bash
python3 submission/verify_theorem26.py
```

Full repository verification:

```bash
python3 verify_all.py
```

The manuscript was compiled with three consecutive `pdflatex -halt-on-error` passes. The final local build is 20 pages and has no final-pass LaTeX errors or warnings.

## Scientific scope

The current manuscript deliberately distinguishes:

- the affine $\mathbb F_2$ parity-family identities;
- the finite-scale bounded-rank counting result;
- the bicycle-free conditioning corollary;
- the exact signed-circulant analysis;
- exploratory computations and exact symbolic checks.

The bicycle-free result is presented as a conditioning consequence of the known random-signing theorem, not as a new concentration theorem. The matching lower bound for the period-8 global-optimality conjecture remains open.

## Repository layout

- `submission/` — canonical manuscript source, release documentation, checksum manifest, and theorem-specific verification script.
- `verify_all.py` — repository-wide verification driver.
- `verify_theorem26.py` — theorem-specific exact symbolic verification.
- `atlas.csv`, `campaign.csv`, `variance_onset_v1.csv`, `variance_onset_v2.csv` — archived computational data.
- `campaign.py`, `variance_onset.py`, `trace_rates.py`, `signed_spectra.py`, `prism_L.py`, `gadgets.py`, and related drivers — reproducibility and exploratory computations.

The `main` branch is the canonical public branch. Earlier freeze branches such as `final-2026-09-19` are retained as historical snapshots.
