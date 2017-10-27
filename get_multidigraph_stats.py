import pickle
import sys
import networkx as nx
import itertools

G = nx.MultiDiGraph ()            

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main ():
    global G
    f = open(sys.argv[1])
    G = pickle.load(f)
    f.close()

    n = len(G)
    m = len(G.edges())
    link_ave = m /float (n*(n-1))      

    num = 0
    den = 0
    for u in G:
        for v in G:
            num += (G.number_of_edges(u,v) - link_ave) * (G.number_of_edges(v,u) - link_ave)
            den += (G.number_of_edges(u,v) - link_ave) * (G.number_of_edges(u,v) - link_ave) 
    r = num / float(den)
    print ("|V|: \t%d" % n)
    print ("|E|: \t%d" % m)
    print ("link ave: \t%f" % link_ave)
    print ("reciprocity: \t%f" % r)
if __name__ == "__main__":
    main()

