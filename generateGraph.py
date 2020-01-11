from nltk.corpus import wordnet as wn
from os import path
import igraph as ig

import graphFunctions
import graphPlots
import loadWordNet
import labelProp

from sklearn.externals.joblib import Memory
memory = Memory(location='./cache', verbose=0)

# Graph cache functions
def graphPath(name):
    return "graphs/" + name + ".graphml"

def storeGraph(name, g):
    g.save(graphPath(name))
    
def readGraph(name):
    if(path.exists(graphPath(name))):
        return ig.load(graphPath(name))
    return None

def graphCache(function):
    def new_function():
        stored_graph = readGraph(function.__name__)
        if(stored_graph != None):
            return stored_graph
        g = function()
        storeGraph(function.__name__, g)
        return g

    return new_function

 # Graph functions   

def getGraph(words_synsets):
    lemmas = loadWordNet.getAllLemmas(words_synsets)

    graph = graphFunctions.createGraph(loadWordNet.getNames(lemmas))

    for lemma in lemmas:
        base_lemma_name = loadWordNet.getName(lemma)

        synonyms = loadWordNet.findSynonymsLemma(lemma)

        for synonym_name in loadWordNet.getNames(synonyms):
            graphFunctions.addEdgeIf(graph, base_lemma_name, synonym_name)
    
    graph.es()['weight'] = [1]*len(graph.get_edgelist()) # TODO remove dummy way of adding weights
    return graph

@graphCache
def getFullADJGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ))
    return getGraph(words_synsets)

@graphCache
def getSmallADJGraph():
    name = "smallAdjGraph"
    storedGraph = readGraph(name)
    if(storedGraph != None):
        return storedGraph

    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ))[:500]
    return getGraph(words_synsets)


# Main for tests

if __name__ == "__main__":
    # memory.clear(warn=False)
    g = getFullADJGraph()
    # ig.plot(g)
    # print(graphFunctions.shortestPath(g, "good", "bad"))
    # graphPlots.plotWithLabels(g.subgraph(graphFunctions.shortestPath(g, "good", "bad")[0]))
    # storeGraph("fullAdjGraph", g)