# Parity families and signed spectra

## Official release

**Manuscript:** *Parity families and signed spectra: kernel averaging, near-Ramanujan bounds, and exact circulant models*  
**Author:** Vaibhav Suvagiya  
**Institution:** Sardar Vallabhbhai National Institute of Technology, Surat  
**Release status:** Official audited manuscript snapshot — September 2026

The canonical manuscript source is:

- `submission/final_combined_paper_final.tex`

The official compiled PDF corresponding to this source is the **20-page** artifact:

- `Parity_families_signed_spectra_FINAL_OFFICIAL.pdf` — distributed as an external binary artifact in this release workflow.

### SHA-256

- Source: `1f7fc908f8eb6569934333dea538192fb7f02fd9ecffca016156723932cd49bc`
- PDF: `c4980d0d7445d562ee70c49c598c949de873a190f5ca7ada5045b444faf6bd8c`

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

The theorem-specific verification script is pinned to the repository commit:

```
b37002b020edd5d26065a0ee6ee7cff85cf7814c
```

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

The `main` branch is the canonical public branch. The exact current release is also frozen at `final-2026-09-20`; the earlier `final-2026-09-19` branch is retained as a historical snapshot.
