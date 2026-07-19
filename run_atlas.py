import time, csv, numpy as np, networkx as nx
from signed_spectra import defect_atlas_entry

graphs = []
# exhaustive: all connected regular graphs, 3<=n<=7 (networkx atlas)
for G in nx.graph_atlas_g()[1:]:
    n = G.number_of_nodes()
    if n < 3 or not nx.is_connected(G): continue
    degs = set(d for _, d in G.degree())
    if len(degs) == 1 and degs.pop() >= 2:
        d = G.degree(0); m = G.number_of_edges()
        graphs.append((f"reg{n}_{d}_{m}_{len(graphs)}", G))
# structured set
S = {"Petersen": nx.petersen_graph(), "Q3": nx.hypercube_graph(3),
     "Q4": nx.hypercube_graph(4), "Heawood": nx.heawood_graph(),
     "MobiusKantor": nx.moebius_kantor_graph(),
     "C8(1,2)": nx.circulant_graph(8,[1,2]),
     "C10(1,2)": nx.circulant_graph(10,[1,2]),
     "C12(1,2)": nx.circulant_graph(12,[1,2])}
for k,v in S.items(): graphs.append((k, nx.convert_node_labels_to_integers(v)))

rows=[]
for name,G in graphs:
    t=time.time()
    e = defect_atlas_entry(G,name)
    e["sec"]=round(time.time()-t,1)
    rows.append(e)
    print(f"{name:14s} n={e['n']:2d} d={e['d']} g={e['girth']} k={e['k']:2d} "
          f"minrho={e['min_rho']:.4f} floor={e['floor']:.4f} "
          f"delta={e['defect']:+.4f} P(rho<floor)={e['frac_below_floor']:.2f} "
          f"opt cyc unb {e['cycle_profile']}", flush=True)
with open("atlas.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader()
    for r in rows: w.writerow(r)
print("done", len(rows))
