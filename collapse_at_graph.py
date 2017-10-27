import pickle
import networkx as nx

G = nx.MultiDiGraph ()            
H = nx.MultiDiGraph ()            
I = nx.DiGraph ()
J = nx.Graph ()

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main ():
    f = open("at_multidigraph.pkl")
    H = pickle.load(f)
    f.close()

    for u,v in H.edges_iter():
        if I.has_edge(u,v):
            I[u][v]["weight"] = I[u][v]["weight"] + 1
        else:
            I.add_edge(u,v, weight = 1)
    
    for u,v in I.edges_iter():
        if I.has_edge(u,v) and I.has_edge(v,u):
            J.add_edge(u,v, weight=min(I[u][v]["weight"], I[v][u]["weight"]))


    dumpit("at_digraph.pkl", I)
    dumpit("at_graph.pkl", J)
    
if __name__ == "__main__":
    main()

    

    
