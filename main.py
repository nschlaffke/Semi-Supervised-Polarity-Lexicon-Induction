# First time, uncomment this to install wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import igraph as ig
import numpy as np

import graphFunctions
import generateGraph
import score
import helper
import labelProp
import minCut
import newScore
import graphPlots
import loadWordNet


def performMinCut(graph, real_positives, real_negatives, fscores, isSynsetGraph):

    good = loadWordNet.convertIf(["good"], isSynsetGraph)
    bad = loadWordNet.convertIf(["bad"], isSynsetGraph)

    if(isSynsetGraph):
        # this only works for graphs that contain adjectives
        good = ["good.a.01"]
        bad = ["bad.a.01"]

    # Use the simplest min cut
    (predicted_positives, predicted_negatives, cluster) = minCut.getSimpleMinCut(
        graph, good, bad)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)

    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(newScore.getScores("Simple min-cut", real_positives, real_negatives,
                       predicted_positives, predicted_negatives))
    
    # Try to improve min-cut, adding a high capacity to adjacent edges, so they don't get cut
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonNeighboursEdgesMinCut(
        graph, good, bad)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(newScore.getScores("Non Neighbours min-cut", real_positives, real_negatives,
                       predicted_positives, predicted_negatives))

    NUMBER_OF_SEEDS = 50
    negative_seed = loadWordNet.convertIf(np.random.choice(real_negatives, NUMBER_OF_SEEDS), isSynsetGraph)
    positive_seed = loadWordNet.convertIf(np.random.choice(real_positives, NUMBER_OF_SEEDS), isSynsetGraph)

    # Try to improve min-cut, adding a subgraph of connected edges so they don't get cut
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonSubgraphEdgesMinCut(
        graph, positive_seed, negative_seed)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(newScore.getScores("Non Subgraph min-cut", real_positives, real_negatives, predicted_positives,
                                         predicted_negatives))
    
    # Add both formulas
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonSubgraphNonNeighboursEdgesMinCut(
        graph, positive_seed, negative_seed)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(newScore.getScores("Non Neig-Sub min-cut", real_positives, real_negatives, predicted_positives,
                                         predicted_negatives))


def performLabelProp(graph, real_positives, real_negatives, fscores, isSynsetGraph):
    NUMBER_OF_SEEDS = 30
    print("Label propagation")
    negative_seed = np.random.choice(real_negatives, NUMBER_OF_SEEDS)
    positive_seed = np.random.choice(real_positives, NUMBER_OF_SEEDS)

    (predicted_positives, predicted_negatives) = labelProp.performLabelProp(
        graph,
        loadWordNet.convertIf(negative_seed, isSynsetGraph),
        loadWordNet.convertIf(positive_seed, isSynsetGraph))

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(newScore.getScores("LP", real_positives, real_negatives,
                       predicted_positives, predicted_negatives))

# MAIN

def performAllTests(graph_name, synsetGraph = False):

    graph = getattr(generateGraph, graph_name)()
    graph = graphFunctions.removeDisconnectedVertices(graph)

    if(not synsetGraph):
        used_dictionary = graphFunctions.getVerticesNames(
            graph, range(len(graph.vs())))
        
        real_positives = [word for word in helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
                        if word in used_dictionary]
        real_negatives = [word for word in helper.readCsvWords("./LMDictCsv/LMDnegative.csv")
                        if word in used_dictionary]
    else:
        real_positives = helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
        real_negatives = helper.readCsvWords("./LMDictCsv/LMDnegative.csv")

    fscores = []

    performMinCut(graph, real_positives, real_negatives, fscores, synsetGraph)
    performLabelProp(graph, real_positives, real_negatives, fscores, synsetGraph)


performAllTests("getFullADJADVSynsetGraph", True)