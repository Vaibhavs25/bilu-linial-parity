"""campaign.py -- the unified Section-7 experimental campaign (Paper A).

Three components, one harness, all strategies at an EQUAL SPECTRAL-EVALUATION
BUDGET per instance (N_EVAL spectral-radius evaluations; deterministic
and hardware-portable, unlike wall-clock), with >=20 instances per set:

  1. Exploratory matched-budget baselines: retained parity subsystem vs
     uniform random signings, simulated annealing, and tabu search.
  2. Corrected ablation: retained parity subsystem vs a uniformly random
     affine GF(2) system with EXACTLY THE SAME RANK (codimension) on each
     instance.
  3. MCMC-conditioned graph control: 4-regular instances constrained to a
     prescribed C4-count band by symmetric double-edge-swap MCMC. We call
     this an MCMC control; no uniformity or mixing guarantee is claimed.

The planted graphs may have inconsistent full short-even systems. On such
instances CycleSystem retains a consistent RREF subsystem; this arm is
therefore named a retained/greedy-consistent parity subsystem rather than
the full prescribed parity family.

Instance sets (20 each): planted4reg n=64; MCMC-conditioned n=64; circulants
C_n(1,2), n = 24,28,...,100. The C4 count is recorded per instance.

Checkpointed to campaign_v2.csv (one row per instance x strategy); rerun
resumes. `python3 campaign.py --quick` runs a small smoke configuration.
"""
import csv
import zlib
import os
import sys
import time
import numpy as np
import networkx as nx
from scipy import stats
from variance_onset import CycleSystem, planted_4cycles
from signed_spectra import signed_adjacency, edge_list

CSV = "campaign_v2.csv"
N_EVAL = 2000           # rho-evaluations per strategy per instance
                        # (~1.2 s at n=64 on the reference machine)
N_INST = 20
SEED0 = 1000

# ---------------------------------------------------------------- utilities

def rho(G, E, signs):
    return float(np.abs(np.linalg.eigvalsh(
        signed_adjacency(G.number_of_nodes(), E, signs))).max())

def count_c4(A):
    """#4-cycles of a 4-regular simple graph: (tr A^4 - 28 n)/8."""
    A2 = A @ A
    return int(round((float(np.sum(A2 * A2)) - 28 * A.shape[0]) / 8))

class AffineF2:
    """Affine system R x = b over F2 on k co-tree coordinates: particular
    solution + nullspace basis; .sample(rng) draws a uniform solution."""
    def __init__(self, R, b):
        R = R.astype(np.uint8).copy()
        b = b.astype(np.uint8).copy()
        k = R.shape[1]
        rr, piv = 0, []
        for c in range(k):
            p = next((i for i in range(rr, len(R)) if R[i, c]), None)
            if p is None:
                continue
            R[[rr, p]], b[[rr, p]] = R[[p, rr]], b[[p, rr]]
            for i in range(len(R)):
                if i != rr and R[i, c]:
                    R[i] ^= R[rr]
                    b[i] ^= b[rr]
            piv.append(c)
            rr += 1
        self.consistent = not any(b[rr:])
        self.k, self.piv = k, piv
        free = [c for c in range(k) if c not in piv]
        self.free = free
        x0 = np.zeros(k, np.uint8)
        for i, c in enumerate(piv):
            x0[c] = b[i]
        self.x0 = x0
        self.basis = []
        for f in free:
            v = np.zeros(k, np.uint8)
            v[f] = 1
            for i, c in enumerate(piv):
                v[c] = R[i, f]
            self.basis.append(v)

    def sample(self, rng):
        x = self.x0.copy()
        for v in self.basis:
            if rng.integers(0, 2):
                x ^= v
        return x

def cotree_signs(G, E, tree_mask, x):
    """Sign vector: +1 on tree edges, co-tree coordinate bits give -1."""
    s = np.ones(len(E))
    j = 0
    for i in range(len(E)):
        if not tree_mask[i]:
            if x[j]:
                s[i] = -1.0
            j += 1
    return s

def cotree_setup(G, E):
    T = nx.minimum_spanning_tree(G)
    tset = {tuple(sorted(e)) for e in T.edges()}
    tree_mask = np.array([e in tset for e in E])
    kdim = int((~tree_mask).sum())
    return tree_mask, kdim

def even_cycle_rows(G, E, tree_mask, L=4):
    """Even cycles <= L as rows over the co-tree coordinates, RHS 1."""
    eidx = {e: i for i, e in enumerate(E)}
    cot_pos = {}
    j = 0
    for i in range(len(E)):
        if not tree_mask[i]:
            cot_pos[i] = j
            j += 1
    # tree-path parity: for a tree edge, which fundamental coordinates flip it
    # -> easier: express each cycle over ALL edges, then reduce mod tree via
    # fundamental cycles. Build fundamental cycle matrix F[cotree j, edge i].
    Tg = nx.Graph([e for i, e in enumerate(E) if tree_mask[i]])
    Tg.add_nodes_from(G.nodes)
    rows = []
    for c in nx.simple_cycles(G, length_bound=L):
        if len(c) % 2:
            continue
        r_full = np.zeros(len(E), np.uint8)
        for a in range(len(c)):
            r_full[eidx[tuple(sorted((c[a], c[(a + 1) % len(c)])))]] ^= 1
        # cycle sign in co-tree coords = its co-tree incidence (tree edges
        # are +1 by gauge, so only co-tree entries matter)
        r = np.zeros(j, np.uint8)
        for i in range(len(E)):
            if not tree_mask[i] and r_full[i]:
                r[cot_pos[i]] = 1
        rows.append(r)
    return np.array(rows, np.uint8) if rows else np.zeros((0, j), np.uint8)

# --------------------------------------------------------- GF(2) rank helpers

def gf2_rank(A):
    """Rank of a binary matrix over GF(2)."""
    A = np.asarray(A, dtype=np.uint8).copy()
    r = 0
    for col in range(A.shape[1]):
        p = next((i for i in range(r, A.shape[0]) if A[i, col]), None)
        if p is None:
            continue
        A[[r, p]] = A[[p, r]]
        for i in range(r + 1, A.shape[0]):
            if A[i, col]:
                A[i] ^= A[r]
        r += 1
        if r == A.shape[0]:
            break
    return r

def random_full_rank_matrix(r, c, rng):
    """Draw an r-by-c random binary matrix of exact row rank r."""
    if r == 0:
        return np.zeros((0, c), dtype=np.uint8)
    while True:
        R = rng.integers(0, 2, (r, c), dtype=np.uint8)
        if gf2_rank(R) == r:
            return R

# ---------------------------------------------------------------- strategies

def strat_family(G, E, T, rng, L=4):
    """Sample the retained affine parity subsystem. If the full short-even
    system is inconsistent, this is the consistent RREF subsystem."""
    cs = CycleSystem(G, L)
    kd = len(cs.free)
    best = np.inf
    for _ in range(T):
        s = cs.solution(rng.integers(0, 2, kd, dtype=np.uint8))
        best = min(best, rho(G, E, s))
    return best, T

def strat_randcon(G, E, T, rng, L=4):
    """Ablation arm with exactly the same constraint rank as the parity arm."""
    cs = CycleSystem(G, L)
    tree_mask, kdim = cotree_setup(G, E)
    target_rank = cs.rank
    R = random_full_rank_matrix(target_rank, kdim, rng)
    b = np.ones(target_rank, np.uint8)
    sys_ = AffineF2(R, b)
    if sys_.rank != target_rank or not sys_.consistent:
        raise RuntimeError("failed to construct exact-rank affine control")
    best = np.inf
    for _ in range(T):
        s = cotree_signs(G, E, tree_mask, sys_.sample(rng))
        best = min(best, rho(G, E, s))
    return best, T
def strat_random(G, E, T, rng):
    best = np.inf
    for _ in range(T):
        best = min(best, rho(G, E, rng.choice([-1.0, 1.0], len(E))))
    return best, T

def strat_anneal(G, E, T, rng):
    m = len(E)
    best, n_eval = np.inf, 0
    while n_eval < T:
        s = rng.choice([-1.0, 1.0], m)
        cur = rho(G, E, s)
        n_eval += 1
        best = min(best, cur)
        temp = 0.15
        while temp > 1e-3 and n_eval < T:
            e = int(rng.integers(m))
            s[e] *= -1
            new = rho(G, E, s)
            n_eval += 1
            if new <= cur or rng.random() < np.exp((cur - new) / temp):
                cur = new
                best = min(best, cur)
            else:
                s[e] *= -1
            temp *= 0.999
    return best, n_eval

def strat_tabu(G, E, T, rng):
    m = len(E)
    tenure = max(4, m // 8)
    best, n_eval = np.inf, 0
    while n_eval < T:
        s = rng.choice([-1.0, 1.0], m)
        cur = rho(G, E, s)
        n_eval += 1
        best = min(best, cur)
        tabu = {}
        stall = 0
        it = 0
        while stall < 25 and n_eval < T:
            cand_best, cand_e = np.inf, -1
            order = rng.permutation(m)
            for e in order[:m]:
                if n_eval >= T:
                    break
                s[e] *= -1
                v = rho(G, E, s)
                n_eval += 1
                s[e] *= -1
                if (tabu.get(e, -1) < it or v < best - 1e-12) and v < cand_best:
                    cand_best, cand_e = v, e
            if cand_e < 0:
                break
            s[cand_e] *= -1
            tabu[cand_e] = it + tenure
            stall = stall + 1 if cand_best >= cur - 1e-12 else 0
            cur = cand_best
            best = min(best, cur)
            it += 1
    return best, n_eval

STRATEGIES = [("greedy_parity", strat_family), ("randcon", strat_randcon),
              ("random", strat_random), ("anneal", strat_anneal),
              ("tabu", strat_tabu)]

# ------------------------------------------------------- instance generators

def gen_planted(i):
    G, got = planted_4cycles(64, 4, 32, np.random.default_rng(SEED0 + i))
    return f"planted64[{i}]", G

def gen_conditioned(i, band=(26, 38), burn=4000):
    """MCMC control on 4-regular n=64 graphs kept in a prescribed #C4 band.
A warm start enters the band, then symmetric double-swap MCMC proposes moves
that are accepted only when the graph remains simple, 4-regular, and in-band.
No uniformity or mixing guarantee is claimed."""
    rng = np.random.default_rng(SEED0 + 500 + i)
    n = 64
    G = nx.random_regular_graph(4, n, seed=int(rng.integers(1 << 31)))
    A = nx.to_numpy_array(G)
    c4 = count_c4(A)

    def try_swap(require_gain):
        nonlocal c4
        edges = list(map(tuple, np.argwhere(np.triu(A) > 0)))
        (a, b) = edges[rng.integers(len(edges))]
        (c, d) = edges[rng.integers(len(edges))]
        if len({a, b, c, d}) < 4:
            return False
        if rng.integers(2):
            c, d = d, c
        if A[a, c] or A[b, d]:
            return False
        A[a, b] = A[b, a] = A[c, d] = A[d, c] = 0
        A[a, c] = A[c, a] = A[b, d] = A[d, b] = 1
        new = count_c4(A)
        ok = (new > c4) if require_gain else (band[0] <= new <= band[1])
        if ok:
            c4 = new
            return True
        A[a, c] = A[c, a] = A[b, d] = A[d, b] = 0
        A[a, b] = A[b, a] = A[c, d] = A[d, c] = 1
        return False

    guard = 0
    while c4 < band[0] and guard < 200000:      # warm into the band
        try_swap(require_gain=True)
        guard += 1
    assert band[0] <= c4 <= band[1] + 20, f"warm start failed (c4={c4})"
    while c4 > band[1]:                          # (rarely) overshot
        try_swap(require_gain=False)
    for _ in range(burn):                        # MCMC burn-in within the band
        try_swap(require_gain=False)
    G = nx.from_numpy_array(A)
    return f"conditioned64[{i}](c4={c4})", G

def gen_circulant(i):
    n = 24 + 4 * i
    return f"C{n}(1,2)", nx.convert_node_labels_to_integers(
        nx.circulant_graph(n, [1, 2]))

SETS = [("planted", gen_planted), ("conditioned", gen_conditioned),
        ("circulant", gen_circulant)]

# ------------------------------------------------------------------ main

def main():
    global CSV
    quick = "--quick" in sys.argv
    if quick:
        CSV = "campaign_quick.csv"   # never pollute the campaign artifact
    n_inst = 3 if quick else N_INST
    budget = 400 if quick else N_EVAL
    done = set()
    if os.path.exists(CSV):
        with open(CSV) as f:
            for r in csv.DictReader(f):
                done.add((r["set"], int(r["i"]), r["strategy"]))
    write_header = not os.path.exists(CSV)
    fout = open(CSV, "a", newline="")
    writer = None
    for set_name, gen in SETS:
        for i in range(n_inst):
            if all((set_name, i, s) in done for s, _ in STRATEGIES):
                continue
            name, G = gen(i)
            E = edge_list(G)
            d = max(x for _, x in G.degree())
            floor = 2 * np.sqrt(d - 1)
            cs_meta = CycleSystem(G, 4)
            constraint_rows = cs_meta.ncon
            constraint_rank = cs_meta.rank
            c4_count = count_c4(nx.to_numpy_array(G)) if d == 4 else None
            for sname, fn in STRATEGIES:
                if (set_name, i, sname) in done:
                    continue
                rng = np.random.default_rng(
                    zlib.crc32(f"{set_name}|{i}|{sname}".encode()))
                t0 = time.perf_counter()
                best, n_eval = fn(G, E, budget, rng)
                wall = time.perf_counter() - t0
                row = dict(set=set_name, i=i, instance=name,
                           n=G.number_of_nodes(), d=d, floor=round(floor, 6),
                           c4_count=c4_count, constraint_rows=constraint_rows,
                           constraint_rank=constraint_rank,
                           strategy=sname, best_rho=round(best, 6),
                           gap=round(best - floor, 6), n_eval=n_eval,
                           wall=round(wall, 3), budget=budget)
                if writer is None:
                    writer = csv.DictWriter(fout, fieldnames=list(row.keys()))
                    if write_header:
                        writer.writeheader()
                writer.writerow(row)
                fout.flush()
            print(f"{name:26s} done", flush=True)
    fout.close()
    summarize()

def summarize():
    rows = list(csv.DictReader(open(CSV)))
    print("\n================ CAMPAIGN SUMMARY (gap to Kesten floor; "
          "95% t-CIs) ================")
    for set_name, _ in SETS:
        sub = [r for r in rows if r["set"] == set_name]
        if not sub:
            continue
        insts = sorted({int(r["i"]) for r in sub})
        print(f"\n-- {set_name} ({len(insts)} instances, "
              f"budget {sub[0]['budget']} rho-evals per strategy) --")
        gaps = {}
        for sname, _ in STRATEGIES:
            g = [float(r["gap"]) for r in sub
                 if r["strategy"] == sname and r["gap"] != "nan"]
            if not g:
                continue
            g = np.array(g)
            tcrit = stats.t.ppf(0.975, len(g) - 1)
            ci = tcrit * g.std(ddof=1) / np.sqrt(len(g))
            gaps[sname] = {int(r["i"]): float(r["gap"]) for r in sub
                           if r["strategy"] == sname}
            ne = np.mean([float(r["n_eval"]) for r in sub
                          if r["strategy"] == sname])
            print(f"  {sname:8s} mean gap {g.mean():+7.4f} +/- {ci:.4f}   "
                  f"(min {g.min():+.4f}, max {g.max():+.4f}; "
                  f"mean evals {ne:.0f})")
        # paired deltas vs family
        if "greedy_parity" in gaps:
            print("  paired deltas (strategy - retained parity; positive = retained parity wins):")
            for sname in ("random", "anneal", "tabu", "randcon"):
                if sname not in gaps:
                    continue
                common = sorted(set(gaps["greedy_parity"]) & set(gaps[sname]))
                dl = np.array([gaps[sname][i] - gaps["greedy_parity"][i]
                               for i in common])
                tcrit = stats.t.ppf(0.975, len(dl) - 1)
                ci = tcrit * dl.std(ddof=1) / np.sqrt(len(dl))
                sig = "SIG" if abs(dl.mean()) > ci else "ns "
                print(f"    {sname:8s} {dl.mean():+7.4f} +/- {ci:.4f}  [{sig}]")

if __name__ == "__main__":
    main()
