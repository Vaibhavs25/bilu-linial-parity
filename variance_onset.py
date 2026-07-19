"""
variance_onset.py — does rho depend only on the short-even-cycle signature?

For each instance G:
  1. Build the F2 system "every even cycle of length <= L is unbalanced"
     over co-tree sign bits (tree edges fixed +1, one representative per
     switching class). Greedy-drop inconsistent rows -> ONE consistent
     subset, beta = nsat/ncon.
  2. The solution space is affine: particular solution + kernel. Kernel
     directions change ONLY long-cycle signs; the short even signature is
     frozen. Sample N_TAILS kernel points, record the rho distribution.
  3. Reference: N_RAND uniformly random signings (short cycles vary too).
  Zero spread across tails  => rho determined by the short-even signature.
  Spread onset (vs n)       => long-cycle terms entering; measures where
                               the trace expansion stops being dominated
                               by short even cycles.

Families: random 2-lift towers of Q3 and K4 (symmetry-free, generic),
planted-4-cycle random 4-regular graphs (non-transitive, tunable cycle
density), plain random 4-regular (sparse-cycle control), circulants
(vertex-transitive control: flat for the boring reason).

Checkpointed: appends to variance_onset.csv, skips completed rows.
Usage:  python3 variance_onset.py [--smoke]
"""
import sys, os, csv, time
import numpy as np
import networkx as nx
from signed_spectra import spanning_tree_split, edge_list, signed_adjacency

CSV = "variance_onset_v2.csv"  # v1 (shipped) used field name beta and included x0 in stats
N_TAILS, N_RAND = 200, 100

# ------------------------------------------------------------ F2 system

class CycleSystem:
    """Constraints: sum of co-tree bits over each even cycle (<=L) == 1."""

    def __init__(self, G, L):
        self.G = G
        self.n = G.number_of_nodes()
        self.E, self.tree_idx, self.cot_idx = spanning_tree_split(G)
        self.k = len(self.cot_idx)
        eidx = {e: i for i, e in enumerate(self.E)}
        cpos = {ei: j for j, ei in enumerate(self.cot_idx)}
        rows = []
        for c in nx.simple_cycles(G, length_bound=L):
            if len(c) % 2:
                continue
            row = np.zeros(self.k, dtype=np.uint8)
            for a in range(len(c)):
                e = tuple(sorted((c[a], c[(a + 1) % len(c)])))
                i = eidx[e]
                if i in cpos:               # tree edges are fixed +1
                    row[cpos[i]] ^= 1
            rows.append(row)
        self.ncon = len(rows)
        A = (np.array(rows, dtype=np.uint8) if rows
             else np.zeros((0, self.k), np.uint8))
        b = np.ones(len(rows), dtype=np.uint8)
        # RREF over GF(2)
        A, b = A.copy(), b.copy()
        piv, r = [], 0
        for c in range(self.k):
            pr = next((i for i in range(r, len(A)) if A[i, c]), None)
            if pr is None:
                continue
            A[[r, pr]], b[[r, pr]] = A[[pr, r]], b[[pr, r]]
            hit = np.nonzero(A[:, c])[0]
            for i in hit:
                if i != r:
                    A[i] ^= A[r]
                    b[i] ^= b[r]
            piv.append(c)
            r += 1
        self.nsat = self.ncon - int(b[r:].sum())   # 0=x rows with rhs 1
        self.A, self.b, self.piv, self.rank = A[:r], b[:r], piv, r
        self.free = [c for c in range(self.k) if c not in piv]

    def solution(self, tail_bits):
        """tail_bits over free columns -> full sign vector over E."""
        x = np.zeros(self.k, dtype=np.uint8)
        x[self.free] = tail_bits
        for i, c in enumerate(self.piv):
            v = self.b[i]
            for fc in self.free:            # back-substitute
                if self.A[i, fc]:
                    v ^= x[fc]
            x[c] = v
        signs = np.ones(len(self.E))
        for j, ei in enumerate(self.cot_idx):
            if x[j]:
                signs[ei] = -1.0
        return signs

def rho(G, signs):
    n = G.number_of_nodes()
    A = signed_adjacency(n, edge_list(G), signs)
    if n >= 256:  # sparse extremal eigenvalues; dense fallback on any hiccup
        try:
            from scipy.sparse import csr_matrix
            from scipy.sparse.linalg import eigsh
            w = eigsh(csr_matrix(A), k=2, which="BE",
                      return_eigenvectors=False, tol=1e-9)
            return float(np.abs(w).max())
        except Exception:
            pass
    return float(np.abs(np.linalg.eigvalsh(A)).max())

# ------------------------------------------------------------- families

def random_2lift(G, rng):
    while True:
        H = nx.Graph()
        H.add_nodes_from((v, i) for v in G.nodes for i in (0, 1))
        for (u, v) in G.edges():
            if rng.integers(2):                       # -1 : cross
                H.add_edge((u, 0), (v, 1)); H.add_edge((u, 1), (v, 0))
            else:
                H.add_edge((u, 0), (v, 0)); H.add_edge((u, 1), (v, 1))
        if nx.is_connected(H):
            return nx.convert_node_labels_to_integers(H)

def lift_tower(base, n_target, rng):
    G = nx.convert_node_labels_to_integers(base)
    while G.number_of_nodes() < n_target:
        G = random_2lift(G, rng)
    return G

def planted_4cycles(n, d, n_plant, rng, tries_per=200):
    G = nx.random_regular_graph(d, n, seed=int(rng.integers(1 << 30)))
    while not nx.is_connected(G):
        G = nx.random_regular_graph(d, n, seed=int(rng.integers(1 << 30)))
    planted = 0
    for _ in range(n_plant * tries_per):
        if planted >= n_plant:
            break
        b = int(rng.integers(n))
        nb = list(G[b])
        if len(nb) < 2:
            continue
        a, c = rng.choice(nb, 2, replace=False)
        nc = [w for w in G[c] if w not in (a, b)]
        if not nc:
            continue
        dd = int(rng.choice(nc))
        if G.has_edge(a, dd):
            continue
        xs = [w for w in G[a] if w not in (b, dd)]
        ys = [w for w in G[dd] if w not in (c, a)]
        rng.shuffle(xs); rng.shuffle(ys)
        done = False
        for x in xs:
            for y in ys:
                if x != y and not G.has_edge(x, y):
                    G.remove_edge(a, x); G.remove_edge(dd, y)
                    G.add_edge(a, dd);  G.add_edge(x, y)
                    if nx.is_connected(G):
                        planted += 1; done = True
                    else:
                        G.remove_edge(a, dd); G.remove_edge(x, y)
                        G.add_edge(a, x);    G.add_edge(dd, y)
                    break
            if done:
                break
    return G, planted

# ---------------------------------------------------------------- runner

def measure(name, G, L, seed):
    t0 = time.time()
    rng = np.random.default_rng(seed)
    n = G.number_of_nodes()
    d = max(dd for _, dd in G.degree())
    cs = CycleSystem(G, L)
    kdim = len(cs.free)
    # zero tail = deterministic greedy particular solution: reported
    # separately (rho_zero_tail) and EXCLUDED from dispersion statistics
    # -- including it inflated tail_std in an earlier version (it is a
    # 12--34 sigma outlier on towers).
    tails = [np.zeros(kdim, dtype=np.uint8)]
    n_draw = min(N_TAILS, 1 << min(kdim, 30)) - 1
    if kdim <= 20:  # small kernel: sample distinct tails
        pool = rng.choice(np.arange(1, 1 << kdim),
                          size=min(n_draw, (1 << kdim) - 1), replace=False)
        for bits in pool:
            tails.append(np.array([(int(bits) >> j) & 1 for j in range(kdim)],
                                  dtype=np.uint8))
    else:
        for _ in range(n_draw):
            tails.append(rng.integers(0, 2, kdim, dtype=np.uint8))
    tr = np.array([rho(G, cs.solution(t)) for t in tails])
    tr_nozero = tr[1:]   # always exclude the deterministic zero tail
    if len(tr_nozero) >= 2:  # need at least 2 points for a meaningful std
        tr_stats = tr_nozero
    else:  # kdim=0 (zero tail only) or kdim=1 (one non-zero tail): no dispersion
        tr_stats = np.array([np.nan])
    rr = np.array([rho(G, rng.choice([-1.0, 1.0], len(cs.E)))
                   for _ in range(N_RAND)])
    row = dict(family=name, n=n, d=d, seed=seed, L=L,
               m=len(cs.E), k=cs.k, ncon=cs.ncon, nsat=cs.nsat,
               beta_greedy=round(cs.nsat / cs.ncon, 4) if cs.ncon else 1.0,
               kernel_dim=kdim, ntails=len(tails),
               floor=round(2 * np.sqrt(d - 1), 4),
               rho_zero_tail=round(float(tr[0]), 6),
               tail_mean=round(float(tr_stats.mean()), 6),
               tail_std=round(float(tr_stats.std()), 6),
               tail_min=round(float(tr_stats.min()), 6),
               tail_max=round(float(tr_stats.max()), 6),
               tail_spread=round(float(tr_stats.max() - tr_stats.min()), 6),
               rand_mean=round(float(rr.mean()), 4),
               rand_std=round(float(rr.std()), 4),
               rand_min=round(float(rr.min()), 4),
               std_ratio=round(float(tr_stats.std() / max(rr.std(), 1e-12)), 4),
               sec=round(time.time() - t0, 1))
    return row

def instances(smoke):
    rng = np.random.default_rng(2026)
    tower_ns = [16, 32, 64] if smoke else [16, 32, 64, 128, 256, 512, 1024]
    plant_ns = [32, 64] if smoke else [32, 64, 128, 256, 512]
    seeds = [0] if smoke else [0, 1, 2]
    for s in seeds:
        for nt in tower_ns:
            yield (f"towerQ3", lift_tower(nx.hypercube_graph(3), nt,
                   np.random.default_rng(100 + s)), 6, s)
            yield (f"towerK4", lift_tower(nx.complete_graph(4), nt,
                   np.random.default_rng(200 + s)), 6, s)
        for np_ in plant_ns:
            G, got = planted_4cycles(np_, 4, np_ // 2,
                                     np.random.default_rng(300 + s))
            # 'got' counts successful swaps (not net 4-cycle count); it is
            # part of the family name, so it is now also part of the
            # checkpoint identity -- a rerun landing a different got will
            # recompute rather than silently duplicate.
            yield (f"planted4reg[{got}]", G, 4, s)
    for np_ in ([64] if smoke else [64, 256]):
        yield ("plain4reg", nx.random_regular_graph(4, np_, seed=9), 4, 0)
    for nc in ([30] if smoke else [30, 120, 480]):
        yield ("circulant12", nx.convert_node_labels_to_integers(
               nx.circulant_graph(nc, [1, 2])), 4, 0)

def main():
    smoke = "--smoke" in sys.argv
    done = set()
    if os.path.exists(CSV):
        with open(CSV) as f:
            for r in csv.DictReader(f):
                done.add((r["family"], int(r["n"]), int(r["seed"])))
    write_header = not os.path.exists(CSV)
    fout = open(CSV, "a", newline="")
    writer = None
    for name, G, L, seed in instances(smoke):
        key = (name.split('[')[0], G.number_of_nodes(), seed)  # strip realized swap count
        if key in done:
            continue
        row = measure(name, G, L, seed)
        if writer is None:
            writer = csv.DictWriter(fout, fieldnames=list(row.keys()))
            if write_header:
                writer.writeheader()
        writer.writerow(row); fout.flush()
        print(f"{row['family']:16s} n={row['n']:5d} s={seed} "
              f"beta_greedy={row['beta_greedy']:.3f} kdim={row['kernel_dim']:4d} | "
              f"tail std={row['tail_std']:.2e} spread={row['tail_spread']:.4f} "
              f"min={row['tail_min']:.4f} zero={row['rho_zero_tail']:.4f} | "
              f"rand std={row['rand_std']:.4f} min={row['rand_min']:.4f} | "
              f"floor={row['floor']} ratio={row['std_ratio']:.3f} "
              f"[{row['sec']}s]", flush=True)
    fout.close()
    print("complete ->", CSV)

if __name__ == "__main__":
    main()
