import nltk
import sys
import re
import json
import networkx as nx
import pickle

G = nx.MultiDiGraph()            
H = nx.MultiDiGraph()            
def main():
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    
    f = file (sys.argv[1])
    G = pickle.load(f)
    f.close()

    for u,v,data in G.edges_iter (data=True):
        if G.has_edge(u,v) and G.has_edge(v,u):
            H.add_edge(u,v,attr_dict=data)

    f = file ("at_recip_digraph.pkl", "w")
    pickle.dump(H,f)
    f.close ()

if __name__ == "__main__":
    main()

    
        

