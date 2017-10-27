# natural-helpers
 This should build all the revelant @-graphs from a JSON file of tweets and store them in pkl files.
It also creates some badly formatted statistics (in a file called graph_stats.txt)
In the Makefile ou will need to change the line below to point to the json file you are using 
(Mine is in a directory called trowser, which you probably don't have in your filesystem)

JSON_FILE=../trowser/oneyear.json

Save the Makefile and run:

> make

To rerun, first type:

> rm *.pkl

You may have to play around with environment settings to get this to
work. Here are my environment setting commands that I run before running the progrma
export PYTHONPATH=/usr/local/lib/python2.7/site-packages/;
export PYTHONIOENCODING=utf-8;

Here is a brief dictionary of the graphs generated. There are others
generated too:

* R: at_graph.pkl
* M: thank_you_graph.pkl
* BIN: Not generated
* H: thank_you_no_binaries.pkl
* CH: thank_you_no_onesies.pkl
* TH: Not generated
