# First time, uncomment this to install wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import igraph as ig

import graphFunctions
import generateGraph

graph = generateGraph.getSmallADJGraph()
graphFunctions.getMinCut(graph, "good", "bad")
# label_prop = labelProp.performLabelProp(graph, ['abaxial'], ['abducent'])