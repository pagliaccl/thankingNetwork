# This makefile should build all the revelant @-graphs from a JSON file of tweets and store them in pkl files.
# It also creates some badly formatted statistics (in a file called graph_stats.txt)
# You will need to change the line below to point to the json file you are using 
# (Mine is in a directory called trowser, which you probably don't have in your filesystem)

JSON_FILE=../trowser3/oneyear.json

# Once you enter this line, the command to run (where the prompt is ">") is simply:

# > make

# To rerun, first type:

#> rm *.pkl

# You may have to play around with environment settings to get this to work. Here are my environment setting commands that I run before running the progrma
#export PYTHONPATH=/usr/local/lib/python2.7/site-packages/;
#export PYTHONIOENCODING=utf-8;

# Here is a brief dictionary of the graphs generated. There are others generated too.
# R: at_graph.pkl
# M: thank_you_graph.pkl
# BIN: Not generated
# H: thank_you_no_binaries.pkl
# CH: thank_you_no_onesies.pkl
# TH: Not generated
#
# The graphs that are not generated can easily be derived using the pkl files that are created by this process.

all: 	thank_you_graph.pkl graph_stats.txt

thank_you_multidigraph.pkl:	at_multidigraph.pkl make_thank_you_graph.py
	 python make_thank_you_graph.py at_multidigraph.pkl 

at_multidigraph.pkl: make_at_multidigraph.py
	python make_at_multidigraph.py ${JSON_FILE}

thank_you_graph.pkl: at_multidigraph.pkl thank_you_multidigraph.pkl graph_play.py
	python collapse_thank_you_graph.py

thank_you_graph.gexf: thank_you_graph.pkl thank_you_digraph.pkl
	python  make_gexf.py

at_recip_multidigraph.pkl: at_multidigraph.pkl make_at_recip_multidigraph.py
	python make_at_recip_multidigraph.py at_multidigraph.pkl	

at_graph.pkl: at_recip_multidigraph.pkl
	python collapse_at_graph.py

at_no_onesies.pkl: at_graph.pkl
	python remove_binaries_and_onesies_from_at_graph.py

thank_you_no_onesies.pkl: thank_you_graph.pkl
	python remove_binaries_and_onesies.py

graph_stats.txt: at_graph.pkl at_no_onesies.pkl thank_you_no_onesies.pkl
	python get_graph_stats.py at_graph.pkl > graph_stats.txt	
	python get_graph_stats.py at_no_onesies.pkl >> graph_stats.txt
	python get_graph_stats.py thank_you_graph.pkl >> graph_stats.txt	
	python get_graph_stats.py thank_you_no_binaries.pkl >> graph_stats.txt
	python get_graph_stats.py thank_you_no_onesies.pkl >> graph_stats.txt
	python get_graph_in_multidigraph_stats.py at_graph.pkl thank_you_multidigraph.pkl >> graph_stats.txt	
	python get_graph_in_multidigraph_stats.py at_no_onesies.pkl thank_you_multidigraph.pkl>> graph_stats.txt
	python get_graph_in_multidigraph_stats.py thank_you_graph.pkl thank_you_multidigraph.pkl >> graph_stats.txt	
	python get_graph_in_multidigraph_stats.py thank_you_no_binaries.pkl thank_you_multidigraph.pkl >> graph_stats.txt
	python get_graph_in_multidigraph_stats.py thank_you_no_onesies.pkl thank_you_multidigraph.pkl >> graph_stats.txt
	python get_graph_in_multidigraph_stats.py at_graph.pkl at_multidigraph.pkl >> graph_stats.txt	
	python get_graph_in_multidigraph_stats.py at_no_onesies.pkl at_multidigraph.pkl>> graph_stats.txt
	python get_graph_in_multidigraph_stats.py thank_you_graph.pkl at_multidigraph.pkl >> graph_stats.txt	
	python get_graph_in_multidigraph_stats.py thank_you_no_binaries.pkl at_multidigraph.pkl >> graph_stats.txt
	python get_graph_in_multidigraph_stats.py thank_you_no_onesies.pkl at_multidigraph.pkl >> graph_stats.txt

screen_name-id.pkl:
	python -OO make_name-id_dict.py ${JSON_FILE} screen_name-id.pkl
