import numpy as np, networkx as nx
from signed_spectra import compare_strategies

rng = np.random.default_rng(7)
def show(r, extra=""):
    print(f"{r['name']:12s} n={r['n']:3d} d={r['d']} L={r['L']} floor={r['floor']:.3f} "
          f"unsigned={r['unsigned']:.3f} | sat {r['satisfied']}/{r['constraints']} | "
          f"rand best/mean {r['rand_best']:.3f}/{r['rand_mean']:.3f} | "
          f"unb best/mean {r['unb_best']:.3f}/{r['unb_mean']:.3f} | "
          f"rand+LS {r.get('rand+LS',float('nan')):.3f} unb+LS {r.get('unb+LS',float('nan')):.3f} {extra}", flush=True)

configs = [
 ("Q5", nx.hypercube_graph(5), 4, True, "target sqrt5=2.236"),
 ("Q6", nx.hypercube_graph(6), 4, True, "target sqrt6=2.449"),
 ("C30(1,2)", nx.circulant_graph(30,[1,2]), 4, True, "quad (parity) family"),
 ("C30(1,2)L3all", nx.circulant_graph(30,[1,2]), 3, False, "ALL cycles<=3: triangles forced"),
 ("C60(1,2)", nx.circulant_graph(60,[1,2]), 4, True, "quad (parity) family"),
 ("C30(1,2,3)", nx.circulant_graph(30,[1,2,3]), 4, True, ""),
 ("K12", nx.complete_graph(12), 4, True, "conference-ish target ~sqrt11=3.317"),
 ("rand3reg60", nx.random_regular_graph(3,60,seed=1), 6, True, "MOP regime control"),
]
for name,G,L,eo,extra in configs:
    G = nx.convert_node_labels_to_integers(G)
    r = compare_strategies(G, name, L, n_rand=60, n_unb=60, ls=True, rng=rng,
                           even_only=eo)
    show(r, extra)
