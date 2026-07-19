import numpy as np, networkx as nx
from signed_spectra import qG_verdict
from fractions import Fraction

tests = []
for G in nx.graph_atlas_g()[1:]:
    n=G.number_of_nodes()
    if n<3 or n>7 or not nx.is_connected(G): continue
    degs=set(d for _,d in G.degree())
    if len(degs)==1 and degs.pop()>=2: tests.append((f"reg{n}_{G.degree(0)}_{G.number_of_edges()}",G))
tests += [("Petersen", nx.petersen_graph()), ("Q3", nx.convert_node_labels_to_integers(nx.hypercube_graph(3))),
          ("K33", nx.complete_bipartite_graph(3,3))]
print(f"{'graph':12s} {'d':>2s} {'real-rooted':>11s} {'max|Im|':>9s} {'maxRe':>8s} {'4(d-1)':>7s}")
for name,G in tests:
    v = qG_verdict(nx.convert_node_labels_to_integers(G), name)
    print(f"{name:12s} {v['d']:2d} {str(v['real_rooted']):>11s} {v['max_im']:9.4f} "
          f"{v['max_real_part']:8.4f} {v['bound_4dm1']:7d}", flush=True)

# exact hand-check C4: q = x^4 -8x^3 +20x^2 -16x +8 = (x^2-4x+2)^2 + 4 > 0
from sympy import symbols, Poly, expand
x = symbols('x')
p_bal = expand(x**2*(x-4)**2); p_unb = expand((x-2)**4)
q = expand((p_bal+p_unb)/2)
print("\nC4 exact: q =", q, " == (x^2-4x+2)^2+4:", expand((x**2-4*x+2)**2+4-q)==0)
