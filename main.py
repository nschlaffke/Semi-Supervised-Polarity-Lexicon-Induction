# First time, uncomment this to install wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import igraph as ig

import generateGraph
import loadWordNet

# possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
words_synsets = list(wn.all_synsets(wn.ADJ))

lemmas = loadWordNet.getAllLemmas(words_synsets)

graph = generateGraph.createGraph(loadWordNet.getNames(lemmas))

for lemma in lemmas:
    base_lemma_name = loadWordNet.getName(lemma)

    synonyms = loadWordNet.findSynonymsLemma(lemma)

    for synonym_name in loadWordNet.getNames(synonyms):
        generateGraph.addEdgeIf(graph, base_lemma_name, synonym_name)

min_cut = generateGraph.getMinCut(graph, 'good', 'bad')

print(min_cut[0])
print(min_cut[1])