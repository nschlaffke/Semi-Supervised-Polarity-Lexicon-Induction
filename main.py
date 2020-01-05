# First time, uncomment this to install wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import igraph as ig

import generateGraph
import loadWordNet
import labelProp

from sklearn.externals.joblib import Memory

memory = Memory(cachedir='./cache', verbose=0)
# possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB

@memory.cache
def get_graph():
    words_synsets = list(wn.all_synsets(wn.ADJ))

    lemmas = loadWordNet.getAllLemmas(words_synsets)[:100] # TODO remove word limit

    graph = generateGraph.createGraph(loadWordNet.getNames(lemmas))

    for lemma in lemmas:
        base_lemma_name = loadWordNet.getName(lemma)

        synonyms = loadWordNet.findSynonymsLemma(lemma)

        for synonym_name in loadWordNet.getNames(synonyms):
            generateGraph.addEdgeIf(graph, base_lemma_name, synonym_name)
    
    graph.es['weight'] = [1]*len(graph.get_edgelist()) # TODO remove dummy way of adding weights
    return graph

graph = get_graph()

label_prop = labelProp.performLabelProp(graph, ['abaxial'], ['abducent'])