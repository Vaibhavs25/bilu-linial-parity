"""Exact verification of the kernel-averaged L-identity (Paper A, Prop 10)
on the prism: enumerates prime non-backtracking cycle classes to |p| <= 14,
identifies the parity-confined ones (z(p) in W), and checks both the
coefficient form (E_F tr B^k = Euler RHS for all k <= 14) and the log-det
form at u = 0.2. Restored from the research transcript; runtime ~1 min."""
import numpy as np
import networkx as nx
from variance_onset import CycleSystem
from signed_spectra import edge_list

LMAX = 14

G = nx.convert_node_labels_to_integers(
    nx.cartesian_product(nx.cycle_graph(3), nx.complete_graph(2)))
n, E = G.number_of_nodes(), edge_list(G)
m = len(E)
eidx = {e: i for i, e in enumerate(E)}
cs = CycleSystem(G, 4)
print(f"prism: n={n} m={m} ncon={cs.ncon} nsat={cs.nsat} "
      f"kdim={len(cs.free)} -> family size {1 << len(cs.free)}")

dedges = [(u, v) for u, v in E] + [(v, u) for u, v in E]
di = {e: i for i, e in enumerate(dedges)}

def Bmat(signs):
    B = np.zeros((2 * m, 2 * m))
    for i, (u, v) in enumerate(dedges):
        for w in G[v]:
            if w == u:
                continue
            B[i, di[(v, w)]] = signs[eidx[tuple(sorted((v, w)))]]
    return B

fam = [cs.solution(np.array([t], dtype=np.uint8)) for t in (0, 1)]
Bs = [Bmat(s) for s in fam]
Bu = Bmat(np.ones(m))

# ---- enumerate prime classes (primitive cyclic classes of closed NB walks)
primes = []
seen = set()

def rotations(w):
    return [tuple(w[i:] + w[:i]) for i in range(len(w))]

def dfs(walk, first):
    l = len(walk)
    u, v = walk[-1]
    if l <= LMAX and v == first[0] and l >= 2 and walk[-1] != (first[1], first[0]):
        if (u, v) != (first[1], first[0]):
            w = tuple(walk)
            r = min(rotations(list(w)))
            if r == w and r not in seen:
                prim = True
                for d in range(1, l):
                    if l % d == 0 and w == tuple(list(w[:d]) * (l // d)):
                        prim = False
                        break
                if prim:
                    seen.add(r)
                    primes.append((l, list(w)))
    if l == LMAX:
        return
    for w2 in G[v]:
        if w2 == u:
            continue
        dfs(walk + [(v, w2)], first)

for e in dedges:
    dfs([e], e)

# internal Bass check on the unsigned operator
Pk = {}
for l, w in primes:
    Pk[l] = Pk.get(l, 0) + 1
ok = True
Buk = np.eye(2 * m)
for k in range(1, LMAX + 1):
    Buk = Buk @ Bu
    lhs = np.trace(Buk)
    rhs = sum(d * Pk.get(d, 0) for d in range(1, k + 1) if k % d == 0)
    ok &= abs(lhs - rhs) < 1e-6
print(f"primes<={LMAX}: {len(primes)}; Euler-product internal check (unsigned): {ok}")
assert ok

# ---- W membership (z(p) in span of even cycles <= 4) and frozen sign
Wrows = []
for c in nx.simple_cycles(G, length_bound=4):
    if len(c) % 2:
        continue
    r = np.zeros(m, dtype=np.uint8)
    for a in range(len(c)):
        r[eidx[tuple(sorted((c[a], c[(a + 1) % len(c)])))]] ^= 1
    Wrows.append(r)
Wm = np.array(Wrows)

def solveGF2(Amat, b):
    A = np.concatenate([Amat.T, b[:, None]], axis=1).astype(np.uint8)
    rr, piv = 0, []
    for c in range(A.shape[1] - 1):
        p = next((i for i in range(rr, A.shape[0]) if A[i, c]), None)
        if p is None:
            continue
        A[[rr, p]] = A[[p, rr]]
        for i in range(A.shape[0]):
            if i != rr and A[i, c]:
                A[i] ^= A[rr]
        piv.append(c)
        rr += 1
    for i in range(rr, A.shape[0]):
        if A[i, -1]:
            return None
    x = np.zeros(A.shape[1] - 1, dtype=np.uint8)
    for i, c in enumerate(piv):
        x[c] = A[i, -1]
    return x

def zvec(walk):
    z = np.zeros(m, dtype=np.uint8)
    for (u, v) in walk:
        z[eidx[tuple(sorted((u, v)))]] ^= 1
    return z

frozen = []
for l, w in primes:
    x = solveGF2(Wm, zvec(w))
    if x is not None:
        frozen.append((l, int(x.sum()) % 2, w))
bylen = {l: sum(1 for a, b, c in frozen if a == l)
         for l in sorted(set(a for a, b, c in frozen))}
print(f"parity-confined primes (z in W) up to {LMAX}: {len(frozen)}  by length: {bylen}")

# ---- coefficient form: E_F tr B^k == Euler RHS for all k
Bks = [np.eye(2 * m) for _ in Bs]
allok = True
for k in range(1, LMAX + 1):
    for i in range(2):
        Bks[i] = Bks[i] @ Bs[i]
    lhs = np.mean([np.trace(X) for X in Bks])
    rhs = 0.0
    for l, w in primes:
        if k % l == 0 and (k // l) % 2 == 0:
            rhs += l
    for l, par, w in frozen:
        if k % l == 0 and (k // l) % 2 == 1:
            rhs += l * ((-1) ** par)
    match = abs(lhs - rhs) < 1e-6
    allok &= match
    print(f"k={k:2d}  E_fam tr B^k = {lhs:12.4f}   Euler RHS = {rhs:12.4f}   match={match}")
assert allok

# ---- log-det form at u = 0.2 (truncated at |p| <= LMAX)
u = 0.2
lhs = np.mean([np.log(abs(np.linalg.det(np.eye(2 * m) - u * X))) for X in Bs])
rhs = 0.5 * np.log(abs(np.linalg.det(np.eye(2 * m) - u * u * Bu)))
for l, par, w in frozen:
    eps = (-1) ** par
    rhs -= 0.5 * np.log((1 + eps * u ** l) / (1 - eps * u ** l))
print(f"\nlog-det identity at u={u}: LHS={lhs:.8f} RHS={rhs:.8f} "
      f"(truncation at L={LMAX}; |u(d-1)|^{LMAX}~{(u * 2) ** LMAX:.1e})")
assert abs(lhs - rhs) < 1e-6
print("prism_L: ALL CHECKS PASS")
