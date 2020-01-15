from nltk.corpus import wordnet as wn
from os import path
import igraph as ig
import queue as queueClass

import graphFunctions
import graphPlots
import loadWordNet
import labelProp
import helper

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

def getLemmasGraph(words_synsets):
    lemmas = loadWordNet.getAllLemmas(words_synsets)

    graph = graphFunctions.createGraph(loadWordNet.getNames(lemmas))

    for i, lemma in enumerate(lemmas):
        print (round((i/len(lemmas))*100, 2), end="\r")
        base_lemma_name = loadWordNet.getName(lemma)

        synonyms = loadWordNet.findSynonymsLemma(lemma)

        for synonym_name in loadWordNet.getNames(synonyms):
            graphFunctions.addEdgeIf(graph, base_lemma_name, synonym_name)
    
    return graph

def getSynsetGraph(words_synsets):

    graph = graphFunctions.createGraph(loadWordNet.getNames(words_synsets))

    for i, word_synset in enumerate(words_synsets):
        print (round((i/len(words_synsets))*100, 2), end="\r")
        synonyms = loadWordNet.findRelatedSynsets(word_synset)

        for synonym_name in loadWordNet.getNames(synonyms):
            graphFunctions.addEdgeIf(graph, loadWordNet.getName(word_synset), synonym_name)
    
    return graph

def getAntonymGraph(words_synsets):
    lemmas = loadWordNet.getAllLemmas(words_synsets)

    graph = graphFunctions.createGraph(loadWordNet.getNames(lemmas))

    for i, lemma in enumerate(lemmas):
        print(round((i/len(lemmas))*100, 2), end="\r")
        base_lemma_name = loadWordNet.getName(lemma)

        antonyms = []
        if lemma.antonyms():
            antonyms = [x.name() for x in lemma.antonyms()]

        for synonym_name in antonyms:
            graphFunctions.addEdgeIf(graph, base_lemma_name, synonym_name)

    new_edges = []
    v = graph.vcount()
    return graph

class QueueObject:
  def __init__(self, depth, synset):
    self.depth = depth
    self.synset = synset

def getSynsetsDepth(words_synsets, max_depth, useSynsets = False):

    new_words_synsets = set(words_synsets)
    
    queue = queueClass.Queue()
    for synset in words_synsets:
        queue.put(QueueObject(1, synset))
    
    while(not queue.empty()):
        print (queue.qsize(), end="\r")
        current = queue.get()
        
        if(current.depth > max_depth):
            continue

        if(not useSynsets):
            synonyms = loadWordNet.findSynsetSynonymsSynset(current.synset)
        else:
            synonyms = loadWordNet.findRelatedSynsets(current.synset)

        for synonym in synonyms:
            if(synonym not in new_words_synsets):
                queue.put(QueueObject(current.depth + 1, synonym))
                new_words_synsets.add(synonym)
            
    
    return list(new_words_synsets)

def getSynsetsFromWords(words):
    new_words_synsets = set()
    
    for word in words:
        synsets = loadWordNet.getSynsets(word)
        for synset in synsets:
            new_words_synsets.add(synset)

    return list(new_words_synsets)

    
# Get graph functions
@graphCache
def getFullAdjAdvAntonymGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ)) + list(wn.all_synsets(wn.ADV))
    return getAntonymGraph(words_synsets)

@graphCache
def getFullGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets())
    return getLemmasGraph(words_synsets)

@graphCache
def getFullADJGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ))
    return getLemmasGraph(words_synsets)

@graphCache
def getFullADJADVGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ)) + list(wn.all_synsets(wn.ADV))
    return getLemmasGraph(words_synsets)

@graphCache
def getSmallADJGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ))[:500]
    return getLemmasGraph(words_synsets)

@graphCache
def getValidateOnlyWordsGraph():
    real_positives = helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
    real_negatives = helper.readCsvWords("./LMDictCsv/LMDnegative.csv")

    words_synsets = getSynsetsFromWords(real_negatives + real_positives)
    return getLemmasGraph(words_synsets)

@graphCache
def getGoodBadDepthGraph():
    good = wn.synset('good.a.01')
    bad = wn.synset('bad.a.01')

    words_synsets = getSynsetsDepth([good, bad], 4)
    return getLemmasGraph(words_synsets)

# Synset graphs

@graphCache
def getFullADJADVSynsetGraph():
    # possible word types: ADJ, ADJ_SAT, ADV, NOUN, VERB
    words_synsets = list(wn.all_synsets(wn.ADJ)) + list(wn.all_synsets(wn.ADV)) + [wn.synset('good.a.01')] + [wn.synset('bad.a.01')]
    return getSynsetGraph(words_synsets)

@graphCache
def getGoodBadDepthSynsetGraph():
    good = wn.synset('good.a.01')
    bad = wn.synset('bad.a.01')

    words_synsets = getSynsetsDepth([good, bad], 4, True)
    return getSynsetGraph(words_synsets)
@graphCache
def getFullAdjAdvAntExtGraph():
    raise FileNotFoundError

# Main for tests

if __name__ == "__main__":
    # memory.clear(warn=False)
    # g = getFullGraph()
    # ig.plot(g)
    # print(graphFunctions.shortestPath(g, "good", "bad"))
    # graphPlots.plotWithLabels(g.subgraph(graphFunctions.shortestPath(g, "good", "bad")[0]))
    # storeGraph("fullAdjGraph", g)

    # good = wn.synset('good.a.01')
    # synsets = getSynsetsDepth([good], 1)
    # print(helper.unique(loadWordNet.getNames(synsets)))
    # g = getLemmasGraph(synsets)
    # graphPlots.plotBigKKLayoutWithLabels(g)

    g = getGoodBadDepthGraph()
    graphPlots.plotBigKKLayoutWithLabels(g)

    g = getGoodBadDepthSynsetGraph()
    graphPlots.plotBigKKLayoutWithLabels(g)
