# Parity families for the Bilu–Linial conjecture — bundle v3 (post re-audit)

Two companion manuscripts, an aux-verified verification suite, three
executed drivers, a CI gate, and regenerated data. Incorporates two rounds
of external adversarial audit (v1 and v2, July 2026).

## Manuscripts
| file | what |
|---|---|
| `paper_a.tex` / `paper_a.pdf` | *Parity families and a kernel-averaged L-function for near-Ramanujan signings* (14 pp). |
| `combined_note_archive.tex` | Original research note (provenance; numbering differs). |

## Verification and CI
- `verify_all.py` — **18/18 PASS**; every check string names the compiled
  theorem number. The trapping check now tests the d−2 remainder after
  removing the trivial classes (rate 2.13 in [1.9, 2.7]); q_G checks are
  exact (integer charpolys + Sturm).
- `ci.sh` — runs the suite **and all three drivers**, fails on any [FAIL]
  or traceback. All components executed green at packaging time.

## Drivers (all executed; outputs back the quoted §7 claims)
- `run_qg.py` — exhaustive q_G table (all connected regular graphs ≤ 7
  vertices + Petersen/Q3/K33), **Sturm-exact verdicts**: real-rooted iff
  odd cycle or K4 — matching Remark 6 line for line.
- `run_plan2.py` — strategy comparison on the **even-cycle (parity)
  system** with **fair LS seeding** (best-of-60 both arms). C30/C60: quad
  system fully satisfiable (30/30, 60/60), family at {2.790, 2.828} =
  {ρ₋, 2√2}, beating fair LS (2.790 vs 2.856); triangle-forcing 3.945 vs
  random 3.44; K12 greedy 90/1485 with LS ≈ 4.56 both arms.
- `run_atlas.py` — regenerates `atlas.csv`; girth now exact (`nx.girth`),
  so C7 reports 7, not inf.

## Data
- `variance_onset_v2.csv` — **the current artifact** (62 rows, regenerated
  with zero-tail excluded from all dispersion statistics, distinct-tail
  sampling for small kernels, NaN dispersion at kdim=0, sparse
  eigensolver ≥ 256). Honest tower dispersion ratios: **0.79–1.21**
  across n ∈ {256, 512, 1024}, all families and seeds — the range quoted
  in Paper A §7 is read directly off this file.
- `variance_onset_v1.csv` — the pre-fix run, kept as provenance (its
  `tail_std` includes the 12–34σ zero-tail outlier).

## Restored drivers (every quoted Sec. 7-8 figure now has an artifact)
- `trace_rates.py` — R_F/R_all/R_bal vs the tree profile at k <= 40:
  towerK4-128 R_F(40)=2.769, planted-128 3.327, C60(1,2) 2.872 with R_all
  stalling at 3.68; plus the constant-density three-average block
  (Efam/nt 0.080-0.107, excess 0.12-0.13 at n=256/512), reproducing the
  original session run bit-for-bit. Executing it exposed and fixed a
  latent wrong assertion (the tree profile CAN dip below the floor at
  finite k, d=4 n=128 k=40).
- `gadgets.py` — Theta(2,2,lam) table (1.348/1.268/1.222/1.190/1.150),
  quad-ring (rho=1.2425, rank 5), tree-burst vs 2^(D/(D+lam)), unicyclic
  winding bound with sharpness. All Remark-18 numbers asserted.
- `prism_L.py` — exact Prop-10 verification: 2514 primes to length 14,
  1598 parity-confined, coefficient form matches for all k <= 14, log-det
  identity to 8 digits at u=0.2.

## Experimental campaign (`campaign.py`, `campaign.csv`)
Matched-budget baselines + parity ablation + conditioned-uniform control:
20 instances/set, EQUAL EVALUATION BUDGET (2000 rho-evals per strategy
per instance), crc32-derived deterministic seeds -- two cold runs are
byte-identical apart from the diagnostic wall column. Paired 95% t-CIs,
deltas vs family (positive = family wins): uniform random
+0.094/+0.091/+0.296 (planted/conditioned/circulant, all SIG);
matched-codimension RANDOM constraints +0.098/+0.094/+0.633 (all SIG:
the effect is parity, not conditioning); simulated annealing
+0.053/+0.051 (SIG) on the generic sets; tabu search statistically
indistinguishable there (-0.003/+0.000, ns) -- the family matches a
tuned search with zero search; the conditioned-uniform control
reproduces the planted numbers (generator bias excluded); circulants:
family dominates every arm (+0.17 to +0.63). Note: the earlier
wall-clock budgeting favoured the heuristics via the family's per-draw
solve overhead; the evaluation budget removes that bias. `campaign.py
--quick` (used by ci.sh) writes to campaign_quick.csv and never touches
the artifact. Checkpointed; rerun resumes.

## v2 re-audit changelog (all items closed)
- **N1** qG_polynomial NameError → guard moved inside the loop on the raw
  np.poly output; driver runs. Bonus: `qG_verdict` was misclassifying C7
  via np.roots near-double roots — now Sturm-exact.
- **N2** wrong system → `unbalanced_signing_family(even_only=True)` default;
  the triangle experiment passes `even_only=False` explicitly; run_plan2
  rerun and §7 cross-checked against its actual output.
- **N3** zero tail reintroduced by `rng.choice(1<<kdim, …)` → sampled from
  `arange(1, 1<<kdim)`.
- **N4** kdim=0 emitted outlier as statistics → NaN dispersion columns.
- **N5** README/zip mismatch → archive restored; packaging now asserts
  every listed file exists.
- **N6** rigged LS comparison → both arms seed from best-of-60; §7's
  local-search sentence rewritten with the fair numbers.
- **N7** "sit at the floor" → "within 0.2 of the floor, none separates."
- Residuals: girth actually fixed (not documented-around); Outlook
  "reduces" → "isolates"; Lemma 15 gloss cut to one sentence; ratio range
  re-pinned to the regenerated artifact (0.79–1.21).

## Still open before submission
Author fields; supervisor read of Lemmas 15/19/20 and Props 16/21-24;
optional: growing-d trapping family. Paper B: Remark 4 is now covered by
PROOF (the flux identity chi_S = chi_H + alternate-triangle sum forces
alpha = -1; rho_-(8) = sqrt(4+sqrt2) = 2.326846...), with the lattice-max
clause extended to every even n >= 8.
