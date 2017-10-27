import json
import networkx as nx
import pickle

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

J = nx.Graph ()
H = nx.Graph ()
I = nx.MultiDiGraph()
G = nx.MultiDiGraph()
names = dict()
invnames = dict()
def main ():
    global J
    global I
    global H
    global G
    global names
    f = open("thank_you_graph.pkl")
    J = pickle.load(f)
    f.close()

    f = open("thank_you_multidigraph.pkl")
    I = pickle.load(f)
    f.close()

    f = open("at_multidigraph.pkl")
    G = pickle.load(f)
    f.close()

    f = file ("GRAPHS/mutualitygraph.json")
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        if j["type"] == "edge":
            H.add_edge(j["src"], j["dest"], data_dict=j["properties"]) 
        else:
            names[j["properties"]["name"]] = j["uid"]
            invnames[j["uid"]] = j["properties"]["name"]
       
    f.close ()

    all_tweets = G.out_degree()
    thx_tweets = I.out_degree()

    print ("screen_name, total_tweets, tu_tweets")
    for user in all_tweets:
        if user in thx_tweets:
            tu = thx_tweets[user]
        else:
            tu = 0
        if all_tweets[user] > 0:
            print ("%s, %d, %d" % (user, all_tweets[user], tu))
               
    dumpit("js-helper.pkl", H)

   
if __name__ == "__main__":
    main()
