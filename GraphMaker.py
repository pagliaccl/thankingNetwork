import os
import json
import string
import codecs
import math

# Test Functions

def Shorten(inputName, outputName, linecount):
    out = open(outputName, 'w')
    i = 0
    with open(inputName, 'r') as file:
        for line in file:
            if i <= linecount - 1:
                out.write(line)
            elif i <= linecount:
                out.write(line.rstrip())
            else:
                break
            i += 1


# Helper Functions

def UserFind(tweetJSONname, phraseTEXTname):

    # Constant Program Values
    uservalid = []
    uservalid.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'])
    uservalid.extend(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    wild = '*'
    record = []

    # Build Phrase List
    phrases = []
    with open(phraseTEXTname, 'r') as file:
        for line in file:
            phrases.append(line.rstrip().encode("ascii", "ignore").lower().translate(string.maketrans("",""), ","))
    phrases.append("@*")

    # Primary Logic Loop
    vxr = 1 #DEBUG
    namedict = {}
    with open(tweetJSONname, 'r') as file:
        # For Each Tweet
        for line in file:
            #DEBUG
            if vxr%100 == 0:
                print vxr
            vxr += 1
            #DEBUG
            decoded = json.loads(line.rstrip())
            if "text" in decoded:
                if not namedict.has_key(decoded["user"]["screen_name"].lower()):
                    namedict[decoded["user"]["screen_name"].lower()] = decoded["user"]["id_str"]
                # Get Text Content of Tweet
                textContent = decoded["text"].encode("ascii", "ignore").lower().translate(string.maketrans(" "," "), ",").translate(string.maketrans(" "," "), "*").translate(string.maketrans(" "," "), '"').translate(string.maketrans(" "," "), '\n')
                # Tokenize Text Content
                next = ""
                tokens = []
                for c in textContent:
                    if c == " ":
                        if next != "":
                            tokens.append(next)
                            next = ""
                    else:
                        next += c
                if next != "":
                    tokens.append(next)
                # For Each Phrase
                found = []
                for p in phrases:
                    l = p.split(" ")
                    
                    # Same Number of Words in Phrase as in Tweet
                    if len(l) == len(tokens):
                        y = True
                        # For Each Word "l[x]" (in Phrase) and Corresponding "tval" in Tweet
                        for x in range(len(l)):
                            tval = tokens[x]
                            # If Last Word, Remove Trailing Punctuation
                            if x == len(l) - 1:
                                tval = tokens[x]
                                cond = True
                                while cond:
                                    if len(l[x]) >= len(tval):
                                        cond = False
                                    elif tval[-1] in string.punctuation:
                                        tval = tval[:-1]
                                    else:
                                        cond = False
                            # Only Compare Up To Wildcard in Phrase
                            if wild in l[x]:
                                v = l[x].find(wild)
                                pv = l[x][:v]
                                tv = tval[:v]
                                if pv != tv:
                                    y = False
                                    break
                            elif l[x] != tval:
                                y = False
                                break
                        if y:
                            if p == "@*":
                                uval = "@"
                                for g in tval[1:]:
                                    if g in uservalid:
                                        uval += g
                                    else:
                                        break
                                found.append(uval)
                            else:
                                found.append(p)

                    # More Words in Phrase than in Tweet
                    elif len(l) > len(tokens):
                        continue

                    # Fewer Words in Phrase than in Tweet
                    else:
                        for z in range(len(tokens) - len(l) + 1):
                            toEval = tokens[z:(z+len(l))]
                            y = True
                            for x in range(len(l)):
                                if x != len(l) - 1:
                                    tval = toEval[x]
                                else:
                                    tval = toEval[x]
                                    cond = True
                                    while cond:
                                        if len(l[x]) >= len(tval):
                                            cond = False
                                        elif tval[-1] in string.punctuation:
                                            tval = tval[:-1]
                                        else:
                                            cond = False
                                if wild in l[x]:
                                    v = l[x].find(wild)
                                    pv = l[x][:v]
                                    tv = tval[:v]
                                    if pv != tv:
                                        y = False
                                        break
                                elif l[x] != tval:
                                    y = False
                                    break
                            if y:
                                if p == "@*":
                                    uval = "@"
                                    for g in tval[1:]:
                                        if g in uservalid:
                                            uval += g
                                        else:
                                            break
                                    found.append(uval)
                                else:
                                    found.append(p)
                record.append([textContent, found, decoded['user']['id_str'], decoded['user']['screen_name']])

    master = {}
    for e in record:
        if master.has_key(e[2]):
            master[e[2]].append(e[1])
        else:
            master[e[2]] = [e[3], e[1]]
    #enterprise = open('enterprise', 'w')
    #for key in master:
    #    enterprise.write(str(key) + ": " + str(master[key]) + '\n')

    return [master, namedict]

def MakeCSV(graphJSONname, CSVname):
    out = open(CSVname, 'w')
    master = {}
    with open(graphJSONname, 'r') as file:
        for line in file:
            decoded = json.loads(line.rstrip())
            uid = decoded["uid"]
            name = decoded["name"]
            tweets = decoded["properties"]["tweets"]
            outNUM = len(decoded["outbound"])
            outSTD = 0
            outTHX = 0
            for e in decoded["outbound"]:
                outSTD += int(decoded["outbound"][e]["weight"])
                outTHX += int(decoded["outbound"][e]["times_thanked"])

            for e in decoded["outbound"]:
                if not master.has_key(e):
                    array = ["@", "0", "0", "0", "0", "0", "0", "0"]
                else:
                    array = master[e]
                array[5] = str(int(array[5]) + 1)
                array[6] = str(int(array[6]) + int(decoded["outbound"][e]["weight"]))
                array[7] = str(int(array[6]) + int(decoded["outbound"][e]["times_thanked"]))

            if master.has_key(uid):
                array = master[uid]
            else:
                array = ["@", "0", "0", "0", "0", "0", "0", "0"]
            array[0] = name
            array[1] = tweets
            array[2] = str(outNUM)
            array[3] = str(outSTD)
            array[4] = str(outTHX)
            master[uid] = array
    out.write("UID,Name,Tweets,OutNUM,OutSTD,OutTHX,InNUM,InSTD,InTHX")
    for e in master:
        vect = master[e]
        out.write('\n' + e + ',' + vect[0] + ',' + vect[1] + ',' + vect[2] + ',' + vect[3] + ',' + vect[4] + ',' + vect[5] + ',' + vect[6] + ',' + vect[7])

# Complete Graph Functions

def MakeGraph(linkdata, namebank, graphJSONname):
    graph = open(graphJSONname, 'w')
    first = True
    for key in linkdata:
        value = linkdata[key]
        tweets = value[1:]
        if first:
            construct = ""
            first = False
        else:
            construct = "\n"
        construct += '{"uid": "' + key + '", "name": "' + value[0]
        construct += '", "properties": {"tweets": "' + str(len(tweets)) + '"}'
        outgoing = {}
        for t in tweets:
            if len(tweets) == 0:
                continue
            thx = False
            log = {}
            for s in t:
                if s[0] != '@':
                    thx = True
                else:
                    if not namebank.has_key(s[1:].lower()):
                        continue
                    else:
                        r_uid = namebank[s[1:].lower()]
                        if not log.has_key(r_uid):
                            log[r_uid] = [0, 1]
            if thx:
                for logkey in log:
                    log[logkey] = [1, 1]
            for logkey in log:
                logvalue = log[logkey]
                if outgoing.has_key(logkey):
                    outvalue = outgoing[logkey]
                    outgoing[logkey] = [outvalue[0] + logvalue[0], outvalue[1] + logvalue[1]]
                else:
                    outgoing[logkey] = logvalue
        construct += ', "outbound": {'
        init = True
        for outkey in outgoing:
            if init:
                init = False
            else:
                construct += ', '
            outvalue = outgoing[outkey]
            construct += '"' + outkey + '" : {' + '"weight": "' + str(outvalue[1]) + '", "times_thanked": "' + str(outvalue[0]) + '"}'
        construct += '}}'
        graph.write(construct)

def Gephify(inputJSONname, nodeOutputName, edgeOutputName):
    nodes = open(nodeOutputName, 'w')
    edges = open(edgeOutputName, 'w')
    nodes.write("Id,Label,Tweets")
    edges.write("Source,Target,Label,Type,Weight,TT")
    with open(inputJSONname, 'r') as file:
        for line in file:
            decoded = json.loads(line.rstrip())
            node_Id = decoded["uid"]
            node_Label = decoded["name"]
            node_Tweets = decoded["properties"]["tweets"]
            nodes.write('\n' + node_Id + ',' + node_Label + ',' + node_Tweets)
            edge_Source = decoded["uid"]
            users = []
            for e in decoded["outbound"]:
                users.append(e)
            for u in users:
                edge_Target = u
                edge_Label = node_Id + " to " + edge_Target
                edge_Type = "Directed"
                edge_Weight = decoded["outbound"][u]["weight"]
                edge_TT = decoded["outbound"][u]["times_thanked"]
                edges.write('\n' + edge_Source + ',' + edge_Target + ',' + edge_Label + ',' + edge_Type + ',' + edge_Weight + ',' + edge_TT)

def GraphMaker(inputJSONname, inputWordsName, outputGraphName):
    uout = UserFind(inputJSONname, inputWordsName)
    MakeGraph(uout[0], uout[1], outputGraphName)
    MakeMutualityGraph(uout[0], uout[1], outputGraphName)

# Reciprocity Graph Functions

def MakeReciprocityGraph(graphJSONname, outputJSONname):
    master = {}
    users = {}
    with open(graphJSONname, 'r') as file:
        for line in file:
            decoded = json.loads(line.rstrip())
            for u in decoded["outbound"]:
                if decoded["uid"] != u:
                    master[decoded["uid"] + ':' + u] = [decoded["outbound"][u]["weight"], decoded["outbound"][u]["times_thanked"]]
            users[decoded["uid"]] = [decoded["name"], decoded["properties"]["tweets"]]
    nodes = {}
    edges = {}
    ignore = {}
    for e in master:
        x = e.split(':')
        f = x[1] + ':' + x[0]
        if not master.has_key(f):
            continue
        elif ignore.has_key(e):
            continue
        else:
            ignore[e] = True
            ignore[f] = True
            r = min(int(master[e][0]), int(master[f][0]))
            m = min(int(master[e][1]), int(master[f][1]))
            p = int(master[e][0]) + int(master[f][0])
            edges[e] = [str(r), str(m), str(p)]
            nodes[x[0]] = users[x[0]]
            nodes[x[1]] = users[x[1]]
    with open(outputJSONname, 'w') as out:
        init = True
        for e in nodes:
            if init:
                init = False
            else:
                out.write('\n')
            out.write('{"type": "node", "uid": "' + e + '", "properties": {"name": "' + nodes[e][0] + '", "tweets": "' + nodes[e][1] + '"}}')
        for e in edges:
            x = e.split(':')
            out.write('\n' + '{"type": "edge", "src": "' + x[0] + '", "dest": "' + x[1] + '", "directionality": "bi", "properties": {"reciprocity": "' + edges[e][0] + '", "mutuality": "' + edges[e][1] + '", "positivity": "' + edges[e][2] + '"}}')

def GephifyReciprocity(inputJSONname, nodeOutputName, edgeOutputName):
    nodes = open(nodeOutputName, 'w')
    edges = open(edgeOutputName, 'w')
    nodes.write("Id,Label,Tweets")
    edges.write("Source,Target,Label,Type,Weight,Mutuality,Positivity")
    with open(inputJSONname, 'r') as file:
        for line in file:
            decoded = json.loads(line.rstrip())
            if decoded["type"] == "node":
                node_Id = decoded["uid"]
                node_Label = decoded["properties"]["name"]
                node_Tweets = decoded["properties"]["tweets"]
                nodes.write('\n' + node_Id + ',' + node_Label + ',' + node_Tweets)
            if decoded["type"] == "edge":
                edge_Source = decoded["src"]
                edge_Target = decoded["dest"]
                edge_Label = edge_Source + " to " + edge_Target
                edge_Type = "Undirected"
                edge_Weight = decoded["properties"]["reciprocity"]
                edge_Mutuality = decoded["properties"]["mutuality"]
                edge_Positivity = decoded["properties"]["positivity"]
                edges.write('\n' + edge_Source + ',' + edge_Target + ',' + edge_Label + ',' + edge_Type + ',' + edge_Weight + ',' + edge_Mutuality + ',' + edge_Positivity)
    nodes.close()
    edges.close()


# MutualityGraphFunctions

def MakeMutualityGraph(graphJSONname, outputJSONname):
    master = {}
    users = {}
    with open(graphJSONname, 'r') as file:
        for line in file:
            decoded = json.loads(line.rstrip())
            for u in decoded["outbound"]:
                if decoded["uid"] != u:
                    if int(decoded["outbound"][u]["times_thanked"]) > 0:
                        master[decoded["uid"] + ':' + u] = [decoded["outbound"][u]["weight"], decoded["outbound"][u]["times_thanked"]]
            users[decoded["uid"]] = [decoded["name"], decoded["properties"]["tweets"]]
    nodes = {}
    edges = {}
    ignore = {}
    for e in master:
        x = e.split(':')
        f = x[1] + ':' + x[0]
        if not master.has_key(f):
            continue
        elif ignore.has_key(e):
            continue
        else:
            ignore[e] = True
            ignore[f] = True
            r = min(int(master[e][0]), int(master[f][0]))
            m = min(int(master[e][1]), int(master[f][1]))
            p = int(master[e][0]) + int(master[f][0])
            edges[e] = [str(r), str(m), str(p)]
            nodes[x[0]] = users[x[0]]
            nodes[x[1]] = users[x[1]]
    with open(outputJSONname, 'w') as out:
        init = True
        for e in nodes:
            if init:
                init = False
            else:
                out.write('\n')
            out.write('{"type": "node", "uid": "' + e + '", "properties": {"name": "' + nodes[e][0] + '", "tweets": "' + nodes[e][1] + '"}}')
        for e in edges:
            x = e.split(':')
            out.write('\n' + '{"type": "edge", "src": "' + x[0] + '", "dest": "' + x[1] + '", "directionality": "bi", "properties": {"reciprocity": "' + edges[e][0] + '", "mutuality": "' + edges[e][1] + '", "positivity": "' + edges[e][2] + '"}}')

def GephifyMutuality(inputJSONname, nodeOutputName, edgeOutputName):
    nodes = open(nodeOutputName, 'w')
    edges = open(edgeOutputName, 'w')
    nodes.write("Id,Label,Tweets")
    edges.write("Source,Target,Label,Type,Weight")
    with open(inputJSONname, 'r') as file:
        for line in file:
            decoded = json.loads(line.rstrip())
            if decoded["type"] == "node":
                node_Id = decoded["uid"]
                node_Label = decoded["properties"]["name"]
                node_Tweets = decoded["properties"]["tweets"]
                nodes.write('\n' + node_Id + ',' + node_Label + ',' + node_Tweets)
            if decoded["type"] == "edge":
                edge_Source = decoded["src"]
                edge_Target = decoded["dest"]
                edge_Label = edge_Source + " to " + edge_Target
                edge_Type = "Undirected"
                edge_Weight = decoded["properties"]["mutuality"]
                edges.write('\n' + edge_Source + ',' + edge_Target + ',' + edge_Label + ',' + edge_Type + ',' + edge_Weight)
    nodes.close()
    edges.close()

MakeMutualityGraph("atgraph.json", "mutuality.json")
GephifyMutuality("mutuality.json", "mnodes.json", "medges.json")