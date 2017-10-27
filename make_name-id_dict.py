import sys
import re
import json
import networkx as nx
import pickle
      
def main():
    

    name_id = dict()
    
    # Add nodes in the graph
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        name_id[j["user"]["screen_name"]] = int(j["user"]["id_str"])
    f.close ()

    
    f = file (sys.argv[2], "w")
    
    pickle.dump(name_id, f)

    f.close()
    
if __name__ == "__main__":
    main()
