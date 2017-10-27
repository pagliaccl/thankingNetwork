import pickle
import networkx as nx

G = nx.Graph ()            
H = nx.Graph ()            
I = nx.Graph ()
keepers = set()
#J = nx.Graph ()

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main ():
    f = open("thank_you_graph.pkl")
    G = pickle.load(f)
    f.close()

    for u,v,data in G.edges_iter(data=True):
        if G.degree(u) > 1 or G.degree(v) > 1:
            H.add_edge(u,v,data_dict = data)
    
    for u in H:
        if H.degree(u) > 1:
            keepers.add(u)

    I = H.subgraph(keepers);
        


    dumpit("thank_you_no_binaries.pkl", H)
    dumpit("thank_you_no_onesies.pkl", I)
    
if __name__ == "__main__":
    main()

    

    
