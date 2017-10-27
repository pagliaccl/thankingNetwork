import pickle
import networkx as nx

I = nx.DiGraph ()
J = nx.Graph ()

def main():
    f = open("thank_you_digraph.pkl")
    I = pickle.load(f)
    f.close()

    f = open("thank_you_graph.pkl")
    J = pickle.load(f)
    f.close()

    print len(J)

    for node in J.nodes():
        if J.degree(node) < 2:
            J.remove_node(node)
            
    nx.write_gexf(I, "thank_you_digraph.gexf")
    nx.write_gexf(J, "thank_you_graph.gexf")
    nx.write_gml(I, "thank_you_digraph.gml")
    nx.write_gml(J, "thank_you_graph.gml")
    print len(J)
    
if __name__ == "__main__":
    main()

