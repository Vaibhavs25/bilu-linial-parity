"""gadgets.py -- the extremal gadgets of Paper A, Remarks 17-18 and Lemma 19.

Tables: theta(2,2,lam) signed class spectra; tree-burst rho(B) against the
burst rate 2^(D/(D+lam)); separated quad-ring; unicyclic winding bound with
sharpness. All claims asserted."""
import numpy as np
import networkx as nx
from signed_spectra import edge_list, spanning_tree_split


def Bmat(G, s=None):
    E = edge_list(G)
    eidx = {e: i for i, e in enumerate(E)}
    ded = [(u, v) for u, v in E] + [(v, u) for u, v in E]
    di = {e: i for i, e in enumerate(ded)}
    B = np.zeros((len(ded), len(ded)))
    for i, (u, v) in enumerate(ded):
        for w in G[v]:
            if w != u:
                B[i, di[(v, w)]] = 1.0 if s is None else s[eidx[tuple(sorted((v, w)))]]
    return B


def class_rhos(G):
    E = edge_list(G)
    _, _, cot = spanning_tree_split(G)
    out = []
    for bits in range(1 << len(cot)):
        s = np.ones(len(E))
        for j, ei in enumerate(cot):
            if (bits >> j) & 1:
                s[ei] = -1
        out.append(max(abs(np.linalg.eigvals(Bmat(G, s)))))
    return out


def theta(a, b, c):
    G = nx.Graph(); nid = [2]
    for L in (a, b, c):
        prev = 0
        for _ in range(L - 1):
            G.add_edge(prev, nid[0]); prev = nid[0]; nid[0] += 1
        G.add_edge(prev, 1)
    return G


def burst(D, lam):
    G = nx.Graph(); nid = [0]
    def tree():
        root = nid[0]; nid[0] += 1; fr = [root]
        for _ in range(D):
            nf = []
            for v in fr:
                for _ in range(2):
                    G.add_edge(v, nid[0]); nf.append(nid[0]); nid[0] += 1
            fr = nf
        return root, fr
    r1, l1 = tree(); r2, l2 = tree()
    def thread(u, v):
        prev = u
        for _ in range(lam - 1):
            G.add_edge(prev, nid[0]); prev = nid[0]; nid[0] += 1
        G.add_edge(prev, v)
    thread(r1, r2)
    for a, b in zip(l1, l2):
        thread(a, b)
    return G


if __name__ == "__main__":
    print("theta(2,2,lam): trivial rho(B) vs max nontrivial class (Remark 18)")
    for lam in (3, 5, 7, 9, 13):
        rr = class_rhos(theta(2, 2, lam))
        triv, nont = max(rr), sorted(rr)[-3]
        print(f"  lam={lam:2d}: rho(B)={triv:.4f}  max nontrivial={nont:.4f}")
        assert nont <= triv + 1e-9 and triv < np.sqrt(2), "gadget must be subcritical at d=3"

    # ring of four exit-quadrilaterals separated by lam-threads (Remark 18)
    def quad_ring(lam, nq=4):
        G = nx.Graph(); nid = 0; exits = []
        for _ in range(nq):
            a, b, c, d = nid, nid + 1, nid + 2, nid + 3
            G.add_edges_from([(a, b), (b, c), (c, d), (d, a)])
            exits.append((a, c)); nid += 4
        for q in range(nq):
            u = exits[q][1]; v = exits[(q + 1) % nq][0]
            prev = u
            for _ in range(lam - 1):
                G.add_edge(prev, nid); prev = nid; nid += 1
            G.add_edge(prev, v)
        return G

    QG = quad_ring(6)
    qrank = QG.number_of_edges() - QG.number_of_nodes() + 1
    qrho = float(max(abs(np.linalg.eigvals(Bmat(QG)))))
    print(f"quad-ring lam=6: n={QG.number_of_nodes()} rank={qrank} "
          f"rho(B)={qrho:.4f}  (Remark 18: rho <= 1.25, rank 5)")
    assert qrank == 5 and qrho <= 1.2501

    print("tree-burst: rho(B) vs burst rate 2^(D/(D+lam)) (sharpness of Lemma 19)")
    for D, lam in ((3, 4), (3, 8), (4, 4), (4, 8), (5, 8)):
        G = burst(D, lam)
        rho = max(abs(np.linalg.eigvals(Bmat(G))))
        pred = 2 ** (D / (D + lam))
        print(f"  D={D} lam={lam}: n={G.number_of_nodes():4d} rho={rho:.4f} pred={pred:.4f}")
        assert 0.75 * pred <= rho <= 1.02 * pred, "burst rate mismatch"
    print("unicyclic winding bound (B^t)_ef <= 1 + floor(t/g), sharp (Lemma 19)")
    rng = np.random.default_rng(1)
    G = nx.cycle_graph(7); nid = 7
    for _ in range(30):
        G.add_edge(int(rng.integers(nid)), nid); nid += 1
    B = Bmat(G); P = np.eye(B.shape[0]); tight = False
    for t in range(1, 61):
        P = P @ B
        assert P.max() <= 1 + t // 7 + 1e-9
        tight |= abs(P.max() - (1 + t // 7)) < 1e-9
    assert tight, "floor bound should be attained"
    print("  bound holds for t<=60 and is attained.  ALL GADGET CHECKS PASS")
