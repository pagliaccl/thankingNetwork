import json
import networkx as nx
import pickle
import sys

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

J = nx.Graph ()
H = nx.Graph ()
I = nx.Graph()
G = nx.Graph()
names = dict()
invnames = dict()
def main ():
    global J
    global I
    global H
    global G
    global names
    global central
    global helpers
    global mutual
    global recipG
    global errs
    global keepers

    f = open("thank_you_no_onesies.pkl")
    J = pickle.load(f)
    f.close()
    
    f = open("thank_you_no_binaries.pkl")
    I = pickle.load(f)
    f.close()

    f = open("thank_you_graph.pkl")
    H = pickle.load(f)
    f.close()
    
    f = open("at_graph.pkl")
    G = pickle.load(f)
    f.close()

    central = set(J.nodes())
    helpers = set(I.nodes())
    mutual = set(H.nodes())
    recipG = set(G.nodes())
    errs = set()
    keepers = set()
    
    f = file ("masterfile.csv")
    g = file ("master_3.csv", "w")
    line = f.readline()
    headers = line.split(",")
    ind = dict()
    for i in range(0,len(headers)):
        ind[headers[i]] = i
    while True:
        line = f.readline()
        if line == "":
            break
        values = line.split(",")
        #print ind["screen_name"]
        #print line
        name = values[ind["screen_name"]]
        if name in recipG:
            values[ind["R"]] = "1"
            keepers.add(name)
        else:
            errs.add(name)
            values[ind["R"]] = "0"
        if name in recipG - mutual:
            values[ind["RXM"]] = "1"
        else:
            values[ind["RXM"]] = "0"
        if name in mutual:
            values[ind["M"]] = "1"
        else:
            values[ind["M"]] = "0"
        if name in helpers:
            values[ind["XBIN"]] = "1"
        else:
            values[ind["XBIN"]] = "0"
        if name in mutual - helpers:
            values[ind["BIN"]] = "1"
        else:
            values[ind["BIN"]] = "0"
        if name in helpers - central:
            values[ind["TH"]] = "1"
        else:
            values[ind["TH"]] = "0"
        if name in central:
            values[ind["CH"]] = "1"
        else:
            values[ind["CH"]] = "0"
            
        g.write (",".join(values))
    f.close ()
    g.write("\n")
    for name in recipG - keepers:
        R = "1"
        if name in recipG - mutual:
            RXM = "1"
        else:
            RXM = "0"
        if name in mutual:
            M = "1"
        else:
            M = "0"
        if name in helpers:
            XBIN = "1"
        else:
            XBIN = "0"
        if name in mutual - helpers:
            BIN = "1"
        else:
            BIN = "0"
        if name in helpers - central:
            TH = "1"
        else:
            TH = "0"
        if name in central:
            CH = "1"
        else:
            CH = "0"
        g.write (",%s,%s,%s,%s,%s,%s,%s,%s,,,,,,,,,\n" % (name,R,RXM,M,XBIN,BIN,TH,CH))
        
    g.close ()
    
    '''
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
    '''
   
if __name__ == "__main__":
    main()
