# Filters twitter json file text field 
# python -OO twep.py TWITTER_FILE REGEX

# usage:
# export PYTHONIOENCODING=utf-8; python twaydar.py TWITTER_USER_FILE

import nltk
import sys
import re
import json
import networkx as nx
import pickle
import tweetokenize

G = nx.MultiDiGraph()            
def main():
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    
    # Add nodes in the graph
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        G.add_node(j["user"]["screen_name"])
    f.close ()

    # Add a multi-edge for each @
    f = file (sys.argv[1])
    #gettokens = tweetokenize.Tokenizer()
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        
        tokens = nltk.word_tokenize(j["text"].encode('ascii', 'ignore') )
        #tokens = gettokens.tokenize(j["text"])
        #tokens = [lmtzr.lemmatize(w.lower()) for w in tokens]
        #tokes = frozenset([lmtzr.lemmatize(w.lower()) for w in tokens])
        #if tokens & frozenset({"homosexual", "homo", "lesbian", "dike", "gay"}):
        for i, x in enumerate(tokens):
            try:
                if x == "@":
                    from_user = j["user"]["screen_name"]
                    to_user = tokens[i+1]
                    if to_user in G and from_user in G and to_user != from_user:
                        G.add_edge (from_user, to_user, tokens = tokens)
                    if from_user == "KatieKruppner" and to_user == "TayyyJayyy":
                        print j["text"]
                #print j["user"]["screen_name"] + " " + tokens[i+1]
            except IndexError:
                pass
        
    f.close()

    f = file ("at_multidigraph.pkl", "w")
    
    pickle.dump(G, f)

    f.close()
    
if __name__ == "__main__":
    main()
