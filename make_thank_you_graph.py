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
        tokens = data["tokens"]
        tokes = frozenset([lmtzr.lemmatize(w.lower()) for w in tokens])
        if tokes & {"thanks", "thx", "thnx", "thank you", "ty", "thank"}:
            #print tokens
            H.add_edge(u,v, tokens = tokens)

    f = file ("thank_you_multidigraph.pkl", "w")
    pickle.dump(H,f)
    f.close ()

if __name__ == "__main__":
    main()

    
        

