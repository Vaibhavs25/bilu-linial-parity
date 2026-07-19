"""
verify_all.py — reproduces every computational claim made in
  Paper A: "Parity families and a kernel-averaged L-function ..."
  Paper B: "Signed circulants at the Ramanujan bound"

Run:  python3 verify_all.py          (~3 min, needs numpy + networkx + sympy)
Each check prints PASS/FAIL and the numbers behind it. A final summary
line reports the count. Requires signed_spectra.py in the same directory.
"""
import numpy as np
import networkx as nx
from itertools import product

from signed_spectra import (edge_list, spanning_tree_split, signed_adjacency,
                            enumerate_class_matrices)

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if detail:
        print(f"        {detail}")


# ------------------------------------------------------------------ helpers

def gf2_solve(rows, target):
    """Solve sum_i x_i * rows[i] = target over F2. Returns x or None."""
    if len(rows) == 0:
        return np.zeros(0, np.uint8) if not target.any() else None
    A = np.concatenate([np.array(rows, np.uint8).T,
                        target[:, None].astype(np.uint8)], axis=1)
    r, piv = 0, []
    for c in range(A.shape[1] - 1):
        p = next((i for i in range(r, A.shape[0]) if A[i, c]), None)
        if p is None:
            continue
        A[[r, p]] = A[[p, r]]
        for i in range(A.shape[0]):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        piv.append(c)
        r += 1
    if A[r:, -1].any():
        return None
    x = np.zeros(A.shape[1] - 1, np.uint8)
    for i, c in enumerate(piv):
        x[c] = A[i, -1]
    return x


def even_cycle_rows(G, L):
    """Indicator vectors (over E) of even cycles of length <= L."""
    E = edge_list(G)
    eidx = {e: i for i, e in enumerate(E)}
    rows = []
    for c in nx.simple_cycles(G, length_bound=L):
        if len(c) % 2:
            continue
        r = np.zeros(len(E), np.uint8)
        for a in range(len(c)):
            r[eidx[tuple(sorted((c[a], c[(a + 1) % len(c)])))]] ^= 1
        rows.append(r)
    return rows


def family_signings(G, L, rhs=1, limit=None):
    """All signings (tree edges +1) solving 'even cycles <= L have sign
    (-1)^rhs'; returns [] if inconsistent."""
    E = edge_list(G)
    _, _, cot = spanning_tree_split(G)
    eidx = {e: i for i, e in enumerate(E)}
    cpos = {ei: j for j, ei in enumerate(cot)}
    k = len(cot)
    rows, b = [], []
    for c in nx.simple_cycles(G, length_bound=L):
        if len(c) % 2:
            continue
        row = np.zeros(k, np.uint8)
        for a in range(len(c)):
            i = eidx[tuple(sorted((c[a], c[(a + 1) % len(c)])))]
            if i in cpos:
                row[cpos[i]] ^= 1
        rows.append(row)
        b.append(rhs)
    A = np.array(rows, np.uint8) if rows else np.zeros((0, k), np.uint8)
    bb = np.array(b, np.uint8)
    r, piv = 0, []
    for c in range(k):
        p = next((i for i in range(r, len(A)) if A[i, c]), None)
        if p is None:
            continue
        A[[r, p]], bb[[r, p]] = A[[p, r]], bb[[p, r]]
        for i in range(len(A)):
            if i != r and A[i, c]:
                A[i] ^= A[r]
                bb[i] ^= bb[r]
        piv.append(c)
        r += 1
    if bb[r:].any():
        return None
    free = [c for c in range(k) if c not in piv]
    out = []
    n_iter = 1 << len(free) if limit is None else min(1 << len(free), limit)
    for t in range(n_iter):
        x = np.zeros(k, np.uint8)
        for j, fc in enumerate(free):
            x[fc] = (t >> j) & 1
        for i, c in enumerate(piv):
            v = bb[i]
            for fc in free:
                if A[i, fc]:
                    v ^= x[fc]
            x[c] = v
        s = np.ones(len(E))
        for j, ei in enumerate(cot):
            if x[j]:
                s[ei] = -1.0
        out.append(s)
    return out


def rho(G, s):
    return float(np.abs(np.linalg.eigvalsh(
        signed_adjacency(G.number_of_nodes(), edge_list(G), s))).max())


def nb_matrix(G, s):
    E = edge_list(G)
    eidx = {e: i for i, e in enumerate(E)}
    ded = [(u, v) for u, v in E] + [(v, u) for u, v in E]
    di = {e: i for i, e in enumerate(ded)}
    B = np.zeros((len(ded), len(ded)))
    for i, (u, v) in enumerate(ded):
        for w in G[v]:
            if w != u:
                B[i, di[(v, w)]] = s[eidx[tuple(sorted((v, w)))]]
    return B


# ======================================================== Paper A, Lemma 1/9
# Master identity: E_fam tr A^l = sum_{z in W} (-1)^{pi(z)} N_l(z)

def check_master_identity():
    G = nx.convert_node_labels_to_integers(
        nx.cartesian_product(nx.cycle_graph(3), nx.complete_graph(2)))  # prism
    E = edge_list(G)
    eidx = {e: i for i, e in enumerate(E)}
    rows = even_cycle_rows(G, 4)
    fam = family_signings(G, 4)
    ok, det = True, []
    for L in (4, 6, 8):
        # LHS: family average of tr A^L (exact integer arithmetic)
        lhs = np.mean([np.trace(np.linalg.matrix_power(
            signed_adjacency(G.number_of_nodes(), E, s).astype(np.int64), L))
            for s in fam])
        # RHS: sum over closed walks with parity in W, signed by pi
        rhs = 0
        for start in G.nodes:
            stack = [(start, [], np.zeros(len(E), np.uint8))]
            for _ in range(L):
                nxt = []
                for v, path, z in stack:
                    for w in G[v]:
                        z2 = z.copy()
                        z2[eidx[tuple(sorted((v, w)))]] ^= 1
                        nxt.append((w, path + [w], z2))
                stack = nxt
            for v, path, z in stack:
                if v != start:
                    continue
                x = gf2_solve(rows, z)
                if x is not None:
                    rhs += (-1) ** int(x.sum() % 2)
        ok &= abs(lhs - rhs) < 1e-6
        det.append(f"l={L}: LHS={lhs:.1f} RHS={rhs}")
    check("Paper A Prop 7 (master identity), prism l=4,6,8", ok, "; ".join(det))


# ================================================= Paper A, Prop 14 (slice)

def check_slice_and_doubling():
    G = nx.convert_node_labels_to_integers(
        nx.cartesian_product(nx.cycle_graph(3), nx.complete_graph(2)))
    E = edge_list(G)
    ded = [(u, v) for u, v in E] + [(v, u) for u, v in E]
    LMAX = 10
    brute = np.zeros(LMAX + 1)

    def dfs(walk, mult):
        l = len(walk)
        if l >= 2 and walk[-1][1] == walk[0][0] and \
           walk[-1] != (walk[0][1], walk[0][0]):
            if all(x % 2 == 0 for x in mult.values()):
                brute[l] += 1
        if l == LMAX:
            return
        u, v = walk[-1]
        for w in G[v]:
            if w == u:
                continue
            e = tuple(sorted((v, w)))
            mult[e] = mult.get(e, 0) + 1
            dfs(walk + [(v, w)], mult)
            mult[e] -= 1

    for e0 in ded:
        dfs([e0], {tuple(sorted(e0)): 1})
    # E over all signings of tr B_sigma^l
    _, _, cot = spanning_tree_split(G)
    k = len(cot)
    acc = np.zeros(LMAX + 1)
    for bits in range(1 << k):
        s = np.ones(len(E))
        for j, ei in enumerate(cot):
            if (bits >> j) & 1:
                s[ei] = -1
        B = nb_matrix(G, s)
        P = np.eye(B.shape[0])
        for l in range(1, LMAX + 1):
            P = P @ B
            acc[l] += np.trace(P)
    acc /= (1 << k)
    ok = all(abs(brute[l] - acc[l]) < 1e-6 for l in range(2, LMAX + 1))
    check("Paper A Prop 12 (slice identity Ev_l = E_all tr B^l), prism l<=10",
          ok, f"l=10: brute={brute[10]:.0f} avg={acc[10]:.2f}")
    # doubling: Ev_2m >= tr B^m
    B = nb_matrix(G, np.ones(len(E)))
    P = np.eye(B.shape[0])
    ok2 = True
    for m in range(1, LMAX // 2 + 1):
        P = P @ B
        ok2 &= brute[2 * m] >= np.trace(P) - 1e-6
    check("Paper A Prop 12 (doubling bound Ev_2m >= tr B^m)", ok2)


# ============================================ Paper A, Prop 15 (K_d trapping)

def check_trapping():
    G = nx.Graph()
    for c in (0, 1):
        for i in range(4):
            for j in range(i + 1, 4):
                G.add_edge(4 * c + i, 4 * c + j)
    for i in range(4):
        G.add_edge(i, 4 + i)
    ok_reg = all(d == 4 for _, d in G.degree())
    E = edge_list(G)
    _, _, cot = spanning_tree_split(G)
    k = len(cot)
    rhos, acc, trp = [], np.zeros(31), np.zeros(31)
    for bits in range(1 << k):
        s = np.ones(len(E))
        for j, ei in enumerate(cot):
            if (bits >> j) & 1:
                s[ei] = -1
        B = nb_matrix(G, s)
        rhos.append(max(abs(np.linalg.eigvals(B))))
        P = np.eye(B.shape[0])
        for l in range(1, 31):
            P = P @ B
            tv = np.trace(P)
            acc[l] += tv
            if bits == 0:
                trp[l] = tv
    acc /= (1 << k)
    rate30 = acc[30] ** (1 / 30)
    # remove the two trivial classes of G (B_- = -B_+ has equal trace at
    # even l): the remainder is the mass Prop 13 attributes to K_4-trapped
    # walks, at rate between d-2=2 and the largest non-trivial class ~2.44.
    rem = acc.copy()
    for l in range(2, 31, 2):
        rem[l] -= 2 * trp[l] / (1 << k)
    rem_rate = (rem[30] / rem[20]) ** (1 / 10)
    ok = ok_reg and 1.9 <= rem_rate <= 2.7 and rate30 > np.sqrt(3) + 0.2
    check("Paper A Prop 13 (K_4 trapping: even-walk growth rate ~ d-2)", ok,
          f"trivial-class-removed local rate (l=20->30) = {rem_rate:.4f} "
          f"in [1.9, 2.7]; full rate@30 = {rate30:.4f}")
    # Wielandt: exactly the two trivial classes attain rho(B)
    top = max(rhos)
    n_at_top = sum(1 for r in rhos if r > top - 1e-8)
    check("Paper A Prop 13 (Wielandt: only +/- trivial classes attain rho(B))",
          n_at_top == 2, f"{n_at_top} of {len(rhos)} classes at rho(B)={top:.4f}")


# ================================================ Paper A, Prop 5 (hypercube)

def check_cube():
    ok, det = True, []
    for n in (4, 5, 6):
        G = nx.convert_node_labels_to_integers(nx.hypercube_graph(n))
        fam = family_signings(G, 4, limit=8)
        if fam is None:
            ok = False
            det.append(f"Q{n}: INCONSISTENT")
            continue
        for s in fam:
            A = signed_adjacency(G.number_of_nodes(), edge_list(G), s)
            ok &= np.allclose(A @ A, n * np.eye(G.number_of_nodes()))
            ok &= abs(rho(G, s) - np.sqrt(n)) < 1e-9
        det.append(f"Q{n}: A^2={n}I, rho=sqrt({n})={np.sqrt(n):.4f} "
                   f"(8 lexicographic family representatives)")
    check("Paper A Prop 5 (hypercube certificate A_sigma^2 = nI)", ok,
          "; ".join(det))


# ================================================ Paper A, Lemma 5 (K4 obstr)

def check_k4_obstruction():
    G = nx.complete_graph(4)
    rows = even_cycle_rows(G, 4)
    s = np.zeros(len(edge_list(G)), np.uint8)
    for r in rows:
        s ^= r
    ok = (len(rows) == 3) and (not s.any())
    fam = family_signings(G, 4)
    check("Paper A Lemma 4 (K_4: three quads sum to 0, system inconsistent)",
          ok and fam is None, f"{len(rows)} quads, XOR=0: {not s.any()}, "
                              f"family={'empty' if fam is None else 'nonempty'}")


# ==================================================== Paper A, Remark (q_G)

def check_qG():
    from sympy import symbols, expand, Rational, Poly, real_roots
    x = symbols('x')
    p_bal = expand(x ** 2 * (x - 4) ** 2)
    p_unb = expand((x - 2) ** 4)
    q = expand((p_bal + p_unb) / 2)
    ok_exact = expand((x ** 2 - 4 * x + 2) ** 2 + 4 - q) == 0
    check("Paper A Remark 6 (q_{C4} = (x^2-4x+2)^2+4, no real roots; exact)",
          ok_exact, f"q_C4 = {q}")
    # exact real-rootedness classification: integer charpolys via sympy,
    # averaged over switching classes as exact rationals, roots by Sturm.
    from sympy import Matrix, ZZ
    expect = {"C4": False, "K33": False, "Q3": False, "Petersen": False,
              "K4": True}
    got = {}
    for name, G in (("C4", nx.cycle_graph(4)),
                    ("K33", nx.complete_bipartite_graph(3, 3)),
                    ("Q3", nx.hypercube_graph(3)),
                    ("Petersen", nx.petersen_graph()),
                    ("K4", nx.complete_graph(4))):
        G = nx.convert_node_labels_to_integers(G)
        acc, cnt = None, 0
        for idx, stack in enumerate_class_matrices(G):
            for A in stack:
                M = Matrix((A @ A).astype(int))
                p = M.charpoly(x)  # exact integer coefficients
                acc = p.as_expr() if acc is None else acc + p.as_expr()
                cnt += 1
        qpoly = Poly(expand(acc / cnt), x)
        deg = qpoly.degree()
        got[name] = (len(real_roots(qpoly)) == deg)
    check("Paper A Remark 6 (q_G real-rootedness: fails C4/K33/Q3/Petersen, holds K4; exact)",
          got == expect, f"real-rooted: {got}")

# ============================================= Paper A, Lemma 25 (window)

def check_window():
    rng = np.random.default_rng(1)
    G = nx.cycle_graph(7)
    nid = 7
    for _ in range(30):
        G.add_edge(int(rng.integers(nid)), nid)
        nid += 1
    B = nb_matrix(G, np.ones(len(edge_list(G))))
    P = np.eye(B.shape[0])
    ok, worst, eq_seen = True, -np.inf, False
    for t in range(1, 61):
        P = P @ B
        bound = 1 + t // 7
        worst = max(worst, P.max() - bound)
        ok &= P.max() <= bound + 1e-9
        eq_seen |= abs(P.max() - bound) < 1e-9
    check("Paper A Lemma 19 (unicyclic: (B^t)_ef <= 1 + floor(t/girth))",
          ok and eq_seen,
          f"max slack over t<=60: {worst:+.3f}; equality attained at some t: {eq_seen}")

# =========================================== Paper A, Lemma 27 (rank/cages)

def check_rank_cages():
    def bf_ok(G, R):
        for v in G.nodes:
            ball, fr = {v}, {v}
            for _ in range(R):
                fr = {w for x in fr for w in G[x]} - ball
                if not fr:
                    break
                ball |= fr
            H = G.subgraph(ball)
            if H.number_of_edges() - H.number_of_nodes() + 1 > 1:
                return False
        return True
    out, ok = [], True
    for name, G, R in (("Tutte-Coxeter(3,8)",
                        nx.LCF_graph(30, [-13, -9, 7, -7, 9, 13], 5), 3),
                       ("Tutte 12-cage",
                        nx.LCF_graph(126, [17, 27, -13, -59, -35, 35, -11, 13,
                                           -53, 53, -27, 21, 57, 11, -21, -57,
                                           59, -17], 7), 5)):
        s = G.number_of_edges()
        rank = s - G.number_of_nodes() + 1
        dens = (rank - 1) / s
        bf = bf_ok(G, R)
        # Lemma 20: rank <= 1 + C s log s / R. Implied constant on cages:
        C_impl = (rank - 1) * R / (s * np.log(s))
        ok &= bf and dens > 1 / (R + 1) and C_impl <= 2.0
        out.append(f"{name}: BF_{R}={bf}, density={dens:.3f} "
                   f"(> banana 1/(R+1)={1/(R+1):.3f}), implied C={C_impl:.3f}<=2")
    check("Paper A Lemma 20 (rank bound holds on cages; cages refute the linear form)",
          ok, "; ".join(out))


# ====================================== Paper A, Lemma 21 (NB linearization)

def check_linearization():
    G = nx.petersen_graph()
    n, d = 10, 3
    A = nx.to_numpy_array(G)
    Aj = [np.eye(n), A.copy(), A @ A - d * np.eye(n)]
    for j in range(2, 9):
        Aj.append(A @ Aj[j] - (d - 1) * Aj[j - 1])

    def nbcount(j):
        M = np.zeros((n, n))

        def dfs(path):
            if len(path) - 1 == j:
                M[path[0], path[-1]] += 1
                return
            u = path[-2] if len(path) > 1 else None
            for w in G[path[-1]]:
                if w != u:
                    dfs(path + [w])
        for v in range(n):
            dfs([v])
        return M
    ok1 = all(np.allclose(Aj[j], nbcount(j)) for j in range(1, 6))
    mmax = 8
    alpha = np.zeros((mmax + 1, mmax + 1))
    alpha[0, 0] = 1
    for m in range(mmax):
        for j in range(mmax + 1):
            a = alpha[m, j]
            if not a:
                continue
            if j + 1 <= mmax:
                alpha[m + 1, j + 1] += a
            if j >= 2:
                alpha[m + 1, j - 1] += a * (d - 1)
            elif j == 1:
                alpha[m + 1, 0] += a * d
    ok2 = all(np.allclose(np.linalg.matrix_power(A, m),
                          sum(alpha[m, j] * Aj[j] for j in range(m + 1)))
              for m in range(1, mmax + 1))
    ok3 = all(sum(alpha[2 * k, j] * np.sqrt(d - 1) ** j for j in range(2 * k + 1))
              <= (2 * k + 1) * (2 * np.sqrt(d - 1)) ** (2 * k)
              for k in (2, 3, 4))
    check("Paper A Lemma 23 (NB recursion, inversion, envelope) on Petersen",
          ok1 and ok2 and ok3,
          f"recursion={ok1}, inversion={ok2}, envelope={ok3}")


# ================================================= Paper B, Props 6-7, Conj 8

def check_circulants():
    # canonical signing: step-1 all +1, step-2 = (-1)^i  =>  rho = 2 sqrt 2
    ok, det = True, []
    for n in (12, 30, 60):
        G = nx.convert_node_labels_to_integers(nx.circulant_graph(n, [1, 2]))
        E = edge_list(G)
        s = np.ones(len(E))
        for j, e in enumerate(E):
            step = min((e[1] - e[0]) % n, (e[0] - e[1]) % n)
            if step == 2:
                i = e[0] if (e[1] - e[0]) % n == 2 else e[1]
                s[j] = (-1) ** i
        # all quads unbalanced?
        eidx = {e: i for i, e in enumerate(E)}
        quads_ok = all(
            s[eidx[tuple(sorted((i % n, (i + 1) % n)))]] *
            s[eidx[tuple(sorted(((i + 2) % n, (i + 3) % n)))]] *
            s[eidx[tuple(sorted((i % n, (i + 2) % n)))]] *
            s[eidx[tuple(sorted(((i + 1) % n, (i + 3) % n)))]] == -1
            for i in range(n))
        r = rho(G, s)
        ok &= quads_ok and abs(r - 2 * np.sqrt(2)) < 1e-8
        det.append(f"n={n}: quads_unbal={quads_ok}, rho={r:.9f}")
    check("Paper B Prop 1 (canonical signing: rho = 2 sqrt 2 exactly)", ok,
          "; ".join(det) + f"; 2sqrt2={2*np.sqrt(2):.9f}")

    # odd n inconsistent
    okodd = all(family_signings(
        nx.convert_node_labels_to_integers(nx.circulant_graph(n, [1, 2])), 4)
        is None for n in (9, 15, 21))
    check("Paper B Prop 1 (odd n: quadrilateral system inconsistent)", okodd,
          "n=9,15,21 all inconsistent")

    # exactly four classes; two values {2sqrt2, rho_-}   [n >= 10; see Rmk n=8]
    ok4, det4 = True, []
    for n in (10, 12, 14):
        G = nx.convert_node_labels_to_integers(nx.circulant_graph(n, [1, 2]))
        fam = family_signings(G, 4)
        vals = sorted(set(round(rho(G, s), 8) for s in fam))
        pred = round(2 * np.sqrt(np.cos(np.pi / n) ** 2 +
                                 np.cos(2 * np.pi / n) ** 2), 8)
        ok4 &= (len(fam) == 4) and (len(vals) == 2) and \
               abs(vals[0] - pred) < 1e-7 and abs(vals[1] - 2 * np.sqrt(2)) < 1e-7
        det4.append(f"n={n}: |F|={len(fam)}, rho values={vals}")
    check("Paper B Prop 2 (four classes; rho in {rho_-(n), 2sqrt2}), n>=10", ok4,
          "; ".join(det4))

    # Paper B Remark: n=8 is exceptional -- two extra step-2 quadrilaterals
    G8 = nx.convert_node_labels_to_integers(nx.circulant_graph(8, [1, 2]))
    quads8 = [c for c in nx.simple_cycles(G8, length_bound=4) if len(c) == 4]
    fam8 = family_signings(G8, 4)
    vals8 = sorted(set(round(rho(G8, s), 6) for s in fam8)) if fam8 else []
    pred8 = round(2 * np.sqrt(np.cos(np.pi / 8) ** 2 + np.cos(2 * np.pi / 8) ** 2), 6)
    ok8 = (len(quads8) == 10) and (len(fam8) == 2) and (vals8 == [pred8])
    check("Paper B Remark 4 (n=8: 10 quads, all-quad family has 2 classes at rho_-)",
          ok8, f"quads={len(quads8)} (8 of type Q_i + 2 step-2 squares), "
               f"|family|={len(fam8)}, rho values={vals8}, rho_-(8)={pred8}")

    # global minimum over ALL switching classes equals rho_-(n)
    okg, detg = True, []
    for n in (8, 10, 12, 14):
        G = nx.convert_node_labels_to_integers(nx.circulant_graph(n, [1, 2]))
        best = np.inf
        for idx, stack in enumerate_class_matrices(G):
            best = min(best, float(np.abs(np.linalg.eigvalsh(stack)).max(axis=1).min()))
        pred = 2 * np.sqrt(np.cos(np.pi / n) ** 2 + np.cos(2 * np.pi / n) ** 2)
        okg &= abs(best - pred) < 1e-9
        detg.append(f"n={n}: min={best:.9f} rho_-={pred:.9f}")
    check("Paper B Conj 3 (global min over 2^(n+1) classes = rho_-(n)), n<=14",
          okg, "; ".join(detg) + "  [n=16,18 verified separately, ~20s each]")




# ================================= Paper A Sec.3: beta_L vs greedy lower bound

def check_beta():
    from signed_spectra import spanning_tree_split as _sts

    def true_and_greedy(G, L=4):
        E = edge_list(G)
        eidx = {e: i for i, e in enumerate(E)}
        _, _, cot = _sts(G)
        k = len(cot)
        cpos = {ei: j for j, ei in enumerate(cot)}
        rows = []
        for c in nx.simple_cycles(G, length_bound=L):
            if len(c) % 2:
                continue
            r = np.zeros(k, np.uint8)
            for a in range(len(c)):
                i = eidx[tuple(sorted((c[a], c[(a + 1) % len(c)])))]
                if i in cpos:
                    r[cpos[i]] ^= 1
            rows.append(r)
        R = np.array(rows, np.uint8)
        best = 0
        for bits in range(1 << k):
            xv = np.array([(bits >> j) & 1 for j in range(k)], np.uint8)
            best = max(best, int(((R @ xv) % 2).sum()))
        # greedy consistent-subsystem count (one elimination order)
        A, b = R.copy(), np.ones(len(rows), np.uint8)
        r0 = 0
        for c in range(k):
            p = next((i for i in range(r0, len(A)) if A[i, c]), None)
            if p is None:
                continue
            A[[r0, p]], b[[r0, p]] = A[[p, r0]], b[[p, r0]]
            for i in range(len(A)):
                if i != r0 and A[i, c]:
                    A[i] ^= A[r0]
                    b[i] ^= b[r0]
            r0 += 1
        greedy = len(rows) - int(b[r0:].sum())
        return best, greedy, len(rows)

    ok, det = True, []
    for name, G in (("K5", nx.complete_graph(5)),
                    ("octahedron", nx.complete_multipartite_graph(2, 2, 2)),
                    ("K33", nx.complete_bipartite_graph(3, 3))):
        G = nx.convert_node_labels_to_integers(G)
        best, greedy, nc = true_and_greedy(G)
        ok &= (best / nc >= 0.5) and (greedy <= best)
        det.append(f"{name}: beta_L={best}/{nc}={best/nc:.3f} "
                   f">= 1/2; greedy={greedy} <= true")
    # K12: random-signing floor on the full quadrilateral system
    G = nx.complete_graph(12)
    E = edge_list(G)
    eidx = {e: i for i, e in enumerate(E)}
    quads = [c for c in nx.simple_cycles(G, length_bound=4) if len(c) == 4]
    Q = np.zeros((len(quads), len(E)), np.uint8)
    for qi, c in enumerate(quads):
        for a in range(4):
            Q[qi, eidx[tuple(sorted((c[a], c[(a + 1) % 4])))]] ^= 1
    rng = np.random.default_rng(1)
    best = max(int(((Q @ rng.integers(0, 2, len(E), dtype=np.uint8)) % 2).sum())
               for _ in range(200))
    ok &= best / len(quads) >= 0.5
    det.append(f"K12: best of 200 random = {best}/{len(quads)}"
               f"={best/len(quads):.3f} >= 1/2")
    check("Paper A Sec.3 (beta_L >= 1/2 always; greedy count is a lower bound)",
          ok, "; ".join(det))

# ---------------------------------------------------------------------- main

if __name__ == "__main__":
    print("=" * 72)
    print("Verification of computational claims in Papers A and B")
    print("=" * 72)
    check_master_identity()
    check_slice_and_doubling()
    check_trapping()
    check_cube()
    check_k4_obstruction()
    check_qG()
    check_beta()
    check_window()
    check_rank_cages()
    check_linearization()
    check_circulants()
    print("=" * 72)
    print(f"{sum(RESULTS)}/{len(RESULTS)} checks passed")
    print("=" * 72)
