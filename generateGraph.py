from nltk.corpus import wordnet as wn
import igraph as ig

import graphFunctions
import graphPlots
import loadWordNet
import labelProp

from sklearn.externals.joblib import Memory
memory = Memory(location='./cache', verbose=0)

def getADJGraph(words_synsets):
    lemmas = loadWordNet.getAllLemmas(words_synsets)

    graph = graphFunctions.createGraph(loadWordNet.getNames(lemmas))

    for lemma in lemmas:
        base_lemma_name = loadWordNet.getName(lemma)

        synonyms = loadWordNet.findSynonymsLemma(lemma)

        for synonym_name in loadWordNet.getNames(synonyms):
            graphFunctions.addEdgeIf(graph, base_lemma_name, synonym_name)
    
    graph.es()['weight'] = [1]*len(graph.get_edgelist()) # TODO remove dummy way of adding weights
    return graph

@memory.cache
def getFullADJGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ))
    return getADJGraph(words_synsets)

    

@memory.cache
def getSmallADJGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ))[:500]
    return getADJGraph(words_synsets)

if __name__ == "__main__":
    # memory.clear(warn=False)
    g = getFullADJGraph()
    # ig.plot(g)
    print(graphFunctions.shortestPath(g, "good", "bad"))
    graphPlots.plotWithLabels(g.subgraph(graphFunctions.shortestPath(g, "good", "bad")[0]))