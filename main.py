# First time, uncomment this to install wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import igraph as ig

import graphFunctions
import generateGraph

graph = generateGraph.getFullADJGraph()
result = graphFunctions.getMinCut(graph, "good", "bad")
print(len(result[0]))
print(len(result[1]))

# label_prop = labelProp.performLabelProp(graph, ['abaxial'], ['abducent'])