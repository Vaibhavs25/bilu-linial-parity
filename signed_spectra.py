"""
signed_spectra.py — experimental toolkit for the Bilu-Linial defect program.

Conventions:
  * Graph G connected, adjacency A. A signing sigma in {+1,-1}^E.
  * Spectrum of A_sigma depends only on the switching class, which is
    determined by the signs of cycles. Fix a spanning tree T, set tree
    edges to +1; the 2^(m-n+1) assignments to co-tree edges enumerate
    switching classes exactly once (equal weight under uniform sigma).
  * rho(A_sigma) = max |eigenvalue|.  Kesten floor F(d) = 2*sqrt(d-1).
  * defect delta(G) = min_class rho - F(d).
"""
import itertools
import numpy as np
import networkx as nx
from fractions import Fraction

# ---------------------------------------------------------------- basics

def edge_list(G):
    return [tuple(sorted(e)) for e in G.edges()]

def spanning_tree_split(G):
    """Return (edges, tree_idx, cotree_idx) with a fixed edge order."""
    E = edge_list(G)
    T = nx.minimum_spanning_tree(G)
    tset = {tuple(sorted(e)) for e in T.edges()}
    tree_idx = [i for i, e in enumerate(E) if e in tset]
    cot_idx = [i for i, e in enumerate(E) if e not in tset]
    return E, tree_idx, cot_idx

def signed_adjacency(n, E, signs):
    A = np.zeros((n, n))
    for (u, v), s in zip(E, signs):
        A[u, v] = s
        A[v, u] = s
    return A

def enumerate_class_matrices(G, chunk=1 << 14):
    """Yield (bits, stack_of_A_sigma) over all switching classes, chunked.

    bits: int array of co-tree sign patterns (bit=1 means -1 edge).
    """
    n = G.number_of_nodes()
    E, tree_idx, cot_idx = spanning_tree_split(G)
    k = len(cot_idx)
    base = signed_adjacency(n, E, np.ones(len(E)))
    # rank-2 flip matrices for each co-tree edge: A -> A - 2*(E_uv+E_vu)
    flips = []
    for i in cot_idx:
        u, v = E[i]
        M = np.zeros((n, n))
        M[u, v] = M[v, u] = -2.0
        flips.append(M)
    flips = np.array(flips) if k else np.zeros((0, n, n))
    total = 1 << k
    for start in range(0, total, chunk):
        idx = np.arange(start, min(start + chunk, total), dtype=np.int64)
        stack = np.broadcast_to(base, (len(idx), n, n)).copy()
        for j in range(k):
            mask = (idx >> j) & 1
            stack[mask == 1] += flips[j]
        yield idx, stack

def defect_atlas_entry(G, name, cycle_len_bound=6):
    """Exhaustive min over switching classes; also profile of short cycles
    unbalanced at (one) optimum."""
    n, d = G.number_of_nodes(), max(dict(G.degree()).values())
    E, tree_idx, cot_idx = spanning_tree_split(G)
    k = len(cot_idx)
    floor = 2.0 * np.sqrt(d - 1)
    best_rho, best_bits = np.inf, None
    rand_rhos = []
    for idx, stack in enumerate_class_matrices(G):
        w = np.linalg.eigvalsh(stack)
        rho = np.abs(w).max(axis=1)
        j = rho.argmin()
        if rho[j] < best_rho:
            best_rho, best_bits = float(rho[j]), int(idx[j])
        rand_rhos.append(rho)
    rand_rhos = np.concatenate(rand_rhos)
    # short-cycle profile at optimum
    signs = np.ones(len(E))
    for j, ei in enumerate(cot_idx):
        if (best_bits >> j) & 1:
            signs[ei] = -1
    eidx = {e: i for i, e in enumerate(E)}
    cyc_stats = {}
    try:
        cycles = nx.simple_cycles(G, length_bound=cycle_len_bound)
    except TypeError:  # networkx < 3.1 lacks length_bound
        raise RuntimeError("networkx >= 3.1 required (simple_cycles length_bound)")
        # unreachable:
        cycles = []
    for c in cycles:
        L = len(c)
        prod = 1
        for a in range(L):
            e = tuple(sorted((c[a], c[(a + 1) % L])))
            prod *= signs[eidx[e]]
        tot, unb = cyc_stats.get(L, (0, 0))
        cyc_stats[L] = (tot + 1, unb + (1 if prod < 0 else 0))
    girth = nx.girth(G)  # exact girth (inf only for forests)
    return dict(name=name, n=n, d=d, m=len(E), k=k, girth=girth,
                floor=floor, min_rho=best_rho, defect=best_rho - floor,
                mean_rho=float(rand_rhos.mean()),
                frac_below_floor=float((rand_rhos < floor - 1e-9).mean()),
                cycle_profile={L: f"{u}/{t}" for L, (t, u) in
                               sorted(cyc_stats.items())})

# ------------------------------------------------- q_G = E det(xI - A^2)

def qG_polynomial(G):
    """Exact E_sigma det(xI - A_sigma^2) as Fraction coefficients
    (uniform over switching classes = uniform over sigma)."""
    n = G.number_of_nodes()
    coeffs_sum = None
    count = 0
    for idx, stack in enumerate_class_matrices(G):
        for A in stack:
            w = np.linalg.eigvalsh(A)
            p_raw = np.poly(np.round(w ** 2, 12))   # char poly of A^2
            resid = float(np.abs(p_raw - np.round(p_raw)).max())
            assert resid < 1e-6, (
                f"qG charpoly not near-integer (resid={resid}); float64 overflow")
            p = [Fraction(int(round(c))) for c in np.round(p_raw)]
            coeffs_sum = p if coeffs_sum is None else \
                [a + b for a, b in zip(coeffs_sum, p)]
            count += 1
    return [c / count for c in coeffs_sum]

def qG_verdict(G, name):
    d = max(dict(G.degree()).values())
    q = qG_polynomial(G)  # exact Fraction coefficients
    # exact real-rootedness by Sturm (real_roots counts with multiplicity);
    # np.roots is kept only for the reported float diagnostics -- a double
    # real root perturbs to ~1e-8i and misclassifies odd cycles otherwise.
    from sympy import Poly, symbols, real_roots, Rational
    xs = symbols('x')
    qp = Poly([Rational(c.numerator, c.denominator) for c in q], xs)
    real_rooted = (len(real_roots(qp)) == qp.degree())
    r = np.roots([float(c) for c in q])
    im = float(np.abs(r.imag).max()) if len(r) else 0.0
    return dict(name=name, d=d, real_rooted=real_rooted, max_im=im,
                max_real_part=float(r.real.max()),
                bound_4dm1=4 * (d - 1),
                coeffs=[str(c) for c in q])

# ------------------------------------- GF(2): unbalance all short cycles

def short_cycles(G, L):
    return [c for c in nx.simple_cycles(G, length_bound=L)]

def unbalanced_signing_family(G, L, n_samples=1, rng=None, even_only=True):
    """Sign patterns (tree edges +1) for the system 'every even cycle
    of length <= L unbalanced' -- the parity family (even_only=True,
    the default). Pass even_only=False to constrain ALL cycles <= L,
    e.g. to force triangles unbalanced deliberately.
    Row-reduces over GF(2), dropping inconsistent rows greedily.

    Returns (sols, ncon, nsat_greedy). CAUTION: nsat_greedy is the size
    of ONE consistent subsystem found by this particular elimination
    order. It is a lower bound on the max-satisfiable count and is
    ORDER-DEPENDENT; it is NOT beta_L * ncon (computing beta_L exactly
    is MAX-XOR-SAT, NP-hard). By averaging over uniform signings,
    beta_L >= 1/2 always. If nsat_greedy < ncon the system is
    inconsistent and the returned signings do NOT unbalance all short
    cycles -- callers must check nsat_greedy == ncon before treating
    sols as the parity family."""
    rng = rng or np.random.default_rng(0)
    E, tree_idx, cot_idx = spanning_tree_split(G)
    k = len(cot_idx)
    eidx = {e: i for i, e in enumerate(E)}
    cpos = {ei: j for j, ei in enumerate(cot_idx)}
    rows, rhs = [], []
    for c in short_cycles(G, L):
        if even_only and len(c) % 2:
            continue
        row = np.zeros(k, dtype=np.uint8)
        for a in range(len(c)):
            e = tuple(sorted((c[a], c[(a + 1) % len(c)])))
            i = eidx[e]
            if i in cpos:
                row[cpos[i]] ^= 1
        rows.append(row)
        rhs.append(1)
    Amat = np.array(rows, dtype=np.uint8) if rows else np.zeros((0, k), np.uint8)
    b = np.array(rhs, dtype=np.uint8)
    # Gaussian elimination over GF(2), greedy-drop inconsistent rows
    Aw, bw = Amat.copy(), b.copy()
    piv_cols, kept = [], []
    r = 0
    for c in range(k):
        pr = None
        for i in range(r, len(Aw)):
            if Aw[i, c]:
                pr = i
                break
        if pr is None:
            continue
        Aw[[r, pr]] = Aw[[pr, r]]
        bw[[r, pr]] = bw[[pr, r]]
        for i in range(len(Aw)):
            if i != r and Aw[i, c]:
                Aw[i] ^= Aw[r]
                bw[i] ^= bw[r]
        piv_cols.append(c)
        r += 1
    n_bad = int(sum(1 for i in range(r, len(Aw)) if bw[i]))  # 0=x with rhs 1
    # particular solution
    x0 = np.zeros(k, dtype=np.uint8)
    for i, c in enumerate(piv_cols):
        x0[c] = bw[i]
    free_cols = [c for c in range(k) if c not in piv_cols]
    sols = []
    for _ in range(n_samples):
        x = x0.copy()
        if free_cols:
            x[free_cols] = rng.integers(0, 2, len(free_cols), dtype=np.uint8)
            # back-substitute pivots given free choices
            for i, c in enumerate(piv_cols):
                v = bw[i]
                for fc in free_cols:
                    if Aw[i, fc]:
                        v ^= x[fc]
                x[c] = v
        signs = np.ones(len(E))
        for j, ei in enumerate(cot_idx):
            if x[j]:
                signs[ei] = -1
        sols.append(signs)
    return sols, len(rows), len(rows) - n_bad

def rho_of(G, signs):
    A = signed_adjacency(G.number_of_nodes(), edge_list(G), signs)
    return float(np.abs(np.linalg.eigvalsh(A)).max())

def local_search(G, signs, iters=400):
    """Steepest-descent on rho via single co-tree flips. Each candidate
    flip is evaluated with a full dense eigvalsh (a flip is a rank-2
    perturbation of A, but no incremental update is implemented; cost
    is O(iters * k * n^3)). Co-tree flips reach every switching class,
    so the search space is complete; the neighbourhood structure
    depends on the spanning tree."""
    E, tree_idx, cot_idx = spanning_tree_split(G)
    s = signs.copy()
    cur = rho_of(G, s)
    for _ in range(iters):
        best, bj = cur, None
        for j in cot_idx:
            s[j] *= -1
            r = rho_of(G, s)
            s[j] *= -1
            if r < best - 1e-12:
                best, bj = r, j
        if bj is None:
            break
        s[bj] *= -1
        cur = best
    return cur, s

def compare_strategies(G, name, L, n_rand=60, n_unb=60, ls=True, rng=None, even_only=True):
    rng = rng or np.random.default_rng(1)
    d = max(dict(G.degree()).values())
    floor = 2 * np.sqrt(d - 1)
    E = edge_list(G)
    # pure random (signs kept so rand+LS can seed from the best draw)
    rsigns = [rng.choice([-1.0, 1.0], len(E)) for _ in range(n_rand)]
    rr = [rho_of(G, s) for s in rsigns]
    # unbalanced short cycles + random tail
    sols, ncon, nsat = unbalanced_signing_family(G, L, n_samples=n_unb, rng=rng, even_only=even_only)
    ur = [rho_of(G, s) for s in sols]
    out = dict(name=name, n=G.number_of_nodes(), d=d, floor=floor,
               unsigned=rho_of(G, np.ones(len(E))),
               L=L, constraints=ncon, satisfied=nsat,
               rand_best=min(rr), rand_mean=float(np.mean(rr)),
               unb_best=min(ur), unb_mean=float(np.mean(ur)))
    if ls:
        # fair seeding: both sides start local search from the best of
        # their own n draws (previously best-of-60 vs a single draw)
        i = int(np.argmin(ur))
        out["unb+LS"] = local_search(G, sols[i], iters=200)[0]
        j = int(np.argmin(rr))
        out["rand+LS"] = local_search(G, rsigns[j], iters=200)[0]
    return out
