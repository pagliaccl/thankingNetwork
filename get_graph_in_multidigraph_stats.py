import pickle
import sys
import networkx as nx
import itertools

G = nx.MultiDiGraph ()            
H = nx.Graph ()
def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def main ():
    global G
    global H
    f = open(sys.argv[2])
    G = pickle.load(f)
    f.close()

    f = open(sys.argv[1])
    H = pickle.load(f)
    f.close()

    n = len(H)
    m = len(G.edges(H.nodes()))
    link_ave = m /float (n*(n-1))      

    num = 0
    den = 0
    for u in H:
        for v in H:
            num += (G.number_of_edges(u,v) - link_ave) * (G.number_of_edges(v,u) - link_ave)
            den += (G.number_of_edges(u,v) - link_ave) * (G.number_of_edges(u,v) - link_ave) 
    r = num / float(den)

    print ("***** %s in %s ******" % (sys.argv[1],sys.argv[2]))
    print ("|V|: \t%d" % n)
    print ("ave messages: \t%f" % (m/float(n)))
    print ("link ave: \t%f" % link_ave)
    print ("reciprocity: \t%f" % r)
if __name__ == "__main__":
    main()

