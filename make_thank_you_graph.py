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
        if tokes & {"blessed","#blessed","bless up","major key","much love","#muchlove","props","respect","gives me life","give me life","preach","#preach","real mvp","shoutout","OG","S/O","keep it real","keeps it real","is the bomb","is the man","is the shit","lit","\u0001f64f","\u0001f64c","\u0001f511","\u0001f525","\u00002467","\u0001f4a3","\u0001f44d","\u0001f4af"}:
            #print tokens
            H.add_edge(u,v, tokens = tokens)

    f = file ("thank_you_multidigraph.pkl", "w")
    pickle.dump(H,f)
    f.close ()

if __name__ == "__main__":
    main()

    
        

