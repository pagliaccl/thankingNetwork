# Filters twitter json file text field 
# python -OO twep.py TWITTER_FILE REGEX

# usage:
# export PYTHONIOENCODING=utf-8; python twaydar.py TWITTER_USER_FILE

import sys
import re
import json
import pickle

def main():
    
    # Add nodes in the graph
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        if j["user"]["screen_name"] == "miranduhhh_xo" or j["user"]["screen_name"] == "Briannainclema":
            print j["user"]["screen_name"] + "\t" + j["text"]
    f.close ()

    
    
if __name__ == "__main__":
    main()
