"""trace_rates.py -- the three-average trace rates against the tree profile.

Computes R_F(k) = (E_F tr A^{2k})^{1/2k} over the sampled parity family,
R_all over uniform signings, R_bal over the balanced family (all short even
cycles balanced), and the tree profile (n * t_{2k}(d))^{1/2k}, on a random
2-lift tower of K4 and a planted-quadrilateral instance (n=128 each).
These are the quantities discussed in Paper A, Section 8.
"""
import numpy as np
import networkx as nx
from variance_onset import CycleSystem, lift_tower, planted_4cycles
from signed_spectra import signed_adjacency, edge_list


def tree_t2k(d, k):
    """Closed walks of length 2k at the root of the d-regular tree."""
    w = np.zeros(2 * k + 1)
    w[0] = 1.0
    for _ in range(2 * k):
        nw = np.zeros_like(w)
        for j in range(2 * k + 1):
            if not w[j]:
                continue
            up = d if j == 0 else d - 1
            if j + 1 <= 2 * k:
                nw[j + 1] += w[j] * up
            if j - 1 >= 0:
                nw[j - 1] += w[j]
        w = nw
    return w[0]


def rates(name, G, L=6, M=200, ks=(10, 20, 30, 40), seed=7):
    rng = np.random.default_rng(seed)
    E = edge_list(G)
    n, d = G.number_of_nodes(), G.degree(0)
    cs = CycleSystem(G, L)
    kd = len(cs.free)
    s0 = cs.solution(np.zeros(kd, dtype=np.uint8))
    def spec(s):
        return np.linalg.eigvalsh(signed_adjacency(n, E, s))
    fam = [spec(cs.solution(rng.integers(0, 2, kd, dtype=np.uint8))) for _ in range(M)]
    bal = [spec(cs.solution(rng.integers(0, 2, kd, dtype=np.uint8)) * s0) for _ in range(M)]
    alls = [spec(rng.choice([-1.0, 1.0], len(E))) for _ in range(M)]
    floor = 2 * np.sqrt(d - 1)
    print(f"== {name}: n={n} d={d} ncon={cs.ncon} nsat_greedy={cs.nsat} kdim={kd} floor={floor:.4f}")
    print(f"{'k':>3s} {'R_F':>8s} {'R_all':>8s} {'R_bal':>8s} {'R_tree':>8s}")
    for k in ks:
        RF = np.mean([np.sum(w ** (2 * k)) for w in fam]) ** (1 / (2 * k))
        RA = np.mean([np.sum(w ** (2 * k)) for w in alls]) ** (1 / (2 * k))
        RB = np.mean([np.sum(w ** (2 * k)) for w in bal]) ** (1 / (2 * k))
        RT = (n * tree_t2k(d, k)) ** (1 / (2 * k))
        print(f"{k:3d} {RF:8.4f} {RA:8.4f} {RB:8.4f} {RT:8.4f}")
        assert np.isfinite([RF, RA, RB, RT]).all()
        # Correct sandwich: t_{2k} <= (2k choose k)(d-1)^k <= (2 sqrt(d-1))^{2k},
        # so RT <= floor * n^{1/2k}; the k^{-3/2} prefactor can pull RT slightly
        # BELOW the floor at finite k (it does at d=4, n=128, k=40) -- the old
        # assertion RT > floor was wrong and never executed before shipping.
        assert 0.9 * floor < RT <= floor * n ** (1 / (2 * k)) + 1e-9
    print()


def constant_density():
    """The three-average measurement at constant quadrilateral density
    (Paper A Sec. 8: excess 0.12--0.15, Efam/nt 0.08--0.11, seeds as in the
    original run: instance seed 300, sampling seed 5)."""
    import copy
    def tree_prof(d, K):
        a = np.zeros(2 * K + 2); a[0] = 1.0; out = {}
        for step in range(2 * K):
            b = np.zeros_like(a)
            for r in range(2 * K + 1):
                if a[r]:
                    b[r + 1] += a[r] * (d if r == 0 else d - 1)
                    if r > 0:
                        b[r - 1] += a[r]
            a = b
            if step % 2 == 1:
                out[step + 1] = a[0]
        return out

    def measure(G, L, M, K, tag):
        rng = np.random.default_rng(5)
        n, d = G.number_of_nodes(), max(x for _, x in G.degree())
        E = edge_list(G)
        cs = CycleSystem(G, L); kd = len(cs.free)
        csb = copy.copy(cs); csb.b = np.zeros_like(cs.b)
        lam = {}
        for nm, gen in (("fam", lambda: cs.solution(rng.integers(0, 2, kd, dtype=np.uint8))),
                        ("bal", lambda: csb.solution(rng.integers(0, 2, kd, dtype=np.uint8))),
                        ("all", lambda: rng.choice([-1., 1.], len(E)))):
            lam[nm] = np.array([np.linalg.eigvalsh(
                signed_adjacency(n, E, gen())) for _ in range(M)])
        t2k = tree_prof(d, K)
        print(f"== {tag}: n={n} beta_greedy={cs.nsat}/{cs.ncon} floor={2*np.sqrt(d-1):.4f}")
        for k in (8, 16, 24, 30):
            Es = {nm: float(np.mean(np.sum(lam[nm] ** (2 * k), axis=1))) for nm in lam}
            nt = n * t2k[2 * k]
            print(f" k={k:2d} R_fam={Es['fam']**(1/(2*k)):.4f} "
                  f"R_all={Es['all']**(1/(2*k)):.4f} R_bal={Es['bal']**(1/(2*k)):.4f} "
                  f"R_tree={nt**(1/(2*k)):.4f} Efam/nt={Es['fam']/nt:.4f} "
                  f"Ebal/Eall={Es['bal']/Es['all']:.2f}", flush=True)

    for nn, MM in ((256, 500), (512, 300)):
        G, got = planted_4cycles(nn, 4, nn // 2, np.random.default_rng(300))
        measure(G, 4, MM, 30, f"planted4reg n={nn} [{got} planted]")


if __name__ == "__main__":
    rates("towerK4 n=128 (seed 100)",
          lift_tower(nx.complete_graph(4), 128, np.random.default_rng(100)))
    G, got = planted_4cycles(128, 4, 64, np.random.default_rng(300))
    rates(f"planted4reg n=128 ({got} swaps)", G, L=4)
    rates("C60(1,2) circulant control",
          nx.convert_node_labels_to_integers(nx.circulant_graph(60, [1, 2])), L=4)
    constant_density()
